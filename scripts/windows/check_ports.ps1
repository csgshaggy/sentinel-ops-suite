param(
    [string[]]$Ports = @("8000","8080","5000","3000")
)

. "$PSScriptRoot/banner.ps1"

Write-Host "[PORTS] Checking ports: $($Ports -join ', ')"
Write-Host ""

foreach ($port in $Ports) {
    $result = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($result) {
        Write-Host "[BUSY] Port $port is in use:"
        $result | Format-Table -AutoSize
    } else {
        Write-Host "[FREE] Port $port is available"
    }
}
