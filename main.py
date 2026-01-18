import pandas as pd
from src.detector import TransactionDetector

def generate_dummy_data():
    data = {
        'user_id': [101, 102, 101, 103],
        'amount': [200, 7000, 50, 300],
        'country': ['CA', 'CA', 'UK', 'US'],
        'time': ['2026-01-18 10:00:00', '2026-01-18 10:05:00', 
                 '2026-01-18 10:00:45', '2026-01-18 11:00:00']
    }
    pd.DataFrame(data).to_csv('transactions.csv', index=False)

if __name__ == "__main__":
    generate_dummy_data()
    print("--- Transaction Analyzer ---")
    detector = TransactionDetector('transactions.csv')
    detector.load_data()
    results = detector.detect_fraud()
    
    print("\n[Flagged Transactions Report]")
    print(results[['user_id', 'amount', 'country', 'reason']])