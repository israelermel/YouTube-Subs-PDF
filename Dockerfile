FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    gnupg && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip \
    https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set environment variables
ENV PATH="/usr/local/bin/chromedriver:${PATH}"

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by Flask
EXPOSE 5000

# Set Flask app environment variable
ENV FLASK_APP=app.py

# Copy the rest of the application code
COPY . /app/

# Command to run the Flask application
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]