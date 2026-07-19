import reflex as rx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import struct

# 1. 创建底层的 FastAPI 实例
custom_fastapi = FastAPI(title="Reflex VLESS Node")

# 配置你的 VLESS 核心参数（从你的链接中提取）
TARGET_UUID = "792c9cd6-9ece-4ebc-ff02-86eaf8bf7e73"

@custom_fastapi.websocket("/")
async def vless_websocket_endpoint(websocket: WebSocket):
    """
    极简版 Python VLESS 协议解析与转发核心
    """
    await websocket.accept()
    remote_reader, remote_writer = None, None
    
    try:
        # 1. 读取 VLESS 握手数据包
        initial_data = await websocket.receive_bytes()
        if len(initial_data) < 20:
            await websocket.close()
            return

        # 2. 验证 UUID (VLESS 协议第一步：1字节版本号 + 16字节UUID)
        version = initial_data[0]
        client_uuid = initial_data[1:17].hex()
        # 将 hex 转为标准的 UUID 格式 (8-4-4-4-12)
        formatted_uuid = f"{client_uuid[:8]}-{client_uuid[8:12]}-{client_uuid[12:16]}-{client_uuid[16:20]}-{client_uuid[20:]}"
        
        if formatted_uuid != TARGET_UUID:
            print(f"Auth Failed: Invalid UUID {formatted_uuid}")
            await websocket.close()
            return

        # 3. 解析请求的目标地址与端口
        # 附加信息长度(1字节) -> 指令(1字节) -> 端口(2字节) -> 地址类型(1字节)
        addon_len = initial_data[17]
        cursor = 18 + addon_len
        cmd = initial_data[cursor] # 1 = TCP, 2 = UDP
        
        cursor += 1
        port = struct.unpack('!H', initial_data[cursor:cursor+2])[0]
        
        cursor += 2
        addr_type = initial_data[cursor]
        
        cursor += 1
        if addr_type == 1: # IPv4
            host = ".".join(str(b) for b in initial_data[cursor:cursor+4])
            cursor += 4
        elif addr_type == 2: # 域名
            domain_len = initial_data[cursor]
            host = initial_data[cursor+1:cursor+1+domain_len].decode('utf-8')
            cursor += 1 + domain_len
        else:
            await websocket.close()
            return

        # 剩余的数据是客户端发来的第一波真实网络请求数据
        payload = initial_data[cursor:]

        # 4. 连接到目标远程服务器 (真正的目标网站)
        remote_reader, remote_writer = await asyncio.open_connection(host, port)
        
        # 5. 向目标服务器发送 VLESS 响应首包（VLESS 协议要求服务端回应 1字节版本 + 1字节附加信息长度）
        # 这里回应 version 0, addon_len 0
        await websocket.send_bytes(b'\x00\x00')
        
        if payload:
            remote_writer.write(payload)
            await remote_writer.drain()

        # 6. 开始双向流量转发 (Data Forwarding)
        async def pipe_client_to_remote():
            try:
                while True:
                    data = await websocket.receive_bytes()
                    if not data: break
                    remote_writer.write(data)
                    await remote_writer.drain()
            except Exception:
                pass

        async def pipe_remote_to_client():
            try:
                while True:
                    data = await remote_reader.read(4096)
                    if not data: break
                    await websocket.send_bytes(data)
            except Exception:
                pass

        # 并发执行双向转发
        await asyncio.gather(pipe_client_to_remote(), pipe_remote_to_client())

    except (WebSocketDisconnect, Exception) as e:
        print(f"Connection closed or error: {e}")
    finally:
        if remote_writer:
            remote_writer.close()
            await remote_writer.wait_closed()

# --- 以下是正常的 Reflex 前端 UI 部分（用于完美伪装） ---

class State(rx.State):
    pass

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Welcome to My Portfolio", size="8"),
            rx.text("This is a personal demo landing page hosted on Reflex.", color_scheme="gray"),
            rx.button("Explore Projects", color_scheme="blue"),
            align="center",
            spacing="5",
        ),
        height="100vh",
    )

# 将自定义的 FastAPI 代理注入到 Reflex App 中
app = rx.App(api_transformer=custom_fastapi)
# 修改后的正确代码（将 path 改为 route）
app.add_page(index, route="/")