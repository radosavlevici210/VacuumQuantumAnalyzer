#!/bin/bash
# Production startup script for Scientific Calculator

echo "Starting Scientific Calculator in production mode..."

# Set production environment variables
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=5000
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Start the application
streamlit run app.py \
    --server.headless true \
    --server.port 5000 \
    --server.address 0.0.0.0 \
    --browser.gatherUsageStats false \
    --logger.level error \
    --client.showErrorDetails false
