# Basis-Image mit Python
FROM python:3.9-slim

# Installiere Chrome und Abhängigkeiten für Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# Anforderungen kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Den restlichen Code kopieren
COPY . .

# Startbefehl für die Streamlit-App
CMD ["streamlit", "run", "main.py", "--server.port=8501"]