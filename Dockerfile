# Sử dụng Python 3.10 slim làm base image
FROM python:3.10-slim

# Đặt working directory trong container
WORKDIR /app

# Sao chép file requirements.txt trước để tận dụng Docker layer caching
COPY catty-reminders-app/requirements.txt .

# Cài đặt dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ code ứng dụng vào container
COPY catty-reminders-app/ .

# Tạo thư mục cho database nếu cần
RUN mkdir -p /app/data

# Expose port 8181 (port mà ứng dụng chạy)
EXPOSE 8181

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check để kiểm tra container có healthy không
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8181')" || exit 1

# Command để chạy ứng dụng
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8181"]

