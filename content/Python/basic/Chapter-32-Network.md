+++
title = "第32章 网络编程"
weight = 320
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第32章 网络编程：让你的程序学会"上网冲浪"

> 🧑‍💻 警告：本章内容可能会让你对"打开网页"这件事产生全新的敬畏——因为你会发现，每一次点击背后，都有一大堆协议在疯狂加班。

**网络编程**，听起来高大上对吧？但说白了，就是让你的程序能够和其他程序"打电话"。想象一下，你用微信给朋友发消息，背后的技术栈能让这条消息从你的手机出发，穿越半个地球，准确无误地落到你朋友手里——这，就是网络编程的魔力。

Python 在网络编程方面堪称"瑞士军刀"，无论是写个小爬虫爬取网页，还是搭一个高性能 Web 服务器，Python 都能轻松搞定。

---

## 32.1 网络协议

### 32.1.1 TCP / IP 协议栈

在正式开始写代码之前，咱们得先聊聊"协议"这个玩意儿。**协议（Protocol）** 就是网络世界里的"交通规则"——没有规则，大家想怎么传数据就怎么传，那网络早就乱成一锅粥了。

**TCP/IP 协议栈** 是互联网的基础，它其实不是单个协议，而是一整套协议族。形象地说，它就像一栋大楼，不同的楼层负责不同的事情：

```
┌─────────────────────────────────────────────┐
│           TCP/IP 协议栈（OSI 参考模型）       │
├─────────────────────────────────────────────┤
│  7️⃣ 应用层 (Application)    HTTP, FTP, SMTP │
│  6️⃣ 表示层 (Presentation)    TLS/SSL, JSON   │
│  5️⃣ 会话层 (Session)         NetBIOS, RPC    │
├─────────────────────────────────────────────┤
│  4️⃣ 传输层 (Transport)       TCP, UDP        │
├─────────────────────────────────────────────┤
│  3️⃣ 网络层 (Network)         IP, ICMP,路由   │
├─────────────────────────────────────────────┤
│  2️⃣ 数据链路层 (Data Link)   Ethernet, WiFi  │
│  1️⃣ 物理层 (Physical)        光纤, 电缆, 无线电│
└─────────────────────────────────────────────┘
```

**TCP（Transmission Control Protocol，传输控制协议）**：
- 面向连接的协议，类似于打电话——必须先接通，才能通话
- 提供可靠传输，数据包丢了会重发，顺序乱了会帮你排好
- 确保"数据一定送到，送到的数据一定是对的"
- 速度相对较慢，但稳如老狗

**UDP（User Datagram Protocol，用户数据报协议）**：
- 无连接的协议，类似于发快递——把包裹往快递柜一扔，就不管了
- 不保证可靠传输，可能丢包，可能乱序
- 速度飞快，适合实时性要求高的场景（如视频通话、游戏）
- 简单粗暴，但也因此开销小

**IP（Internet Protocol，互联网协议）**：
- 负责给每个设备分配一个唯一的地址（IP 地址）
- 就像你的家庭住址，快递员根据地址找上门
- IPv4 地址已经快用完了（42 亿个），所以现在有了 IPv6（几乎无限多）

> 💡 **小知识**：为什么 TCP 比 UDP 慢？因为 TCP 要先"三次握手"建立连接，传输完还要"四次挥手"断开连接，就像打电话要先问候"你好啊"，挂断前要说"再见"。UDP 呢？直接开炮，打完就跑，完全不管对方收到没有。

---

### 32.1.2 HTTP / HTTPS 协议详解

**HTTP（HyperText Transfer Protocol，超文本传输协议）** 是 Web 的根基。你平时上网浏览网页，就是浏览器和服务器之间用 HTTP "对话"。

#### HTTP 请求方法

| 方法 | 含义 | 典型用途 |
|------|------|---------|
| GET | 获取资源 | 浏览网页、获取数据 |
| POST | 提交数据 | 登录、注册、提交表单 |
| PUT | 更新/替换资源 | 更新用户信息 |
| DELETE | 删除资源 | 删除帖子 |
| PATCH | 部分更新 | 修改用户名 |
| HEAD | 获取头部信息 | 检查资源是否存在 |

