param(
    [string[]]$Ports = @("8000","8080","5000","3000")
)

. "$PSScriptRoot/banner.ps1"

Write-Host "[KILL] Attempting to free ports: $($Ports -join ', ')"
Write-Host ""

foreach ($port in $Ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connections) {
        foreach ($conn in $connections) {
            Write-Host "[KILL] Killing PID $($conn.OwningProcess) on port $port"
            Stop-Process -Id $conn.OwningProcess -Force
        }
    } else {
        Write-Host "[OK] Port $port already free"
    }
}
