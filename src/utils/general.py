import json
import logging
import random
import re
import shutil
import time
import warnings
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Finds the repository root directory relative to this script/notebook."""
    # If running inside a script in src/, parent is root.
    # Adjust anchor file if needed, or search up for a marker like pyproject.toml
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    return current  # Fallback to current working directory


def load_prompt(filename: str) -> str:
    """Loads a prompt file relative to the project root directory."""
    root = get_project_root()
    prompt_path = root / "prompts" / filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found at: {prompt_path.resolve()}")
    return prompt_path.read_text(encoding="utf-8")


class BWORProblem(BaseModel):
    id: str
    en_question: str
    cn_question: str
    answer: float | None = None
    solution_status: str
    domain: str
    problem_type: str
    difficulty: str


def load_random_problem(
    jsonl_path: str = "problems/data/test.jsonl",
    line_id: int = -1,
    max_retries: int = 5,
) -> BWORProblem:
    """Reads the JSONL file and returns a BWOR problem instance."""
    root = get_project_root()
    path = root / jsonl_path
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at {path.resolve()}")

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError(f"No valid lines found in dataset at {path.resolve()}")

    # Handle explicit line index request
    if line_id != -1:
        if 0 <= line_id < len(lines):
            data = json.loads(lines[line_id])
            return BWORProblem(**data)
        else:
            raise IndexError(
                f"line_id {line_id} out of bounds for file with {len(lines)} lines."
            )

    # Retry loop for random selection in case malformed entries exist
    for attempt in range(max_retries):
        selected_line = random.choice(lines)
        try:
            data = json.loads(selected_line)
            return BWORProblem(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            problem_id = data.get("id", "UNKNOWN") if "data" in locals() else "UNKNOWN"
            logger.warning(
                f"Failed to instantiate BWORProblem (ID: {problem_id}): {e}. Retrying ({attempt + 1}/{max_retries})..."
            )
            time.sleep(1)

    raise RuntimeError(
        f"Failed to load a valid BWORProblem after {max_retries} attempts."
    )


def save_solution_artifact(
    problem_id: str, content: str | BaseModel | dict, artifact_type: str
) -> Path:
    """
    Saves solution artifacts (markdown, python code, or json execution results) to disk.
    artifact_type: 'markdown', 'code', or 'results'
    """
    # Map artifact types to file extensions
    ext_map = {"markdown": "md", "code": "py", "result": "json"}
    ext = ext_map.get(artifact_type, artifact_type)

    directory = Path(f"solutions/{artifact_type}")
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / f"{problem_id}.{ext}"

    # Handle Pydantic objects or dicts for JSON outputs
    if isinstance(content, BaseModel):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content.model_dump(mode="json"), f, indent=4)
    elif isinstance(content, dict):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
    else:
        # String content (Markdown / Python Code)
        file_path.write_text(str(content).strip(), encoding="utf-8")

    return file_path


def extract_python_code(llm_output: str) -> str:
    """Extracts raw code from inside ```python ... ``` fences."""
    pattern = r"```python\s*(.*?)\s*```"
    match = re.search(pattern, llm_output, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback if the LLM omitted fences
    cleaned = llm_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()

    return cleaned


def get_event_text(events: Any) -> str:
    """Extracts text content from a list of ADK Events."""
    text_parts = []
    for event in events:
        # Check if the event contains content and parts
        if (
            hasattr(event, "content")
            and event.content
            and hasattr(event.content, "parts")
        ):
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    text_parts.append(part.text)
    return "\n".join(text_parts)


def extract_tag_content(text: str, tag_name: str) -> str | None:
    """Extracts content inside <tag_name>...</tag_name> blocks."""
    pattern = rf"<{tag_name}>\s*(.*?)\s*</{tag_name}>"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # Return None if unchanged or empty
        if content and content.upper() != "UNCHANGED":
            return content
    return None


def clean_experiment_directories():
    """Wipes historical run artifacts before running top-level loop J."""
    targets = [
        Path("solutions/markdown"),
        Path("solutions/code"),
        Path("solutions/result"),
        Path("solutions/epoch"),
        Path("prompts/versions"),
    ]
    for target in targets:
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)
    print("🧹 Cleared solutions/ and prompts/versions/ directories.")


def clean_experiment_files(epoch_nr: int):
    """Safely moves experiment artifacts >= epoch_nr to a trash directory."""
    targets = [
        Path("solutions/markdown"),
        Path("solutions/code"),
        Path("solutions/result"),
        Path("solutions/epoch"),
        Path("prompts/versions"),
    ]

    trash_dir = Path(".trash") / f"epoch_clean_{epoch_nr}"
    trash_dir.mkdir(parents=True, exist_ok=True)

    removed_count = 0

    for target in targets:
        if not target.exists():
            continue

        for file in target.iterdir():
            if not file.is_file():
                continue

            match = re.search(r"[_v]v?(\d+)$", file.stem)
            if match:
                file_version = int(match.group(1))
                if file_version >= epoch_nr:
                    # Create matching directory structure inside .trash
                    destination = trash_dir / target.relative_to(".") / file.name
                    destination.parent.mkdir(parents=True, exist_ok=True)

                    shutil.move(file, destination)
                    removed_count += 1

    print(
        f"🧹 Moved {removed_count} artifacts (version >= v{epoch_nr}) to {trash_dir}."
    )




@dataclass
class EpochResults:
    all_solutions: int
    successful_solutions: int
    share_solved: float
    mae: float
    failed_batch_results: list[Any]


def get_epoch_results(batch_results: Sequence[Any]) -> EpochResults:
    """Evaluates epoch batch results, handling both numeric target answers

    and target_answer is None / null (infeasible problems).
    """
    all_solutions = len(batch_results)
    successful_solutions = 0
    errors = []
    failed_batch_results = []

    for br in batch_results:
        target_answer = br.target_answer
        stdout = br.exec_result.stdout or ""
        model_answer = None
        is_failed = False

        # --- CASE 1: Expected Infeasible Problem (Target Answer is None/null) ---
        if target_answer is None:
            # Model is correct if solver reported NO_FEASIBLE_SOLUTION
            if "NO_FEASIBLE_SOLUTION" in stdout:
                successful_solutions += 1
                # Note: No numerical relative error appended for infeasible problems
            else:
                is_failed = True

        # --- CASE 2: Expected Feasible Numerical Problem ---
        else:
            if br.exec_result.success:
                # Extract numerical value after OPTIMAL_VALUE: using regex
                match = re.search(
                    r"OPTIMAL_VALUE:\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)",
                    stdout,
                )

                if match:
                    try:
                        model_answer = float(match.group(1))

                        # Calculate relative error (safely handle target_answer == 0)
                        if abs(target_answer) > 1e-9:
                            rel_error = abs(target_answer - model_answer) / abs(
                                target_answer
                            )
                        else:
                            rel_error = abs(model_answer)

                        # Fail if deviation is strictly greater than 5%
                        if rel_error > 0.05:
                            is_failed = True
                        else:
                            successful_solutions += 1
                            errors.append(min(10.0, rel_error))

                    except ValueError:
                        is_failed = True
                else:
                    # Executed cleanly (exit code 0), but missed OPTIMAL_VALUE print pattern
                    is_failed = True
            else:
                # Script execution failed (traceback, syntax error, etc.)
                is_failed = True

        if is_failed:
            failed_batch_results.append(br)

        # status = "❌ FAIL" if is_failed else "✅ PASS"
        # print(
        #     f"Replayed [{br.problem_id}_{br.version_tag}]: {status} "
        #     f"(Target: {target_answer}) (Answer: {model_answer})"
        # )

    # Compute MAE based on numerical error count
    mae = (sum(errors) / len(errors)) if len(errors) > 0 else 10.0
    mae = min(10.0, mae)
    share_solved = (successful_solutions / all_solutions) if all_solutions > 0 else 0.0

    return EpochResults(
        all_solutions=all_solutions,
        successful_solutions=successful_solutions,
        share_solved=share_solved,
        mae=mae,
        failed_batch_results=failed_batch_results,
    )


def silence() -> None:
    """Turn down library chatter so the agent's own trace is easy to read.

    ADK prints a handful of [EXPERIMENTAL] feature notices, and google-genai logs a
    line every time it sees both GOOGLE_API_KEY and GEMINI_API_KEY in the
    environment (harmless, left over from the CrewAI week). None of it is ours to
    act on, so we quiet it. Call silence() before importing ADK.
    """
    warnings.filterwarnings("ignore", message=r".*\[EXPERIMENTAL\].*")
    logging.getLogger("google_genai._api_client").setLevel(logging.ERROR)
