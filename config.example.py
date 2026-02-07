# 飞书远程开发助手 v1.0.0 - 配置模板
#
# 使用说明:
# 1. 复制此文件为 config.py
# 2. 填写你的飞书应用凭证
# 3. (可选) 设置 ANTHROPIC_API_KEY 环境变量

# ==================== 飞书应用配置 ====================

# 从飞书开放平台获取: https://open.feishu.cn/
# 路径: 开发管理 -> 凭证与基础信息 -> App ID
APP_ID = "your_app_id_here"

# 路径: 开发管理 -> 凭证与基础信息 -> App Secret
APP_SECRET = "your_app_secret_here"

# ==================== 路径配置 ====================
#
# 默认情况下，所有文件都在项目目录内:
# - workspace/     : 任务工作空间
# - logs/          : 日志文件
# - *.json         : 运行时数据文件
#
# 如需自定义路径，取消下面的注释并修改:

# from pathlib import Path
# WORKSPACE_BASE = Path.home() / "feishu_workspace"
# TASK_QUEUE_FILE = Path.home() / "feishu_tasks.json"
# RESULT_FILE = Path.home() / "feishu_result.json"
# LOG_FILE = Path.home() / "feishu_agent_server.log"

# ==================== Claude Agent SDK 配置 ====================

# API Key (可选)
# 如果不设置,将使用本地 Claude Code CLI 的配置
# 获取地址: https://console.anthropic.com/
ANTHROPIC_API_KEY = None  # 或 "sk-ant-xxxxx"

# ==================== 系统提示配置 ====================

# 默认系统提示
SYSTEM_PROMPT = """你是一个远程开发助手，通过飞书接收用户指令。

当前任务:
- 任务ID: {task_id}
- 工作空间: {task_workspace}
- 用户指令: {user_message}

重要规则:
1. 所有文件操作都在任务工作空间中进行
2. 创建文件时使用明确的文件名和内容
3. 执行命令前先说明将做什么
4. 返回结果时要简洁清晰
5. 遇到错误时提供详细的错误信息和解决建议
"""

# ==================== Agent SDK 权限配置 ====================

# 允许使用的工具
# 可选值: "Read", "Write", "Edit", "Bash", "Glob", "Grep"
ALLOWED_TOOLS = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]

# 权限模式
# 可选值: "acceptEdits", "bypassPermissions", "default"
# - acceptEdits: 自动批准文件编辑
# - bypassPermissions: 完全自动运行
# - default: 需要手动确认
PERMISSION_MODE = "acceptEdits"
