+++
title = "第42章 网络编程——让程序"上网冲浪""
weight = 420
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第42章 网络编程——让程序"上网冲浪"

你知道吗？当你刷着微博、聊着微信、看着视频的时候，背后是一大堆程序员写的大量网络代码在疯狂运转。这些代码每天处理着数以亿计的数据包，把你的"想吃火锅"这条消息从你的手机传递到你朋友的手机上。而这一切的起点，可能就是今天我们要学的——**网络编程**（Network Programming）。

本章我们将用C++来实现真正的网络通信！从最基础的socket API，到高大上的ASIO异步框架，再到HTTP协议的实战操作。读完这章，你也能写出像模像样的网络程序了。准备好了吗？让我们开始这场"冲浪"之旅！

---

## 42.1 网络编程基础概念

在开始敲代码之前，我们得先搞清楚一些基本概念。就像盖房子之前要了解砖头和水泥一样，网络编程也有一些"行话"需要掌握。

### 客户端与服务端：谁先开口说话？

网络通信分为两个角色：**服务端**（Server）和**客户端**（Client）。

**服务端**：也叫服务器，是那个"守株待兔"的角色。它先启动，绑定一个端口，然后坐在那里等着有人来敲门。就像开店的老板，先开店门，等着顾客上门。

**客户端**：是主动出击的那一方。它知道服务端的地址（IP和端口），然后主动去连接。就像顾客，主动走到店里消费。

```
  客户端                                    服务端
    |                                        |
    |  ── connect() ──▶  请求连接           |
    |                                        |
    |         ◀───  accept() ──              |
    |                                        |
    |  ◀═══ 双向通信 (read/write) ═══▶        |
    |                                        |
    |  ── close() ──▶  关闭连接             |
    |                                        |
```

### TCP vs UDP：两种不同的"快递方式"

**TCP**（Transmission Control Protocol，传输控制协议）就像有保障的顺丰快递：
- **面向连接**：先建立连接，再传输数据（打电话前先拨号）
- **可靠传输**：丢包了会重发，收到了会确认
- **保证顺序**：先发的数据先到
- **流量控制**：不会一次性发太多把你淹没

**UDP**（User Datagram Protocol，用户数据报协议）就像不保证送达的平信：
- **无连接**：直接发数据，不需要先握手
- **不可靠**：可能丢包，可能乱序
- **轻量级**：头部小，开销低，速度快

| 特性 | TCP | UDP |
|------|-----|-----|
| 连接方式 | 面向连接 | 无连接 |
| 可靠性 | 可靠 | 不可靠 |
| 顺序性 | 保证顺序 | 不保证 |
| 速度 | 较慢 | 快 |
| 头部大小 | 20-60字节 | 8字节 |
| 使用场景 | 文件传输、网页、邮件 | 视频通话、DNS、游戏 |

> **小知识**：你上网看网页用的是TCP（HTTP/HTTPS），你视频通话大概率用的是UDP（RTP）。没有绝对的优劣，只有合适的场景。

### IP地址与端口：网络世界的"门牌号"

**IP地址**是设备的"身份证号"，用于在网络上唯一标识一台设备。IPv4地址长这样：`192.168.1.100`，IPv6更长：`2001:0db8:85a3:0000:0000:8a2e:0370:7334`。

**端口号**是设备上的"房间号"，用于区分同一设备上的不同服务。一台电脑可以运行多个网络服务，靠端口号来区分。端口号范围是0-65535，其中0-1023是系统端口（如80是HTTP，443是HTTPS），我们程序一般用10000以上的端口。

### socket：网络编程的主角

**socket**（套接字）是网络编程的核心概念，可以理解为网络的"插座"。程序员通过socket来发送和接收数据，就像通过插座来使用电器一样。

在Linux/Unix系统中，一切皆文件，socket也是一个文件描述符。在Windows中，socket是一个独立的句柄类型。

```cpp
/*
 * socket 创建流程（TCP服务端）
 *
 * 1. socket()      创建socket
 * 2. bind()        绑定地址和端口
 * 3. listen()      监听连接
 * 4. accept()      接受连接
 * 5. read/write    数据通信
 * 6. close()       关闭连接
 */

#include <iostream>
#include <cstring>

// 不同平台的头文件
#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib")
    typedef int socklen_t;
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    typedef int SOCKET;
    #define INVALID_SOCKET (-1)
    #define SOCKET_ERROR (-1)
#endif

int main() {
    std::cout << "=== 网络编程基础概念演示 ===" << std::endl;
    std::cout << std::endl;

#ifdef _WIN32
    // Windows下需要初始化Winsock
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup 失败！" << std::endl;
        return 1;
    }
    std::cout << "Winsock 初始化成功！" << std::endl;
#endif

    std::cout << std::endl;
    std::cout << "TCP socket 创建流程：" << std::endl;
    std::cout << "  1. socket()  - 创建一个socket（插座）" << std::endl;
    std::cout << "  2. bind()    - 把socket绑定到地址和端口（插上插座）" << std::endl;
    std::cout << "  3. listen()  - 开始监听（开门营业）" << std::endl;
    std::cout << "  4. accept()  - 等待客户端连接（接待顾客）" << std::endl;
    std::cout << "  5. recv/send - 数据通信（买卖东西）" << std::endl;
    std::cout << "  6. closesocket() - 关闭连接（送客关门）" << std::endl;

    std::cout << std::endl;
    std::cout << "UDP socket 创建流程：" << std::endl;
    std::cout << "  1. socket()  - 创建一个socket" << std::endl;
    std::cout << "  2. bind()    - 绑定地址和端口" << std::endl;
    std::cout << "  3. recvfrom/sendto - 数据通信（直接喊话）" << std::endl;
    std::cout << "  4. closesocket() - 关闭socket" << std::endl;

    std::cout << std::endl;
    std::cout << "注意：UDP不需要listen和accept，因为它是无连接的！" << std::endl;
    std::cout << "      就像广播，谁都能发，不用先握手。" << std::endl;

#ifdef _WIN32
    WSACleanup();
#endif

    return 0;
}
```

> **小知识**：为什么Windows下需要`WSAStartup()`？因为Windows觉得网络这么重要的功能，应该由应用程序主动申请才能用，不像Linux那样"生来就有"。这大概就是Windows的"安全"哲学吧——默认不给你，用的时候再说。

---

## 42.2 平台抽象层：让代码跨平台

网络编程有一个令人头疼的问题：不同操作系统的API不一样！Linux用`close()`，Windows用`closesocket()`；Linux的错误码是负数，Windows是特定的错误码。

为了让代码看起来整洁，我们先写一个跨平台的封装层。这就像翻译员，把不同语言翻译成统一的一种。

```cpp
/*
 * platform_socket.h
 * 跨平台socket封装层
 *
 * 统一不同操作系统的差异，让代码可以在Windows和Linux上同时运行
 */

#ifndef PLATFORM_SOCKET_H
#define PLATFORM_SOCKET_H

#ifdef _WIN32
    #define WIN32_LEAN_AND_MEAN
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib")
    typedef int socklen_t;
    #define SET_NONBLOCKING(sock) { u_long mode = 1; ioctlsocket(sock, FIONBIO, &mode); }
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <errno.h>
    typedef int SOCKET;
    #define INVALID_SOCKET (-1)
    #define SOCKET_ERROR (-1)
    #define closesocket close
    #define SET_NONBLOCKING(sock) do { int flags = fcntl(sock, F_GETFL, 0); fcntl(sock, F_SETFL, flags | O_NONBLOCK); } while(0)
#endif

// 错误处理宏
#ifdef _WIN32
    #define SOCKET_GET_ERROR() (WSAGetLastError())
#else
    #define SOCKET_GET_ERROR() (errno)
#endif

// 初始化/清理（Windows需要，Linux是空操作）
inline int socket_init() {
#ifdef _WIN32
    WSADATA wsaData;
    return WSAStartup(MAKEWORD(2, 2), &wsaData);
#else
    return 0; // Linux不需要初始化
#endif
}

inline void socket_cleanup() {
#ifdef _WIN32
    WSACleanup();
#endif
}

// 创建TCP socket
inline SOCKET create_tcp_socket() {
    return socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
}

// 创建UDP socket
inline SOCKET create_udp_socket() {
    return socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
}

// 设置地址结构
inline void set_address(struct sockaddr_in* addr, const char* ip, unsigned short port) {
    memset(addr, 0, sizeof(struct sockaddr_in));
    addr->sin_family = AF_INET;
    addr->sin_port = htons(port);
    if (ip == nullptr || strcmp(ip, "0.0.0.0") == 0 || strcmp(ip, "") == 0) {
        addr->sin_addr.s_addr = INADDR_ANY; // 监听所有网卡
    } else {
        inet_pton(AF_INET, ip, &addr->sin_addr);
    }
}

// 关闭socket
inline void close_socket(SOCKET sock) {
    if (sock != INVALID_SOCKET) {
#ifdef _WIN32
        shutdown(sock, SD_BOTH);
        closesocket(sock);
#else
        shutdown(sock, SHUT_RDWR);
        close(sock);
#endif
    }
}

#endif // PLATFORM_SOCKET_H
```