#### HTTP 状态码

状态码是服务器给浏览器的"回复短信"：

| 状态码 | 含义 | 例子 |
|--------|------|------|
| 1xx | 信息性 | 100 Continue |
| 2xx | 成功 | 200 OK, 201 Created |
| 3xx | 重定向 | 301 永久移动, 302 临时移动 |
| 4xx | 客户端错误 | 404 Not Found, 403 Forbidden |
| 5xx | 服务器错误 | 500 Internal Server Error, 503 Service Unavailable |

> 💡 **谐音梗记忆法**：404——"四零四"，找不到就是"死啦死啦"找不到！500——服务器脑子"五百"年不转一次，出错了！

#### HTTP 请求和响应结构

```
# HTTP 请求格式
请求方法  URL  HTTP版本
Host: example.com
Accept: text/html
...其他头部...

# 请求体（POST/PUT时才有）

# HTTP 响应格式
HTTP版本  状态码  状态描述
Content-Type: text/html
Content-Length: 1234
...其他头部...

# 响应体（HTML/JSON等内容）
```

#### HTTPS 是什么？

**HTTPS = HTTP + TLS/SSL**，简单说就是加密版的 HTTP。

为什么要加密？因为在网络上传输的数据，就像明信片一样中途可以被任何人看到。想象一下，你在网上购物输入信用卡密码，如果没有加密，黑客在中途一拦截——完蛋，密码泄露！

HTTPS 通过**TLS（Transport Layer Security）**协议给数据加密，就像把明信片装进密封的信封里，只有收信人才能打开。

```
┌─────────────────────────────────────────┐
│            HTTPS 工作原理               │
│                                         │
│   客户端                              服务器  │
│     │                                   │  │
│     │  1. 发起 HTTPS 请求                │  │
│     │ ────────────────────────────────> │  │
│     │                                   │  │
│     │  2. 发送证书（包含公钥）            │  │
│     │ <─────────────────────────────── │  │
│     │                                   │  │
│     │  3. 验证证书 + 生成会话密钥         │  │
│     │ ────────────────────────────────> │  │
│     │                                   │  │
│     │  4. 用会话密钥加密通信              │  │
│     │ <═══════════════════════════════> │  │
│     │         加密通道建立！             │  │
└─────────────────────────────────────────┘
```

---

### 32.1.3 WebSocket

**WebSocket** 是一种让服务器能主动给客户端发消息的技术。

传统的 HTTP 是"请求-响应"模式：客户端不主动，服务器不能随便给客户端发消息。就像你点外卖，你得不断打电话问"我的外卖到哪了？"——累不累？

WebSocket 就像建立了一个"热线电话"，一旦连接建立，双方可以随时互相发消息。实时聊天、在线游戏、股票行情推送都用它。

```
┌─────────────────────────────────────────────┐
│         HTTP vs WebSocket 对比              │
├─────────────────────────────────────────────┤
│  HTTP                                       │
│  客户端 ──请求──> 服务器                     │
│  客户端 <──响应── 服务器                     │
│  （必须客户端先开口）                         │
├─────────────────────────────────────────────┤
│  WebSocket                                  │
│  客户端 ══连接建立══> 服务器                 │
│  客户端 <──随时发消息── 服务器               │
│  客户端 ──随时发消息──> 服务器               │
│  （双向通道，平等对话）                       │
└─────────────────────────────────────────────┘
```

WebSocket 的握手过程基于 HTTP：

```python
# 客户端发起握手（ Upgrade 头部表示要升级协议）
"""
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
"""

# 服务器响应
"""
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
"""
```

---

## 32.2 Socket 编程

终于到正题了！**Socket（套接字）** 是网络编程的核心。你可以把 Socket 想象成"网络插头"——插上它，你的程序就能和其他程序"通电"了。

Python 的 `socket` 模块是标准库，无需安装，直接 `import socket` 就能用。

### 32.2.1 TCP Socket（服务器 / 客户端）

#### TCP 服务器

