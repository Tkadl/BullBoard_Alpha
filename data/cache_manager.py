"""
Cache Management Module
Handles Streamlit caching for data operations
"""

import streamlit as st
from .processor import (
    load_and_validate_data as _load_and_validate_data,
    get_processed_symbols as _get_processed_symbols,
    calculate_summary_statistics as _calculate_summary_statistics
)


@st.cache_data
def cache_data_loading():
    """Cached wrapper for data loading"""
    return _load_and_validate_data()


@st.cache_data
def cache_symbol_processing(_df):
    """Cached wrapper for symbol processing"""
    return _get_processed_symbols(_df)


@st.cache_data
def cache_statistics_calculation(_filtered_df, selected_symbols_hash, date_hash):
    """Cached wrapper for statistics calculation"""
    return _calculate_summary_statistics(_filtered_df, selected_symbols_hash, date_hash)
