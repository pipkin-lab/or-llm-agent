import os
import subprocess
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

# 1. Local Workspace & MCP Setup
WORKSPACE = Path("task_worker/workspace").resolve()
WORKSPACE.mkdir(parents=True, exist_ok=True)

filesystem_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(WORKSPACE)],
            cwd=str(WORKSPACE),
        ),
        timeout=60,
    ),
    errlog=subprocess.DEVNULL,
)

# 2. Local LLM Endpoint Setup
local_llm = LiteLlm(
    model="openai/qwen38_q3",
    api_base="http://localhost:8000/v1",
    api_key="not-needed",
    temperature=0.2,  # Low temperature for precise code/math generation
)

# 3. Execution Tool for Running Generated Code
def run_python_script(script_name: str) -> str:
    """Executes a python script inside the sandbox workspace using uv/python and returns execution output."""
    file_path = WORKSPACE / script_name
    if not file_path.exists():
        return f"Error: File {script_name} does not exist in workspace."
    
    try:
        # Runs using 'uv run' or fallback to system python
        result = subprocess.run(
            ["uv", "run", str(file_path)],
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        return output if output else "Script executed with no stdout output."
    except Exception as e:
        return f"Execution exception: {str(e)}"

# 4. OR Coder Agent (Step 2 -> Step 3)
or_coder_agent = LlmAgent(
    name="or_coder_agent",
    model=local_llm,
    instruction="""You are an Operations Research Software Engineer specializing in Google OR-Tools.
Your role:
1. Receive mathematical formulations of optimization problems.
2. Translate them into clean, self-contained Python scripts using `ortools.linear_solver.pywraplp`.
3. Save the Python script to the workspace file path using the filesystem tool.
4. Execute the script using `run_python_script`.
5. If execution results in an error, INFEASIBLE status, or bug, modify the script and try again.

Always format your script using standard pywraplp constructs:
```python
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')  # or SCIP for MILP
# Define variables, constraints, objective, solve, and print outputs explicitly.
"""
