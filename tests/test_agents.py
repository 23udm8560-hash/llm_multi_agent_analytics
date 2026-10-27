import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analytics_system.agents.supervisor_agent import SupervisorAgent


def test_supervisor_selects_anomaly_agent():
    selected = SupervisorAgent().select_agents("Run analysis and detect outliers")
    assert "anomaly" in selected
