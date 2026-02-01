@"
# Network Scanner 🔍

[![GitHub release](https://img.shields.io/github/v/release/zedraider/network-scanner)](https://github.com/zedraider/network-scanner/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Real-World Tested](https://img.shields.io/badge/Real--World-Tested-green)](https://github.com/zedraider/network-scanner#-real-world-success-story)
[![GitHub stars](https://img.shields.io/github/stars/zedraider/network-scanner?style=social)](https://github.com/zedraider/network-scanner/stargazers)

A fast Python tool for discovering web interfaces in local networks. Perfect for finding routers, repeaters, IoT devices, and other network equipment.

> **Real-World Proven**: Successfully found a 'lost' Xiaomi router with forgotten static IP!

## Features

- 🚀 **Fast multithreaded scanning** - scans entire /24 network in seconds
- 🔍 **Automatic router detection** - identifies routers and repeaters
- 🌐 **HTTP/HTTPS support** - works with both protocols
- 📊 **Smart encoding detection** - handles UTF-8, GBK, GB2312 (Chinese devices)
- 💾 **Export results** - saves to JSON and text formats
- 🎨 **Colored console output** - easy to read results
- ⚡ **UV integration** - faster than pip

## Quick Start

\`\`\`bash
# Install with UV (recommended)
uv pip install network-scanner

# Or from source
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner
uv pip install -e .

# Scan your network
network-scanner --save
\`\`\`

## Real-World Success Story

This tool was born from a real need: finding a 'lost' Xiaomi router with a forgotten static IP address. After years of service as a repeater, the router needed configuration updates but its IP was unknown.

**The Discovery:**
- First scan found pfSense at 192.168.3.1
- Unknown device at 192.168.3.86 showed garbled text: \`å°ç±³è·¯ç±å¨\`
- Added automatic encoding detection
- **Success!** The garbled text decoded to \`小米路由器\` (Xiaomi Router!)

**Result:** Router found, settings updated, problem solved! Read the full story in [PROJECT_STORY.md](PROJECT_STORY.md).

## Usage Examples

\`\`\`bash
# Basic scan
network-scanner

# Scan specific network
network-scanner --network 192.168.0.0/24

# Check additional ports
network-scanner --ports 80,443,8080,8443,8888

# Save results
network-scanner --save
\`\`\`

## Project Structure

\`\`\`
network-scanner/
├── src/network_scanner/    # Source code
├── tests/                  # Unit tests
├── examples/               # Usage examples
├── scripts/                # Helper scripts
├── docs/                   # Documentation
└── .github/workflows/     # CI/CD pipeline
\`\`\`

## Development

\`\`\`bash
# Setup development environment
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e '.[dev]'

# Run tests
pytest

# Run linter
ruff check src/
\`\`\`

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created to solve a real networking problem
- Inspired by the need to find 'lost' network devices
- Built with ❤️ for sysadmins and network enthusiasts

---

⭐ **If you found this tool useful, please consider giving it a star on GitHub!** ⭐

---
*Last updated: $(Get-Date -Format 'yyyy-MM-dd')*
"@ | Out-File -FilePath README.md -Encoding UTF8