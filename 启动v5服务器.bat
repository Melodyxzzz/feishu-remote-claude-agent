@echo off
REM 快速启动脚本（手动启动）
REM 可以放在桌面快捷方式

title 飞书远程开发助手 v1.0.0

echo ========================================
echo 飞书远程开发助手 v1.0.0
echo ========================================
echo.
echo 正在启动服务器...
echo.

cd /d C:\Users\Administrator\feishu-remote-claude-agent
python feishu_agent_server.py

pause
