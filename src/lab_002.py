
import asyncio
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner

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


NUM_EPOCHS = 30  # Outer Loop J
BATCH_SIZE = 5  # Inner Loop I

START = 10

# clean up previous epochs, if START=0 - all files will be removed
clean_experiment_files(START)

if START == 0:
    # Typically we will never run version 0
    current_math_prompt = load_prompt("math_agent.txt")
    current_code_prompt = load_prompt("code_agent.txt")
    Path("prompts/versions/math_agent_v0.txt").write_text(
        current_math_prompt, encoding="utf-8"
    )
    Path("prompts/versions/code_agent_v0.txt").write_text(
        current_code_prompt, encoding="utf-8"
    )
else:
    # Initialize base prompt strings
    current_math_prompt = load_prompt(f"versions/math_agent_v{START - 1}.txt")
    current_code_prompt = load_prompt(f"versions/code_agent_v{START - 1}.txt")

meta_optimizer_instruction = load_prompt("meta_optimizer.txt")

# MAIN LOOP
for j in range(START, NUM_EPOCHS):
    version_tag = f"v{j}"
    print(
        f"\n==================== STARTING EPOCH {j} ({version_tag}) ===================="
    )

    # Instantiate Pipeline with active prompt versions
    pipeline = ORPipeline(
        model=FAST_MODEL,
        math_prompt=current_math_prompt,
        code_prompt=current_code_prompt,
        version_tag=version_tag,
    )

    batch_results = []

    ############################
    # MAIN Inner Batch Loop
    ############################
    for i in range(BATCH_SIZE):
        problem = load_random_problem("problems/data/test.jsonl")
        print(f"[{i + 1}/{BATCH_SIZE}] Problem: {problem.id}")

        res = pipeline.solve(problem)
        batch_results.append(res)

        status = "✅ PASS" if res.exec_result.success else "❌ FAIL"
        print(f"  Result: {status}")

    # ###########################
    # # DEBUGGING Inner Batch Loop
    # ###########################
    # # Replay/Debug Loop: Reconstruct PipelineResult directly from saved files
    # import json

    # from executor import ExecutionResult
    # from or_llm_agent.utils import get_project_root
    # from pipeline import PipelineResult

    # # 1. Load problem dataset into a lookup map for target_answer
    # with open(
    #     Path(get_project_root()) / "problems/data/test.jsonl", "r", encoding="utf-8"
    # ) as f:
    #     problems_raw = [json.loads(line) for line in f if line.strip()]

    # target_answers = {p["id"]: p.get("answer", 0.0) for p in problems_raw if "id" in p}
    # print(target_answers)

    # # 2. Discover execution result files for the given version_tag
    # dir_path = Path(get_project_root()) / "solutions/result"
    # matching_files = list(dir_path.glob(f"*_{version_tag}.json"))

    # batch_results = []
    # print(
    #     f"--- Replaying existing results for {version_tag} ({len(matching_files)} solutions found) ---"
    # )

    # for result_file in matching_files:
    #     # Extract problem_id (e.g., "BWOR-001_v12.json" -> "BWOR-001")
    #     problem_id = result_file.stem.replace(f"_{version_tag}", "")

    #     # Load ExecutionResult
    #     with open(result_file, "r", encoding="utf-8") as f:
    #         exec_raw = json.load(f)

    #     exec_result = ExecutionResult(
    #         success=exec_raw["success"],
    #         stdout=exec_raw["stdout"],
    #         stderr=exec_raw["stderr"],
    #         returncode=exec_raw["returncode"],
    #     )

    #     # Load associated Markdown and Code files
    #     md_path = (
    #         Path(get_project_root())
    #         / f"solutions/markdown/{problem_id}_{version_tag}.md"
    #     )
    #     code_path = (
    #         Path(get_project_root()) / f"solutions/code/{problem_id}_{version_tag}.py"
    #     )

    #     markdown_model = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    #     python_code = (
    #         code_path.read_text(encoding="utf-8") if code_path.exists() else ""
    #     )

    #     # Reconstruct PipelineResult
    #     res = PipelineResult(
    #         problem_id=problem_id,
    #         version_tag=version_tag,
    #         target_answer=target_answers.get(problem_id, 0.0),
    #         markdown_model=markdown_model,
    #         python_code=python_code,
    #         exec_result=exec_result,
    #     )
    #     batch_results.append(res)

    #     status = "✅ PASS" if exec_result.success else "❌ FAIL"
    #     print(
    #         f"Replayed [{problem_id}_{version_tag}]: {status} (Target: {res.target_answer})"
    #     )

    # # print(batch_results)
    # # STOP DEBUGGING

    ############################
    # CLEAN solutions
    ############################
    # # Track epoch performance stats
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

    # # Epoch statistics metrics
    # mae = (sum(errors) / successful_solutions) if successful_solutions > 0 else 10.0
    # mae = min(10.0, mae)
    # share_solved = (successful_solutions / all_solutions) if all_solutions > 0 else 0.0

    epoc_rec = get_epoch_results(batch_results)
    print(
        f"Epoch {j}: Total={epoc_rec.all_solutions}, Solved={epoc_rec.successful_solutions}, Share={epoc_rec.share_solved:.2%}, MAE={epoc_rec.mae:.2%}"
    )


    #####################
    # GENERATE INPUTS   #
    #####################

    # Build reduced-context summary string strictly for Meta-Optimizer
    summary_lines = [
        f"Batch Execution Results for Failed Solutions (Epoch {j}):",
        "Failed Solutions are defined as scripts returning errors, missing OPTIMAL_VALUE in stdout, or exceeding 5% deviation from target.\n",
    ]

    for r in epoc_rec.failed_batch_results:
        summary_lines.append(f"Problem ID: {r.problem_id}")
        summary_lines.append(f"Target Answer: {r.target_answer}")
        summary_lines.append(f"Execution Success: {r.exec_result.success}")

        if not r.exec_result.success:
            summary_lines.append(f"Error Traceback:\n{r.exec_result.stderr.strip()}")
        else:
            summary_lines.append(f"Output:\n{r.exec_result.stdout.strip()}")

        summary_lines.append(
            f"Mathematical Optimization Model:\n{r.markdown_model.strip()}"
        )
        summary_lines.append(f"Python Script:\n{r.python_code.strip()}\n" + "-" * 40)

    summary_text = "\n".join(summary_lines)

    epoch_results_text = (
        f"Epoch Results {j}:\n"
        f"Number of problems: {epoc_rec.all_solutions}\n"
        f"Number of solved problems: {epoc_rec.successful_solutions}\n"
        f"Share of solved problems: {int(epoc_rec.share_solved * 100)}%\n"
        f"Mean Absolute Error: {int(epoc_rec.mae * 100)}%\n"
    )
    Path(f"solutions/epoch/run_{version_tag}.txt").write_text(
        epoch_results_text, encoding="utf-8"
    )

    # Previous epoch results
    previous_epoch_results_text = "no previous epoch results"
    previous_math_prompt = "no previous math agent instructions"
    previous_code_prompt = "no previous code agent instructions"
    previous_changelogs = "no previous changelogs"
    if j > 0:
        content = Path(f"solutions/epoch/run_v{j - 1}.txt").read_text(encoding="utf-8")
        previous_epoch_results_text = f"Epoch {j-1} Results:\n{content}\n"

        content = Path(f"prompts/versions/math_agent_v{j - 1}.txt").read_text(encoding="utf-8")
        previous_math_prompt = f"Epoch {j-1} Math Agent Instructions:\n{content}\n"

        content = Path(f"prompts/versions/code_agent_v{j - 1}.txt").read_text(encoding="utf-8")
        previous_code_prompt = f"Epoch {j-1} Code Agent Instructions:\n{content}\n"

        # Option: Pass the last 3-5 changelogs to keep context crisp
        max_history = 5
        start_idx = max(0, j - max_history)
        
        list_previous_changelogs = []
        for i in range(start_idx, j):
            log_content = Path(f"solutions/epoch/changelog_v{i}.txt").read_text(encoding="utf-8")
            list_previous_changelogs.append(f"--- CHANGELOG EPOCH {i} ---\n{log_content}")
            
        previous_changelogs = "\n\n".join(list_previous_changelogs)


    # Run Meta-Optimizer Agent
    optimizer_agent = LlmAgent(
        model=REASONING_MODEL,
        name="meta_optimizer",
        instruction=meta_optimizer_instruction,
        timeout=30 * 60,
    )

    optimizer_prompt = f"""

    {previous_math_prompt}

    {previous_code_prompt}

    {previous_epoch_results_text}

    {previous_changelogs}

    Current Math Agent Instructions:
    {current_math_prompt}

    Current Code Agent Instructions:
    {current_code_prompt}

    {epoch_results_text}

    {summary_text}
    """

    opt_events = asyncio.run(
        InMemoryRunner(agent=optimizer_agent).run_debug(optimizer_prompt)
    )
    opt_response = get_event_text(opt_events)

    math_prompt = extract_tag_content(opt_response, "math_agent_instructions")
    if math_prompt:
        current_math_prompt = math_prompt

    code_prompt = extract_tag_content(opt_response, "code_agent_instructions")
    if code_prompt:
        current_code_prompt = code_prompt

    # Brute force clean curly brackets
    current_math_prompt = current_math_prompt.replace("{", "<curly_brackets>").replace(
        "}", "</curly_brackets>"
    )
    current_code_prompt = current_code_prompt.replace("{", "<curly_brackets>").replace(
        "}", "</curly_brackets>"
    )

    # Save active prompt snapshot
    Path(f"prompts/versions/math_agent_{version_tag}.txt").write_text(
        current_math_prompt, encoding="utf-8"
    )
    Path(f"prompts/versions/code_agent_{version_tag}.txt").write_text(
        current_code_prompt, encoding="utf-8"
    )

    # Save changelog
    changelog = extract_tag_content(opt_response, "changelog") or "None"
    Path(f"solutions/epoch/changelog_{version_tag}.txt").write_text(
        changelog, encoding="utf-8"
    )

    # TODO: when run in debug - save current_math_prompt & code_prompt

    # # Parse tags and update prompt strings for epoch j+1
    # updates = parse_and_apply_prompt_updates(
    #     llm_output=opt_response,
    #     prompts_dir="prompts",
    #     version_tag=f"v{j+1}"
    # )

    # # Reload updated prompts if modified by optimizer
    # if updates["math_agent"]:
    #     current_math_prompt = Path("prompts/math_agent.txt").read_text(encoding="utf-8")
    # if updates["code_agent"]:
    #     current_code_prompt = Path("prompts/code_agent.txt").read_text(encoding="utf-8")



    # # Define only clean solutions
    # all_solutions = 0
    # successful_solutions = 0
    # solutions = []
    # batch_results_with_potential = []
    # for br in batch_results:
    #     is_potential = False
    #     target_answer = br.target_answer
    #     all_solutions += 1
    #     successful_solutions += 1
    #     try:
    #         extract_optimal_value = br.exec_result.stdout.replace("OPTIMAL_VALUE: ", "")
    #         extract_optimal_value = extract_optimal_value.replace("\n", " ")
    #         if len(extract_optimal_value.split(" ")) > 1:
    #             # print("multiple values")
    #             model_answer = float(extract_optimal_value.split(" ")[0])
    #         else:
    #             model_answer = float(extract_optimal_value)
    #         if abs(target_answer - model_answer) / abs(target_answer) > 0.05:
    #             is_potential = True
    #         solutions.append(
    #             [
    #                 target_answer,
    #                 model_answer,
    #                 abs(target_answer - model_answer) / abs(target_answer),
    #             ]
    #         )
    #     except:
    #         is_potential = True
    #         successful_solutions -= 1
    #     batch_results_with_potential.append(br)
    # if successful_solutions > 0:
    #     target = [f[0] for f in solutions]
    #     model = [f[1] for f in solutions]
    #     per = [min(10.0, f[-1]) for f in solutions]
    #     mae = sum(per) / successful_solutions
    # else:
    #     mae = 10
    # # print(j, all_solutions, successful_solutions, mae)
    # # print(target, model, per)
    # mae = min(10.0, mae)
    # share_solved = successful_solutions / all_solutions
    # print(j, all_solutions, successful_solutions, share_solved, mae)

    # # Format batch summary for Meta-Optimizer
    # summary_text = ""
    # if len(batch_results_with_potential) > 0:
    #     summary_text = f"Batch Execution Results for Failed Solutions (Epoch {j}):\n"
    #     summary_text += "Failed Solutions defined either as stdout without OPTIMAL_VALUE or 5% deviation from target answer.\n"
    #     for r in batch_results_with_potential:
    #         summary_text += f"\nProblem ID: {r.problem_id}\n"
    #         summary_text += f"Target Answer: {r.target_answer}\n"
    #         summary_text += f"Execution Success: {r.exec_result.success}\n"
    #         if not r.exec_result.success:
    #             summary_text += f"Error Traceback:\n{r.exec_result.stderr}\n"
    #         else:
    #             summary_text += f"Output:\n{r.exec_result.stdout}\n"

    #         summary_text += f"Mathematical Optimization Model:\n{r.markdown_model}\n"
    #         summary_text += f"Python Script:\n{r.python_code}\n"

    # epoch_results_text = f"Epoch Results {j}:\n"
    # epoch_results_text += f"Number of problems: {all_solutions}\n"
    # epoch_results_text += f"Number of solved problems: {successful_solutions}\n"
    # epoch_results_text += f"Share of solved problems: {int(share_solved * 100)}%\n"
    # epoch_results_text += f"Mean  Absolute Error: {int(mae * 100)}%\n"

    # Path(f"solutions/epoch/run_v{j}.txt").write_text(
    #     epoch_results_text, encoding="utf-8"
    # )
