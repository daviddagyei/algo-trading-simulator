# 📈 Trading Strategy Backtest Tool

A comprehensive Streamlit-based application for backtesting multiple trading strategies on financial assets. This tool allows you to test and compare the performance of different algorithmic trading strategies with real market data from Yahoo Finance.

## 🎯 Key Features

### Trading Strategies
- **Trend Following**: Moving average crossover strategy with customizable short and long windows
- **Mean Reversion**: Bollinger Bands-based strategy for range-bound markets
- **Cross-Asset Arbitrage**: Pairs trading strategy for correlated assets

### Asset Support
- **Cryptocurrencies**: Bitcoin, Ethereum, and other digital assets
- **Stocks**: Major US equities (Apple, Microsoft, Google, Amazon, Tesla, etc.)
- **ETFs**: Market indices (SPY, QQQ) and sector ETFs
- **Commodities**: Gold, Oil, and other commodity ETFs
- **Custom Symbols**: Support for any Yahoo Finance ticker

### Advanced Features
- **Interactive Visualizations**: Plotly-powered charts with trading signals
- **Performance Metrics**: Comprehensive analysis including Sharpe ratio, max drawdown, total return
- **Risk Management**: Configurable position sizing and starting capital
- **Buy & Hold Comparison**: Benchmark your strategy against passive investing
- **Multiple Time Intervals**: Daily, hourly, and 5-minute data
- **Transaction Costs**: Realistic trading cost modeling for arbitrage strategies

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Required Python packages (see Installation section)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd finm25000_hw5
   ```

2. **Install required packages**
   ```bash
   pip install streamlit pandas numpy plotly yfinance datetime
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```
   
   Or use the provided script:
   ```bash
   chmod +x run_streamlit.sh
   ./run_streamlit.sh
   ```

4. **Access the app**
   - Open your web browser and navigate to `http://localhost:8501`
   - The application will launch in your default browser automatically

## 📊 How to Use

### 1. Strategy Selection
Choose from three available strategies:
- **Trend Following**: Best for trending markets
- **Mean Reversion**: Best for range-bound markets  
- **Cross-Asset Arbitrage**: For pairs of correlated assets

### 2. Asset Configuration
- **Popular Assets**: Select from pre-configured popular stocks, crypto, and ETFs
- **Custom Symbols**: Enter any valid Yahoo Finance ticker symbol
- **Asset Pairs**: For arbitrage, choose popular pairs or create custom combinations

### 3. Time Period Setup
- Set start and end dates for your backtest
- Choose data interval: Daily (1d), Hourly (1h), or 5-minute (5m)

### 4. Risk Parameters
- **Starting Cash**: Initial capital for the backtest ($1,000 - $1,000,000)
- **Position Size**: Number of shares/units to trade (0.01 - 1,000)

### 5. Strategy Parameters

#### Trend Following
- **Short MA Window**: Fast moving average period (5-50 days)
- **Long MA Window**: Slow moving average period (20-200 days)

#### Mean Reversion
- **Bollinger Window**: Period for Bollinger Bands calculation (10-50 days)
- **Standard Deviations**: Number of std devs for band width (1.0-3.0)

#### Cross-Asset Arbitrage
- **Spread Threshold**: Signal threshold in standard deviations (1.0-3.5)
- **Lookback Window**: Period for spread calculation (10-90 days)
- **Transaction Cost**: Trading fees as percentage (0.0-1.0%)

### 6. Run Backtest
Click the **"🚀 Run Backtest"** button to execute the strategy and view results.

## 📈 Understanding Results

### Performance Metrics
- **Total Return**: Strategy's overall percentage return
- **Sharpe Ratio**: Risk-adjusted return measure
- **Max Drawdown**: Largest peak-to-trough decline
- **Number of Trades**: Total executed trades

### Visualizations
- **Price Charts**: Asset prices with strategy indicators (moving averages, Bollinger Bands)
- **Trading Signals**: Buy/sell signals overlaid on price charts
- **Signal Timeline**: Time series of trading signals
- **Spread Analysis**: For arbitrage strategies, shows price spread and thresholds

### Trade Analysis
- **Trade History**: Complete log of all executed trades
- **Trade Statistics**: Summary of buy/sell trade counts
- **Price Statistics**: Average trade prices and volatility

### Benchmark Comparison
- **Buy & Hold**: Compare strategy performance vs. passive investing
- **Equal Weight**: For arbitrage, compare vs. equal-weighted portfolio