```python
import socket

# 创建一个 TCP socket
# socket.AF_INET 表示 IPv4，socket.SOCK_STREAM 表示 TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定到地址和端口
# '' 表示监听所有可用网络接口，8080 是端口号
server_socket.bind(('', 8080))

# 开始监听，参数表示最大排队连接数
server_socket.listen(5)

print("🖥️  TCP 服务器启动，监听 8080 端口...")

while True:
    # 接受客户端连接（阻塞等待）
    # 返回一个新的 socket（用于和该客户端通信）和客户端地址
    client_socket, client_addr = server_socket.accept()
    print(f"📞 有客户端连接：{client_addr}")
    
    # 接收客户端数据（最多 1024 字节）
    data = client_socket.recv(1024)
    print(f"📩 收到数据：{data.decode('utf-8')}")
    
    # 发送响应
    response = "你好，客户端！我是服务器！👋"
    client_socket.send(response.encode('utf-8'))
    
    # 关闭与客户端的连接
    client_socket.close()
    print(f"🔌 已关闭与 {client_addr} 的连接")
```

> 💡 **形象理解**：TCP 服务器就像一个火锅店老板，`bind` 是租下店面，`listen` 是挂上"营业中"的牌子，`accept` 是等待客人进门。来了客人就开一个包间（新的 socket）专门服务他，原来的 socket 继续在门口等下一位。

#### TCP 客户端

```python
import socket

# 创建 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器（注意：这里客户端也需要指定地址和端口吗？
# 不需要！客户端的端口是系统自动分配的"临时工位"）
server_addr = ('127.0.0.1', 8080)  # 127.0.0.1 是本机地址（localhost）
client_socket.connect(server_addr)

print("🔗 已连接到服务器")

# 发送数据
message = "服务器你好，我是客户端！"
client_socket.send(message.encode('utf-8'))
print(f"📤 已发送：{message}")

# 接收响应
response = client_socket.recv(1024)
print(f"📥 收到响应：{response.decode('utf-8')}")

# 关闭连接
client_socket.close()
print("🔌 连接已关闭")
```

**运行效果**：

```
# 先运行服务器
$ python tcp_server.py
🖥️  TCP 服务器启动，监听 8080 端口...
📞 有客户端连接：('127.0.0.1', 54321)
📩 收到数据：服务器你好，我是客户端！
🔌 已关闭与 ('127.0.0.1', 54321) 的连接

# 再运行客户端
$ python tcp_client.py
🔗 已连接到服务器
📤 已发送：服务器你好，我是客户端！
📥 收到响应：你好，客户端！我是服务器！👋
🔌 连接已关闭
```

> ⚠️ **注意**：服务器需要先运行，等待客户端来连接。如果先运行客户端，它会报错"连接被拒绝"，因为找不到服务器。

### 32.2.2 UDP Socket

UDP 编程比 TCP 更简单，因为 UDP 是"无连接"的，不需要三次握手，也不需要关闭连接。

```python
import socket

# 创建 UDP socket
# SOCK_DGRAM 表示数据报模式（UDP）
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定地址
udp_server.bind(('', 8080))

print("📡 UDP 服务器启动，监听 8080 端口...")

while True:
    # recvfrom 返回数据和数据来源的地址
    data, client_addr = udp_server.recvfrom(1024)
    print(f"📩 收到来自 {client_addr} 的数据：{data.decode('utf-8')}")
    
    # 发送响应（不需要先 accept）
    response = f"收到！你的消息是：{data.decode('utf-8')}"
    udp_server.sendto(response.encode('utf-8'), client_addr)
```

```python
import socket

# 创建 UDP socket
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_addr = ('127.0.0.1', 8080)

# 直接发送数据，不需要 connect！
message = "UDP 测试消息"
udp_client.sendto(message.encode('utf-8'), server_addr)

# 接收响应
response, server_addr = udp_client.recvfrom(1024)
print(f"📥 收到响应：{response.decode('utf-8')}")

udp_client.close()
```

