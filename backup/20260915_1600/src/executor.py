import subprocess
import sys
import tempfile
from pathlib import Path

from pydantic import BaseModel


class ExecutionResult(BaseModel):
    success: bool
    stdout: str
    stderr: str
    returncode: int


def run_generated_code(cleaned_code: str, timeout_seconds: int = 90) -> ExecutionResult:
    """
    Executes generated OR-Tools/Pyomo Python code in an isolated subprocess.
    Captures stdout (solver results) and stderr (tracebacks for Step 5).
    """

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(cleaned_code)
        temp_path = tf.name

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return ExecutionResult(
            success=(result.returncode == 0),
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
            returncode=result.returncode,
        )
    except subprocess.TimeoutExpired:
        return ExecutionResult(
            success=False,
            stdout="",
            stderr=f"Execution timed out after {timeout_seconds} seconds.",
            returncode=-1,
        )
    finally:
        Path(temp_path).unlink(missing_ok=True)
