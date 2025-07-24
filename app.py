import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
TRANSFORMERS_AVAILABLE = False
pipeline = None

# Page configuration
st.set_page_config(
    page_title="BullBoard - Advanced Stock Analytics",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced Header Styling */
   .main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="20" cy="80" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    pointer-events: none;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.logo-icon {
    font-size: 3.5rem;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}

.logo-text h1 {
    margin: 0;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(45deg, #ffffff, #f8f9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.tagline {
    font-size: 1.2rem;
    font-weight: 500;
    opacity: 0.95;
    margin-top: 0.25rem;
}

.value-props {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}

.prop-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: transform 0.3s ease;
}

.prop-item:hover {
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.2);
}

.prop-icon {
    font-size: 1.8rem;
}

.prop-text {
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    white-space: nowrap;
}

.header-subtitle {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 1rem;
    opacity: 0.9;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1.5rem;
        text-align: center;
    }
    
    .value-props {
        justify-content: center;
        gap: 1rem;
    }
    
    .logo-text h1 {
        font-size: 2.5rem;
    }
    
    .tagline {
        font-size: 1rem;
    }
}
    
/* Metric Cards - Fixed height and text positioning */
.metric-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 50%, #ffffff 100%);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 
        0 4px 6px -1px rgba(0, 0, 0, 0.1),
        0 2px 4px -1px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    height: 160px; /* Increased from 140px */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: 8px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 
        0 12px 25px rgba(102, 126, 234, 0.15),
        0 8px 10px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    border-color: rgba(102, 126, 234, 0.3);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-radius: 0 2px 2px 0;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100px;
    height: 100px;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
    border-radius: 50%;
}

.metric-header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.metric-icon {
    font-size: 18px;
    margin-right: 10px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.metric-title {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    line-height: 1.2 !important;
}

.metric-value {
    font-size: 28px !important; /* Slightly smaller to make room */
    font-weight: 800 !important;
    color: #1e293b !important;
    margin: 8px 0 12px 0 !important; /* Added bottom margin */
    line-height: 1.1 !important;
    position: relative;
    z-index: 1;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.metric-subtitle {
    font-size: 13px !important; /* Slightly smaller but still readable */
    color: #667eea !important;
    font-weight: 600 !important;
    position: relative;
    z-index: 1;
    text-transform: capitalize;
    line-height: 1.2 !important;
    margin-bottom: 4px !important; /* Add bottom margin */
    display: block !important; /* Ensure it displays properly */
}

/* Section Headers - Keep existing styles */
.section-header {
    display: flex;
    align-items: center;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e2e8f0;
}

.section-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.section-header h2 {
    margin: 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
}

/* Fix for dark theme text visibility */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.main .block-container {
    color: #ffffff;
}

/* Additional refinements */
.element-container {
    margin-bottom: 0 !important;
}

/* Responsive adjustments for cards */
@media (max-width: 768px) {
    .metric-card {
        height: 120px;
        padding: 16px;
    }
    
    .metric-value {
        font-size: 24px !important;
    }
    
    .metric-title {
        font-size: 10px !important;
    }
}

/* Section Headers - Fixed colors */
.section-header {
    display: flex;
    align-items: center;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e2e8f0;
}

.section-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.section-header h2 {
    margin: 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
}

/* Fix for dark theme text visibility */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.main .block-container {
    color: #ffffff;
}
    
    /* Status Cards */
    .status-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .status-success {
        background: #d5f4e6;
        border-color: #2ecc71;
        color: #27ae60;
    }
    
    .status-warning {
        background: #fef9e7;
        border-color: #f39c12;
        color: #e67e22;
    }
    
    .status-info {
        background: #ebf3fd;
        border-color: #3498db;
        color: #2980b9;
    }
    
    /* AI Insight Cards */
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffd700;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }
    
    .section-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def create_header():
    """Create an enhanced, more appealing header section"""
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <span class="logo-icon">🐂</span>
                <div class="logo-text">
                    <h1>BullBoard</h1>
                    <div class="tagline">Professional Stock Analysis Made Simple</div>
                </div>
            </div>
            <div class="value-props">
                <div class="prop-item">
                    <span class="prop-icon">📊</span>
                    <span class="prop-text">Objective Data</span>
                </div>
                <div class="prop-item">
                    <span class="prop-icon">🎯</span>
                    <span class="prop-text">Clear Insights</span>
                </div>
                <div class="prop-item">
                    <span class="prop-icon">⚡</span>
                    <span class="prop-text">Real-time Analysis</span>
                </div>
            </div>
        </div>
        <div class="header-subtitle">
            Objective insights for informed decision-making • No advice, just facts
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, subtitle="", icon="📊"):
    """Create a metric card using Streamlit components with custom styling"""
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-title">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Return empty string to prevent "None" from appearing
    return ""
        
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

def create_risk_return_scatter(summary):
    """Create interactive risk vs return scatter plot"""
    
    # Remove rows with NaN values that cause plotting issues
    clean_summary = summary.dropna(subset=['avg_custom_risk_score', 'avg_rolling_yield_21', 'total_return'])
    
    if clean_summary.empty:
        st.warning("No valid data available for risk-return analysis.")
        return None
    
    fig = px.scatter(
        clean_summary,
        x='avg_custom_risk_score',
        y='avg_rolling_yield_21',
        size=abs(clean_summary['total_return']) + 0.01,  # Ensure no zero/negative sizes
        color='total_return',
        hover_name='symbol',
        title="Risk vs Return Analysis",
        labels={
            'avg_custom_risk_score': 'Risk Score',
            'avg_rolling_yield_21': 'Average Return',
            'total_return': 'Total Return'
        },
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        title_font_size=16,
        height=500,
        showlegend=True
    )
    
    return fig

