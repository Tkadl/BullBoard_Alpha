"""
Portfolio-Level Analysis Module
Market regime detection and portfolio optimization insights
"""


def detect_market_regime(portfolio_data):
    """Detect current market regime with confidence levels"""
    positive_stocks = (portfolio_data['total_return'] > 0).sum()
    total_stocks = len(portfolio_data)
    avg_volatility = portfolio_data['volatility_21'].mean()
    avg_return = portfolio_data['total_return'].mean()
    
    positive_ratio = positive_stocks / total_stocks
    
    if positive_ratio > 0.7 and avg_return > 0.1:
        return {
            'regime': 'Bull Market', 
            'confidence': 'High', 
            'description': f'{positive_ratio:.0%} of stocks positive with {avg_return:.1%} average return',
            'characteristics': 'Broad-based gains with strong momentum'
        }
    elif positive_ratio < 0.4 and avg_return < 0:
        return {
            'regime': 'Bear Market', 
            'confidence': 'High', 
            'description': f'{positive_ratio:.0%} of stocks positive with {avg_return:.1%} average return',
            'characteristics': 'Widespread declines across holdings'
        }
    elif avg_volatility > 0.08:
        return {
            'regime': 'High Volatility', 
            'confidence': 'Medium', 
            'description': f'Average volatility at {avg_volatility:.1%}',
            'characteristics': 'Elevated uncertainty and price swings'
        }
    else:
        return {
            'regime': 'Neutral Market', 
            'confidence': 'Medium', 
            'description': f'{positive_ratio:.0%} positive stocks, {avg_volatility:.1%} average volatility',
            'characteristics': 'Mixed signals with no clear directional bias'
        }


def generate_portfolio_optimization_insights(summary_data):
    """Generate objective portfolio construction insights - educational only"""
    insights = []
    
    # Top performers by different metrics (FACTUAL REPORTING)
    top_sharpe = summary_data.nlargest(3, 'avg_sharpe_21')['symbol'].tolist()
    top_return = summary_data.nlargest(3, 'total_return')['symbol'].tolist()
    low_risk = summary_data.nsmallest(3, 'avg_custom_risk_score')['symbol'].tolist()
    
    # CHANGED: More objective language
    insights.append(f"📊 **Highest Risk-Adjusted Returns**: {', '.join(top_sharpe)} show the best Sharpe ratios in your selection")
    insights.append(f"📈 **Top Absolute Returns**: {', '.join(top_return)} delivered the highest total returns")
    insights.append(f"📉 **Most Stable**: {', '.join(low_risk)} exhibit the lowest volatility patterns")
    
    # Risk distribution analysis (FACTUAL)
    high_risk_count = (summary_data['avg_custom_risk_score'] > 0.08).sum()
    total_count = len(summary_data)
    risk_percentage = (high_risk_count / total_count) * 100
    
    if high_risk_count / total_count > 0.5:
        insights.append(f"⚠️ **Risk Concentration**: {risk_percentage:.0f}% of your selection ({high_risk_count}/{total_count} stocks) shows elevated risk")
    elif high_risk_count > 0:
        insights.append(f"📊 **Risk Distribution**: {risk_percentage:.0f}% of your selection ({high_risk_count}/{total_count} stocks) shows elevated risk")
    else:
        insights.append(f"🛡️ **Risk Distribution**: All selected stocks show moderate to low risk characteristics")
    
    return insights
