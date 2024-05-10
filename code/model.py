import pandas as pd


class DataLoader:
    """Handles loading, cleaning, and storing of CSV data."""

    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.filename)
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found.")

        self.clean_data()

    def clean_data(self):
        pass

    def get_data(self):
        return self.data
