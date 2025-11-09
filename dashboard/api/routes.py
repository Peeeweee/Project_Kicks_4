# /dashboard/api/routes.py

from flask import jsonify, current_app, request
from . import bp
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import pandas as pd

# Note: All functions now access the dataframe and color constants
# via `current_app` instead of global variables.

def apply_filters(df):
    """
    Apply filters from request parameters to the dataframe
    Returns filtered dataframe
    """
    filtered_df = df.copy()

    # Get filter parameters from request
    year = request.args.get('year', '')
    quarter = request.args.get('quarter', '')
    region = request.args.get('region', '')
    product = request.args.get('product', '')
    retailer = request.args.get('retailer', '')
    sales_method = request.args.get('sales_method', '')

    # Apply filters if provided
    if year:
        filtered_df = filtered_df[filtered_df['Year'] == int(year)]

    if quarter:
        filtered_df = filtered_df[filtered_df['Quarter'] == int(quarter)]

    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]

    if product:
        filtered_df = filtered_df[filtered_df['Product'] == product]

    if retailer:
        filtered_df = filtered_df[filtered_df['Retailer'] == retailer]

    if sales_method:
        filtered_df = filtered_df[filtered_df['Sales Method'] == sales_method]

    return filtered_df

@bp.route('/sales-trend')
def sales_trend():
    """API endpoint for sales trend over time"""
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    # Group by month
    monthly_sales = df.groupby(df['Invoice Date'].dt.to_period('M')).agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index()
    monthly_sales['Invoice Date'] = monthly_sales['Invoice Date'].dt.to_timestamp()

    fig = go.Figure()

    # Add area fill under the line
    fig.add_trace(go.Scatter(
        x=monthly_sales['Invoice Date'],
        y=monthly_sales['Total Sales'],
        mode='lines+markers',
        name='Total Sales',
        line=dict(color=COLORS['primary'], width=4, shape='spline'),
        marker=dict(
            size=10,
            color=COLORS['primary'],
            line=dict(color='white', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(0, 87, 184, 0.1)',
        hovertemplate='<b>📅 %{x|%B %Y}</b><br>' +
                      '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '📈 Monthly Sales Trend',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Month',
        yaxis_title='Total Sales ($)',
        hovermode='x unified',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        ),
        margin=dict(l=70, r=30, t=80, b=60)
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        showline=True,
        linewidth=2,
        linecolor='#2c3e50'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        showline=True,
        linewidth=2,
        linecolor='#2c3e50',
        tickformat='$,.0f'
    )

    return jsonify(json.loads(fig.to_json()))


@bp.route('/sales-by-region')
def sales_by_region():
    """API endpoint for sales by region"""
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    region_sales = df.groupby('Region').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=False)

    # Unified blue gradient color scheme
    blue_colors = ['#004C8A', '#0057B8', '#1E88E5', '#42A5F5', '#64B5F6']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=region_sales['Region'],
        y=region_sales['Total Sales'],
        name='Total Sales',
        marker=dict(
            color=blue_colors[:len(region_sales)],
            line=dict(color='white', width=2)
        ),
        text=region_sales['Total Sales'],
        texttemplate='$%{text:,.0s}',
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>🌍 %{x}</b><br>' +
                      '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=region_sales['Units Sold']
    ))

    fig.update_layout(
        title={
            'text': '🗺️ Sales by Region',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Region',
        yaxis_title='Total Sales ($)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=70, r=30, t=80, b=60)
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))


