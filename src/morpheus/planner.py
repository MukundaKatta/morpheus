"""Task planning and execution plan creation."""

from __future__ import annotations

from dataclasses import dataclass, field

from morpheus.core import Task, TaskDecomposer


@dataclass
class ExecutionPlan:
    """A structured plan for completing a complex task."""

    goal: str
    tasks: list[Task] = field(default_factory=list)
    estimated_steps: int = 0

    def summary(self) -> str:
        lines = [f"Plan: {self.goal}", f"Steps: {len(self.tasks)}"]
        for i, t in enumerate(self.tasks, 1):
            lines.append(f"  {i}. {t.description}")
        return "\n".join(lines)


class TaskPlanner:
    """Plan and structure complex coding tasks."""

    def __init__(self) -> None:
        self.decomposer = TaskDecomposer()

    def create_execution_plan(self, goal: str) -> ExecutionPlan:
        """Create a detailed execution plan from a goal description."""
        tasks = self.decomposer.decompose(goal)
        ordered = self.decomposer.prioritize(tasks)
        return ExecutionPlan(goal=goal, tasks=ordered, estimated_steps=len(ordered))

    def decompose(self, description: str) -> list[Task]:
        """Decompose a task into subtasks."""
        return self.decomposer.decompose(description)

    def prioritize(self, tasks: list[Task]) -> list[Task]:
        """Prioritize tasks by dependencies."""
        return self.decomposer.prioritize(tasks)
