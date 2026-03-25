# 🔥 Morpheus

> Orchestrate autonomous coding agents at scale

[![CI](https://github.com/MukundaKatta/morpheus/actions/workflows/ci.yml/badge.svg)](https://github.com/MukundaKatta/morpheus/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)]()

## What is Morpheus?

Morpheus is a Python framework for orchestrating autonomous coding agents. It decomposes complex programming tasks into subtasks, assigns them to specialized agents, manages code generation and review pipelines, and coordinates multi-agent collaboration for software development at scale.

## ✨ Features

- ✅ Task decomposition — break complex coding tasks into subtasks
- ✅ Agent orchestration — manage multiple coding agents in parallel
- ✅ Code review pipeline — automatic quality checks on generated code
- ✅ Planning engine — create execution plans from natural language tasks
- ✅ CLI for running and monitoring coding agents
- 🔜 Git integration for automatic PR creation
- 🔜 Multi-language code generation support

## 🚀 Quick Start

```bash
pip install -e .
morpheus plan "Build a REST API for user management"
morpheus run "Add pagination to the user list endpoint"
morpheus status
```

## 🏗️ Architecture

```mermaid
graph TD
    A[User Task] --> B[TaskDecomposer]
    B --> C[Execution Plan]
    C --> D[AgentOrchestrator]
    D --> E[CodingAgent 1]
    D --> F[CodingAgent 2]
    D --> G[CodingAgent N]
    E --> H[ReviewPipeline]
    F --> H
    G --> H
    H --> I[Quality Report]
    I --> J[Final Output]
```

## 📖 Inspired By

Inspired by [Devin](https://devin.ai) and [OpenHands](https://github.com/All-Hands-AI/OpenHands) but focused on orchestration patterns for multiple specialized agents.

---

**Built by [Officethree Technologies](https://github.com/MukundaKatta)** | Made with ❤️ and AI
