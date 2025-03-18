class Agent1:
    def __init__(self, data_source):
        self.data_source = data_source

    def query_approved_status(self):
        # Simulate querying the data source for approved statuses
        entries = self.data_source.get_entries()
        approved_entries = [entry for entry in entries if entry['ApprovalStatus'] == 'Approved']
        return approved_entries, len(approved_entries)

    def process_approval_query(self):
        approved_entries, count = self.query_approved_status()
        return f"There are {count} approved entries.", approved_entries