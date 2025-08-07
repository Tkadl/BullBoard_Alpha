"""
Application Settings and Configuration
Contains analysis parameters, chart settings, and defaults
"""

# ==========================================
# ANALYSIS SETTINGS
# ==========================================

# Risk thresholds for stock categorization
HIGH_RISK_THRESHOLD = 0.15
MODERATE_RISK_THRESHOLD = 0.08
LOW_RISK_THRESHOLD = 0.04

# Return categories for performance classification
EXCELLENT_RETURN_THRESHOLD = 0.2  # 20%+
STRONG_RETURN_THRESHOLD = 0.15    # 15%+
GOOD_RETURN_THRESHOLD = 0.05      # 5%+
MODEST_RETURN_THRESHOLD = 0        # 0%+

# Data processing parameters
MIN_DAYS_NEEDED = 65
ROLLING_WINDOW_DAYS = 21
MAX_DRAWDOWN_DAYS = 63

# Volatility analysis
HIGH_VOLATILITY_THRESHOLD = 0.08
MODERATE_VOLATILITY_THRESHOLD = 0.05

# Sharpe ratio categories
EXCELLENT_SHARPE_THRESHOLD = 1.2
GOOD_SHARPE_THRESHOLD = 0.8
MODERATE_SHARPE_THRESHOLD = 0.3

# ==========================================
# CHART CONFIGURATIONS
# ==========================================

# Chart dimensions
CHART_HEIGHT = 500
PERFORMANCE_CHART_HEIGHT = 400
CORRELATION_HEATMAP_HEIGHT = 500
METRICS_CHART_HEIGHT = 400

# Color schemes
CHART_COLOR_SCHEME = 'RdYlGn'
DEFAULT_CHART_COLORS = ['#e74c3c', '#2ecc71', '#3498db']
QUALITATIVE_COLORS = 'Set1'

# Chart styling
CHART_BACKGROUND_COLOR = 'rgba(0,0,0,0)'
CHART_PAPER_BACKGROUND = 'rgba(0,0,0,0)'
CHART_FONT_FAMILY = "Inter"
CHART_FONT_SIZE = 12
CHART_TITLE_FONT_SIZE = 20

# ==========================================
# UI DEFAULTS
# ==========================================

# Debug mode settings
DEBUG_MODE = False
DEBUG_TICKERS = ['AAPL', 'MSFT', 'GOOGL']

# ETL settings (if needed for UI display)
BATCH_SIZE = 1
DELAY_BETWEEN_BATCHES = 2
MAX_RETRIES = 3

# Portfolio analysis defaults
DEFAULT_PORTFOLIO_SIZE_WARNING = 3  # Warn if less than 3 stocks
GOOD_PORTFOLIO_SIZE = 6             # Consider 6+ stocks well diversified
ITEMS_PER_BROWSE_PAGE = 15          # For pagination

# Performance categories
MILESTONE_INTERVAL = 25  # Show progress every 25 stocks
LARGE_PORTFOLIO_THRESHOLD = 50  # Different handling for 50+ stocks