@bp.route('/product-performance')
def product_performance():
    """API endpoint for product category performance"""
    df = current_app.df
    CHART_COLORS = current_app.CHART_COLORS

    # Apply filters
    df = apply_filters(df)

    product_sales = df.groupby('Product').agg({
        'Total Sales': 'sum',
        'Units Sold': 'sum',
        'Operating Profit': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=False)

    # Unified blue color scheme
    blue_colors = ['#0057B8', '#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB']

    fig = go.Figure(data=[go.Pie(
        labels=product_sales['Product'],
        values=product_sales['Total Sales'],
        hole=0.5,
        marker=dict(
            colors=blue_colors,
            line=dict(color='white', width=3)
        ),
        textposition='auto',
        textinfo='label+percent',
        textfont=dict(size=11, family='Arial Black'),
        hovertemplate='<b>👟 %{label}</b><br>' +
                      '💰 Sales: <b>$%{value:,.0f}</b><br>' +
                      '📊 Share: <b>%{percent}</b><br>' +
                      '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=product_sales['Units Sold'],
        pull=[0.05, 0, 0, 0, 0, 0]
    )])

    fig.update_layout(
        title={
            'text': '🎯 Sales Distribution by Product Category',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=11, family='Arial')
        ),
        annotations=[dict(
            text=f'<b>${product_sales["Total Sales"].sum():,.0f}</b><br><span style="font-size:12px">Total Sales</span>',
            x=0.5, y=0.5,
            font_size=14,
            font_family='Arial Black',
            font_color='#2c3e50',
            showarrow=False
        )],
        autosize=True,
        margin=dict(l=20, r=150, t=80, b=20)
    )

    return jsonify(json.loads(fig.to_json()))


@bp.route('/retailer-performance')
def retailer_performance():
    """API endpoint for retailer performance"""
    df = current_app.df
    CHART_COLORS = current_app.CHART_COLORS

    # Apply filters
    df = apply_filters(df)

    retailer_sales = df.groupby('Retailer').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=True)  # Ascending for horizontal bars

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=retailer_sales['Retailer'],
        x=retailer_sales['Total Sales'],
        orientation='h',
        marker=dict(
            color=retailer_sales['Total Sales'],
            colorscale='Blues',
            showscale=False,
            line=dict(color='white', width=2)
        ),
        text=retailer_sales['Total Sales'],
        texttemplate='$%{text:,.0s}',
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>🏬 %{y}</b><br>' +
                      '💰 Sales: <b>$%{x:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=retailer_sales['Units Sold']
    ))

    fig.update_layout(
        title={
            'text': '🏪 Sales by Retailer',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Total Sales ($)',
        yaxis_title='',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=120, r=100, t=80, b=60)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')
    fig.update_yaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')

    return jsonify(json.loads(fig.to_json()))


@bp.route('/sales-method')
def sales_method():
    """API endpoint for sales by method"""
    df = current_app.df
    CHART_COLORS = current_app.CHART_COLORS

    # Apply filters
    df = apply_filters(df)

    method_sales = df.groupby('Sales Method').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=False)

    # Unified blue color scheme for channels
    channel_colors = ['#0057B8', '#42A5F5', '#90CAF9']

    # Enhanced donut chart with modern styling
    fig = go.Figure(data=[go.Pie(
        labels=method_sales['Sales Method'],
        values=method_sales['Total Sales'],
        hole=0.4,  # Donut chart
        marker=dict(
            colors=channel_colors,
            line=dict(color='white', width=3)
        ),
        textposition='auto',
        textinfo='label+percent',
        textfont=dict(size=13, family='Arial Black', color='#2c3e50'),
        hovertemplate='<b>🛒 %{label}</b><br>' +
                      '💰 Sales: <b>$%{value:,.0f}</b><br>' +
                      '📊 Share: <b>%{percent}</b><br>' +
                      '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=method_sales['Units Sold']
    )])

    fig.update_layout(
        title={
            'text': '🛍️ Sales by Channel',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12, family='Arial')
        ),
        annotations=[dict(
            text=f'<b>${method_sales["Total Sales"].sum():,.0f}</b><br><span style="font-size:12px">Total Sales</span>',
            x=0.5, y=0.5,
            font_size=14,
            font_family='Arial Black',
            font_color='#2c3e50',
            showarrow=False
        )],
        autosize=True,
        margin=dict(l=20, r=150, t=80, b=20)
    )
    return jsonify(json.loads(fig.to_json()))