> 🧪 **UDP vs TCP 对比实验**：
> - TCP 是"打电话"：必须先接通，双方同时在线
> - UDP 是"发短信"：发出去就不管了，对方可能没收到
> - TCP 适合：网页访问、文件传输、登录认证（要可靠）
> - UDP 适合：视频通话、游戏、直播（偶尔丢一帧无所谓）

### 32.2.3 聊天程序实战

好，综合运用一下，写一个**带图形界面**的聊天程序！当然，这里先演示**命令行版本**，GUI 版本只需要替换输入输出部分即可。

```python
"""
UDP 多人聊天室
原理：所有用户加入同一个广播组，发的消息大家都能看到
"""

import socket
import threading

# 配置
BROADCAST_IP = '192.168.255.255'  # 局域网广播地址（需要根据实际网络修改）
PORT = 5000
BUFFER_SIZE = 1024

class ChatRoom:
    def __init__(self, username):
        self.username = username
        # 创建 UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 设置允许广播
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', PORT))
        self.running = True
    
    def send_message(self, message):
        """发送消息到聊天室"""
        full_message = f"[{self.username}]: {message}"
        self.sock.sendto(full_message.encode('utf-8'), (BROADCAST_IP, PORT))
    
    def receive_messages(self):
        """接收聊天室消息（在独立线程中运行）"""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                message = data.decode('utf-8')
                # 打印消息（排除自己发的，避免刷屏）
                if not message.startswith(f"[{self.username}]"):
                    print(f"\r📢 {message}\n[{self.username}]: ", end='')
            except Exception:
                pass
    
    def start(self):
        """启动聊天"""
        # 启动接收线程
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        print(f"🚀 进入聊天室（广播地址: {BROADCAST_IP}:{PORT}）")
        print("开始聊天吧！输入消息后按回车发送，输入 'quit' 退出\n")
        
        try:
            while True:
                message = input(f"[{self.username}]: ")
                if message.lower() == 'quit':
                    self.send_message("👋 离开了聊天室")
                    break
                self.send_message(message)
        except KeyboardInterrupt:
            print("\n⚠️ 被中断，退出聊天室")
        finally:
            self.running = False
            self.sock.close()
            print("🔌 已断开连接")


# 使用示例
if __name__ == '__main__':
    username = input("请输入你的昵称：")
    chat_room = ChatRoom(username)
    chat_room.start()
```

> 💡 **聊天室原理**：每个参与者都加入同一个端口（5000），发送时使用广播地址。广播就像在教室里喊一声，所有人都能听到。接收线程在后台持续监听，有新消息就打印出来。

---

## 32.3 HTTP 客户端

### 32.3.1 requests 使用

`requests` 是 Python 最流行的 HTTP 客户端库，堪称"躺平式" HTTP 请求——用它写 HTTP 请求，就像呼吸一样简单。

```bash
# 安装 requests
pip install requests
```

#### GET 请求

```python
import requests

# 最简单的 GET 请求
response = requests.get('https://api.github.com/users/octocat')
print(response.status_code)  # 状态码：200 表示成功
print(response.json())  # 解析 JSON 响应

# 带参数的 GET 请求
params = {
    'page': 1,
    'per_page': 10,
    'q': 'python'
}
response = requests.get('https://api.github.com/search/repositories', params=params)
data = response.json()
print(f"找到 {data['total_count']} 个仓库")

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
}
response = requests.get('https://api.github.com/users/octocat', headers=headers)
print(response.headers['Content-Type'])  # application/json; charset=utf-8
```

#### POST 请求

```python
import requests

# POST 请求（提交表单数据）
data = {
    'username': 'test_user',
    'password': '123456'
}
response = requests.post('https://httpbin.org/post', data=data)
print(response.json())

# POST JSON 数据
json_data = {
    'title': '我的博客文章',
    'content': '这是一篇关于 Python 网络编程的文章',
    'author': '小明'
}
response = requests.post('https://httpbin.org/post', json=json_data)
print(response.json())
```

#### 处理响应

