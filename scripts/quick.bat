@echo off
chcp 65001 >nul
echo ========================================
echo    Network Scanner - Быстрый запуск
echo ========================================
echo.

cd /d "%~dp0.."

REM Проверяем виртуальную среду
if not exist ".venv\Scripts\activate.bat" (
    echo Ошибка: Виртуальная среда не найдена!
    echo Запустите scripts\start.bat для настройки
    pause
    exit /b 1
)

REM Активируем среду
call .venv\Scripts\activate.bat

REM Запускаем сканер
echo Запускаю network-scanner...
echo.
network-scanner --save

echo.
pause