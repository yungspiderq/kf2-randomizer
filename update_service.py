"""Verified, opt-in updates for the standalone Windows Qt application.

Release metadata comes only from the project's official GitHub repository. Updates
are offered only from stable GitHub Releases and checked by SHA-256 before use.
This module deliberately has no Qt dependency so it can be tested separately.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Callable
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

REPOSITORY = "yungspiderq/kf2-randomizer"
API_URL = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
RELEASES_URL = f"https://github.com/{REPOSITORY}/releases"
ASSET_NAME = "KF2-Randomizer.exe"
MAX_SIZE = 350 * 1024 * 1024
CHUNK_SIZE = 256 * 1024
USER_AGENT = "KF2-Randomizer-Updater/1.0"


class UpdateError(Exception):
    """Something prevented a safe update."""


class UpdateCancelled(UpdateError):
    """Download was cancelled by the user."""


@dataclass(frozen=True)
class Release:
    version: str
    url: str
    asset_url: str
    checksum: str
    size: int
    notes: str = ""


def version_tuple(text: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", text.strip(), re.ASCII)
    if not match:
        raise UpdateError(f"Некорректная версия релиза: {text!r}")
    return tuple(int(x) for x in match.groups())  # type: ignore[return-value]


def _get(url: str, *, limit: int) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urlopen(req, timeout=15) as response:
        data = response.read(limit + 1)
        if len(data) > limit:
            raise UpdateError("Ответ GitHub слишком большой")
        return data


def _secure_asset_url(url: str, name: str) -> bool:
    p = urlsplit(url)
    return (
        p.scheme == "https" and p.netloc == "github.com"
        and p.path.startswith(f"/{REPOSITORY}/releases/download/")
        and p.path.endswith("/" + name) and not p.username and not p.password
        and not p.query and not p.fragment
    )


def fetch_latest(current_version: str) -> Release | None:
    """Return a newer stable release, or None if already up to date.

    The checksum must be provided by GitHub's asset digest or our published
    .sha256 sidecar. If neither exists, the release isn't offered for install.
    """
    try:
        payload = json.loads(_get(API_URL, limit=128 * 1024))
    except HTTPError as exc:
        if exc.code == 404:
            raise UpdateError("На GitHub пока нет опубликованных релизов") from exc
        raise UpdateError(f"GitHub вернул ошибку HTTP {exc.code}") from exc
    except (OSError, ValueError) as exc:
        raise UpdateError(f"Не удалось проверить обновления: {exc}") from exc

    if not isinstance(payload, dict) or payload.get("draft") or payload.get("prerelease"):
        raise UpdateError("GitHub не вернул стабильный релиз")
    version = str(payload.get("tag_name", ""))
    if version_tuple(version) <= version_tuple(current_version):
        return None

    assets = payload.get("assets") or []
    asset = next((a for a in assets if isinstance(a, dict) and a.get("name") == ASSET_NAME), None)
    if asset is None:
        raise UpdateError("В релизе нет KF2-Randomizer.exe")
    asset_url = str(asset.get("browser_download_url", ""))
    if not _secure_asset_url(asset_url, ASSET_NAME):
        raise UpdateError("GitHub вернул неожиданный адрес исполняемого файла")
    size = asset.get("size")
    if not isinstance(size, int) or not (10_000 <= size <= MAX_SIZE):
        raise UpdateError("Некорректный размер файла обновления")

    digest = str(asset.get("digest") or "")
    checksum = digest[7:].lower() if re.fullmatch(r"sha256:[0-9a-fA-F]{64}", digest) else ""
    if not checksum:
        checksum_asset = next((a for a in assets if isinstance(a, dict) and a.get("name") == ASSET_NAME + ".sha256"), None)
        if not checksum_asset:
            raise UpdateError("В релизе отсутствует контрольная сумма SHA-256")
        sum_url = str(checksum_asset.get("browser_download_url", ""))
        if not _secure_asset_url(sum_url, ASSET_NAME + ".sha256"):
            raise UpdateError("Некорректный адрес SHA-256")
        try:
            content = _get(sum_url, limit=1024).decode("ascii").strip()
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            raise UpdateError(f"Не удалось получить SHA-256: {exc}") from exc
        match = re.fullmatch(r"([0-9a-fA-F]{64})(?:\s+\*?KF2-Randomizer\.exe)?", content)
        if not match:
            raise UpdateError("Неверный формат SHA-256 в релизе")
        checksum = match.group(1).lower()

    release_url = str(payload.get("html_url", ""))
    if not release_url.startswith(RELEASES_URL + "/tag/"):
        release_url = RELEASES_URL
    return Release(
        version=version.lstrip("v"),
        url=release_url,
        asset_url=asset_url,
        checksum=checksum,
        size=size,
        notes=str(payload.get("body") or "")[:450],
    )


def download_update(
    release: Release,
    progress: Callable[[int, int], None] | None = None,
    cancelled: Callable[[], bool] | None = None,
) -> Path:
    """Download and verify a release into a unique temporary directory."""
    if not _secure_asset_url(release.asset_url, ASSET_NAME):
        raise UpdateError("Источник обновления недопустим")
    if not re.fullmatch(r"[0-9a-f]{64}", release.checksum):
        raise UpdateError("Невозможно проверить SHA-256 обновления")

    temp_dir = Path(tempfile.mkdtemp(prefix="kf2-randomizer-update-"))
    destination = temp_dir / ASSET_NAME
    total = 0
    digest = hashlib.sha256()
    req = Request(release.asset_url, headers={"User-Agent": USER_AGENT, "Accept": "application/octet-stream"})
    try:
        with urlopen(req, timeout=45) as response, destination.open("wb") as output:
            while True:
                if cancelled and cancelled():
                    raise UpdateCancelled("Загрузка отменена")
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_SIZE or total > release.size:
                    raise UpdateError("Размер загружаемого файла превышает ожидаемый")
                output.write(chunk)
                digest.update(chunk)
                if progress:
                    progress(total, release.size)
        if total != release.size:
            raise UpdateError("Файл обновления загружен не полностью")
        if digest.hexdigest() != release.checksum:
            raise UpdateError("Контрольная сумма SHA-256 не совпадает — обновление отменено")
        with destination.open("rb") as binary:
            if binary.read(2) != b"MZ":
                raise UpdateError("Загруженный файл не является Windows EXE")
        return destination
    except Exception:
        destination.unlink(missing_ok=True)
        try:
            temp_dir.rmdir()
        except OSError:
            pass
        raise


def _ps_literal(path: str) -> str:
    return "'" + path.replace("'", "''") + "'"


def launch_replace_and_restart(downloaded_exe: Path) -> None:
    """Start a detached Windows updater that waits for us to exit.

    The replacement is only attempted for PyInstaller-frozen Windows builds;
    Python source runs must never overwrite python.exe.
    """
    if os.name != "nt" or not getattr(sys, "frozen", False):
        raise UpdateError("Автоматическая установка работает только в собранной Windows EXE-версии")
    target = Path(sys.executable).resolve()
    if target.name.lower() != ASSET_NAME.lower():
        raise UpdateError("Имя запущенной программы не соответствует файлу обновления")
    downloaded_exe = downloaded_exe.resolve(strict=True)
    if not downloaded_exe.is_file():
        raise UpdateError("Загруженное обновление не найдено")
    # This is only executed after the user confirms the update. Use an encoded
    # PowerShell command so paths with spaces and special symbols are handled.
    ps_script = f"""
$ErrorActionPreference = 'Stop'
try {{
  Wait-Process -Id {os.getpid()} -Timeout 90 -ErrorAction SilentlyContinue
}} catch {{}}
Start-Sleep -Milliseconds 600
$source = {_ps_literal(str(downloaded_exe))}
$target = {_ps_literal(str(target))}
try {{
  Copy-Item -LiteralPath $source -Destination $target -Force -ErrorAction Stop
  Start-Process -FilePath $target
  Remove-Item -LiteralPath $source -Force -ErrorAction SilentlyContinue
}} catch {{
  Add-Type -AssemblyName PresentationFramework
  [System.Windows.MessageBox]::Show('Не удалось установить обновление. Проверьте права записи в папку программы.', 'KF2 Randomizer')
}}
"""
    encoded = base64.b64encode(ps_script.encode("utf-16-le")).decode("ascii")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.Popen(
        ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-EncodedCommand", encoded],
        creationflags=flags,
        close_fds=True,
    )