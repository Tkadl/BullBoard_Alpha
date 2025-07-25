"""
Main ETL Pipeline Orchestrator
Coordinates all ETL modules while preserving exact logic
"""
import os
import traceback
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
import time

# Imports from other etl files
from .utils import get_last_update_info, should_do_incremental_update, get_sp500_symbols
from .validators import validate_data_quality
from .data_fetcher import fetch_with_retry, fetch_incremental_data


def main():
    print("\n=== ETL MAIN FUNCTION STARTED ===")
    print("ETL running from directory:", os.getcwd())
    
    # === CONFIGURATION ===
    DEBUG_ONLY_A_FEW = False
    
    if DEBUG_ONLY_A_FEW:
        print("🔧 DEBUG MODE: Using limited tickers")
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        batch_size = 1
        delay_between_batches = 5
        max_retries = 3
        print("DEBUG: Only fetching these tickers:", tickers)
        # Skip the S&P 500 test in debug mode
        skip_sp500_test = True
    else:
        print("📈 PRODUCTION MODE")
        tickers = get_sp500_symbols()
        batch_size = 1
        delay_between_batches = 10
        max_retries = 3
        skip_sp500_test = False
    
    # Other configuration
    min_days_needed = 65
    yield_thresh = 0.01          
    risk_thresh = 0.06           
    rolling_vol_days = 21
    rolling_drawdown_days = 63
    
    try:
        # Conditional S&P 500 test - ONLY runs in production mode
        if not skip_sp500_test:
            print("Step 1: Fetching S&P 500 symbols...")
            tickers = get_sp500_symbols()  # Only runs in production mode
            print(f"✅ Successfully got {len(tickers)} symbols")
            print(f"First 10 symbols: {tickers[:10]}")
        else:
            print("Step 1: Skipping S&P 500 fetch (debug mode)")
            print(f"✅ Using debug tickers: {tickers}")
        
        # Test single stock fetch with actual first ticker
        print(f"\nStep 2: Testing single stock fetch...")
        test_ticker = yf.Ticker(tickers[0])
        test_data = test_ticker.history(period="5d")
        print(f"✅ Test fetch successful: {len(test_data)} days of {tickers[0]} data")
        
        # Test the date setup
        print("\nStep 3: Testing date configuration...")
        start_date = "2024-01-01"
        end_date = date.today().strftime("%Y-%m-%d")
        print(f"✅ Date range: {start_date} to {end_date}")
        
        # Test existing data check
        print("\nStep 4: Checking existing data...")
        existing_df, last_date, existing_symbols = get_last_update_info()
        print(f"✅ Existing data check complete")
        print(f"Last date: {last_date}")
        print(f"Existing symbols: {len(existing_symbols) if existing_symbols else 0}")
        
        print("\n🎉 All basic tests passed! Issue is likely in the actual data fetching...")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
        return


    # Original code continues here...
    print("\nContinuing with original ETL logic...")
    print(f"Using: batch_size={batch_size}, delay={delay_between_batches}s")

    print(f"Checking for existing data and update requirements...")

    # Check already extracted data
    can_do_incremental, reason = should_do_incremental_update(last_date, existing_symbols, tickers)
    print(f"Update decision: {reason}")
    
    if can_do_incremental:
        print("=== PERFORMING INCREMENTAL UPDATE ===")
        
        # Fetch only new data
        good_dfs, bad_tickers = fetch_incremental_data(
            tickers, last_date, end_date, min_days_needed, batch_size, delay_between_batches
        )
        
        print(f"Incremental fetch: {len(good_dfs)} symbols updated, {len(bad_tickers)} failed")
        
        if good_dfs:
            # Combine new data with standardized columns
            print(f"🔧 Standardizing {len(good_dfs)} incremental DataFrames...")
            standardized_dfs = []
            multiindex_count = 0
            
            for i, df_temp in enumerate(good_dfs):
                # Flatten MultiIndex columns if they exist
                if isinstance(df_temp.columns, pd.MultiIndex):
                    df_temp.columns = df_temp.columns.get_level_values(0)
                    multiindex_count += 1
                
                # Standardize column order
                expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'symbol', 'Date']
                df_temp = df_temp[expected_columns]
                standardized_dfs.append(df_temp)
            
            print(f"  ✅ Processed {len(good_dfs)} DataFrames ({multiindex_count} required MultiIndex flattening)")
            
            new_df = pd.concat(standardized_dfs, ignore_index=True)
            print(f"✅ Incremental concatenation complete: {new_df.shape}")
            
            # Add timestamp for new data
            download_time = datetime.now()
            new_df['download_time'] = download_time.strftime('%Y-%m-%d %H:%M')
            
            # Combine with existing data
            df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Remove duplicates (in case of overlap)
            df = df.drop_duplicates(subset=['symbol', 'Date'], keep='last')
            df = df.sort_values(['symbol', 'Date']).reset_index(drop=True)
            
            print(f"Combined dataset: {len(df)} total records")
        else:
            print("No new data fetched - using existing data")
            df = existing_df

    else:
        print("=== PERFORMING FULL REFRESH ===")
        print(f"Fetching data for {len(tickers)} symbols...")
        
        good_dfs = []
        bad_tickers = []

        # Create batches
        batches = [tickers[i:i + batch_size] for i in range(0, len(tickers), batch_size)]
        total_batches = len(batches)
        start_time = datetime.now()
        
        for batch_num, batch in enumerate(batches, 1):
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} symbols)...")
            
    
            # Process each ticker individually (Stack Overflow single ticker approach)
            for ticker in batch:
                try:
                    print(f"  Downloading {ticker}...")
                    # Download single ticker without group_by - creates simple columns
                    data = yf.download(ticker, start=start_date, end=end_date, 
                                      auto_adjust=True, prepost=True, threads=True)
                    
                    if data.empty or len(data) < min_days_needed:
                        print(f"  ⚠️ Insufficient data for {ticker}: {len(data)} rows")
                        bad_tickers.append(ticker)
                        continue
                        
                    # Add ticker column (Stack Overflow approach)
                    data['symbol'] = ticker
                    data['Date'] = data.index
                    good_dfs.append(data.reset_index(drop=True))
                    print(f"  ✅ {ticker}: {len(data)} rows added")
                    
                except Exception as e:
                    print(f"  ❌ Error downloading {ticker}: {e}")
                    bad_tickers.append(ticker)
                    continue
            
        if good_dfs:
            print("🔧 Standardizing DataFrame columns before concatenation...")
            standardized_dfs = []
            
            for i, df_temp in enumerate(good_dfs):
                print(f"  DEBUG: DataFrame {i} columns before standardization: {list(df_temp.columns)}")
                
                # Flatten MultiIndex columns if they exist
                if isinstance(df_temp.columns, pd.MultiIndex):
                    print(f"  🔧 Flattening MultiIndex columns for DataFrame {i}")
                    # Take only the first level (the actual column names)
                    df_temp.columns = df_temp.columns.get_level_values(0)
                
                # Standardize column order
                expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'symbol', 'Date']
                df_temp = df_temp[expected_columns]
                standardized_dfs.append(df_temp)
                print(f"  ✅ DataFrame {i} standardized: {list(df_temp.columns)}")
                
            df = pd.concat(standardized_dfs, ignore_index=True)
            print(f"✅ Concatenation complete: {df.shape}")
            print(f"✅ Final columns: {list(df.columns)}")
            print(f"✅ Column type: {type(df.columns)}")
        else:
            print("No data fetched — check your internet connection and ticker list.")
            return
            
        # TIMESTAMP DATA DOWNLOAD
        download_time = datetime.now()
        df['download_time'] = download_time.strftime('%Y-%m-%d %H:%M')
    
    # DATA VALIDATION BEFORE CALC
    bad_symbols = []
    for sym, group in df.groupby('symbol'):
        if group.shape[0] < min_days_needed:
            bad_symbols.append(sym)
    df = df[~df['symbol'].isin(bad_symbols)]

    # ROLLING ANALYTICS
    print("🔧 Calculating rolling analytics...")
    df = df.sort_values(['symbol', 'Date']).reset_index(drop=True)
    
    # Calculate analytics with proper error handling
    try:
        df['daily_return'] = df.groupby('symbol')['Close'].pct_change(fill_method=None)
        df['volatility_21'] = df.groupby('symbol')['daily_return'].rolling(rolling_vol_days).std().reset_index(0, drop=True)
        df['rolling_yield_21'] = df.groupby('symbol')['daily_return'].rolling(rolling_vol_days).mean().reset_index(0, drop=True)
        df['sharpe_21'] = (df['rolling_yield_21'] / df['volatility_21']) * np.sqrt(252)
        
        # Simplified max drawdown calculation to avoid length mismatch
        df['max_drawdown_63'] = df.groupby('symbol')['Close'].rolling(rolling_drawdown_days).max().reset_index(0, drop=True) - \
                               df.groupby('symbol')['Close'].rolling(rolling_drawdown_days).min().reset_index(0, drop=True)
        df['max_drawdown_63'] = df['max_drawdown_63'] / df.groupby('symbol')['Close'].rolling(rolling_drawdown_days).max().reset_index(0, drop=True)
        
        df['custom_risk_score'] = df['volatility_21'] * 0.7 + df['max_drawdown_63'] * 0.3
        print("✅ Rolling analytics calculated successfully")
        
    except Exception as e:
        print(f"⚠️ Error in rolling analytics: {e}")
        # Add default values if calculations fail
        df['daily_return'] = 0
        df['volatility_21'] = 0
        df['rolling_yield_21'] = 0
        df['sharpe_21'] = 0
        df['max_drawdown_63'] = 0
        df['custom_risk_score'] = 0

    # Get each stock's latest analytics
    latest = df.sort_values('Date').groupby('symbol').tail(1)
    latest = latest[['symbol', 'Date', 'custom_risk_score', 'rolling_yield_21', 'sharpe_21', 'volatility_21', 'max_drawdown_63']].copy()
    latest = latest.sort_values('custom_risk_score', ascending=False)
    latest.reset_index(drop=True, inplace=True)

    # Data quality validation before saving
    df = validate_data_quality(df)
    
    # Save summary table for Streamlit app
    print("\n=== ETL SUMMARY BEFORE FINAL SAVE ===")
    try:
        print(f"DataFrame shape: {df.shape}")
        print(f"Unique symbols: {df['symbol'].nunique() if 'symbol' in df.columns else 'MISSING SYMBOL COL'}")
        print("Sample rows:")
        print(df.head())
    except Exception as e:
        print("❗ Trouble with dataframe before save:", str(e))
        print(traceback.format_exc())
    
    # Write file and confirm output
    output_path = "latest_results.csv"
    print("Attempting to save data to:", output_path)
    try:
        df.to_csv(output_path, index=False)
        print("✅ Data saved. File size:", os.path.getsize(output_path), "bytes")
    except Exception as e:
        print(f"❌ Failed to save output CSV: {e}")
        print(traceback.format_exc())
    
    # Show files in directory so you know file is truly there
    print("Files in cwd:", os.listdir(os.getcwd()))

if __name__ == "__main__":
    main()
