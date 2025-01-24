FROM ubuntu:22.04

#Update packages and install dependencies
RUN apt-get update && apt-get --no-install-recommends --no-install-suggests -y install \
    python3.10 \
    build-essential \
    libpq-dev \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    python3-wheel \
    wget \
    gnupg \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Copy all files for dir /app
COPY . /app
WORKDIR /app

#Install chrome from local file
RUN apt-get update && apt-get install -y ./src/chrome/google-chrome-stable_114.0.5735.198-1_amd64.deb

RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python3 main.py