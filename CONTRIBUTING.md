@"
# Contributing to Network Scanner

Thank you for considering contributing to Network Scanner!

## How to Contribute

### Reporting Bugs
1. Check if the bug already exists in Issues
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Network environment details

### Suggesting Features
1. Check if the feature is already requested
2. Explain the use case and benefits
3. Consider if it aligns with project goals

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a Pull Request

## Development Setup

\`\`\`bash
# Clone and setup
git clone https://github.com/zedraider/network-scanner.git
cd network-scanner

# Create virtual environment
uv venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows

# Install in development mode
uv pip install -e '.[dev]'

# Run tests
pytest

# Run linter
ruff check src/
\`\`\`

## Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Write tests for new features

## Project Goals
- Keep it simple and practical
- Solve real networking problems
- Maintain good performance
- Support different encodings and devices

## Questions?
Open an issue or start a discussion!

Thank you for helping make Network Scanner better! 🚀
"@ | Out-File -FilePath CONTRIBUTING.md -Encoding UTF8