@bp.route('/top-states')
def top_states():
    """API endpoint for top performing states"""
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    state_sales = df.groupby('State').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=False).head(10)

    # Enhanced bar chart with gradient colors and text labels
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=state_sales['State'],
        y=state_sales['Total Sales'],
        marker=dict(
            color=state_sales['Total Sales'],
            colorscale='Teal',
            showscale=False,
            line=dict(color='white', width=2)
        ),
        text=state_sales['Total Sales'],
        texttemplate='$%{text:.2s}',
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>📍 %{x}</b><br>' +
                      '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                      '💵 Profit: <b>$%{customdata[0]:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata[1]:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=list(zip(state_sales['Operating Profit'], state_sales['Units Sold']))
    ))

    fig.update_layout(
        title={
            'text': '🗺️ Top 10 States by Sales',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='State',
        yaxis_title='Total Sales ($)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=60, r=40, t=80, b=60)
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))


@bp.route('/margin-analysis')
def margin_analysis():
    """API endpoint for operating margin analysis"""
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    product_margin = df.groupby('Product').agg({
        'Operating Margin': 'mean',
        'Total Sales': 'sum',
        'Operating Profit': 'sum'
    }).reset_index().sort_values('Operating Margin', ascending=True)

    # Enhanced horizontal bar chart with gradient colors
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=product_margin['Product'],
        x=product_margin['Operating Margin'] * 100,
        orientation='h',
        marker=dict(
            color=product_margin['Operating Margin'] * 100,
            colorscale='Greens',
            showscale=False,
            line=dict(color='white', width=2)
        ),
        text=product_margin['Operating Margin'] * 100,
        texttemplate='%{text:.1f}%',
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>👟 %{y}</b><br>' +
                      '📊 Avg Margin: <b>%{x:.1f}%</b><br>' +
                      '💰 Sales: <b>$%{customdata[0]:,.0f}</b><br>' +
                      '💵 Profit: <b>$%{customdata[1]:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=list(zip(product_margin['Total Sales'], product_margin['Operating Profit']))
    ))

    fig.update_layout(
        title={
            'text': '📈 Average Operating Margin by Product',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Operating Margin (%)',
        yaxis_title='',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=120, r=100, t=80, b=60)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')

    return jsonify(json.loads(fig.to_json()))


@bp.route('/quarterly-performance')
def quarterly_performance():
    """API endpoint for quarterly performance"""
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    df['Year_Quarter'] = df['Year'].astype(str) + ' Q' + df['Quarter'].astype(str)
    quarterly = df.groupby('Year_Quarter').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index()

    # Enhanced dual-axis chart with modern styling
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add bars with gradient effect
    fig.add_trace(
        go.Bar(
            x=quarterly['Year_Quarter'],
            y=quarterly['Total Sales'],
            name='💰 Total Sales',
            marker=dict(
                color=quarterly['Total Sales'],
                colorscale='Blues',
                showscale=False,
                line=dict(color='white', width=2)
            ),
            text=quarterly['Total Sales'],
            texttemplate='$%{text:.2s}',
            textposition='outside',
            textfont=dict(size=10, color='#2c3e50', family='Arial Black'),
            hovertemplate='<b>📅 %{x}</b><br>' +
                          '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                          '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                          '<extra></extra>',
            customdata=quarterly['Units Sold']
        ),
        secondary_y=False,
    )

    # Add line with enhanced markers
    fig.add_trace(
        go.Scatter(
            x=quarterly['Year_Quarter'],
            y=quarterly['Operating Profit'],
            name='💵 Operating Profit',
            mode='lines+markers+text',
            line=dict(color='#27ae60', width=4, shape='spline'),
            marker=dict(size=10, color='#27ae60', line=dict(color='white', width=2)),
            text=quarterly['Operating Profit'],
            texttemplate='$%{text:.2s}',
            textposition='top center',
            textfont=dict(size=10, color='#27ae60', family='Arial Black'),
            hovertemplate='<b>📅 %{x}</b><br>' +
                          '💵 Profit: <b>$%{y:,.0f}</b><br>' +
                          '<extra></extra>',
            fill='tozeroy',
            fillcolor='rgba(39, 174, 96, 0.1)'
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title={
            'text': '📊 Quarterly Sales & Profit Performance',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        hovermode='x unified',
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, family='Arial')
        ),
        margin=dict(l=60, r=60, t=100, b=60)
    )
    fig.update_xaxes(title_text='Quarter', showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(title_text='Total Sales ($)', secondary_y=False, showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')
    fig.update_yaxes(title_text='Operating Profit ($)', secondary_y=True, showgrid=False, showline=True, linewidth=2, linecolor='#27ae60', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))


@bp.route('/price-distribution')
def price_distribution():
    """API endpoint for price distribution analysis"""
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    # Enhanced histogram with gradient colors and better styling
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df['Price per Unit'],
        nbinsx=30,
        marker=dict(
            color=df['Price per Unit'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title=dict(text="Price ($)", font=dict(size=13, family='Arial Black')),
                thickness=15,
                len=0.7,
                x=1.02
            ),
            line=dict(color='white', width=1.5)
        ),
        hovertemplate='<b>💵 Price Range: $%{x:.2f}</b><br>' +
                      '📊 Count: <b>%{y}</b><br>' +
                      '<extra></extra>',
        name=''
    ))

    # Calculate statistics for annotation
    mean_price = df['Price per Unit'].mean()
    median_price = df['Price per Unit'].median()

    fig.update_layout(
        title={
            'text': '💲 Distribution of Product Prices',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Price per Unit ($)',
        yaxis_title='Frequency',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=400,
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=60, r=120, t=80, b=60),
        annotations=[
            dict(
                text=f'📊 Mean: ${mean_price:.2f}<br>📍 Median: ${median_price:.2f}',
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                showarrow=False,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#2c3e50',
                borderwidth=2,
                borderpad=8,
                font=dict(size=11, family='Arial', color='#2c3e50'),
                align='left'
            )
        ]
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$.2f')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50')

    return jsonify(json.loads(fig.to_json()))


