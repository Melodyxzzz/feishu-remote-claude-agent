@echo off
REM 适用于 Windows 任务计划程序的 VBScript

Option Explicit
Dim objShell, objFSO
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

Const TASK_NAME = "FeishuV1.0.0"
Const BATCH_FILE = "C:\Users\Administrator\feishu-remote-claude-agent\start_agent_server.bat"
Const WORKING_DIR = "C:\Users\Administrator\feishu-remote-claude-agent"

' 检查文件是否存在
If Not objFSO.FileExists(BATCH_FILE) Then
    WScript.Echo "错误: 找不到启动脚本: " & BATCH_FILE
    WScript.Quit 1
End If

' 创建任务计划命令
Dim cmd
cmd = "schtasks /create /tn """ & TASK_NAME & """ _
    & " /tr """ & BATCH_FILE & """" _
    & " /sc onlogon /rl highest /f"

' 执行命令
Dim result
result = objShell.Run(cmd, 0, True)

If result = 0 Then
    WScript.Echo "[OK] v1.0.0 自启动任务已创建"
    WScript.Echo ""
    WScript.Echo "任务名称: " & TASK_NAME
    WScript.Echo "启动脚本: " & BATCH_FILE
    WScript.Echo ""
    WScript.Echo "下次登录时将自动启动服务器"
Else
    WScript.Echo "[ERROR] 创建失败，错误代码: " & result
End If

Set objFSO = Nothing
Set objShell = Nothing

WScript.Echo ""
WScript.Echo "按任意键退出..."
WScript.StdIn.ReadLine
