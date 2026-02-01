# Installation Guide

## Prerequisites
- Python 3.8 or higher
- Git (for source installation)
- Network access to scan

## Installation Methods

Method 1: From GitHub (Recommended)

# Clone the repository
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner

# Install UV if not installed
# Windows:
irm https://astral.sh/uv/install.ps1 | iex

# Linux/Mac:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install network-scanner
uv pip install -e .

Method 2: Direct UV Install

# Install directly with UV
uv pip install git+https://github.com/zedraider/network-scanner.git
Method 3: Manual Installation

# Download the source
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
Verify Installation

# Check if installed
network-scanner --help

# Test with a quick scan
network-scanner --network 192.168.1.0/24
Troubleshooting
"Command not found"
Make sure the virtual environment is activated or the package is installed globally.

Permission errors on Windows
Run PowerShell as Administrator.

SSL errors
The tool ignores SSL errors by default. If you need strict SSL, modify the code.

Slow scanning
Adjust the thread count: network-scanner --threads 20