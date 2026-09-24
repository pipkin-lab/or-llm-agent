import sys
import subprocess
import tempfile
from pathlib import Path

def execute_solver_script(python_code: str) -> dict:
    """
    Executes generated OR-Tools or Pyomo code in an isolated subprocess.
    Returns standard output, error trace, and return code.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tf:
        tf.write(python_code)
        temp_path = tf.name

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Execution timed out", "returncode": -1}
    finally:
        Path(temp_path).unlink(missing_ok=True)
