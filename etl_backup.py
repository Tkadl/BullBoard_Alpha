import os
import traceback
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
import time  # Add this import

def get_market_aware_dates():
    """Get trading dates that account for market schedules"""
    import pandas as pd
    from datetime import datetime, timedelta
    import pytz
    
    try:
        # Use market timezone (NYSE)
        market_tz = pytz.timezone('America/New_York')
        now_market = datetime.now(market_tz)
        
        # Market closes at 4 PM ET
        market_close_today = now_market.replace(hour=16, minute=0, second=0, microsecond=0)
        
        # If it's before market close today, use yesterday as end date
        if now_market < market_close_today:
            end_date = (now_market - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            end_date = now_market.strftime('%Y-%m-%d')
        
        # Account for weekends - if end_date is weekend, go to Friday
        end_datetime = pd.to_datetime(end_date)
        if end_datetime.weekday() >= 5:  # Saturday=5, Sunday=6
            days_back = end_datetime.weekday() - 4  # Go back to Friday
            end_date = (end_datetime - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        start_date = "2024-01-01"  # Your existing start date
        
        print(f"📅 Market-aware dates: {start_date} to {end_date} (Market TZ: {now_market.strftime('%Y-%m-%d %H:%M %Z')})")
        
        return start_date, end_date, market_tz
        
    except Exception as e:
        print(f"⚠️ Error in market date calculation, falling back to simple dates: {e}")
        # Fallback to your existing logic
        from datetime import date
        start_date = "2024-01-01"
        end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # Use yesterday
        return start_date, end_date, None

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

def get_last_update_info():
    """Check existing data and determine what needs updating"""
    try:
        existing_df = pd.read_csv("latest_results.csv", parse_dates=["Date"])
        if existing_df.empty:
            return None, None, []
        
        last_date = existing_df['Date'].max().strftime("%Y-%m-%d")
        existing_symbols = existing_df['symbol'].unique().tolist()
        return existing_df, last_date, existing_symbols
    except FileNotFoundError:
        print("No existing data file found - will perform full refresh")
        return None, None, []

def should_do_incremental_update(last_date, existing_symbols, current_tickers):
    """Determine if incremental update is possible and beneficial"""
    if last_date is None:
        return False, "No existing data"
    
    # Check if last update was today (no new data to fetch)
    last_update = datetime.strptime(last_date, "%Y-%m-%d")
    today = datetime.now().date()
    
    if last_update.date() >= today:
        return False, "Data already up to date"
    
    # Check if it's been more than 5 days (probably better to do full refresh)
    days_since_update = (datetime.now() - last_update).days
    if days_since_update > 5:
        return False, f"Data is {days_since_update} days old - full refresh recommended"
    
    # Check if ticker list has changed significantly
    symbol_diff = set(current_tickers) - set(existing_symbols)
    if len(symbol_diff) > 20:
        return False, f"Many new symbols detected: {len(symbol_diff)}"
    
    return True, f"Will fetch {days_since_update} day(s) of new data"

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

def get_sp500_symbols():
    """Get complete S&P 500 symbols list"""
    print("DEBUG: get_sp500_symbols() function called!")  # Add this line
    sp500_symbols = [
        'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ATO', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO',
        'BA', 'BAC', 'BALL', 'BAX', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF-B', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BMY', 'BR', 'BRK-B', 'BRO', 'BSX', 'BWA',
        'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDAY', 'CDNS', 'CDW', 'CE', 'CEG', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP', 'COST', 'CPB', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CTVA', 'CVS', 'CVX', 'CZR',
        'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISH', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN',
        'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR',
        'F', 'FANG', 'FAST', 'FBHS', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTNT', 'FTV',
        'GD', 'GE', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN', 'GS', 'GWW',
        'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM',
        'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ',
        'JBHT', 'JCI', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'JWN',
        'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSS',
        'L', 'LDOS', 'LEG', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB', 'LYV',
        'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NLOK', 'NLSN', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA',
        'ODFL', 'OGN', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OTIS', 'OXY',
        'PARA', 'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PVH', 'PWR', 'PXD', 'PYPL',
        'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX',
        'SBAC', 'SBNY', 'SBUX', 'SCHW', 'SEDG', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY',
        'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO', 'TMUS', 'TPG', 'TPR', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TXN', 'TXT', 'TYL',
        'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ',
        'WAB', 'WAT', 'WBA', 'WBD', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS'
    ]
    
    print(f"Loaded {len(sp500_symbols)} S&P 500 symbols")
    return sp500_symbols

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
        # Conditional S&P 500 test - ONLY run in production mode
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

    # Check what data we already have
    can_do_incremental, reason = should_do_incremental_update(last_date, existing_symbols, tickers)
    print(f"Update decision: {reason}")
    
    # Continue with your existing if/else logic...
    if can_do_incremental:
        print("=== PERFORMING INCREMENTAL UPDATE ===")
        
        # Fetch only new data
        good_dfs, bad_tickers = fetch_incremental_data(
            tickers, last_date, end_date, min_days_needed, batch_size, delay_between_batches
        )
        
        print(f"Incremental fetch: {len(good_dfs)} symbols updated, {len(bad_tickers)} failed")
        
        if good_dfs:
            # Combine new data with standardized columns
            print("🔧 Standardizing incremental data columns...")
            standardized_dfs = []
            
            for i, df_temp in enumerate(good_dfs):
                print(f"  DEBUG: Incremental DataFrame {i} columns before standardization: {list(df_temp.columns)}")
                
                # Flatten MultiIndex columns if they exist
                if isinstance(df_temp.columns, pd.MultiIndex):
                    print(f"  🔧 Flattening MultiIndex columns for incremental DataFrame {i}")
                    df_temp.columns = df_temp.columns.get_level_values(0)
                
                # Now standardize column order
                expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'symbol', 'Date']
                df_temp = df_temp[expected_columns]
                standardized_dfs.append(df_temp)
                print(f"  ✅ Incremental DataFrame {i} standardized: {list(df_temp.columns)}")
                
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

        # Create batches (this was missing!)
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
                
                # Now standardize column order
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
