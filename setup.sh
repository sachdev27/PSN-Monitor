#!/bin/bash

# Define virtual environment and service name
VENV_DIR="venv"
SERVICE_NAME="psn_monitor"

# Define Python executable
PYTHON_EXEC=python3

# Step 1: Check if virtual environment exists, create if not
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment already exists. Skipping creation."
else
    echo "🚀 Creating virtual environment..."
    $PYTHON_EXEC -m venv $VENV_DIR
    echo "✅ Virtual environment created successfully."
fi

# Step 2: Activate the virtual environment
echo "🔄 Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 3: Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install --upgrade pip  # Upgrade pip first
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully."
else
    echo "⚠️ No requirements.txt found. Skipping dependency installation."
fi

# Step 4: Create a Systemd service file // ( Optional )
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

if [ -f "$SERVICE_FILE" ]; then
    echo "✅ Service file already exists. Skipping creation."
else
    echo "🚀 Creating systemd service file..."
    sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=PSN Monitoring Service
After=network.target

[Service]
ExecStart=$(pwd)/venv/bin/python $(pwd)/main.py
WorkingDirectory=$(pwd)
Restart=always
User=$USER
Environment=PATH=$(pwd)/venv/bin

[Install]
WantedBy=multi-user.target
EOF
    echo "✅ Service file created successfully: $SERVICE_FILE"
fi

# Step 5: Reload systemd, enable and start the service
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "🚀 Enabling and starting the service..."
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "✅ Service started successfully! Run 'sudo systemctl status $SERVICE_NAME' to check the status."
