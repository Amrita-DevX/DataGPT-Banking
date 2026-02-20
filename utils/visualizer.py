"""
Visualizer - Creates charts from query results
Automatically selects appropriate chart type based on data
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_visualization(df, question=""):
    """
    Create appropriate visualization for query results
    
    Args:
        df: Pandas DataFrame with query results
        question: Original question (helps determine chart type)
        
    Returns:
        plotly figure or None if visualization not needed
    """
    
    # Don't visualize if too many columns or rows
    if len(df.columns) > 10 or len(df) == 0:
        return None
    
    # If only one row, no need for chart
    if len(df) == 1:
        return None
    
    # Detect chart type based on data structure
    
    # Case 1: Time series data (has date column)
    date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    if date_cols and len(df.columns) >= 2:
        date_col = date_cols[0]
        value_col = [col for col in df.columns if col != date_col][0]
        
        fig = px.line(
            df, 
            x=date_col, 
            y=value_col,
            title=f"{value_col} over time"
        )
        return fig
    
    # Case 2: Two columns - likely category and value (bar chart)
    if len(df.columns) == 2:
        col1, col2 = df.columns
        
        # Determine which is category and which is value
        if pd.api.types.is_numeric_dtype(df[col2]):
            category_col, value_col = col1, col2
        else:
            category_col, value_col = col2, col1
        
        # Bar chart for comparisons
        fig = px.bar(
            df,
            x=category_col,
            y=value_col,
            title=f"{value_col} by {category_col}"
        )
        return fig
    
    # Case 3: Multiple numeric columns (grouped bar)
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 1 and len(df.columns) <= 5:
        # Use first non-numeric column as index
        category_col = [col for col in df.columns if col not in numeric_cols][0] if any(col not in numeric_cols for col in df.columns) else df.columns[0]
        
        fig = px.bar(
            df,
            x=category_col,
            y=list(numeric_cols),
            title="Comparison",
            barmode='group'
        )
        return fig
    
    # Default: No visualization
    return None


def create_summary_metrics(df):
    """
    Create summary metrics cards for numeric data
    
    Args:
        df: Pandas DataFrame
        
    Returns:
        dict: Summary statistics
    """
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    if len(numeric_cols) == 0:
        return None
    
    summary = {}
    for col in numeric_cols:
        summary[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'min': df[col].min(),
            'max': df[col].max(),
            'sum': df[col].sum()
        }
    
    return summary