"""Core coding agent components."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """A unit of work for a coding agent."""

    description: str
    task_id: str = ""
    status: TaskStatus = TaskStatus.PENDING
    dependencies: list[str] = field(default_factory=list)
    output: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeBlock:
    """A generated block of code."""

    language: str
    content: str
    file_path: str = ""
    line_count: int = 0

    def __post_init__(self) -> None:
        self.line_count = len(self.content.splitlines())


@dataclass
class ReviewResult:
    """Result of a code review."""

    passed: bool
    score: float
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


class TaskDecomposer:
    """Decomposes complex tasks into manageable subtasks."""

    PATTERNS: dict[str, list[str]] = {
        "api": ["Define data models", "Create API endpoints", "Add validation", "Write tests"],
        "frontend": ["Create components", "Add styling", "Implement state management", "Write tests"],
        "database": ["Design schema", "Create migrations", "Add indexes", "Write seed data"],
        "general": ["Analyze requirements", "Implement core logic", "Add error handling", "Write tests"],
    }

    def decompose(self, task_description: str) -> list[Task]:
        """Break a complex task into subtasks based on pattern matching."""
        task_type = self._detect_type(task_description)
        patterns = self.PATTERNS.get(task_type, self.PATTERNS["general"])

        subtasks: list[Task] = []
        for i, pattern in enumerate(patterns):
            subtask = Task(
                description=f"{pattern} for: {task_description}",
                task_id=f"task-{i + 1}",
                dependencies=[f"task-{i}"] if i > 0 else [],
            )
            subtasks.append(subtask)
        return subtasks

    def prioritize(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by dependency order."""
        completed_ids: set[str] = set()
        ordered: list[Task] = []
        remaining = list(tasks)

        while remaining:
            batch = [t for t in remaining if all(d in completed_ids for d in t.dependencies)]
            if not batch:
                ordered.extend(remaining)
                break
            ordered.extend(batch)
            completed_ids.update(t.task_id for t in batch)
            remaining = [t for t in remaining if t not in batch]

        return ordered

    @staticmethod
    def _detect_type(description: str) -> str:
        lower = description.lower()
        if any(kw in lower for kw in ["api", "endpoint", "rest", "route"]):
            return "api"
        if any(kw in lower for kw in ["frontend", "component", "ui", "page"]):
            return "frontend"
        if any(kw in lower for kw in ["database", "schema", "migration", "table"]):
            return "database"
        return "general"


class CodeGenerator:
    """Generate code from task descriptions."""

    def generate(self, task: Task) -> CodeBlock:
        """Generate a code block for a task.

        In production, this calls an LLM. Here we use template-based generation.
        """
        description = task.description.lower()

        if "model" in description or "schema" in description:
            code = self._generate_model(task.description)
        elif "endpoint" in description or "api" in description:
            code = self._generate_endpoint(task.description)
        elif "test" in description:
            code = self._generate_test(task.description)
        else:
            code = self._generate_generic(task.description)

        return CodeBlock(language="python", content=code, file_path="generated.py")

    @staticmethod
    def _generate_model(description: str) -> str:
        return f'"""Model generated for: {description}"""\nfrom pydantic import BaseModel\n\n\nclass Item(BaseModel):\n    id: int\n    name: str\n    description: str = ""\n    active: bool = True\n'

    @staticmethod
    def _generate_endpoint(description: str) -> str:
        return f'"""Endpoint generated for: {description}"""\nfrom fastapi import APIRouter\n\nrouter = APIRouter()\n\n\n@router.get("/items")\nasync def list_items():\n    return {{"items": []}}\n'

    @staticmethod
    def _generate_test(description: str) -> str:
        return f'"""Tests generated for: {description}"""\n\n\ndef test_placeholder():\n    assert True\n'

    @staticmethod
    def _generate_generic(description: str) -> str:
        return f'"""Generated for: {description}"""\n\n\ndef main():\n    print("Implementation for: {description}")\n\n\nif __name__ == "__main__":\n    main()\n'


class ReviewPipeline:
    """Review generated code for quality."""

    def review(self, code: CodeBlock) -> ReviewResult:
        """Run quality checks on generated code."""
        issues: list[str] = []
        suggestions: list[str] = []

        # Check for common issues
        if not code.content.strip():
            issues.append("Empty code block")

        if code.line_count < 3:
            suggestions.append("Code is very short — consider adding more logic")

        if "import *" in code.content:
            issues.append("Wildcard import detected")

        if "except:" in code.content and "except Exception" not in code.content:
            issues.append("Bare except clause — use specific exceptions")

        if '"""' not in code.content and "'''" not in code.content:
            suggestions.append("Missing docstrings")

        # Calculate score
        max_deductions = len(issues) * 20 + len(suggestions) * 5
        score = max(0.0, min(100.0, 100.0 - max_deductions))
        passed = len(issues) == 0 and score >= 60

        return ReviewResult(passed=passed, score=score, issues=issues, suggestions=suggestions)


class CodingAgent:
    """An autonomous coding agent that plans, implements, and reviews code."""

    def __init__(self, name: str = "default") -> None:
        self.name = name
        self.decomposer = TaskDecomposer()
        self.generator = CodeGenerator()
        self.reviewer = ReviewPipeline()

    def plan(self, task_description: str) -> list[Task]:
        """Create an execution plan for a task."""
        return self.decomposer.decompose(task_description)

    def implement(self, task: Task) -> CodeBlock:
        """Generate code for a single task."""
        task.status = TaskStatus.IN_PROGRESS
        code = self.generator.generate(task)
        task.status = TaskStatus.COMPLETED
        task.output = code.content
        return code

    def review(self, code: CodeBlock) -> ReviewResult:
        """Review generated code."""
        return self.reviewer.review(code)

    def iterate(self, task: Task, max_attempts: int = 3) -> CodeBlock:
        """Generate and review code, iterating until quality passes."""
        for attempt in range(max_attempts):
            code = self.implement(task)
            result = self.review(code)
            if result.passed:
                return code
        return code  # Return last attempt even if not perfect
