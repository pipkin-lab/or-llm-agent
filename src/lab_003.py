
import asyncio
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner

import pandas as pd
import numpy as np

from or_llm_agent.utils import (
    clean_experiment_files,
    extract_tag_content,
    get_epoch_results,
    get_event_text,
    load_prompt,
    load_random_problem,
)
from pipeline import ORPipeline

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

    # ############################
    # # MAIN Inner Batch Loop
    # ############################
    # for i in range(NUMBER_OF_PROBLEMS):
    #     problem = load_random_problem("problems/data/test.jsonl", i)
    #     print(f"[{i + 1} of {NUMBER_OF_PROBLEMS}] Problem: {problem.id}")

    #     res = pipeline.solve(problem)
    #     batch_results.append(res)

    #     status = "✅ PASS" if res.exec_result.success else "❌ FAIL"
    #     print(f"  Result: {status}")

    ###########################
    # DEBUGGING Inner Batch Loop
    ###########################
    # Replay/Debug Loop: Reconstruct PipelineResult directly from saved files
    import json

    from executor import ExecutionResult
    from or_llm_agent.utils import get_project_root
    from pipeline import PipelineResult

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

        # status = "❌ FAIL" if is_failed else "✅ PASS"
        # print(
        #     f"Replayed [{br.problem_id}_{br.version_tag}]: {status} "
        #     f"(Target: {target_answer}) (Answer: {model_answer})"
        # )

        # status = "✅ PASS" if exec_result.success else "❌ FAIL"
        # print(
        #     f"Replayed [{problem_id}_{version_tag}]: {status} (Target: {res.target_answer})"
        # )

    # # # print(batch_results)
    # # # STOP DEBUGGING

    ############################
    # CLEAN solutions
    ############################
    # # Track eval performance stats
    # all_solutions = len(batch_results)
    # successful_solutions = 0
    # errors = []
    # failed_batch_results = []

    # for br in batch_results:
    #     target_answer = br.target_answer
    #     model_answer = None
    #     is_failed = False

    #     if br.exec_result.success:
    #         # Extract numerical value after OPTIMAL_VALUE: using regex
    #         match = re.search(
    #             r"OPTIMAL_VALUE:\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)",
    #             br.exec_result.stdout,
    #         )

    #         if match:
    #             try:
    #                 model_answer = float(match.group(1))

    #                 # Calculate relative error (safely handle target_answer == 0)
    #                 if abs(target_answer) > 1e-9:
    #                     rel_error = abs(target_answer - model_answer) / abs(
    #                         target_answer
    #                     )
    #                 else:
    #                     rel_error = abs(model_answer)

    #                 # Fail if deviation is strictly greater than 5%
    #                 if rel_error > 0.05:
    #                     is_failed = True
    #                 else:
    #                     successful_solutions += 1
    #                     errors.append(min(10.0, rel_error))

    #             except ValueError:
    #                 is_failed = True
    #         else:
    #             # Code executed cleanly (exit code 0), but missed the OPTIMAL_VALUE print pattern
    #             is_failed = True
    #     else:
    #         # Script execution failed (traceback, solver failure, syntax error)
    #         is_failed = True

    #     if is_failed:
    #         failed_batch_results.append(br)
        
    #     status = "❌ FAIL" if is_failed else "✅ PASS" 
    #     print(
    #         f"Replayed [{br.problem_id}_{br.version_tag}]: {status} (Target: {target_answer}) (Answer: {model_answer})"
    #     )

    # # eval statistics metrics
    # mae = (sum(errors) / successful_solutions) if successful_solutions > 0 else 10.0
    # mae = min(10.0, mae)
    # share_solved = (successful_solutions / all_solutions) if all_solutions > 0 else 0.0

    # eval_rec = get_epoch_results(batch_results)
    # print(
    #     f"Eval {j}: Total={eval_rec.all_solutions}, Solved={eval_rec.successful_solutions}, Share={eval_rec.share_solved:.2%}, MAE={eval_rec.mae:.2%}"
    # )


    # #####################
    # # GENERATE INPUTS   #
    # #####################

    # # Build reduced-context summary string strictly for Meta-Optimizer
    # summary_lines = [
    #     f"Batch Execution Results for Failed Solutions (Eval {j}):",
    #     "Failed Solutions are defined as scripts returning errors, missing OPTIMAL_VALUE in stdout, or exceeding 5% deviation from target.\n",
    # ]

    # for r in eval_rec.failed_batch_results:
    #     summary_lines.append(f"Problem ID: {r.problem_id}")
    #     summary_lines.append(f"Target Answer: {r.target_answer}")
    #     summary_lines.append(f"Execution Success: {r.exec_result.success}")

    #     if not r.exec_result.success:
    #         summary_lines.append(f"Error Traceback:\n{r.exec_result.stderr.strip()}")
    #     else:
    #         summary_lines.append(f"Output:\n{r.exec_result.stdout.strip()}")

    #     summary_lines.append(
    #         f"Mathematical Optimization Model:\n{r.markdown_model.strip()}"
    #     )
    #     summary_lines.append(f"Python Script:\n{r.python_code.strip()}\n" + "-" * 40)

    # summary_text = "\n".join(summary_lines)

    # eval_results_text = (
    #     f"eval Results {j}:\n"
    #     f"Number of problems: {eval_rec.all_solutions}\n"
    #     f"Number of solved problems: {eval_rec.successful_solutions}\n"
    #     f"Share of solved problems: {int(eval_rec.share_solved * 100)}%\n"
    #     f"Mean Absolute Error: {int(eval_rec.mae * 100)}%\n"
    # )
    # Path(f"solutions/eval/run_eval_{version_tag}.txt").write_text(
    #     eval_rec_result, encoding="utf-8"
    # )

# After the loop finishes:
df = pd.DataFrame(records)
df.to_csv("solutions/eval/run_eval_final.csv", index=False)
