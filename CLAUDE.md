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

### Environment Setup
```bash
# Set up or activate development environment
source ./activate.sh
```

**IMPORTANT**: Always activate the virtual environment before running any commands. Use `source ./activate.sh` before each command.

### Testing
```bash
# Run all tests with coverage
source ./activate.sh && python -m pytest --cov=src tests/

# Run tests with detailed output
source ./activate.sh && python -m pytest -v tests/

# Run specific test file
source ./activate.sh && python -m pytest tests/test_redis_wrapper.py
source ./activate.sh && python -m pytest tests/test_aioredis_wrapper.py
```

### Linting and Code Quality
```bash
# Run pre-commit hooks for all code quality checks
source ./activate.sh && pre-commit run --all-files
```

**IMPORTANT**: Always use `pre-commit run --all-files` for code quality checks. Never run pylint, mypy, or black directly.

### Dependencies Management
```bash
# Update requirements (uses custom script)
source ./activate.sh && bash ./scripts/compile_requirements.sh

# Update pre-commit hooks
source ./activate.sh && pre-commit autoupdate

# Install all dev dependencies
source ./activate.sh && make reqs
```

### Building and Publishing
```bash
# Build package
source ./activate.sh && pip install -e .

# Version management
source ./activate.sh && make ver-bug      # Bump patch version
source ./activate.sh && make ver-feature  # Bump minor version
source ./activate.sh && make ver-release  # Bump major version
```

## Testing Strategy

Tests use mocking to simulate Redis `MOVED` exceptions and verify the redirect behavior works correctly. The test mocks create fake Redis instances that throw `MOVED` exceptions to test the wrapper's redirect logic.

Both sync and async wrappers have comprehensive test coverage including edge cases for redirect parsing and connection handling.
