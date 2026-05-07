# AI 提示词工具箱

> 专为云端部署和飞书浏览器环境打造的 AI 提示词生成、优化与管理工具。

---

## 项目简介

AI 提示词工具箱是一个基于 FastAPI + SQLite 构建的轻量级 Web 应用，提供提示词生成、提示词优化和提示词管理三大核心功能。前端采用原生 HTML + Tailwind CSS，无需 Node.js 构建流程，整个项目可打包为单一 Docker 镜像，一键部署。

项目针对**飞书内置浏览器**和**移动端 WebView** 做了专门兼容，复制、确认弹窗、文件导出等操作在飞书环境中均可正常使用。

---

## 核心功能

### 1. 提示词生成器
选择场景类型、输出风格和语言，输入需求描述，一键生成结构化的高质量 AI 提示词。

**支持场景：**
- **图片生成** — 生成适用于 Stable Diffusion / Midjourney / DALL-E 的英文提示词
- **文案创作** — 生成小红书、公众号、广告文案等内容
- **编程开发** — 生成代码实现、算法解释、技术方案等
- **分析推理** — 生成数据分析、逻辑推理、决策建议等

**输出风格：**
- 专业严谨
- 详细全面
- 简洁精炼

### 2. 提示词优化器
输入原始提示词，系统自动分析缺陷并给出优化建议，同时输出优化后的完整提示词。

**优化目标：**
- 提高清晰度
- 增强结构化
- 增加细节约束
- 精简表达
- 强化角色设定

### 3. 提示词管理库
保存、搜索、分类、复制、删除提示词，支持 JSON 导入导出，数据持久化存储在 SQLite 数据库中。

---

## 技术架构

```
┌─────────────────────────────────────┐
│           前端 (Frontend)            │
│  原生 HTML + Tailwind CSS (CDN)     │
│  飞书 WebView 兼容层                 │
└──────────────┬──────────────────────┘
               │ 同域名 /api/* 请求
┌──────────────▼──────────────────────┐
│           后端 (Backend)             │
│  FastAPI (Python 3.11)              │
│  SQLite (文件型数据库)               │
│  单进程 Uvicorn 服务                 │
└─────────────────────────────────────┘
```

**设计原则：**
- **单容器单端口**：前端静态文件由 FastAPI 直接挂载，无需 Nginx 反向代理
- **零外部依赖**：仅需 Python 标准库 + FastAPI，无需 MySQL/Redis
- **数据持久化**：SQLite 数据库文件通过 Docker Volume 挂载到宿主机
- **飞书兼容**：复制、弹窗、下载等交互均做了降级兼容

---

## 目录结构

```
prompt-tool-linux/
├── backend/                 # FastAPI 后端
│   ├── main.py              # API 路由、数据库操作、静态文件挂载
│   ├── models.py            # Pydantic 数据模型（请求/响应校验）
│   ├── services.py          # 提示词生成/优化的业务逻辑
│   ├── requirements.txt     # Python 依赖
│   └── Dockerfile           # 后端镜像构建文件
├── frontend/                # 前端页面
│   └── index.html           # 单页应用（含 CSS/JS）
├── docker-compose.yml       # Docker Compose 编排
├── data/                    # 数据持久化目录（自动创建）
│   └── prompts.db           # SQLite 数据库文件
├── README.md                # 本文件（项目介绍）
└── DEPLOY.md                # 详细部署文档
```

---

## 飞书浏览器兼容性说明

飞书内置浏览器基于 WebView，对以下 Web API 有严格限制，本项目已针对性处理：

| 功能 | 普通浏览器 | 飞书浏览器限制 | 本项目方案 |
|------|-----------|--------------|-----------|
| 复制到剪贴板 | `navigator.clipboard` | 大概率被禁用 | 三层 fallback：Clipboard API → execCommand → 手动弹窗 |
| 确认弹窗 | `window.confirm()` | 可能被拦截或样式异常 | 自定义 CSS Modal 弹窗 |
| 文件下载 | `Blob` + `a[download]` | 可能被拦截 | 后端返回 `StreamingResponse` 文件流 |
| 本地存储 | `localStorage` | 隔离/清空 | 全部数据存后端 SQLite，不依赖前端存储 |

---

## API 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/generate` | 生成提示词 |
| POST | `/api/optimize` | 优化提示词 |
| GET | `/api/prompts` | 获取提示词列表（支持 `q` 搜索、`scene` 筛选） |
| POST | `/api/prompts` | 新增提示词 |
| DELETE | `/api/prompts/{id}` | 删除提示词 |
| GET | `/api/prompts/export` | 导出 JSON 文件 |
| POST | `/api/prompts/import` | 导入 JSON 数据 |

---

## 快速开始

```bash
cd prompt-tool-linux
docker compose up -d --build
```

访问 http://localhost:8088

详细部署方式请参考 [DEPLOY.md](./DEPLOY.md)

---

## License

MIT
