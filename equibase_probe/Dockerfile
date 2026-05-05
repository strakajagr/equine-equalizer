FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcairo2 libcups2 libdbus-1-3 libdrm2 libgbm1 libglib2.0-0 \
    libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 \
    libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxext6 \
    libxfixes3 libxi6 libxrandr2 libxrender1 libxshmfence1 libxss1 libxtst6 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    playwright==1.42.0 \
    playwright-stealth==2.0.0 \
    && playwright install chromium

WORKDIR /app
COPY probe.py /app/

CMD ["python", "/app/probe.py"]
