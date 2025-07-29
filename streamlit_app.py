#!/usr/bin/env python3
"""
Streamlit App for Trend Following Strategy Backtesting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from market_data_loader import MarketDataLoader
from strategies.trend_following import run_backtest as tf_run_backtest
from strategies.mean_reversion import run_backtest as mr_run_backtest
from strategies.arbitrage import run_backtest as arb_run_backtest


def main():
    """Main Streamlit app"""
    
    st.set_page_config(
        page_title="Trading Strategy Backtest Tool",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Trading Strategy Backtest Tool")
    st.markdown("---")
    
    # Sidebar for parameters
    st.sidebar.header("🔧 Strategy Parameters")
    
    # Strategy selection
    st.sidebar.subheader("🎯 Strategy Selection")
    
    strategy_type = st.sidebar.selectbox(
        "Choose Strategy:",
        ["Trend Following", "Mean Reversion", "Cross-Asset Arbitrage"],
        index=0
    )
    
    # Asset selection
    st.sidebar.subheader("📊 Asset Selection")
    
    # Popular assets
    popular_assets = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Google": "GOOGL",
        "Amazon": "AMZN",
        "Tesla": "TSLA",
        "S&P 500 ETF": "SPY",
        "NASDAQ ETF": "QQQ",
        "Gold": "GLD",
        "Oil": "USO"
    }
    
    # Popular asset pairs for arbitrage
    popular_pairs = {
        "Apple vs Microsoft": ("AAPL", "MSFT"),
        "Google vs Microsoft": ("GOOGL", "MSFT"),
        "Apple vs Google": ("AAPL", "GOOGL"),
        "Amazon vs Microsoft": ("AMZN", "MSFT"),
        "Tesla vs Apple": ("TSLA", "AAPL"),
        "SPY vs QQQ": ("SPY", "QQQ"),
        "Bitcoin vs Ethereum": ("BTC-USD", "ETH-USD")
    }
    
    if strategy_type == "Cross-Asset Arbitrage":
        # Asset pair selection for arbitrage
        pair_input_method = st.sidebar.radio(
            "Choose asset pair input method:",
            ["Popular Pairs", "Custom Symbols"]
        )
        
        if pair_input_method == "Popular Pairs":
            pair_name = st.sidebar.selectbox(
                "Select an asset pair:",
                list(popular_pairs.keys()),
                index=0
            )
            symbol1, symbol2 = popular_pairs[pair_name]
            asset_name = pair_name
        else:
            col1, col2 = st.sidebar.columns(2)
            with col1:
                symbol1 = st.sidebar.text_input(
                    "First Asset (e.g., AAPL):",
                    value="AAPL"
                ).upper()
            with col2:
                symbol2 = st.sidebar.text_input(
                    "Second Asset (e.g., MSFT):",
                    value="MSFT"
                ).upper()
            asset_name = f"{symbol1} vs {symbol2}"
    else:
        # Single asset selection for other strategies
        input_method = st.sidebar.radio(
            "Choose asset input method:",
            ["Popular Assets", "Custom Symbol"]
        )
        
        if input_method == "Popular Assets":
            asset_name = st.sidebar.selectbox(
                "Select an asset:",
                list(popular_assets.keys()),
                index=0
            )
            symbol = popular_assets[asset_name]
        else:
            symbol = st.sidebar.text_input(
                "Enter symbol (e.g., AAPL, BTC-USD):",
                value="AAPL"
            ).upper()
            asset_name = symbol
    
    # Date range
    st.sidebar.subheader("📅 Date Range")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365*2),
            max_value=datetime.now()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # Risk parameters (moved before strategy parameters)
    st.sidebar.subheader("💰 Risk Parameters")
    
    starting_cash = st.sidebar.number_input(
        "Starting Cash ($)",
        min_value=1000,
        max_value=1000000,
        value=100000,
        step=10000
    )
    
    position_size = st.sidebar.number_input(
        "Position Size (shares/units)",
        min_value=0.01,
        max_value=1000.0,
        value=1.0,
        step=0.1,
        format="%.2f"
    )
    
    # Strategy parameters
    st.sidebar.subheader("⚙️ Strategy Parameters")
    
    if strategy_type == "Trend Following":
        short_win = st.sidebar.slider(
            "Short MA Window (days)",
            min_value=5,
            max_value=50,
            value=20,
            step=5
        )
        
        long_win = st.sidebar.slider(
            "Long MA Window (days)",
            min_value=20,
            max_value=200,
            value=50,
            step=10
        )
        
        # Strategy parameters
        params = {
            'starting_cash': starting_cash,
            'position_size': position_size,
            'short_win': short_win,
            'long_win': long_win
        }
        
    elif strategy_type == "Mean Reversion":
        bollinger_win = st.sidebar.slider(
            "Bollinger Bands Window (days)",
            min_value=10,
            max_value=50,
            value=20,
            step=5
        )
        
        num_std = st.sidebar.slider(
            "Standard Deviations",
            min_value=1.0,
            max_value=3.0,
            value=2.0,
            step=0.5
        )
        
        # Strategy parameters
        params = {
            'starting_cash': starting_cash,
            'position_size': position_size,
            'bollinger_win': bollinger_win,
            'num_std': num_std
        }
        
    else:  # Cross-Asset Arbitrage
        threshold = st.sidebar.slider(
            "Spread Threshold (std deviations)",
            min_value=1.0,
            max_value=3.5,
            value=2.0,
            step=0.5
        )
        
        lookback_window = st.sidebar.slider(
            "Lookback Window (days)",
            min_value=10,
            max_value=90,
            value=30,
            step=5
        )
        
        transaction_cost = st.sidebar.slider(
            "Transaction Cost (%)",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01,
            format="%.2f"
        ) / 100
        
        # Strategy parameters
        params = {
            'starting_cash': starting_cash,
            'position_size': position_size,
            'threshold': threshold,
            'lookback_window': lookback_window,
            'transaction_cost': transaction_cost
        }
    
    # Data interval
    st.sidebar.subheader("📊 Data Settings")
    interval = st.sidebar.selectbox(
        "Data Interval",
        ["1d", "1h", "5m"],
        index=0
    )
    
    # Run backtest button
    run_backtest_btn = st.sidebar.button(
        "🚀 Run Backtest",
        type="primary",
        use_container_width=True
    )
    
    # Main content area
    if run_backtest_btn:
        # Validation based on strategy type
        if strategy_type == "Trend Following":
            if short_win >= long_win:
                st.error("❌ Short MA window must be less than Long MA window!")
                return
        elif strategy_type == "Cross-Asset Arbitrage":
            if symbol1 == symbol2:
                st.error("❌ Assets must be different for arbitrage strategy!")
                return
        
        if start_date >= end_date:
            st.error("❌ Start date must be before end date!")
            return
        
        # Show loading spinner
        with st.spinner(f"📡 Loading {asset_name} data and running {strategy_type} backtest..."):
            try:
                # Load data
                loader = MarketDataLoader(interval=interval, period="max")
                
                if strategy_type == "Cross-Asset Arbitrage":
                    # Load data for both assets
                    data1 = loader.get_history(
                        symbol1, 
                        start=start_date.strftime("%Y-%m-%d"),
                        end=end_date.strftime("%Y-%m-%d")
                    )
                    
                    data2 = loader.get_history(
                        symbol2, 
                        start=start_date.strftime("%Y-%m-%d"),
                        end=end_date.strftime("%Y-%m-%d")
                    )
                    
                    if data1.empty or data2.empty:
                        st.error(f"❌ No data found for one or both symbols ({symbol1}, {symbol2}). Please check the symbols and try again.")
                        return
                    
                    # Prepare data for both assets
                    data1_reset = data1.reset_index()
                    data2_reset = data2.reset_index()
                    data1_reset = data1_reset.rename(columns={'Date': 'timestamp'})
                    data2_reset = data2_reset.rename(columns={'Date': 'timestamp'})
                    
                    # Flatten multi-level columns if needed
                    if isinstance(data1_reset.columns, pd.MultiIndex):
                        data1_reset.columns = [col[0] if col[0] else 'timestamp' for col in data1_reset.columns]
                    if isinstance(data2_reset.columns, pd.MultiIndex):
                        data2_reset.columns = [col[0] if col[0] else 'timestamp' for col in data2_reset.columns]
                    
                    # Create history DataFrames
                    data1_history = pd.DataFrame({
                        'timestamp': data1_reset['timestamp'],
                        'last_price': data1_reset['last_price']
                    })
                    
                    data2_history = pd.DataFrame({
                        'timestamp': data2_reset['timestamp'],
                        'last_price': data2_reset['last_price']
                    })
                    
                else:
                    # Single asset data loading
                    data = loader.get_history(
                        symbol, 
                        start=start_date.strftime("%Y-%m-%d"),
                        end=end_date.strftime("%Y-%m-%d")
                    )
                    
                    if data.empty:
                        st.error(f"❌ No data found for symbol {symbol}. Please check the symbol and try again.")
                        return
                    
                    # Prepare data
                    data_reset = data.reset_index()
                    data_reset = data_reset.rename(columns={'Date': 'timestamp'})
                
                    # Flatten multi-level columns if needed
                    if isinstance(data_reset.columns, pd.MultiIndex):
                        data_reset.columns = [col[0] if col[0] else 'timestamp' for col in data_reset.columns]
                
                # Run backtest based on strategy type
                if strategy_type == "Trend Following":
                    signals, trades, metrics = tf_run_backtest(data_reset, params, symbol)
                    display_results(data_reset, signals, trades, metrics, symbol, asset_name, params, strategy_type)
                elif strategy_type == "Mean Reversion":
                    signals, trades, metrics = mr_run_backtest(data_reset, params, symbol)
                    display_results(data_reset, signals, trades, metrics, symbol, asset_name, params, strategy_type)
                else:  # Cross-Asset Arbitrage
                    signals, trades, metrics = arb_run_backtest(data1_history, data2_history, params, symbol1, symbol2)
                    display_arbitrage_results(data1_history, data2_history, signals, trades, metrics, symbol1, symbol2, asset_name, params)
                
            except Exception as e:
                st.error(f"❌ Error during backtesting: {str(e)}")
                st.exception(e)
    
    else:
        # Show instructions
        st.markdown("""
        ## Welcome to the Trading Strategy Backtest Tool! 🎯
        
        This tool allows you to backtest multiple trading strategies on any asset available on Yahoo Finance.
        
        ### Available Strategies:
        1. **Trend Following**: Moving average crossover strategy
        2. **Mean Reversion**: Bollinger Bands mean reversion strategy
        3. **Cross-Asset Arbitrage**: Pairs trading strategy for correlated assets
        
        ### How to use:
        1. **Select a strategy** from the sidebar
        2. **Select an asset** (popular assets or custom symbol)
        3. **Set the date range** for your backtest
        4. **Configure strategy parameters**:
           - **Trend Following**: Short/Long MA windows, position size, starting cash
           - **Mean Reversion**: Bollinger window, std deviations, position size, starting cash
        5. **Click "Run Backtest"** to see results
        
        ### Strategy Logic:
        
        **Trend Following:**
        - **Buy Signal**: When short MA crosses above long MA
        - **Sell Signal**: When short MA crosses below long MA
        
        **Mean Reversion:**
        - **Buy Signal**: When price crosses below lower Bollinger Band
        - **Sell Signal**: When price crosses above upper Bollinger Band
        - **Exit Signal**: When price returns to middle line
        
        ### Tips:
        - **Trend Following**: Works best in trending markets
        - **Mean Reversion**: Works best in range-bound markets
        - Try different parameter combinations for optimization
        - Compare strategy performance vs. buy-and-hold
        """)
        
        # Show sample assets
        st.subheader("📊 Popular Assets Available")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Cryptocurrencies**")
            st.markdown("- BTC-USD (Bitcoin)")
            st.markdown("- ETH-USD (Ethereum)")
            st.markdown("- ADA-USD (Cardano)")
            
        with col2:
            st.markdown("**Stocks**")
            st.markdown("- AAPL (Apple)")
            st.markdown("- MSFT (Microsoft)")
            st.markdown("- GOOGL (Google)")
            st.markdown("- TSLA (Tesla)")
            
        with col3:
            st.markdown("**ETFs & Commodities**")
            st.markdown("- SPY (S&P 500)")
            st.markdown("- QQQ (NASDAQ)")
            st.markdown("- GLD (Gold)")
            st.markdown("- USO (Oil)")


def display_results(data, signals, trades, metrics, symbol, asset_name, params, strategy_type):
    """Display backtest results"""
    
    # Key metrics at the top
    st.subheader(f"📊 Results for {asset_name} ({symbol})")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Return",
            f"{metrics['total_return']:.2%}",
            delta=f"{metrics['total_return']:.2%}"
        )
    
    with col2:
        st.metric(
            "Sharpe Ratio",
            f"{metrics['sharpe_ratio']:.2f}",
            delta=f"{metrics['sharpe_ratio']:.2f}"
        )
    
    with col3:
        st.metric(
            "Max Drawdown",
            f"{metrics['max_drawdown']:.2%}",
            delta=f"{metrics['max_drawdown']:.2%}"
        )
    
    with col4:
        st.metric(
            "Number of Trades",
            metrics['num_trades'],
            delta=metrics['num_trades']
        )
    
    # Detailed metrics
    st.subheader("📈 Detailed Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Strategy Performance:**")
        st.write(f"- Starting Cash: ${params['starting_cash']:,.2f}")
        st.write(f"- Final Value: ${metrics['final_cash']:,.2f}")
        st.write(f"- Total P&L: ${metrics['final_cash'] - params['starting_cash']:,.2f}")
        st.write(f"- Position Size: {params['position_size']} units")
    
    with col2:
        # Buy and hold comparison
        if len(data) > 0:
            buy_hold_return = (data['last_price'].iloc[-1] - data['last_price'].iloc[0]) / data['last_price'].iloc[0]
            buy_hold_final = params['starting_cash'] * (1 + buy_hold_return)
            
            st.write("**Buy & Hold Comparison:**")
            st.write(f"- Buy & Hold Return: {buy_hold_return:.2%}")
            st.write(f"- Buy & Hold Final: ${buy_hold_final:,.2f}")
            st.write(f"- Strategy vs B&H: {metrics['total_return'] - buy_hold_return:.2%}")
    
    # Price chart with signals
    st.subheader(f"📈 Price Chart with {strategy_type} Signals")
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'Price and {strategy_type} Indicators', 'Trading Signals'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Price
    fig.add_trace(
        go.Scatter(
            x=signals['timestamp'],
            y=signals['last_price'],
            name='Price',
            line=dict(color='black', width=1)
        ),
        row=1, col=1
    )
    
    if strategy_type == "Trend Following":
        # Moving averages
        fig.add_trace(
            go.Scatter(
                x=signals['timestamp'],
                y=signals['ma_short'],
                name=f'MA{params["short_win"]}',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=signals['timestamp'],
                y=signals['ma_long'],
                name=f'MA{params["long_win"]}',
                line=dict(color='red', width=1)
            ),
            row=1, col=1
        )
    
    else:  # Mean Reversion
        # Bollinger Bands
        fig.add_trace(
            go.Scatter(
                x=signals['timestamp'],
                y=signals['upper'],
                name='Upper Band',
                line=dict(color='red', width=1, dash='dash'),
                showlegend=True
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=signals['timestamp'],
                y=signals['lower'],
                name='Lower Band',
                line=dict(color='green', width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(0,100,80,0.1)',
                showlegend=True
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=signals['timestamp'],
                y=signals['mid'],
                name='Middle Line',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
    
    # Buy/Sell signals
    buy_signals = signals[signals['signal'] == 1]
    sell_signals = signals[signals['signal'] == -1]
    
    if not buy_signals.empty:
        fig.add_trace(
            go.Scatter(
                x=buy_signals['timestamp'],
                y=buy_signals['last_price'],
                mode='markers',
                name='Buy Signal',
                marker=dict(color='green', size=10, symbol='triangle-up')
            ),
            row=1, col=1
        )
    
    if not sell_signals.empty:
        fig.add_trace(
            go.Scatter(
                x=sell_signals['timestamp'],
                y=sell_signals['last_price'],
                mode='markers',
                name='Sell Signal',
                marker=dict(color='red', size=10, symbol='triangle-down')
            ),
            row=1, col=1
        )
    
    # Signal line chart
    fig.add_trace(
        go.Scatter(
            x=signals['timestamp'],
            y=signals['signal'],
            name='Signal',
            line=dict(color='purple', width=2),
            fill='tonexty'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title=f"{asset_name} ({symbol}) - {strategy_type} Strategy",
        height=700,
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Signal", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trade history
    if trades:
        st.subheader("📋 Trade History")
        
        trades_df = pd.DataFrame(trades)
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df['price'] = trades_df['price'].round(2)
        
        # Display trade table
        st.dataframe(
            trades_df[['timestamp', 'side', 'quantity', 'price', 'signal']],
            use_container_width=True
        )
        
        # Trade statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Trade Statistics:**")
            buy_trades = len(trades_df[trades_df['side'] == 'buy'])
            sell_trades = len(trades_df[trades_df['side'] == 'sell'])
            st.write(f"- Total Trades: {len(trades_df)}")
            st.write(f"- Buy Trades: {buy_trades}")
            st.write(f"- Sell Trades: {sell_trades}")
        
        with col2:
            if len(trades_df) > 1:
                avg_price = trades_df['price'].mean()
                price_std = trades_df['price'].std()
                st.write("**Price Statistics:**")
                st.write(f"- Average Price: ${avg_price:.2f}")
                st.write(f"- Price Std Dev: ${price_std:.2f}")
    else:
        st.info("ℹ️ No trades were generated with the current parameters.")


def display_arbitrage_results(data1, data2, signals, trades, metrics, symbol1, symbol2, asset_name, params):
    """Display arbitrage backtest results"""
    
    # Key metrics at the top
    st.subheader(f"📊 Arbitrage Results for {asset_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Return",
            f"{metrics['total_return']:.2%}",
            delta=f"{metrics['total_return']:.2%}"
        )
    
    with col2:
        st.metric(
            "Sharpe Ratio",
            f"{metrics['sharpe_ratio']:.2f}",
            delta=f"{metrics['sharpe_ratio']:.2f}"
        )
    
    with col3:
        st.metric(
            "Max Drawdown",
            f"{metrics['max_drawdown']:.2%}",
            delta=f"{metrics['max_drawdown']:.2%}"
        )
    
    with col4:
        st.metric(
            "Pairs Traded",
            metrics['num_pairs_traded'],
            delta=metrics['num_pairs_traded']
        )
    
    # Detailed metrics
    st.subheader("📈 Detailed Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Strategy Performance:**")
        st.write(f"- Starting Cash: ${params['starting_cash']:,.2f}")
        st.write(f"- Final Value: ${metrics['final_cash']:,.2f}")
        st.write(f"- Total P&L: ${metrics['final_cash'] - params['starting_cash']:,.2f}")
        st.write(f"- Transaction Costs: ${metrics['transaction_costs']:,.2f}")
        st.write(f"- Position Size: {params['position_size']} shares each")
        st.write(f"- Total Trades: {metrics['num_trades']} ({metrics['num_pairs_traded']} pairs)")
    
    with col2:
        # Individual asset returns comparison
        if len(data1) > 0 and len(data2) > 0:
            asset1_return = (data1['last_price'].iloc[-1] - data1['last_price'].iloc[0]) / data1['last_price'].iloc[0]
            asset2_return = (data2['last_price'].iloc[-1] - data2['last_price'].iloc[0]) / data2['last_price'].iloc[0]
            equal_weight_return = (asset1_return + asset2_return) / 2
            equal_weight_final = params['starting_cash'] * (1 + equal_weight_return)
            
            st.write("**Buy & Hold Comparison:**")
            st.write(f"- {symbol1} Return: {asset1_return:.2%}")
            st.write(f"- {symbol2} Return: {asset2_return:.2%}")
            st.write(f"- Equal Weight Return: {equal_weight_return:.2%}")
            st.write(f"- Equal Weight Final: ${equal_weight_final:,.2f}")
            st.write(f"- Strategy vs Equal Weight: {metrics['total_return'] - equal_weight_return:.2%}")
    
    # Price chart with spread
    st.subheader(f"📈 Asset Prices and Spread Analysis")
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(f'{symbol1} vs {symbol2} Prices', 'Price Spread', 'Trading Signals'),
        vertical_spacing=0.1,
        row_heights=[0.4, 0.3, 0.3]
    )
    
    # Normalize prices for better comparison
    data1_norm = data1['last_price'] / data1['last_price'].iloc[0] * 100
    data2_norm = data2['last_price'] / data2['last_price'].iloc[0] * 100
    
    # Asset prices (normalized)
    fig.add_trace(
        go.Scatter(
            x=data1['timestamp'],
            y=data1_norm,
            name=f'{symbol1} (normalized)',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data2['timestamp'],
            y=data2_norm,
            name=f'{symbol2} (normalized)',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )
    
    # Price spread
    if 'spread' in signals.columns:
        fig.add_trace(
            go.Scatter(
                x=signals['timestamp'],
                y=signals['spread'],
                name='Price Spread',
                line=dict(color='purple', width=2)
            ),
            row=2, col=1
        )
        
        # Add spread thresholds if available
        if 'upper_threshold' in signals.columns:
            fig.add_trace(
                go.Scatter(
                    x=signals['timestamp'],
                    y=signals['upper_threshold'],
                    name='Upper Threshold',
                    line=dict(color='red', width=1, dash='dash')
                ),
                row=2, col=1
            )
            
        if 'lower_threshold' in signals.columns:
            fig.add_trace(
                go.Scatter(
                    x=signals['timestamp'],
                    y=signals['lower_threshold'],
                    name='Lower Threshold',
                    line=dict(color='green', width=1, dash='dash')
                ),
                row=2, col=1
            )
    
    # Trading signals
    fig.add_trace(
        go.Scatter(
            x=signals['timestamp'],
            y=signals['signal'],
            name='Signal',
            line=dict(color='orange', width=2),
            fill='tonexty'
        ),
        row=3, col=1
    )
    
    fig.update_layout(
        title=f"{asset_name} - Cross-Asset Arbitrage Strategy",
        height=800,
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Normalized Price", row=1, col=1)
    fig.update_yaxes(title_text="Spread", row=2, col=1)
    fig.update_yaxes(title_text="Signal", row=3, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategy parameters summary
    st.subheader("⚙️ Strategy Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Arbitrage Settings:**")
        st.write(f"- Threshold: {params['threshold']} std deviations")
        st.write(f"- Lookback Window: {params['lookback_window']} days")
        st.write(f"- Transaction Cost: {params['transaction_cost']:.1%}")
    
    with col2:
        if 'hedge_ratio' in signals.columns:
            avg_hedge_ratio = signals['hedge_ratio'].mean()
            hedge_ratio_std = signals['hedge_ratio'].std()
            st.write("**Hedge Ratio Statistics:**")
            st.write(f"- Average Hedge Ratio: {avg_hedge_ratio:.2f}")
            st.write(f"- Hedge Ratio Std Dev: {hedge_ratio_std:.2f}")
    
    # Trade history
    if trades:
        st.subheader("📋 Trade History")
        
        trades_df = pd.DataFrame(trades)
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df['price'] = trades_df['price'].round(2)
        
        # Group trades by pair
        pair_trades = []
        for i in range(0, len(trades_df), 2):
            if i + 1 < len(trades_df):
                trade1 = trades_df.iloc[i]
                trade2 = trades_df.iloc[i + 1]
                pair_trades.append({
                    'timestamp': trade1['timestamp'],
                    'asset1_side': trade1['side'],
                    'asset1_symbol': trade1['symbol'],
                    'asset1_price': trade1['price'],
                    'asset2_side': trade2['side'],
                    'asset2_symbol': trade2['symbol'],
                    'asset2_price': trade2['price'],
                    'signal': trade1['signal']
                })
        
        if pair_trades:
            pairs_df = pd.DataFrame(pair_trades)
            st.write("**Pair Trades:**")
            st.dataframe(
                pairs_df[['timestamp', 'asset1_side', 'asset1_symbol', 'asset1_price', 
                         'asset2_side', 'asset2_symbol', 'asset2_price', 'signal']],
                use_container_width=True
            )
        
        # Trade statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Trade Statistics:**")
            asset1_trades = len(trades_df[trades_df['symbol'] == symbol1])
            asset2_trades = len(trades_df[trades_df['symbol'] == symbol2])
            st.write(f"- Total Individual Trades: {len(trades_df)}")
            st.write(f"- {symbol1} Trades: {asset1_trades}")
            st.write(f"- {symbol2} Trades: {asset2_trades}")
            st.write(f"- Pairs Traded: {metrics['num_pairs_traded']}")
        
        with col2:
            if len(trades_df) > 1:
                avg_price = trades_df['price'].mean()
                price_std = trades_df['price'].std()
                st.write("**Price Statistics:**")
                st.write(f"- Average Trade Price: ${avg_price:.2f}")
                st.write(f"- Price Std Dev: ${price_std:.2f}")
    else:
        st.info("ℹ️ No trades were generated with the current parameters. Try adjusting the threshold or lookback window.")


if __name__ == "__main__":
    main()
