# AI Kernel Explorer

[![PyPI](https://img.shields.io/pypi/v/ai-kernel-explorer?color=blue)](https://pypi.org/project/ai-kernel-explorer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ai-kernel-explorer)](https://pypi.org/project/ai-kernel-explorer/)
[![PyPI - License](https://img.shields.io/pypi/l/ai-kernel-explorer?color=blue)](https://pypi.org/project/ai-kernel-explorer/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ai-kernel-explorer)](https://pypi.org/project/ai-kernel-explorer/)

## Explore the Linux kernel source code with AI-generated summaries

The Linux kernel is a large and complex codebase, with over 30 million lines of code. Understanding the codebase can be challenging, especially for newcomers. To help developers navigate the codebase more easily, this is a lightweight tool that uses GPT-4o to generate summaries of the Linux kernel source code as you explore.

## Installation

```bash
pip install ai-kernel-explorer # or ideally pipx install ai-kernel-explorer
```

```text
usage: ai-kernel-explorer [-h] [--api-key API_KEY] [--cache CACHE] [--model MODEL] [--version] [root]

Explore the Linux kernel source code with AI-generated summaries.

positional arguments:
  root               The root directory of the Linux kernel source code. (default: /usr/src)

options:
  -h, --help         show this help message and exit
  --api-key API_KEY  Your OpenAI API key. (default: $OPENAI_API_KEY)
  --cache CACHE      The path to store AI responses. (default: ~/.cache/ai-kernel-explorer)
  --model MODEL      The OpenAI model to use. (default: gpt-4o)
  --version          show program's version number and exit
```

[https://github.com/mathiscode/ai-kernel-explorer](https://github.com/mathiscode/ai-kernel-explorer)
