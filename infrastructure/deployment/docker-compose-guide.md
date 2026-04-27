# Docker Compose Guide

How to run the Crucible data pipeline in a container. Docker eliminates "works on my machine" issues, isolates Python dependencies, and makes it easy to run the pipeline on a server without a desktop environment.

**When to use this**: If you're running the pipeline on a Linux server, want to avoid polluting your local Python environment, or want a clean way to manage the schedule with container restart policies.

**When to skip this**: If you're running locally on macOS and already have the conda environment working, cron is simpler.

---

## Project Structure

```
crucible-cio-team/
├── .env                          # API keys — never committed
├── .gitignore                    # Must include .env
├── context/                      # Written by pipeline, read by agents
├── scripts/
│   └── update-context.py
└── infrastructure/
    └── deployment/
        ├── docker-compose-guide.md   # This file
        ├── Dockerfile.pipeline       # Pipeline container image
        └── entrypoint.sh             # Container startup script
```

---

## Dockerfile.pipeline

Create at `infrastructure/deployment/Dockerfile.pipeline`:

```dockerfile
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY infrastructure/deployment/requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copy project files (context dir volume-mounted at runtime)
COPY scripts/ ./scripts/
COPY orchestrator/ ./orchestrator/

# Entrypoint
COPY infrastructure/deployment/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

---

## requirements-docker.txt

Create at `infrastructure/deployment/requirements-docker.txt`:

```
requests==2.32.3
pandas==2.2.3
python-dotenv==1.0.1
ib_insync==0.9.86
kalshi-python==1.0.2
schedule==1.2.2
```

Note: `norgatedata` is not included — it requires the NDU desktop application which cannot run in a container. The Norgate section of the pipeline will gracefully skip and log a warning when running in Docker.

---

## entrypoint.sh

Create at `infrastructure/deployment/entrypoint.sh`:

```bash
#!/bin/bash
set -e

echo "[Crucible] Container started at $(date -u)"
echo "[Crucible] Running pipeline immediately on startup..."

python scripts/update-context.py

echo "[Crucible] Entering scheduled loop (6:30 AM Mon-Fri)..."
python - <<'PYEOF'
import schedule
import time
from datetime import datetime

def run_pipeline():
    import subprocess
    day = datetime.now().weekday()  # 0=Mon, 6=Sun
    if day < 5:  # weekdays only
        print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}] Running pipeline...")
        result = subprocess.run(
            ["python", "scripts/update-context.py"],
            capture_output=False
        )
        if result.returncode != 0:
            print(f"[ERROR] Pipeline exited with code {result.returncode}")

schedule.every().day.at("06:30").do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(30)
PYEOF
```

---

## docker-compose.yml

Place at the project root:

```yaml
version: "3.9"

services:
  pipeline:
    build:
      context: .
      dockerfile: infrastructure/deployment/Dockerfile.pipeline
    container_name: crucible-pipeline
    restart: unless-stopped

    # Load API keys from .env — never bake them into the image
    env_file:
      - .env

    # Mount the context directory so the host can read what the container writes
    volumes:
      - ./context:/app/context

    # IBKR: connect to host's TWS/Gateway
    # On Linux, use host.docker.internal or the host's actual LAN IP
    # On macOS Docker Desktop, host.docker.internal resolves automatically
    extra_hosts:
      - "host.docker.internal:host-gateway"

    # Override IBKR host to reach the host machine
    environment:
      - IBKR_HOST=host.docker.internal
      - IBKR_PORT=7497
      - IBKR_CLIENT_ID=20

    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## .env Template

```bash
# FRED
FRED_API_KEY=your_fred_key_here

# Kalshi
KALSHI_API_KEY=your_kalshi_key_here
KALSHI_EMAIL=your_email@example.com
KALSHI_PASSWORD=your_password_here

# IBKR (overridden by docker-compose environment section for Docker)
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=10
```

---

## .gitignore Entries

Add these to `.gitignore` — they should already be there, but verify:

```gitignore
# Credentials — never commit
.env
.env.local
.env.*

# Norgate data directory (if on host)
norgate_data/

# Pipeline logs
*.log
/tmp/

# Python
__pycache__/
*.pyc
*.pyo
.venv/
```

---

## Building and Running

### Build the image

```bash
docker compose build pipeline
```

### Start the pipeline service

```bash
docker compose up -d pipeline
```

This starts the container in the background. On startup, it runs the pipeline once immediately, then enters the scheduled loop.

### Verify it started

```bash
docker compose ps
# pipeline   running   (healthy)

docker compose logs pipeline
# Should show the initial pipeline run
```

### Check context files were written

```bash
ls -la context/
cat context/macro-state.md | head -20
```

### Run the pipeline manually (on demand)

```bash
docker compose exec pipeline python scripts/update-context.py
```

### Stop the service

```bash
docker compose stop pipeline
```

### Full rebuild (after dependency changes)

```bash
docker compose down pipeline
docker compose build --no-cache pipeline
docker compose up -d pipeline
```

---

## Checking Logs When Something Fails

### View recent logs

```bash
docker compose logs --tail=100 pipeline
```

### Follow logs in real time

```bash
docker compose logs -f pipeline
```

### Enter the container for debugging

```bash
docker compose exec pipeline bash
# Inside container:
python scripts/update-context.py
python -c "import requests; print(requests.__version__)"
env | grep FRED  # Verify env vars are set
```

### Check IBKR connectivity from inside the container

```bash
docker compose exec pipeline bash -c "python -c \"
from ib_insync import IB
ib = IB()
ib.connect('host.docker.internal', 7497, clientId=99, timeout=5)
print('Connected:', ib.isConnected())
ib.disconnect()
\""
```

---

## Common Issues

### Context files not updated

Check that the volume mount is correct:
```bash
docker inspect crucible-pipeline | grep -A5 Mounts
# Should show: /local/path/context -> /app/context
```

### IBKR connection refused from container

1. Confirm TWS/Gateway is running on the host
2. Confirm IBKR API is enabled for the host's IP
3. On Linux, `host.docker.internal` requires Docker 20.10+. For older Docker:
   ```bash
   IBKR_HOST=$(ip route | awk '/default/ {print $3}')
   ```
4. Add the host IP to IBKR's trusted IP list in API settings

### Environment variables not loaded

Verify `.env` is in the same directory as `docker-compose.yml` and that `env_file: .env` is present in the service definition. Check with:
```bash
docker compose exec pipeline env | grep FRED
```

### Package version conflicts

Pin versions in `requirements-docker.txt`. Use `pip freeze` from your working local environment to generate the pinned list:
```bash
conda activate crucible
pip freeze | grep -E "requests|pandas|ib_insync|kalshi|schedule|dotenv"
```
