"""
BullBoard ETL Package
Professional stock data pipeline for market analysis

This package provides modular ETL functionality for:
- Stock data fetching from Yahoo Finance
- Data quality validation and cleaning
- Market-aware date handling
- Incremental data updates

Modules:
- main: Main ETL pipeline orchestrator
- data_fetcher: Stock data downloading with retry logic
- validators: Data quality validation and anomaly detection
- utils: Helper functions and utilities

Usage:
    from etl.main import main
    main()  # Run the complete ETL pipeline
"""

__version__ = "1.0.0"
__author__ = "Tkadl"

# Import main function for easy access
from .main import main

# Make key functions available at package level
from .utils import get_sp500_symbols, get_last_update_info
from .validators import validate_data_quality
from .data_fetcher import fetch_with_retry, fetch_incremental_data

__all__ = [
    'main',
    'get_sp500_symbols',
    'get_last_update_info', 
    'validate_data_quality',
    'fetch_with_retry',
    'fetch_incremental_data'
]