@bp.route('/summary-stats')
def summary_stats():
    """API endpoint for summary statistics table"""
    df = current_app.df
    stats = {
        'By Product': df.groupby('Product').agg({
            'Total Sales': 'sum', 'Units Sold': 'sum', 'Operating Profit': 'sum', 'Operating Margin': 'mean'
        }).to_dict('index'),
        'By Retailer': df.groupby('Retailer').agg({
            'Total Sales': 'sum', 'Units Sold': 'sum', 'Operating Profit': 'sum', 'Operating Margin': 'mean'
        }).to_dict('index'),
        'By Region': df.groupby('Region').agg({
            'Total Sales': 'sum', 'Units Sold': 'sum', 'Operating Profit': 'sum', 'Operating Margin': 'mean'
        }).to_dict('index'),
    }
    return jsonify(stats)

@bp.route('/sales-by-retailer')
def sales_by_retailer():
    """API endpoint for sales by retailer - Customer Patterns"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    retailer_sales = df.groupby('Retailer').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=True)

    # Green theme for customer patterns
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=retailer_sales['Retailer'],
        x=retailer_sales['Total Sales'],
        orientation='h',
        marker=dict(
            color=retailer_sales['Total Sales'],
            colorscale='Greens',
            showscale=False,
            line=dict(color='white', width=2)
        ),
        text=retailer_sales['Total Sales'],
        texttemplate='$%{text:,.0s}',
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>🏬 %{y}</b><br>' +
                      '💰 Sales: <b>$%{x:,.0f}</b><br>' +
                      '💵 Profit: <b>$%{customdata[0]:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata[1]:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=list(zip(retailer_sales['Operating Profit'], retailer_sales['Units Sold']))
    ))

    fig.update_layout(
        title={
            'text': '🏪 Sales by Retailer',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Total Sales ($)',
        yaxis_title='',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=500,
        hoverlabel=dict(bgcolor="white", font_size=13),
        autosize=True,
        margin=dict(l=120, r=100, t=80, b=60)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')
    fig.update_yaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')

    return jsonify(json.loads(fig.to_json()))

@bp.route('/sales-by-sales-method')
def sales_by_sales_method():
    """API endpoint for sales by sales method - Customer Patterns"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    method_sales = df.groupby('Sales Method').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=False)

    # Green theme donut chart for customer patterns
    green_colors = ['#1B5E20', '#388E3C', '#66BB6A']

    fig = go.Figure(data=[go.Pie(
        labels=method_sales['Sales Method'],
        values=method_sales['Total Sales'],
        hole=0.45,
        marker=dict(
            colors=green_colors,
            line=dict(color='white', width=3)
        ),
        textposition='auto',
        textinfo='label+percent',
        textfont=dict(size=13, family='Arial Black', color='#2c3e50'),
        hovertemplate='<b>🛒 %{label}</b><br>' +
                      '💰 Sales: <b>$%{value:,.0f}</b><br>' +
                      '📊 Share: <b>%{percent}</b><br>' +
                      '💵 Profit: <b>$%{customdata[0]:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata[1]:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=list(zip(method_sales['Operating Profit'], method_sales['Units Sold']))
    )])

    fig.update_layout(
        title={
            'text': '🛍️ Sales by Sales Method',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=500,
        hoverlabel=dict(bgcolor="white", font_size=13),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12, family='Arial')
        ),
        annotations=[dict(
            text=f'<b>${method_sales["Total Sales"].sum():,.0f}</b><br><span style="font-size:12px">Total Sales</span>',
            x=0.5, y=0.5,
            font_size=14,
            font_family='Arial Black',
            font_color='#2c3e50',
            showarrow=False
        )],
        autosize=True,
        margin=dict(l=20, r=150, t=80, b=20)
    )

    return jsonify(json.loads(fig.to_json()))

