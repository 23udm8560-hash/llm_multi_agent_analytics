class SQLAgent:
    """Reserved extension point for a future read-only SQL querying agent."""
    name = "SQL Agent"

    def run(self, question: str):
        raise NotImplementedError("SQL Agent is an extension point; configure a database and read-only query policy first.")
