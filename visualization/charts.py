"""
Chart Creation Module
Interactive visualizations using Plotly for stock and portfolio analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config.settings import (
    CHART_HEIGHT,
    PERFORMANCE_CHART_HEIGHT,
    CORRELATION_HEATMAP_HEIGHT,
    CHART_COLOR_SCHEME,
    DEFAULT_CHART_COLORS,
    CHART_BACKGROUND_COLOR,
    CHART_PAPER_BACKGROUND,
    CHART_FONT_FAMILY,
    CHART_FONT_SIZE,
    CHART_TITLE_FONT_SIZE
)


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
        color_continuous_scale=CHART_COLOR_SCHEME
    )
    
    fig.update_layout(
        title_font_size=16,
        height=CHART_HEIGHT,
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
            'font': {'size': CHART_TITLE_FONT_SIZE, 'family': CHART_FONT_FAMILY}
        },
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_BACKGROUND_COLOR,
        paper_bgcolor=CHART_PAPER_BACKGROUND,
        height=PERFORMANCE_CHART_HEIGHT,
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
    
    colors = DEFAULT_CHART_COLORS
    
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
            'font': {'size': CHART_TITLE_FONT_SIZE, 'family': CHART_FONT_FAMILY}
        },
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        plot_bgcolor=CHART_BACKGROUND_COLOR,
        paper_bgcolor=CHART_PAPER_BACKGROUND,
        height=PERFORMANCE_CHART_HEIGHT
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
            'font': {'size': CHART_TITLE_FONT_SIZE, 'family': CHART_FONT_FAMILY}
        },
        font=dict(family=CHART_FONT_FAMILY, size=CHART_FONT_SIZE),
        height=CORRELATION_HEATMAP_HEIGHT
    )
    
    return fig