@bp.route('/sales-by-state')
def sales_by_state():
    df = current_app.df
    COLORS = current_app.COLORS

    # Apply filters
    df = apply_filters(df)

    # State name to abbreviation mapping
    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    state_sales = df.groupby('State').agg({
        'Total Sales': 'sum',
        'Units Sold': 'sum'
    }).reset_index()
    state_sales['State_Code'] = state_sales['State'].map(state_abbrev)

    # Create choropleth map using Graph Objects for better control
    fig = go.Figure(data=go.Choropleth(
        locations=state_sales['State_Code'],
        z=state_sales['Total Sales'],
        locationmode='USA-states',
        colorscale=[
            [0, '#f0f0f0'],
            [0.2, '#cfe2f3'],
            [0.4, '#9fc5e8'],
            [0.6, '#6fa8dc'],
            [0.8, '#3d85c6'],
            [1.0, COLORS['secondary']]
        ],
        colorbar=dict(
            title=dict(text="Total Sales ($)", font=dict(size=13, family='Arial Black')),
            tickformat='$,.0s',
            len=0.7,
            thickness=20
        ),
        text=state_sales['State'],
        customdata=state_sales['Units Sold'],
        hovertemplate='<b>🗺️ %{text}</b><br>' +
                      '💰 Sales: <b>$%{z:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                      '<extra></extra>',
        marker_line_color='white',
        marker_line_width=2
    ))

    fig.update_layout(
        title={
            'text': '🌎 Sales by State Heatmap',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(230, 245, 255)',
            bgcolor='#fafafa'
        ),
        height=600,
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=10, r=10, t=80, b=10)
    )

    return jsonify(json.loads(fig.to_json()))

