# Network Scanner 🔍

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## English

A fast Python tool for discovering web interfaces in local networks. Perfect for finding routers, repeaters, IoT devices, and other network equipment.

**Real-World Proven**: Successfully found a "lost" Xiaomi router with forgotten IP address!

### 🌟 Features

- 🚀 **Fast multithreaded scanning** – scans entire /24 network in seconds
- 🔍 **Automatic router detection** – identifies routers and repeaters with smart keyword matching
- 🌐 **Multi-encoding support** – handles UTF-8, GBK, GB2312 for international devices
- 📊 **Smart analysis** – extracts page titles, server info, and content types
- 💾 **Export results** – saves to JSON and text formats with timestamps
- 🎨 **Colored console output** – easy-to-read results with emoji indicators
- ⚡ **UV integration** – faster dependency management than pip
- 🐧 **Cross-platform** – works on Windows, Linux, macOS
- 🧪 **Tested** – comprehensive test suite with 95% coverage

### 📖 The Story Behind This Tool

This project was born from a **real-world problem**: A user had a Xiaomi router configured with a static IP address years ago and forgot it. The router was working as a repeater in a pfSense-managed network, but needed configuration updates.

**The Challenge**: Find the router's IP address without resetting it to factory defaults.

**The Solution**: `network-scanner` was created. It scanned the network, found an unknown device with garbled text `å°ç±³è·¯ç±å¨`, fixed the Chinese encoding, and revealed it was actually `小米路由器` (Xiaomi Router) at `192.168.3.86`!

**Mission Accomplished**: The router was found, settings were updated, and the tool was proven effective in real conditions.

### 🚀 Quick Start

#### Installation with UV (Recommended)

    # Install UV if you don't have it
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # or on Windows:
    # irm https://astral.sh/uv/install.ps1 | iex

    # Clone and install
    git clone https://github.com/zedraider/network-scanner.git
    cd network-scanner
    uv sync

    # Or install globally
    uv pip install git+https://github.com/zedraider/network-scanner.git

#### Basic Usage

    # Scan default network (192.168.1.0/24)
    network-scanner

    # Scan specific network
    network-scanner --network 192.168.0.0/24

    # Save results to files
    network-scanner --save

    # Check additional ports
    network-scanner --ports 80,443,8080,8443,8888

    # Get help
    network-scanner --help

### 📋 Examples

Find All Web Interfaces

    network-scanner --network 192.168.1.0/24 --save

Search for Routers with Specific Ports

    network-scanner --ports 80,81,82,443,8080,8081,8443,8888 --save

Quick Windows Launch
Double-click `scripts/start.bat` or run:

    .\scripts\start.bat

### 🖥️ Output Example

    🚀 ROUTER! Web interface found:
      IP:        192.168.3.86
      Port:      80
      URL:       http://192.168.3.86:80
      Status:    200
      Title:     小米路由器
      Server:    nginx
      Size:      1760 bytes
      Type:      text/html

### 🎯 Use Cases

- ✅ Find unknown devices in your network
- ✅ Discover router IP when you forget it
- ✅ Inventory network equipment
- ✅ Security audits – find exposed web interfaces
- ✅ Network troubleshooting
- ✅ IoT device discovery
- ✅ Home lab management

### 🛠️ Advanced Features

#### Python API

    from network_scanner import NetworkScanner

    # Create scanner with custom settings
    scanner = NetworkScanner(
        network="192.168.1.0/24",
        timeout=3,
        threads=30
    )

    # Add custom ports
    scanner.common_ports.extend([81, 82, 8001])

    # Run scan
    results = scanner.scan_network()

    # Save results
    scanner.save_results()

#### Custom Scripts

Check out the `scripts/` directory:

- `start.bat` – Windows launcher
- `start.ps1` – PowerShell launcher
- `investigate_device.py` – Detailed device investigation
- `final_report.py` – Generate summary reports

### 📁 Project Structure

    network-scanner/
    ├── src/network_scanner/   # Source code
    │   ├── scanner.py         # Main scanner class
    │   ├── cli.py             # Command-line interface
    │   └── __init__.py
    ├── tests/                 # Unit tests (36 tests, 95% coverage)
    ├── examples/              # Usage examples
    ├── scripts/               # Helper scripts
    ├── docs/                  # Documentation
    ├── .github/workflows/     # CI/CD pipelines
    └── results/               # Scan results (gitignored)

