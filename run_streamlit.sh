#!/bin/bash
"""
Run the Streamlit Trading Strategy App
"""

echo "🚀 Starting Trend Following Strategy Backtest App..."
echo "📊 App will be available at: http://localhost:8501"
echo "🔗 Use Ctrl+C to stop the app"
echo "---"

# Activate virtual environment and run streamlit
source .venv/bin/activate
streamlit run streamlit_app.py
