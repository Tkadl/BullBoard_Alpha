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
    """Simplified version for debugging"""
    print("🔍 === SIMPLE LOAD TEST ===")
    
    try:
        if not os.path.exists("latest_results.csv"):
            print("❌ File not found")
            return None
            
        print("📂 File found, loading...")
        df = pd.read_csv("latest_results.csv")
        print(f"✅ Loaded: {df.shape}")
        
        if df.empty:
            print("❌ Empty DataFrame")
            return None
            
        print("🎉 Success!")
        return df
        
    except Exception as e:
        print(f"❌ Exception: {e}")
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
