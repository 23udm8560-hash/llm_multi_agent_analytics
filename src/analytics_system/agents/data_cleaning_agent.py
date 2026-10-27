from analytics_system.data_processing.cleaner import clean_dataframe


class DataCleaningAgent:
    name = "Data Cleaning Agent"

    def run(self, df, **options):
        return clean_dataframe(df, **options)
