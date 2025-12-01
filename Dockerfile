# Use Python 3.10 on Debian (Stable & Compatible with Selenium)
FROM python:3.10-slim

# 1. Install System Dependencies & Google Chrome
# We need wget/gnupg to download Chrome, and unzip/curl for other tools.
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 2. Set Working Directory
WORKDIR /app

# 3. Install Python Dependencies
# We copy requirements first to leverage Docker cache
COPY requirements.txt .
# Add pysqlite3-binary because standard Linux sqlite3 is often too old for ChromaDB
RUN pip install --no-cache-dir -r requirements.txt pysqlite3-binary

# 4. Copy Application Code
COPY . .

# 5. Make the start script executable
RUN chmod +x start.sh

# 6. Expose Ports (8000 for Backend, 8501 for Frontend)
EXPOSE 8000 8501

# 7. Run the Master Script
CMD ["./start.sh"]