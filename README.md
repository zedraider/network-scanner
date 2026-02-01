# Network Scanner 🔍

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/zedraider/network-scanner?style=social)](https://github.com/zedraider/network-scanner/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zedraider/network-scanner?style=social)](https://github.com/zedraider/network-scanner/network/members)
[![GitHub issues](https://img.shields.io/github/issues/zedraider/network-scanner)](https://github.com/zedraider/network-scanner/issues)
[![UV](https://img.shields.io/badge/uv-package%20manager-blueviolet)](https://github.com/astral-sh/uv)
[![Tests](https://github.com/zedraider/network-scanner/actions/workflows/python-tests.yml/badge.svg)](https://github.com/zedraider/network-scanner/actions/workflows/python-tests.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A fast Python tool for discovering web interfaces in local networks. Perfect for finding routers, repeaters, IoT devices, and other network equipment.

**Real-World Proven**: Successfully found a "lost" Xiaomi router with forgotten IP address!

## 🌟 Features

- 🚀 **Fast multithreaded scanning** - scans entire /24 network in seconds
- 🔍 **Automatic router detection** - identifies routers and repeaters with smart keyword matching
- 🌐 **Multi-encoding support** - handles UTF-8, GBK, GB2312 for international devices
- 📊 **Smart analysis** - extracts page titles, server info, and content types
- 💾 **Export results** - saves to JSON and text formats with timestamps
- 🎨 **Colored console output** - easy-to-read results with emoji indicators
- ⚡ **UV integration** - faster dependency management than pip
- 🐧 **Cross-platform** - works on Windows, Linux, macOS
- 🧪 **Tested** - comprehensive test suite with 95% coverage

## 📖 The Story Behind This Tool

This project was born from a **real-world problem**: A user had a Xiaomi router configured with a static IP address years ago and forgot it. The router was working as a repeater in a pfSense-managed network, but needed configuration updates.

**The Challenge**: Find the router's IP address without resetting it to factory defaults.

**The Solution**: `network-scanner` was created. It scanned the network, found an unknown device with garbled text `å°ç±³è·¯ç±å¨`, fixed the Chinese encoding, and revealed it was actually `小米路由器` (Xiaomi Router) at `192.168.3.86`!

**Mission Accomplished**: The router was found, settings were updated, and the tool was proven effective in real conditions.

## 🚀 Quick Start

### Installation with UV (Recommended)

```bash
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
```
Basic Usage
```bash
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
```
📋 Examples
Find All Web Interfaces
```bash
network-scanner --network 192.168.1.0/24 --save
Search for Routers with Specific Ports

network-scanner --ports 80,81,82,443,8080,8081,8443,8888 --save
Quick Windows Launch
Double-click scripts/start.bat or run:
```
```powershell
.\scripts\start.bat
```
🖥️ Output Example
```text
🚀 РОУТЕР! Найден веб-интерфейс:
  IP:        192.168.3.86
  Порт:      80
  URL:       http://192.168.3.86:80
  Статус:    200
  Заголовок: 小米路由器
  Сервер:    nginx
  Размер:    1760 байт
  Тип:       text/html
```
🎯 Use Cases
✅ Find unknown devices in your network

✅ Discover router IP when you forget it

✅ Inventory network equipment

✅ Security audits - find exposed web interfaces

✅ Network troubleshooting

✅ IoT device discovery

✅ Home lab management

🛠️ Advanced Features
Python API
```python
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
```
Custom Scripts
Check out the scripts/ directory:

start.bat - Windows launcher

start.ps1 - PowerShell launcher

investigate_device.py - Detailed device investigation

final_report.py - Generate summary reports

📁 Project Structure
text
network-scanner/
├── src/network_scanner/     # Source code
│   ├── scanner.py           # Main scanner class
│   ├── cli.py               # Command-line interface
│   └── __init__.py
├── tests/                   # Unit tests (36 tests, 95% coverage)
├── examples/                # Usage examples
├── scripts/                 # Helper scripts
├── docs/                    # Documentation
├── .github/workflows/       # CI/CD pipelines
└── results/                 # Scan results (gitignored)
🧪 Testing
```python
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_scanner.py -v
All tests run automatically on GitHub Actions for every commit and pull request.
```
🔧 Development
```bash
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
```
🤝 Contributing
Contributions are welcome! Whether you found a bug, have a feature request, or want to improve documentation:

Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

Please make sure tests pass before submitting PRs.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Created to solve a real networking problem

Inspired by the need to find "lost" devices in complex networks

Built with ❤️ for sysadmins, network engineers, and IT enthusiasts

Uses UV for blazing fast dependency management

⭐ Show Your Support
If this tool helped you find a "lost" device in your network, give it a star! ⭐

Found a bug or have a feature request? Open an issue.

"The tool that found a forgotten router can find devices in your network too!" 🚀