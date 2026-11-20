"""Fast, offline tests for the secure GitHub update flow."""
import hashlib
import io
import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from update_service import (
    ASSET_NAME, API_URL, Release, UpdateCancelled, UpdateError,
    _secure_asset_url, download_update, fetch_latest, version_tuple,
)

URL = "https://github.com/yungspiderq/kf2-randomizer/releases/download/v0.5.0/KF2-Randomizer.exe"
CHECKSUM_URL = URL + ".sha256"
DATA = b"MZ" + b"example-safe-update-data" * 700
DIGEST = hashlib.sha256(DATA).hexdigest()


class Tests(TestCase):
    def test_version(self):
        self.assertLess(version_tuple("v0.4.0"), version_tuple("0.4.1"))
        self.assertLess(version_tuple("0.4.9"), version_tuple("0.5.0"))
        with self.assertRaises(UpdateError):
            version_tuple("v0.4.0-beta")

    def test_asset_url_rules(self):
        self.assertTrue(_secure_asset_url(URL, ASSET_NAME))
        self.assertFalse(_secure_asset_url(URL.replace("github.com", "github.com.evil.org"), ASSET_NAME))
        self.assertFalse(_secure_asset_url(URL.replace("https", "http"), ASSET_NAME))
        self.assertFalse(_secure_asset_url("https://evil.org/KF2-Randomizer.exe", ASSET_NAME))

    def test_release_when_newer(self):
        payload = {"tag_name": "v0.5.0", "draft": False, "prerelease": False,
                   "html_url": "https://github.com/yungspiderq/kf2-randomizer/releases/tag/v0.5.0",
                   "body": "Update improvements",
                   "assets": [{"name": ASSET_NAME, "browser_download_url": URL, "digest": "sha256:" + DIGEST, "size": len(DATA)}]}
        with patch("update_service._get", return_value=json.dumps(payload).encode()):
            release = fetch_latest("0.4.0")
            self.assertEqual(release.version, "0.5.0")
            self.assertEqual(release.checksum, DIGEST)
            self.assertIsNone(fetch_latest("0.5.0"))

    def test_release_checksum_sidecar(self):
        payload = {"tag_name": "v0.5.0", "assets": [
            {"name": ASSET_NAME, "browser_download_url": URL, "size": len(DATA)},
            {"name": ASSET_NAME + ".sha256", "browser_download_url": CHECKSUM_URL}]}
        def fake_get(url, *, limit):
            return json.dumps(payload).encode() if url == API_URL else (DIGEST + "  " + ASSET_NAME).encode()
        with patch("update_service._get", side_effect=fake_get):
            self.assertEqual(fetch_latest("0.4.0").checksum, DIGEST)

    def test_download_and_verify(self):
        release = Release("0.5.0", "", URL, DIGEST, len(DATA))
        with patch("update_service.urlopen", return_value=io.BytesIO(DATA)):
            path = download_update(release)
        self.assertEqual(path.read_bytes(), DATA)
        path.unlink()
        path.parent.rmdir()

    def test_reject_wrong_digest(self):
        release = Release("0.5.0", "", URL, "0" * 64, len(DATA))
        with patch("update_service.urlopen", return_value=io.BytesIO(DATA)):
            with self.assertRaisesRegex(UpdateError, "SHA-256"):
                download_update(release)

    def test_reject_cancelled(self):
        release = Release("0.5.0", "", URL, DIGEST, len(DATA))
        with patch("update_service.urlopen", return_value=io.BytesIO(DATA)):
            with self.assertRaises(UpdateCancelled):
                download_update(release, cancelled=lambda: True)