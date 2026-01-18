import pandas as pd

class TransactionDetector:
    def __init__(self, data_path, threshold=5000):
        self.data_path = data_path
        self.threshold = threshold
        self.df = None

    def load_data(self):
        """Loads CSV data and ensures 'time' is in datetime format."""
        self.df = pd.read_csv(self.data_path)
        self.df['time'] = pd.to_datetime(self.df['time'])
        return self.df

    def detect_fraud(self):
        """Applies business rules to flag suspicious transactions."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Rule 1: High Amount
        high_amount = self.df['amount'] > self.threshold

        # Rule 2: Unusual Country (Non-CA/US)
        unusual_country = ~self.df['country'].isin(['CA', 'US'])

        # Rule 3: High Frequency (Multiple transactions within 60 seconds)
        self.df = self.df.sort_values(by=['user_id', 'time'])
        time_diff = self.df.groupby('user_id')['time'].diff().dt.total_seconds()
        high_frequency = time_diff < 60

        # Assign flags and reasons
        self.df['is_flagged'] = high_amount | unusual_country | high_frequency
        self.df['reason'] = ""
        self.df.loc[high_amount, 'reason'] += "High Amount; "
        self.df.loc[unusual_country, 'reason'] += "Unusual Country; "
        self.df.loc[high_frequency, 'reason'] += "High Frequency; "
        
        return self.df[self.df['is_flagged']]