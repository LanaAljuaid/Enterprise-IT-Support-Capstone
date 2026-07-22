FROM python:3.11-slim
 
# Keep Python output unbuffered so logs/print statements show up immediately
ENV PYTHONUNBUFFERED=1
 
WORKDIR /app
 
# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the rest of the project
COPY . .
 
# Runs the pipeline defined in main.py
CMD ["python", "main.py"]