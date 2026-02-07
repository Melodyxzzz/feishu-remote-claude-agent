@echo off
chcp 65001 >nul
echo ========================================
echo 飞书远程开发服务 - 卸载开机自启动
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

REM 删除任务计划
schtasks /delete /tn "飞书远程开发-服务器" /f
if %errorLevel% equ 0 (
    echo [OK] 飞书服务器已删除
) else (
    echo [WARN] 飞书服务器未找到或已删除
)

schtasks /delete /tn "飞书远程开发-监控器" /f
if %errorLevel% equ 0 (
    echo [OK] 智能监控器已删除
) else (
    echo [WARN] 智能监控器未找到或已删除
)

echo.
echo ========================================
echo [OK] 开机自启动已卸载！
echo ========================================
echo.
pause
