# Hướng Dẫn Cấu Hình GitHub Secrets cho Deploy Workflow

## ❌ Lỗi hiện tại:
```
Error: can't connect without a private SSH key or password
```

**Nguyên nhân**: Chưa cấu hình GitHub Secrets (SSH_HOST, SSH_USER, SSH_PRIVATE_KEY)

---

## 🔑 Bước 1: Tạo SSH Key trên VM

**Chạy trên VM của bạn** (qua SSH hoặc console):

```bash
# Tạo SSH key mới cho GitHub Actions
ssh-keygen -t rsa -C "github-actions" -f ~/.ssh/github_actions -N ""

# Thêm public key vào authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys

# Set permissions đúng
chmod 600 ~/.ssh/github_actions
chmod 644 ~/.ssh/github_actions.pub
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

echo "✅ SSH key đã được tạo!"
```

---

## 📋 Bước 2: Copy Private Key

**Chạy lệnh này để hiển thị private key:**

```bash
cat ~/.ssh/github_actions
```

**Output sẽ giống như:**
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
(nhiều dòng)
...
-----END RSA PRIVATE KEY-----
```

⚠️ **QUAN TRỌNG**: Copy **TOÀN BỘ** nội dung (bao gồm cả dòng BEGIN và END)

---

## 🌐 Bước 3: Thêm Secrets vào GitHub

### Vào GitHub Repository:
1. Mở repo: https://github.com/[your-username]/devops-minh
2. Click **Settings** (tab trên cùng)
3. Sidebar bên trái: **Secrets and variables** → **Actions**
4. Click nút **New repository secret**

### Thêm 3 Secrets sau:

#### Secret 1: SSH_PRIVATE_KEY
- **Name**: `SSH_PRIVATE_KEY`
- **Value**: Paste toàn bộ nội dung từ lệnh `cat ~/.ssh/github_actions`
  ```
  -----BEGIN RSA PRIVATE KEY-----
  MIIEpAIBAAKCAQEA...
  ...
  -----END RSA PRIVATE KEY-----
  ```
- Click **Add secret**

#### Secret 2: SSH_HOST
- **Name**: `SSH_HOST`
- **Value**: `course.prafdin.ru`
- Click **Add secret**

#### Secret 3: SSH_USER
- **Name**: `SSH_USER`
- **Value**: `quangminh` (hoặc username VM của bạn)
- Click **Add secret**

---

## ✅ Bước 4: Kiểm Tra SSH Connection (Optional)

**Test kết nối từ máy local tới VM qua FRP:**

```bash
ssh -p 2468 quangminh@course.prafdin.ru -i ~/.ssh/github_actions
```

Nếu connect được nghĩa là SSH key hoạt động!

---

## 🚀 Bước 5: Test Workflow

### Cách 1: Tạo Release (theo yêu cầu workflow)
1. Vào GitHub repo → **Releases**
2. Click **"Create a new release"**
3. **Tag**: `v1.0.0`
4. **Release title**: `Release v1.0.0`
5. **Description**: Test deployment
6. Click **"Publish release"**
7. Workflow sẽ tự động chạy!

### Cách 2: Sửa trigger để test nhanh (tạm thời)
Thay đổi trong `deploy.yml`:
```yaml
on:
  push:
    branches: [ github-action ]
  release:
    types: [published]
```

Sau đó:
```bash
git add .
git commit -m "Test deployment workflow"
git push origin github-action
```

---

## 🔍 Xem Kết Quả

1. Vào repo → **Actions** tab
2. Click vào workflow run mới nhất
3. Xem logs để debug nếu có lỗi

---

## 📌 Thông Tin Cấu Hình Của Bạn

```
PROXY      = course.prafdin.ru
TOKEN      = devops
ID         = chan
SSH_PORT   = 2468
APP_URL    = http://app.chan.course.prafdin.ru
```

---

## ⚠️ Troubleshooting

### Lỗi: "Permission denied (publickey)"
→ Kiểm tra SSH key đã được add vào `~/.ssh/authorized_keys` chưa

### Lỗi: "Connection refused"
→ Kiểm tra FRP service đang chạy: `sudo systemctl status frpc`

### Lỗi: "Host key verification failed"
→ Thêm vào deploy.yml:
```yaml
with:
  host: ${{secrets.SSH_HOST}}
  port: 2468
  username: ${{secrets.SSH_USER}}
  key: ${{secrets.SSH_PRIVATE_KEY}}
  script_stop: true
```

---

## ✨ Sau Khi Hoàn Thành

Bạn sẽ có CI/CD pipeline hoàn chỉnh:
- ✅ **CI Workflow** (`ci.yml`) - Chạy tests tự động khi push
- ✅ **CD Workflow** (`deploy.yml`) - Deploy tự động khi tạo release

🎉 **Lab 2 hoàn thành!**

