"""Morpheus CLI."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from morpheus.core import CodingAgent
from morpheus.planner import TaskPlanner

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="morpheus")
def main() -> None:
    """Morpheus — Orchestrate autonomous coding agents."""
    pass


@main.command()
@click.argument("task")
def plan(task: str) -> None:
    """Create an execution plan for a coding task."""
    planner = TaskPlanner()
    execution_plan = planner.create_execution_plan(task)

    console.print(f"\n[bold blue]📋 Execution Plan[/bold blue]\n")
    console.print(f"  Goal: {execution_plan.goal}")
    console.print(f"  Steps: {execution_plan.estimated_steps}\n")

    for i, t in enumerate(execution_plan.tasks, 1):
        console.print(f"  [cyan]{i}.[/cyan] {t.description}")
    console.print()


@main.command()
@click.argument("task")
def run(task: str) -> None:
    """Run a coding agent on a task."""
    agent = CodingAgent(name="primary")
    console.print(f"\n[bold blue]🤖 Running agent:[/bold blue] {task}\n")

    code = agent.iterate(agent.decomposer.decompose(task)[0])
    review = agent.review(code)

    console.print(f"  Generated: {code.line_count} lines of {code.language}")
    console.print(f"  Review: {'[green]PASSED' if review.passed else '[red]FAILED'}[/]")
    console.print(f"  Score: {review.score}/100\n")


@main.command()
def status() -> None:
    """Show agent status."""
    console.print("\n[bold]Morpheus Agent Status[/bold]")
    console.print("  Agents: 0 active")
    console.print("  Tasks: 0 queued\n")


if __name__ == "__main__":
    main()
