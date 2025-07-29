# Trading Strategy Backtest Tool

A comprehensive Streamlit-based application for backtesting multiple trading strategies on financial assets. This tool allows you to test and compare the performance of different algorithmic trading strategies with real market data from Yahoo Finance.

## Key Features

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

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Required Python packages (see Installation section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/daviddagyei/algo-trading-simulator.git
   cd algo-trading-simulator
   ```

2. **Set up Python environment (recommended)**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On Linux/Mac:
   source .venv/bin/activate
   # On Windows:
   # .venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   # Core dependencies for the application
   pip install streamlit pandas numpy plotly yfinance pytz
   
   # Optional: For development and testing
   pip install pytest jupyter
   
   # Or install from requirements file:
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import streamlit, pandas, numpy, plotly, yfinance; print('All dependencies installed successfully!')"
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

### Streamlit Cloud Deployment

To deploy this app on Streamlit Cloud:

1. **Fork/Clone this repository** to your GitHub account

2. **Visit [share.streamlit.io](https://share.streamlit.io)**

3. **Connect your GitHub account** and select this repository

4. **Set the main file path** to `streamlit_app.py`

5. **Deploy** - Streamlit Cloud will automatically install dependencies from `requirements.txt`

The app will be available at: `https://your-username-algo-trading-simulator-streamlit-app-xxxxxx.streamlit.app`

## How to Use

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
Click the **"Run Backtest"** button to execute the strategy and view results.

## Understanding Results

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

## Project Structure & Dependencies

```
/
├── streamlit_app.py          # Main Streamlit application
├── market_data_loader.py     # Yahoo Finance data fetching
├── oms.py                    # Order Management System
├── order_book.py             # Order book simulation
├── order.py                  # Order data structures
├── position_tracker.py       # Position and P&L tracking
├── simulation.ipynb          # Jupyter notebook for analysis
├── run_streamlit.sh          # Launch script
├── run_app.sh               # Alternative launch script
├── .gitignore               # Git ignore file for Python projects
├── LICENSE                  # MIT License
├── strategies/              # Strategy implementations
│   ├── trend_following.py   # Moving average crossover
│   ├── mean_reversion.py    # Bollinger Bands strategy
│   └── arbitrage.py         # Pairs trading strategy
└── README.md               # This file
```

### Core Dependencies & Components

The application is built on several interconnected modules that work together to provide a complete trading simulation environment:

#### Market Data Layer
- **`market_data_loader.py`**: Core data fetching module
  - Integrates with Yahoo Finance API via `yfinance` library
  - Supports multiple asset classes (stocks, crypto, ETFs, commodities)
  - Handles different time intervals (1d, 1h, 5m)
  - Includes data caching and timezone management
  - Provides clean OHLCV data formatting for strategies

#### Trading Infrastructure
- **`order.py`**: Order data structure
  - Defines the `Order` dataclass with fields: id, symbol, side, quantity, type, price, timestamp
  - Supports market, limit, and stop order types
  - Handles order validation and formatting

- **`oms.py`**: Order Management System
  - Validates incoming orders (side, quantity, type, price requirements)
  - Tracks order status and lifecycle
  - Routes orders to matching engines
  - Provides order acceptance/rejection logic

- **`order_book.py`**: Order book simulation
  - Simulates realistic order matching
  - Manages bid/ask spreads
  - Handles market impact and slippage modeling
  - Provides liquidity simulation for backtesting

- **`position_tracker.py`**: Portfolio & P&L tracking
  - Maintains real-time position tracking per symbol
  - Calculates cash balances and trade settlements
  - Records complete trade blotter/history
  - Computes unrealized and realized P&L
  - Provides portfolio-level risk metrics

#### Strategy Engine
- **`strategies/trend_following.py`**: Moving average crossover strategy
  - Implements short/long MA calculation
  - Generates buy/sell signals on crossovers
  - Handles position sizing and risk management

- **`strategies/mean_reversion.py`**: Bollinger Bands strategy
  - Calculates dynamic support/resistance levels
  - Mean reversion signal generation
  - Bollinger Band parameter optimization

- **`strategies/arbitrage.py`**: Pairs trading strategy
  - Correlation analysis between asset pairs
  - Spread calculation and normalization
  - Long/short position management
  - Transaction cost modeling

#### User Interface
- **`streamlit_app.py`**: Main web application
  - Interactive parameter configuration
  - Real-time visualization with Plotly
  - Strategy comparison and benchmarking
  - Results analysis and export

### Python Dependencies

The application requires the following Python packages:

```bash
# Core data and computation
pandas>=1.3.0          # Data manipulation and analysis
numpy>=1.21.0          # Numerical computing
yfinance>=0.1.87       # Yahoo Finance API access

# Web application framework
streamlit>=1.25.0      # Interactive web app framework

# Data visualization
plotly>=5.15.0         # Interactive charts and graphs

# Date/time handling
datetime               # Built-in Python module
pytz                   # Timezone handling

# Development and testing (optional)
pytest>=7.0.0          # Unit testing framework
jupyter>=1.0.0         # Notebook support
```

### Data Flow Architecture

1. **Data Ingestion**: `market_data_loader.py` fetches historical price data
2. **Strategy Execution**: Strategy modules process data and generate signals
3. **Order Generation**: Trading signals create `Order` objects
4. **Order Processing**: `oms.py` validates and manages order lifecycle
5. **Trade Execution**: `order_book.py` simulates realistic order matching
6. **Position Management**: `position_tracker.py` updates portfolios and P&L
7. **Visualization**: `streamlit_app.py` displays results and analytics

### Testing Infrastructure

The project includes comprehensive testing files (in `__pycache__/` when run):
- `test_market_data_loader_pytest.py`: Data fetching and validation tests
- `test_order_and_oms.py`: Order management system tests
- `test_order_book_sanity.py`: Order book simulation tests
- `test_position_tracker.py`: Portfolio tracking tests
- `test_strategies.py`: Strategy logic and performance tests
- `test_integration.py`: End-to-end system tests

### Execution Scripts

- **`run_streamlit.sh`**: Main application launcher
  ```bash
  #!/bin/bash
  streamlit run streamlit_app.py --server.port 8501
  ```

- **`run_app.sh`**: Alternative launcher with additional options
  ```bash
  #!/bin/bash
  python -m streamlit run streamlit_app.py
  ```

## Technical Details

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

## Limitations & Considerations

- **Backtest Bias**: Historical performance doesn't guarantee future results
- **Transaction Costs**: Real trading involves spreads, commissions, and slippage
- **Market Impact**: Large orders can move prices (not modeled)
- **Survivorship Bias**: Analysis only includes currently available assets
- **Look-ahead Bias**: Strategies use only historical data available at each point

## Customization

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

## Support & Troubleshooting

### Common Issues & Solutions

#### Installation Issues
- **ImportError**: Ensure all dependencies are installed in the correct Python environment
- **Version Conflicts**: Use virtual environments to isolate package versions
- **yfinance Connection**: Check internet connection and Yahoo Finance availability

#### Runtime Issues
- **Data Loading Errors**: Verify ticker symbols are valid on Yahoo Finance
- **Empty DataFrames**: Check date ranges have sufficient market data
- **Performance Issues**: Use smaller date ranges or daily intervals for initial testing

#### Streamlit Issues
- **Port Already in Use**: Change port with `streamlit run streamlit_app.py --server.port 8502`
- **Browser Not Opening**: Manually navigate to `http://localhost:8501`
- **Caching Issues**: Clear Streamlit cache with Ctrl+C, then restart

### Getting Help
For questions, issues, or feature requests:
1. Check existing documentation and examples
2. Review error messages for troubleshooting hints
3. Verify Yahoo Finance ticker symbols are correct
4. Ensure date ranges have sufficient data
5. Check that all dependencies are properly installed

## Educational Use

This tool is designed for educational and research purposes to understand:
- Algorithmic trading strategy development
- Quantitative finance concepts
- Risk management principles
- Performance evaluation metrics
- Market behavior analysis

**Disclaimer**: This tool is for educational purposes only. Do not use for actual trading without proper risk management and regulatory compliance.
