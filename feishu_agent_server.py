"""
飞书远程开发助手 v1.0.0 - 基于 Claude Agent SDK
项目: feishu-remote-claude-agent
使用 Claude Agent SDK 实现完全自动化
"""

import asyncio
import json
import os
import re
import sys
import threading
import lark_oapi as lark
from datetime import datetime
from pathlib import Path
from typing import Optional

# 版本信息
VERSION = "1.0.0"
PROJECT_NAME = "feishu-remote-claude-agent"

# Claude Agent SDK
try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("Claude Agent SDK 未安装")
    print("请运行: pip install claude-agent-sdk")
    sys.exit(1)

# ==================== 配置 ====================
# 获取项目根目录（脚本所在目录）
PROJECT_ROOT = Path(__file__).parent.absolute()

# 从环境变量读取飞书应用凭证
# 也可以创建 config.py 文件（参考 config.example.py）
APP_ID = os.getenv("FEISHU_APP_ID", "")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")

# 尝试从 config.py 加载配置（如果存在）
try:
    if not APP_ID or not APP_SECRET:
        import config
        APP_ID = getattr(config, "APP_ID", APP_ID)
        APP_SECRET = getattr(config, "APP_SECRET", APP_SECRET)
        WORKSPACE_BASE = getattr(config, "WORKSPACE_BASE", PROJECT_ROOT / "workspace")
        TASK_QUEUE_FILE = getattr(config, "TASK_QUEUE_FILE", PROJECT_ROOT / "feishu_tasks.json")
        RESULT_FILE = getattr(config, "RESULT_FILE", PROJECT_ROOT / "feishu_result.json")
        LOG_FILE = getattr(config, "LOG_FILE", PROJECT_ROOT / "logs" / "feishu_agent_server.log")
    else:
        WORKSPACE_BASE = PROJECT_ROOT / "workspace"
        TASK_QUEUE_FILE = PROJECT_ROOT / "feishu_tasks.json"
        RESULT_FILE = PROJECT_ROOT / "feishu_result.json"
        LOG_FILE = PROJECT_ROOT / "logs" / "feishu_agent_server.log"
except ImportError:
    WORKSPACE_BASE = PROJECT_ROOT / "workspace"
    TASK_QUEUE_FILE = PROJECT_ROOT / "feishu_tasks.json"
    RESULT_FILE = PROJECT_ROOT / "feishu_result.json"
    LOG_FILE = PROJECT_ROOT / "logs" / "feishu_agent_server.log"

# 确保必要的目录存在
WORKSPACE_BASE.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# 验证必需配置
if not APP_ID or not APP_SECRET:
    print("错误: 飞书应用凭证未配置")
    print("")
    print("请选择以下方式之一配置:")
    print("1. 设置环境变量:")
    print("   set FEISHU_APP_ID=your_app_id")
    print("   set FEISHU_APP_SECRET=your_app_secret")
    print("")
    print("2. 创建 config.py 文件（参考 config.example.py）")
    print("")
    sys.exit(1)

# ==================== 日志函数 ====================
def log(level: str, message: str):
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] [{level}] {message}\n"
    # 移除 emoji，避免 Windows GBK 编码问题
    clean_msg = log_msg.encode('ascii', 'ignore').decode('ascii').strip()
    print(clean_msg if clean_msg else log_msg.strip().encode('utf-8').decode('utf-8', 'ignore'))
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg)
    except:
        pass

