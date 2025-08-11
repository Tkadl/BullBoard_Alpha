"""
Individual Stock Analysis Module
Risk assessment, performance context, and quality metrics for individual stocks
"""

from config.settings import (
    HIGH_RISK_THRESHOLD,
    MODERATE_RISK_THRESHOLD,
    EXCELLENT_SHARPE_THRESHOLD,
    GOOD_SHARPE_THRESHOLD,
    MODERATE_SHARPE_THRESHOLD
)


def calculate_comprehensive_risk_profile(symbol, data):
    """Calculate a comprehensive risk assessment"""
    risk_factors = {}
    
    # 1. Volatility Risk
    volatility = data.get('volatility_21', 0)
    if volatility > 0.08:
        risk_factors['volatility'] = {'level': 'High', 'score': 3, 'description': f'Significant price swings ({volatility:.1%} volatility)'}
    elif volatility > 0.05:
        risk_factors['volatility'] = {'level': 'Moderate', 'score': 2, 'description': f'Moderate price fluctuations ({volatility:.1%} volatility)'}
    else:
        risk_factors['volatility'] = {'level': 'Low', 'score': 1, 'description': f'Relatively stable price movements ({volatility:.1%} volatility)'}
    
    # 2. Drawdown Risk
    max_drawdown = data.get('avg_max_drawdown_63', 0)
    if max_drawdown > 0.20:
        risk_factors['drawdown'] = {'level': 'High', 'score': 3, 'description': f'Large peak-to-trough declines ({max_drawdown:.1%})'}
    elif max_drawdown > 0.10:
        risk_factors['drawdown'] = {'level': 'Moderate', 'score': 2, 'description': f'Moderate downside exposure ({max_drawdown:.1%})'}
    else:
        risk_factors['drawdown'] = {'level': 'Low', 'score': 1, 'description': f'Limited downside risk ({max_drawdown:.1%})'}
    
    # 3. Consistency Risk
    sharpe = data.get('avg_sharpe_21', 0)
    if sharpe < 0.5:
        risk_factors['consistency'] = {'level': 'High', 'score': 3, 'description': f'Inconsistent return patterns (Sharpe: {sharpe:.2f})'}
    elif sharpe < 1.0:
        risk_factors['consistency'] = {'level': 'Moderate', 'score': 2, 'description': f'Moderately consistent returns (Sharpe: {sharpe:.2f})'}
    else:
        risk_factors['consistency'] = {'level': 'Low', 'score': 1, 'description': f'Consistent return generation (Sharpe: {sharpe:.2f})'}
    
    return risk_factors


def analyze_performance_context(symbol, data, portfolio_context):
    """Analyze performance in context of market and peers"""
    insights = []
    
    total_return = data.get('total_return', 0)
    symbol_volatility = data.get('volatility_21', 0)
    
    # Market context
    market_avg = portfolio_context.get('avg_return', 0)
    market_volatility = portfolio_context.get('avg_volatility', 0.05)
    
    # Relative performance analysis
    relative_performance = total_return - market_avg
    if abs(relative_performance) > 0.05:  # 5% difference is significant
        direction = "outperformed" if relative_performance > 0 else "underperformed"
        insights.append(
            f"📊 **Relative Performance**: {symbol} {direction} your selection average by {abs(relative_performance):.1%}"
        )
    
    # Risk-adjusted comparison
    if symbol_volatility < market_volatility * 0.8 and total_return > market_avg:
        insights.append(
            f"🎯 **Risk Efficiency**: {symbol} achieved above-average returns ({total_return:.1%}) with below-average risk ({symbol_volatility:.1%})"
        )
    elif symbol_volatility > market_volatility * 1.2 and total_return < market_avg:
        insights.append(
            f"⚠️ **Risk-Return Mismatch**: {symbol} shows higher risk ({symbol_volatility:.1%}) than average but lower returns ({total_return:.1%})"
        )
    
    return insights


def calculate_quality_metrics(symbol, data):
    """Calculate objective quality metrics (0-100 scale)"""
    metrics = {}
    
    # Consistency Score (based on Sharpe ratio)
    sharpe = data.get('avg_sharpe_21', 0)
    consistency_score = min(100, max(0, (sharpe + 1) * 40))  # Normalize to 0-100
    
    # Efficiency Score (return per unit of risk)
    risk_score = data.get('avg_custom_risk_score', 0.01)
    total_return = data.get('total_return', 0)
    if risk_score > 0:
        efficiency_score = min(100, max(0, (total_return / risk_score) * 5))
    else:
        efficiency_score = 0
    
    # Growth Score (annualized return potential)
    avg_return = data.get('avg_rolling_yield_21', 0)
    annualized_return = avg_return * 252
    growth_score = min(100, max(0, (annualized_return + 0.1) * 200))  # Normalize
    
    # Overall score (weighted average)
    overall_score = (consistency_score * 0.4 + efficiency_score * 0.4 + growth_score * 0.2)
    
    return {
        'consistency': round(consistency_score, 1),
        'efficiency': round(efficiency_score, 1),
        'growth': round(growth_score, 1),
        'overall': round(overall_score, 1)
    }
