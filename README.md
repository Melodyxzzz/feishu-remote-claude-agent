# feishu-remote-claude-agent

> 基于 Claude Agent SDK 的飞书远程开发助手 v1.0.0

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Claude Agent SDK](https://img.shields.io/badge/Claude_Agent_SDK-0.1.31+-green.svg)](https://github.com/anthropics/claude-agent-sdk)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

**feishu-remote-claude-agent** 是一个创新的远程开发助手，通过飞书消息与 Claude AI 进行交互，实现真正的远程自动化开发。

### 核心特性

- **完全自动化**: 使用 Claude Agent SDK 自动调用 Claude，无需手动干预
- **自然语言交互**: 支持中文自然语言指令，AI 智能理解和执行
- **安全隔离**: 每个任务在独立工作空间中执行，互不干扰
- **实时响应**: 飞书 WebSocket 长连接，消息即时处理
- **多功能支持**: 文件操作、代码编辑、命令执行、Git 操作等

## 系统架构

```
┌─────────────┐
│  飞书手机端  │ 用户发送指令
└──────┬──────┘
       │ WebSocket 长连接
       ▼
┌─────────────────────────────┐
│  feishu_agent_server.py     │
│  (Python + Agent SDK)       │
│                             │
│  1. 接收飞书消息            │
│  2. 添加到任务队列          │
│  3. Agent SDK 自动处理      │
│  4. 结果返回飞书            │
└─────────────────────────────┘
       │
       │ claude-agent-sdk
       ▼
┌─────────────────────────────┐
│  Claude Agent (自动执行)     │
│                             │
│  - 读取文件                 │
│  - 编辑代码                 │
│  - 执行命令                 │
│  - Git 提交                 │
└─────────────────────────────┘
```

## 快速开始

### 前置要求

- Python 3.14 或更高版本
- 飞书开放平台账号 (获取 APP_ID 和 APP_SECRET)
- Claude Code CLI 或 ANTHROPIC_API_KEY

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/feishu-remote-claude-agent.git
   cd feishu-remote-claude-agent
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**

   编辑 `feishu_agent_server.py` 中的配置：
   ```python
   APP_ID = "your_app_id"
   APP_SECRET = "your_app_secret"
   ```

   或设置环境变量：
   ```env
   ANTHROPIC_API_KEY=your-api-key-here
   ```

4. **启动服务器**
   ```bash
   python feishu_agent_server.py
   ```

5. **在飞书中发送指令**

   示例：
   - `创建hello.txt，内容为Hello World`
   - `列出当前目录的文件`
   - `把hello.txt的内容改成Hello Claude`

## 开机自启动

### Windows 系统

**安装自启动:**
```bash
# 右键以管理员身份运行
install_v5_autostart.bat
```

**卸载自启动:**
```bash
# 右键以管理员身份运行
uninstall_v5_autostart.bat
```

**验证自启动:**
```bash
schtasks /query /tn "飞书远程开发-v1.0.0服务器"
```

## 使用指南

### 基础用法

1. **文件操作**
   ```
   创建test.py，内容为print("Hello World")
   读取package.json
   删除temp.txt
   ```

2. **代码编辑**
   ```
   把index.html的标题改成"我的应用"
   在utils.js中添加一个计算平方的函数
   ```

3. **命令执行**
   ```
   运行npm install
   执行python test.py
   查看当前目录的git状态
   ```

### 高级用法

1. **复杂任务**
   ```
   创建一个Python脚本实现快速排序
   分析当前目录的文件结构并生成报告
   重构这个函数，使其更高效
   ```

2. **Git 操作**
   ```
   提交当前修改到Git
   创建新分支feature/login
   查看最近的提交历史
   ```

3. **自然语言对话**
   ```
   今天广州天气怎么样？
   解释一下什么是量子计算
   帮我理解这段代码的作用
   ```

## 工作原理

### Agent SDK 自动化流程

```python
async for message in query(
    prompt=user_message,
    options=ClaudeAgentOptions(
        system_prompt=custom_prompt,
        allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        permission_mode="acceptEdits"
    )
):
    # Claude 自动执行操作
    pass
```

### 关键配置

**allowed_tools** - 控制功能：
- `Read`, `Glob`, `Grep`: 只读分析
- `Read`, `Edit`, `Glob`: 分析和修改代码
- `Read`, `Edit`, `Bash`, `Glob`, `Grep`: 全自动化

**permission_mode** - 控制权限：
- `acceptEdits`: 自动批准文件编辑
- `bypassPermissions`: 完全自动运行
- `default`: 需要手动确认

## 安全隔离

每个任务都在独立的文件夹中执行：

```
feishu_workspace/
├── 任务1_创建hello.txt/     ← 任务1的工作空间
├── 任务2_列出文件/         ← 任务2的工作空间
└── 任务3_修改代码/         ← 任务3的工作空间
```

**好处**：
- 任务之间互不干扰
- 可以随时删除特定任务
- 便于追溯和管理

## 项目结构

```
feishu-remote-claude-agent/
├── feishu_agent_server.py      # 主服务器
├── requirements.txt            # Python 依赖
├── README.md                   # 项目文档
├── install_v5_autostart.bat    # 安装自启动
├── uninstall_v5_autostart.bat  # 卸载自启动
├── 启动v5服务器.bat             # 手动启动脚本
├── setup_agent_server.bat      # 安装脚本
└── start_agent_server.bat      # 启动脚本
```

## 故障排查

### 错误: `ModuleNotFoundError: No module named 'claude_agent_sdk'`

**解决**: 安装依赖
```bash
pip install -r requirements.txt
```

### 错误: `API key not found`

**解决**: 设置环境变量
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 错误: 飞书消息发送失败

**解决**: 检查 APP_ID 和 APP_SECRET 配置

### 错误: WebSocket 连接失败

**解决**:
1. 检查网络连接
2. 验证飞书应用凭证
3. 查看日志文件 `feishu_agent_server.log`

## 最佳实践

1. **明确指令**: 清晰描述你想要什么
   - ✅ "创建index.html，包含一个按钮"
   - ❌ "做个网页"

2. **使用工作空间**: 了解任务在独立文件夹中执行
   - 文件路径: `feishu_workspace/任务X_任务名称/`

3. **权限控制**: 根据需求配置 `allowed_tools`
   - 只读分析: `["Read", "Glob", "Grep"]`
   - 修改代码: `["Read", "Edit", "Glob"]`
   - 全自动化: `["Read", "Edit", "Bash", "Glob", "Grep"]`

4. **安全性**: 生产环境建议使用 `acceptEdits` 模式
   - 自动批准文件编辑
   - 其他操作需要确认

## 版本历史

### v1.0.0 (2026-02-07)

- 使用 Claude Agent SDK 实现完全自动化
- 支持自然语言理解和交互
- 安全的工作空间隔离
- WebSocket 实时消息处理
- 完整的文件操作和命令执行支持

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) - Anthropic 出品的 Claude AI 自动化工具
- [lark-oapi](https://github.com/larksuite/oapi-sdk-python) - 飞书开放平台 Python SDK
- [Claude Code](https://claude.ai/code) - Anthropic 的 AI 编程助手

## 联系方式

- 项目主页: [https://github.com/yourusername/feishu-remote-claude-agent](https://github.com/yourusername/feishu-remote-claude-agent)
- 问题反馈: [GitHub Issues](https://github.com/yourusername/feishu-remote-claude-agent/issues)

---

**版本**: v1.0.0 | **更新日期**: 2026-02-07
