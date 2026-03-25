"""Tests for Morpheus core functionality."""

from morpheus.core import CodingAgent, TaskDecomposer, CodeGenerator, ReviewPipeline, Task
from morpheus.orchestrator import AgentOrchestrator
from morpheus.planner import TaskPlanner


class TestTaskDecomposer:
    def test_decompose_api_task(self) -> None:
        d = TaskDecomposer()
        tasks = d.decompose("Build a REST API for users")
        assert len(tasks) >= 3
        assert tasks[0].task_id == "task-1"

    def test_prioritize(self) -> None:
        d = TaskDecomposer()
        tasks = d.decompose("Build a web frontend")
        ordered = d.prioritize(tasks)
        assert ordered[0].dependencies == []


class TestCodeGenerator:
    def test_generate_model(self) -> None:
        gen = CodeGenerator()
        task = Task(description="Define data models for users")
        code = gen.generate(task)
        assert "BaseModel" in code.content

    def test_generate_endpoint(self) -> None:
        gen = CodeGenerator()
        task = Task(description="Create API endpoints for items")
        code = gen.generate(task)
        assert "router" in code.content


class TestReviewPipeline:
    def test_review_good_code(self) -> None:
        from morpheus.core import CodeBlock
        reviewer = ReviewPipeline()
        code = CodeBlock(language="python", content='"""Good code."""\n\ndef hello():\n    return "hi"\n')
        result = reviewer.review(code)
        assert result.passed is True

    def test_review_empty_code(self) -> None:
        from morpheus.core import CodeBlock
        reviewer = ReviewPipeline()
        code = CodeBlock(language="python", content="")
        result = reviewer.review(code)
        assert result.passed is False


class TestCodingAgent:
    def test_plan(self) -> None:
        agent = CodingAgent()
        tasks = agent.plan("Create a todo API")
        assert len(tasks) > 0

    def test_implement(self) -> None:
        agent = CodingAgent()
        task = Task(description="Implement user model", task_id="t1")
        code = agent.implement(task)
        assert code.content


class TestOrchestrator:
    def test_add_agent(self) -> None:
        orch = AgentOrchestrator()
        orch.add_agent("agent-1")
        assert orch.agent_count == 1

    def test_run_pipeline(self) -> None:
        orch = AgentOrchestrator()
        orch.add_agent("worker")
        tasks = [Task(description="Write tests", task_id="t1")]
        results = orch.run_pipeline(tasks)
        assert len(results) == 1

    def test_monitor_progress(self) -> None:
        orch = AgentOrchestrator()
        progress = orch.monitor_progress()
        assert progress["total_tasks"] == 0


class TestPlanner:
    def test_create_plan(self) -> None:
        planner = TaskPlanner()
        plan = planner.create_execution_plan("Build an e-commerce API")
        assert plan.estimated_steps > 0
        assert plan.goal == "Build an e-commerce API"
