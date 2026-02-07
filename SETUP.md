# 快速设置指南

## 配置飞书应用凭证

### 方式 1: 使用环境变量（推荐）

**Windows:**
```cmd
set FEISHU_APP_ID=cli_axxxxxxxxxxxx
set FEISHU_APP_SECRET=your_app_secret_here
python feishu_agent_server.py
```

**Linux/Mac:**
```bash
export FEISHU_APP_ID=cli_axxxxxxxxxxxx
export FEISHU_APP_SECRET=your_app_secret_here
python feishu_agent_server.py
```

### 方式 2: 使用配置文件

1. 复制配置模板:
   ```cmd
   copy config.example.py config.py
   ```

2. 编辑 `config.py`，填入你的凭证:
   ```python
   APP_ID = "cli_axxxxxxxxxxxx"
   APP_SECRET = "your_app_secret_here"
   ```

3. 启动服务器:
   ```cmd
   python feishu_agent_server.py
   ```

## 获取飞书应用凭证

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建应用或选择已有应用
3. 进入"开发管理" → "凭证与基础信息"
4. 复制 App ID 和 App Secret

## 设置开机自启动

### Windows

1. 编辑 `install_v5_autostart.bat`，添加环境变量:
   ```cmd
   set FEISHU_APP_ID=your_app_id
   set FEISHU_APP_SECRET=your_app_secret
   ```

2. 右键以管理员身份运行 `install_v5_autostart.bat`

### 验证安装

```cmd
schtasks /query /tn "飞书远程开发-v1.0.0服务器"
```

## 常见问题

**Q: 提示"飞书应用凭证未配置"怎么办？**

A: 请确保设置了 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量，或创建了 `config.py` 文件。

**Q: 如何设置 ANTHROPIC_API_KEY？**

A: 可选设置。如果不设置，将使用本地 Claude Code CLI 的配置。
```cmd
set ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**Q: 自启动任务启动失败？**

A: 检查任务计划程序中的历史记录，确认:
- Python 路径是否在 PATH 中
- 环境变量是否正确配置
- feishu_agent_server.py 文件路径是否正确
