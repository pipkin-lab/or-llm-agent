import asyncio
from dataclasses import dataclass

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

from executor import ExecutionResult, run_generated_code
from or_llm_agent.utils import (
    extract_python_code,
    get_event_text,
    save_solution_artifact,
)


@dataclass
class PipelineResult:
    problem_id: str
    version_tag: str
    target_answer: float
    markdown_model: str
    python_code: str
    exec_result: ExecutionResult


class ORPipeline:
    def __init__(
        self, model, math_prompt: str, code_prompt: str, version_tag: str = "v0"
    ):
        self.model = model
        self.version_tag = version_tag
        self.math_prompt = math_prompt
        self.code_prompt = code_prompt

        # Instantiate Agents dynamically with injected prompts
        self.math_agent = LlmAgent(
            model=self.model, name="math_agent", instruction=self.math_prompt
        )
        self.code_agent = LlmAgent(
            model=self.model, name="code_agent", instruction=self.code_prompt
        )

    async def _solve_async(self, problem) -> PipelineResult:
        # Step 1: Formulation & Math Modeling
        formulation_prompt = (
            f"Analyze and model this OR problem:\n{problem.en_question}"
        )
        res_1_events = await InMemoryRunner(agent=self.math_agent).run_debug(
            formulation_prompt
        )
        markdown_model = get_event_text(res_1_events)

        # Version-aware artifact saving
        save_solution_artifact(
            f"{problem.id}_{self.version_tag}", markdown_model, "markdown"
        )

        # Step 2: Code Generation
        code_prompt = f"Convert this mathematical model into Google OR-Tools Python code:\n{markdown_model}"
        res_2_events = await InMemoryRunner(agent=self.code_agent).run_debug(
            code_prompt
        )
        raw_code = get_event_text(res_2_events)
        python_code = extract_python_code(raw_code)

        # Version-aware artifact saving
        save_solution_artifact(f"{problem.id}_{self.version_tag}", python_code, "code")

        # Step 3: Subprocess Execution
        exec_res = run_generated_code(python_code)
        save_solution_artifact(f"{problem.id}_{self.version_tag}", exec_res, "result")

        return PipelineResult(
            problem_id=problem.id,
            version_tag=self.version_tag,
            target_answer=problem.answer,
            markdown_model=markdown_model,
            python_code=python_code,
            exec_result=exec_res,
        )

    def solve(self, problem) -> PipelineResult:
        """Synchronous entry point wrapping internal async runner."""
        return asyncio.run(self._solve_async(problem))