@bp.route('/sales-by-day-of-week')
def sales_by_day_of_week():
    """API endpoint for sales by day of week - Customer Patterns"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    # Define proper day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day_of_week_sales = df.groupby('Day_of_Week').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index()

    # Sort by day order
    day_of_week_sales['Day_of_Week'] = pd.Categorical(day_of_week_sales['Day_of_Week'], categories=day_order, ordered=True)
    day_of_week_sales = day_of_week_sales.sort_values('Day_of_Week')

    # Green gradient colors for customer patterns
    green_gradient = ['#1B5E20', '#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=day_of_week_sales['Day_of_Week'],
        y=day_of_week_sales['Total Sales'],
        marker=dict(
            color=green_gradient[:len(day_of_week_sales)],
            line=dict(color='white', width=2)
        ),
        text=day_of_week_sales['Total Sales'],
        texttemplate='$%{text:.2s}',
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>📅 %{x}</b><br>' +
                      '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                      '💵 Profit: <b>$%{customdata[0]:,.0f}</b><br>' +
                      '📦 Units: <b>%{customdata[1]:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=list(zip(day_of_week_sales['Operating Profit'], day_of_week_sales['Units Sold']))
    ))

    fig.update_layout(
        title={
            'text': '📅 Sales by Day of the Week',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Day of Week',
        yaxis_title='Total Sales ($)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=500,
        hoverlabel=dict(bgcolor="white", font_size=13),
        autosize=True,
        margin=dict(l=70, r=40, t=80, b=60)
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))

# ============================================================================
# PRODUCT ANALYSIS ENDPOINTS
# ============================================================================

@bp.route('/product-revenue-profit')
def product_revenue_profit():
    """Product revenue and profit comparison - Product Analysis"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    product_data = df.groupby('Product').agg({
        'Total Sales': 'sum',
        'Operating Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Total Sales', ascending=False)

    # Purple/Orange theme for product analysis
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=product_data['Product'],
        y=product_data['Total Sales'],
        name='💰 Total Sales',
        marker=dict(color='#7B1FA2', line=dict(color='white', width=2)),  # Purple
        text=product_data['Total Sales'],
        texttemplate='$%{text:,.0s}',
        textposition='outside',
        textfont=dict(size=10, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>👟 %{x}</b><br>💰 Sales: <b>$%{y:,.0f}</b><br>📦 Units: <b>%{customdata:,.0f}</b><extra></extra>',
        customdata=product_data['Units Sold']
    ))
    fig.add_trace(go.Bar(
        x=product_data['Product'],
        y=product_data['Operating Profit'],
        name='💵 Operating Profit',
        marker=dict(color='#FF6F00', line=dict(color='white', width=2)),  # Orange
        text=product_data['Operating Profit'],
        texttemplate='$%{text:,.0s}',
        textposition='outside',
        textfont=dict(size=10, color='#2c3e50', family='Arial Black'),
        hovertemplate='<b>👟 %{x}</b><br>💵 Profit: <b>$%{y:,.0f}</b><extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '💼 Product Revenue & Profit Comparison',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Product Category',
        yaxis_title='Amount ($)',
        barmode='group',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=12, family='Arial Black')
        ),
        autosize=True,
        margin=dict(l=70, r=30, t=100, b=120)
    )
    fig.update_xaxes(showgrid=False, tickangle=-45, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))