```python
import requests

response = requests.get('https://httpbin.org/json')

# 常用属性
print(response.status_code)   # 状态码
print(response.headers)       # 响应头
print(response.text)          # 响应体（文本）
print(response.content)       # 响应体（字节）
print(response.json())        # JSON 解析

# 判断是否成功
if response.status_code == 200:
    data = response.json()
    print("请求成功！")
elif response.status_code == 404:
    print("资源不存在")
else:
    print(f"出错了，状态码：{response.status_code}")
```

> 💡 **httpbin.org** 是一个超好用的测试网站，它会把你发送的请求原封不动地返回来，特别适合调试 HTTP 请求。

### 32.3.2 httpx（同步 / 异步）

**httpx** 是一个现代化的 HTTP 客户端，支持同步和异步两种模式。如果你已经熟悉 `requests`，那 `httpx` 几乎可以无缝切换。

```bash
pip install httpx
```

#### 同步模式

```python
import httpx

# 同步 GET 请求（和 requests 几乎一样）
response = httpx.get('https://httpbin.org/json')
print(response.status_code)
print(response.json())

# 带参数和头部
headers = {'Authorization': 'Bearer token123'}
params = {'page': 1, 'limit': 10}
response = httpx.get('https://httpbin.org/get', headers=headers, params=params)
print(response.json())

# POST 请求
response = httpx.post('https://httpbin.org/post', json={'key': 'value'})
print(response.json())
```

#### 异步模式

```python
import httpx
import asyncio

async def fetch_data():
    """异步获取多个网页（并发执行，比串行快很多）"""
    
    async with httpx.AsyncClient() as client:
        # 并发请求多个 URL
        urls = [
            'https://httpbin.org/delay/1',  # 故意延迟 1 秒
            'https://httpbin.org/delay/2',  # 故意延迟 2 秒
            'https://httpbin.org/get',
        ]
        
        # 使用 asyncio.gather 并发执行
        # 如果串行执行需要 1+2+0.1=3.1 秒，并发只需要 max(1,2,0.1)=2 秒
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        for resp in responses:
            print(f"{resp.url}: {resp.status_code}")

# 运行异步函数
asyncio.run(fetch_data())
```

> 🚀 **异步的优势**：想象你要下载 100 张图片，每张图片下载需要 1 秒。如果用同步方式，总共需要 100 秒。但如果用异步并发，只需要大约 1 秒（假设网络够快）。这就是异步编程的威力！

### 32.3.3 文件上传与下载

#### 文件下载

```python
import requests

# 最简单的文件下载
url = 'https://www.python.org/static/img/python-logo.png'
response = requests.get(url, stream=True)

with open('python-logo.png', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print("✅ 下载完成！")

# 带进度显示的下载
def download_with_progress(url, filename):
    """带进度显示的文件下载"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('Content-Length', 0))
    
    downloaded = 0
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size:
                percent = (downloaded / total_size) * 100
                print(f"\r📥 下载进度：{percent:.1f}%", end='')
    
    print(f"\n✅ {filename} 下载完成！")

# 使用示例
download_with_progress(
    'https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe',
    'python-installer.exe'
)
```

#### 文件上传

```python
import requests

# 上传文件
with open('my-document.pdf', 'rb') as f:
    files = {'file': ('document.pdf', f, 'application/pdf')}
    response = requests.post('https://httpbin.org/post', files=files)
    print(response.json())

# 上传多个文件
with open('image1.png', 'rb') as f1, open('image2.png', 'rb') as f2:
    files = [
        ('images', ('image1.png', f1, 'image/png')),
        ('images', ('image2.png', f2, 'image/png')),
    ]
    response = requests.post('https://httpbin.org/post', files=files)
    print(response.json())

# 上传文件 + 附带表单数据
with open('avatar.jpg', 'rb') as f:
    files = {'avatar': ('my-avatar.jpg', f, 'image/jpeg')}
    data = {'username': '小明', 'bio': 'Python爱好者'}
    response = requests.post('https://httpbin.org/post', files=files, data=data)
    print(response.json())
```

> 💡 **stream=True 的作用**：如果不加 `stream=True`，`requests` 会先把整个文件下载到内存，然后再写入磁盘。对于大文件来说，这可能导致内存爆满。加了 `stream=True` 后，`iter_content` 会一块一块地读取和写入，内存占用稳定。

