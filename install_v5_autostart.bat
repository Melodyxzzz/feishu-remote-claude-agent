@echo off
chcp 65001 >nul
echo ========================================
echo 飞书远程开发助手 v1.0.0 - 安装开机自启动
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 需要管理员权限！
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo 正在注册开机自启动任务...
echo.

REM 获取 Python 路径
for %%i in (python.exe) do set PYTHON_PATH=%%~$PATH:i
if not defined PYTHON_PATH (
    echo 错误: 找不到 python.exe
    echo 请确保 Python 已安装并在 PATH 中
    pause
    exit /b 1
)

echo Python 路径: %PYTHON_PATH%
echo.

REM 删除旧的自启动任务（如果存在）
echo [1/3] 删除旧的自启动任务...
schtasks /delete /tn "飞书远程开发-v1.0.0服务器" /f 2>nul
schtasks /delete /tn "飞书远程开发-v4服务器" /f 2>nul
schtasks /delete /tn "飞书远程开发-监控器" /f 2>nul
echo 已完成

REM 创建 v5 服务器任务计划
echo [2/3] 创建 v5 服务器自启动任务...
schtasks /create /tn "飞书远程开发-v1.0.0服务器" /tr "\"%PYTHON_PATH%\" \"%USERPROFILE%\feishu_agent_server.py\"" /sc onlogon /rl highest /f 2>nul

if %errorLevel% equ 0 (
    echo [OK] 服务器已注册到开机自启动
) else (
    echo [WARN] 服务器注册失败（可能已存在）
)

echo.
echo [3/3] 查看已注册的任务...
schtasks /query /tn "飞书远程开发-v1.0.0服务器" 2>nul

echo.
echo ========================================
echo [OK] v1.0.0 开机自启动安装完成！
echo ========================================
echo.
echo ✅ 已注册任务:
echo    - 飞书远程开发-v1.0.0服务器
echo.
echo 下次开机时，服务器将自动启动。
echo.
echo 如需删除自启动，请运行:
echo    uninstall_v5_autostart.bat
echo.
pause
