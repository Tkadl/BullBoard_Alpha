"""
Stock Data Fetching Module
Handles all yfinance interactions and column standardization
"""
import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta


def fetch_with_retry(tickers_batch, start_date, end_date, max_retries=3, base_delay=3):
    """
    Fetch data with retry logic for rate limiting
    """
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} for batch: {tickers_batch}")
            raw = yf.download(
                tickers_batch, 
                start=start_date, 
                end=end_date, 
                auto_adjust=True,
                prepost=True,
                threads=True
            )
            return raw, []  # Return data and empty failed list
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {tickers_batch}: {e}")
            if attempt == max_retries - 1:
                print(f"All attempts failed for batch: {tickers_batch}")
                return None, tickers_batch  # Return None and failed tickers
            
            # Exponential backoff
            sleep_time = base_delay * (2 ** attempt)
            print(f"Waiting {sleep_time} seconds before retry...")
            time.sleep(sleep_time)
    
    return None, tickers_batch


def fetch_incremental_data(tickers, last_date, end_date, min_days_needed, batch_size=1, delay_between_batches=2):
    """Fetch only new data since last_date"""
    from datetime import datetime, timedelta
    
    # Calculate start date (day after last_date)
    last_update = datetime.strptime(last_date, "%Y-%m-%d")
    incremental_start = (last_update + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Fetching incremental data from {incremental_start} to {end_date}")
    
    good_dfs = []
    bad_tickers = []
    
    # Use same batch processing logic as your current code
    total_batches = (len(tickers) + batch_size - 1) // batch_size
    
    for batch_num, i in enumerate(range(0, len(tickers), batch_size), 1):
        batch = tickers[i:i+batch_size]
        print(f"Processing incremental batch {batch_num}/{total_batches} ({len(batch)} symbols)...")
        
        # Use same single-ticker approach for incremental updates
        for ticker in batch:
            try:
                data = yf.download(ticker, start=incremental_start, end=end_date,
                                  auto_adjust=True, progress=False, threads=True)
                
                if data.empty:
                    bad_tickers.append(ticker)
                    continue
                    
                data['symbol'] = ticker
                data['Date'] = data.index
                good_dfs.append(data.reset_index(drop=True))
                
            except Exception as e:
                print(f"Error in incremental fetch for {ticker}: {e}")
                bad_tickers.append(ticker)
                continue
            
        if delay_between_batches > 0:
            time.sleep(delay_between_batches)
    
    return good_dfs, bad_tickers