---

## 32.4 API 设计

### 32.4.1 RESTful API 设计原则

**REST（Representational State Transfer，表述性状态转移）** 是一种 API 设计风格。遵循 REST 原则设计的 API 就是"RESTful API"。

> 📖 **历史小知识**：REST 是 Roy Fielding 在 2000 年的博士论文中提出的。这位大佬也是 HTTP 协议的主要设计者之一。所以 REST 和 HTTP 有着天然的联系。

#### RESTful 六大原则

1. **客户端-服务器架构**：客户端负责 UI，服务器负责数据存储，职责分离
2. **无状态**：每个请求都包含所有必要信息，服务器不需要记住之前的请求
3. **可缓存**：响应可以被缓存，提高性能
4. **分层系统**：客户端不需要知道背后有多少层服务器
5. **统一接口**：所有资源通过统一的接口访问
6. **按需代码（可选）**：服务器可以向客户端发送可执行代码

#### RESTful URL 设计

```
# ❌ 不好的设计（RESTful 之前的"黑暗时代"）
GET /getUsers              # 动词+名词
GET /getUserById?id=1      # 动词+名词+参数
POST /createUser           # 动词+名词
POST /deleteUser?id=1      # 动词+名词

# ✅ 好的设计（RESTful 风格）
GET    /users              # 获取所有用户
GET    /users/1            # 获取 ID 为 1 的用户
POST   /users              # 创建新用户
PUT    /users/1            # 更新 ID 为 1 的用户（完整更新）
PATCH  /users/1            # 部分更新 ID 为 1 的用户
DELETE /users/1            # 删除 ID 为 1 的用户
```

> 🏠 **类比理解**：RESTful URL 就像"门牌号"，而旧的 API 风格像"打电话给某人让他帮你做某事"。比如你要找"住在朝阳区建国路 88 号的张三"，RESTful 会说"GET /residents/88/zhangsan"，而旧风格会说"GET /callPerson?person=zhangsan&address=88"。

#### RESTful 状态码使用

| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | OK | 成功获取/更新资源 |
| 201 | Created | 成功创建新资源 |
| 204 | No Content | 成功删除（无返回体） |
| 400 | Bad Request | 请求格式错误 |
| 401 | Unauthorized | 未认证（没登录） |
| 403 | Forbidden | 已认证但无权限 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

### 32.4.2 FastAPI / Flask API

Python 有很多 Web 框架可以快速搭建 API，这里介绍两个最流行的：**Flask**（轻量级）和 **FastAPI**（现代化、高性能）。

#### Flask：微框架，简单直接

```bash
pip install flask
```

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# 模拟数据库
users = [
    {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com'},
    {'id': 2, 'name': '李四', 'email': 'lisi@example.com'},
]
next_id = 3

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '欢迎使用用户管理 API',
        'endpoints': ['/users', '/users/<id>']
    })

@app.route('/users', methods=['GET'])
def get_users():
    """获取所有用户"""
    return jsonify({'users': users})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': '用户不存在'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """创建用户"""
    global next_id
    data = request.json
    
    new_user = {
        'id': next_id,
        'name': data.get('name'),
        'email': data.get('email')
    }
    users.append(new_user)
    next_id += 1
    
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户"""
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    data = request.json
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    """部分更新用户（仅更新提供的字段）"""
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    data = request.json
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    users = [u for u in users if u['id'] != user_id]
    return '', 204

if __name__ == '__main__':
    print("🚀 Flask API 服务器启动：http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
```

#### FastAPI：现代化、高性能、自动文档

```bash
pip install fastapi uvicorn
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="用户管理 API", version="1.0.0")

# Pydantic 模型（自动验证数据）
class User(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# 模拟数据库
users_db = {
    1: {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com'},
    2: {'id': 2, 'name': '李四', 'email': 'lisi@example.com'},
}
next_id = 3

@app.get('/')
def index():
    """首页"""
    return {'message': '欢迎使用 FastAPI 用户管理 API'}

@app.get('/users')
def get_users():
    """获取所有用户"""
    return {'users': list(users_db.values())}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    """获取单个用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail='用户不存在')
    return users_db[user_id]

