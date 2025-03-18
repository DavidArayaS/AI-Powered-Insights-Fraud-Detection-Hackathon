class Agent2:
    def __init__(self, data_source):
        self.data_source = data_source

    def query_low_credit_scores(self, approved_entries):
        # Simulate querying the data source for users with credit scores less than 500
        low_credit_entries = [entry for entry in approved_entries if entry['CreditScore'] < 500]
        return low_credit_entries, len(low_credit_entries)

    def process_credit_score_query(self, approved_entries):
        low_credit_entries, count = self.query_low_credit_scores(approved_entries)
        return f"There are {count} users with credit scores less than 500.", low_credit_entries