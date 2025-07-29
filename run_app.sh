#!/bin/bash

# Trading Simulator App Launcher
# Navigate to the project directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Check if all required files exist
if [ ! -f "trading_simulator_app.py" ]; then
    echo "❌ trading_simulator_app.py not found!"
    exit 1
fi

if [ ! -f "market_data_loader.py" ]; then
    echo "❌ market_data_loader.py not found!"
    exit 1
fi

echo "🚀 Starting Trading Simulator App..."
echo "📊 Open your browser to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the app"
echo ""

# Run the Streamlit app
streamlit run trading_simulator_app.py --server.port 8501 --server.address localhost
