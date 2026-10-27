import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pandas as pd
from analytics_system.core.graph import run_workflow


def test_workflow_runs():
    df = pd.DataFrame({"amount": [10, 20, 30, 40], "region": ["A", "B", "A", "B"]})
    result = run_workflow(df)
    assert result["status"] == "completed"
    assert result["profile"]["rows"] == 4
    assert "insights" in result
