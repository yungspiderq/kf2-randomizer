param(
  [Parameter(Mandatory=$true)][string] $ExePath,
  [Parameter(Mandatory=$true)][string] $Label
)
$ErrorActionPreference = 'Stop'
$exe = (Resolve-Path $ExePath).Path
$marker = Join-Path $env:RUNNER_TEMP "kf2-startup-$Label.txt"
Remove-Item -LiteralPath $marker -Force -ErrorAction SilentlyContinue
$argline = '--startup-smoke-test "' + $marker + '"'
$proc = Start-Process -FilePath $exe -ArgumentList $argline -PassThru
if (!$proc.WaitForExit(90000)) {
  try { $proc.Kill() } catch {}
  throw "$Label packaged EXE startup timed out"
}
if ($proc.ExitCode -ne 0) { throw "$Label startup failed (exit $($proc.ExitCode))" }
if (!(Test-Path -LiteralPath $marker)) { throw "$Label missing Python/Qt startup marker" }
$expected = 'KF2_RANDOMIZER_STARTUP_OK v' + (Get-Content VERSION.txt -Raw).Trim()
$actual = (Get-Content -LiteralPath $marker -Raw).Trim()
if ($actual -ne $expected) { throw "$Label startup marker unexpected: $actual" }
Write-Host "Packaged $Label startup passed: $actual"
