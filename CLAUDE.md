# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a Python library that provides Redis wrappers to automatically handle cluster redirect exceptions (`MOVED`). The library offers both synchronous and asynchronous Redis client wrappers.

### Core Components

- `src/redis_redirect/redis_wrapper.py` - Synchronous Redis wrapper (`RedisWrapper` class)
- `src/redis_redirect/aioredis_wrapper.py` - Asynchronous Redis wrapper (`AioRedisWrapper` class)
- `src/redis_redirect/pubsub.py` - Pub/sub functionality wrapper

Both wrappers use `__getattribute__` method overriding to intercept Redis method calls and catch `MOVED` exceptions. When a `MOVED` exception is encountered, they:
1. Parse the new Redis host/port from the exception message
2. Create a new Redis connection to the redirected host
3. Retry the original operation

The wrappers inherit from their respective Redis classes primarily for IDE autocompletion support, but don't call the parent constructors.

## Development Commands

### Testing
```bash
# Run all tests with coverage
python -m pytest --cov=src tests/

# Run tests with detailed output
python -m pytest -v tests/

# Run specific test file
python -m pytest tests/test_redis_wrapper.py
python -m pytest tests/test_aioredis_wrapper.py
```

### Linting and Code Quality
```bash
# Install development dependencies
pip install -r requirements.dev.txt

# Run pylint (configured in CI)
pylint src/

# Run mypy type checking
mypy src/

# Format code with black
black src/ tests/

# Check code style
pydocstyle src/
```

### Dependencies Management
```bash
# Update requirements (uses custom script)
bash ./scripts/compile_requirements.sh

# Update pre-commit hooks
pre-commit autoupdate

# Install all dev dependencies
make reqs
```

### Building and Publishing
```bash
# Build package
pip install -e .

# Version management
make ver-bug      # Bump patch version
make ver-feature  # Bump minor version
make ver-release  # Bump major version
```

## Testing Strategy

Tests use mocking to simulate Redis `MOVED` exceptions and verify the redirect behavior works correctly. The test mocks create fake Redis instances that throw `MOVED` exceptions to test the wrapper's redirect logic.

Both sync and async wrappers have comprehensive test coverage including edge cases for redirect parsing and connection handling.
