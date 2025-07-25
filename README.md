# BullBoard - Professional Stock Analytics Platform

## Project Structure
```
bullboard_alpha/
├── app.py              # Streamlit web application
├── etl/                # ETL pipeline package
│   ├── __init__.py     # Python package configuration
│   ├── main.py         # Main orchestration
│   ├── data_fetcher.py # Stock data downloading
│   ├── validators.py   # Data quality checks
│   └── utils.py        # Helper functions
└── requirements.txt
```
## Technical Stack
- Frontend: Streamlit
- Data Source: Yahoo Finance (yfinance)
- Analytics: Pandas, NumPy
- Visualization: Plotly

## Architecture
The ETL pipeline follows a modular design:

- Data Fetcher: Handles yfinance API calls with retry logic
- Data Processor: Calculates rolling analytics and risk metrics
- Validators: Ensures data quality and detects anomalies
- Utils: Market-aware date handling and helper functions