# ==================== 任务管理 ====================
class TaskManager:
    def __init__(self):
        self.tasks = self._load_tasks()
        self.processed = set()
        self.lock = threading.Lock()

    def _load_tasks(self):
        if TASK_QUEUE_FILE.exists():
            try:
                with open(TASK_QUEUE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_tasks(self):
        with open(TASK_QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self, task: dict) -> int:
        """添加新任务"""
        with self.lock:
            task_id = max([t.get("id", 0) for t in self.tasks], default=0) + 1
            task["id"] = task_id
            task["timestamp"] = datetime.now().isoformat()
            task["status"] = "pending"
            self.tasks.append(task)
            self._save_tasks()
            return task_id

    def get_pending_tasks(self):
        """获取待处理任务"""
        with self.lock:
            return [t for t in self.tasks
                    if t.get("status") in ["pending", "confirmed"]
                    and t["id"] not in self.processed]

    def update_task_status(self, task_id: int, status: str, result: Optional[dict] = None):
        """更新任务状态"""
        with self.lock:
            for task in self.tasks:
                if task["id"] == task_id:
                    task["status"] = status
                    if status == "completed":
                        task["completedAt"] = datetime.now().isoformat()
                    elif status == "failed":
                        task["failedAt"] = datetime.now().isoformat()
                    if result:
                        task["result"] = result
                    break
            self._save_tasks()

    def save_result(self, task_id: int, success: bool, output: str = None, error: str = None):
        """保存任务结果"""
        result = {
            "taskId": task_id,
            "success": success,
            "output": output,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "processed": False
        }
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

# ==================== Claude Agent 处理器 ====================
class ClaudeAgentProcessor:
    def __init__(self, workspace_base: Path):
        self.workspace_base = workspace_base

    def _get_task_workspace(self, task_id: int, task_summary: str) -> Path:
        """获取任务工作空间"""
        folder_name = f"任务{task_id}_{task_summary[:20]}"
        task_path = self.workspace_base / folder_name
        task_path.mkdir(parents=True, exist_ok=True)
        return task_path

    async def process_task(self, task: dict) -> dict:
        """使用 Agent SDK 处理任务"""
        task_id = task["id"]
        user_message = task["userMessage"]

        log("INFO", f"🤖 Agent SDK 开始处理任务 #{task_id}: {user_message}")

        # 创建任务工作空间
        task_workspace = self._get_task_workspace(task_id, task.get("taskSummary", "unknown"))
        log("INFO", f"   工作空间: {task_workspace}")

        # 构建系统提示
        system_prompt = f"""你是一个远程开发助手，正在通过飞书接收用户指令。

当前任务:
- 任务ID: #{task_id}
- 工作空间: {task_workspace}
- 用户指令: {user_message}

重要规则:
1. 所有文件操作都在任务工作空间中进行
2. 创建文件时使用明确的文件名和内容
3. 执行命令前先说明将做什么
4. 如果用户要求 Git 提交，说明需要手动确认
5. 返回结果时要简洁清晰

工作空间已准备就绪，请执行用户指令。"""

        # 收集输出
        output_parts = []

        try:
            # 使用 Agent SDK 查询
            async for message in query(
                prompt=user_message,
                options=ClaudeAgentOptions(
                    system_prompt=system_prompt,
                    allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
                    permission_mode="acceptEdits"  # 自动批准编辑操作
                )
            ):
                # 处理不同类型的消息
                msg_type = type(message).__name__

                if msg_type == "AssistantMessage":
                    # Claude 的思考和输出
                    for block in message.content:
                        if hasattr(block, "text"):
                            output_parts.append(block.text)
                            log("INFO", f"   📝 {block.text[:100]}")

                elif msg_type == "ResultMessage":
                    # 最终结果
                    log("INFO", f"   ✅ 完成: {message.subtype}")
                    output_parts.append(f"\n[任务完成: {message.subtype}]")

            # 构建最终输出
            final_output = "\n".join(output_parts)

            return {
                "success": True,
                "output": final_output
            }

        except Exception as e:
            log("ERROR", f"   ❌ Agent SDK 执行失败: {e}")
            return {
                "success": False,
                "error": f"执行失败: {str(e)}"
            }

# ==================== 飞书消息处理 ====================
# 全局实例
task_manager = TaskManager()
agent_processor = ClaudeAgentProcessor(WORKSPACE_BASE)
lark_client = None

def get_lark_client():
    """获取飞书客户端单例"""
    global lark_client
    if lark_client is None:
        lark_client = lark.Client.builder() \
            .app_id(APP_ID) \
            .app_secret(APP_SECRET) \
            .log_level(lark.LogLevel.ERROR) \
            .build()
    return lark_client

def send_message_to_feishu(chat_id: str, text: str, message_id: str = None) -> bool:
    """发送消息到飞书"""
    try:
        client = get_lark_client()

        # 如果有 message_id，使用 reply API
        if message_id:
            request = lark.api.im.v1.ReplyMessageRequest.builder() \
                .message_id(message_id) \
                .request_body(lark.api.im.v1.ReplyMessageRequestBody.builder()
                    .content(json.dumps({"text": text}))
                    .msg_type("text")
                    .reply_in_thread(False)
                    .build()) \
                .build()

            response = client.im.v1.message.reply(request)
        else:
            # 否则使用 create API
            request = lark.api.im.v1.CreateMessageRequest.builder() \
                .receive_id_type("chat_id") \
                .request_body(lark.api.im.v1.CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("text")
                    .content(json.dumps({"text": text}))
                    .build()) \
                .build()

            response = client.im.v1.message.create(request)

        if response.code == 0:
            log("INFO", "✅ 消息发送成功")
            return True
        else:
            log("ERROR", f"消息发送失败: {response.msg}")
            return False

    except Exception as e:
        log("ERROR", f"发送消息异常: {e}")
        return False

def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1):
    """处理飞书接收消息事件"""
    try:
        # 使用 JSON marshal 序列化对象来访问数据
        data_json = lark.JSON.marshal(data)

        # 解析 JSON - 数据在 event.event 里
        event_wrapper = json.loads(data_json)
        event_data = event_wrapper.get('event', {})

        # 提取字段
        sender_data = event_data.get('sender', {})
        sender_id = sender_data.get('sender_id', {}).get('open_id', '')

        message_data = event_data.get('message', {})
        chat_id = message_data.get('chat_id', '')
        message_id = message_data.get('message_id', '')
        message_type = message_data.get('message_type', '')
        content_raw = message_data.get('content', '{}')

        log("INFO", f"收到消息 - Sender: {sender_id}, Type: {message_type}")

        if message_type != "text":
            return

        # 解析消息内容
        try:
            content = json.loads(content_raw) if isinstance(content_raw, str) else content_raw
            user_message = content.get("text", "").strip()
        except:
            user_message = ""

        if not user_message:
            return

        log("INFO", f"用户消息: {user_message}")

        # 检查是否是简单确认
        if is_simple_confirmation(user_message):
            handle_confirmation(user_message, sender_id, chat_id, message_id)
            return

        # 添加任务到队列
        safe_summary = re.sub(r'[<>:"/\\|?*]', '_', user_message[:20])
        task = {
            "senderId": sender_id,
            "chatId": chat_id,
            "messageId": message_id,
            "userMessage": user_message,
            "taskSummary": safe_summary,
            "remote": True,
            "workspaceBasePath": str(WORKSPACE_BASE)
        }

        task_id = task_manager.add_task(task)

        # 立即回复
        send_message_to_feishu(chat_id,
            f"✅ 已收到消息，任务ID: #{task_id}\n\n正在由 AI 处理...", message_id)

    except Exception as e:
        log("ERROR", f"处理消息失败: {e}")

