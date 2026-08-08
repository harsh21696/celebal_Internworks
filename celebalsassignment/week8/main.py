"""
main.py
=======
Runs the entire pipeline end-to-end in order:
  1. Generate raw data
  2. Clean data
  3. Build SQLite DB and load cleaned data
  4. Run the edge-case test suite
Then launches the interactive CLI reporting tool.

Run:
    python main.py
"""

import subprocess
import sys
import os

BASE = os.path.dirname(__file__)


def run(script_path, cwd):
    print(f"\n{'='*60}\nRunning {script_path}\n{'='*60}")
    result = subprocess.run([sys.executable, script_path], cwd=cwd)
    if result.returncode != 0:
        print(f"Step failed: {script_path}")
        sys.exit(result.returncode)


def main():
    run("generate_data.py", os.path.join(BASE, "data_generation"))
    run("clean_data.py", os.path.join(BASE, "cleaning"))
    run("load_data.py", os.path.join(BASE, "database"))
    run("edge_cases.py", os.path.join(BASE, "tests"))

    print("\nPipeline complete! Launching the CLI reporting tool...\n")
    subprocess.run([sys.executable, "report_generator.py"], cwd=os.path.join(BASE, "reports"))


if __name__ == "__main__":
    main()