@app.post('/users', status_code=201)
def create_user(user: User):
    """创建用户"""
    global next_id
    new_user = {'id': next_id, **user.model_dump()}
    users_db[next_id] = new_user
    next_id += 1
    return new_user

@app.put('/users/{user_id}')
def update_user(user_id: int, user: UserUpdate):
    """更新用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail='用户不存在')
    
    db_user = users_db[user_id]
    update_data = user.model_dump(exclude_unset=True)
    db_user.update(update_data)
    return db_user

@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    """删除用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail='用户不存在')
    del users_db[user_id]
    return {'message': '用户已删除'}

if __name__ == '__main__':
    print("🚀 FastAPI 服务器启动：http://127.0.0.1:8000")
    print("📖 API 文档：http://127.0.0.1:8000/docs")
    uvicorn.run(app, host='127.0.0.1', port=8000)
```

> 🎉 **FastAPI 的一大亮点**：运行后自动生成交互式 API 文档！访问 `http://127.0.0.1:8000/docs` 可以看到 Swagger UI，可以直接在网页上测试每个 API 接口，简直是开发者的福音！

### 32.4.3 API 认证（JWT / OAuth2）

#### JWT（JSON Web Token）

**JWT** 是一种开放标准，用于在各方之间安全地传输信息。最常见的场景就是用户登录——服务器验证用户名密码后，生成一个 JWT 返回给客户端，客户端后续请求带着这个 token 就行了。

JWT 的结构：

```
┌─────────────────────────────────────────────────────────┐
│                     JWT 组成                             │
│                                                         │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                │
│  ←─── Header（头部）──→                                 │
│                                                         │
│  eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.       │
│  ←────────── Payload（载荷）─────────→                  │
│                                                         │
│  SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c          │
│  ←──────────── Signature（签名）──────────→            │
└─────────────────────────────────────────────────────────┘
```

```python
import jwt
import datetime

# JWT 配置
SECRET_KEY = '你的超级密钥，别让人知道！'  # 生产环境要放环境变量
ALGORITHM = 'HS256'  # HMAC SHA-256

def create_token(user_id: int, username: str) -> str:
    """生成 JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # 24 小时过期
        'iat': datetime.datetime.utcnow()  # 签发时间
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token 已过期')
    except jwt.InvalidTokenError:
        raise Exception('无效的 Token')

# 使用示例
token = create_token(user_id=1, username='小明')
print(f"生成的 Token：{token}")

try:
    payload = verify_token(token)
    print(f"Token 验证成功！用户信息：{payload}")
except Exception as e:
    print(f"Token 验证失败：{e}")
```

#### Flask + JWT 实现登录认证

