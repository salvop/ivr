#!/bin/bash

# CollectFlowAPI - Deployment Script
# ==================================
# Author: Salvatore Privitera
# Company: FIDES S.p.A.
# Description: Deployment script for CollectFlowAPI on Linux servers
# Version: 1.0.0
# License: Proprietary - FIDES S.p.A.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log "Docker and Docker Compose are available"
}

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        error ".env file not found. Please create it with your configuration."
        exit 1
    fi
    log ".env file found"
}

# Initialize logs directory
init_logs() {
    log "Initializing logs directory..."
    
    # Get log path from .env or use default
    if [ -f .env ]; then
        LOG_PATH=$(grep "^LOG_PATH=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        if [ -z "$LOG_PATH" ]; then
            LOG_PATH="logs/app.log"
        fi
    else
        LOG_PATH="logs/app.log"
    fi
    
    # Extract directory from LOG_PATH
    LOG_DIR=$(dirname "$LOG_PATH")
    
    if [ "$LOG_DIR" != "." ]; then
        mkdir -p "$LOG_DIR"
        chmod 755 "$LOG_DIR"
        log "Logs directory created: $LOG_DIR"
    fi
    
    # Create log file if it doesn't exist
    touch "$LOG_PATH"
    chmod 644 "$LOG_PATH"
    log "Log file ready: $LOG_PATH"
}

# Stop existing containers
stop_containers() {
    log "Stopping existing containers..."
    docker-compose down --remove-orphans || true
}

# Build and start containers
deploy() {
    log "Building Docker image..."
    docker-compose build --no-cache
    
    log "Starting services..."
    docker-compose up -d
    
    log "Waiting for services to be healthy..."
    sleep 10
    
    # Check health
    if docker-compose ps | grep -q "healthy"; then
        log "Deployment successful! 🎉"
        log "API is available at: http://localhost:8000"
        log "Health check: http://localhost:8000/health"
        log "API docs: http://localhost:8000/docs"
    else
        warn "Service might still be starting up. Check logs with: docker-compose logs -f"
    fi
}

# Show logs
show_logs() {
    log "Showing container logs..."
    docker-compose logs -f
}

# Main deployment
main() {
    log "Starting CollectFlowAPI deployment..."
    
    check_docker
    check_env
    init_logs
    stop_containers
    deploy
    
    log "Deployment completed!"
}

# Parse command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        log "Stopping services..."
        docker-compose down
        ;;
    "restart")
        log "Restarting services..."
        docker-compose restart
        ;;
    "status")
        docker-compose ps
        ;;
    *)
        echo "Usage: $0 {deploy|logs|stop|restart|status}"
        echo "  deploy  - Deploy the application (default)"
        echo "  logs    - Show container logs"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  status  - Show service status"
        exit 1
        ;;
esac
