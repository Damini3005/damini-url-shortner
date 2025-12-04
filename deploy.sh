#!/bin/bash

# Directory where your repository lives
REPO_DIR="/home/damini/damini-url-shortner" 

# Move into the repository directory
cd "$REPO_DIR" || { echo "Repo directory not found"; exit 1; }

echo "Stopping existing Uvicorn server..."
pkill -f "uvicorn src.main:app" 2>/dev/null
sleep 2

echo "Pulling latest changes..."
git pull origin develop || { echo "Git pull failed"; exit 1; }
echo "Done!"

echo "Present working directory:"
pwd

echo "Listing files:"
ls

# Move to app directory
cd app || { echo "App directory not found"; exit 1; }

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed successfully."

# Create logs directory
mkdir -p start_logs

# Log file with timestamp
TIMESTAMP=$(TZ='Asia/Kolkata' date +"%Y-%m-%d_%H-%M")
LOGFILE="start_logs/uvicorn_$TIMESTAMP.log"

# Start Uvicorn in background with logs
echo "Starting Uvicorn server..."
nohup uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload > "$LOGFILE" 2>&1 &

echo "Uvicorn started successfully!"
echo "Logs are available at: $LOGFILE"
