"""
测试 lark-oapi SDK 事件数据结构
"""
import lark_oapi as lark

# 模拟事件数据结构
print("=== lark-oapi SDK 事件处理测试 ===\n")

# 查看 P2ImMessageReceiveV1 的结构
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

print("P2ImMessageReceiveV1 类属性:")
attrs = [attr for attr in dir(P2ImMessageReceiveV1) if not attr.startswith('_')]
for attr in attrs:
    print(f"  - {attr}")

print("\n" + "="*50)
print("\n根据飞书文档，事件数据应该这样访问:")
print("""
# 正确的访问方式（可能）:

def do_p2_im_message_receive_v1(data):
    # 方式1: 直接属性访问
    sender_id = data.sender.sender_id.open_id
    chat_id = data.message.chat_id

    # 方式2: 通过 _event_dict
    event_dict = data._event_dict
    sender_id = event_dict['sender']['sender_id']['open_id']

    # 方式3: 使用 marshal 查看完整结构
    import json
    print(json.dumps(data.__dict__, indent=2))
""")
