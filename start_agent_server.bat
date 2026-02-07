@echo off
chcp 65001 >nul
title 飞书远程开发助手 v5 - Agent SDK

echo ========================================
echo 飞书远程开发助手 v5
echo Agent SDK 版本
echo ========================================
echo.
echo 正在启动服务器...
echo.

python feishu_agent_server.py

pause
