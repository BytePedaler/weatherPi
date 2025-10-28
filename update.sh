#!/bin/bash
# This script checks for updates from GitHub and restarts the service if new code is found.

# Automatically detect the user's home directory
USER_HOME=$(eval echo "~$USER")
CODE_DIR="$USER_HOME/weatherPi/code"

# Navigate to the code directory
cd "$CODE_DIR" || exit

# Fetch latest changes
git fetch origin main >/dev/null 2>&1

# Compare current commit with remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): Update detected. Pulling latest changes..." >> "$USER_HOME/weatherPi/update.log"
    git reset --hard origin/main >> "$USER_HOME/weatherPi/update.log" 2>&1

    # Restart the running service to apply the update
    sudo systemctl restart weatherpi.service
    echo "$(date): Service restarted after update." >> "$USER_HOME/weatherPi/update.log"
else
    echo "$(date): No updates found." >> "$USER_HOME/weatherPi/update.log"
fi
