"""
ETL Utility Functions
Helper functions for date handling, file operations, and symbol management
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, date
import time

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
        
        start_date = "2024-01-01"  # Current existing start date
        
        print(f"📅 Market-aware dates: {start_date} to {end_date} (Market TZ: {now_market.strftime('%Y-%m-%d %H:%M %Z')})")
        
        return start_date, end_date, market_tz
        
    except Exception as e:
        print(f"⚠️ Error in market date calculation, falling back to simple dates: {e}")
        # Fallback to your existing logic
        from datetime import date
        start_date = "2024-01-01"
        end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # Use yesterday
        return start_date, end_date, None


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
  
