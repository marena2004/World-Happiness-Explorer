" Module for Model"
import pandas as pd


class Model:
    """Handles loading, cleaning, and storing of CSV data."""

    def __init__(self):
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv("WorldHappiness2015-2019.csv")
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found.")

        self.clean_data()

    def clean_data(self):
        # Rename index
        self.data.rename(index={'Taiwan Province of China': 'Taiwan',
                                'Hong Kong S.A.R., China': 'Hong Kong',
                                'Trinidad & Tobago': 'Trinidad and Tobago',
                                'Northern Cyprus': 'North Cyprus',
                                'North Macedonia': 'Macedonia'}, inplace=True)

        # Add the correct Region value to changed index
        self.data.loc[self.data['Country'] == 'Taiwan', 'Region'] = 'Eastern Asia'
        self.data.loc[self.data['Country'] == 'Hong Kong', 'Region'] = 'Eastern Asia'
        self.data.loc[self.data['Country'] == 'Trinidad and Tobago', 'Region'] = 'Latin America and Caribbean'
        self.data.loc[self.data['Country'] == 'North Cyprus', 'Region'] = 'Central and Eastern Europe'
        self.data.loc[self.data['Country'] == 'Macedonia', 'Region'] = 'Central and Eastern Europe'
        self.data.loc[self.data['Country'] == 'Gambia', 'Region'] = 'Sub-Saharan Africa'

    def get_data(self):
        return self.data
