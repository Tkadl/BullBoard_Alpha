"""
Data processing package for BullBoard application
Handles data loading, validation, and statistical calculations
"""

from .processor import (
    load_and_validate_data,
    get_processed_symbols,
    calculate_summary_statistics
)

from .cache_manager import (
    cache_data_loading,
    cache_symbol_processing,
    cache_statistics_calculation
)

__version__ = "1.0.0"

__all__ = [
    'load_and_validate_data',
    'get_processed_symbols', 
    'calculate_summary_statistics',
    'cache_data_loading',
    'cache_symbol_processing',
    'cache_statistics_calculation'
]