这个封装层统一了Windows和Linux的socket API，后续代码就可以直接使用了。程序员偷懒是进步的动力！

---

## 42.3 TCP服务端：我是"网红店老板"

现在我们来实现一个TCP服务端！服务端的角色就像一个网红店老板：先开店（bind+listen），等待顾客（accept），然后服务顾客（recv+send）。

### 42.3.1 基础TCP服务端

让我们先写一个最简单版本的TCP服务端，它能接收客户端的连接，并回显（echo）客户端发送的消息。

```cpp
/*
 * tcp_server_basic.cpp
 * 基础TCP服务端 - 回显服务器
 *
 * 功能：接收客户端消息，然后原样发回去
 * 这就像复读机，你说啥它说啥（但至少是个能聊天的复读机）
 *
 * 编译（Linux/Mac）: g++ -std=c++17 -o tcp_server tcp_server_basic.cpp
 * 编译（Windows）:  cl /EHsc /std:c++17 tcp_server_basic.cpp ws2_32.lib
 * 运行: ./tcp_server
 * 测试: telnet localhost 8888  或  nc localhost 8888
 */

#include <iostream>
#include <cstring>
#include <vector>
#include "platform_socket.h"

// 服务端配置
const char* SERVER_IP = "0.0.0.0";   // 监听所有网络接口
const int SERVER_PORT = 8888;        // 端口号（选个顺口的）
const int BUFFER_SIZE = 4096;        // 缓冲区大小

int main() {
    std::cout << "=== TCP回显服务器 ===" << std::endl;
    std::cout << "监听地址: " << SERVER_IP << ":" << SERVER_PORT << std::endl;

    // 1. 初始化socket库（Windows需要，Linux跳过）
    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    // 2. 创建socket
    SOCKET serverSocket = create_tcp_socket();
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "socket创建失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        socket_cleanup();
        return 1;
    }
    std::cout << "socket创建成功！" << std::endl;

    // 3. 设置socket选项（地址重用，避免程序退出后端口被占用）
    int opt = 1;
#ifdef _WIN32
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif

    // 4. 绑定地址和端口
    struct sockaddr_in serverAddr;
    set_address(&serverAddr, SERVER_IP, SERVER_PORT);

    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "bind绑定失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        close_socket(serverSocket);
        socket_cleanup();
        return 1;
    }
    std::cout << "地址绑定成功！" << std::endl;

    // 5. 开始监听
    if (listen(serverSocket, 10) == SOCKET_ERROR) {
        std::cerr << "listen监听失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        close_socket(serverSocket);
        socket_cleanup();
        return 1;
    }
    std::cout << "开始监听连接请求..." << std::endl;
    std::cout << "等待客户端连接（按Ctrl+C退出）..." << std::endl;

    // 6. 接受连接并通信（主循环）
    while (true) {
        struct sockaddr_in clientAddr;
        socklen_t clientAddrLen = sizeof(clientAddr);

        // accept会阻塞，直到有客户端连接
        SOCKET clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);

        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "accept失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
            continue; // 继续等待下一个连接
        }

        // 获取客户端信息
        char clientIP[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, sizeof(clientIP));
        unsigned short clientPort = ntohs(clientAddr.sin_port);
        std::cout << "[" << clientIP << ":" << clientPort << "] 已连接！" << std::endl;

        // 与客户端通信
        char buffer[BUFFER_SIZE];
        while (true) {
            // 接收数据
            memset(buffer, 0, BUFFER_SIZE);
            int bytesRead = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);

            if (bytesRead > 0) {
                std::cout << "[" << clientIP << ":" << clientPort << "] 收到: " << buffer << std::endl;

                // 回显（Echo）: 把收到的消息发回去
                int bytesSent = send(clientSocket, buffer, bytesRead, 0);
                if (bytesSent == SOCKET_ERROR) {
                    std::cerr << "send失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
                    break;
                }
                std::cout << "[" << clientIP << ":" << clientPort << "] 回显: " << buffer << std::endl;

            } else if (bytesRead == 0) {
                std::cout << "[" << clientIP << ":" << clientPort << "] 断开连接" << std::endl;
                break;
            } else {
                std::cerr << "recv失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
                break;
            }
        }

        // 关闭与客户端的连接
        close_socket(clientSocket);
        std::cout << "[" << clientIP << ":" << clientPort << "] 连接已关闭" << std::endl;
    }

    // 清理（实际上不会执行到这里，因为是无限循环）
    close_socket(serverSocket);
    socket_cleanup();
    return 0;
}

/*
 * 测试方法：
 *
 * 1. 编译运行服务器
 *    $ g++ -std=c++17 -o tcp_server tcp_server_basic.cpp
 *    $ ./tcp_server
 *    === TCP回显服务器 ===
 *    监听地址: 0.0.0.0:8888
 *    socket创建成功！
 *    地址绑定成功！
 *    开始监听连接请求...
 *    等待客户端连接（按Ctrl+C退出）...
 *
 * 2. 另开一个终端，用nc连接
 *    $ nc localhost 8888
 *    Hello Server    <-- 你输入的
 *    Hello Server    <-- 服务器回显的
 *    你好世界
 *    你好世界
 *
 * 3. 服务器端会显示
 *    [127.0.0.1:54321] 已连接！
 *    [127.0.0.1:54321] 收到: Hello Server
 *    [127.0.0.1:54321] 发送: Hello Server
 *    [127.0.0.1:54321] 断开连接
 */
```

### 42.3.2 多线程TCP服务端：同时接待多位顾客

上面的服务器一次只能接待一个客户，这效率太低了！想象一下麦当劳只有一个收银台，排队得排到明年。

我们来写一个多线程版本，让每个客户端连接都由一个独立的线程处理。

```cpp
/*
 * tcp_server_multithread.cpp
 * 多线程TCP服务器
 *
 * 改进：每个客户端连接都由独立的线程处理
 * 就像麦当劳有多个收银台，同时接待多位顾客
 *
 * 编译: g++ -std=c++17 -pthread -o tcp_server_mt tcp_server_multithread.cpp
 */

#include <iostream>
#include <cstring>
#include <thread>
#include <vector>
#include <atomic>
#include "platform_socket.h"

const char* SERVER_IP = "0.0.0.0";
const int SERVER_PORT = 8888;
const int BUFFER_SIZE = 4096;
const int MAX_CLIENTS = 100; // 最大同时连接数

// 原子变量，用于生成唯一的客户端ID
std::atomic<int> g_client_id_counter(0);

// 处理单个客户端的函数
void handle_client(SOCKET clientSocket, struct sockaddr_in clientAddr) {
    int clientId = ++g_client_id_counter; // 获取客户端ID

    char clientIP[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, sizeof(clientIP));
    unsigned short clientPort = ntohs(clientAddr.sin_port);

    std::cout << "[客户端#" << clientId << "] " << clientIP << ":" << clientPort
              << " 已连接（线程ID: " << std::this_thread::get_id() << "）" << std::endl;

    char buffer[BUFFER_SIZE];

    // 简单的应用层协议：计算器服务
    // 客户端发送 "num1 op num2" 格式，如 "10 + 20"
    // 服务器返回结果
    while (true) {
        memset(buffer, 0, BUFFER_SIZE);
        int bytesRead = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);

        if (bytesRead <= 0) {
            if (bytesRead == 0) {
                std::cout << "[客户端#" << clientId << "] 连接正常关闭" << std::endl;
            } else {
                std::cerr << "[客户端#" << clientId << "] recv失败，错误码: "
                          << SOCKET_GET_ERROR() << std::endl;
            }
            break;
        }

        buffer[bytesRead] = '\0'; // 确保字符串以\0结尾
        std::cout << "[客户端#" << clientId << "] 收到: " << buffer << std::endl;

        // 解析并计算
        // 支持 + - * / 四种运算
        int a, b;
        char op;
        if (sscanf(buffer, "%d %c %d", &a, &op, &b) == 3) {
            double result = 0;
            bool valid = true;

            switch (op) {
                case '+': result = a + b; break;
                case '-': result = a - b; break;
                case '*': result = a * b; break;
                case '/':
                    if (b != 0) result = (double)a / b;
                    else valid = false;
                    break;
                default: valid = false;
            }

            if (valid) {
                if (op == '/' && result != (int)result) {
                    snprintf(buffer, BUFFER_SIZE, "%.2f", result);
                } else {
                    snprintf(buffer, BUFFER_SIZE, "%d", (int)result);
                }
            } else {
                snprintf(buffer, BUFFER_SIZE, "错误: 无效的运算");
            }
        } else if (strcmp(buffer, "quit") == 0 || strcmp(buffer, "exit") == 0) {
            snprintf(buffer, BUFFER_SIZE, "再见！欢迎下次光临！");
            send(clientSocket, buffer, strlen(buffer), 0);
            std::cout << "[客户端#" << clientId << "] 客户端请求退出" << std::endl;
            break;
        } else {
            snprintf(buffer, BUFFER_SIZE, "错误: 请发送格式如 '10 + 20' 的计算表达式，或 'quit' 退出");
        }

        // 发送响应
        int bytesSent = send(clientSocket, buffer, strlen(buffer), 0);
        if (bytesSent == SOCKET_ERROR) {
            std::cerr << "[客户端#" << clientId << "] send失败，错误码: "
                      << SOCKET_GET_ERROR() << std::endl;
            break;
        }
        std::cout << "[客户端#" << clientId << "] 发送: " << buffer << std::endl;
    }

    close_socket(clientSocket);
    std::cout << "[客户端#" << clientId << "] 连接已关闭" << std::endl;
}

int main() {
    std::cout << "=== 多线程TCP计算器服务器 ===" << std::endl;
    std::cout << "支持运算: 加(+), 减(-), 乘(*), 除(/)" << std::endl;
    std::cout << "示例: 发送 '10 + 20' 将返回 '30'" << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    SOCKET serverSocket = create_tcp_socket();
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "socket创建失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        socket_cleanup();
        return 1;
    }

    // 地址重用
    int opt = 1;
#ifdef _WIN32
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif

    struct sockaddr_in serverAddr;
    set_address(&serverAddr, SERVER_IP, SERVER_PORT);

    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "bind绑定失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        close_socket(serverSocket);
        socket_cleanup();
        return 1;
    }

    if (listen(serverSocket, MAX_CLIENTS) == SOCKET_ERROR) {
        std::cerr << "listen监听失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        close_socket(serverSocket);
        socket_cleanup();
        return 1;
    }

    std::cout << "服务器监听端口 " << SERVER_PORT << " ..." << std::endl;
    std::cout << "等待客户端连接..." << std::endl;

    // 存储所有客户端线程
    std::vector<std::thread> clientThreads;

    while (true) {
        struct sockaddr_in clientAddr;
        socklen_t clientAddrLen = sizeof(clientAddr);

        SOCKET clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "accept失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            continue;
        }

        // 为每个客户端创建一个新线程
        std::thread clientThread(handle_client, clientSocket, clientAddr);
        clientThread.detach(); // 分离线程，让它独立运行

        // 也可以用join代替detach，但那样就要等每个线程结束才能继续
        // clientThread.join();
    }

    close_socket(serverSocket);
    socket_cleanup();
    return 0;
}

/*
 * 测试：
 * $ nc localhost 8888
 * 10 + 20
 * 30
 * 100 * 5
 * 500
 * 10 / 3
 * 3.33
 * quit
 * 再见！欢迎下次光临！
 */
```

