#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

# Try running docker compose
if docker-compose version &>/dev/null; then
    docker-compose --env-file .env.dev up
elif docker compose version &>/dev/null; then
    docker compose --env-file .env.dev up
else
    echo -e "${RED}Error :${NC} You should have Docker and Docker Compose installed on your machine to run this script."
    echo -e "\tManual installation procedure: https://github.com/Phloemus/ABRomics-KG?tab=readme-ov-file#without-docker"
    exit 1
fi
