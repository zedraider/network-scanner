# Network Scanner 🔍

A fast Python tool for discovering web interfaces in local networks. Perfect for finding routers, repeaters, IoT devices, and other network equipment.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- 🚀 **Fast multithreaded scanning** - scans entire /24 network in seconds
- 🔍 **Automatic router detection** - identifies routers and repeaters
- 🌐 **HTTP/HTTPS support** - works with both protocols
- 📊 **Smart analysis** - extracts page titles and server info
- 💾 **Export results** - saves to JSON and text formats
- 🎨 **Colored console output** - easy to read results
- ⚡ **UV integration** - faster than pip

## Installation

### Using UV (Recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on Windows:
# irm https://astral.sh/uv/install.ps1 | iex

# Clone and install
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner
uv sync

Using pip
bash
pip install network-scanner
From source
bash
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner
pip install -e .
Quick Start
bash
# Basic scan
network-scanner

# Scan specific network
network-scanner --network 192.168.0.0/24

# Save results
network-scanner --save

# Check additional ports
network-scanner --ports 80,443,8080,8443,8888

# Help
network-scanner --help
Examples
Find all web interfaces:
bash
network-scanner --network 192.168.1.0/24 --save
Scan with custom ports:
bash
network-scanner --ports 80,81,82,443,8080,8081,8443,8888
Windows users can double-click:
bash
scripts\start.bat
Output Example
text
🔥 ROUTER! Web interface found:
  IP:        192.168.1.1
  Port:      80 (http)
  URL:       http://192.168.1.1:80
  Status:    200
  Title:     pfSense - Login
  Server:    nginx
  Size:      9366 bytes
Use Cases
✅ Find unknown devices in your network

✅ Discover router IP when you forget it

✅ Inventory network equipment

✅ Security audits - find exposed web interfaces

✅ Network troubleshooting

Advanced Usage
Python API
python
from network_scanner import NetworkScanner

scanner = NetworkScanner(network="192.168.1.0/24")
results = scanner.scan_network()

for device in results:
    print(f"{device['ip']}:{device['port']} - {device['title']}")
Integration with pfSense
The tool was originally created to find network devices when working with pfSense firewalls.

Project Structure
text
network-scanner/
├── src/network_scanner/    # Source code
├── tests/                  # Unit tests
├── examples/               # Usage examples
├── scripts/                # Helper scripts
└── docs/                   # Documentation
Development
bash
# Setup development environment
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/

# Run type checking
mypy src/
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Created for practical network administration needs

Inspired by real-world pfSense deployment scenarios

Built with ❤️ for sysadmins and network enthusiasts