@bp.route('/product-profitability-matrix')
def product_profitability_matrix():
    """Product profitability matrix: Margin vs Volume - Product Analysis"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    product_data = df.groupby('Product').agg({
        'Units Sold': 'sum',
        'Operating Margin': 'mean',
        'Total Sales': 'sum'
    }).reset_index()

    # Create color scale based on sales
    color_scale = product_data['Total Sales'].values

    # Purple colorscale for product analysis
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=product_data['Units Sold'],
        y=product_data['Operating Margin'] * 100,
        mode='markers+text',
        marker=dict(
            size=product_data['Total Sales'] / 4000000,
            color=color_scale,
            colorscale=[[0, '#E1BEE7'], [0.5, '#9C27B0'], [1, '#4A148C']],  # Purple gradient
            showscale=True,
            colorbar=dict(
                title=dict(text="Total<br>Sales ($)", font=dict(size=11, family='Arial Black')),
                tickformat='$,.0s',
                thickness=15,
                len=0.7
            ),
            opacity=0.85,
            line=dict(width=3, color='white')
        ),
        text=product_data['Product'].str.split().str[0],  # Show first word only
        textposition='middle center',
        textfont=dict(size=10, color='white', family='Arial Black'),
        hovertemplate='<b>👟 %{customdata}</b><br>' +
                      '📦 Units Sold: <b>%{x:,.0f}</b><br>' +
                      '📊 Avg Margin: <b>%{y:.1f}%</b><br>' +
                      '💰 Sales: <b>$%{marker.color:,.0f}</b><br>' +
                      '<extra></extra>',
        customdata=product_data['Product']
    ))

    fig.update_layout(
        title={
            'text': '🎯 Product Profitability Matrix<br><sub style="font-size:12px">Bubble size represents Total Sales</sub>',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Total Units Sold',
        yaxis_title='Average Operating Margin (%)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        showlegend=False,
        hoverlabel=dict(bgcolor="white", font_size=13),
        autosize=True,
        margin=dict(l=70, r=120, t=100, b=60)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat=',')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', ticksuffix='%')

    return jsonify(json.loads(fig.to_json()))

@bp.route('/product-by-sales-channel')
def product_by_sales_channel():
    """Product performance by sales channel - Product Analysis"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    channel_product = df.groupby(['Sales Method', 'Product']).agg({
        'Total Sales': 'sum',
        'Units Sold': 'sum'
    }).reset_index()

    # Purple/Orange gradient for products
    purple_orange_colors = ['#7B1FA2', '#9C27B0', '#BA68C8', '#FF6F00', '#FF8F00', '#FFA726']

    fig = go.Figure()

    for i, product in enumerate(sorted(channel_product['Product'].unique())):
        product_data = channel_product[channel_product['Product'] == product]
        fig.add_trace(go.Bar(
            x=product_data['Sales Method'],
            y=product_data['Total Sales'],
            name=product,
            marker=dict(color=purple_orange_colors[i % len(purple_orange_colors)], line=dict(color='white', width=2)),
            text=product_data['Total Sales'],
            texttemplate='$%{text:.2s}',
            textposition='outside',
            textfont=dict(size=9, color='#2c3e50', family='Arial Black'),
            hovertemplate='<b>👟 ' + product + '</b><br>' +
                          '🛒 Channel: <b>%{x}</b><br>' +
                          '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                          '📦 Units: <b>%{customdata:,.0f}</b><br>' +
                          '<extra></extra>',
            customdata=product_data['Units Sold']
        ))

    fig.update_layout(
        title={
            'text': '📊 Product Sales by Channel',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Sales Channel',
        yaxis_title='Total Sales ($)',
        barmode='group',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Arial')
        ),
        autosize=True,
        margin=dict(l=70, r=30, t=80, b=120)
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))