> **小提示**：`detach()`让线程在后台运行，主线程不用等待它结束。但这样就无法再管理这个线程了。对于服务器来说，detach是合适的，因为我们不需要等待每个客户端断开。但要注意：如果主线程先退出，detach的线程也会被强制终止，所以要确保主线程活得够久。

---

## 42.4 TCP客户端：主动出击的"顾客"

服务端写好了，现在来写客户端。客户端的角色是主动连接服务端，然后发送请求。

### 42.4.1 基础TCP客户端

```cpp
/*
 * tcp_client_basic.cpp
 * 基础TCP客户端
 *
 * 功能：连接到服务器，发送消息并接收响应
 * 这就像打电话，先拨号（connect），然后通话（send/recv）
 *
 * 编译: g++ -std=c++17 -o tcp_client tcp_client_basic.cpp
 * 运行: ./tcp_client
 */

#include <iostream>
#include <cstring>
#include "platform_socket.h"

const char* SERVER_IP = "127.0.0.1"; // 连接本地服务器
const int SERVER_PORT = 8888;
const int BUFFER_SIZE = 4096;

int main(int argc, char* argv[]) {
    // 可以通过命令行参数指定服务器地址和端口
    const char* serverIP = (argc > 1) ? argv[1] : SERVER_IP;
    int serverPort = (argc > 2) ? std::atoi(argv[2]) : SERVER_PORT;

    std::cout << "=== TCP客户端 ===" << std::endl;
    std::cout << "目标服务器: " << serverIP << ":" << serverPort << std::endl;

    // 初始化
    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    // 创建socket
    SOCKET clientSocket = create_tcp_socket();
    if (clientSocket == INVALID_SOCKET) {
        std::cerr << "socket创建失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        socket_cleanup();
        return 1;
    }
    std::cout << "socket创建成功！" << std::endl;

    // 连接服务器
    struct sockaddr_in serverAddr;
    set_address(&serverAddr, serverIP, (unsigned short)serverPort);

    std::cout << "正在连接服务器..." << std::endl;
    if (connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "连接失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        std::cerr << "请确保服务器已经启动！" << std::endl;
        close_socket(clientSocket);
        socket_cleanup();
        return 1;
    }
    std::cout << "连接成功！" << std::endl;

    // 通信循环
    char sendBuffer[BUFFER_SIZE];
    char recvBuffer[BUFFER_SIZE];

    std::cout << "\n输入消息发送给服务器（输入 'quit' 退出）：" << std::endl;

    while (true) {
        std::cout << "> ";
        std::cin.getline(sendBuffer, BUFFER_SIZE);

        // 发送数据
        int sendLen = strlen(sendBuffer);
        if (sendLen == 0) {
            continue; // 空行，跳过
        }

        int bytesSent = send(clientSocket, sendBuffer, sendLen, 0);
        if (bytesSent == SOCKET_ERROR) {
            std::cerr << "send失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
            break;
        }
        std::cout << "已发送: " << sendBuffer << std::endl;

        // 接收响应
        memset(recvBuffer, 0, BUFFER_SIZE);
        int bytesRecv = recv(clientSocket, recvBuffer, BUFFER_SIZE - 1, 0);

        if (bytesRecv > 0) {
            recvBuffer[bytesRecv] = '\0';
            std::cout << "服务器响应: " << recvBuffer << std::endl;
        } else if (bytesRecv == 0) {
            std::cout << "服务器关闭了连接" << std::endl;
            break;
        } else {
            std::cerr << "recv失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
            break;
        }

        // 检查是否退出
        if (strcmp(sendBuffer, "quit") == 0 || strcmp(sendBuffer, "exit") == 0) {
            std::cout << "主动退出连接" << std::endl;
            break;
        }
    }

    // 清理
    close_socket(clientSocket);
    socket_cleanup();

    std::cout << "客户端已退出" << std::endl;
    return 0;
}

/*
 * 测试步骤：
 *
 * 终端1: 启动服务器
 * $ ./tcp_server
 *
 * 终端2: 启动客户端
 * $ ./tcp_client
 * === TCP客户端 ===
 * 目标服务器: 127.0.0.1:8888
 * socket创建成功！
 * 正在连接服务器...
 * 连接成功！
 *
 * 输入消息发送给服务器（输入 'quit' 退出）：
 * > Hello Server
 * 已发送: Hello Server
 * 服务器响应: Hello Server
 * > quit
 * 已发送: quit
 * 服务器响应: 再见！欢迎下次光临！
 * 主动退出连接
 * 客户端已退出
 */
```

### 42.4.2 带有重连机制的TCP客户端

实际应用中，网络可能会不稳定。我们来写一个更健壮的客户端，带有自动重连机制。