def create_performance_chart(filtered_df, selected_symbols):
    """Create normalized performance comparison chart"""
    if len(selected_symbols) == 0:
        return None
    
    # Calculate normalized performance
    perf_data = []
    for symbol in selected_symbols:
        symbol_data = filtered_df[filtered_df['symbol'] == symbol].sort_values('Date')
        if not symbol_data.empty:
            symbol_data = symbol_data.copy()
            symbol_data['normalized'] = symbol_data['Close'] / symbol_data['Close'].iloc[0] * 100
            perf_data.append(symbol_data[['Date', 'normalized', 'symbol']])
    
    if not perf_data:
        return None
    
    combined_data = pd.concat(perf_data)
    
    fig = px.line(
        combined_data,
        x='Date',
        y='normalized',
        color='symbol',
        title="Normalized Performance Comparison (Base 100)",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_layout(
        title={
            'text': "Normalized Performance Comparison (Base 100)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        hovermode='x unified'
    )
    
    fig.update_xaxes(gridcolor='lightgray', gridwidth=0.5)
    fig.update_yaxes(gridcolor='lightgray', gridwidth=0.5)
    
    return fig

def create_portfolio_metrics_chart(summary):
    """Create portfolio metrics comparison chart"""
    metrics = ['volatility_21', 'avg_rolling_yield_21', 'avg_sharpe_21']
    metric_names = ['Volatility', 'Expected Return', 'Sharpe Ratio']
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=metric_names,
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['#e74c3c', '#2ecc71', '#3498db']
    
    for i, (metric, name, color) in enumerate(zip(metrics, metric_names, colors)):
        top_5 = summary.nlargest(5, metric)
        
        fig.add_trace(
            go.Bar(
                x=top_5['symbol'],
                y=top_5[metric],
                name=name,
                marker_color=color,
                showlegend=False
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(
        title={
            'text': "Top 5 Stocks by Key Metrics",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def create_correlation_heatmap(filtered_df, selected_symbols):
    """Create correlation heatmap for selected stocks"""
    if len(selected_symbols) < 2:
        return None
    
    # Pivot data to get returns for each stock
    pivot_data = filtered_df.pivot(index='Date', columns='symbol', values='daily_return')
    pivot_data = pivot_data[selected_symbols].dropna()
    
    if pivot_data.empty:
        return None
    
    correlation_matrix = pivot_data.corr()
    
    fig = px.imshow(
        correlation_matrix,
        title="Stock Correlation Matrix",
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    
    fig.update_layout(
        title={
            'text': "Stock Correlation Matrix",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        font=dict(family="Inter", size=12),
        height=500
    )
    
    return fig

def get_sector_mapping():
    """Map stocks to sectors for better organization"""
    return {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'CSCO', 'INTC', 'AMD', 'QCOM', 'TXN', 'AVGO', 'PYPL', 'UBER', 'SNOW'],
        'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'TFC', 'PNC', 'COF', 'AXP', 'BLK', 'SCHW', 'CB', 'ICE', 'CME', 'SPGI', 'MCO', 'V', 'MA'],
        'Healthcare': ['UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'ABT', 'LLY', 'MRK', 'BMY', 'AMGN', 'GILD', 'CVS', 'CI', 'ANTM', 'HUM', 'CNC', 'BIIB', 'REGN', 'VRTX', 'ISRG'],
        'Consumer Discretionary': ['HD', 'NKE', 'MCD', 'LOW', 'SBUX', 'TJX', 'BKNG', 'MAR', 'GM', 'F', 'CCL', 'RCL', 'MGM', 'DIS', 'CMCSA'],
        'Consumer Staples': ['WMT', 'PG', 'KO', 'PEP', 'COST', 'WBA', 'EL', 'CL', 'KMB', 'GIS', 'K', 'HSY', 'MDLZ'],
        'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'OXY', 'BKR'],
        'Industrials': ['BA', 'CAT', 'HON', 'UPS', 'RTX', 'LMT', 'GE', 'MMM', 'FDX', 'NOC', 'UNP', 'CSX', 'NSC'],
        'Materials': ['LIN', 'APD', 'ECL', 'FCX', 'NEM', 'DOW', 'DD', 'PPG', 'SHW', 'NUE'],
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'EXC', 'XEL', 'SRE', 'AEP', 'ES', 'AWK'],
        'Real Estate': ['AMT', 'CCI', 'PLD', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'WELL', 'SPG']
    }

def create_enhanced_stock_selection(unique_symbols):
    """Create enhanced stock selection with sector filtering"""
    sector_mapping = get_sector_mapping()
    
    # Create reverse mapping for symbols not in defined sectors
    symbol_to_sector = {}
    for sector, symbols in sector_mapping.items():
        for symbol in symbols:
            symbol_to_sector[symbol] = sector
    
    # Add "Other" category for symbols not in predefined sectors
    other_symbols = [sym for sym in unique_symbols if sym not in symbol_to_sector]
    if other_symbols:
        sector_mapping['Other'] = other_symbols
        for sym in other_symbols:
            symbol_to_sector[sym] = 'Other'
    
    # Sector filter UI
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_sectors = st.multiselect(
            "Filter by Sector",
            options=list(sector_mapping.keys()),
            default=['Technology', 'Financial Services', 'Healthcare'],  # Start with popular sectors
            help="Select sectors to filter available stocks"
        )
    
    with col2:
        if st.button("🏢 All Sectors", key="select_all_sectors"):
            selected_sectors = list(sector_mapping.keys())
            st.rerun()
    
    # Get filtered symbols based on selected sectors
    filtered_symbols = []
    for sector in selected_sectors:
        if sector in sector_mapping:
            filtered_symbols.extend(sector_mapping[sector])
    
    # Remove duplicates and filter to only available symbols
    filtered_symbols = list(set(filtered_symbols))
    available_symbols = [sym for sym in filtered_symbols if sym in unique_symbols]
    available_symbols.sort()
    
    # Stock selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_symbols = st.multiselect(
            "Choose stocks to analyze",
            available_symbols,
            default=available_symbols[:8] if len(available_symbols) >= 8 else available_symbols,
            help="Select stocks for detailed analysis and comparison"
        )
    
    with col2:
        if st.button("📈 Select All", key="select_all_stocks"):
            selected_symbols = available_symbols
            st.rerun()
    
    # Show selection summary
    if selected_symbols:
        st.info(f"Selected {len(selected_symbols)} stocks from {len(selected_sectors)} sectors")
    
    return selected_symbols

def get_complete_symbol_name_mapping():
    """Complete mapping of S&P 500 ticker symbols to company names"""
    return {
        # A
        'A': 'Agilent Technologies Inc.',
        'AAL': 'American Airlines Group Inc.',
        'AAP': 'Advance Auto Parts Inc.',
        'AAPL': 'Apple Inc.',
        'ABBV': 'AbbVie Inc.',
        'ABC': 'AmerisourceBergen Corp.',
        'ABMD': 'Abiomed Inc.',
        'ABT': 'Abbott Laboratories',
        'ACN': 'Accenture PLC',
        'ADBE': 'Adobe Inc.',
        'ADI': 'Analog Devices Inc.',
        'ADM': 'Archer-Daniels-Midland Co.',
        'ADP': 'Automatic Data Processing Inc.',
        'ADSK': 'Autodesk Inc.',
        'AEE': 'Ameren Corp.',
        'AEP': 'American Electric Power Co. Inc.',
        'AES': 'AES Corp.',
        'AFL': 'Aflac Inc.',
        'AIG': 'American International Group Inc.',
        'AIZ': 'Assurant Inc.',
        'AJG': 'Arthur J. Gallagher & Co.',
        'AKAM': 'Akamai Technologies Inc.',
        'ALB': 'Albemarle Corp.',
        'ALGN': 'Align Technology Inc.',
        'ALK': 'Alaska Air Group Inc.',
        'ALL': 'Allstate Corp.',
        'ALLE': 'Allegion PLC',
        'AMAT': 'Applied Materials Inc.',
        'AMCR': 'Amcor PLC',
        'AMD': 'Advanced Micro Devices Inc.',
        'AME': 'AMETEK Inc.',
        'AMGN': 'Amgen Inc.',
        'AMP': 'Ameriprise Financial Inc.',
        'AMT': 'American Tower Corp.',
        'AMZN': 'Amazon.com Inc.',
        'ANET': 'Arista Networks Inc.',
        'ANSS': 'ANSYS Inc.',
        'AON': 'Aon PLC',
        'AOS': 'A.O. Smith Corp.',
        'APA': 'APA Corp.',
        'APD': 'Air Products and Chemicals Inc.',
        'APH': 'Amphenol Corp.',
        'APTV': 'Aptiv PLC',
        'ARE': 'Alexandria Real Estate Equities Inc.',
        'ATO': 'Atmos Energy Corp.',
        'ATVI': 'Activision Blizzard Inc.',
        'AVB': 'AvalonBay Communities Inc.',
        'AVGO': 'Broadcom Inc.',
        'AVY': 'Avery Dennison Corp.',
        'AWK': 'American Water Works Co. Inc.',
        'AXP': 'American Express Co.',
        'AZO': 'AutoZone Inc.',
        
        # B
        'BA': 'Boeing Co.',
        'BAC': 'Bank of America Corp.',
        'BALL': 'Ball Corp.',
        'BAX': 'Baxter International Inc.',
        'BBWI': 'Bath & Body Works Inc.',
        'BBY': 'Best Buy Co. Inc.',
        'BDX': 'Becton Dickinson and Co.',
        'BEN': 'Franklin Resources Inc.',
        'BF-B': 'Brown-Forman Corp.',
        'BIIB': 'Biogen Inc.',
        'BIO': 'Bio-Rad Laboratories Inc.',
        'BK': 'Bank of New York Mellon Corp.',
        'BKNG': 'Booking Holdings Inc.',
        'BKR': 'Baker Hughes Co.',
        'BLK': 'BlackRock Inc.',
        'BMY': 'Bristol-Myers Squibb Co.',
        'BR': 'Broadridge Financial Solutions Inc.',
        'BRK-B': 'Berkshire Hathaway Inc.',
        'BRO': 'Brown & Brown Inc.',
        'BSX': 'Boston Scientific Corp.',
        'BWA': 'BorgWarner Inc.',
        
        # C
        'C': 'Citigroup Inc.',
        'CAG': 'Conagra Brands Inc.',
        'CAH': 'Cardinal Health Inc.',
        'CARR': 'Carrier Global Corp.',
        'CAT': 'Caterpillar Inc.',
        'CB': 'Chubb Ltd.',
        'CBOE': 'Cboe Global Markets Inc.',
        'CBRE': 'CBRE Group Inc.',
        'CCI': 'Crown Castle Inc.',
        'CCL': 'Carnival Corp.',
        'CDAY': 'Ceridian HCM Holding Inc.',
        'CDNS': 'Cadence Design Systems Inc.',
        'CDW': 'CDW Corp.',
        'CE': 'Celanese Corp.',
        'CEG': 'Constellation Energy Corp.',
        'CHTR': 'Charter Communications Inc.',
        'CI': 'Cigna Corp.',
        'CINF': 'Cincinnati Financial Corp.',
        'CL': 'Colgate-Palmolive Co.',
        'CLX': 'Clorox Co.',
        'CMA': 'Comerica Inc.',
        'CMCSA': 'Comcast Corp.',
        'CME': 'CME Group Inc.',
        'CMG': 'Chipotle Mexican Grill Inc.',
        'CMI': 'Cummins Inc.',
        'CMS': 'CMS Energy Corp.',
        'CNC': 'Centene Corp.',
        'CNP': 'CenterPoint Energy Inc.',
        'COF': 'Capital One Financial Corp.',
        'COO': 'Cooper Cos. Inc.',
        'COP': 'ConocoPhillips',
        'COST': 'Costco Wholesale Corp.',
        'CPB': 'Campbell Soup Co.',
        'CPRT': 'Copart Inc.',
        'CRM': 'Salesforce Inc.',
        'CSCO': 'Cisco Systems Inc.',
        'CSX': 'CSX Corp.',
        'CTAS': 'Cintas Corp.',
        'CTLT': 'Catalent Inc.',
        'CTRA': 'Coterra Energy Inc.',
        'CTSH': 'Cognizant Technology Solutions Corp.',
        'CTVA': 'Corteva Inc.',
        'CVS': 'CVS Health Corp.',
        'CVX': 'Chevron Corp.',
        'CZR': 'Caesars Entertainment Inc.',
        
        # D
        'D': 'Dominion Energy Inc.',
        'DAL': 'Delta Air Lines Inc.',
        'DD': 'DuPont de Nemours Inc.',
        'DE': 'Deere & Co.',
        'DFS': 'Discover Financial Services',
        'DG': 'Dollar General Corp.',
        'DGX': 'Quest Diagnostics Inc.',
        'DHI': 'D.R. Horton Inc.',
        'DHR': 'Danaher Corp.',
        'DIS': 'Walt Disney Co.',
        'DISH': 'DISH Network Corp.',
        'DLR': 'Digital Realty Trust Inc.',
        'DLTR': 'Dollar Tree Inc.',
        'DOV': 'Dover Corp.',
        'DOW': 'Dow Inc.',
        'DPZ': 'Domino\'s Pizza Inc.',
        'DRE': 'Duke Realty Corp.',
        'DRI': 'Darden Restaurants Inc.',
        'DTE': 'DTE Energy Co.',
        'DUK': 'Duke Energy Corp.',
        'DVA': 'DaVita Inc.',
        'DVN': 'Devon Energy Corp.',
        
        # E
        'EA': 'Electronic Arts Inc.',
        'EBAY': 'eBay Inc.',
        'ECL': 'Ecolab Inc.',
        'ED': 'Consolidated Edison Inc.',
        'EFX': 'Equifax Inc.',
        'EIX': 'Edison International',
        'EL': 'Estee Lauder Cos. Inc.',
        'EMN': 'Eastman Chemical Co.',
        'EMR': 'Emerson Electric Co.',
        'ENPH': 'Enphase Energy Inc.',
        'EOG': 'EOG Resources Inc.',
        'EPAM': 'EPAM Systems Inc.',
        'EQIX': 'Equinix Inc.',
        'EQR': 'Equity Residential',
        'ES': 'Eversource Energy',
        'ESS': 'Essex Property Trust Inc.',
        'ETN': 'Eaton Corp. PLC',
        'ETR': 'Entergy Corp.',
        'ETSY': 'Etsy Inc.',
        'EVRG': 'Evergy Inc.',
        'EW': 'Edwards Lifesciences Corp.',
        'EXC': 'Exelon Corp.',
        'EXPD': 'Expeditors International of Washington Inc.',
        'EXPE': 'Expedia Group Inc.',
        'EXR': 'Extended Stay America Inc.',
        
        # F
        'F': 'Ford Motor Co.',
        'FANG': 'Diamondback Energy Inc.',
        'FAST': 'Fastenal Co.',
        'FBHS': 'Fortune Brands Home & Security Inc.',
        'FCX': 'Freeport-McMoRan Inc.',
        'FDS': 'FactSet Research Systems Inc.',
        'FDX': 'FedEx Corp.',
        'FE': 'FirstEnergy Corp.',
        'FFIV': 'F5 Inc.',
        'FIS': 'Fidelity National Information Services Inc.',
        'FISV': 'Fiserv Inc.',
        'FITB': 'Fifth Third Bancorp',
        'FLT': 'FleetCor Technologies Inc.',
        'FMC': 'FMC Corp.',
        'FOX': 'Fox Corp.',
        'FOXA': 'Fox Corp.',
        'FRC': 'First Republic Bank',
        'FRT': 'Federal Realty Investment Trust',
        'FTNT': 'Fortinet Inc.',
        'FTV': 'Fortive Corp.',
        
        # G
        'GD': 'General Dynamics Corp.',
        'GE': 'General Electric Co.',
        'GILD': 'Gilead Sciences Inc.',
        'GIS': 'General Mills Inc.',
        'GL': 'Globe Life Inc.',
        'GLW': 'Corning Inc.',
        'GM': 'General Motors Co.',
        'GNRC': 'Generac Holdings Inc.',
        'GOOG': 'Alphabet Inc.',
        'GOOGL': 'Alphabet Inc.',
        'GPC': 'Genuine Parts Co.',
        'GPN': 'Global Payments Inc.',
        'GRMN': 'Garmin Ltd.',
        'GS': 'Goldman Sachs Group Inc.',
        'GWW': 'W.W. Grainger Inc.',
        
        # H
        'HAL': 'Halliburton Co.',
        'HAS': 'Hasbro Inc.',
        'HBAN': 'Huntington Bancshares Inc.',
        'HBI': 'Hanesbrands Inc.',
        'HCA': 'HCA Healthcare Inc.',
        'HD': 'Home Depot Inc.',
        'HES': 'Hess Corp.',
        'HIG': 'Hartford Financial Services Group Inc.',
        'HII': 'Huntington Ingalls Industries Inc.',
        'HLT': 'Hilton Worldwide Holdings Inc.',
        'HOLX': 'Hologic Inc.',
        'HON': 'Honeywell International Inc.',
        'HPE': 'Hewlett Packard Enterprise Co.',
        'HPQ': 'HP Inc.',
        'HRL': 'Hormel Foods Corp.',
        'HSIC': 'Henry Schein Inc.',
        'HST': 'Host Hotels & Resorts Inc.',
        'HSY': 'Hershey Co.',
        'HUM': 'Humana Inc.',
        'HWM': 'Howmet Aerospace Inc.',
        
        # I
        'IBM': 'International Business Machines Corp.',
        'ICE': 'Intercontinental Exchange Inc.',
        'IDXX': 'IDEXX Laboratories Inc.',
        'IEX': 'IDEX Corp.',
        'IFF': 'International Flavors & Fragrances Inc.',
        'ILMN': 'Illumina Inc.',
        'INCY': 'Incyte Corp.',
        'INFO': 'IHS Markit Ltd.',
        'INTC': 'Intel Corp.',
        'INTU': 'Intuit Inc.',
        'IP': 'International Paper Co.',
        'IPG': 'Interpublic Group of Cos. Inc.',
        'IPGP': 'IPG Photonics Corp.',
        'IQV': 'IQVIA Holdings Inc.',
        'IR': 'Ingersoll Rand Inc.',
        'IRM': 'Iron Mountain Inc.',
        'ISRG': 'Intuitive Surgical Inc.',
        'IT': 'Gartner Inc.',
        'ITW': 'Illinois Tool Works Inc.',
        'IVZ': 'Invesco Ltd.',
        
        # J
        'JBHT': 'J.B. Hunt Transport Services Inc.',
        'JCI': 'Johnson Controls International PLC',
        'JKHY': 'Jack Henry & Associates Inc.',
        'JNJ': 'Johnson & Johnson',
        'JNPR': 'Juniper Networks Inc.',
        'JPM': 'JPMorgan Chase & Co.',
        'JWN': 'Nordstrom Inc.',
        
        # K
        'K': 'Kellogg Co.',
        'KEY': 'KeyCorp',
        'KEYS': 'Keysight Technologies Inc.',
        'KHC': 'Kraft Heinz Co.',
        'KIM': 'Kimco Realty Corp.',
        'KLAC': 'KLA Corp.',
        'KMB': 'Kimberly-Clark Corp.',
        'KMI': 'Kinder Morgan Inc.',
        'KMX': 'CarMax Inc.',
        'KO': 'Coca-Cola Co.',
        'KR': 'Kroger Co.',
        'KSS': 'Kohl\'s Corp.',
        
        # L
        'L': 'Loews Corp.',
        'LDOS': 'Leidos Holdings Inc.',
        'LEG': 'Leggett & Platt Inc.',
        'LEN': 'Lennar Corp.',
        'LH': 'Laboratory Corp. of America Holdings',
        'LHX': 'L3Harris Technologies Inc.',
        'LIN': 'Linde PLC',
        'LKQ': 'LKQ Corp.',
        'LLY': 'Eli Lilly and Co.',
        'LMT': 'Lockheed Martin Corp.',
        'LNC': 'Lincoln National Corp.',
        'LNT': 'Alliant Energy Corp.',
        'LOW': 'Lowe\'s Cos. Inc.',
        'LRCX': 'Lam Research Corp.',
        'LUMN': 'Lumen Technologies Inc.',
        'LUV': 'Southwest Airlines Co.',
        'LVS': 'Las Vegas Sands Corp.',
        'LW': 'Lamb Weston Holdings Inc.',
        'LYB': 'LyondellBasell Industries NV',
        'LYV': 'Live Nation Entertainment Inc.',
        
        # M
        'MA': 'Mastercard Inc.',
        'MAA': 'Mid-America Apartment Communities Inc.',
        'MAR': 'Marriott International Inc.',
        'MAS': 'Masco Corp.',
        'MCD': 'McDonald\'s Corp.',
        'MCHP': 'Microchip Technology Inc.',
        'MCK': 'McKesson Corp.',
        'MCO': 'Moody\'s Corp.',
        'MDLZ': 'Mondelez International Inc.',
        'MDT': 'Medtronic PLC',
        'MET': 'MetLife Inc.',
        'META': 'Meta Platforms Inc.',
        'MGM': 'MGM Resorts International',
        'MHK': 'Mohawk Industries Inc.',
        'MKC': 'McCormick & Co. Inc.',
        'MKTX': 'MarketAxess Holdings Inc.',
        'MLM': 'Martin Marietta Materials Inc.',
        'MMC': 'Marsh & McLennan Cos. Inc.',
        'MMM': '3M Co.',
        'MNST': 'Monster Beverage Corp.',
        'MO': 'Altria Group Inc.',
        'MOH': 'Molina Healthcare Inc.',
        'MOS': 'Mosaic Co.',
        'MPC': 'Marathon Petroleum Corp.',
        'MPWR': 'Monolithic Power Systems Inc.',
        'MRK': 'Merck & Co. Inc.',
        'MRNA': 'Moderna Inc.',
        'MRO': 'Marathon Oil Corp.',
        'MS': 'Morgan Stanley',
        'MSCI': 'MSCI Inc.',
        'MSFT': 'Microsoft Corp.',
        'MSI': 'Motorola Solutions Inc.',
        'MTB': 'M&T Bank Corp.',
        'MTCH': 'Match Group Inc.',
        'MTD': 'Mettler-Toledo International Inc.',
        'MU': 'Micron Technology Inc.',
        'NCLH': 'Norwegian Cruise Line Holdings Ltd.',
        'NDAQ': 'Nasdaq Inc.',
        'NDSN': 'Nordson Corp.',
        'NEE': 'NextEra Energy Inc.',
        'NEM': 'Newmont Corp.',
        'NFLX': 'Netflix Inc.',
        'NI': 'NiSource Inc.',
        'NKE': 'Nike Inc.',
        'NLOK': 'NortonLifeLock Inc.',
        'NLSN': 'Nielsen Holdings PLC',
        'NOC': 'Northrop Grumman Corp.',
        'NOW': 'ServiceNow Inc.',
        'NRG': 'NRG Energy Inc.',
        'NSC': 'Norfolk Southern Corp.',
        'NTAP': 'NetApp Inc.',
        'NTRS': 'Northern Trust Corp.',
        'NUE': 'Nucor Corp.',
        'NVDA': 'NVIDIA Corp.',
        'NVR': 'NVR Inc.',
        'NWL': 'Newell Brands Inc.',
        'NWS': 'News Corp.',
        'NWSA': 'News Corp.',
        
        # O
        'ODFL': 'Old Dominion Freight Line Inc.',
        'OGN': 'Organon & Co.',
        'OKE': 'ONEOK Inc.',
        'OMC': 'Omnicom Group Inc.',
        'ORCL': 'Oracle Corp.',
        'ORLY': 'O\'Reilly Automotive Inc.',
        'OTIS': 'Otis Worldwide Corp.',
        'OXY': 'Occidental Petroleum Corp.',
        
        # P
        'PARA': 'Paramount Global',
        'PAYC': 'Paycom Software Inc.',
        'PAYX': 'Paychex Inc.',
        'PCAR': 'PACCAR Inc.',
        'PCG': 'PG&E Corp.',
        'PEAK': 'Healthpeak Properties Inc.',
        'PEG': 'Public Service Enterprise Group Inc.',
        'PEP': 'PepsiCo Inc.',
        'PFE': 'Pfizer Inc.',
        'PFG': 'Principal Financial Group Inc.',
        'PG': 'Procter & Gamble Co.',
        'PGR': 'Progressive Corp.',
        'PH': 'Parker-Hannifin Corp.',
        'PHM': 'PulteGroup Inc.',
        'PKG': 'Packaging Corp. of America',
        'PKI': 'PerkinElmer Inc.',
        'PLD': 'Prologis Inc.',
        'PM': 'Philip Morris International Inc.',
        'PNC': 'PNC Financial Services Group Inc.',
        'PNR': 'Pentair PLC',
        'PNW': 'Pinnacle West Capital Corp.',
        'POOL': 'Pool Corp.',
        'PPG': 'PPG Industries Inc.',
        'PPL': 'PPL Corp.',
        'PRU': 'Prudential Financial Inc.',
        'PSA': 'Public Storage',
        'PSX': 'Phillips 66',
        'PTC': 'PTC Inc.',
        'PVH': 'PVH Corp.',
        'PWR': 'Quanta Services Inc.',
        'PXD': 'Pioneer Natural Resources Co.',
        'PYPL': 'PayPal Holdings Inc.',
        
        # Q-R
        'QCOM': 'Qualcomm Inc.',
        'QRVO': 'Qorvo Inc.',
        'RCL': 'Royal Caribbean Cruises Ltd.',
        'RE': 'Everest Re Group Ltd.',
        'REG': 'Regency Centers Corp.',
        'REGN': 'Regeneron Pharmaceuticals Inc.',
        'RF': 'Regions Financial Corp.',
        'RHI': 'Robert Half Inc.',
        'RJF': 'Raymond James Financial Inc.',
        'RL': 'Ralph Lauren Corp.',
        'RMD': 'ResMed Inc.',
        'ROK': 'Rockwell Automation Inc.',
        'ROL': 'Rollins Inc.',
        'ROP': 'Roper Technologies Inc.',
        'ROST': 'Ross Stores Inc.',
        'RSG': 'Republic Services Inc.',
        'RTX': 'Raytheon Technologies Corp.',
        
        # S
        'SBAC': 'SBA Communications Corp.',
        'SBNY': 'Signature Bank',
        'SBUX': 'Starbucks Corp.',
        'SCHW': 'Charles Schwab Corp.',
        'SEDG': 'SolarEdge Technologies Inc.',
        'SEE': 'Sealed Air Corp.',
        'SHW': 'Sherwin-Williams Co.',
        'SIVB': 'SVB Financial Group',
        'SJM': 'J.M. Smucker Co.',
        'SLB': 'Schlumberger NV',
        'SNA': 'Snap-on Inc.',
        'SNPS': 'Synopsys Inc.',
        'SO': 'Southern Co.',
        'SPG': 'Simon Property Group Inc.',
        'SPGI': 'S&P Global Inc.',
        'SRE': 'Sempra Energy',
        'STE': 'STERIS PLC',
        'STT': 'State Street Corp.',
        'STX': 'Seagate Technology Holdings PLC',
        'STZ': 'Constellation Brands Inc.',
        'SWK': 'Stanley Black & Decker Inc.',
        'SWKS': 'Skyworks Solutions Inc.',
        'SYF': 'Synchrony Financial',
        'SYK': 'Stryker Corp.',
        'SYY': 'Sysco Corp.',
        
        # T
        'T': 'AT&T Inc.',
        'TAP': 'Molson Coors Beverage Co.',
        'TDG': 'TransDigm Group Inc.',
        'TDY': 'Teledyne Technologies Inc.',
        'TECH': 'Bio-Techne Corp.',
        'TEL': 'TE Connectivity Ltd.',
        'TER': 'Teradyne Inc.',
        'TFC': 'Truist Financial Corp.',
        'TFX': 'Teleflex Inc.',
        'TGT': 'Target Corp.',
        'TJX': 'TJX Cos. Inc.',
        'TMO': 'Thermo Fisher Scientific Inc.',
        'TMUS': 'T-Mobile US Inc.',
        'TPG': 'TPG Inc.',
        'TPR': 'Tapestry Inc.',
        'TRMB': 'Trimble Inc.',
        'TROW': 'T. Rowe Price Group Inc.',
        'TRV': 'Travelers Cos. Inc.',
        'TSCO': 'Tractor Supply Co.',
        'TSLA': 'Tesla Inc.',
        'TSN': 'Tyson Foods Inc.',
        'TT': 'Trane Technologies PLC',
        'TTWO': 'Take-Two Interactive Software Inc.',
        'TXN': 'Texas Instruments Inc.',
        'TXT': 'Textron Inc.',
        'TYL': 'Tyler Technologies Inc.',
        
        # U-V
        'UAL': 'United Airlines Holdings Inc.',
        'UDR': 'UDR Inc.',
        'UHS': 'Universal Health Services Inc.',
        'ULTA': 'Ulta Beauty Inc.',
        'UNH': 'UnitedHealth Group Inc.',
        'UNP': 'Union Pacific Corp.',
        'UPS': 'United Parcel Service Inc.',
        'URI': 'United Rentals Inc.',
        'USB': 'U.S. Bancorp',
        'V': 'Visa Inc.',
        'VFC': 'V.F. Corp.',
        'VLO': 'Valero Energy Corp.',
        'VMC': 'Vulcan Materials Co.',
        'VNO': 'Vornado Realty Trust',
        'VRSK': 'Verisk Analytics Inc.',
        'VRSN': 'VeriSign Inc.',
        'VRTX': 'Vertex Pharmaceuticals Inc.',
        'VTR': 'Ventas Inc.',
        'VTRS': 'Viatris Inc.',
        'VZ': 'Verizon Communications Inc.',
        
        # W-Z
        'WAB': 'Westinghouse Air Brake Technologies Corp.',
        'WAT': 'Waters Corp.',
        'WBA': 'Walgreens Boots Alliance Inc.',
        'WBD': 'Warner Bros. Discovery Inc.',
        'WDC': 'Western Digital Corp.',
        'WEC': 'WEC Energy Group Inc.',
        'WELL': 'Welltower Inc.',
        'WFC': 'Wells Fargo & Co.',
        'WHR': 'Whirlpool Corp.',
        'WM': 'Waste Management Inc.',
        'WMB': 'Williams Cos. Inc.',
        'WMT': 'Walmart Inc.',
        'WRB': 'W.R. Berkley Corp.',
        'WRK': 'WestRock Co.',
        'WST': 'West Pharmaceutical Services Inc.',
        'WTW': 'Willis Towers Watson PLC',
        'WY': 'Weyerhaeuser Co.',
        'XRAY': 'DENTSPLY SIRONA Inc.',
        'XYL': 'Xylem Inc.',
        'YUM': 'Yum! Brands Inc.',
        'ZBH': 'Zimmer Biomet Holdings Inc.',
        'ZBRA': 'Zebra Technologies Corp.',
        'ZION': 'Zions Bancorp NA',
        'ZTS': 'Zoetis Inc.'
    }

def create_user_friendly_stock_selection(unique_symbols):
    """Modern 2-column stock selection interface"""
    
    # Initialize session state for selection basket
    if 'stock_basket' not in st.session_state:
        st.session_state.stock_basket = []
    
    symbol_to_name = get_complete_symbol_name_mapping()
    
    st.markdown("---")
   # Add custom CSS
    st.markdown("""
    <style>
    .gradient-container-left {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 5px 20px 0px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-height: 600px;
    }
    
    .gradient-container-right {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0px 20px 5px;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-height: 600px;
    }
    
    .white-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 12px 15px;
        border-radius: 10px;
        color: #2d3436;
        font-weight: bold;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .portfolio-header {
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
        margin-bottom: 20px;
    }
    
    .white-text {
        color: white !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the layout using HTML containers
    col1, col2 = st.columns([35, 65], gap="large")
    
    with col1:
        st.markdown('<div class="gradient-container-left">', unsafe_allow_html=True)
        
        # Portfolio header
        st.markdown('<div class="portfolio-header">📊 Your Portfolio</div>', unsafe_allow_html=True)
        
        if st.session_state.stock_basket:
            # Display stocks selected
            st.markdown(f'<div class="white-container">{len(st.session_state.stock_basket)} stocks selected:</div>', unsafe_allow_html=True)
            
            # Display each stock
            for symbol in st.session_state.stock_basket:
                company_name = symbol_to_name.get(symbol, symbol)
                
                # Stock display with remove button
                subcol1, subcol2 = st.columns([3, 1])
                with subcol1:
                    st.markdown(f'''
                    <div class="white-container" style="border-left: 4px solid #4facfe;">
                        {symbol} - {company_name[:25]}{'...' if len(company_name) > 25 else ''}
                    </div>
                    ''', unsafe_allow_html=True)
                with subcol2:
                    if st.button("❌", key=f"remove_{symbol}", help="Remove"):
                        st.session_state.stock_basket.remove(symbol)
                        st.rerun()
            
            # Portfolio status
            portfolio_size = len(st.session_state.stock_basket)
            if portfolio_size <= 3:
                status_color = "#ff9500"
                status_text = "Small portfolio"
                status_emoji = "🟡"
            elif portfolio_size <= 6:
                status_color = "#28a745"
                status_text = "Good diversity"
                status_emoji = "🟢"
            else:
                status_color = "#007bff"
                status_text = "Well diversified"
                status_emoji = "🔵"
            
            st.markdown(f'''
            <div style="
                background: rgba(255, 255, 255, 0.95);
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                color: {status_color};
                font-weight: bold;
                margin: 15px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 2px solid {status_color};
            ">
            {status_emoji} {portfolio_size} stocks selected - {status_text}
            </div>
            ''', unsafe_allow_html=True)
            
            # Action buttons
            button_col1, button_col2 = st.columns(2)
            with button_col1:
                if st.button("🗑️ Clear All", key="clear_basket"):
                    st.session_state.stock_basket = []
                    st.rerun()
            with button_col2:
                st.markdown('''
                <div style="
                    background: rgba(255, 255, 255, 0.95);
                    padding: 10px 15px;
                    border-radius: 10px;
                    text-align: center;
                    color: #28a745;
                    font-weight: bold;
                    box-shadow: 0 3px 12px rgba(0,0,0,0.1);
                    border: 2px solid #28a745;
                ">
                ✅ Ready to Analyze!
                </div>
                ''', unsafe_allow_html=True)
        
        else:
            # Empty state
            st.markdown('<div class="white-container" style="text-align: center; padding: 20px;">👈 Select stocks from the categories or search</div>', unsafe_allow_html=True)
            
            st.markdown('<p class="white-text">Quick start suggestions:</p>', unsafe_allow_html=True)
            
            quick_add = ['AAPL', 'MSFT', 'GOOGL']
            for symbol in quick_add:
                if symbol in unique_symbols:
                    if st.button(f"+ Add {symbol}", key=f"quick_{symbol}"):
                        st.session_state.stock_basket.append(symbol)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close left gradient container
    
    with col2:
        st.markdown('<div class="gradient-container-right">', unsafe_allow_html=True)
        
        # Discovery header
        st.markdown('<div class="portfolio-header">🎯 Add Stocks</div>', unsafe_allow_html=True)
        
        # Method selector
        st.markdown('<p class="white-text">Choose method:</p>', unsafe_allow_html=True)
        discovery_method = st.selectbox(
            "",
            ["⚡ Quick Categories", "🔍 Search Stocks", "📊 Browse All"],
            key="discovery_method",
            label_visibility="collapsed"
        )
        
        if discovery_method == "⚡ Quick Categories":
            st.markdown('<div class="white-container">One-click portfolio themes:</div>', unsafe_allow_html=True)
            
            categories = {
                "🍎 Big Tech": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA'],
                "🏦 Major Banks": ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS'],
                "⚡ AI & Chips": ['NVDA', 'AMD', 'INTC', 'QCOM', 'AVGO'],
                "💊 Healthcare": ['UNH', 'JNJ', 'PFE', 'ABBV', 'MRK', 'LLY'],
                "🛒 Consumer": ['WMT', 'COST', 'HD', 'TGT', 'NKE', 'SBUX'],
                "⚡ Energy": ['XOM', 'CVX', 'COP', 'NEE', 'DUK'],
                "🏭 Industrial": ['BA', 'CAT', 'GE', 'HON', 'MMM', 'UPS'],
                "💰 Dividends": ['JNJ', 'PG', 'KO', 'PEP', 'MCD', 'WMT']
            }
            
            # Category buttons in 2 columns
            cat_col1, cat_col2 = st.columns(2, gap="medium")
            category_items = list(categories.items())
            
            with cat_col1:
                for i in range(0, len(category_items), 2):
                    category_name, stocks = category_items[i]
                    if st.button(f"{category_name} ({len(stocks)})", key=f"cat_{i}", use_container_width=True):
                        added_count = 0
                        for stock in stocks:
                            if stock in unique_symbols and stock not in st.session_state.stock_basket:
                                st.session_state.stock_basket.append(stock)
                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} stocks!")
                            st.rerun()
            
            with cat_col2:
                for i in range(1, len(category_items), 2):
                    category_name, stocks = category_items[i]
                    if st.button(f"{category_name} ({len(stocks)})", key=f"cat_{i}", use_container_width=True):
                        added_count = 0
                        for stock in stocks:
                            if stock in unique_symbols and stock not in st.session_state.stock_basket:
                                st.session_state.stock_basket.append(stock)
                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} stocks!")
                            st.rerun()
            
            # Tip
            st.markdown('''
            <div style="
                background: rgba(255, 255, 255, 0.95);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                color: #e17055;
                font-weight: bold;
                margin-top: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid #fdcb6e;
            ">
            💡 Tip: Click any category above to add all its stocks to your portfolio!
            </div>
            ''', unsafe_allow_html=True)
        
        elif discovery_method == "🔍 Search Stocks":
            st.markdown('<div class="white-container">Find companies by name or ticker:</div>', unsafe_allow_html=True)
            
            search_term = st.text_input(
                "",
                placeholder="e.g., 'Apple', 'Tesla', 'AAPL'",
                key="stock_search",
                label_visibility="collapsed"
            )
            
            if search_term:
                matches = []
                search_lower = search_term.lower()
                for symbol in unique_symbols:
                    company_name = symbol_to_name.get(symbol, symbol)
                    if (search_lower in symbol.lower() or 
                        search_lower in company_name.lower()):
                        matches.append((symbol, company_name))
                
                if matches:
                    st.markdown(f'<div class="white-container">Found {len(matches)} matches:</div>', unsafe_allow_html=True)
                    
                    for symbol, company_name in matches[:10]:
                        search_col1, search_col2 = st.columns([3, 1])
                        with search_col1:
                            st.markdown(f'''
                            <div class="white-container" style="border-left: 3px solid #f093fb;">
                                <strong>{symbol}</strong> - {company_name}
                            </div>
                            ''', unsafe_allow_html=True)
                        with search_col2:
                            if st.button("➕", key=f"add_{symbol}", help="Add"):
                                if symbol not in st.session_state.stock_basket:
                                    st.session_state.stock_basket.append(symbol)
                                    st.success(f"Added {symbol}!")
                                    st.rerun()
                else:
                    st.markdown('<div class="white-container" style="color: #e74c3c; text-align: center;">No matches found. Try a different search term.</div>', unsafe_allow_html=True)
        
        elif discovery_method == "📊 Browse All":
            st.markdown('<div class="white-container">All available stocks:</div>', unsafe_allow_html=True)
            
            items_per_page = 15
            total_items = len(unique_symbols)
            total_pages = (total_items - 1) // items_per_page + 1
            
            st.markdown('<p class="white-text">Select page:</p>', unsafe_allow_html=True)
            page = st.selectbox(
                "",
                range(1, total_pages + 1),
                key="browse_page",
                label_visibility="collapsed"
            )
            
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            
            st.markdown(f'<div class="white-container">Showing stocks {start_idx + 1}-{end_idx} of {total_items}:</div>', unsafe_allow_html=True)
            
            for i in range(start_idx, end_idx):
                symbol = unique_symbols[i]
                company_name = symbol_to_name.get(symbol, symbol)
                
                browse_col1, browse_col2 = st.columns([3, 1])
                with browse_col1:
                    st.markdown(f'''
                    <div class="white-container" style="border-left: 3px solid #f093fb;">
                        <strong>{symbol}</strong> - {company_name}
                    </div>
                    ''', unsafe_allow_html=True)
                with browse_col2:
                    if st.button("➕", key=f"browse_add_{symbol}", help="Add"):
                        if symbol not in st.session_state.stock_basket:
                            st.session_state.stock_basket.append(symbol)
                            st.success(f"Added {symbol}!")
                            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close right gradient container
    
    # Return selection
    if st.session_state.stock_basket:
        return st.session_state.stock_basket
    else:
        default_stocks = ['AAPL', 'MSFT', 'GOOGL']
        available_defaults = [stock for stock in default_stocks if stock in unique_symbols]
        return available_defaults[:3] if available_defaults else unique_symbols[:3]

def main():
    create_header()
    
        
        # ETL Pipeline Button
    if st.button("🔄 Refresh Data", key="etl_button"):
        with st.spinner("🔄 Fetching latest market data... This may take 1-2 minutes."):
            import etl
            etl.main()
        st.success("✅ Data updated successfully!")
        st.rerun()

     # Force Refresh UI Button
        if st.button("🔄 Force Refresh UI", key="force_refresh_ui"):
            # Clear all caches
            st.cache_data.clear()
            if hasattr(st, 'cache_resource'):
                st.cache_resource.clear()
            
            # Clear session state
            for key in list(st.session_state.keys()):
                if key not in ['etl_button', 'force_refresh_ui']:  # Keep button states
                    del st.session_state[key]
            
            st.success("UI refreshed! Changes should now be visible.")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Settings")
        
        st.success("🧠 Advanced Rule-Based Analytics Active")
        st.info("💡 Sophisticated insights without AI dependencies")
   
    # Load and validate data
    def load_and_validate_data():
        """Cache the main data loading to avoid repeated CSV reads"""
        try:
            import os
            
            # Check if file exists (log only, don't show to user)
            if not os.path.exists("latest_results.csv"):
                print("❌ File 'latest_results.csv' not found!")  # Console log only
                return None
            
            # Log file info to console
            file_size = os.path.getsize("latest_results.csv")
            print(f"📁 Loading CSV file: {file_size:,} bytes")  # Console log only
            
            # Load data WITHOUT automatic date parsing
            df = pd.read_csv("latest_results.csv")
            
            print(f"📊 Raw data loaded: {df.shape}")  # Debug
            print(f"📊 Columns: {list(df.columns)}")  # Debug
            print(f"📊 Date column sample: {df['Date'].head(3).tolist() if 'Date' in df.columns else 'NO DATE COLUMN'}")  # Debug
            
            # Try to parse dates manually with error handling
            if 'Date' in df.columns:
                try:
                    # Handle different date formats that might exist
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    print("✅ Date parsing successful")
                    
                    # Remove rows with invalid dates
                    invalid_dates = df['Date'].isna().sum()
                    if invalid_dates > 0:
                        print(f"⚠️ Removing {invalid_dates} rows with invalid dates")
                        df = df.dropna(subset=['Date'])
                    
                except Exception as date_error:
                    print(f"⚠️ Date parsing failed: {date_error}")
                    # Keep the data anyway - dates as strings are still usable
            else:
                print("⚠️ No Date column found")
            
            print(f"✅ Final data shape: {df.shape}")  # Debug
            
            if df.empty:
                print("❌ DataFrame is empty after processing")
                return None
                
            if 'symbol' not in df.columns:
                print("❌ Missing 'symbol' column")
                print(f"Available columns: {list(df.columns)}")
                return None
            
            print(f"✅ Loaded {len(df):,} records, {df['symbol'].nunique()} symbols")  # Console log only
            return df
            
        except FileNotFoundError:
            print("❌ File not found: latest_results.csv")
            return None
        except pd.errors.EmptyDataError:
            print("❌ CSV file is empty")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
            
            return df
            
        except FileNotFoundError:
            print("❌ File not found: latest_results.csv")
            return None
        except pd.errors.EmptyDataError:
            print("❌ CSV file is empty")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    # Load and validate data with caching
    df = load_and_validate_data()
    # === ADD THIS DEBUG SECTION HERE ===
    print("=== DEBUG: DATA LOADING RESULT ===")
    try:
        import os
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir('.')}")
        
        if os.path.exists('latest_results.csv'):
            print("✅ latest_results.csv EXISTS")
            file_size = os.path.getsize('latest_results.csv')
            print(f"File size: {file_size:,} bytes")
            
            # Check what load_and_validate_data() actually returned
            print(f"df is None: {df is None}")
            if df is not None:
                print(f"DataFrame shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                print(f"Sample data:")
                print(df.head())
                print(f"Unique symbols: {df['symbol'].nunique() if 'symbol' in df.columns else 'NO SYMBOL COLUMN'}")
            else:
                print("❌ load_and_validate_data() returned None")
                
                # Try loading manually to see what fails
                try:
                    df_test = pd.read_csv('latest_results.csv', parse_dates=["Date"])
                    print(f"Manual load successful: {df_test.shape}")
                    print(f"Manual load columns: {list(df_test.columns)}")
                except Exception as manual_error:
                    print(f"Manual load also failed: {manual_error}")
            
        else:
            print("❌ latest_results.csv NOT FOUND")
            
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()
    print("=== END DEBUG ===")
    # === END DEBUG SECTION ===
    if df is None:
        st.error("Failed to load data. Please refresh the data first.")
        st.stop()
    
   # Data info section with improved metric cards
    st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2>Market Overview</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Stocks Analyzed", str(df['symbol'].nunique()), "Active Symbols", "🏢")
    
    with col2:
        create_metric_card("Data Points", f"{len(df):,}", "Total Records", "📊")
    
    with col3:
        if 'download_time' in df.columns and not df['download_time'].isna().all():
            try:
                last_update = pd.to_datetime(df['download_time'].iloc[0])
                formatted_time = last_update.strftime("%H:%M")
                create_metric_card("Last Update", formatted_time, "Today", "🕐")
            except:
                create_metric_card("Last Update", "Recent", "Data Fresh", "🕐")
        else:
            create_metric_card("Last Update", "Recent", "Data Fresh", "🕐")
    
    with col4:
        date_range = df['Date'].max() - df['Date'].min()
        create_metric_card("Date Range", f"{date_range.days}", "Days Coverage", "📅")
    
    # Add some spacing after metrics
    st.markdown("<br>", unsafe_allow_html=True)
    

    @st.cache_data
    def get_processed_symbols(_df):
        """Cache symbol processing"""
        return sorted(_df['symbol'].unique())
    
    unique_symbols = get_processed_symbols(df)
    selected_symbols = create_user_friendly_stock_selection(unique_symbols)
    
    # Filter data based on selection
    filtered_df = df[df['symbol'].isin(selected_symbols)] if selected_symbols else df
    
    # Date Range Selection
    if not filtered_df.empty:
        min_date = filtered_df['Date'].min().date()
        max_date = filtered_df['Date'].max().date()
        
        date_range = st.date_input(
            "Select analysis period",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['Date'] >= pd.to_datetime(start_date)) &
                (filtered_df['Date'] <= pd.to_datetime(end_date))
            ]
    
    if filtered_df.empty:
        st.warning("No data available for selected stocks and date range.")
        st.stop()
    
    @st.cache_data
    def calculate_summary_statistics(_filtered_df, selected_symbols_hash, date_hash):
        """Cache expensive summary calculations"""
        return (
            _filtered_df
            .groupby("symbol")
            .agg(
                period_start=("Date", "min"),
                period_end=("Date", "max"),
                period_days=("Date", "count"),
                avg_close=("Close", "mean"),
                avg_daily_return=("daily_return", "mean"),
                total_return=("Close", lambda x: (x.iloc[-1] / x.iloc[0]) - 1 if len(x) > 1 and x.iloc[0] != 0 else np.nan),
                volatility_21=("volatility_21", "mean"),
                avg_rolling_yield_21=("rolling_yield_21", "mean"),
                avg_sharpe_21=("sharpe_21", "mean"),
                avg_max_drawdown_63=("max_drawdown_63", "mean"),
                avg_custom_risk_score=("custom_risk_score", "mean"),
            )
            .reset_index()
        )
    
    # Generate summary statistics with caching
    symbols_hash = hash(str(sorted(selected_symbols))) if selected_symbols else 0
    date_hash = hash(str(date_range)) if 'date_range' in locals() else 0
    summary = calculate_summary_statistics(filtered_df, symbols_hash, date_hash)

    # Portfolio Overview
    if len(selected_symbols) > 1:
        st.markdown('<div class="section-header"><span class="section-icon">💼</span><h2>Portfolio Overview</h2></div>', unsafe_allow_html=True)
        
        # Portfolio metrics with enhanced calculations
        portfolio_return = summary['total_return'].mean()
        portfolio_risk = summary['avg_custom_risk_score'].mean()
        best_performer = summary.loc[summary['total_return'].idxmax(), 'symbol']
        worst_performer = summary.loc[summary['total_return'].idxmin(), 'symbol']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Dynamic return analysis with intelligent indicators
            return_icon = "📈" if portfolio_return > 0 else "📉" if portfolio_return < 0 else "➡️"
            return_magnitude = abs(portfolio_return)
            
            if return_magnitude > 0.2:  # >20% return
                return_descriptor = "Excellent" if portfolio_return > 0 else "Major Loss"
            elif return_magnitude > 0.1:  # >10% return
                return_descriptor = "Strong" if portfolio_return > 0 else "Heavy Loss"
            elif return_magnitude > 0.05:  # >5% return
                return_descriptor = "Good" if portfolio_return > 0 else "Moderate Loss"
            elif return_magnitude > 0:
                return_descriptor = "Modest" if portfolio_return > 0 else "Small Loss"
            else:
                return_descriptor = "Flat"
            
            create_metric_card(
                "Portfolio Return",
                f"{portfolio_return:.2%}",
                return_descriptor,
                return_icon
            )
        
        with col2:
            # Intelligent risk assessment
            if portfolio_risk > 0.15:
                risk_icon = "🔴"
                risk_level = "High Risk"
            elif portfolio_risk > 0.08:
                risk_icon = "🟡"
                risk_level = "Moderate"
            elif portfolio_risk > 0.04:
                risk_icon = "🟢"
                risk_level = "Low Risk"
            else:
                risk_icon = "🟢"
                risk_level = "Very Safe"
                
            create_metric_card(
                "Average Risk Score",
                f"{portfolio_risk:.3f}",
                risk_level,
                risk_icon
            )
        
        with col3:
            # Best performer with shorter context
            best_return = summary.loc[summary['symbol'] == best_performer, 'total_return'].iloc[0]
            
            create_metric_card(
                "Best Performer",
                best_performer,
                f"{best_return:.2%} • Top Pick",
                "🏆"
            )
        
        with col4:
            # Worst performer with shorter context
            worst_return = summary.loc[summary['symbol'] == worst_performer, 'total_return'].iloc[0]
            
            create_metric_card(
                "Worst Performer",
                worst_performer,
                f"{worst_return:.2%} • Review",
                "⚠️"
            )
   # Create portfolio context for individual stock analysis
    portfolio_context = {
        'avg_return': summary['total_return'].mean(),
        'avg_volatility': summary['volatility_21'].mean() if 'volatility_21' in summary.columns else 0,
        'portfolio_size': len(selected_symbols),
        'best_performer': summary.loc[summary['total_return'].idxmax(), 'symbol'] if not summary.empty else None,
        'worst_performer': summary.loc[summary['total_return'].idxmin(), 'symbol'] if not summary.empty else None
    }
            
    # Individual Stock Analysis Section
    st.subheader("🔍 Individual Stock Analysis")
    st.markdown("*Comprehensive analysis for all your selected stocks*")  
    
    # Analyze ALL selected stocks, sorted by return (best first, but show all)
    all_stocks = summary.sort_values('total_return', ascending=False)
    
    for _, row in all_stocks.iterrows():
        # Get comprehensive insights for EVERY stock
        comprehensive_insights = generate_comprehensive_analysis(row['symbol'], row, portfolio_context)
        
        if comprehensive_insights:
            # Add a visual indicator for performance level
            return_pct = row['total_return']
            if return_pct > 0.15:
                performance_indicator = "🚀 Strong Performer"
            elif return_pct > 0.05:
                performance_indicator = "📈 Positive"
            elif return_pct > 0:
                performance_indicator = "📊 Modest Gains"
            elif return_pct > -0.10:
                performance_indicator = "📉 Declining"
            else:
                performance_indicator = "⚠️ Significant Decline"
            
            with st.expander(f"📊 {row['symbol']} - {performance_indicator} ({return_pct:.1%})"):
                for insight in comprehensive_insights:
                    st.markdown(insight)
                    
# Advanced Analytics Section
    st.markdown('<div class="section-header"><span class="section-icon">🧠</span><h2>Advanced Market Intelligence</h2></div>', unsafe_allow_html=True)
    
    if not summary.empty:
        # Market regime analysis
        market_insights = generate_market_regime_insights(summary)
        if market_insights:
            st.subheader("📊 Market Regime Analysis")
            for insight in market_insights:
                st.info(insight)
        
        # Portfolio optimization tips
        portfolio_tips = generate_portfolio_optimization_insights(summary)
        if portfolio_tips:
            st.subheader("🎯 Portfolio Composition Analysis")
            for tip in portfolio_tips:
                st.success(tip)
        
        st.markdown("---")
        
    
    # Interactive Charts Section
    st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2>Interactive Analytics</h2></div>', unsafe_allow_html=True)
    
    # Risk vs Return Scatter Plot
    if not summary.empty:
        fig = create_risk_return_scatter(summary)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance Comparison Chart
    if selected_symbols:
        perf_fig = create_performance_chart(filtered_df, selected_symbols)
        if perf_fig:
            st.plotly_chart(perf_fig, use_container_width=True)
    
    # Metrics Comparison Chart
    if not summary.empty:
        metrics_fig = create_portfolio_metrics_chart(summary)
        st.plotly_chart(metrics_fig, use_container_width=True)
    
    # Correlation Heatmap
    if len(selected_symbols) > 1:
        corr_fig = create_correlation_heatmap(filtered_df, selected_symbols)
        if corr_fig:
            st.plotly_chart(corr_fig, use_container_width=True)
    
    # Data Table Section
    st.markdown('<div class="section-header"><span class="section-icon">📋</span><h2>Detailed Analysis</h2></div>', unsafe_allow_html=True)
    
    # Summary table with better formatting
    if not summary.empty:
        # Format the summary table for better display
        display_summary = summary.copy()
        display_summary['total_return'] = display_summary['total_return'].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
        display_summary['avg_daily_return'] = display_summary['avg_daily_return'].apply(lambda x: f"{x:.4%}" if pd.notna(x) else "N/A")
        display_summary['avg_rolling_yield_21'] = display_summary['avg_rolling_yield_21'].apply(lambda x: f"{x:.4%}" if pd.notna(x) else "N/A")
        display_summary['volatility_21'] = display_summary['volatility_21'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
        display_summary['avg_sharpe_21'] = display_summary['avg_sharpe_21'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        display_summary['avg_custom_risk_score'] = display_summary['avg_custom_risk_score'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
        display_summary['avg_close'] = display_summary['avg_close'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(
            display_summary,
            use_container_width=True,
            column_config={
                "symbol": "Stock",
                "total_return": "Total Return",
                "avg_daily_return": "Avg Daily Return",
                "avg_close": "Avg Price",
                "volatility_21": "Volatility",
                "avg_sharpe_21": "Sharpe Ratio",
                "avg_custom_risk_score": "Risk Score"
            }
        )
    
    # Top performers section
    if not summary.empty and len(summary) > 5:
        st.markdown("### 🏆 Top Performers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🚀 Highest Returns**")
            top_returns = summary.nlargest(5, 'total_return')[['symbol', 'total_return']]
            for _, row in top_returns.iterrows():
                st.markdown(f"• **{row['symbol']}**: {row['total_return']:.2%}")
        
        with col2:
            st.markdown("**⚡ Best Risk-Adjusted Returns**")
            top_sharpe = summary.nlargest(5, 'avg_sharpe_21')[['symbol', 'avg_sharpe_21']]
            for _, row in top_sharpe.iterrows():
                st.markdown(f"• **{row['symbol']}**: {row['avg_sharpe_21']:.2f}")

if __name__ == "__main__":
    main()
