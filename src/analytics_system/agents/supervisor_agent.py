class SupervisorAgent:
    name = "Supervisor Agent"

    def select_agents(self, request: str) -> list[str]:
        text = (request or "").lower()
        selected = ["profiling", "cleaning", "eda", "visualization", "insights"]
        if "only chart" in text or "only visual" in text:
            selected = ["profiling", "visualization", "insights"]
        if "no clean" in text or "without cleaning" in text:
            selected = [name for name in selected if name != "cleaning"]
        if "anomal" in text or "outlier" in text:
            selected.append("anomaly")
        if "report" in text or "pdf" in text:
            selected.append("report")
        # Preserve order while removing duplicates.
        return list(dict.fromkeys(selected))
