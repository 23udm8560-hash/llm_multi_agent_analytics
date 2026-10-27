"""CLI smoke test for the core workflow.
Usage: python main.py path/to/file.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import pandas as pd
from analytics_system.core.graph import run_workflow

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/file.csv")
        raise SystemExit(2)
    path = Path(sys.argv[1])
    df = pd.read_csv(path)
    result = run_workflow(df)
    print("Status:", result["status"])
    print("Profile:", result["profile"])
    print(result["insights"])
