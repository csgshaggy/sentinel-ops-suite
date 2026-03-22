. "$PSScriptRoot/banner.ps1"

Write-Host "[ENV] Python version:"
python --version
Write-Host ""

Write-Host "[ENV] Pip packages:"
pip list
Write-Host ""

Write-Host "[ENV] Git status:"
git status -s
Write-Host ""

Write-Host "[ENV] Disk usage:"
Get-PSDrive C | Format-Table
Write-Host ""

Write-Host "[ENV] Memory usage:"
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize
