"""
Visualization Package for BullBoard Application
Chart creation and data visualization components
"""

from .charts import (
    create_risk_return_scatter,
    create_performance_chart,
    create_portfolio_metrics_chart,
    create_correlation_heatmap
)

__version__ = "1.0.0"

__all__ = [
    'create_risk_return_scatter',
    'create_performance_chart',
    'create_portfolio_metrics_chart',
    'create_correlation_heatmap'
]
