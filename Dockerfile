# 1. Use an official, lightweight Python Linux image as the foundation
FROM python:3.11-slim

# 2. Tell the container where we will be working inside of it
WORKDIR /app

# 3. Copy only the requirements file first (This caches the installation step to save time on future builds)
COPY requirements.txt .

# 4. Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application scripts into the container
COPY scraper.py .
COPY main.py .

# 6. Define the exact command the container runs when it wakes up
CMD ["python", "main.py"]