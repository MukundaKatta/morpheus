"""Agent orchestration — manage multiple coding agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from morpheus.core import CodingAgent, Task, TaskStatus, CodeBlock, ReviewResult


@dataclass
class AgentResult:
    """Result from an agent's work on a task."""

    agent_name: str
    task: Task
    code: CodeBlock
    review: ReviewResult


class AgentOrchestrator:
    """Orchestrate multiple coding agents working on related tasks."""

    def __init__(self) -> None:
        self._agents: dict[str, CodingAgent] = {}
        self._results: list[AgentResult] = []

    def add_agent(self, name: str) -> CodingAgent:
        """Create and register a new coding agent."""
        agent = CodingAgent(name=name)
        self._agents[name] = agent
        return agent

    def assign_task(self, agent_name: str, task: Task) -> AgentResult:
        """Assign a task to a specific agent and get the result."""
        agent = self._agents.get(agent_name)
        if agent is None:
            raise KeyError(f"Agent not found: {agent_name}")

        code = agent.implement(task)
        review = agent.review(code)
        result = AgentResult(agent_name=agent_name, task=task, code=code, review=review)
        self._results.append(result)
        return result

    def run_pipeline(self, tasks: list[Task]) -> list[AgentResult]:
        """Run all tasks through the agent pipeline sequentially."""
        agent_names = list(self._agents.keys())
        if not agent_names:
            self.add_agent("default")
            agent_names = ["default"]

        results: list[AgentResult] = []
        for i, task in enumerate(tasks):
            agent_name = agent_names[i % len(agent_names)]
            result = self.assign_task(agent_name, task)
            results.append(result)
        return results

    def monitor_progress(self) -> dict[str, Any]:
        """Get current progress of all tasks."""
        total = len(self._results)
        passed = sum(1 for r in self._results if r.review.passed)
        avg_score = (
            sum(r.review.score for r in self._results) / total if total > 0 else 0
        )
        return {
            "total_tasks": total,
            "passed_review": passed,
            "failed_review": total - passed,
            "average_score": round(avg_score, 1),
        }

    def collect_results(self) -> list[dict[str, Any]]:
        """Collect all results as serializable dicts."""
        return [
            {
                "agent": r.agent_name,
                "task": r.task.description,
                "status": r.task.status.value,
                "review_passed": r.review.passed,
                "review_score": r.review.score,
                "issues": r.review.issues,
            }
            for r in self._results
        ]

    @property
    def agent_count(self) -> int:
        return len(self._agents)
