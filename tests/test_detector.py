import pytest
import pandas as pd
import os
from src.detector import TransactionDetector

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV file for testing."""
    file = tmp_path / "test_data.csv"
    data = {
        'user_id': [1, 1],
        'amount': [10000, 20],
        'country': ['CA', 'CA'],
        'time': ['2026-01-01 10:00:00', '2026-01-01 10:00:30']
    }
    pd.DataFrame(data).to_csv(file, index=False)
    return file

def test_fraud_logic(sample_csv):
    detector = TransactionDetector(sample_csv)
    detector.load_data()
    flagged = detector.detect_fraud()
    
    # User 1 should be flagged for High Amount AND High Frequency
    assert len(flagged) > 0
    assert "High Amount" in flagged.iloc[0]['reason']
    assert "High Frequency" in flagged.iloc[1]['reason']