## 🏗️ Project Structure

```
finm25000_hw5/
├── streamlit_app.py          # Main Streamlit application
├── market_data_loader.py     # Yahoo Finance data fetching
├── oms.py                    # Order Management System
├── order_book.py             # Order book simulation
├── order.py                  # Order data structures
├── position_tracker.py       # Position and P&L tracking
├── simulation.ipynb          # Jupyter notebook for analysis
├── run_streamlit.sh          # Launch script
├── run_app.sh               # Alternative launch script
├── strategies/              # Strategy implementations
│   ├── trend_following.py   # Moving average crossover
│   ├── mean_reversion.py    # Bollinger Bands strategy
│   └── arbitrage.py         # Pairs trading strategy
└── README.md               # This file
```

## 🔧 Technical Details

### Data Source
- **Yahoo Finance**: Real-time and historical market data via yfinance
- **Coverage**: Global stocks, ETFs, cryptocurrencies, commodities
- **Intervals**: 1-minute to 1-day granularity

### Strategy Logic

#### Trend Following
- **Buy Signal**: Short MA crosses above Long MA
- **Sell Signal**: Short MA crosses below Long MA
- **Position**: Long only, fully invested when in position

#### Mean Reversion
- **Buy Signal**: Price touches lower Bollinger Band
- **Sell Signal**: Price touches upper Bollinger Band
- **Exit Signal**: Price returns to middle line (SMA)

#### Cross-Asset Arbitrage
- **Long/Short Pairs**: Simultaneously long undervalued and short overvalued asset
- **Spread Calculation**: Price ratio or difference between assets
- **Mean Reversion**: Trade when spread deviates from historical mean

### Performance Calculation
- **Returns**: Calculated from trade-by-trade P&L
- **Sharpe Ratio**: (Return - Risk-free rate) / Volatility
- **Max Drawdown**: Maximum peak-to-trough portfolio value decline
- **Transaction Costs**: Configurable percentage of trade value

## 📋 Examples

### Example 1: Trend Following on Apple Stock
1. Select "Trend Following" strategy
2. Choose "Apple" from popular assets
3. Set date range: Jan 1, 2023 - Dec 31, 2023
4. Configure: Short MA = 10, Long MA = 30
5. Set starting cash: $10,000, position size: 10 shares
6. Run backtest

### Example 2: Mean Reversion on Bitcoin
1. Select "Mean Reversion" strategy
2. Choose "Bitcoin" or enter "BTC-USD"
3. Set parameters: Bollinger window = 20, Std dev = 2.0
4. Use 1-hour data interval for intraday trading
5. Run backtest

### Example 3: Arbitrage between Apple and Microsoft
1. Select "Cross-Asset Arbitrage" strategy
2. Choose "Apple vs Microsoft" pair
3. Set threshold = 2.0, lookback = 30 days
4. Include transaction costs = 0.1%
5. Run backtest

## 🚧 Limitations & Considerations

- **Backtest Bias**: Historical performance doesn't guarantee future results
- **Transaction Costs**: Real trading involves spreads, commissions, and slippage
- **Market Impact**: Large orders can move prices (not modeled)
- **Survivorship Bias**: Analysis only includes currently available assets
- **Look-ahead Bias**: Strategies use only historical data available at each point

## 🛠️ Customization

### Adding New Strategies
1. Create new strategy file in `strategies/` folder
2. Implement `run_backtest(data, params, symbol)` function
3. Return signals, trades, and metrics
4. Import and integrate in `streamlit_app.py`

### Extending Asset Coverage
- Add new asset categories to `popular_assets` dictionary
- Include new asset pairs in `popular_pairs` for arbitrage
- Yahoo Finance supports most global markets

### Custom Indicators
- Modify strategy files to include additional technical indicators
- Update visualization functions to display new indicators
- Add parameter controls in the Streamlit sidebar

## 📞 Support

For questions, issues, or feature requests:
1. Check existing documentation and examples
2. Review error messages for troubleshooting hints
3. Verify Yahoo Finance ticker symbols are correct
4. Ensure date ranges have sufficient data

## 🎓 Educational Use

This tool is designed for educational and research purposes to understand:
- Algorithmic trading strategy development
- Quantitative finance concepts
- Risk management principles
- Performance evaluation metrics
- Market behavior analysis

**Disclaimer**: This tool is for educational purposes only. Do not use for actual trading without proper risk management and regulatory compliance.
