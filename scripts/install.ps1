# Установщик для Windows
Write-Host "=== Network Scanner Installer ===" -ForegroundColor Cyan

# Проверяем Python
try {
    $pythonVersion = python --version
    Write-Host "Python найден: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python не найден! Установите Python 3.8 или выше." -ForegroundColor Red
    Write-Host "Скачайте с: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Проверяем/устанавливаем uv
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "UV найден" -ForegroundColor Green
} else {
    Write-Host "Устанавливаю UV..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | iex
}

# Создаем виртуальную среду
Write-Host "Создаю виртуальную среду..." -ForegroundColor Yellow
uv venv

# Активируем среду
Write-Host "Активирую среду..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Устанавливаем пакет
Write-Host "Устанавливаю network-scanner..." -ForegroundColor Yellow
uv pip install -e .

Write-Host "`nУстановка завершена!" -ForegroundColor Green
Write-Host "Используйте команды:" -ForegroundColor Cyan
Write-Host "  network-scanner           - запуск сканера" -ForegroundColor White
Write-Host "  network-scanner --help    - справка" -ForegroundColor White
Write-Host "  scripts\start.bat         - запуск через BAT файл" -ForegroundColor White

Write-Host "`nНажмите Enter для выхода..." -ForegroundColor Gray
Read-Host