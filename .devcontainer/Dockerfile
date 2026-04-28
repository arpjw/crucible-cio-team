FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    git \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/crucible-cio-team

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
