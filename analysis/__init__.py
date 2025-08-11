"""
Analysis Engine Package for BullBoard Application
Advanced analytics for stocks and portfolios
"""

from .stock_analyzer import (
    calculate_comprehensive_risk_profile,
    analyze_performance_context,
    calculate_quality_metrics
)

from .portfolio_analyzer import (
    detect_market_regime,
    generate_portfolio_optimization_insights
)

from .insights_generator import (
    generate_comprehensive_analysis,
    generate_market_regime_insights
)

__version__ = "1.0.0"

__all__ = [
    'calculate_comprehensive_risk_profile',
    'analyze_performance_context', 
    'calculate_quality_metrics',
    'detect_market_regime',
    'generate_portfolio_optimization_insights',
    'generate_comprehensive_analysis',
    'generate_market_regime_insights'
]