```cpp
/*
 * tcp_client_robust.cpp
 * 健壮的TCP客户端 - 带自动重连
 *
 * 特性：
 * 1. 自动重连机制，网络断开后会自动尝试重连
 * 2. 心跳检测，定期发送心跳包检测连接状态
 * 3. 连接超时设置
 *
 * 编译: g++ -std=c++17 -pthread -o tcp_client_robust tcp_client_robust.cpp
 */

#include <iostream>
#include <cstring>
#include <thread>
#include <atomic>
#include <chrono>
#include "platform_socket.h"

const char* DEFAULT_SERVER_IP = "127.0.0.1";
const int DEFAULT_SERVER_PORT = 8888;
const int BUFFER_SIZE = 4096;
const int MAX_RETRY_COUNT = 5;
const int RECONNECT_DELAY_SEC = 3;
const int HEARTBEAT_INTERVAL_SEC = 10;

std::atomic<bool> g_running(true);
std::atomic<bool> g_connected(false);

// 心跳线程，定期发送心跳包
void heartbeat_thread(SOCKET sock) {
    while (g_running && g_connected) {
        std::this_thread::sleep_for(std::chrono::seconds(HEARTBEAT_INTERVAL_SEC));

        if (!g_connected) break;

        // 发送心跳包
        const char* heartbeat = "HEARTBEAT";
        int sent = send(sock, heartbeat, strlen(heartbeat), 0);
        if (sent == SOCKET_ERROR) {
            std::cerr << "[心跳] 发送失败，连接可能已断开" << std::endl;
            g_connected = false;
            break;
        }
        std::cout << "[心跳] 心跳包已发送" << std::endl;
    }
}

// 连接服务器
bool connect_to_server(SOCKET& sock, const char* ip, int port) {
    struct sockaddr_in serverAddr;
    set_address(&serverAddr, ip, (unsigned short)port);

    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "[连接] 连接失败: " << SOCKET_GET_ERROR() << std::endl;
        return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    const char* serverIP = (argc > 1) ? argv[1] : DEFAULT_SERVER_IP;
    int serverPort = (argc > 2) ? std::atoi(argv[2]) : DEFAULT_SERVER_PORT;

    std::cout << "=== 健壮的TCP客户端 ===" << std::endl;
    std::cout << "服务器: " << serverIP << ":" << serverPort << std::endl;
    std::cout << "最大重试次数: " << MAX_RETRY_COUNT << std::endl;
    std::cout << "心跳间隔: " << HEARTBEAT_INTERVAL_SEC << "秒" << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    int retryCount = 0;
    SOCKET clientSocket = INVALID_SOCKET;
    std::thread heartbeat;

    while (retryCount < MAX_RETRY_COUNT && g_running) {
        // 如果已连接，先关闭旧连接
        if (clientSocket != INVALID_SOCKET) {
            close_socket(clientSocket);
            if (heartbeat.joinable()) heartbeat.join();
        }

        // 创建新socket
        clientSocket = create_tcp_socket();
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "[连接] socket创建失败！" << std::endl;
            break;
        }

        std::cout << "\n[连接] 尝试连接服务器（第 " << (retryCount + 1) << " 次）..." << std::endl;

        if (connect_to_server(clientSocket, serverIP, serverPort)) {
            std::cout << "[连接] 连接成功！" << std::endl;
            g_connected = true;
            retryCount = 0; // 重置重试计数

            // 启动心跳线程
            heartbeat = std::thread(heartbeat_thread, clientSocket);

            // 通信循环
            char buffer[BUFFER_SIZE];
            while (g_running && g_connected) {
                std::cout << "> ";
                if (!std::cin.getline(buffer, BUFFER_SIZE)) {
                    // cin失败（可能是EOF）
                    g_running = false;
                    break;
                }

                if (strlen(buffer) == 0) continue;

                int sent = send(clientSocket, buffer, strlen(buffer), 0);
                if (sent == SOCKET_ERROR) {
                    std::cerr << "[错误] 发送失败: " << SOCKET_GET_ERROR() << std::endl;
                    g_connected = false;
                    break;
                }

                if (strcmp(buffer, "quit") == 0 || strcmp(buffer, "exit") == 0) {
                    g_running = false;
                    break;
                }

                // 接收响应
                memset(buffer, 0, BUFFER_SIZE);
                int received = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
                if (received > 0) {
                    buffer[received] = '\0';
                    std::cout << "服务器: " << buffer << std::endl;
                } else if (received == 0) {
                    std::cout << "[连接] 服务器关闭了连接" << std::endl;
                    g_connected = false;
                    break;
                } else {
                    std::cerr << "[错误] 接收失败: " << SOCKET_GET_ERROR() << std::endl;
                    g_connected = false;
                    break;
                }
            }

            g_connected = false;
        } else {
            retryCount++;
            if (retryCount < MAX_RETRY_COUNT) {
                std::cout << "[重连] " << RECONNECT_DELAY_SEC << "秒后重试..." << std::endl;
                std::this_thread::sleep_for(std::chrono::seconds(RECONNECT_DELAY_SEC));
            }
        }
    }

    if (heartbeat.joinable()) heartbeat.join();
    if (clientSocket != INVALID_SOCKET) close_socket(clientSocket);
    socket_cleanup();

    if (retryCount >= MAX_RETRY_COUNT) {
        std::cout << "已达到最大重试次数，退出。" << std::endl;
    } else {
        std::cout << "客户端已退出" << std::endl;
    }

    return 0;
}
```

---

## 42.5 UDP编程：更快但不保证送达

TCP是打电话，UDP则是对讲机——你直接喊出去，不确认对方有没有听到。

### 42.5.1 UDP服务端

```cpp
/*
 * udp_server.cpp
 * UDP服务端
 *
 * UDP不需要listen和accept，因为它是无连接的
 * 服务器直接等待数据，然后回复
 *
 * 编译: g++ -std=c++17 -o udp_server udp_server.cpp
 */

#include <iostream>
#include <cstring>
#include "platform_socket.h"

const char* SERVER_IP = "0.0.0.0";
const int SERVER_PORT = 9999;
const int BUFFER_SIZE = 4096;

int main() {
    std::cout << "=== UDP服务器 ===" << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    // 创建UDP socket
    SOCKET serverSocket = create_udp_socket();
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "socket创建失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        socket_cleanup();
        return 1;
    }
    std::cout << "UDP socket创建成功！" << std::endl;

    // 地址重用
    int opt = 1;
#ifdef _WIN32
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif

    // 绑定地址
    struct sockaddr_in serverAddr;
    set_address(&serverAddr, SERVER_IP, SERVER_PORT);

    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "bind绑定失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        close_socket(serverSocket);
        socket_cleanup();
        return 1;
    }
    std::cout << "绑定成功，监听端口: " << SERVER_PORT << std::endl;
    std::cout << "等待数据..." << std::endl;

    // UDP通信循环
    char buffer[BUFFER_SIZE];
    struct sockaddr_in clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);

    while (true) {
        // recvfrom接收数据，同时获取发送者地址
        memset(buffer, 0, BUFFER_SIZE);
        int bytesRead = recvfrom(serverSocket, buffer, BUFFER_SIZE - 1, 0,
                                  (struct sockaddr*)&clientAddr, &clientAddrLen);

        if (bytesRead > 0) {
            char clientIP[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, sizeof(clientIP));
            unsigned short clientPort = ntohs(clientAddr.sin_port);

            buffer[bytesRead] = '\0';
            std::cout << "[" << clientIP << ":" << clientPort << "] 收到: " << buffer << std::endl;

            // 简单处理：如果是"ping"，返回"pong"
            if (strcmp(buffer, "ping") == 0) {
                const char* response = "pong";
                sendto(serverSocket, response, strlen(response), 0,
                       (struct sockaddr*)&clientAddr, sizeof(clientAddr));
                std::cout << "[" << clientIP << ":" << clientPort << "] 发送: pong" << std::endl;
            } else {
                // 原样返回
                sendto(serverSocket, buffer, bytesRead, 0,
                       (struct sockaddr*)&clientAddr, sizeof(clientAddr));
                std::cout << "[" << clientIP << ":" << clientPort << "] 回显: " << buffer << std::endl;
            }
        } else {
            std::cerr << "recvfrom失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        }
    }

    close_socket(serverSocket);
    socket_cleanup();
    return 0;
}

/*
 * 测试：
 * $ ./udp_server
 * === UDP服务器 ===
 * UDP socket创建成功！
 * 绑定成功，监听端口: 9999
 * 等待数据...
 *
 * 另一个终端用nc测试UDP：
 * $ nc -u localhost 9999
 * ping
 * pong
 * hello
 * hello
 */
```

### 42.5.2 UDP客户端

```cpp
/*
 * udp_client.cpp
 * UDP客户端
 *
 * 编译: g++ -std=c++17 -o udp_client udp_client.cpp
 */

#include <iostream>
#include <cstring>
#include <thread>
#include <atomic>
#include "platform_socket.h"

const char* SERVER_IP = "127.0.0.1";
const int SERVER_PORT = 9999;
const int BUFFER_SIZE = 4096;

std::atomic<bool> g_running(true);

int main(int argc, char* argv[]) {
    const char* serverIP = (argc > 1) ? argv[1] : SERVER_IP;
    int serverPort = (argc > 2) ? std::atoi(argv[2]) : SERVER_PORT;

    std::cout << "=== UDP客户端 ===" << std::endl;
    std::cout << "目标服务器: " << serverIP << ":" << serverPort << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    SOCKET clientSocket = create_udp_socket();
    if (clientSocket == INVALID_SOCKET) {
        std::cerr << "socket创建失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        socket_cleanup();
        return 1;
    }

    // 设置服务器地址
    struct sockaddr_in serverAddr;
    set_address(&serverAddr, serverIP, (unsigned short)serverPort);

    char buffer[BUFFER_SIZE];
    struct sockaddr_in responseAddr;
    socklen_t responseAddrLen = sizeof(responseAddr);

    std::cout << "\n输入消息（输入 'quit' 退出）:" << std::endl;

    while (g_running) {
        std::cout << "> ";
        if (!std::cin.getline(buffer, BUFFER_SIZE)) {
            g_running = false;
            break;
        }

        if (strlen(buffer) == 0) continue;

        if (strcmp(buffer, "quit") == 0 || strcmp(buffer, "exit") == 0) {
            break;
        }

        // 发送数据（不需要先连接）
        int sent = sendto(clientSocket, buffer, strlen(buffer), 0,
                          (struct sockaddr*)&serverAddr, sizeof(serverAddr));
        if (sent == SOCKET_ERROR) {
            std::cerr << "sendto失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
            continue;
        }
        std::cout << "已发送: " << buffer << std::endl;

        // 接收响应
        memset(buffer, 0, BUFFER_SIZE);
        int received = recvfrom(clientSocket, buffer, BUFFER_SIZE - 1, 0,
                                 (struct sockaddr*)&responseAddr, &responseAddrLen);

        if (received > 0) {
            buffer[received] = '\0';
            std::cout << "服务器响应: " << buffer << std::endl;
        } else if (received == SOCKET_ERROR) {
            // 超时或错误
            std::cerr << "recvfrom失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        }
    }

    close_socket(clientSocket);
    socket_cleanup();
    std::cout << "客户端已退出" << std::endl;
    return 0;
}

/*
 * 注意：UDP可能丢包，所以如果服务器没启动，客户端会一直等待响应
 * 可以用 setsockopt 设置 SO_RCVTIMEO 超时
 */
```

