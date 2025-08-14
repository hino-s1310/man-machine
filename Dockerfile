# Python 3.11 slimイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ChromeとChromeDriverのインストール
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriverのインストール
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}') \
    && wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" -O CHROME_DRIVER_VERSION \
    && wget -q "https://chromedriver.storage.googleapis.com/$(cat CHROME_DRIVER_VERSION)/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip CHROME_DRIVER_VERSION

# FirefoxとGeckoDriverのインストール
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# GeckoDriverのインストール
RUN wget -q "https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.33.0-linux64.tar.gz" \
    && tar -xzf geckodriver-v0.33.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.33.0-linux64.tar.gz

# Python依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 必要なディレクトリを作成
RUN mkdir -p reports/data/xml reports/data/report reports/data/log reports/data/zip

# ポートを公開
EXPOSE 8501

# 環境変数を設定
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# ヘルスチェック用のスクリプトを作成
RUN echo '#!/bin/bash\ncurl -f http://localhost:8501/_stcore/health || exit 1' > /healthcheck.sh \
    && chmod +x /healthcheck.sh

# ヘルスチェックを設定
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /healthcheck.sh

# Streamlitアプリケーションを起動
CMD ["streamlit", "run", "reports/Execution.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
