# 🔥 FORGE

<div align="center">
  <img width="1200" height="630" alt="FORGE-BANNER" src="https://github.com/user-attachments/assets/d7d01338-f310-40c9-a9bd-f692be5787c3" />


  
  **Shape code. Ship faster. Forge the future.**
  
  ![PyPI](https://img.shields.io/pypi/v/forge-cli?color=orange&style=flat-square)
  ![MIT License](https://img.shields.io/github/license/LebToki/forge-cli?style=flat-square)
  ![GitHub Stars](https://img.shields.io/github/stars/LebToki/forge-cli?style=flat-square)
  ![Discord](https://img.shields.io/discord/yourid?color=5865F2&style=flat-square)
</div>

---

**FORGE** is an intelligent development assistant that lives in your terminal. Powered by DeepSeek AI, it connects directly to your codebase and GitHub, helping you build, fix, and ship software faster than ever.

## ✨ Features

### 🎨 Beautiful Terminal UI

- Live streaming responses with syntax highlighting
- Animated spinners and progress bars
- Color-coded diffs and file trees
- Real-time command output

### 🔧 Local Development Superpowers

- Read/write/edit files with AI assistance
- Run commands and code in any language
- Search and navigate your codebase
- Automatic error fixing

### 🌐 GitHub Integration

- Clone and manage repositories
- Create branches and commits
- Open pull requests with AI-generated descriptions
- Fix issues automatically

### 🛡️ You're in Control

- Bring your own API keys (DeepSeek, GitHub)
- Confirm every destructive action
- Local workspace for privacy
- Open source and auditable

---

## 🚀 Quick Start

```bash
# Configure your keys
forge config set deepseek.api_key YOUR_KEY
forge config set github.token YOUR_TOKEN

# Ask questions about your code
forge ask "What does this function do?" --file src/main.py

# Fix bugs and open PRs
forge task "Fix the login bug and create a pull request"

# Generate tests
forge task "Write unit tests for the user service"

# Refactor code
forge task "Convert this callback to async/await" --file api/client.js
```

---

## 📦 Installation

### Via pip

```bash
pip install forge-cli[github]  # with GitHub support
pip install forge-cli           # core only
```

### Via Homebrew (macOS)

```bash
brew tap LebToki/forge
brew install forge
```

### From source

```bash
git clone https://github.com/LebToki/forge-cli.git
cd forge-cli
pip install -e .[dev]
```

---

## 🎯 Why Forge?

| Benefit | Description |
|---------|-------------|
| **Stay in the flow** | No switching between browser, editor, and terminal |
| **Real understanding** | DeepSeek actually groks your codebase |
| **End-to-end automation** | From idea to PR in one command |
| **Privacy first** | Your keys, your data, your control |
| **Beautiful experience** | Terminal UI that doesn't suck |

---

## 🤝 Contributing

We'd love your help! Check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

- 💬 Join our Discord
- 🐛 Report bugs on GitHub Issues
- 📖 Improve the documentation

---

## 📚 Documentation

Full documentation at [https://2tinteractive.com/demo/forge/docs/](https://2tinteractive.com/demo/forge/docs/)

- [Getting Started](https://2tinteractive.com/demo/forge/docs/getting-started)
- [Configuration](https://2tinteractive.com/demo/forge/docs/configuration)
- [GitHub Integration](https://2tinteractive.com/demo/forge/docs/github-integration)
- [Tool Reference](https://2tinteractive.com/demo/forge/docs/tool-reference)
- [Examples](https://2tinteractive.com/demo/forge/docs/examples)

---

## 📄 License

MIT © **Tarek Tarabichi** from **2tinteractive**

---

## ⭐ Show Your Support

If you find FORGE useful, please consider:

- Starring the repo ⭐
- Sharing it with friends 🚀
- Contributing code or docs 🤝

---

<div align="center">
  <sub>Built with 🔥 by developers who love the terminal</sub>
</div>