---

## 42.6 IPv6支持：让程序拥抱未来

IPv4地址早就不够用了！IPv6才是未来的主流。我们的代码也要与时俱进。

### IPv6与IPv4的关键区别

| 对比项 | IPv4 | IPv6 |
|--------|------|------|
| 地址长度 | 32位（4字节） | 128位（16字节） |
| 地址格式 | `192.168.1.1` | `2001:0db8:85a3::8a2e:0370:7334` |
| 地址族 | `AF_INET` | `AF_INET6` |
| 结构体 | `sockaddr_in` | `sockaddr_in6` |
| 地址长度 | `sizeof(sockaddr_in)` | `sizeof(sockaddr_in6)` |
| 表示函数 | `inet_pton(AF_INET, ...)` | `inet_pton(AF_INET6, ...)` |

### 统一地址封装（推荐做法）

为了同时支持IPv4和IPv6，我们可以用` sockaddr_storage`来存储任意类型的地址：

```cpp
/*
 * ipv6_server.cpp
 * 支持IPv6的TCP服务器
 *
 * 同时监听IPv4和IPv6（双栈）
 *
 * 编译: g++ -std=c++17 -o ipv6_server ipv6_server.cpp
 */

#include <iostream>
#include <cstring>
#include <vector>
#include "platform_socket.h"

const int SERVER_PORT = 8888;
const int BUFFER_SIZE = 4096;

// IPv6版本的地址设置函数
inline void set_address_v6(struct sockaddr_in6* addr, const char* ip, unsigned short port) {
    memset(addr, 0, sizeof(struct sockaddr_in6));
    addr->sin6_family = AF_INET6;
    addr->sin6_port = htons(port);
    if (ip == nullptr || strcmp(ip, "::") == 0 || strcmp(ip, "") == 0) {
        addr->sin6_addr = in6addr_any; // 监听所有接口
    } else {
        inet_pton(AF_INET6, ip, &addr->sin6_addr);
    }
}

// 获取地址字符串（兼容IPv4/IPv6）
inline void get_address_str(struct sockaddr* addr, char* ip_str, int ip_len, int* port) {
    if (addr->sa_family == AF_INET) {
        struct sockaddr_in* addr4 = (struct sockaddr_in*)addr;
        inet_ntop(AF_INET, &addr4->sin_addr, ip_str, ip_len);
        if (port) *port = ntohs(addr4->sin_port);
    } else if (addr->sa_family == AF_INET6) {
        struct sockaddr_in6* addr6 = (struct sockaddr_in6*)addr;
        inet_ntop(AF_INET6, &addr6->sin6_addr, ip_str, ip_len);
        if (port) *port = ntohs(addr6->sin6_port);
    }
}

int main() {
    std::cout << "=== IPv6双栈TCP服务器 ===" << std::endl;
    std::cout << "监听端口: " << SERVER_PORT << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    // 创建IPv6 TCP socket
    SOCKET serverSocket = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "IPv6 socket创建失败！" << std::endl;
        // 降级提示
        std::cerr << "你的系统可能不支持IPv6。" << std::endl;
        socket_cleanup();
        return 1;
    }

    // 关键！设置IPv6 only选项为0，允许同时接收IPv4和IPv6连接
    int no = 0;
    setsockopt(serverSocket, IPPROTO_IPV6, IPV6_V6ONLY, (const char*)&no, sizeof(no));

    // 地址重用
    int opt = 1;
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));

    // 绑定
    struct sockaddr_in6 serverAddr;
    set_address_v6(&serverAddr, "::", SERVER_PORT); // "::" 表示IPv6双栈

    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "bind绑定失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
        closesocket(serverSocket);
        socket_cleanup();
        return 1;
    }

    if (listen(serverSocket, 10) == SOCKET_ERROR) {
        std::cerr << "listen失败！" << std::endl;
        closesocket(serverSocket);
        socket_cleanup();
        return 1;
    }

    std::cout << "服务器已启动，等待连接..." << std::endl;

    while (true) {
        struct sockaddr_storage clientAddr;
        socklen_t clientAddrLen = sizeof(clientAddr);

        SOCKET clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "accept失败！" << std::endl;
            continue;
        }

        char ipStr[INET6_ADDRSTRLEN];
        int clientPort;
        get_address_str((struct sockaddr*)&clientAddr, ipStr, sizeof(ipStr), &clientPort);
        std::cout << "客户端连接: " << ipStr << ":" << clientPort << std::endl;

        // 回显服务
        char buffer[BUFFER_SIZE];
        while (true) {
            memset(buffer, 0, BUFFER_SIZE);
            int bytesRead = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
            if (bytesRead <= 0) break;

            buffer[bytesRead] = '\0';
            std::cout << "收到: " << buffer << std::endl;
            send(clientSocket, buffer, bytesRead, 0);
        }

        closesocket(clientSocket);
        std::cout << "客户端断开: " << ipStr << std::endl;
    }

    closesocket(serverSocket);
    socket_cleanup();
    return 0;
}

/*
 * 测试IPv6：
 * $ ./ipv6_server
 * $ nc -6 localhost 8888   # 强制IPv6
 * $ nc localhost 8888      # IPv4也能连
 *
 * 查看服务器是否监听IPv6：
 * $ netstat -tlnp | grep 8888
 */
```

> **小知识**：为什么设置`IPV6_V6ONLY = 0`？默认情况下，IPv6 socket只接受IPv6连接。但我们设置为0后，同一个端口就能同时接受IPv4和IPv6连接了！这就是"双栈"模式。不过要注意，IPv4和IPv6的地址表示完全不同，代码里要做好适配。

---

## 42.7 实用工具：完整HTTP客户端

HTTP是互联网上最重要的协议。让我们来实现一个简单的HTTP客户端，能发送GET请求并解析响应。

