# AI 提示词工具箱 部署文档

本文档提供多种部署方式，包括 Docker Compose（推荐）、纯 Docker 和裸机部署。

---

## 目录

- [环境要求](#环境要求)
- [方式一：Docker Compose 部署（推荐）](#方式一docker-compose-部署推荐)
- [方式二：纯 Docker 部署](#方式二纯-docker-部署)
- [方式三：裸机部署](#方式三裸机部署)
- [数据备份与恢复](#数据备份与恢复)
- [修改端口](#修改端口)
- [常见问题](#常见问题)

---

## 环境要求

### Docker 部署
- Docker Engine >= 20.10
- Docker Compose >= 2.0（或 docker compose 插件）

### 裸机部署
- Python >= 3.11
- pip
- 操作系统：Linux / macOS / WSL

---

## 方式一：Docker Compose 部署（推荐）

这是最简单、推荐的部署方式，适合所有生产环境。

### 1. 拉取代码

```bash
git clone <你的仓库地址> prompt-tool-linux
cd prompt-tool-linux
```

如果没有 Git，可以直接下载源码压缩包并解压到目标目录。

### 2. 启动服务

```bash
docker compose up -d --build
```

命令说明：
- `-d` — 后台运行
- `--build` — 第一次运行时构建镜像

### 3. 验证部署

```bash
# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f

# 测试接口
curl http://localhost:8088/api/generate \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"desc":"测试","scene":"copywriting","style":"concise","lang":"zh"}'
```

### 4. 访问应用

打开浏览器访问：

```
http://<服务器IP>:8088
```

如果是本地部署：`http://localhost:8088`

### 5. 停止和重启

```bash
# 停止
docker compose down

# 重启
docker compose restart

# 重新构建并启动（代码更新后使用）
docker compose up -d --build
```

### 6. 更新部署

```bash
# 拉取新代码（如果用 Git）
git pull

# 重新构建并启动
docker compose up -d --build
```

> 更新时 SQLite 数据库不会丢失，因为通过 volume 挂载在 `data/` 目录。

---

## 方式二：纯 Docker 部署

如果不想用 Docker Compose，可以直接用 Docker 启动。

### 1. 构建镜像

```bash
cd prompt-tool-linux
docker build -f backend/Dockerfile -t prompt-tool .
```

### 2. 创建数据目录

```bash
mkdir -p data
```

### 3. 运行容器

```bash
docker run -d \
  --name prompt-tool \
  -p 8088:8088 \
  -v "$(pwd)/data:/app/data" \
  --restart unless-stopped \
  prompt-tool
```

### 4. 管理

```bash
# 查看日志
docker logs -f prompt-tool

# 重启
docker restart prompt-tool

# 停止并删除
docker rm -f prompt-tool
```

---

## 方式三：裸机部署

适合不想用 Docker 或需要在轻量级 VPS 上部署的场景。

### 1. 环境准备

```bash
# 确认 Python 版本 >= 3.11
python3 --version

# 如果不满足，请先升级（以 Ubuntu 为例）
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv
```

### 2. 创建虚拟环境

```bash
cd prompt-tool-linux/backend
python3.11 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 创建数据目录

```bash
mkdir -p ../data
```

### 5. 启动服务

```bash
cd ..
PYTHONPATH=backend python3.11 -m uvicorn backend.main:app --host 0.0.0.0 --port 8088
```

或使用 nohup 后台运行：

```bash
nohup python3.11 -m uvicorn backend.main:app --host 0.0.0.0 --port 8088 > server.log 2>&1 &
```

### 6. 使用 systemd 守护（生产环境推荐）

创建服务文件：

```bash
sudo tee /etc/systemd/system/prompt-tool.service > /dev/null << 'EOF'
[Unit]
Description=AI 提示词工具箱
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/prompt-tool-linux
Environment="PYTHONPATH=/opt/prompt-tool-linux/backend"
ExecStart=/opt/prompt-tool-linux/backend/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8088
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

> 注意：将 `/opt/prompt-tool-linux` 替换为你的实际项目路径。

启动并设置开机自启：

```bash
sudo systemctl daemon-reload
sudo systemctl enable prompt-tool
sudo systemctl start prompt-tool
sudo systemctl status prompt-tool
```

---

## 数据备份与恢复

### 自动备份

SQLite 数据库是单个文件，备份非常简单：

```bash
# Docker 部署
cp data/prompts.db data/prompts.db.$(date +%Y%m%d).backup

# 裸机部署（假设项目在 /opt/prompt-tool-linux）
cp /opt/prompt-tool-linux/data/prompts.db /opt/prompt-tool-linux/data/prompts.db.$(date +%Y%m%d).backup
```

建议添加 cron 定时备份：

```bash
0 2 * * * cp /opt/prompt-tool-linux/data/prompts.db /opt/prompt-tool-linux/data/prompts.db.$(date +\%Y\%m\%d).backup
```

### 通过 API 导出

在管理库页面点击"导出 JSON"按钮，或访问：

```bash
curl http://localhost:8088/api/prompts/export -o prompts_backup.json
```

### 恢复数据

```bash
# 停止服务
docker compose down

# 复制备份文件覆盖（仅适用于单文件备份）
cp data/prompts.db.20240115.backup data/prompts.db

# 重新启动
docker compose up -d
```

---

## 修改端口

默认端口是 `8088`。如需修改，需要同时改动两处：

### 1. 修改 docker-compose.yml

```yaml
services:
  prompt-tool:
    # ...
    ports:
      - "你的端口:8088"   # 修改左侧宿主端口
```

示例：改为 `3000` 端口

```yaml
ports:
  - "3000:8088"
```

### 2. 重新启动

```bash
docker compose up -d
```

### 3. 如果有防火墙，开放端口

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 3000/tcp

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload
```

---

## 常见问题

### Q1: 容器启动失败，提示端口被占用

解决：查找并停止占用端口的进程

```bash
sudo lsof -i :8088
sudo kill -9 <PID>
```

或修改 `docker-compose.yml` 换用其他端口。

### Q2: 前端页面能打开，但 API 请求报错

解决：检查后端日志

```bash
docker compose logs -f
```

常见原因：
- 服务启动中，等待几秒后刷新
- 磁盘空间不足

### Q3: 飞书中复制功能不工作

解决：本项目已对飞书浏览器做了兼容处理。如果仍然复制失败，会自动弹出手动复制窗口，请手动选中文本后复制。

### Q4: 导出 JSON 文件名乱码

解决：后端已设置 `Content-Disposition` 头中文编码为 UTF-8。如果某些浏览器仍然显示乱码，可以在管理库页面点击复制按钮，手动粘贴到文件中保存。

### Q5: 如何完全重置数据

```bash
# Docker Compose 部署
docker compose down
rm -f data/prompts.db
docker compose up -d

# 纯 Docker 部署
docker rm -f prompt-tool
rm -f data/prompts.db
docker run -d --name prompt-tool -p 8088:8088 -v "$(pwd)/data:/app/data" prompt-tool

# 裸机部署
rm -f data/prompts.db
# 然后重启服务
```

### Q6: 如何在子路径下部署（例如 /tools/prompt）

本项目前端使用相对路径调用 API（`API = ''`），会自动适配当前域名。如果需要放在反向代理的子路径下，请确保代理正确转发请求：

```nginx
location /tools/prompt/ {
    proxy_pass http://localhost:8088/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

## 性能调优

### 服务器资源占用

- **CPU**：低负载，平均使用率 < 1%
- **内存**：约 50-100MB
- **磁盘**：镜像约 200MB，数据库按实际数据增长

### 推荐配置

| 场景 | CPU | 内存 | 磁盘 |
|------|-----|------|------|
| 个人使用 | 1 核 | 512MB | 2GB |
| 小团队 | 2 核 | 1GB | 5GB |
| 企业部署 | 4 核 | 2GB | 20GB |

---

## 联系与反馈

如遇到部署问题，请检查：
1. [常见问题](#常见问题) 部分
2. 服务器日志输出
3. 磁盘和内存使用情况
