from analytics_system.data_processing.profiler import profile_dataframe


class DataProfilingAgent:
    name = "Data Profiling Agent"

    def run(self, df):
        return profile_dataframe(df)
