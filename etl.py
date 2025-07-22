import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
import time  # Add this import

def validate_data_quality(df, min_days_needed=65):
    """Basic data validation and anomaly detection"""
    print("=== PERFORMING DATA QUALITY CHECKS ===")
    
    original_count = len(df)
    issues = []
    
    # Check 1: Remove extreme price movements (likely data errors >100% in one day)
    if 'daily_return' in df.columns:
        df['temp_return'] = df.groupby('symbol')['Close'].pct_change()
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

def fetch_incremental_data(tickers, last_date, end_date, min_days_needed, batch_size=30, delay_between_batches=2):
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
        
        try:
            raw = yf.download(
                tickers=" ".join(batch),
                start=incremental_start,
                end=end_date,
                group_by='ticker',
                auto_adjust=True,
                progress=False,
                threads=True
            )
            
            if len(batch) == 1:
                ticker = batch[0]
                temp = raw.copy()
                if temp.empty:
                    bad_tickers.append(ticker)
                    continue
                temp['symbol'] = ticker
                temp['Date'] = temp.index
                good_dfs.append(temp.reset_index(drop=True))
            else:
                for ticker in batch:
                    try:
                        temp = raw[ticker].copy()
                        if temp.empty:
                            bad_tickers.append(ticker)
                            continue
                        temp['symbol'] = ticker
                        temp['Date'] = temp.index
                        good_dfs.append(temp.reset_index(drop=True))
                    except KeyError:
                        bad_tickers.append(ticker)
                        continue
                        
        except Exception as e:
            print(f"Error in batch {batch_num}: {e}")
            bad_tickers.extend(batch)
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
    print("=== ETL MAIN FUNCTION STARTED ===")
    
    # === USER CONFIGURATION ===
    tickers = get_sp500_symbols()  # Use dynamic S&P 500 list    
    start_date = "2024-01-01"
    end_date = date.today().strftime("%Y-%m-%d")  # Use date.today() instead
    min_days_needed = 65
    yield_thresh = 0.01          # 1% daily yield
    risk_thresh = 0.06           # Custom risk score
    rolling_vol_days = 21
    rolling_drawdown_days = 63
    batch_size = 20  # Reduced batch size for better reliability with more symbols
    delay_between_batches = 1  # Add delay between batches

    print(f"Checking for existing data and update requirements...")

    # Check what data we already have
    existing_df, last_date, existing_symbols = get_last_update_info()
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
            # Combine new data
            new_df = pd.concat(good_dfs, ignore_index=True)
            new_df = new_df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
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

        # Download data in batches with progress tracking
        total_batches = (len(tickers) + batch_size - 1) // batch_size
        start_time = datetime.now()
        
            
        for batch_num, i in enumerate(range(0, len(tickers), batch_size), 1):
            batch = tickers[i:i+batch_size]
            batch_info = f"Fetching {len(batch)} symbols: {batch[0]} to {batch[-1]}"
      
            
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} symbols)...")
            
            try:
                raw = yf.download(
                    tickers=" ".join(batch),
                    start=start_date,
                    end=end_date,
                    group_by='ticker',
                    auto_adjust=True,
                    progress=False,
                    threads=True
                )
                
                if len(batch) == 1:
                    ticker = batch[0]
                    temp = raw.copy()
                    if temp.empty or len(temp) < min_days_needed:
                        bad_tickers.append(ticker)
                        continue
                    temp['symbol'] = ticker
                    temp['Date'] = temp.index
                    good_dfs.append(temp.reset_index(drop=True))
                else:
                    for ticker in batch:
                        try:
                            temp = raw[ticker].copy()
                            if temp.empty or len(temp) < min_days_needed:
                                bad_tickers.append(ticker)
                                continue
                            temp['symbol'] = ticker
                            temp['Date'] = temp.index
                            good_dfs.append(temp.reset_index(drop=True))
                        except KeyError:
                            bad_tickers.append(ticker)
                            continue
                            
            except Exception as e:
                print(f"Error in batch {batch_num}: {e}")
                bad_tickers.extend(batch)
                continue
            
            # Add delay between batches to be respectful to the API
            if batch_num < total_batches:
                time.sleep(delay_between_batches)
        
        print(f"Successfully fetched: {len(good_dfs)} symbols")
        print(f"Failed to fetch: {len(bad_tickers)} symbols")
        if bad_tickers:
            print(f"Failed symbols: {bad_tickers[:10]}{'...' if len(bad_tickers) > 10 else ''}")

        if good_dfs:
            df = pd.concat(good_dfs, ignore_index=True)
            df = df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
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
    df = df.sort_values(['symbol', 'Date']).reset_index(drop=True)
    df['daily_return'] = df.groupby('symbol')['Close'].pct_change(fill_method=None)
    df['volatility_21'] = df.groupby('symbol')['daily_return'].rolling(rolling_vol_days).std().reset_index(0, drop=True)
    df['rolling_yield_21'] = df.groupby('symbol')['daily_return'].rolling(rolling_vol_days).mean().reset_index(0, drop=True)
    df['sharpe_21'] = (df['rolling_yield_21'] / df['volatility_21']) * np.sqrt(252)
    df['max_drawdown_63'] = df.groupby('symbol')['Close'].rolling(rolling_drawdown_days)\
        .apply(lambda x: (np.max(x) - np.min(x)) / np.max(x) if len(x) > 0 and np.max(x) != 0 else 0, raw=False)\
        .reset_index(0, drop=True)
    df['custom_risk_score'] = df['volatility_21'] * 0.7 + df['max_drawdown_63'] * 0.3

    # Get each stock's latest analytics
    latest = df.sort_values('Date').groupby('symbol').tail(1)
    latest = latest[['symbol', 'Date', 'custom_risk_score', 'rolling_yield_21', 'sharpe_21', 'volatility_21', 'max_drawdown_63']].copy()
    latest = latest.sort_values('custom_risk_score', ascending=False)
    latest.reset_index(drop=True, inplace=True)

    # Data quality validation before saving
    df = validate_data_quality(df)
    
    # Save summary table for Streamlit app
    df.to_csv("latest_results.csv", index=False)
    print(f"Data saved to latest_results.csv with {len(df)} total records for {df['symbol'].nunique()} unique symbols")

if __name__ == "__main__":
    main()