### 🧪 Testing

    # Run all tests
    pytest tests/

    # Run with coverage
    pytest --cov=src tests/

    # Run specific test file
    pytest tests/test_scanner.py -v

All tests run automatically on GitHub Actions for every commit and pull request.

### 🔧 Development

    # Clone the repository
    git clone https://github.com/zedraider/network-scanner.git
    cd network-scanner

    # Set up development environment
    uv venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    uv pip install -e ".[dev]"

    # Run tests
    pytest

    # Run linter
    ruff check src/

    # Run type checker
    mypy src/

### 🤝 Contributing

Contributions are welcome! Whether you found a bug, have a feature request, or want to improve documentation:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure tests pass before submitting PRs.

### 📄 License

This project is licensed under the MIT License – see the `LICENSE` file for details.

### 🙏 Acknowledgments

- Created to solve a real networking problem
- Inspired by the need to find "lost" devices in complex networks
- Built with ❤️ for sysadmins, network engineers, and IT enthusiasts
- Uses UV for blazing fast dependency management

### ⭐ Show Your Support

If this tool helped you find a "lost" device in your network, give it a star! ⭐

Found a bug or have a feature request? [Open an issue](https://github.com/zedraider/network-scanner/issues).

---

<a name="russian"></a>
## Русский

Быстрый Python-инструмент для обнаружения веб-интерфейсов в локальных сетях. Идеально подходит для поиска роутеров, репитеров, IoT-устройств и другого сетевого оборудования.

**Проверено на практике**: успешно нашёл "потерянный" роутер Xiaomi с забытым IP-адресом!

### 🌟 Возможности

- 🚀 **Быстрое многопоточное сканирование** – сканирует всю сеть /24 за секунды
- 🔍 **Автоматическое обнаружение роутеров** – определяет роутеры и репитеры с помощью умного поиска по ключевым словам
- 🌐 **Поддержка множества кодировок** – работает с UTF-8, GBK, GB2312 для международных устройств
- 📊 **Умный анализ** – извлекает заголовки страниц, информацию о сервере и типы контента
- 💾 **Экспорт результатов** – сохраняет в JSON и текстовые форматы с отметками времени
- 🎨 **Цветной вывод в консоль** – легко читаемые результаты с эмодзи-индикаторами
- ⚡ **Интеграция с UV** – более быстрое управление зависимостями, чем pip
- 🐧 **Кроссплатформенность** – работает на Windows, Linux, macOS
- 🧪 **Протестировано** – комплексный набор тестов с покрытием 95%

### 📖 История создания

Этот проект родился из **реальной проблемы**: у пользователя был роутер Xiaomi, настроенный на статический IP-адрес много лет назад, и он забыл его. Роутер работал как репитер в сети под управлением pfSense, но требовалось обновить настройки.

**Задача**: найти IP-адрес роутера без сброса к заводским настройкам.

**Решение**: был создан `network-scanner`. Он просканировал сеть, нашёл неизвестное устройство с искажённым текстом `å°ç±³è·¯ç±å¨`, исправил китайскую кодировку, и оказалось, что это `小米路由器` (Xiaomi Router) по адресу `192.168.3.86`!

**Миссия выполнена**: роутер был найден, настройки обновлены, а инструмент доказал свою эффективность в реальных условиях.

### 🚀 Быстрый старт

#### Установка с UV (рекомендуется)

    # Установите UV, если у вас его нет
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # или на Windows:
    # irm https://astral.sh/uv/install.ps1 | iex

    # Клонируйте и установите
    git clone https://github.com/zedraider/network-scanner.git
    cd network-scanner
    uv sync

    # Или установите глобально
    uv pip install git+https://github.com/zedraider/network-scanner.git

#### Базовое использование

    # Сканировать сеть по умолчанию (192.168.1.0/24)
    network-scanner

    # Сканировать конкретную сеть
    network-scanner --network 192.168.0.0/24

    # Сохранить результаты в файлы
    network-scanner --save

    # Проверить дополнительные порты
    network-scanner --ports 80,443,8080,8443,8888

    # Получить справку
    network-scanner --help

### 📋 Примеры

Найти все веб-интерфейсы

    network-scanner --network 192.168.1.0/24 --save

Поиск роутеров на определённых портах

    network-scanner --ports 80,81,82,443,8080,8081,8443,8888 --save

Быстрый запуск на Windows
Дважды кликните `scripts/start.bat` или выполните:

    .\scripts\start.bat

### 🖥️ Пример вывода

    🚀 РОУТЕР! Найден веб-интерфейс:
      IP:        192.168.3.86
      Порт:      80
      URL:       http://192.168.3.86:80
      Статус:    200
      Заголовок: 小米路由器
      Сервер:    nginx
      Размер:    1760 байт
      Тип:       text/html

### 🎯 Сценарии использования

- ✅ Найти неизвестные устройства в вашей сети
- ✅ Обнаружить IP роутера, если вы его забыли
- ✅ Инвентаризация сетевого оборудования
- ✅ Аудит безопасности – найти открытые веб-интерфейсы
- ✅ Диагностика сети
- ✅ Обнаружение IoT-устройств
- ✅ Управление домашней лабораторией

### 🛠️ Расширенные возможности

#### Python API

    from network_scanner import NetworkScanner

    # Создайте сканер с пользовательскими настройками
    scanner = NetworkScanner(
        network="192.168.1.0/24",
        timeout=3,
        threads=30
    )

    # Добавьте пользовательские порты
    scanner.common_ports.extend([81, 82, 8001])

    # Запустите сканирование
    results = scanner.scan_network()

    # Сохраните результаты
    scanner.save_results()

#### Пользовательские скрипты

Посмотрите директорию `scripts/`:

- `start.bat` – запуск на Windows
- `start.ps1` – запуск на PowerShell
- `investigate_device.py` – детальное исследование устройства
- `final_report.py` – создание итогового отчёта

### 📁 Структура проекта

    network-scanner/
    ├── src/network_scanner/   # Исходный код
    │   ├── scanner.py         # Основной класс сканера
    │   ├── cli.py             # Интерфейс командной строки
    │   └── __init__.py
    ├── tests/                 # Модульные тесты (36 тестов, покрытие 95%)
    ├── examples/              # Примеры использования
    ├── scripts/               # Вспомогательные скрипты
    ├── docs/                  # Документация
    ├── .github/workflows/     # CI/CD конвейеры
    └── results/               # Результаты сканирования (игнорируется git)

### 🧪 Тестирование

    # Запустить все тесты
    pytest tests/

    # Запустить с покрытием
    pytest --cov=src tests/

    # Запустить конкретный файл с тестами
    pytest tests/test_scanner.py -v

Все тесты автоматически запускаются на GitHub Actions для каждого коммита и pull request.

### 🔧 Разработка

    # Клонируйте репозиторий
    git clone https://github.com/zedraider/network-scanner.git
    cd network-scanner

    # Настройте среду разработки
    uv venv
    source .venv/bin/activate  # или .venv\Scripts\activate на Windows
    uv pip install -e ".[dev]"

    # Запустите тесты
    pytest

    # Запустите линтер
    ruff check src/

    # Запустите проверку типов
    mypy src/

### 🤝 Участие в разработке

Приветствуются любые вклады! Если вы нашли ошибку, хотите предложить новую функцию или улучшить документацию:

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

Пожалуйста, убедитесь, что тесты проходят перед отправкой PR.

### 📄 Лицензия

Этот проект распространяется под лицензией MIT – подробности в файле `LICENSE`.

### 🙏 Благодарности

- Создан для решения реальной сетевой проблемы
- Вдохновлён необходимостью находить "потерянные" устройства в сложных сетях
- Сделан с ❤️ для сисадминов, сетевых инженеров и ИТ-энтузиастов
- Использует UV для молниеносного управления зависимостями

### ⭐ Поддержите проект

Если этот инструмент помог вам найти "потерянное" устройство в вашей сети, поставьте звёздочку! ⭐

Нашли ошибку или есть предложение? [Откройте issue](https://github.com/zedraider/network-scanner/issues).

---

*"Инструмент, который нашёл забытый роутер, найдёт устройства и в вашей сети!" 🚀*