```cpp
/*
 * http_client.cpp
 * 简单HTTP客户端
 *
 * 实现基本的HTTP/1.0 GET请求
 * 解析响应状态码和body
 *
 * 编译: g++ -std=c++17 -o http_client http_client.cpp
 * 运行: ./http_client www.example.com / 或者 ./http_client 127.0.0.1 8080 /
 */

#include <iostream>
#include <cstring>
#include <map>
#include "platform_socket.h"

const int BUFFER_SIZE = 8192;
const int CONNECT_TIMEOUT_SEC = 5;
const int RECEIVE_TIMEOUT_SEC = 10;

struct HttpResponse {
    int statusCode;
    std::string statusMessage;
    std::map<std::string, std::string> headers;
    std::string body;

    void clear() {
        statusCode = 0;
        statusMessage.clear();
        headers.clear();
        body.clear();
    }
};

class HttpClient {
private:
    SOCKET m_sock;
    std::string m_host;
    int m_port;

    bool connect_server() {
        struct sockaddr_in serverAddr;
        set_address(&serverAddr, m_host.c_str(), (unsigned short)m_port);

        // 设置连接超时
#ifdef _WIN32
        DWORD timeout = CONNECT_TIMEOUT_SEC * 1000;
        setsockopt(m_sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeout, sizeof(timeout));
        setsockopt(m_sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeout, sizeof(timeout));
#else
        struct timeval timeout;
        timeout.tv_sec = CONNECT_TIMEOUT_SEC;
        timeout.tv_usec = 0;
        setsockopt(m_sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));
        setsockopt(m_sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
#endif

        return connect(m_sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) != SOCKET_ERROR;
    }

    bool send_request(const std::string& path) {
        // 构建HTTP/1.0请求
        std::string request = "GET " + path + " HTTP/1.0\r\n";
        request += "Host: " + m_host + "\r\n";
        request += "User-Agent: CppHttpClient/1.0\r\n";
        request += "Accept: */*\r\n";
        request += "Connection: close\r\n";
        request += "\r\n";

        int sent = send(m_sock, request.c_str(), request.length(), 0);
        return sent != SOCKET_ERROR;
    }

    bool parse_response(HttpResponse& resp) {
        char buffer[BUFFER_SIZE];
        int totalReceived = 0;
        std::string headerPart;
        bool headerDone = false;

        // 接收所有数据
        while (true) {
            memset(buffer, 0, BUFFER_SIZE);
            int received = recv(m_sock, buffer, BUFFER_SIZE - 1, 0);

            if (received > 0) {
                if (!headerDone) {
                    headerPart += buffer;

                    // 检查是否读完header
                    size_t headerEnd = headerPart.find("\r\n\r\n");
                    if (headerEnd != std::string::npos) {
                        // 解析header
                        std::string headerArea = headerPart.substr(0, headerEnd);
                        resp.body = headerPart.substr(headerEnd + 4);

                        // 解析状态行
                        size_t firstLineEnd = headerArea.find("\r\n");
                        std::string statusLine = headerArea.substr(0, firstLineEnd);

                        // 解析 HTTP/1.x 200 OK
                        size_t space1 = statusLine.find(' ');
                        size_t space2 = statusLine.rfind(' ');
                        if (space1 != std::string::npos && space2 != std::string::npos) {
                            resp.statusCode = std::atoi(statusLine.c_str() + space1 + 1);
                            resp.statusMessage = statusLine.substr(space2 + 1);
                        }

                        // 解析headers
                        size_t pos = firstLineEnd + 2;
                        while (pos < headerArea.length()) {
                            size_t lineEnd = headerArea.find("\r\n", pos);
                            if (lineEnd == std::string::npos) break;

                            std::string line = headerArea.substr(pos, lineEnd - pos);
                            size_t colon = line.find(':');
                            if (colon != std::string::npos) {
                                std::string key = line.substr(0, colon);
                                std::string value = line.substr(colon + 1);
                                // 去掉开头的空格
                                while (value.length() > 0 && value[0] == ' ') {
                                    value = value.substr(1);
                                }
                                resp.headers[key] = value;
                            }

                            pos = lineEnd + 2;
                        }

                        totalReceived = resp.body.length();
                        headerDone = true;
                    }
                } else {
                    resp.body += buffer;
                    totalReceived += received;
                }
            } else {
                break;
            }
        }

        return resp.statusCode > 0;
    }

public:
    HttpClient(const std::string& host, int port) : m_host(host), m_port(port) {
        m_sock = create_tcp_socket();
    }

    ~HttpClient() {
        close_socket(m_sock);
    }

    HttpResponse get(const std::string& path) {
        HttpResponse resp;
        resp.clear();

        if (m_sock == INVALID_SOCKET) {
            std::cerr << "无效的socket" << std::endl;
            return resp;
        }

        if (!connect_server()) {
            std::cerr << "连接服务器失败！" << std::endl;
            return resp;
        }

        if (!send_request(path)) {
            std::cerr << "发送请求失败！" << std::endl;
            return resp;
        }

        if (!parse_response(resp)) {
            std::cerr << "解析响应失败！" << std::endl;
            return resp;
        }

        return resp;
    }
};

// 解析URL
bool parse_url(const std::string& url, std::string& host, int& port, std::string& path) {
    size_t pos = 0;

    // 去掉 http://
    if (url.substr(0, 7) == "http://") {
        pos = 7;
    } else if (url.substr(0, 8) == "https://") {
        std::cerr << "HTTPS暂不支持（需要SSL/TLS）" << std::endl;
        return false;
    }

    // 找到路径开始的位置
    size_t pathPos = url.find('/', pos);
    if (pathPos == std::string::npos) {
        host = url.substr(pos);
        path = "/";
    } else {
        host = url.substr(pos, pathPos - pos);
        path = url.substr(pathPos);
    }

    // 检查是否有端口
    size_t colonPos = host.find(':');
    if (colonPos != std::string::npos) {
        port = std::atoi(host.c_str() + colonPos + 1);
        host = host.substr(0, colonPos);
    } else {
        port = 80;
    }

    return true;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "用法: " << argv[0] << " <URL>" << std::endl;
        std::cout << "示例: " << argv[0] << " http://www.example.com/" << std::endl;
        std::cout << "      " << argv[0] << " http://127.0.0.1:8080/api/test" << std::endl;
        return 1;
    }

    std::string url = argv[1];
    std::string host;
    int port;
    std::string path;

    if (!parse_url(url, host, port, path)) {
        return 1;
    }

    std::cout << "=== 简单HTTP客户端 ===" << std::endl;
    std::cout << "主机: " << host << std::endl;
    std::cout << "端口: " << port << std::endl;
    std::cout << "路径: " << path << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    HttpClient client(host, port);
    HttpResponse resp = client.get(path);

    socket_cleanup();

    if (resp.statusCode > 0) {
        std::cout << "\n=== 响应 ===" << std::endl;
        std::cout << "状态码: " << resp.statusCode << " " << resp.statusMessage << std::endl;
        std::cout << "Headers:" << std::endl;
        for (const auto& h : resp.headers) {
            std::cout << "  " << h.first << ": " << h.second << std::endl;
        }
        std::cout << "\nBody (" << resp.body.length() << " 字节):" << std::endl;
        std::string displayBody = resp.body;
        bool truncated = false;
        if (displayBody.length() > 200) {
            displayBody = displayBody.substr(0, 200);
            truncated = true;
        }
        std::cout << displayBody << std::endl;

        if (truncated) {
            std::cout << "\n（以上为响应body的前200字符，完整内容有" << resp.body.length() << "字节）" << std::endl;
        }
    } else {
        std::cout << "请求失败！" << std::endl;
        return 1;
    }

    return 0;
}

/*
 * 测试：
 * $ ./http_client http://www.example.com/
 * === 简单HTTP客户端 ===
 * 主机: www.example.com
 * 端口: 80
 * 路径: /
 * 状态码: 200 OK
 * Headers:
 *   Content-Type: text/html
 *   Content-Length: ...
 *
 * Body (1256 字节):
 * <!doctype html>
 * <html>
 * ...
 */
```

> **小知识**：真实的HTTP客户端要复杂得多！需要处理：chunked编码、gzip压缩、HTTPS（SSL/TLS）、重定向、Cookie、代理、Keep-Alive等等。这只是个教学级别的简化版。
>
> **实用建议**：生产环境推荐使用成熟的库，如 `libcurl`（老牌全能）、`cpp-httplib`（C++简单易用）、` Boost.Beast`（Boost家族）。自己从头实现完整HTTP？除非你想深入理解协议，否则真的没必要。用库不丢人，"重复造轮子"才吓人！

---

## 42.8 select多路复用：一个线程服务多个客户端

多线程虽然简单，但线程数量太多会消耗大量资源。有没有办法用一个线程同时管理多个连接？答案是：**I/O多路复用**。

`select()`是最经典的多路复用机制。它允许你同时监视多个socket，当某个socket有数据可读或可写时，`select()`会告诉你。

