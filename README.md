# Transaction Fraud Detector

A lightweight, rule-based fraud detection engine designed to identify high-risk financial activities. Built with Python and Streamlit for easy visualization.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Live Demo

Website URL: https://fraud-detector-csv.streamlit.app/

## Features

- **Rule-based Detection** - Interpretable flags tied to specific business rules
- **Interactive Dashboard** - Streamlit web app for easy analysis
- **CSV Upload** - Analyze your own transaction data
- **Real-time Metrics** - View flagged transactions with visualizations

## Detection Rules

| Rule | Description |
|------|-------------|
| **High Amount** | Transactions exceeding configurable threshold (default: $5,000) |
| **Unusual Country** | Transactions from non-authorized jurisdictions (outside CA/US) |
| **High Frequency** | Multiple transactions within 60 seconds (potential bot/scam) |

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dang0810/fraud-detector.git
cd fraud-detector

# Install dependencies
pip install -r requirements.txt
```

### Run Streamlit App

```bash
streamlit run app.py
```

### Run CLI Version

```bash
python main.py
```

### Run Tests

```bash
pytest tests/ -v
```


## CSV Format

Your CSV file should contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | int | User identifier |
| `amount` | float | Transaction amount |
| `country` | string | 2-letter country code |
| `time` | datetime | Transaction timestamp |



