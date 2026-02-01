@echo off
chcp 65001 >nul
echo ========================================
echo    Network Scanner
echo ========================================
echo.

REM Переходим в корень проекта
cd /d "%~dp0.."

REM Проверяем uv
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo Ошибка: uv не установлен!
    echo Установите: powershell -c "irm https://astral.sh/uv/install.ps1 ^| iex"
    pause
    exit /b 1
)

REM Создаем виртуальную среду если нет
if not exist ".venv\Scripts\activate.bat" (
    echo [1/4] Создаю виртуальную среду...
    uv venv
)

REM Активируем среду
call .venv\Scripts\activate.bat

REM Устанавливаем пакет в режиме разработки
echo [2/4] Устанавливаю network-scanner...
uv pip install -e .

echo [3/4] Запускаю сканер...
echo.

REM Запускаем через установленный скрипт
network-scanner --save

echo.
echo ========================================
echo Сканирование завершено!
echo Для повторного запуска введите: network-scanner
echo ========================================
echo.
pause