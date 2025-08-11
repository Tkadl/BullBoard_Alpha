"""
Data Processing Module
Handles data loading, validation, and statistical calculations
"""

import pandas as pd
import numpy as np
import os
import traceback
from config.settings import MIN_DAYS_NEEDED


def load_and_validate_data():
    """Cache the main data loading to avoid repeated CSV reads"""
    try:
        # Check if file exists (log only, don't show to user)
        if not os.path.exists("latest_results.csv"):
            print("❌ File 'latest_results.csv' not found!")  # Console log only
            return None
        
        # Log file info to console
        file_size = os.path.getsize("latest_results.csv")
        print(f"📁 Loading CSV file: {file_size:,} bytes")  # Console log only
        
        # Load data WITHOUT automatic date parsing
        df = pd.read_csv("latest_results.csv")
        
        print(f"📊 Raw data loaded: {df.shape}")  # Debug
        print(f"📊 Columns: {list(df.columns)}")  # Debug
        print(f"📊 Date column sample: {df['Date'].head(3).tolist() if 'Date' in df.columns else 'NO DATE COLUMN'}")  # Debug
        
        # Try to parse dates manually with error handling
        if 'Date' in df.columns:
            try:
                # Handle different date formats that might exist
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                print("✅ Date parsing successful")
                
                # Remove rows with invalid dates
                invalid_dates = df['Date'].isna().sum()
                if invalid_dates > 0:
                    print(f"⚠️ Removing {invalid_dates} rows with invalid dates")
                    df = df.dropna(subset=['Date'])
                
            except Exception as date_error:
                print(f"⚠️ Date parsing failed: {date_error}")
                # Keep the data anyway - dates as strings are still usable
        else:
            print("⚠️ No Date column found")
        
        print(f"✅ Final data shape: {df.shape}")  # Debug
        
        if df.empty:
            print("❌ DataFrame is empty after processing")
            return None
            
        if 'symbol' not in df.columns:
            print("❌ Missing 'symbol' column")
            print(f"Available columns: {list(df.columns)}")
            return None
        
        print(f"✅ Loaded {len(df):,} records, {df['symbol'].nunique()} symbols")  # Console log only
        return df
        
    except FileNotFoundError:
        print("❌ File not found: latest_results.csv")
        return None
    except pd.errors.EmptyDataError:
        print("❌ CSV file is empty")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        traceback.print_exc()
        return None


def get_processed_symbols(df):
    """Cache symbol processing"""
    return sorted(df['symbol'].unique())


def calculate_summary_statistics(filtered_df, selected_symbols_hash, date_hash):
    """Cache expensive summary calculations"""
    return (
        filtered_df
        .groupby("symbol")
        .agg(
            period_start=("Date", "min"),
            period_end=("Date", "max"),
            period_days=("Date", "count"),
            avg_close=("Close", "mean"),
            avg_daily_return=("daily_return", "mean"),
            total_return=("Close", lambda x: (x.iloc[-1] / x.iloc[0]) - 1 if len(x) > 1 and x.iloc[0] != 0 else np.nan),
            volatility_21=("volatility_21", "mean"),
            avg_rolling_yield_21=("rolling_yield_21", "mean"),
            avg_sharpe_21=("sharpe_21", "mean"),
            avg_max_drawdown_63=("max_drawdown_63", "mean"),
            avg_custom_risk_score=("custom_risk_score", "mean"),
        )
        .reset_index()
    )
