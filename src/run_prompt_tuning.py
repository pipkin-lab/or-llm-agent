
import asyncio
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner

from utils.general import (
    clean_experiment_files,
    extract_tag_content,
    get_epoch_results,
    get_event_text,
    load_prompt,
    load_random_problem,
)
from utils.pipeline import ORPipeline

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

    # Batch Loop - load and solve the problem
    for i in range(BATCH_SIZE):
        problem = load_random_problem("problems/data/test.jsonl")
        print(f"[{i + 1}/{BATCH_SIZE}] Problem: {problem.id}")

        res = pipeline.solve(problem)
        batch_results.append(res)

        status = "✅ PASS" if res.exec_result.success else "❌ FAIL"
        print(f"  Result: {status}")

    epoc_rec = get_epoch_results(batch_results)
    print(
        f"Epoch {j}: Total={epoc_rec.all_solutions}, Solved={epoc_rec.successful_solutions}, Share={epoc_rec.share_solved:.2%}, MAE={epoc_rec.mae:.2%}"
    )


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


    # RUN Meta-Optimizer Agent
    # init, prepare prompt, parse output, save new instructions
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