```cpp
/*
 * tcp_server_select.cpp
 * 使用select的TCP服务器 - I/O多路复用
 *
 * 优点：单线程就能处理多个客户端，资源消耗低
 * 缺点：select有fd数量限制（Linux通常是1024），且效率不是最优
 *
 * 编译: g++ -std=c++17 -o tcp_server_select tcp_server_select.cpp
 */

#include <iostream>
#include <cstring>
#include <vector>
#include <map>
#include <algorithm>
#include "platform_socket.h"

const char* SERVER_IP = "0.0.0.0";
const int SERVER_PORT = 8888;
const int BUFFER_SIZE = 4096;
const int MAX_FD = 1024;

int main() {
    std::cout << "=== Select多路复用TCP服务器 ===" << std::endl;

    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        return 1;
    }

    // 创建监听socket
    SOCKET listenSocket = create_tcp_socket();
    if (listenSocket == INVALID_SOCKET) {
        std::cerr << "socket创建失败！" << std::endl;
        socket_cleanup();
        return 1;
    }

    int opt = 1;
#ifdef _WIN32
    setsockopt(listenSocket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(listenSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif

    struct sockaddr_in serverAddr;
    set_address(&serverAddr, SERVER_IP, SERVER_PORT);

    if (bind(listenSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "bind绑定失败！" << std::endl;
        close_socket(listenSocket);
        socket_cleanup();
        return 1;
    }

    if (listen(listenSocket, 10) == SOCKET_ERROR) {
        std::cerr << "listen失败！" << std::endl;
        close_socket(listenSocket);
        socket_cleanup();
        return 1;
    }

    std::cout << "服务器监听 " << SERVER_PORT << " 端口..." << std::endl;

    // fd_set：文件描述符集合
    fd_set readfds, masterfds;
    FD_ZERO(&masterfds);
    FD_SET(listenSocket, &masterfds); // 把监听socket加入集合

    SOCKET maxfd = listenSocket;
    std::map<SOCKET, std::string> clientNames; // socket -> 客户端标识

    while (true) {
        readfds = masterfds; // 每次循环都要复制，因为select会修改

        // 等待有socket准备好
        // NULL表示无限等待，直到有socket就绪
        int activity = select(maxfd + 1, &readfds, NULL, NULL, NULL);

        if (activity < 0) {
            std::cerr << "select失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
            break;
        }

        // 遍历所有fd，检查是哪个就绪
        for (SOCKET fd = 0; fd <= maxfd; ++fd) {
            if (!FD_ISSET(fd, &readfds)) continue;

            if (fd == listenSocket) {
                // 监听socket就绪，说明有新的连接
                struct sockaddr_in clientAddr;
                socklen_t clientAddrLen = sizeof(clientAddr);
                SOCKET clientSocket = accept(listenSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);

                if (clientSocket != INVALID_SOCKET) {
                    char ip[INET_ADDRSTRLEN];
                    inet_ntop(AF_INET, &clientAddr.sin_addr, ip, sizeof(ip));
                    int port = ntohs(clientAddr.sin_port);

                    std::cout << "新连接: " << ip << ":" << port
                              << " (socket fd=" << clientSocket << ")" << std::endl;

                    FD_SET(clientSocket, &masterfds);
                    if (clientSocket > maxfd) maxfd = clientSocket;

                    char name[64];
                    snprintf(name, sizeof(name), "%s:%d", ip, port);
                    clientNames[clientSocket] = name;

                    // 发送欢迎消息
                    const char* welcome = "欢迎连接！发送消息测试echo。\n";
                    send(clientSocket, welcome, strlen(welcome), 0);
                }
            } else {
                // 客户端socket就绪，读取数据
                char buffer[BUFFER_SIZE];
                memset(buffer, 0, BUFFER_SIZE);
                int bytesRead = recv(fd, buffer, BUFFER_SIZE - 1, 0);

                if (bytesRead > 0) {
                    buffer[bytesRead] = '\0';
                    std::string name = clientNames.count(fd) ? clientNames[fd] : "unknown";
                    std::cout << "[" << name << "] 收到: " << buffer << std::endl;

                    // 回显
                    send(fd, buffer, bytesRead, 0);
                } else if (bytesRead == 0) {
                    // 客户端关闭连接
                    std::string name = clientNames.count(fd) ? clientNames[fd] : "unknown";
                    std::cout << "[" << name << "] 断开连接" << std::endl;

                    FD_CLR(fd, &masterfds);
                    close_socket(fd);
                    clientNames.erase(fd);
                } else {
                    // 错误
                    std::cerr << "recv失败！错误码: " << SOCKET_GET_ERROR() << std::endl;
                    FD_CLR(fd, &masterfds);
                    close_socket(fd);
                    clientNames.erase(fd);
                }
            }
        }
    }

    close_socket(listenSocket);
    socket_cleanup();
    return 0;
}

/*
 * select的工作原理：
 *
 * 1. 创建一个fd_set集合，放入你想监视的socket
 * 2. 调用select，传入这个集合
 * 3. select会阻塞，直到有socket变得"可读"或"可写"
 * 4. 返回后，检查哪些socket在集合里（被标记了）
 * 5. 处理就绪的socket，然后回到步骤1
 *
 * "可读"意味着：
 * - TCP: 收到数据、连接关闭、发生错误
 * - UDP: 收到数据包
 */
```

---

## 42.9 使用Boost.Asio进行现代网络编程

原生socket API比较底层，用起来繁琐。现代C++网络编程推荐使用**Boost.Asio**（独立的Asio库，或通过Boost.ASIO使用）。注意：C++标准库的`std::networking`技术规范虽然存在，但尚未完全纳入标准，是未来的发展方向。

> **碎碎念**：C++委员会在网络库这件事上已经"规划"了很多年了，标准和实现总是差那么一步。所以别等了，直接上手Asio吧，等标准完善的时候你已经是个老手了！

Boost.Asio支持：
- 同步I/O：简单直接
- 异步I/O：高性能，事件驱动
- 协程支持（C++20）：用同步的方式写异步代码

```cpp
/*
 * asio_echo_server.cpp
 * Boost.Asio回显服务器
 *
 * 这个版本使用异步I/O，性能更好
 *
 * 编译: g++ -std=c++17 -o asio_server asio_echo_server.cpp -lboost_system -lpthread
 * 或者如果你有独立asio库:
 * g++ -std=c++17 -I/path/to/asio -o asio_server asio_echo_server.cpp
 */

#include <iostream>
#include <memory>
#include <string>
#include <array>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

class Session : public std::enable_shared_from_this<Session> {
public:
    Session(tcp::socket socket) : socket_(std::move(socket)) {}

    void start() {
        do_read();
    }

private:
    void do_read() {
        auto self = shared_from_this();
        socket_.async_read_some(
            boost::asio::buffer(data_),
            [this, self](boost::system::error_code ec, std::size_t length) {
                if (!ec) {
                    std::cout << "收到: " << std::string(data_, length) << std::endl;
                    do_write(length);
                }
            });
    }

    void do_write(std::size_t length) {
        auto self = shared_from_this();
        boost::asio::async_write(
            socket_,
            boost::asio::buffer(data_, length),
            [this, self](boost::system::error_code ec, std::size_t /*length*/) {
                if (!ec) {
                    do_read(); // 继续读取下一个请求
                }
            });
    }

    tcp::socket socket_;
    std::array<char, 1024> data_;
};

class Server {
public:
    Server(boost::asio::io_context& io_context, unsigned short port)
        : acceptor_(io_context, tcp::endpoint(tcp::v4(), port)) {
        std::cout << "Asio服务器监听端口 " << port << "..." << std::endl;
        do_accept();
    }

private:
    void do_accept() {
        acceptor_.async_accept(
            [this](boost::system::error_code ec, tcp::socket socket) {
                if (!ec) {
                    std::make_shared<Session>(std::move(socket))->start();
                }
                do_accept(); // 继续接受下一个连接
            });
    }

    tcp::acceptor acceptor_;
};

int main(int argc, char* argv[]) {
    unsigned short port = (argc > 1) ? std::atoi(argv[1]) : 8888;

    try {
        boost::asio::io_context io_context;
        Server server(io_context, port);
        io_context.run(); // 开始事件循环
    } catch (std::exception& e) {
        std::cerr << "异常: " << e.what() << std::endl;
    }

    return 0;
}

/*
 * Asio的优势：
 *
 * 1. 跨平台：Windows、Linux、Mac都能用
 * 2. 异步支持：高性能服务器必备
 * 3. 统一接口：socket、定时器、信号等都用同样的模式
 * 4. 协程支持：C++20协程让异步代码看起来像同步的
 *
 * Asio的缺点：
 * 1. 需要安装Boost或独立Asio库
 * 2. 编译时间可能较长
 * 3. 错误信息有时候很晦涩
 */

/*
 * 如果你不想安装Boost，可以使用standalone Asio：
 * https://think-async.com/Asio/
 *
 * 或者使用更现代的替代品：
 * - libuv (Node.js底层)
 * - libevent
 * - uvw (C++ wrapper for libuv)
 * - cpp-httplib (简单的HTTP库)
 */
```

---

## 42.10 网络编程中的常见问题与安全

### 42.10.1 缓冲区溢出

网络数据不可信！永远不要假设客户端发来的数据长度不超过你的缓冲区。

```cpp
// ❌ 危险！可能缓冲区溢出
char buffer[100];
recv(clientSocket, buffer, 500, 0); // 恶意客户端可以发送超长数据

// ✅ 安全做法：限制读取长度
char buffer[100];
int bytesToRead = std::min(99, expectedMax);
int bytesRead = recv(clientSocket, buffer, bytesToRead, 0);
buffer[bytesRead] = '\0';
```

### 42.10.2 拒绝服务攻击（DoS）

恶意客户端可能：
- 发送大量数据耗尽服务器资源
- 慢速发送：只发送一个字节，然后等很久
- 同时建立大量连接

防御措施：
- 设置读取超时
- 限制单个连接的数据量
- 使用连接池和线程池
- 限制最大连接数

### 42.10.3 输入验证

永远不要直接使用网络数据作为SQL查询、shell命令或文件路径。

```cpp
// ❌ 危险！命令注入漏洞
std::string filename = receive_filename();
system(("cat " + filename).c_str());

// 恶意输入: "test.txt; rm -rf /"
// ✅ 安全：验证输入
std::string filename = receive_filename();
if (!is_valid_filename(filename)) {
    // 拒绝请求
}
```

### 42.10.4 加密传输

明文传输的密码和敏感数据可以被中间人窃取。生产环境务必使用HTTPS（TLS/SSL）。

