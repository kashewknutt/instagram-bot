# Windows bootstrap for the social-agent platform.
# Usage:
#   .\setup.ps1                  # interactive
#   .\setup.ps1 -Profile fleet
#   .\setup.ps1 -Profile instagram

param(
    [ValidateSet("core", "instagram", "fleet")]
    [string]$Profile = "",
    [switch]$NoInstall
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3.11+ is required on PATH."
}

python -m pip install --user pyyaml | Out-Null

$argsList = @()
if ($Profile) { $argsList += @("--profile", $Profile) }
else { $argsList += "-i" }
if ($NoInstall) { $argsList += "--no-install" }

python .\setup.py @argsList

Write-Host ""
Write-Host "Open this folder in Cursor:" -ForegroundColor Cyan
Write-Host "  $PSScriptRoot"
Write-Host ""
Write-Host "Then start Fleet Control (if you chose fleet):" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  python -m orchestrator_app.main"
Write-Host "  # http://127.0.0.1:7400"
