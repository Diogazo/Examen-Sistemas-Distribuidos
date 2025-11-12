FROM python:3.11-slim
WORKDIR /app
COPY storage_system.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "storage_system.py"]
