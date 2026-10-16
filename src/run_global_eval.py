
import json
from pathlib import Path

import pandas as pd
from google.adk.models.lite_llm import LiteLlm

from utils.executor import ExecutionResult
from utils.general import (
    get_epoch_results,
    get_project_root,
    load_prompt,
)
from utils.pipeline import ORPipeline, PipelineResult

# 1. Base Model for Standard Agents (Math Agent & Code Agent)
# Disables prompt caching and forces zero reasoning budget
FAST_MODEL = LiteLlm(
    model="openai/qwen38_q3",
    api_base="http://localhost:8000/v1",
    api_key="not-needed",
    temperature=0.7,
    timeout=600,  # 30-minute timeout so long 8k+ generation runs complete
    max_tokens=16384,  # Large window for total generation 16384
    extra_body={
        "cache_prompt": False,  # Tells llama-server to skip saving/looking up prompt cache
        "reasoning_budget": 0,  # Disables reasoning/thinking tokens
        "chat_template_kwargs": {"enable_thinking": False},
    },
)

# 2. Advanced Model for Meta-Optimizer (Smarter Agent)
# Enables reasoning budget for deep reflection
REASONING_MODEL = LiteLlm(
    model="openai/qwen38_q3",
    api_base="http://localhost:8000/v1",
    api_key="not-needed",
    temperature=0.7,
    timeout=1800,  # 30-minute timeout so long 8k+ generation runs complete
    max_tokens=16384,  # Large window for total generation 16384
    extra_body={
        "cache_prompt": False,  # Still skip prompt cache overhead
        "reasoning_budget": 8192,  # Allows up to 8192 thinking tokens for prompt refinement
        "chat_template_kwargs": {
            "enable_thinking": True,
            "reasoning_effort": "medium",  # Prevents runaway thinking loops!
        },
    },
)


NUMBER_OF_PROBLEMS = 82
COLUMNS = ["problem_id", "version_tag", "target_answer", "success", "mae"]
records = []


# MAIN LOOP
for j in ["00",  "0", "13"]:
    version_tag = f"v{j}"
    print(
        f"\n==================== STARTING EVAL {j} ({version_tag}) ===================="
    )

    # Load prompts
    current_math_prompt = load_prompt(f"versions/math_agent_v{j}.txt")
    current_code_prompt = load_prompt(f"versions/code_agent_v{j}.txt")

    # Instantiate Pipeline with active prompt versions
    pipeline = ORPipeline(
        model=FAST_MODEL,
        math_prompt=current_math_prompt,
        code_prompt=current_code_prompt,
        version_tag=version_tag,
    )

    batch_results = []

    # Replay/Debug Loop: Reconstruct PipelineResult directly from saved files

    # 1. Load problem dataset into a lookup map for target_answer
    with open(
        Path(get_project_root()) / "problems/data/test.jsonl", "r", encoding="utf-8"
    ) as f:
        problems_raw = [json.loads(line) for line in f if line.strip()]

    target_answers = {p["id"]: p.get("answer", None) for p in problems_raw if "id" in p}
    # print(target_answers)

    # 2. Discover execution result files for the given version_tag
    dir_path = Path(get_project_root()) / "solutions/result"
    matching_files = list(dir_path.glob(f"*_{version_tag}.json"))

    batch_results = []
    eval_rec_result = []
    print(
        f"--- Replaying existing results for {version_tag} ({len(matching_files)} solutions found) ---"
    )

    for result_file in matching_files:
        # Extract problem_id (e.g., "BWOR-001_v12.json" -> "BWOR-001")
        problem_id = result_file.stem.replace(f"_{version_tag}", "")

        # Load ExecutionResult
        with open(result_file, "r", encoding="utf-8") as f:
            exec_raw = json.load(f)

        exec_result = ExecutionResult(
            success=exec_raw["success"],
            stdout=exec_raw["stdout"],
            stderr=exec_raw["stderr"],
            returncode=exec_raw["returncode"],
        )

        # Load associated Markdown and Code files
        md_path = (
            Path(get_project_root())
            / f"solutions/markdown/{problem_id}_{version_tag}.md"
        )
        code_path = (
            Path(get_project_root()) / f"solutions/code/{problem_id}_{version_tag}.py"
        )

        markdown_model = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        python_code = (
            code_path.read_text(encoding="utf-8") if code_path.exists() else ""
        )

        # Reconstruct PipelineResult
        res = PipelineResult(
            problem_id=problem_id,
            version_tag=version_tag,
            target_answer=target_answers.get(problem_id, 0.0),
            markdown_model=markdown_model,
            python_code=python_code,
            exec_result=exec_result,
        )
        batch_results.append(res)

        eval_rec_result.append(get_epoch_results([res]))

        # Inside the loop:
        records.append(
            {
                "problem_id": res.problem_id,
                "version_tag": res.version_tag,
                "target_answer": res.target_answer,
                "successful_solutions": eval_rec_result[-1].successful_solutions,
                "mae": eval_rec_result[-1].mae,
            }
        )

# After the loop finishes:
df = pd.DataFrame(records)
df.to_csv("solutions/eval/run_eval_final.csv", index=False)
