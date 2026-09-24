import json
import random
from pathlib import Path
from pydantic import BaseModel

class BWORProblem(BaseModel):
    id: str
    en_question: str
    cn_question: str
    answer: float
    solution_status: str
    domain: str
    problem_type: str
    difficulty: str

def load_random_problem(jsonl_path: str = "problems/data/test.jsonl") -> BWORProblem:
    """Reads the JSONL file and returns a random BWOR problem instance."""
    path = Path(jsonl_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at {path.resolve()}")

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    selected_line = random.choice(lines)
    data = json.loads(selected_line)
    return BWORProblem(**data)
