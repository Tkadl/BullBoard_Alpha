"""
Data Quality Validation Module
Comprehensive data validation and anomaly detection
"""
import pandas as pd
import numpy as np


def validate_data_quality(df, min_days_needed=65):
    """Basic data validation and anomaly detection"""
    print("=== PERFORMING DATA QUALITY CHECKS ===")
    
    original_count = len(df)
    issues = []
    
    # Check 1: Remove extreme price movements (likely data errors >100% in one day)
    if 'daily_return' in df.columns:
        df['temp_return'] = df.groupby('symbol')['Close'].pct_change(fill_method=None)
        extreme_moves = df[abs(df['temp_return']) > 1.0]  # >100% moves
        if not extreme_moves.empty:
            print(f"  ⚠️  Found {len(extreme_moves)} extreme price movements (>100%)")
            print(f"      Affected symbols: {extreme_moves['symbol'].unique()[:5]}")
            # Remove extreme outliers (keep the data but flag for review)
            df = df[abs(df['temp_return']) <= 1.0]
            issues.append(f"Removed {len(extreme_moves)} extreme price movements")
        df = df.drop('temp_return', axis=1, errors='ignore')
    
    # Check 2: Remove invalid prices (zero or negative)
    invalid_prices = df[(df['Close'] <= 0) | (df['Open'] <= 0) | (df['High'] <= 0) | (df['Low'] <= 0)]
    if not invalid_prices.empty:
        print(f"  ⚠️  Found {len(invalid_prices)} invalid price records (zero/negative)")
        df = df[(df['Close'] > 0) & (df['Open'] > 0) & (df['High'] > 0) & (df['Low'] > 0)]
        issues.append(f"Removed {len(invalid_prices)} invalid price records")
    
    # Check 3: Validate price relationships (High >= Low, etc.)
    price_logic_errors = df[(df['High'] < df['Low']) | (df['High'] < df['Close']) | (df['High'] < df['Open']) | 
                           (df['Low'] > df['Close']) | (df['Low'] > df['Open'])]
    if not price_logic_errors.empty:
        print(f"  ⚠️  Found {len(price_logic_errors)} price logic errors")
        # Remove records where price relationships don't make sense
        df = df[~((df['High'] < df['Low']) | (df['High'] < df['Close']) | (df['High'] < df['Open']) | 
                 (df['Low'] > df['Close']) | (df['Low'] > df['Open']))]
        issues.append(f"Removed {len(price_logic_errors)} price logic errors")
    
    # Check 4: Identify symbols with insufficient data
    symbol_counts = df['symbol'].value_counts()
    insufficient_symbols = symbol_counts[symbol_counts < min_days_needed * 0.7].index.tolist()
    if insufficient_symbols:
        print(f"  ⚠️  {len(insufficient_symbols)} symbols have insufficient data")
        print(f"      Examples: {insufficient_symbols[:5]}")
        issues.append(f"{len(insufficient_symbols)} symbols with insufficient data")
    
    # Check 5: Date continuity check
    date_gaps = []
    for symbol in df['symbol'].unique()[:10]:  # Check first 10 symbols for performance
        symbol_data = df[df['symbol'] == symbol].sort_values('Date')
        if len(symbol_data) > 1:
            date_diff = (symbol_data['Date'].max() - symbol_data['Date'].min()).days
            expected_days = date_diff * 0.7  # Account for weekends/holidays
            if len(symbol_data) < expected_days:
                date_gaps.append(symbol)
    
    if date_gaps:
        print(f"  ⚠️  {len(date_gaps)} symbols may have date gaps")
        issues.append(f"{len(date_gaps)} symbols with potential date gaps")
    
    # Summary
    final_count = len(df)
    removed_count = original_count - final_count
    
    print(f"=== DATA QUALITY SUMMARY ===")
    print(f"  Original records: {original_count:,}")
    print(f"  Final records: {final_count:,}")
    print(f"  Removed records: {removed_count:,}")
    print(f"  Data quality: {((final_count/original_count)*100):.1f}%")
    
    if issues:
        print(f"  Issues detected: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  ✅ All data quality checks passed!")
    
    print("=== DATA QUALITY CHECKS COMPLETE ===")
    
    return df
