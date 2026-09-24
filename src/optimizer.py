# import json
# from pathlib import Path
# from datetime import datetime

# class PromptManager:
#     """Handles versioning and reading/writing of prompts."""
#     def __init__(self, prompts_dir: str = "prompts"):
#         self.dir = Path(prompts_dir)
#         self.versions_dir = self.dir / "versions"
#         self.versions_dir.mkdir(parents=True, exist_ok=True)

#     def load_prompt(self, name: str) -> str:
#         return (self.dir / f"{name}.txt").read_text(encoding="utf-8")

#     def save_version(self, name: str, content: str, version_label: str):
#         # Save historical version
#         version_file = self.versions_dir / f"{name}_{version_label}.txt"
#         version_file.write_text(content, encoding="utf-8")
        
#         # Overwrite current active prompt
#         active_file = self.dir / f"{name}.txt"
#         active_file.write_text(content, encoding="utf-8")
#         print(f" Saved new version: {version_file}")

# class BatchEvaluator:
#     """Executes experiments over batches of size N and logs failure patterns."""
#     def __init__(self, batch_size: int = 5):
#         self.batch_size = batch_size

#     def analyze_batch_logs(self, logs: list[dict]) -> str:
#         """Formats batch results into a summary for the Optimizer Agent."""
#         summary = f"Batch Evaluation Summary ({len(logs)} Problems):\n"
#         failures = [l for l in logs if not l["success"]]
        
#         summary += f"Passed: {len(logs) - len(failures)}/{len(logs)}\n"
#         summary += f"Failed: {len(failures)}/{len(logs)}\n\n"
        
#         if failures:
#             summary += "--- Failure Details ---\n"
#             for f in failures:
#                 summary += f"ID: {f['id']}\n"
#                 summary += f"Error: {f['stderr'][-300:]}\n" # Last 300 chars of stack trace
#                 summary += f"Code Snippet:\n{f['code'][:200]}...\n---\n"
#         return summary

# import re
# from pathlib import Path

# def parse_and_apply_prompt_updates(
#     llm_output: str, 
#     prompts_dir: str = "prompts",
#     version_tag: str = "v1.1"
# ) -> dict[str, bool]:
#     """
#     Parses <math_agent_instructions> and <code_agent_instructions> from meta_optimizer output.
#     Updates prompt files on disk if changes are present.
#     """
#     prompts_path = Path(prompts_dir)
#     versions_path = prompts_path / "versions"
#     versions_path.mkdir(parents=True, exist_ok=True)
    
#     updates = {"math_agent": False, "code_agent": False}
    
#     agent_map = {
#         "math_agent": r"<math_agent_instructions>\s*(.*?)\s*</math_agent_instructions>",
#         "code_agent": r"<code_agent_instructions>\s*(.*?)\s*</code_agent_instructions>"
#     }
    
#     for agent_key, pattern in agent_map.items():
#         match = re.search(pattern, llm_output, re.DOTALL)
#         if match:
#             new_content = match.group(1).strip()
            
#             # Skip if explicit UNCHANGED signal or empty
#             if new_content and new_content.upper() != "UNCHANGED":
#                 # # Save active file (e.g. prompts/instructions.math_agent.txt)
#                 # active_file = prompts_path / f"{agent_key}_{version_tag}.txt"
#                 # active_file.write_text(new_content, encoding="utf-8")
                
#                 # Save historical version trace
#                 version_file = versions_path / f"{agent_key}_{version_tag}.txt"
#                 version_file.write_text(new_content, encoding="utf-8")
                
#                 updates[agent_key] = True
#                 print(f" Updated {active_file.name} (Archived to {version_file.name})")

#     return updates