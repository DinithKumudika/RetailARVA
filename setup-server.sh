#!/bin/bash

# Exit on any error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting server setup script...${NC}"

# Step 2: Install Docker Compose
echo -e "${GREEN}Installing Docker Compose...${NC}"
sudo apt update -y
sudo apt install -y docker-compose || { echo -e "${RED}Failed to install docker-compose${NC}"; exit 1; }

# Step 3: Ensure Docker is Running
echo -e "${GREEN}Checking Docker service...${NC}"
if sudo systemctl is-active docker >/dev/null 2>&1; then
    echo "Docker is already running."
else
    echo "Starting Docker..."
    sudo systemctl start docker || { echo -e "${RED}Failed to start Docker${NC}"; exit 1; }
    sudo systemctl enable docker || { echo -e "${RED}Failed to enable Docker${NC}"; exit 1; }
fi

# Step 4: Verify and Fix User Permissions
echo -e "${GREEN}Checking user permissions for Docker...${NC}"
CURRENT_USER=$(whoami)
if groups "$CURRENT_USER" | grep -q docker; then
    echo "User $CURRENT_USER is already in the docker group."
else
    echo "Adding $CURRENT_USER to docker group..."
    sudo usermod -aG docker "$CURRENT_USER" || { echo -e "${RED}Failed to add user to docker group${NC}"; exit 1; }
    echo -e "${GREEN}User added to docker group. You may need to log out and back in for this to take effect.${NC}"
fi

# Step 5: Fix Docker Socket Permissions
echo -e "${GREEN}Fixing Docker socket permissions...${NC}"
sudo chown root:docker /var/run/docker.sock || { echo -e "${RED}Failed to chown docker.sock${NC}"; exit 1; }
sudo chmod 660 /var/run/docker.sock || { echo -e "${RED}Failed to chmod docker.sock${NC}"; exit 1; }

# Step 6: Run Docker Compose
echo -e "${GREEN}Starting Docker Compose...${NC}"
docker-compose -f docker-compose-w-ollama.yaml up -d --build || { echo -e "${RED}Failed to run docker-compose${NC}"; exit 1; }

# Step 7: Open Firewall Ports
echo -e "${GREEN}Configuring firewall (ufw)...${NC}"
if ! sudo ufw status >/dev/null 2>&1; then
    echo "ufw is not installed or not enabled. Installing and enabling..."
    sudo apt install -y ufw
    sudo ufw enable
fi

sudo ufw allow 5000/tcp || { echo -e "${RED}Failed to open port 5000${NC}"; exit 1; }
sudo ufw allow 11434/tcp || { echo -e "${RED}Failed to open port 11434${NC}"; exit 1; }
echo -e "${GREEN}Firewall rules updated:${NC}"
sudo ufw status

# Final Message
echo -e "${GREEN}Server setup completed successfully!${NC}"
echo "If Docker permissions don’t work yet, log out and log back in, then verify with 'docker ps'."