@bp.route('/product-price-distribution')
def product_price_distribution():
    """Product price distribution by category - Product Analysis"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    # Purple/Orange theme for box plots
    purple_orange_colors = ['#7B1FA2', '#9C27B0', '#BA68C8', '#FF6F00', '#FF8F00', '#FFA726']

    fig = go.Figure()

    products = df['Product'].unique()
    for i, product in enumerate(sorted(products)):
        product_df = df[df['Product'] == product]
        fig.add_trace(go.Box(
            y=product_df['Price per Unit'],
            name=product,
            marker=dict(
                color=purple_orange_colors[i % len(purple_orange_colors)],
                line=dict(color='#2c3e50', width=1.5)
            ),
            boxmean='sd',
            line=dict(color=purple_orange_colors[i % len(purple_orange_colors)], width=2),
            hovertemplate='<b>👟 %{fullData.name}</b><br>' +
                          '💵 Price: <b>$%{y:.2f}</b><extra></extra>'
        ))

    fig.update_layout(
        title={
            'text': '💲 Product Price Distribution by Category',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title='Price per Unit ($)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        hoverlabel=dict(bgcolor="white", font_size=13),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Arial')
        ),
        autosize=True,
        margin=dict(l=70, r=30, t=80, b=120)
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$.2f')

    return jsonify(json.loads(fig.to_json()))

@bp.route('/product-sales-trend')
def product_sales_trend():
    """Product sales trend over time - Product Analysis"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    df_copy = df.copy()
    df_copy['Year_Month'] = df_copy['Invoice Date'].dt.to_period('M').dt.to_timestamp()
    product_trend = df_copy.groupby(['Year_Month', 'Product']).agg({
        'Total Sales': 'sum'
    }).reset_index()

    # Purple/Orange theme for lines
    purple_orange_colors = ['#7B1FA2', '#9C27B0', '#BA68C8', '#FF6F00', '#FF8F00', '#FFA726']

    fig = go.Figure()

    # Add a line for each product
    for i, product in enumerate(sorted(product_trend['Product'].unique())):
        product_data = product_trend[product_trend['Product'] == product]
        fig.add_trace(go.Scatter(
            x=product_data['Year_Month'],
            y=product_data['Total Sales'],
            name=product,
            mode='lines+markers',
            line=dict(width=3, color=purple_orange_colors[i % len(purple_orange_colors)], shape='spline'),
            marker=dict(size=8, color=purple_orange_colors[i % len(purple_orange_colors)], line=dict(width=2, color='white')),
            hovertemplate='<b>👟 ' + product + '</b><br>' +
                          '📅 %{x|%b %Y}<br>' +
                          '💰 Sales: <b>$%{y:,.0f}</b><br>' +
                          '<extra></extra>'
        ))

    fig.update_layout(
        title={
            'text': '📈 Product Sales Trend Over Time',
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Month',
        yaxis_title='Total Sales ($)',
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        hovermode='x unified',
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Arial')
        ),
        autosize=True,
        margin=dict(l=70, r=30, t=80, b=120)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=True, linewidth=2, linecolor='#2c3e50', tickformat='$,.0f')

    return jsonify(json.loads(fig.to_json()))

@bp.route('/product-regional-mix')
def product_regional_mix():
    """Product category mix by region"""
    df = current_app.df

    # Apply filters
    df = apply_filters(df)

    region_product = df.groupby(['Region', 'Product']).agg({
        'Total Sales': 'sum'
    }).reset_index()

    # Purple/Orange color palette for products
    purple_orange_colors = ['#7B1FA2', '#9C27B0', '#BA68C8', '#FF6F00', '#FF8F00', '#FFA726']

    # Get unique products to assign colors
    products = region_product['Product'].unique()

    fig = go.Figure()

    for i, product in enumerate(products):
        product_data = region_product[region_product['Product'] == product]

        fig.add_trace(go.Bar(
            x=product_data['Region'],
            y=product_data['Total Sales'],
            name=f'👟 {product}',
            marker=dict(
                color=purple_orange_colors[i % len(purple_orange_colors)],
                line=dict(color='white', width=2)
            ),
            text=[f'${val:,.0f}' for val in product_data['Total Sales']],
            textposition='inside',
            textfont=dict(color='white', size=11, family='Arial Black'),
            hovertemplate='<b>🌍 %{x}</b><br>' +
                         f'<b>👟 {product}</b><br>' +
                         '💰 Sales: $%{y:,.0f}<br>' +
                         '<extra></extra>'
        ))

    fig.update_layout(
        title=dict(
            text='<b>🗺️ Product Mix by Region</b>',
            font=dict(size=20, family='Arial Black', color='#4A148C'),
            x=0.5,
            xanchor='center'
        ),
        barmode='stack',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        autosize=True,
        height=500,
        xaxis=dict(
            title=dict(text='<b>🌍 Region</b>', font=dict(size=14, color='#4A148C')),
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='#E0E0E0'
        ),
        yaxis=dict(
            title=dict(text='<b>💰 Total Sales ($)</b>', font=dict(size=14, color='#4A148C')),
            showgrid=True,
            gridwidth=1,
            gridcolor='#F0F0F0',
            showline=True,
            linewidth=2,
            linecolor='#E0E0E0'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            font=dict(size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E0E0E0',
            borderwidth=1
        ),
        margin=dict(l=60, r=40, t=80, b=100),
        hovermode='closest'
    )

    return jsonify(json.loads(fig.to_json()))