```cpp
/*
 * https_client.cpp
 * 简单的HTTPS客户端（使用OpenSSL）
 *
 * 依赖: OpenSSL库 (libssl-dev on Linux, vcpkg on Windows)
 * 编译: g++ -std=c++17 -o https_client https_client.cpp -lssl -lcrypto
 * 编译(Windows): cl /EHsc /std:c++17 https_client.cpp ssleay32.lib libeay32.lib
 */

#include <iostream>
#include <cstring>
#include <string>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/x509v3.h>

// 初始化OpenSSL
SSL_CTX* init_ssl_ctx() {
    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_all_algorithms();

    // 创建SSL上下文（TLS 1.2+）
    SSL_CTX* ctx = SSL_CTX_new(TLS_client_method());
    if (!ctx) {
        std::cerr << "SSL上下文创建失败！" << std::endl;
        return nullptr;
    }

    // 设置不验证证书（生产环境应启用验证）
    SSL_CTX_set_verify(ctx, SSL_VERIFY_NONE, nullptr);

    // 设置最低TLS版本
    SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);

    return ctx;
}

// 清理OpenSSL
void cleanup_ssl(SSL_CTX* ctx) {
    if (ctx) SSL_CTX_free(ctx);
    EVP_cleanup();
    ERR_free_strings();
}

// HTTPS请求
bool https_request(SSL* ssl, const std::string& host, const std::string& path) {
    // 构建HTTP请求
    std::string request = "GET " + path + " HTTP/1.1\r\n";
    request += "Host: " + host + "\r\n";
    request += "User-Agent: CppHTTPSClient/1.0\r\n";
    request += "Connection: close\r\n";
    request += "\r\n";

    // 发送请求
    int sent = SSL_write(ssl, request.c_str(), request.length());
    if (sent <= 0) {
        int err = SSL_get_error(ssl, sent);
        std::cerr << "SSL_write失败，错误码: " << err << std::endl;
        return false;
    }
    std::cout << "请求已发送 (" << sent << " 字节)" << std::endl;

    // 读取响应
    char buffer[8192];
    std::string response;
    int bytes;
    while ((bytes = SSL_read(ssl, buffer, sizeof(buffer) - 1)) > 0) {
        buffer[bytes] = '\0';
        response += buffer;
    }

    if (bytes < 0) {
        int err = SSL_get_error(ssl, bytes);
        if (err != SSL_ERROR_ZERO_RETURN) {
            std::cerr << "SSL_read失败，错误码: " << err << std::endl;
            return false;
        }
    }

    std::cout << "\n=== 响应 (" << response.size() << " 字节) ===" << std::endl;
    std::cout << response << std::endl;

    return true;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "用法: " << argv[0] << " <主机名> <路径>" << std::endl;
        std::cout << "示例: " << argv[0] << " www.example.com /" << std::endl;
        return 1;
    }

    std::string host = argv[1];
    std::string path = argv[2];
    int port = 443; // HTTPS默认端口

    std::cout << "=== 简单HTTPS客户端 ===" << std::endl;
    std::cout << "主机: " << host << std::endl;
    std::cout << "端口: " << port << std::endl;
    std::cout << "路径: " << path << std::endl;

    // 初始化SSL
    SSL_CTX* ctx = init_ssl_ctx();
    if (!ctx) return 1;

    // 创建socket连接
    if (socket_init() != 0) {
        std::cerr << "socket初始化失败！" << std::endl;
        cleanup_ssl(ctx);
        return 1;
    }

    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "socket创建失败！" << std::endl;
        socket_cleanup();
        cleanup_ssl(ctx);
        return 1;
    }

    // DNS解析
    struct hostent* he = gethostbyname(host.c_str());
    if (!he) {
        std::cerr << "DNS解析失败: " << host << std::endl;
        closesocket(sock);
        socket_cleanup();
        cleanup_ssl(ctx);
        return 1;
    }

    // 连接服务器
    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    memcpy(&serverAddr.sin_addr, he->h_addr, he->h_length);

    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "连接失败！" << std::endl;
        closesocket(sock);
        socket_cleanup();
        cleanup_ssl(ctx);
        return 1;
    }
    std::cout << "TCP连接成功！" << std::endl;

    // 创建SSL对象并绑定到socket
    SSL* ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);

    // 设置SNI（服务器名称指示），现代HTTPS必需
    SSL_set_tlsext_host_name(ssl, host.c_str());

    // 执行TLS握手
    std::cout << "正在执行TLS握手..." << std::endl;
    int ret = SSL_connect(ssl);
    if (ret != 1) {
        int err = SSL_get_error(ssl, ret);
        std::cerr << "TLS握手失败，错误码: " << err << std::endl;
        if (err == SSL_ERROR_SSL) {
            ERR_print_errors_fp(stderr);
        }
        SSL_free(ssl);
        closesocket(sock);
        socket_cleanup();
        cleanup_ssl(ctx);
        return 1;
    }

    std::cout << "TLS握手成功！" << std::endl;
    std::cout << "加密协议: " << SSL_get_version(ssl) << std::endl;
    std::cout << "加密算法: " << SSL_get_cipher(ssl) << std::endl;

    // 发送HTTPS请求
    https_request(ssl, host, path);

    // 清理
    SSL_shutdown(ssl);
    SSL_free(ssl);
    closesocket(sock);
    socket_cleanup();
    cleanup_ssl(ctx);

    return 0;
}

/*
 * HTTPS编程要点：
 *
 * 1. 端口：HTTPS默认用443，不是80
 * 2. 证书验证：生产环境必须验证服务器证书，防止中间人攻击
 * 3. SNI：现代HTTPS服务器托管多个域名，必须发送服务器名称
 * 4. TLS版本：禁用SSL 3.0和TLS 1.0/1.1，它们有安全漏洞
 * 5. 证书链验证：需要安装受信任的CA证书
 *
 * 生产环境建议：
 * - 使用成熟的库如libcurl、cpp-httplib处理HTTPS
 * - 不要自己实现SSL/TLS，那是给自己埋雷
 */
```

---

## 本章小结

恭喜你！终于学完了C++网络编程这一章！让我们来回顾一下学到的知识：

### 核心概念

| 概念 | 说明 |
|------|------|
| **socket** | 网络编程的核心，像网络的"插座" |
| **TCP** | 面向连接、可靠传输、保证顺序，像打电话 |
| **UDP** | 无连接、不可靠、速度快，像对讲机 |
| **IP地址** | 设备的唯一标识，网络世界的"身份证号" |
| **端口号** | 设备上的服务区分，网络世界的"房间号" |

### TCP编程要点

| 步骤 | 函数 | 说明 |
|------|------|------|
| 1 | `socket()` | 创建TCP socket |
| 2 | `bind()` | 绑定地址和端口 |
| 3 | `listen()` | 开始监听连接 |
| 4 | `accept()` | 接受客户端连接 |
| 5 | `recv()`/`send()` | 数据通信 |
| 6 | `closesocket()` | 关闭连接 |

### UDP编程要点

| 步骤 | 函数 | 说明 |
|------|------|------|
| 1 | `socket()` | 创建UDP socket |
| 2 | `bind()` | 绑定地址和端口 |
| 3 | `recvfrom()`/`sendto()` | 数据通信（带地址） |
| 4 | `closesocket()` | 关闭socket |

### I/O多路复用

| 方法 | 特点 |
|------|------|
| `select()` | 经典方法，有fd数量限制（通常1024） |
| `poll()` | 无数量限制，但效率一般 |
| `epoll()`（Linux） | 高效，百万级连接，推荐用于Linux服务器 |
| `kqueue()`（BSD/Mac） | BSD/Mac上的高效方案 |

### 现代网络库

| 库 | 特点 |
|----|------|
| **Boost.Asio** | 最成熟，跨平台，支持同步/异步 |
| **libuv** | Node.js底层，高性能 |
| **cpp-httplib** | 简单的HTTP服务器/客户端 |
| ** Beast** | Boost子库，HTTP/WebSocket |

### 安全注意事项

> **永远不要信任网络输入**：验证、验证、再验证！来自网络的数据就像陌生人递给你的糖——最好别吃。
>
> **防止缓冲区溢出**：限制读取长度，不要用`strcpy`等不安全的函数。你永远不知道客户端会塞给你多长的字符串。
>
> **防止DoS攻击**：设置超时、限制连接数、限制单连接数据量。对付恶意用户要从代码层面给予"尊重"。
>
> **敏感数据要加密**：生产环境必须用HTTPS/TLS。明文传输等于在网上裸奔。
>
> **最小权限原则**：不要用root运行网络服务。
>
> **不要自己写加密**：加密这块水很深，你把握不住。交给OpenSSL、libsodium这些久经沙场的库吧，自己造轮子只会造出"漏洞轮子"。

---

网络编程是C++的重要应用领域。从游戏服务器到高性能Web框架，从嵌入式设备通信到云计算基础设施，到处都有C++网络编程的身影。

虽然原生socket API有些繁琐，但它是理解网络原理的必经之路。掌握了这些基础后，再学习Boost.Asio等现代库就会事半功倍。

继续加油，未来的网络大师！下一章我们将探讨C++的更多高级主题！

> **预告**：下一章我们将探讨C++的模板元编程和编译时计算，让你的代码在编译期就把活干完，运行时飞起来！
