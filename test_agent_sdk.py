"""
测试 Claude Agent SDK 基本功能
"""
import asyncio
import sys
from pathlib import Path

# 检查是否需要 API Key
import os
if not os.getenv("ANTHROPIC_API_KEY"):
    print("Warning: ANTHROPIC_API_KEY not set in environment")
    print("Please create .env file with your API key")
    print("Or run: set ANTHROPIC_API_KEY=sk-ant-xxxxx")

async def test_agent_sdk():
    """测试 Agent SDK 基本功能"""
    try:
        from claude_agent_sdk import query, ClaudeAgentOptions

        print("Claude Agent SDK imported successfully")
        print("Testing basic query...")

        # 简单测试 - 列出当前目录文件
        async for message in query(
            prompt="List the files in current directory",
            options=ClaudeAgentOptions(
                allowed_tools=["Glob"],
                permission_mode="bypassPermissions"
            )
        ):
            msg_type = type(message).__name__
            if msg_type == "AssistantMessage":
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text[:200])
            elif msg_type == "ResultMessage":
                print(f"Result: {message.subtype}")

        print("\nTest completed successfully!")
        return True

    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_sdk())
    sys.exit(0 if success else 1)
