# Contributing to FORGE

First off, thank you for considering contributing to FORGE! We love community contributions.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/forge-cli.git
   cd forge-cli
   ```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install in development mode:

```bash
pip install -e .[dev,github]
```

Set up pre-commit hooks:

```bash
pre-commit install
```

## Development Workflow

Create a branch:

```bash
git checkout -b feature/amazing-feature
```

Make your changes

Run tests:

```bash
pytest
```

Run linting:

```bash
black forge tests
isort forge tests
flake8 forge tests
mypy forge
```

Commit your changes:

```bash
git commit -m "Add amazing feature"
```

Push to your fork:

```bash
git push origin feature/amazing-feature
```

Open a Pull Request

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions focused and small

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Questions?

Join our Discord or open a Discussion
