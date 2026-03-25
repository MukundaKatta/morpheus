# Morpheus Architecture

## Components

- **CodingAgent** — Individual agent that plans, implements, and reviews code
- **TaskDecomposer** — Breaks complex tasks into subtasks with dependencies  
- **CodeGenerator** — Template-based code generation (LLM in production)
- **ReviewPipeline** — Automatic code quality checking
- **AgentOrchestrator** — Manages multiple agents working in parallel
- **TaskPlanner** — Creates structured execution plans

## Flow

```
Task → Decompose → Plan → Assign to Agents → Generate → Review → Output
```
