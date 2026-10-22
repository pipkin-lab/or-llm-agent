# Operations Research LLM Agent

This project evaluates an LLM-driven operations-research workflow. A math agent turns a benchmark problem into a model, a code agent generates Python solver code, and the generated code is executed and scored against the problem's reference answer. A meta-optimizer can revise the math and code prompts between tuning epochs. For every epoch (5 random problems pr epoch) we store run results and changelog, i.e. reflections from meta-optimizer which can later be fed back to meta-optimizer so we can pick up threshold/signals across epochs. 

The tests are done on local Qwen 3.8 ([unsloth/Qwen3.8-27B-GGUF](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/tree/main)).

Inspired by [OR-Agent: Bridging Evolutionary Search and Structured Research for Automated Algorithm Discovery](https://arxiv.org/html/2602.13769v1)   
and corresponding [OR-Agent repo](https://github.com/qiliuchn/OR-Agent)


## Contents
- [Prompts](/prompts/versions/)
- [Problems](/problems/data/test.jsonl) 
- [Solutions Math Formulation](/solutions/markdown/) 
- [Solutions Code](/solutions/code/) 
- [Solutions Result](/solutions/result/)
- [Epoch Changelog](/solutions/epoch/)
- [Epoch Run Results](/solutions/epoch/)
- [Epoch Eval](/solutions/eval/)


## Learnings
Qwen 3.8 is not good at solving OR-problems out of the box.  
Combining two agents (math and code) allows for faster and more focused learning, i.e. either we fail because of agent's ability to translate problem into math (math agent) or math formulation into Python code (code agent). In the begining the main issue is translating math formulation into Python. Then, when Python scripts are executed correctly our meta-optimizer moves onto improving math agent.  
As we meet new OR-problems math agent instructions explode adding new instructions which could be mitigated by creating sub-insturctions for different types of OR-problems, i.e. instead of   **MathAgent**=>**CodeAgent**  we could have    
**ORproblemDetector**=>(**MathAgentProblemTypeA**, **MathAgentProblemTypeB**,...)=>**CodeAgent**.  
Current epoch numbers do not reflect the actual since in the latest run I wanted to compare results from insturctions from epochs (00, 0 and 13) on all 85 problems, where running 00 would fail mostly because of code-agent Python instructions.


## Requirements

- Python 3.12 (see `.python-version`)
- [uv](https://docs.astral.sh/uv/) for installing the locked project dependencies
- An OpenAI-compatible model server listening at `http://localhost:8000/v1`, serving the model name `openai/qwen38_q3` 
- Any solver packages imported by generated code, installed in the same Python environment used to run this project

Install dependencies from the repository root:

```bash
uv sync
```

The model endpoint, model name, generation settings, and timeouts are currently defined directly in `src/run_tuning.py` and `src/run_global_eval.py`. Start a compatible local server before running either script.

## Workflow

### Tune prompts

```bash
uv run python src/run_tuning.py
```

The tuning runner samples problems from `problems/data/test.jsonl`, runs each through the math/code pipeline, scores the batch, and asks a meta-optimizer to update the prompts. The current defaults are 30 epochs, five sampled problems per epoch, and `START = 10`; these values are constants near the top of the script. It loads the preceding prompt version and writes updated versions and epoch logs as it runs.

Before tuning, the runner moves existing versioned artifacts at or after `START` into `.trash/epoch_clean_<START>/`. Review the value of `START` and the affected artifacts before running, especially when resuming or changing an experiment.

### Evaluate saved runs

```bash
uv run python src/run_global_eval.py
```

This script replays existing result JSON files for versions `v00`, `v0`, and `v13` from `solutions/result/`; it does not generate new solutions. It uses the corresponding files in `solutions/code/` and `solutions/markdown/`, and writes the combined metrics to `solutions/eval/run_eval_final.csv`. The required versioned prompt files are loaded from `prompts/versions/`.

Open `src/eval.ipynb` after producing the CSV to group the results by version and calculate aggregate success and error metrics.

## Project layout

- `src/run_tuning.py`: iterative prompt-tuning runner
- `src/run_global_eval.py`: replay and aggregate saved evaluation results
- `src/eval.ipynb`: notebook for inspecting and aggregating evaluation metrics
- `src/utils/pipeline.py`: math modeling, code generation, and execution pipeline
- `src/utils/executor.py`: subprocess execution for generated Python code
- `src/utils/general.py`: prompt/data loading, artifact management, and scoring helpers
- `prompts/`: agent instructions, including versioned prompts
- `problems/data/test.jsonl`: benchmark problems and reference answers
- `solutions/`: generated Markdown models, Python scripts, execution results, epoch logs, and evaluation CSVs

## Current setup note

The checked-in pipeline at `src/utils/pipeline.py` imports `or_llm_agent.executor` and `or_llm_agent.utils`, while the helper modules in this repository are located at `src/utils/`. The project configuration also does not declare an `or_llm_agent` package. Resolve that import/package layout before expecting the runner commands above to work in a clean checkout.