```python
from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = 'secret_key_123'
ALGORITHM = 'HS256'

# 模拟用户数据库（实际项目中要连接真实数据库）
users = {
    'admin': {'password': 'password123', 'role': 'admin'},
    'user': {'password': 'user456', 'role': 'user'}
}

@app.route('/login', methods=['POST'])
def login():
    """登录接口"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 验证用户
    if username not in users or users[username]['password'] != password:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 生成 token
    token = jwt.encode({
        'username': username,
        'role': users[username]['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return jsonify({'token': token})

@app.route('/protected', methods=['GET'])
def protected():
    """受保护的接口，需要携带有效 token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': '未提供认证信息'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return jsonify({
            'message': f'欢迎，{payload["username"]}！',
            'role': payload['role']
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token 已过期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '无效的 Token'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### OAuth2 简介

**OAuth2** 是一种授权框架，让用户可以授权第三方应用访问自己在某个服务上的数据，而不需要提供用户名和密码。

> 🌰 **OAuth2 生活例子**：你想用一个"照片美化"App 处理你存在 Google Photos 里的照片。传统方式是你把 Google 账号密码给这个 App——但这太危险了，它能看到你 Google 账号的所有东西。OAuth2 的做法是：照片 App 跳转到 Google，询问"用户愿意让你访问他的照片吗？"用户点击"允许"，Google 就给照片 App 一个"访问令牌"，这个令牌只能访问照片，不能访问其他东西。

```
┌──────────────────────────────────────────────────────────────┐
│                        OAuth2 流程                            │
│                                                              │
│   用户        照片App           Google                         │
│    │            │                │                            │
│    │  1. 点击"用Google登录"    │                              │
│    │ ─────────> │                │                              │
│    │            │  2. 跳转登录页  │                              │
│    │ ─────────────────────────> │                              │
│    │            │                │                              │
│    │  3. 输入用户名密码，点击"允许"│                             │
│    │ ─────────────────────────> │                              │
│    │            │                │                              │
│    │  4. 返回授权码给照片App     │                              │
│    │ <────────────────────────  │                              │
│    │            │                │                              │
│    │  5. 照片App用授权码换token  │                              │
│    │            │ ──────────────> │                              │
│    │            │                │                              │
│    │  6. 返回访问令牌（只能访问照片）│                             │
│    │            │ <────────────── │                              │
│    │            │                │                              │
│    │  7. 用token获取照片         │                              │
│    │            │ ──────────────> │                              │
│    │            │ <────────────── │                              │
│    │  8. 显示照片（App不知道密码）│                              │
│    │ <──────────────────────────  │                              │
└──────────────────────────────────────────────────────────────┘
```

OAuth2 有四种授权模式：

1. **授权码模式（Authorization Code）**：最安全，适合有后端服务器的应用
2. **隐式授权模式（Implicit）**：适合纯前端应用（已不推荐）
3. **密码凭证模式（Resource Owner Password Credentials）**：直接用用户名密码换 token，适合受信任的应用
4. **客户端凭证模式（Client Credentials）**：客户端以自己的身份访问，不需要用户授权

> 💡 **实战建议**：如果只是为自己的应用添加认证，JWT 通常就够了。如果你要做"用 Google/微信登录"这种第三方登录，那就需要 OAuth2。可以使用 `authlib` 库在 Python 中实现 OAuth2。

---

## 本章小结

恭喜你！你已经完成了网络编程的完整旅程！🎉

本章涵盖的核心知识点：

| 知识点 | 关键内容 |
|--------|---------|
| **TCP/IP 协议栈** | 了解网络分层的思想，TCP（可靠连接）vs UDP（无连接高速）|
| **HTTP/HTTPS** | 请求方法（GET/POST/PUT/DELETE）、状态码、HTTPS 加密原理 |
| **WebSocket** | 全双工通信，服务器可以主动推送消息 |
| **Socket 编程** | Python 标准库 `socket`，TCP 服务器/客户端，UDP 编程 |
| **聊天程序实战** | UDP 广播实现多人聊天室 |
| **HTTP 客户端** | `requests` 库（躺平式 HTTP），`httpx`（同步+异步）|
| **文件上传/下载** | 流式处理大文件，`stream=True` 避免内存爆炸 |
| **RESTful API** | URL 设计原则，资源导向，无状态 |
| **Flask / FastAPI** | Python Web 框架，快速搭建 API |
| **JWT 认证** | Token 机制，无状态认证 |
| **OAuth2** | 第三方授权框架，"用XX登录"的核心技术 |

### 进阶学习建议

- 想深入网络底层？可以研究 `asyncio` 模块和 Python 的异步编程
- 想写高性能服务器？可以试试 `uvicorn`、`gunicorn` 等 ASGI/WSGI 服务器
- 想爬取网页？可以学习 `scrapy` 框架
- 想处理网络抓包？可以学习 `scapy` 库

### 趣味小挑战

1. 改造 TCP 聊天程序，支持多人聊天室（用 `threading` 处理多个客户端）
2. 用 FastAPI 写一个待办事项 API，支持增删改查和 JWT 认证
3. 实现一个带进度条的文件下载器，支持断点续传

---

> 📚 **继续阅读**：下一章我们将探索 **Python 与数据库的交互**，让你的数据能够持久保存！敬请期待！
