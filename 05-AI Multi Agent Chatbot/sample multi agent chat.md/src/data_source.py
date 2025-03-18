class DataSource:
    def __init__(self, records):
        self.records = records

    def get_entries(self):
        return self.records