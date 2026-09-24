import os
import asyncio

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from quiet import silence
silence()  # turn down some noisy library logging so the agent's trace is easy to read

# import os
from pathlib import Path

# from google.adk.agents import LlmAgent
# from google.adk.runners import InMemoryRunner
from google.adk.models.lite_llm import LiteLlm

from or_llm_agent.utils import load_random_problem
from typing import Any
from google.adk.runners import InMemoryRunner
# from src.dataset import load_random_problem
from executor import run_generated_code

from google.adk.runners import InMemoryRunner
from or_llm_agent.utils import load_prompt, load_random_problem, save_solution_artifact, get_event_text, extract_python_code
from executor import run_generated_code


# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(
#     base_url="http://localhost:8000/v1",  # Change port depending on your local provider
#     api_key="not-needed",                 # A non-empty string is required by the SDK
#     model="ollama/qwen38_q3",        # Specify the exact model loaded in your backend
#     temperature=0.7
# )


# # from openai import OpenAI
# def init_openai():
#     openai = OpenAI(
#         base_url="http://localhost:8000/v1",
#         api_key="local-pipeline"
#     )
#     return openai

# openai = init_openai()
# # response = openai.chat.completions.create(model="qwen38_q3", messages=messages)

from google.adk.models.lite_llm import LiteLlm

# 1. Define your custom local model connection
MODEL = LiteLlm(
    model="openai/qwen38_q3",               # "openai/" prefix tells LiteLLM to use OpenAI API specs
    api_base="http://localhost:8000/v1",    # Your llama.server / vLLM endpoint
    api_key="not-needed",
    temperature=0.7
)




# 3. Create Agents for Pipeline

math_modeler = LlmAgent(
    model=MODEL,
    name="math_modeler",
    instruction=load_prompt("math_agent.txt")
)

coder = LlmAgent(
    model=MODEL,
    name="coder",
    instruction=load_prompt("code_agent.txt")
)

# coordinator = LlmAgent(
#     model=MODEL,
#     name="coordinator",
#     instruction=load_prompt("step5_coordinator.txt")
# )



async def agent_math_modeler():
    # Step 1: Formulation
    print("--- STEP 1: Formulation ---")
    formulation_prompt = f"""
    Analyze and formulate this Operations Research problem:
    id: {problem.id}
    question: {problem.en_question}
    """
    res_1_events = await InMemoryRunner(agent=math_modeler).run_debug(formulation_prompt)
    return res_1_events

async def agent_coder(markdown_model):
    code_prompt = f"Convert this mathematical model into Google OR-Tools Python code:\n{markdown_model}"
    res_2_events = await InMemoryRunner(agent=coder).run_debug(code_prompt)
    return res_2_events


if __name__ == "__main__":

    # Load problem
    problem = load_random_problem("problems/data/test.jsonl", 56)
    print(f"Problem ID: {problem.id} | Domain: {problem.domain} | Target: {problem.answer}\n Questions: {problem.en_question}\n")

    # # Formulate problem
    # # res_1_events = agent_math_modeler()
    # res_1_events = asyncio.run(agent_math_modeler())
    # # try:
    # #     res_1_events = agent_math_modeler()
    # # except Exception as exc:
    # #     print("Could not Formulate problem")
    # #     return f"Could not Formulate problem"

    # markdown_model = get_event_text(res_1_events)

    # # Save Markdown model
    # save_solution_artifact(problem.id, markdown_model, "markdown")

    path = f"/mnt/datafast/Development/or-llm-agent/solutions/markdown/{problem.id}_v0.md"
    with open(path, "r", encoding="utf-8") as f:
        markdown_model = f.read()
    print(markdown_model)

    # 3. Step 2: Code Generation
    # res_2_events = agent_coder(markdown_model)
    res_2_events = asyncio.run(agent_coder(markdown_model))
    print(get_event_text(res_2_events))
    python_code = extract_python_code(get_event_text(res_2_events))

    # # Save Python code
    # save_solution_artifact(problem.id, python_code, "code")

    # path = f"/mnt/datafast/Development/or-llm-agent/solutions/code/{problem.id}.py"
    # with open(path, "r", encoding="utf-8") as f:
    #     python_code = f.read()
    # # print(python_code)

    # # 4. Step 3: Subprocess Execution
    # exec_res = run_generated_code(python_code)

    # if exec_res.success:
    #     print(f"✅ Success! Solver Output:\n{exec_res.stdout}")
    # else:
    #     print(f"⚠️ Execution Failed:\n{exec_res.stderr}")
    #     # Trigger Coordinator Agent (Step 5) with exec_res.stderr if needed
