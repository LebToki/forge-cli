# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-02-17

### Added
- **Configuration System**: New TOML-based configuration system with persistent storage in `~/.forge/config.toml`
- **GitHub Integration**: Complete GitHub integration with:
  - Repository listing and cloning
  - Pull request creation and listing
  - Issue management
  - Local git operations (status, commit, branch, push, pull)
- **Enhanced CLI Commands**:
  - `forge config set/get/list` - Configuration management
  - `forge github auth` - Authenticate with GitHub
  - `forge github list` - List repositories
  - `forge github clone` - Clone repositories
  - `forge github commit` - Commit changes
  - `forge github push/pull` - Push and pull
  - `forge github pr-list/pr-create` - Manage PRs
  - `forge github issue-list/issue-create` - Manage issues
  - `forge github status` - Show git status
  - `forge github log` - Show commit history
- **Web Dashboard**: Enhanced AI Dashboard with chat interface and quick actions
- **Test Suite**: Expanded test coverage with 13 tests

### Changed
- Updated `pyproject.toml` with new dependencies (PyGithub, GitPython, keyring, toml)
- Improved error handling and user feedback in CLI commands

### Dependencies
- Added: PyGithub>=2.0.0, GitPython>=3.1.0, keyring>=24.0.0, toml>=0.10.0

## [0.0.1] - 2026-02-16

### Added
- Initial release
- Basic CLI with DeepSeek AI integration
- File system operations
- Terminal UI with Rich library
- Web dashboard (basic)