def is_simple_confirmation(message: str) -> bool:
    """判断是否是简单确认"""
    lower_msg = message.lower().strip()
    confirm_keywords = ["确认", "confirm", "好的", "ok", "是", "yes"]
    cancel_keywords = ["取消", "cancel", "不", "no", "不要", "nope"]

    return (lower_msg in confirm_keywords or
            lower_msg in cancel_keywords or
            lower_msg in ["提交git", "git commit", "git提交"])

def handle_confirmation(user_message: str, sender_id: str, chat_id: str, message_id: str):
    """处理确认响应"""
    # TODO: 实现确认逻辑
    pass

# 创建事件处理器
event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .build()

# ==================== 任务处理循环 ====================
async def process_tasks_loop():
    """任务处理循环"""
    while True:
        try:
            pending_tasks = task_manager.get_pending_tasks()

            if pending_tasks:
                log("INFO", f"🔔 发现 {len(pending_tasks)} 个待处理任务")

                for task in pending_tasks:
                    # 使用 Agent SDK 处理
                    result = await agent_processor.process_task(task)

                    # 保存结果
                    task_manager.save_result(
                        task["id"],
                        result["success"],
                        result.get("output"),
                        result.get("error")
                    )

                    # 更新任务状态
                    status = "completed" if result["success"] else "failed"
                    task_manager.update_task_status(task["id"], status, result)

                    # 发送结果到飞书
                    result_data = task.get("result", {})
                    success = result_data.get("success", False)

                    if success:
                        message = f"✅ 任务 #{task['id']} 执行成功\n\n{result_data.get('output', '')}"
                    else:
                        message = f"❌ 任务 #{task['id']} 执行失败\n\n{result_data.get('error', '未知错误')}"

                    send_message_to_feishu(task["chatId"], message, task["messageId"])
                    log("INFO", f"任务 #{task['id']} 结果已发送")

                    # 标记为已处理
                    task_manager.processed.add(task["id"])

            await asyncio.sleep(1)  # 1秒检查一次

        except Exception as e:
            log("ERROR", f"任务处理循环错误: {e}")
            await asyncio.sleep(5)

# ==================== 主函数 ====================
def start_lark_client():
    """启动飞书 WebSocket 客户端（在单独线程中运行）"""
    client = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.ERROR
    )
    client.start()

def start_agent_processor():
    """启动 Agent 处理器（在主线程中运行）"""
    asyncio.run(process_tasks_loop())

if __name__ == "__main__":
    log("INFO", "========================================")
    log("INFO", f"{PROJECT_NAME} v{VERSION}")
    log("INFO", "基于 Claude Agent SDK 的远程开发助手")
    log("INFO", "========================================")
    log("INFO", f"App ID: {APP_ID}")
    log("INFO", f"工作区: {WORKSPACE_BASE}")
    log("INFO", f"任务队列: {TASK_QUEUE_FILE}")
    log("INFO", "")
    log("INFO", "正在启动服务...")

    # 在单独线程中启动飞书 WebSocket 客户端
    ws_thread = threading.Thread(target=start_lark_client, daemon=True)
    ws_thread.start()

    log("INFO", "✅ 飞书 WebSocket 客户端已启动")
    log("INFO", "📱 现在可以在飞书中发送指令了！")
    log("INFO", "")
    log("INFO", "🎯 Agent SDK 自动化模式:")
    log("INFO", "   1. 接收飞书消息")
    log("INFO", "   2. Agent SDK 自动处理")
    log("INFO", "   3. 结果返回飞书")
    log("INFO", "")
    log("INFO", "按 Ctrl+C 停止")

    try:
        # 在主线程中启动 Agent 处理器
        start_agent_processor()
    except KeyboardInterrupt:
        log("INFO", "正在停止服务器...")
        sys.exit(0)
