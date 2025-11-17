#!/bin/bash

# CollectFlowAPI - Initialize Logs Directory
# =========================================
# Author: Salvatore Privitera
# Company: FIDES S.p.A.
# Description: Script to initialize logs directory structure
# Version: 1.0.0
# License: Proprietary - FIDES S.p.A.

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Set default values
LOG_PATH=${LOG_PATH:-"logs/app.log"}
LOG_LEVEL=${LOG_LEVEL:-"INFO"}

# Extract directory from LOG_PATH
LOG_DIR=$(dirname "$LOG_PATH")

# Create logs directory if it doesn't exist
if [ "$LOG_DIR" != "." ]; then
    mkdir -p "$LOG_DIR"
    chmod 755 "$LOG_DIR"
    echo "📁 Directory creata: $LOG_DIR"
fi

# Create initial log file if it doesn't exist
touch "$LOG_PATH"
chmod 644 "$LOG_PATH"

# Create .gitkeep to preserve empty directory in git
if [ "$LOG_DIR" != "." ]; then
    touch "$LOG_DIR/.gitkeep"
fi

echo "✅ Directory logs inizializzata con successo!"
echo "📁 Path: $(pwd)/$LOG_PATH"
echo "📝 File di log: $LOG_PATH"
echo "🔊 Livello log: $LOG_LEVEL"
echo "🔒 Permessi impostati correttamente"
