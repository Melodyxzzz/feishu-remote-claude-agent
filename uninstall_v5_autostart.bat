@echo off
chcp 65001 >nul
echo ========================================
echo 飞书远程开发助手 v1.0.0 - 卸载开机自启动
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

echo 正在删除开机自启动任务...
echo.

REM 删除 v1.0.0 自启动任务
schtasks /delete /tn "飞书远程开发-v1.0.0服务器" /f 2>nul
echo [OK] 服务器自启动已删除

REM 删除 v4 旧任务（如果存在）
schtasks /delete /tn "飞书远程开发-服务器" /f 2>nul
schtasks /delete /tn "飞书远程开发-监控器" /f 2>nul
echo [OK] v4 旧任务已清理

echo.
echo ========================================
echo [OK] 开机自启动已完全卸载
echo ========================================
echo.
echo 如果需要重新安装，请运行:
echo    install_v5_autostart.bat (v1.0.0)
echo.
pause
