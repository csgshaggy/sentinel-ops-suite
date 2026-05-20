. "$PSScriptRoot/banner.ps1"

Write-Host "[DOCTOR] Running environment diagnostics..."
Write-Host ""

Write-Host "[CHECK] Python version:"
python --version
Write-Host ""

Write-Host "[CHECK] Pip packages:"
pip list | Select-Object -First 20
Write-Host ""

Write-Host "[CHECK] Git branch:"
git rev-parse --abbrev-ref HEAD
Write-Host ""

Write-Host "[CHECK] Uncommitted changes:"
git status -s
Write-Host ""

Write-Host "[CHECK] Open ports:"
Get-NetTCPConnection | Select-Object LocalPort,State,OwningProcess | Format-Table -AutoSize
Write-Host ""

Write-Host "[DOCTOR] Done."
