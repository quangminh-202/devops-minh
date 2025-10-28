# 🐋 Hướng dẫn sử dụng Docker cho Catty Reminders App

## Yêu cầu
- Docker Engine (phiên bản 20.10 trở lên)
- Docker Compose (phiên bản 2.0 trở lên)

## Cài đặt Docker
Nếu chưa cài Docker, chạy lệnh sau:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Sau đó log out và log in lại.

## Các lệnh Docker cơ bản

### 1. Build Docker Image
```bash
# Build image với tag 'catty-reminders'
docker build -t catty-reminders:latest .

# Build với no-cache (rebuild từ đầu)
docker build --no-cache -t catty-reminders:latest .
```

### 2. Chạy Container bằng Docker Run
```bash
# Chạy container ở chế độ detached (-d)
docker run -d \
  -p 8181:8181 \
  --name catty-app \
  -v $(pwd)/catty-reminders-app:/app \
  catty-reminders:latest

# Chạy container ở chế độ interactive (xem logs ngay)
docker run -it -p 8181:8181 --name catty-app catty-reminders:latest
```

### 3. Sử dụng Docker Compose (Khuyên dùng)
```bash
# Start ứng dụng (build nếu cần)
docker-compose up

# Start ở background mode
docker-compose up -d

# Build lại và start
docker-compose up --build

# Stop ứng dụng
docker-compose down

# Stop và xóa volumes
docker-compose down -v
```

## Các lệnh quản lý Container

### Xem danh sách containers
```bash
# Xem containers đang chạy
docker ps

# Xem tất cả containers (cả đã stop)
docker ps -a
```

### Xem logs
```bash
# Xem logs của container
docker logs catty-reminders

# Xem logs real-time (follow)
docker logs -f catty-reminders

# Xem 100 dòng log cuối
docker logs --tail 100 catty-reminders

# Docker Compose logs
docker-compose logs -f
```

### Truy cập vào container
```bash
# Exec vào container (bash shell)
docker exec -it catty-reminders bash

# Hoặc dùng sh nếu bash không có
docker exec -it catty-reminders sh

# Chạy lệnh trong container
docker exec catty-reminders python --version
```

### Stop và Start containers
```bash
# Stop container
docker stop catty-reminders

# Start container đã stop
docker start catty-reminders

# Restart container
docker restart catty-reminders

# Xóa container
docker rm catty-reminders

# Xóa container đang chạy (force)
docker rm -f catty-reminders
```

## Quản lý Images

### Xem danh sách images
```bash
docker images
```

### Xóa images
```bash
# Xóa một image
docker rmi catty-reminders:latest

# Xóa image bằng ID
docker rmi <image-id>

# Xóa các images không dùng
docker image prune
```

## Quản lý Volumes

### Xem volumes
```bash
docker volume ls
```

### Xóa volumes
```bash
# Xóa một volume
docker volume rm catty-data

# Xóa các volumes không dùng
docker volume prune
```

## Testing ứng dụng

### Kiểm tra ứng dụng đang chạy
```bash
# Kiểm tra bằng curl
curl http://localhost:8181

# Kiểm tra health
docker inspect --format='{{.State.Health.Status}}' catty-reminders
```

### Chạy tests trong container
```bash
# Chạy pytest trong container
docker exec catty-reminders pytest -v

# Chạy unit tests
docker exec catty-reminders pytest tests/test_unit.py
```

## Dọn dẹp (Cleanup)

### Dọn dẹp toàn bộ
```bash
# Stop tất cả containers
docker stop $(docker ps -aq)

# Xóa tất cả containers
docker rm $(docker ps -aq)

# Xóa tất cả images
docker rmi $(docker images -q)

# Dọn dẹp hệ thống (containers, images, volumes, networks không dùng)
docker system prune -a --volumes
```

## Troubleshooting

### Container không start được
```bash
# Xem logs để debug
docker logs catty-reminders

# Kiểm tra port có bị chiếm không
sudo lsof -i :8181
```

### Build image lỗi
```bash
# Build lại từ đầu không cache
docker-compose build --no-cache

# Kiểm tra Dockerfile syntax
docker build --progress=plain -t catty-reminders:latest .
```

### Ứng dụng không kết nối được
```bash
# Kiểm tra container có chạy không
docker ps

# Kiểm tra network
docker network inspect bridge

# Kiểm tra port mapping
docker port catty-reminders
```

## Production Tips

### Build optimized image cho production
```bash
# Multi-stage build để giảm size
# Thêm security scanning
docker build -t catty-reminders:prod -f Dockerfile.prod .
```

### Chạy với resource limits
```bash
docker run -d \
  --name catty-app \
  --memory="512m" \
  --cpus="1.0" \
  -p 8181:8181 \
  catty-reminders:latest
```

### Security best practices
- Không chạy container với root user
- Scan image với `docker scan catty-reminders:latest`
- Cập nhật base image thường xuyên
- Sử dụng secrets cho sensitive data

## Tài liệu tham khảo
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

