# start.ps1
Write-Host "=== Network Scanner ===" -ForegroundColor Cyan
Write-Host ""

# Переходим в корень проекта
Set-Location -Path "$PSScriptRoot\.."

# Проверяем наличие виртуальной среды
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    uv venv
}

# Активируем среду
& ".venv\Scripts\Activate.ps1"

# Устанавливаем в режиме разработки
Write-Host "Installing network-scanner..." -ForegroundColor Gray
uv pip install -e .

Write-Host "`nStarting scanner..." -ForegroundColor Green
Write-Host "Usage: network-scanner [--network NETWORK] [--save]" -ForegroundColor Yellow
Write-Host ""

# Запускаем сканер
network-scanner --save

Write-Host "`nScan completed!" -ForegroundColor Cyan
Write-Host "Results saved in results/ folder" -ForegroundColor Gray
Write-Host "`nPress Enter to exit..." -ForegroundColor DarkGray
Read-Host