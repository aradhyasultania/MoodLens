# Contributing to MoodLens

Thank you for your interest in contributing to MoodLens! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Provide:

- **Clear title and description**
- **Use case and benefits**
- **Possible implementation approach**

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   - Run `python test_system.py`
   - Ensure all tests pass
5. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
6. **Push to your branch** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/moodlens.git
cd moodlens

# Create virtual environment
python3 -m venv moodlens-env
source moodlens-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_system.py

# Run application
python moodlens_simplified.py
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and under 50 lines when possible
- Use type hints where appropriate

## Testing

- Add tests for new features
- Ensure existing tests pass
- Test on multiple browsers (Chrome, Firefox, Safari)
- Test responsive design on mobile

## Documentation

- Update README.md for major features
- Add docstrings to new functions
- Comment complex algorithms
- Update API documentation for new endpoints

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🎉

