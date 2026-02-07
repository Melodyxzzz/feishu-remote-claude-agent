@echo off
chcp 65001 >nul
echo ========================================
echo 飞书远程开发助手 v1.0.0 - 安装程序
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.10 或更高版本
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python 已安装: %PYTHON_VERSION%
echo.

REM 安装依赖
echo 正在安装 Python 依赖包...
echo.
echo [1/2] 安装飞书 SDK (lark-oapi)...
pip install lark-oapi>=1.4.0

if errorlevel 1 (
    echo ❌ lark-oapi 安装失败
    pause
    exit /b 1
)

echo ✅ lark-oapi 安装完成
echo.
echo [2/2] 安装 Claude Agent SDK...
pip install claude-agent-sdk>=0.1.0

if errorlevel 1 (
    echo ❌ claude-agent-sdk 安装失败
    echo.
    echo 可能的原因:
    echo 1. 需要有效的 Anthropic API Key
    echo 2. 网络连接问题
    echo.
    echo 请访问 https://console.anthropic.com/ 获取 API Key
    pause
    exit /b 1
)

echo ✅ claude-agent-sdk 安装完成
echo.

REM 创建 .env 文件（如果不存在）
if not exist .env (
    echo 正在创建 .env 配置文件...
    (
        echo # Anthropic API Key ^(必需^)
        echo # 获取地址: https://console.anthropic.com/
        echo ANTHROPIC_API_KEY=sk-ant-your-key-here
        echo.
        echo # 飞书应用配置 ^(通过环境变量或 config.py 配置^)
        echo # FEISHU_APP_ID=your_app_id_here
        echo # FEISHU_APP_SECRET=your_app_secret_here
        echo.
        echo # 工作区基础路径 ^(可选^)
        echo # WORKSPACE=C:\Users\YourUsername\feishu_workspace
    ) > .env
    echo.
    echo ⚠️  重要: 请编辑 .env 文件，设置你的 Anthropic API Key
    echo    获取地址: https://console.anthropic.com/
    echo.
)

REM 创建工作区目录
if not exist feishu_workspace (
    mkdir feishu_workspace
    echo ✅ 已创建工作区目录: feishu_workspace
)

echo.
echo ========================================
echo ✅ 安装完成！
echo ========================================
echo.
echo 📋 下一步操作:
echo.
echo 1. 编辑 .env 文件，设置 ANTHROPIC_API_KEY
echo    获取地址: https://console.anthropic.com/
echo.
echo 2. 启动服务器:
echo    python feishu_agent_server.py
echo.
echo 3. 或者使用启动脚本:
echo    start_agent_server.bat
echo.
pause
