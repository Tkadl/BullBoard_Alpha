"""
Insights Generation Module
Comprehensive analysis and narrative generation for stocks and portfolios
"""

from .stock_analyzer import (
    calculate_comprehensive_risk_profile,
    analyze_performance_context,
    calculate_quality_metrics
)
from .portfolio_analyzer import detect_market_regime


def generate_comprehensive_analysis(symbol, data, portfolio_context):
    """Generate comprehensive, objective stock analysis - guaranteed insights"""
    insights = []
    
    # Get all analysis components
    risk_profile = calculate_comprehensive_risk_profile(symbol, data)
    performance_context = analyze_performance_context(symbol, data, portfolio_context)
    quality_metrics = calculate_quality_metrics(symbol, data)
    
    # Extract key metrics
    total_return = data.get('total_return', 0)
    volatility = data.get('volatility_21', 0)
    sharpe_ratio = data.get('avg_sharpe_21', 0)
    avg_return = data.get('avg_rolling_yield_21', 0)
    
    # 1. PERFORMANCE SUMMARY (Always included)
    if total_return > 0.20:
        insights.append(f"🚀 **Performance**: {symbol} generated strong {total_return:.1%} returns during the selected period")
    elif total_return > 0.05:
        insights.append(f"📈 **Performance**: {symbol} gained {total_return:.1%} over the analysis period")
    elif total_return > 0:
        insights.append(f"📊 **Performance**: {symbol} posted modest {total_return:.1%} returns")
    elif total_return > -0.10:
        insights.append(f"📉 **Performance**: {symbol} declined {abs(total_return):.1%} during the period")
    else:
        insights.append(f"📉 **Performance**: {symbol} experienced significant decline of {abs(total_return):.1%}")
    
    # 2. RISK ASSESSMENT (Always included)
    volatility_info = risk_profile['volatility']
    insights.append(f"📊 **Risk Profile**: {volatility_info['description']}")
    
    # 3. EFFICIENCY ANALYSIS (Always included)
    if sharpe_ratio > 1.2:
        insights.append(f"⭐ **Efficiency**: Excellent risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    elif sharpe_ratio > 0.8:
        insights.append(f"✅ **Efficiency**: Good risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    elif sharpe_ratio > 0.3:
        insights.append(f"📊 **Efficiency**: Moderate risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    else:
        insights.append(f"⚠️ **Efficiency**: Below-average risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    
    # 4. TREND ANALYSIS (Always included)
    if avg_return > 0.001:
        annualized_trend = avg_return * 252
        insights.append(f"📈 **Trend**: Daily average return of {avg_return:.3%} projects to {annualized_trend:.1%} annualized")
    elif avg_return < -0.001:
        annualized_trend = avg_return * 252
        insights.append(f"📉 **Trend**: Daily average decline of {abs(avg_return):.3%} projects to {abs(annualized_trend):.1%} annualized")
    else:
        insights.append(f"📊 **Trend**: Flat trend with minimal daily movement averaging {avg_return:.3%}")
    
    # 5. QUALITY METRICS (Always included)  
    if quality_metrics['overall'] > 70:
        insights.append(f"🏆 **Quality Score**: High rating of {quality_metrics['overall']}/100 across key metrics")
    elif quality_metrics['overall'] > 50:
        insights.append(f"📊 **Quality Score**: Moderate rating of {quality_metrics['overall']}/100 across key metrics")
    else:
        insights.append(f"📊 **Quality Score**: Below-average rating of {quality_metrics['overall']}/100 across key metrics")
    
    # 6. CONTEXT INSIGHTS (if available)
    insights.extend(performance_context)
    
    # 7. DRAWDOWN ANALYSIS (Always included)
    drawdown_info = risk_profile['drawdown']
    insights.append(f"📊 **Downside Risk**: {drawdown_info['description']}")
    
    # 8. FINAL FACTUAL SUMMARY (Always included)
    risk_category = "high-risk" if volatility > 0.08 else "moderate-risk" if volatility > 0.05 else "low-risk"
    return_category = "strong gains" if total_return > 0.15 else "moderate gains" if total_return > 0.05 else "modest gains" if total_return > 0 else "negative returns"
    
    insights.append(f"📋 **Profile**: {symbol} is a {risk_category} stock showing {return_category} over your selected timeframe")
    
    return insights


def generate_market_regime_insights(summary_data):
    """Generate market regime analysis"""
    regime = detect_market_regime(summary_data)
    insights = []
    
    insights.append(f"🌐 **Market Regime**: {regime['regime']} detected with {regime['confidence'].lower()} confidence")
    insights.append(f"📊 **Regime Details**: {regime['description']} - {regime['characteristics']}")
    
    # Regime-specific insights
    if regime['regime'] == 'Bull Market':
        insights.append("💡 **Market Context**: Favorable conditions for growth-oriented strategies")
    elif regime['regime'] == 'Bear Market':
        insights.append("💡 **Market Context**: Defensive positioning and risk management priority")
    elif regime['regime'] == 'High Volatility':
        insights.append("💡 **Market Context**: Consider reduced position sizes and increased monitoring")
    else:
        insights.append("💡 **Market Context**: Mixed environment suggests selective, balanced approach")
    
    return insights
