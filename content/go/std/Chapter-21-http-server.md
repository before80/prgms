+++
title = "第 21 章：HTTP 服务端——net/http"
weight = 210
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 21 章：HTTP 服务端——net/http

> 互联网的每一秒，都有无数个 HTTP 请求在服务器间穿梭。你打开一个网页，是 HTTP；你调用一个 API，是 HTTP；你刷到一个视频，背后还是 HTTP。可以说，HTTP 就是互联网的"普通话"——虽然有时候说着说着就变成了 HTTPS（普通话加密版）。在这一章里，我们来探索 Go 标准库中那个让一切成为可能的包：`net/http`。

---

## 21.1 net/http 包解决什么问题：Web 服务器是互联网最常见的服务形式

HTTP（HyperText Transfer Protocol，超文本传输协议）是万维网的基础。当你在浏览器地址栏输入一个 URL 并按下回车时，浏览器会向目标服务器发送一个 HTTP 请求，服务器处理后返回 HTTP 响应——这个"一问一答"的过程，就是互联网最核心的交互模式。

Web 服务器就是那个"接听"请求并"回复"答案的程序。无论是 Nginx、Apache，还是你用 Go、Python、Node.js 写的服务器，本质上都在做同一件事：**监听端口 → 接收请求 → 处理业务 → 返回响应**。

`net/http` 是 Go 语言标准库中用于构建 HTTP 服务端的瑞士军刀。它帮我们封装了 TCP 监听、协议解析、连接管理、请求路由等繁琐工作，让开发者可以专注于业务逻辑本身。

### 什么是 Web 服务器？

简单来说，Web 服务器就是一个**长期运行的程序**，它绑定到一个端口（通常是 80 或 443），等待客户端（浏览器、App、其他服务）发来 HTTP 请求，然后给出回应。

```go
// 一个能跑起来的 Web 服务器，就是这么朴实无华
package main

import "fmt"

func main() {
    fmt.Println("我是一个 Web 服务器！我在 8080 端口等待请求...")
    fmt.Println("但等等，我好像什么都没做——别急，net/http 帮我包揽了所有脏活累活")
}
```

### 常见 Web 服务器软件

| 服务器 | 语言/平台 | 特点 |
|--------|-----------|------|
| Nginx | C | 高性能反向代理，静态文件服务 |
| Apache HTTPd | C | 老牌霸主，.htaccess 灵活配置 |
| Apache Tomcat | Java | Java Web 应用容器 |
| IIS | C# | Windows 平台亲儿子 |
| Go net/http | Go | 轻量、并发友好、标准库零依赖 |

Go 的 `net/http` 包设计哲学是：**简单却不简陋**。用它几分钟就能搭起一个能扛住并发压力的 HTTP 服务。

---

## 21.2 net/http 核心原理：HTTP 是"请求-响应"协议，Handler 处理请求，ServeMux 路由，ResponseWriter 返回响应

要理解 `net/http`，你只需要搞懂四个核心概念：

1. **HTTP 请求-响应模型**：客户端发请求，服务器回响应，有来有回，童叟无欺。
2. **Handler（处理器）**：一个函数或对象，负责"接单"——处理具体的业务逻辑。
3. **ServeMux（路由器）**：负责"分单"——根据 URL 路径把请求分配给对应的 Handler。
4. **ResponseWriter（响应写入器）**：Handler 用来"发货"——向客户端写入响应内容。

```
┌─────────────────────────────────────────────────────────────┐
│                      HTTP 请求-响应流程                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Client (浏览器)                                           │
│        │                                                    │
│        │  HTTP 请求 (GET /hello HTTP/1.1)                    │
│        ▼                                                    │
│   ┌─────────┐                                               │
│   │ ServeMux │ ◄── URL 路由分发器                            │
│   └────┬────┘                                               │
│        │ /hello → HelloHandler                              │
│        ▼                                                    │
│   ┌─────────┐                                               │
│   │ Handler  │ ◄── 业务逻辑处理者                            │
│   └────┬────┘                                               │
│        │                                                    │
│        ▼                                                    │
│   ResponseWriter.Write()  ──► HTTP 响应 (200 OK + HTML)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**HTTP 的本质**就是一种文本协议。请求和响应都是文本，只是格式有明确规定。你甚至可以手动用 telnet 写一个 HTTP 请求——当然，有了 `net/http`，谁还干这种事呢？

```go
// 这个例子演示了 net/http 的核心工作流程
// 1. 创建 ServeMux（路由器）
// 2. 注册 Handler（处理器）
// 3. 启动服务器
package main

import (
    "fmt"
    "net/http"
)

// HelloHandler 处理 /hello 路径的请求
func HelloHandler(w http.ResponseWriter, r *http.Request) {
    // ResponseWriter 用来写响应
    // *Request 包含请求的所有信息
    fmt.Fprint(w, "你好，HTTP 世界！")
}

func main() {
    // 创建路由器（ ServeMux 是 Go 内置的 HTTP 多路复用器）
    mux := http.NewServeMux()
    
    // 注册处理器：当有人访问 /hello 时，调用 HelloHandler
    mux.HandleFunc("/hello", HelloHandler)
    
    // 启动服务器，监听 8080 端口
    fmt.Println("服务器启动在 http://localhost:8080")
    fmt.Println("访问 http://localhost:8080/hello 看看效果")
    
    // ListenAndServe 是阻塞的，会一直运行直到服务器关闭
    http.ListenAndServe(":8080", mux)
}
```

> **专业词汇解释**
>
> - **HTTP（HyperText Transfer Protocol）**：超文本传输协议，定义了客户端与服务器之间通信的格式。版本从 0.9 进化到 1.0、1.1，再到 2.0 和 3.0。
> - **请求-响应模型（Request-Response Model）**：一种同步交互模式，客户端发起请求后必须等待服务器响应才能继续。
> - **Handler（处理器）**：在 Go 中指实现了 `ServeHTTP(ResponseWriter, *Request)` 方法的任何对象，或 `http.HandlerFunc` 类型的函数。
> - **ServeMux（Server Multiplexer）**：HTTP 请求的多路复用器，根据 URL 路径将请求分发给对应的 Handler。

---

## 21.3 最简 HTTP 服务端：func(w http.ResponseWriter, r *http.Request)

现在让我们写一个**最简单**的 HTTP 服务器。说它"最简"，是因为这大概是使用 Go 写 HTTP 服务所需的最少代码了：

```go
package main

import "net/http"

// 这就是传说中的 Handler 函数签名
// w = ResponseWriter，用来写响应
// r = *Request，包含请求的所有信息
func handler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello, Go HTTP Server!"))
}

func main() {
    // http.HandleFunc 注册一个函数作为 Handler
    // 第一个参数是路径，第二个是处理函数
    http.HandleFunc("/", handler)
    
    // 启动服务器，监听 8080 端口
    // 第二个参数 nil 表示使用默认的 ServeMux
    http.ListenAndServe(":8080", nil)
}
```

运行这段代码，然后在浏览器访问 `http://localhost:8080/`，你就会看到 `Hello, Go HTTP Server!`。

```go
// 输出结果示例（浏览器访问 http://localhost:8080/）
// Hello, Go HTTP Server!
```

> **专业词汇解释**
>
> - **`http.ResponseWriter`**：一个接口，包含三个方法：`Write([]byte) (int, error)`、`WriteHeader(statusCode int)`、`Header() http.Header`。你主要用它来向客户端返回数据。
> - **`*http.Request`**：一个结构体指针，代表一个 HTTP 请求。它包含 `Method`（GET/POST 等）、`URL`、`Header`、`Body`、`Form` 等丰富字段。
> - **Handler 函数签名**：标准形式是 `func(http.ResponseWriter, *http.Request)`，这是 `http.HandlerFunc` 的底层类型。
> - **默认 ServeMux**：`http.HandleFunc` 的第二个参数传 `nil` 时，会使用 `http.DefaultServeMux`，它是 Go 标准库内部维护的一个全局路由器。

---

## 21.4 http.HandleFunc：注册处理函数

`http.HandleFunc` 是我们在 Go 中最常用的注册 Handler 的方式。它的作用是：**把一个 `func(w http.ResponseWriter, r *http.Request)` 函数注册到某个 URL 路径上**。

```go
package main

import (
    "fmt"
    "net/http"
    "time"
)

func timeHandler(w http.ResponseWriter, r *http.Request) {
    // 写入当前时间
    fmt.Fprintf(w, "当前时间：%s", time.Now().Format("2006-01-02 15:04:05"))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "欢迎来到 Go HTTP 服务器！")
}

func aboutHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "这是一个关于页面，关于什么呢？关于 Go 的 net/http 有趣之处！")
}

func main() {
    // 注册多个路径的处理函数
    http.HandleFunc("/", homeHandler)       // 首页
    http.HandleFunc("/time", timeHandler)   // 当前时间
    http.HandleFunc("/about", aboutHandler) // 关于页

    fmt.Println("服务器启动：http://localhost:8080")
    fmt.Println("试试访问：/time 和 /about")
    
    // 启动服务器
    http.ListenAndServe(":8080", nil)
}
```

```go
// 输出示例
// 访问 http://localhost:8080/      → 欢迎来到 Go HTTP 服务器！
// 访问 http://localhost:8080/time  → 当前时间：2024-03-15 14:30:45
// 访问 http://localhost:8080/about → 这是一个关于页面，关于什么呢？关于 Go 的 net/http 有趣之处！
```

### HandleFunc 的底层原理

`http.HandleFunc` 实际上做了两件事：
1. 把你的函数包装成一个 `http.HandlerFunc` 类型（这是函数类型的别名）
2. 调用 `http.Handle(path, handler)` 注册到默认的 `ServeMux` 上

```go
// HandleFunc 的签名是这样的：
// func HandleFunc(pattern string, handler func(ResponseWriter, *Request))

// 内部等价于：
// func HandleFunc(pattern string, handler func(ResponseWriter, *Request)) {
//     Handle(pattern, HandlerFunc(handler))
// }

// HandlerFunc(handler) 把普通函数转型为 http.HandlerFunc
// HandlerFunc 实现了 http.Handler 接口
```

> **专业词汇解释**
>
> - **`http.HandleFunc`**：将一个函数注册为某路径的处理器。函数签名必须是 `func(http.ResponseWriter, *http.Request)`。
> - **`http.HandlerFunc`**：一个类型别名，`type HandlerFunc func(ResponseWriter, *Request)`。它本身实现了 `http.Handler` 接口（通过其 `ServeHTTP` 方法，该方法直接调用自身）。
> - **`fmt.Fprintf` / `fmt.Fprint`**：`Fprint` 系列的 F 代表"File"，即向任何实现了 `io.Writer` 的对象写入。`http.ResponseWriter` 实现了 `io.Writer`，所以可以直接用 `fmt.Fprint`。

---

## 21.5 http.Handle：注册 Handler

`http.Handle` 是另一个注册 Handler 的方式，但它要求传入一个实现了 `http.Handler` 接口的对象，而不仅仅是函数。

这在需要**面向对象**或**共享状态**时特别有用。

```go
package main

import (
    "fmt"
    "net/http"
)

// Counter 是一个状态管理器，统计访问次数
type Counter struct {
    count int
}

// ServeHTTP 方法让 Counter 成为一个 Handler
// 这是 http.Handler 接口的唯一方法
func (c *Counter) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    c.count++
    fmt.Fprintf(w, "你是第 %d 位访客！", c.count)
}

// PageHandler 演示另一种写法——可以携带配置
type PageHandler struct {
    Title   string
    Content string
}

func (p *PageHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "<h1>%s</h1><p>%s</p>", p.Title, p.Content)
}

func main() {
    // 使用 http.Handle 注册实现了 http.Handler 的对象
    http.Handle("/counter", &Counter{})          // 计数器
    http.Handle("/page", &PageHandler{
        Title:   "动态页面",
        Content: "这是一个通过 Handler 对象生成的页面，可以携带配置！",
    })

    fmt.Println("服务器启动：http://localhost:8080")
    fmt.Println("访问 /counter 看看计数效果，访问 /page 看看配置效果")
    
    http.ListenAndServe(":8080", nil)
}
```

```go
// 输出示例
// 访问 http://localhost:8080/counter
// 第一次访问 → 你是第 1 位访客！
// 第二次访问 → 你是第 2 位访客！
// 第三次访问 → 你是第 3 位访客！

// 访问 http://localhost:8080/page
// → <h1>动态页面</h1><p>这是一个通过 Handler 对象生成的页面，可以携带配置！</p>
```

### HandleFunc vs Handle

```
┌──────────────────────────────────────────────────────────────┐
│                    HandleFunc vs Handle                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   http.HandleFunc("/path", myFunc)                          │
│       │                                                      │
│       └──► myFunc 必须是 func(w http.ResponseWriter,        │
│                           r *http.Request)                   │
│       └──► 简单直接，适合无状态的业务逻辑                      │
│                                                              │
│   http.Handle("/path", myHandler)                            │
│       │                                                      │
│       └──► myHandler 必须实现 http.Handler 接口               │
│       └──► 即必须有 ServeHTTP(w http.ResponseWriter,        │
│                            r *http.Request) 方法             │
│       └──► 适合需要共享状态、面向对象、有初始化配置的场景       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 21.6 http.ListenAndServe：启动服务器

`http.ListenAndServe` 是启动 HTTP 服务器的终极函数。它做了三件事：

1. 在指定的地址（形如 `:8080`）上监听 TCP 连接
2. 启动一个无限循环，接受连接
3. 把每个连接交给 ServeMux 分发处理

```go
package main

import (
    "fmt"
    "log"
    "net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello from ListenAndServe!")
}

func main() {
    // 注册处理器
    http.HandleFunc("/hello", helloHandler)

    fmt.Println("=== 启动 HTTP 服务器 ===")
    fmt.Println("监听地址：:8080")
    fmt.Println("按 Ctrl+C 停止服务器")

    // ListenAndServe 返回一个 error
    // 如果出错（比如端口被占用），会打印出来
    // 如果正常关闭（比如调用了 Shutdown），返回 nil
    err := http.ListenAndServe(":8080", nil)
    if err != nil {
        log.Fatalf("服务器启动失败：%v", err)
    }
}
```

```go
// 运行后终端输出：
// === 启动 HTTP 服务器 ===
// 监听地址：:8080
// 按 Ctrl+C 停止服务器
// [浏览器访问后] 127.0.0.1:59834: GET /hello HTTP/1.1 → 200
```

### ListenAndServe 的变体

```go
// 标准启动（使用默认 ServeMux）
http.ListenAndServe(":8080", nil)

// 指定自定义 ServeMux
mux := http.NewServeMux()
http.ListenAndServe(":8080", mux)

// 使用自定义 Server 结构体（更多配置，见 21.22 节）
srv := &http.Server{
    Addr:         ":8080",
    Handler:      mux,
    ReadTimeout:  10 * time.Second,
    WriteTimeout: 10 * time.Second,
}
srv.ListenAndServe()
```

> **专业词汇解释**
>
> - **`ListenAndServe`**：函数签名 `func(addr string, handler Handler) error`。它是一个阻塞调用，正常情况下只有遇到错误或被中断才会返回。
> - **TCP 监听**：调用底层的 `net.Listen("tcp", addr)` 创建一个 TCP socket 监听器。
> - **`log.Fatalf`**：打印格式化的日志后以退出码 1 终止程序。`Fatal` 系列函数会在输出后调用 `os.Exit(1)`。

---

## 21.7 ServeMux：HTTP 路由器，按路径匹配

ServeMux（Server Multiplexer，服务多路复用器）是 `net/http` 的**路由核心**。你可以把它想象成一个大堂经理——客人进门（大堂），问"我要去会议室 A"，大堂经理就指向正确的会议室（Handler）。

```go
package main

import (
    "fmt"
    "net/http"
)

// 不同的处理器
func homeHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "首页 - 这里是 Go HTTP 服务器！")
}

func productsHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "产品列表 - 我们有超棒的 Go 课程！")
}

func contactHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "联系我们 - 发邮件到 hi@example.com")
}

func main() {
    // 创建一个新的 ServeMux（路由器）
    mux := http.NewServeMux()

    // 注册路由规则
    mux.HandleFunc("/", homeHandler)           // 根路径
    mux.HandleFunc("/products", productsHandler) // /products
    mux.HandleFunc("/contact", contactHandler)  // /contact

    fmt.Println("ServeMux 路由演示服务器启动：http://localhost:8080")
    fmt.Println("可访问路径：/, /products, /contact")

    // 启动服务器，传入自定义的 mux
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// 访问 http://localhost:8080/        → 首页 - 这里是 Go HTTP 服务器！
// 访问 http://localhost:8080/products → 产品列表 - 我们有超棒的 Go 课程！
// 访问 http://localhost:8080/contact → 联系我们 - 发邮件到 hi@example.com
```

### ServeMux 的工作原理

```
┌────────────────────────────────────────────────────────────┐
│                      ServeMux 工作流程                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   HTTP 请求：GET /products/new                             │
│                         │                                  │
│                         ▼                                  │
│              ┌─────────────────┐                           │
│              │     ServeMux     │                           │
│              │  (路由匹配器)     │                           │
│              └────────┬────────┘                           │
│                       │                                    │
│        ┌──────────────┼──────────────┐                    │
│        ▼              ▼              ▼                     │
│   /products    /products/new    /contact                   │
│   Handler A    Handler B        Handler C                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

> **专业词汇解释**
>
> - **`http.ServeMux`**：HTTP 请求多路复用器，负责将请求 URL 映射到对应的 Handler。它内部维护一个 map，key 是 URL 路径模式，value 是 Handler。
> - **路由（Routing）**：根据请求的路径（和其他条件）决定由哪个 Handler 来处理请求的过程。
> - **`http.NewServeMux()`**：创建一个全新的 ServeMux 实例，而不是使用全局的 `DefaultServeMux`。推荐在生产环境中使用自定义 ServeMux，避免全局状态带来的意外。

---

## 21.8 路由匹配规则：最长路径优先

这是 ServeMux 最重要的匹配规则：**当有多个路由模式都能匹配一个请求路径时，ServeMux 会选择最长（最具体）的那个**。

```go
package main

import (
    "fmt"
    "net/http"
)

func rootHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Handler: /  (根路径)")
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Handler: /hello  (hello路径)")
}

func helloNameHandler(w http.ResponseWriter, r *http.Request) {
    // 从 URL 中提取名字
    name := r.URL.Path[len("/hello/"):]
    fmt.Fprintf(w, "Handler: /hello/%s  (具体名字路径)", name)
}

func main() {
    mux := http.NewServeMux()

    // 关键点：注册顺序不影响匹配结果
    // ServeMux 总是选择最长匹配的路径
    mux.HandleFunc("/", rootHandler)
    mux.HandleFunc("/hello", helloHandler)        // 匹配 /hello
    mux.HandleFunc("/hello/", helloNameHandler)   // 匹配 /hello/*

    fmt.Println("路由匹配规则演示：http://localhost:8080")
    fmt.Println("最长路径优先匹配！")

    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// 访问 http://localhost:8080/         → Handler: /  (根路径)
// 访问 http://localhost:8080/hello    → Handler: /hello  (hello路径)
// 访问 http://localhost:8080/hello/Alice → Handler: /hello/Alice  (具体名字路径)
// 访问 http://localhost:8080/hello/Bob   → Handler: /hello/Bob  (具体名字路径)
```

### 匹配规则图解

```
请求路径: /hello/Alice

匹配候选：
  /           → 匹配，长度 1
  /hello      → 匹配，长度 6
  /hello/     → 匹配，长度 7
  /hello/Alice → 匹配，长度 13  ◄── 最长！胜出！

优先级 = 路径长度（字节数），越长越优先
```

> **专业词汇解释**
>
> - **最长路径优先（Longest Path Matching）**：ServeMux 使用最长前缀匹配（longest prefix match）。这意味着 `/hello/Alice` 会先尝试匹配 `/hello/Alice`，再尝试 `/hello/`，再 `/hello`，再 `/`。
> - **路径分隔符**：`/` 是路径分隔符，`/hello` 和 `/hello/` 在 Go 的 ServeMux 中是**不同的模式**。`/hello` 匹配 `/hello` 但**不匹配** `/hello/`。

---

## 21.9 http.Handler 接口：ServeHTTP(ResponseWriter, *Request)

`http.Handler` 是整个 `net/http` 包的核心接口。它极其简单——只需要实现一个方法：

```go
// 源码（net/http 包定义）
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

就这一个方法！简单到令人发指，但威力无穷。

```go
package main

import (
    "fmt"
    "net/http"
    "strings"
    "time"
)

// UppercaseHandler 将请求体转换为大写
type UppercaseHandler struct{}

func (h *UppercaseHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // 从请求体读取内容
    body := r.PostFormValue("text")
    if body != "" {
        fmt.Fprint(w, strings.ToUpper(body))
    } else {
        fmt.Fprint(w, "请在 POST 请求的 form 中提交 text 参数")
    }
}

// TimeStampHandler 返回当前时间戳
type TimeStampHandler struct{}

func (h *TimeStampHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "服务器当前时间戳：%d", time.Now().Unix())
}

// 演示：普通函数如何适配 Handler 接口
type StatusHandler struct {
    statusCode int
    message    string
}

func (h *StatusHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(h.statusCode)
    fmt.Fprint(w, h.message)
}

func main() {
    mux := http.NewServeMux()

    // 注册实现 Handler 接口的类型
    mux.Handle("/uppercase", &UppercaseHandler{})
    mux.Handle("/timestamp", &TimeStampHandler{})
    mux.Handle("/notfound", &StatusHandler{404, "哎呀，页面走丢了！"})
    mux.Handle("/teapot", &StatusHandler{418, "我是一个茶壶 🫖"})

    fmt.Println("Handler 接口演示：http://localhost:8080")
    fmt.Println("/uppercase - POST 提交 text，返回大写")
    fmt.Println("/timestamp - 返回当前时间戳")
    fmt.Println("/notfound  - 返回 404")
    fmt.Println("/teapot    - 返回 418")

    http.ListenAndServe(":8080", mux)
}
```

```go
// 测试方式
// curl -X POST -d "text=hello world" http://localhost:8080/uppercase
// → HELLO WORLD

// curl http://localhost:8080/timestamp
// → 服务器当前时间戳：1710000000

// curl -i http://localhost:8080/notfound
// → HTTP/1.1 404
// → 哎呀，页面走丢了！

// curl -i http://localhost:8080/teapot
// → HTTP/1.1 418
// → 我是一个茶壶 🫖
```

### Handler 接口的"魔力"

```
┌──────────────────────────────────────────────────────────────┐
│                    Handler 接口的灵活性                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   任何实现了 ServeHTTP(ResponseWriter, *Request) 的类型       │
│   都是一个 Handler，可以注册到 ServeMux 上                   │
│                                                              │
│   这意味着：                                                 │
│   • 可以是结构体（携带配置和状态）                             │
│   • 可以是函数对象（通过闭包共享状态）                          │
│   • 可以是装饰器包装后的 Handler（中间件模式）                  │
│   • 甚至可以是另一个 ServeMux（嵌套路由）                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 21.10 http.HandlerFunc：函数适配为 Handler

`http.HandlerFunc` 是一个**类型别名**，但它的存在意义非凡——它让**普通函数**可以**直接成为 Handler**。

```go
// 源码本质（简化的理解）
type HandlerFunc func(ResponseWriter, *Request)

// HandlerFunc 实现了 Handler 接口！
func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
    f(w, r)  // 调用的就是函数自身
}
```

```go
package main

import (
    "fmt"
    "net/http"
    "strings"
)

func main() {
    mux := http.NewServeMux()

    // 方法一：直接传入普通函数（HandleFunc 内部会转为 HandlerFunc）
    mux.HandleFunc("/greet", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "你好，陌生人！")
    })

    // 方法二：显式使用 HandlerFunc 转型（等价，但更显式）
    // 这在需要把函数作为参数传递时很有用
    greetFunc := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "显式 HandlerFunc 版本：你好啊！")
    })
    mux.Handle("/greet-explicit", greetFunc)

    // 方法三：把已定义的函数赋值给 HandlerFunc 类型
    uppercase := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        text := r.URL.Query().Get("text")
        fmt.Fprint(w, strings.ToUpper(text))
    })
    mux.Handle("/uppercase", uppercase)

    fmt.Println("HandlerFunc 演示：http://localhost:8080")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// 访问 http://localhost:8080/greet           → 你好，陌生人！
// 访问 http://localhost:8080/greet-explicit  → 显式 HandlerFunc 版本：你好啊！
// 访问 http://localhost:8080/uppercase?text=hello → HELLO
```

### HandlerFunc 转型图解

```
┌─────────────────────────────────────────────────────────────┐
│                   HandlerFunc 转型过程                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   普通函数：                                                 │
│   func myHandler(w http.ResponseWriter, r *http.Request)   │
│                                                             │
│              │                                              │
│              │ http.HandlerFunc()                           │
│              ▼                                              │
│                                                             │
│   HandlerFunc 类型（函数本身的值）：                          │
│   http.HandlerFunc(myHandler)                               │
│                                                             │
│              │                                              │
│              │ 实现了 ServeHTTP 方法                        │
│              ▼                                              │
│                                                             │
│   http.Handler 接口实现！                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 21.11 http.NotFoundHandler、http.RedirectHandler：常用 Handler

Go 标准库贴心地为我们准备了一些**开箱即用的 Handler**，无需任何配置，直接注册就能用。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    // NotFoundHandler：返回 404 Not Found
    // 相当于 w.WriteHeader(404) + 写一个默认的 404 页面
    mux.Handle("/missing", http.NotFoundHandler())

    // RedirectHandler：重定向到另一个 URL
    // 参数：目标 URL，重定向状态码（301/302/303/307/308）
    mux.Handle("/old-page", http.RedirectHandler("http://localhost:8080/new-page", 302))
    mux.Handle("/new-page", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "欢迎来到新页面！你被重定向了。")
    }))

    // RedirectFunc：更简洁的函数式写法
    mux.HandleFunc("/home", func(w http.ResponseWriter, r *http.Request) {
        http.Redirect(w, r, "/new-page", 301)
    })

    fmt.Println("常用 Handler 演示：http://localhost:8080")
    fmt.Println("/missing   → 404 Not Found")
    fmt.Println("/old-page  → 302 重定向到 /new-page")
    fmt.Println("/home      → 301 重定向到 /new-page")

    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl -i http://localhost:8080/missing
// → HTTP/1.1 404 Not Found
// → Content-Type: text/plain; charset=utf-8
// → 404 page not found

// curl -i http://localhost:8080/old-page
// → HTTP/1.1 302 Found
// → Location: http://localhost:8080/new-page
// → (跟随重定向后) → 欢迎来到新页面！你被重定向了。
```

### 常见 Handler 一览

| Handler | 用途 | 示例 |
|---------|------|------|
| `NotFoundHandler` | 返回 404 | 资源不存在 |
| `RedirectHandler(url, code)` | 重定向 | 页面迁移 |
| `StripPrefix(prefix, handler)` | 剥离路径前缀 | 静态文件服务 |
| `TimeoutHandler(handler, duration, msg)` | 超时控制 | 防止慢请求 |
| `FileServer(root)` | 静态文件服务 | 托管文件目录 |
| `RedirectFunc(url, code)` | 函数式重定向 | HandlerFunc 版本 |

---

## 21.12 http.StripPrefix：剥离路径前缀，用于静态文件服务

`http.StripPrefix` 是一个**修饰器型 Handler**，它的工作是：把请求路径的指定前缀"削掉"，然后把请求转发给下一个 Handler。

这在托管静态文件时超级有用——当你的文件在 `/static/` 下，但实际文件在文件系统的某个目录时，就需要 StripPrefix 来"脱掉"前缀。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    // 假设请求 /static/css/style.css
    // StripPrefix("/static", handler) 会：
    // 1. 把 "/static" 前缀去掉
    // 2. 把剩余路径 "/css/style.css" 交给 handler 处理
    // 3. handler 会去它的 root 目录（当前目录）下找 /css/style.css

    // 这里用一个简单的 Handler 演示（实际应该用 FileServer，见 21.14）
    mux.Handle("/static/", http.StripPrefix("/static/",
        http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            fmt.Fprintf(w, "你请求的文件路径（去除 /static 前缀后）: %s", r.URL.Path)
        }),
    ))

    fmt.Println("StripPrefix 演示：http://localhost:8080")
    fmt.Println("/static/css/style.css → 剥去 /static → 你请求的文件路径（去除 /static 前缀后）: /css/style.css")

    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// 访问 http://localhost:8080/static/css/style.css
// → 你请求的文件路径（去除 /static 前缀后）: /css/style.css
```

### StripPrefix 工作原理

```
请求路径: /static/images/logo.png

            ┌────────────────────┐
            │    StripPrefix     │
            │   ("/static", h)   │
            └────────┬───────────┘
                     │
    去掉前缀 "/static" │ r.URL.Path = "/images/logo.png"
                     ▼
            ┌────────────────────┐
            │   下游 Handler      │
            │  (处理 /images/*)   │
            └────────────────────┘
```

---

## 21.13 http.TimeoutHandler：超时包装器

`http.TimeoutHandler` 是一个 Handler 包装器，它给下游 Handler 加上了**超时限制**。如果 Handler 在指定时间内没有完成响应，就会自动终止并返回错误。

这对于防止慢查询、烂代码占用连接特别有用。

```go
package main

import (
    "fmt"
    "net/http"
    "time"
)

func slowHandler(w http.ResponseWriter, r *http.Request) {
    duration := r.URL.Query().Get("wait")
    if duration == "" {
        duration = "5s"
    }
    d, _ := time.ParseDuration(duration)
    fmt.Printf("慢请求开始，要等 %s...\n", d)
    time.Sleep(d)
    fmt.Fprintf(w, "终于等到你了！等了 %s 才返回。", d)
}

func fastHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "快到没朋友！毫秒级响应！")
}

func main() {
    mux := http.NewServeMux()

    // 包装：最多只给 slowHandler 2 秒时间
    // 超时后返回 503 Service Unavailable
    mux.Handle("/slow",
        http.TimeoutHandler(
            http.HandlerFunc(slowHandler),
            2*time.Second,
            "请求超时了，老兄！503 Service Unavailable",
        ))

    // 这个不会超时
    mux.HandleFunc("/fast", fastHandler)

    fmt.Println("TimeoutHandler 演示：http://localhost:8080")
    fmt.Println("/slow?wait=5s → 等 5 秒 → 超时（最多 2 秒）→ 503")
    fmt.Println("/slow?wait=1s → 等 1 秒 → 成功返回")
    fmt.Println("/fast         → 立即返回")

    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl http://localhost:8080/slow?wait=5s
// → 请求超时了，老兄！503 Service Unavailable
// （约 2 秒后返回）

// curl http://localhost:8080/slow?wait=1s
// → 终于等到你了！等了 1s 才返回。

// curl http://localhost:8080/fast
// → 快到没朋友！毫秒级响应！
```

> **警告**：TimeoutHandler 会调用 `w.WriteHeader(http.StatusServiceUnavailable)` 和 `w.Write()` 来写入超时响应。如果下游 Handler 已经写入了部分响应，再超时时可能会导致 `http: superfluous response.WriteHeader` 警告。所以 TimeoutHandler 适合幂等的读请求，写请求要慎用。

---

## 21.14 http.FileServer：开箱即用的静态文件服务器

终于到了你最期待的部分！`http.FileServer` 就是那个让你用**一行代码**就能搭建完整静态文件服务器的神器。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    // FileServer 接收一个 http.Dir 类型参数（就是文件系统路径）
    // 它会托管该目录下的所有文件
    // 当前目录下的 static/ 目录作为静态文件根目录
    mux.Handle("/static/",
        http.StripPrefix("/static/",
            http.FileServer(http.Dir("."))))

    fmt.Println("FileServer 演示服务器启动：http://localhost:8080")
    fmt.Println("访问 /static/<filename> 查看文件")
    fmt.Println("例如：http://localhost:8080/static/index.html")
    fmt.Println("(确保当前目录下有 static 目录和文件)")

    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// 目录结构：
// .
// ├── main.go
// └── static/
//     ├── index.html
//     └── css/
//         └── style.css

// curl http://localhost:8080/static/index.html
// → (返回 index.html 的内容)

// curl http://localhost:8080/static/css/style.css
// → (返回 style.css 的内容)

// curl http://localhost:8080/static/nonexistent.txt
// → 404 page not found
```

### FileServer + StripPrefix 组合拳

```
┌────────────────────────────────────────────────────────────┐
│              FileServer + StripPrefix 组合                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   客户端请求: GET /static/css/style.css                    │
│                                                            │
│                    │                                       │
│                    ▼                                       │
│         ┌──────────────────┐                               │
│         │   StripPrefix    │                               │
│         │  "/static/"      │                               │
│         │  去掉前缀         │                               │
│         └────────┬─────────┘                               │
│                  │ /css/style.css                           │
│                  ▼                                         │
│         ┌──────────────────┐                               │
│         │   FileServer     │                               │
│         │  (http.Dir(".")) │                               │
│         │  从当前目录找文件  │                               │
│         └──────────────────┘                               │
│                  │                                         │
│                  ▼                                         │
│         ./css/style.css ← 找到这个文件！                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 21.15 ResponseWriter.Write：写入响应体

`http.ResponseWriter` 的 `Write` 方法是往客户端发送数据的最基本方式。当你调用 `Write(data)` 时，数据会被写入**响应体（Response Body）**。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/text", func(w http.ResponseWriter, r *http.Request) {
        // Write 接收 []byte，可以是文本也可以是二进制
        w.Write([]byte("这是一段纯文本响应"))
    })

    mux.HandleFunc("/html", func(w http.ResponseWriter, r *http.Request) {
        // 默认 Content-Type 是 text/plain
        // 如果返回 HTML，最好设置一下 Content-Type
        w.Header().Set("Content-Type", "text/html; charset=utf-8")
        w.Write([]byte("<h1>HTML 响应</h1><p>这是一个 HTML 页面</p>"))
    })

    mux.HandleFunc("/json", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.Write([]byte(`{"message": "你好，世界！", "code": 200}`))
    })

    mux.HandleFunc("/bytes", func(w http.ResponseWriter, r *http.Request) {
        // Write 可以写入任意字节数据
        data := []byte{0x48, 0x65, 0x6C, 0x6C, 0x6F} // "Hello" 的字节
        w.Write(data)
    })

    fmt.Println("ResponseWriter.Write 演示：http://localhost:8080")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl http://localhost:8080/text
// → 这是一段纯文本响应

// curl http://localhost:8080/html
// → <h1>HTML 响应</h1><p>这是一个 HTML 页面</p>

// curl -H "Accept: application/json" http://localhost:8080/json
// → {"message": "你好，世界！", "code": 200}
```

> **小贴士**：当你第一次调用 `Write` 时，如果还没有调用 `WriteHeader`，Go 会自动设置一个默认的 `200 OK` 状态码，然后才发送响应头。

---

## 21.16 ResponseWriter.WriteHeader：发送响应头

`WriteHeader` 用来**显式发送 HTTP 状态码**。如果你不调用它，Go 会默认发送 `200 OK`。

什么时候需要手动调用 `WriteHeader`？当你返回**非 200** 的状态码时，比如 `404 Not Found`、`500 Internal Server Error`、`302 Found`（重定向）等。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/ok", func(w http.ResponseWriter, r *http.Request) {
        // 默认 200 OK，不需要显式调用
        fmt.Fprint(w, "一切正常！")
    })

    mux.HandleFunc("/not-found", func(w http.ResponseWriter, r *http.Request) {
        // 必须先 WriteHeader，再 Write
        w.WriteHeader(http.StatusNotFound) // 404
        fmt.Fprint(w, "404 - 页面走丢了！")
    })

    mux.HandleFunc("/server-error", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusInternalServerError) // 500
        fmt.Fprint(w, "500 - 服务器爆炸了！💥")
    })

    mux.HandleFunc("/custom", func(w http.ResponseWriter, r *http.Request) {
        // 429 = Too Many Requests
        w.WriteHeader(429)
        fmt.Fprint(w, "慢点慢点，你请求太快了！")
    })

    fmt.Println("WriteHeader 演示：http://localhost:8080")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl -i http://localhost:8080/not-found
// → HTTP/1.1 404 Not Found
// → Content-Type: text/plain; charset=utf-8
// → 404 - 页面走丢了！

// curl -i http://localhost:8080/custom
// → HTTP/1.1 429 Unknown Status
// → Content-Type: text/plain; charset=utf-8
// → 慢点慢点，你请求太快了！
```

> **注意**：`WriteHeader` 只能调用**一次**！第二次调用会导致 panic：`http: multiple response.WriteHeader calls`。所以写数据时，先 `WriteHeader`，再 `Write`。

---

## 21.17 ResponseWriter.Header：响应头映射

`ResponseWriter.Header()` 返回一个 `http.Header` 类型的映射（本质上就是 `map[string][]string`）。通过它你可以设置、读取、删除响应头。

```go
package main

import (
    "fmt"
    "net/http"
    "time"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/headers", func(w http.ResponseWriter, r *http.Request) {
        h := w.Header()

        // 设置各种响应头
        h.Set("Content-Type", "text/plain; charset=utf-8")
        h.Set("X-Custom-Header", "Hello from Go!")
        h.Set("X-Server-Name", "Go-HTTP-Server/1.0")

        // 设置缓存头
        h.Set("Cache-Control", "max-age=3600")
        h.Set("Expires", time.Now().Add(time.Hour).Format(http.TimeFormat))

        // 设置 CORS 头
        h.Set("Access-Control-Allow-Origin", "*")
        h.Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")

        // 追加多个值的响应头（同一 key 可以有多个 value）
        h.Add("X-Debug", "handler=headers")
        h.Add("X-Debug", "timestamp="+time.Now().Format(time.RFC3339))

        fmt.Fprint(w, "响应头已设置，用 curl -i 查看")
    })

    mux.HandleFunc("/read-headers", func(w http.ResponseWriter, r *http.Request) {
        // 读取请求头
        userAgent := r.Header.Get("User-Agent")
        accept := r.Header.Get("Accept")

        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintf(w, "User-Agent: %s\nAccept: %s\n", userAgent, accept)

        // 遍历所有请求头
        fmt.Fprintln(w, "\n--- 所有请求头 ---")
        for key, values := range r.Header {
            fmt.Fprintf(w, "%s: %s\n", key, values)
        }
    })

    fmt.Println("Header 演示：http://localhost:8080")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl -i http://localhost:8080/headers
// → HTTP/1.1 200 OK
// → Content-Type: text/plain; charset=utf-8
// → X-Custom-Header: Hello from Go!
// → X-Server-Name: Go-HTTP-Server/1.0
// → Cache-Control: max-age=3600
// → Access-Control-Allow-Origin: *
// → X-Debug: handler=headers
// → X-Debug: timestamp=2024-03-15T10:30:00+08:00
// →
// → 响应头已设置，用 curl -i 查看

// curl -i -H "User-Agent: MyClient/1.0" http://localhost:8080/read-headers
// → User-Agent: MyClient/1.0
// → Accept: */*
```

### http.Header 常用方法

| 方法 | 说明 |
|------|------|
| `Set(key, value)` | 设置一个响应头（会覆盖同 key 的所有值） |
| `Add(key, value)` | 添加一个响应头（同 key 可以有多个值） |
| `Get(key)` | 获取第一个值 |
| `Values(key)` | 获取所有值（`[]string`） |
| `Del(key)` | 删除该 key 的所有值 |
| `Write(w)` | 把所有头写入 io.Writer（用于内部协议处理） |

---

## 21.18 Request.Method、Request.URL、Request.Header、Request.Body：请求信息

`http.Request` 结构体包含了客户端请求的所有信息。下面我们来一一拆解。

```go
package main

import (
    "fmt"
    "io"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/info", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain; charset=utf-8")

        // Method: GET, POST, PUT, DELETE, etc.
        fmt.Fprintf(w, "Method: %s\n", r.Method)

        // URL: 请求的 URL 路径和查询参数
        fmt.Fprintf(w, "URL: %s\n", r.URL.String())
        fmt.Fprintf(w, "Path: %s\n", r.URL.Path)
        fmt.Fprintf(w, "RawQuery: %s\n", r.URL.RawQuery)

        // Proto: HTTP 协议版本
        fmt.Fprintf(w, "Proto: %s\n", r.Proto)

        // Host: 目标主机
        fmt.Fprintf(w, "Host: %s\n", r.Host)

        // RemoteAddr: 客户端 IP 地址
        fmt.Fprintf(w, "RemoteAddr: %s\n", r.RemoteAddr)

        fmt.Fprintln(w, "\n--- 请求头 ---")
        for key, values := range r.Header {
            fmt.Fprintf(w, "%s: %s\n", key, values)
        }
    })

    mux.HandleFunc("/body", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")

        // Body: 请求体（io.ReadCloser，需要自己读取）
        // 记得读取后关闭
        defer r.Body.Close()

        body, err := io.ReadAll(r.Body)
        if err != nil {
            w.WriteHeader(http.StatusBadRequest)
            fmt.Fprint(w, "读取请求体失败")
            return
        }

        fmt.Fprintf(w, "Body 长度: %d 字节\n", len(body))
        fmt.Fprintf(w, "Body 内容: %s\n", string(body))
    })

    fmt.Println("Request 信息解析演示：http://localhost:8080")
    fmt.Println("访问 /info 查看请求信息，/body 读取 POST 请求体")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl -X POST -H "Content-Type: text/plain" \
//      -d "Hello, Go!" http://localhost:8080/info
// → Method: POST
// → URL: /info
// → Path: /info
// → Proto: HTTP/1.1
// → Host: localhost:8080
// → RemoteAddr: 127.0.0.1:54321
// →
// --- 请求头 ---
// Content-Type: text/plain
// User-Agent: curl/8.1.2
// Accept: */*

// curl -X POST -d "Hello, Go!" http://localhost:8080/body
// → Body 长度: 10 字节
// → Body 内容: Hello, Go!
```

### Request 核心字段一览

| 字段 | 类型 | 说明 |
|------|------|------|
| `Method` | `string` | HTTP 方法：GET、POST、PUT、DELETE 等 |
| `URL` | `*url.URL` | 请求的 URL（包含 Path、RawQuery 等） |
| `Header` | `http.Header` | 请求头映射 |
| `Body` | `io.ReadCloser` | 请求体（需要 Read 和 Close） |
| `Host` | `string` | 请求的目标主机 |
| `RemoteAddr` | `string` | 客户端地址（IP:Port） |
| `Proto` | `string` | HTTP 协议版本，如 "HTTP/1.1" |
| `Form` | `url.Values` | 表单数据（自动解析） |
| `PostForm` | `url.Values` | 仅 POST 表单数据 |
| `Cookies()` | `[]*http.Cookie` | 所有 Cookie |
| `Context()` | `context.Context` | 请求级别的 Context |

---

## 21.19 Request.Form：URL 查询参数和 POST 表单

`Request.Form` 是一个 `url.Values` 类型（本质是 `map[string][]string`），它能自动解析：
- URL 中的查询参数（`?key=value`）
- POST 表单中的数据（`application/x-www-form-urlencoded`）

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/search", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain; charset=utf-8")

        // ParseForm() 会解析 URL 查询参数和 POST 表单数据
        // 如果不调用，直接访问 Form 会返回空值
        if err := r.ParseForm(); err != nil {
            fmt.Fprintf(w, "解析失败：%v", err)
            return
        }

        fmt.Fprintln(w, "=== Form（查询参数 + POST 表单）===")
        fmt.Fprintf(w, "q: %v\n", r.Form["q"])
        fmt.Fprintf(w, "category: %v\n", r.Form["category"])

        // PostForm 只包含 POST 表单数据（不包含 URL 查询参数）
        fmt.Fprintln(w, "\n=== PostForm（仅 POST 表单）===")
        fmt.Fprintf(w, "username: %v\n", r.PostForm["username"])
        fmt.Fprintf(w, "password: %v\n", r.PostForm["password"])

        // 单值快捷方式
        fmt.Fprintln(w, "\n=== 快捷取值 ===")
        fmt.Fprintf(w, "q (第一个): %s\n", r.FormValue("q"))
        fmt.Fprintf(w, "username (第一个): %s\n", r.PostFormValue("username"))
    })

    fmt.Println("Form 演示：http://localhost:8080")
    fmt.Println("GET /search?q=golang&category=tech     → 查询参数")
    fmt.Println("POST /search q=golang category=tech    → 表单数据")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// GET 请求
// curl "http://localhost:8080/search?q=golang&category=tech"
// → === Form（查询参数 + POST 表单）===
// → q: [golang]
// → category: [tech]
// → === PostForm（仅 POST 表单）===
// → username: []
// → password: []
// → === 快捷取值 ===
// → q (第一个): golang

// POST 表单请求
// curl -X POST -d "q=golang&category=tech&username=alice" http://localhost:8080/search
// → === Form ===
// → q: [golang]
// → category: [tech]
// → username: [alice]
// → === PostForm ===
// → username: [alice]
```

> **注意**：对于 `multipart/form-data`（文件上传），需要用 `r.ParseMultipartForm()` 然后访问 `r.Form["key"]` 或 `r.MultipartForm`。

---

## 21.20 Request.Cookie：读取 Cookie

HTTP 是无状态协议，Cookie 就是在无状态的世界里打的一个有状态的补丁。`Request.Cookie()` 和 `Request.Cookies()` 用来读取客户端携带的 Cookie。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/read-cookies", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain; charset=utf-8")

        // 读取指定名称的 Cookie
        username, err := r.Cookie("username")
        if err != nil {
            fmt.Fprintf(w, "username Cookie 不存在: %v\n", err)
        } else {
            fmt.Fprintf(w, "username Cookie: %s\n", username.Value)
        }

        sessionID, err := r.Cookie("session_id")
        if err != nil {
            fmt.Fprintf(w, "session_id Cookie 不存在: %v\n", err)
        } else {
            fmt.Fprintf(w, "session_id Cookie: %s\n", sessionID.Value)
        }

        // 读取所有 Cookie
        fmt.Fprintln(w, "\n--- 所有 Cookies ---")
        for _, c := range r.Cookies() {
            fmt.Fprintf(w, "%s = %s\n", c.Name, c.Value)
        }
    })

    mux.HandleFunc("/set-cookie", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain; charset=utf-8")

        // 设置 Cookie（通过 Set-Cookie 响应头）
        cookie := &http.Cookie{
            Name:     "username",
            Value:    "alice",
            Path:     "/",
            HttpOnly: true, // 不允许 JavaScript 访问（防 XSS）
            SameSite: http.SameSiteLaxMode,
            MaxAge:   3600, // 1 小时
        }
        http.SetCookie(w, cookie)

        fmt.Fprintln(w, "Cookie 已设置！")
        fmt.Fprintln(w, "请访问 /read-cookies 查看")
    })

    fmt.Println("Cookie 演示：http://localhost:8080")
    fmt.Println("1. 访问 /set-cookie 设置 Cookie")
    fmt.Println("2. 访问 /read-cookies 读取 Cookie")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// 第一步：设置 Cookie
// curl -i http://localhost:8080/set-cookie
// → HTTP/1.1 200 OK
// → Set-Cookie: username=alice; Path=/; HttpOnly; Max-Age=3600
// → Cookie 已设置！

// 第二步：读取 Cookie（带上刚才的 Cookie）
// curl -i --cookie "username=alice;session_id=abc123" http://localhost:8080/read-cookies
// → username Cookie: alice
// → session_id Cookie: abc123
// → --- 所有 Cookies ---
// → username = alice
// → session_id = abc123
```

> **专业词汇解释**
>
> - **Cookie**：服务器发送到用户浏览器并存储在本地的小段数据。下次请求时浏览器会自动带上，用于识别用户状态。
> - **HttpOnly**：设置为 true 时，Cookie 无法被 JavaScript 的 `document.cookie` 访问，可防止 XSS 攻击盗取 Cookie。
> - **SameSite**：防止 CSRF 攻击。`SameSiteLaxMode`（Lax）允许从外部链接导航到本站时携带 Cookie，但不允许跨域 POST。

---

## 21.21 Request.WithContext：创建带新 Context 的请求副本

在 Go 中，`Context`（上下文）是用于**传递请求级别元数据**、**截止时间**和**取消信号**的机制。`Request.WithContext` 用于创建一个**新的请求副本**，但带上不同的 Context。

```go
package main

import (
    "context"
    "fmt"
    "net/http"
    "time"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/normal", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintf(w, "普通请求，Context: %v", r.Context())
    })

    mux.HandleFunc("/with-timeout", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")

        // 创建 2 秒超时的 Context
        ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
        defer cancel() // 很重要：防止内存泄漏

        // 创建带新 Context 的请求副本
        newReq := r.WithContext(ctx)

        // 模拟处理（使用新 Context）
        select {
        case <-newReq.Context().Done():
            fmt.Fprintf(w, "超时了！错误: %v", newReq.Context().Err())
        case <-time.After(1 * time.Second):
            fmt.Fprintf(w, "1秒后完成，使用了带超时的 Context: %v", newReq.Context())
        }
    })

    mux.HandleFunc("/with-value", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")

        // 创建带值的 Context（用于传递请求级别数据）
        ctx := context.WithValue(r.Context(), "user_id", "alice123")
        ctx = context.WithValue(ctx, "trace_id", "trace-xyz-789")
        newReq := r.WithContext(ctx)

        // 在 Handler 的其他地方可以通过 newReq.Context() 获取
        userID := newReq.Context().Value("user_id")
        traceID := newReq.Context().Value("trace_id")

        fmt.Fprintf(w, "user_id=%v, trace_id=%v", userID, traceID)
    })

    fmt.Println("WithContext 演示：http://localhost:8080")
    http.ListenAndServe(":8080", mux)
}
```

```go
// 输出示例
// curl http://localhost:8080/normal
// → 普通请求，Context: context.Background

// curl http://localhost:8080/with-timeout
// → 1秒后完成，使用了带超时的 Context: context.Background

// curl "http://localhost:8080/with-timeout?wait=3"
// (等待 2 秒后)
// → 超时了！错误: context deadline exceeded

// curl http://localhost:8080/with-value
// → user_id=alice123, trace_id=trace-xyz-789
```

### Context 传递链

```
┌────────────────────────────────────────────────────────────┐
│                    Context 传递链                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   原始请求 Context                                          │
│         │                                                  │
│         │ context.WithTimeout(2s)                         │
│         ▼                                                  │
│   带超时的 Context                                          │
│         │                                                  │
│         │ context.WithValue("user_id", "alice")           │
│         ▼                                                  │
│   带值的 Context → r.WithContext(ctx) → 新请求副本         │
│                                                            │
│   新请求副本可以在后续的 Handler、数据库查询、日志等处        │
│   通过 r.Context().Value("user_id") 获取传递的值           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 21.22 Server：服务器配置，Addr、Handler、ReadTimeout、WriteTimeout

`http.Server` 是 `http.ListenAndServe` 的"增强版"。它允许我们配置服务器的各种参数，而不是只能用默认配置。

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "time"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "你好！")
    })

    mux.HandleFunc("/slow", func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(5 * time.Second)
        fmt.Fprint(w, "终于醒了！")
    })

    // 创建 Server 实例，配置各种参数
    srv := &http.Server{
        Addr:         ":8080", // 监听地址

        Handler:      mux,     // 路由器（如果为 nil，使用 DefaultServeMux）

        // 读取超时：从客户端读取请求头的最大时间
        // 如果客户端在这段时间内没有发送完请求头，连接被关闭
        ReadTimeout:  10 * time.Second,

        // 写入超时：向客户端写入响应的最大时间
        // 如果响应在这段时间内没写完，连接被关闭
        WriteTimeout: 10 * time.Second,

        // Idle 超时：keep-alive 连接在空闲时保持多久
        // Go 1.8+ 支持
        IdleTimeout:  120 * time.Second,

        // 最大请求头字节数
        MaxHeaderBytes: 1 << 20, // 1MB

        // ErrorLog：自定义错误日志（默认是标准 logger）
        // ErrorLog: log.New(os.Stderr, "http: ", log.LstdFlags),
    }

    fmt.Println("自定义 Server 配置演示：http://localhost:8080")
    fmt.Println("ReadTimeout:  10s")
    fmt.Println("WriteTimeout: 10s")

    // ListenAndServe 是阻塞的
    // 我们可以配合 context 做优雅关闭（见 21.23）
    if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
        log.Fatalf("服务器错误：%v", err)
    }
}
```

### Server 字段详解

| 字段 | 类型 | 说明 |
|------|------|------|
| `Addr` | `string` | 监听地址，如 `":8080"` 或 `"192.168.1.1:8080"` |
| `Handler` | `Handler` | 路由处理器（nil 则用 DefaultServeMux） |
| `ReadTimeout` | `time.Duration` | 读取请求超时 |
| `WriteTimeout` | `time.Duration` | 写入响应超时 |
| `IdleTimeout` | `time.Duration` | keep-alive 空闲超时 |
| `MaxHeaderBytes` | `int` | 请求头最大字节数 |
| `ErrorLog` | `*log.Logger` | 错误日志输出 |
| `BaseContext` | `func(net.Listener) context.Context` | 基础 Context |
| `ConnContext` | `func(context.Context, net.Conn) context.Context` | 连接级别 Context |

---

## 21.23 Server.Shutdown：优雅关闭

优雅关闭（Graceful Shutdown）是指服务器在停止前，**处理完所有正在进行的请求**，然后再退出，而不是直接拔电源。这对于生产环境至关重要——不能让正在下载文件的用户突然中断。

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(2 * time.Second) // 模拟慢请求
        fmt.Fprint(w, "Hello, 慢但稳!")
    })
    mux.HandleFunc("/quick", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "快!")
    })

    srv := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        WriteTimeout: 10 * time.Second,
    }

    // 在 goroutine 中启动服务器
    go func() {
        fmt.Println("服务器启动：http://localhost:8080")
        fmt.Println("按 Ctrl+C 发送 SIGINT 信号触发优雅关闭")
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("启动失败：%v", err)
        }
    }()

    // 创建通道接收系统信号
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // 阻塞等待信号
    sig := <-quit
    fmt.Printf("\n收到信号: %v，开始优雅关闭...\n", sig)

    // 创建带超时的 Context
    // 如果 10 秒内还没关闭完成，就强制退出
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    // Shutdown 会：
    // 1. 停止接受新连接
    // 2. 等待现有请求处理完毕
    // 3. 关闭所有空闲连接
    // 4. 返回 nil（或超时则返回 context.DeadlineExceeded）
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatalf("优雅关闭失败：%v", err)
    }

    fmt.Println("服务器已优雅关闭，再见！")
}
```

```go
// 模拟测试流程：
// 1. 启动服务器
// $ go run main.go
// 服务器启动：http://localhost:8080

// 2. 打开另一个终端，发送请求
// $ curl http://localhost:8080/quick
// 快!

// 3. 发送一个慢请求（不等待完成）
// $ curl http://localhost:8080/hello
// (不等待)

// 4. 按 Ctrl+C 发送 SIGINT
// ^C
// 收到信号: interrupt，开始优雅关闭...
// 服务器已优雅关闭，再见！
```

### 优雅关闭流程

```
┌────────────────────────────────────────────────────────────┐
│                    优雅关闭流程                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   1. 收到 SIGINT / SIGTERM 信号                            │
│          │                                                 │
│          ▼                                                 │
│   2. srv.Shutdown(ctx) 被调用                              │
│          │                                                 │
│          ├─────────────────────────────────────┐           │
│          ▼                                     ▼           │
│   3. 停止接受新连接                    3. 等待现有请求完成    │
│                                           │                 │
│                                           ▼                 │
│                                    4. 关闭空闲连接          │
│                                           │                 │
│                                           ▼                 │
│                                    5. 返回（可安全退出）    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 21.24 中间件函数签名：func(http.Handler) http.Handler

中间件（Middleware）是 Web 开发中的**装饰器模式**——它在请求到达 Handler 之前和响应返回之后"插入一脚"，做一些横切关注点（cross-cutting concerns）的事情，比如日志、认证、限流、监控等。

在 Go 的 net/http 世界里，中间件就是一个接收 `http.Handler` 返回 `http.Handler` 的函数。

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "time"
)

// 中间件函数签名：func(http.Handler) http.Handler
// 接收一个 Handler，返回一个包装后的新 Handler

// 最简单的中间件：记录每个请求的开始时间
func logMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        log.Printf("[%s] %s 请求开始", r.Method, r.URL.Path)

        // 调用下一个 Handler
        next.ServeHTTP(w, r)

        // 处理完成后记录耗时
        duration := time.Since(start)
        log.Printf("[%s] %s 请求结束，耗时 %v", r.Method, r.URL.Path, duration)
    })
}

// 认证中间件：检查请求头中是否有 Authorization
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            w.WriteHeader(http.StatusUnauthorized)
            fmt.Fprint(w, "未授权：请提供 Authorization 头")
            return
        }
        log.Printf("认证通过，Token: %s", token)
        next.ServeHTTP(w, r)
    })
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello，中间件世界！")
}

func secretHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "这是受保护的秘密页面！")
}

func main() {
    mux := http.NewServeMux()

    // 普通路由（只有日志中间件）
    mux.HandleFunc("/hello", helloHandler)

    // 受保护路由（日志 + 认证）
    mux.Handle("/secret",
        authMiddleware(
            logMiddleware(
                http.HandlerFunc(secretHandler))))

    // 应用全局中间件（包装 ServeMux 本身）
    var handler http.Handler = mux
    handler = logMiddleware(handler)

    fmt.Println("中间件演示：http://localhost:8080")
    fmt.Println("/hello   → 只有日志中间件")
    fmt.Println("/secret  → 日志 + 认证中间件")
    fmt.Println("curl -H 'Authorization: Bearer abc123' http://localhost:8080/secret")

    http.ListenAndServe(":8080", handler)
}
```

```go
// 输出示例（终端日志）
// 2024/03/15 10:30:00 [GET] /hello 请求开始
// 2024/03/15 10:30:00 [GET] /hello 请求结束，耗时 50µs

// 2024/03/15 10:30:05 [GET] /secret 请求开始
// 认证通过，Token: Bearer abc123
// 2024/03/15 10:30:05 [GET] /secret 请求结束，耗时 80µs

// curl -H "Authorization: Bearer abc123" http://localhost:8080/secret
// → 这是受保护的秘密页面！
```

### 中间件链

```
┌────────────────────────────────────────────────────────────┐
│                    中间件链（洋葱模型）                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   请求 ──► logMiddleware ──► authMiddleware ──► Handler    │
│                                                            │
│                              ▲                              │
│                              │                              │
│                              ▼                              │
│                                                            │
│   响应 ◄──── logMiddleware ◄── authMiddleware ◄── Handler  │
│                                                            │
│   中间件可以：                                              │
│   • 在 next.ServeHTTP 之前做事（前置逻辑）                   │
│   • 在 next.ServeHTTP 之后做事（后置逻辑）                    │
│   • 决定是否调用 next（短路逻辑，如认证失败）                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 21.25 日志中间件、Recovery 中间件、CORS 中间件、认证中间件

让我们把常见的几种中间件都实现一遍，然后看看它们在实际项目中的典型用法。

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "runtime/debug"
    "strings"
    "time"
)

// ============================================================
// 1. 日志中间件：记录每个请求的 Method、URL、状态码、耗时
// ============================================================
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        // 包装 ResponseWriter 以捕获状态码
        wrapped := &statusWriter{ResponseWriter: w, statusCode: http.StatusOK}

        next.ServeHTTP(wrapped, r)

        log.Printf("%s %s %d %v",
            r.Method, r.URL.Path, wrapped.statusCode, time.Since(start))
    })
}

// 包装 ResponseWriter，捕获 WriteHeader 的状态码
type statusWriter struct {
    http.ResponseWriter
    statusCode int
}

func (sw *statusWriter) WriteHeader(code int) {
    sw.statusCode = code
    sw.ResponseWriter.WriteHeader(code)
}

// ============================================================
// 2. Recovery 中间件：捕获 panic，防止服务器崩溃
// ============================================================
func recoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                log.Printf("⚠️  panic 恢复：%v\n%s", err, debug.Stack())
                w.WriteHeader(http.StatusInternalServerError)
                fmt.Fprint(w, "服务器内部错误，请稍后再试")
            }
        }()
        next.ServeHTTP(w, r)
    })
}

// ============================================================
// 3. CORS 中间件：处理跨域请求
// ============================================================
func corsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

        // 预检请求（OPTIONS）直接返回
        if r.Method == http.MethodOptions {
            w.WriteHeader(http.StatusNoContent)
            return
        }

        next.ServeHTTP(w, r)
    })
}

// ============================================================
// 4. 认证中间件：简单检查 API Key
// ============================================================
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 从 Header 或 Query 获取 API Key
        apiKey := r.Header.Get("X-API-Key")
        if apiKey == "" {
            apiKey = r.URL.Query().Get("api_key")
        }

        // 这里用硬编码做演示，实际应该查数据库或配置
        if apiKey != "my-secret-key" {
            w.WriteHeader(http.StatusUnauthorized)
            fmt.Fprint(w, `{"error": "未授权，请提供有效的 X-API-Key"}`)
            return
        }

        next.ServeHTTP(w, r)
    })
}

// ============================================================
// 5. 限流中间件（简单版）
// ============================================================
func rateLimitMiddleware(next http.Handler) http.Handler {
    // 简单计数器实现，生产环境推荐使用 token bucket 或 sliding window
    var count int
    var lastReset = time.Now()

    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        now := time.Now()
        if now.Sub(lastReset) > time.Minute {
            count = 0
            lastReset = now
        }
        count++
        if count > 100 {
            w.WriteHeader(http.StatusTooManyRequests)
            fmt.Fprintf(w, "请求太频繁，请稍后再试（当前每分钟限制 100 次）")
            return
        }
        w.Header().Set("X-RateLimit-Count", fmt.Sprintf("%d/100", count))
        next.ServeHTTP(w, r)
    })
}

func main() {
    mux := http.NewServeMux()

    // 业务 Handler
    mux.HandleFunc("/api/hello", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, `{"message": "你好，API！"}`)
    })

    mux.HandleFunc("/api/panic", func(w http.ResponseWriter, r *http.Request) {
        panic("故意抛出一个 panic 来测试 Recovery 中间件！")
    })

    // 组合中间件链
    var handler http.Handler = mux
    handler = loggingMiddleware(handler)
    handler = recoveryMiddleware(handler)
    handler = corsMiddleware(handler)
    handler = authMiddleware(handler)
    handler = rateLimitMiddleware(handler)

    fmt.Println("完整中间件演示：http://localhost:8080")
    fmt.Println("/api/hello  → 受日志+Recovery+CORS+认证+限流中间件保护")
    fmt.Println("curl http://localhost:8080/api/hello -H 'X-API-Key: my-secret-key'")

    http.ListenAndServe(":8080", handler)
}
```

```go
// 测试结果
// curl -i http://localhost:8080/api/hello -H "X-API-Key: my-secret-key"
// → HTTP/1.1 200 OK
// → Access-Control-Allow-Origin: *
// → X-RateLimit-Count: 1/100
// → {"message": "你好，API！"}

// curl -i http://localhost:8080/api/hello
// → HTTP/1.1 401 Unauthorized
// → {"error": "未授权，请提供有效的 X-API-Key"}

// curl http://localhost:8080/api/panic -H "X-API-Key: my-secret-key"
// → HTTP/1.1 500 Internal Server Error
// → 服务器内部错误，请稍后再试
// (终端) 2024/03/15 10:30:00 ⚠️  panic 恢复：故意抛出一个 panic...
```

### 中间件对比

| 中间件 | 作用 | 短路位置 |
|--------|------|----------|
| 日志 | 记录请求信息 | 无（前后都记录） |
| Recovery | 捕获 panic | panic 发生时 |
| CORS | 处理跨域 | OPTIONS 预检直接返回 |
| 认证 | 验证身份 | 认证失败时 |
| 限流 | 控制频率 | 超限时 |

---

## 21.26 http.ListenAndServeTLS：启用 HTTPS

HTTP over TLS（HTTPS）就是加密版的 HTTP。`http.ListenAndServeTLS` 让你用几行代码就能启动一个 HTTPS 服务器。

**前提条件**：你需要有 SSL/TLS 证书。私钥是 `.key` 文件，证书是 `.crt` 文件（或 `.pem`）。生产环境推荐使用 Let's Encrypt 免费证书。

```go
package main

import (
    "fmt"
    "net/http"
)

// 生成自签名证书（仅用于本地测试）：
// openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
// 或者 Go 工具：
// go run crypto/tls/generate_cert.go -host=localhost

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "你访问的是 HTTPS 服务！\n")
        fmt.Fprintf(w, "协议版本：%s\n", r.Proto)
        fmt.Fprintf(w, "请求方法：%s\n", r.Method)
        fmt.Fprintf(w, "访问路径：%s\n", r.URL.Path)
    })

    fmt.Println("HTTPS 服务器演示：https://localhost:8443")
    fmt.Println("⚠️  首次访问会显示证书不受信任（自签名），这是正常的")
    fmt.Println("使用以下命令生成测试证书：")
    fmt.Println("openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'")

    // 启动 HTTPS 服务器
    // certFile = 证书文件（包含公钥）
    // keyFile  = 私钥文件
    err := http.ListenAndServeTLS(
        ":8443",
        "cert.pem",  // 证书文件
        "key.pem",   // 私钥文件
        mux,
    )
    if err != nil {
        fmt.Printf("服务器错误：%v", err)
    }
}
```

```go
// 生成测试证书
// $ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'

// 运行服务器
// $ go run main.go
// HTTPS 服务器演示：https://localhost:8443

// 测试
// $ curl -k https://localhost:8443/  （-k 跳过证书验证）
// → 你访问的是 HTTPS 服务！
// → 协议版本：HTTP/1.1
// → 请求方法：GET
// → 访问路径：/
```

> **重要**：Go 的 TLS 实现默认禁用 SSL 3.0 和 TLS 1.0/1.1（因为它们有已知安全漏洞）。生产环境应使用 TLS 1.2 或 1.3。

---

## 21.27 TLSConfig：配置证书、协议版本、密码套件

`http.Server` 的 `TLSConfig` 字段允许你精细控制 TLS 的各个方面——证书来源、支持的协议版本、密码套件、会话缓存等。

```go
package main

import (
    "crypto/tls"
    "fmt"
    "net/http"
    "time"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        // 获取 TLS 连接信息
        if r.TLS != nil {
            fmt.Fprintf(w, "TLS 版本：%s\n", tls.VersionName(r.TLS.Version))
            fmt.Fprintf(w, "密码套件：%s\n", tls.CipherSuiteName(r.TLS.CipherSuite))
            fmt.Fprintf(w, "服务器名（SNI）：%s\n", r.TLS.ServerName)
        } else {
            fmt.Fprint(w, "非 TLS 连接")
        }
    })

    // 加载证书
    cert, err := tls.LoadX509KeyPair("cert.pem", "key.pem")
    if err != nil {
        fmt.Printf("加载证书失败：%v\n", err)
        fmt.Println("请先运行：openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'")
        return
    }

    // 配置 TLS
    tlsConfig := &tls.Config{
        // 证书
        Certificates: []tls.Certificate{cert},

        // 最低 TLS 版本（1.2 是现代安全标准）
        MinVersion: tls.VersionTLS12,

        // 优先选择的密码套件（性能+安全兼顾）
        // 这里列出一些推荐的套件
        CipherSuites: []uint16{
            tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
            tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
            tls.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,
        },

        // 启用 TLS 1.3（TLS 1.3 有独立的密码套件，系统会自动选择）
        // CurvePreferences: []tls.CurveID{tls.X25519, tls.CurveP256},

        // 服务器名称指示（Server Name Indication，SNI）
        // 让同一个 IP 可以托管多个域名（多个证书）
        ServerName: "localhost",

        // 会话缓存（提升性能）
        // SessionTicketsDisabled: true, // 生产环境可以禁用会话票证（Forward Secrecy）
        SessionCache: tls.NewSessionCache(tlsCache, 128),
    }

    srv := &http.Server{
        Addr:      ":8443",
        Handler:   mux,
        TLSConfig: tlsConfig,
    }

    fmt.Println("TLSConfig 演示：https://localhost:8443")
    fmt.Printf("最低 TLS 版本：TLS 1.2\n")
    fmt.Printf("密码套件：ECDHE-RSA-AES-256-GCM-SHA384 等\n`")

    err = srv.ListenAndServeTLS("", "") // 证书从 TLSConfig 加载
    if err != nil {
        fmt.Printf("服务器错误：%v", err)
    }
}

var tlsCache = tls.NewSessionCache(nil, 0) // 简化示例
```

### TLS 配置参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `Certificates` | `[]tls.Certificate` | 服务器证书（可多个，用于 SNI） |
| `MinVersion` | `uint16` | 最低 TLS 版本（推荐 TLS 1.2） |
| `MaxVersion` | `uint16` | 最高 TLS 版本（TLS 1.3 = 0x0304） |
| `CipherSuites` | `[]uint16` | 允许的密码套件 |
| `CurvePreferences` | `[]tls.CurveID` | 优先的椭圆曲线 |
| `SessionCache` | `tls.SessionCache` | 会话缓存（提升性能） |
| `ServerName` | `string` | SNI 服务器名 |
| `NextProtos` | `[]string` | ALPN 协议列表（如 h2, http/1.1） |

### TLS 版本常量

| 常量 | 值 | 说明 |
|------|----|------|
| `tls.VersionSSL30` | 0x0300 | SSL 3.0（已废弃） |
| `tls.VersionTLS10` | 0x0301 | TLS 1.0（已废弃） |
| `tls.VersionTLS11` | 0x0302 | TLS 1.1（已废弃） |
| `tls.VersionTLS12` | 0x0303 | TLS 1.2（当前主流） |
| `tls.VersionTLS13` | 0x0304 | TLS 1.3（最新） |

---

## 21.28 mTLS：双向证书认证

mTLS（Mutual TLS，双向 TLS）是 TLS 的增强版。在标准 TLS 中，**只有客户端验证服务器的身份**（通过服务器证书）。而在 mTLS 中，**服务器也验证客户端的身份**（通过客户端证书）。

这在微服务间通信、零信任网络、企业内网等场景非常有用。

```go
package main

import (
    "crypto/tls"
    "crypto/x509"
    "fmt"
    "net/http"
    "io/ioutil"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        // 在 mTLS 中，可以从连接中获取客户端证书信息
        if r.TLS != nil && len(r.TLS.PeerCertificates) > 0 {
            cert := r.TLS.PeerCertificates[0]
            fmt.Fprintf(w, "客户端证书已验证！\n")
            fmt.Fprintf(w, "颁发者：%s\n", cert.Issuer)
            fmt.Fprintf(w, "主题：%s\n", cert.Subject)
            fmt.Fprintf(w, "Common Name：%s\n", cert.Subject.CommonName)
        } else {
            fmt.Fprint(w, "没有客户端证书（标准 TLS）")
        }
    })

    // 加载服务器证书
    serverCert, err := tls.LoadX509KeyPair("server.crt", "server.key")
    if err != nil {
        fmt.Printf("加载服务器证书失败：%v\n", err)
        return
    }

    // 加载受信任的 CA 证书（用于验证客户端证书）
    caCertPEM, err := ioutil.ReadFile("ca.crt")
    if err != nil {
        fmt.Printf("加载 CA 证书失败：%v\n", err)
        return
    }
    caCertPool := x509.NewCertPool()
    caCertPool.AppendCertsFromPEM(caCertPEM)

    tlsConfig := &tls.Config{
        Certificates: []tls.Certificate{serverCert},
        ClientAuth:   tls.RequireAndVerifyClientCert, // 强制要求客户端证书
        ClientCAs:    caCertPool,                      // 用这个 CA 池验证客户端证书
        MinVersion:   tls.VersionTLS12,
    }

    srv := &http.Server{
        Addr:      ":8443",
        Handler:   mux,
        TLSConfig: tlsConfig,
    }

    fmt.Println("mTLS 服务器演示：https://localhost:8443")
    fmt.Println("需要客户端携带有效证书才能访问")
    fmt.Println("生成测试证书：")
    fmt.Println("  1. CA: openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 365 -nodes -subj '/CN=My CA'")
    fmt.Println("  2. 服务器证书（用 CA 签名）")
    fmt.Println("  3. 客户端证书（用 CA 签名）")

    srv.ListenAndServeTLS("", "")
}
```

### mTLS 流程图

```
┌────────────────────────────────────────────────────────────┐
│                      mTLS 握手流程                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   客户端                                        服务器      │
│     │                                               │      │
│     │  1. ClientHello ──────────────────────────►  │      │
│     │        (携带客户端证书)                        │      │
│     │                                               │      │
│     │  2. ◄──────────────────────────────── ServerHello │
│     │        (要求客户端证书)                        │      │
│     │                                               │      │
│     │  3. ClientCertificate ────────────────────►  │      │
│     │        (发送客户端证书)                        │      │
│     │                                               │      │
│     │  4. CertificateVerify ────────────────────►  │      │
│     │        (用私钥签名，验证客户端拥有私钥)          │      │
│     │                                               │      │
│     │  5. ◄──────────────────── Finished           │      │
│     │        (服务器验证客户端证书通过)               │      │
│     │                                               │      │
│     │  双向认证完成，安全通道建立！                   │      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

> **专业词汇解释**
>
> - **mTLS（Mutual TLS）**：双向 TLS 认证。客户端和服务器都需要持有证书，双方都要验证对方的身份。
> - **ClientAuth**：服务器端配置，`tls.RequireAndVerifyClientCert` 表示强制要求并验证客户端证书。
> - **ClientCAs**：CA 证书池，服务器用这个池来验证客户端证书是否由可信的 CA 颁发。
> - **Forward Secrecy**：前向保密。即使长期私钥泄露，过去的通信仍然安全（因为每次会话用临时密钥）。ECDHE 系列密码套件支持前向保密。

---

## 21.29 http/cgi、http/fcgi：传统 CGI 和 FastCGI 协议实现

CGI（Common Gateway Interface）和 FastCGI 是 Web 服务器与外部程序通信的古老协议。虽然在 Go 中我们一般直接用 net/http 构建服务，但了解这些协议有助于理解 Web 开发的历史，以及为什么 Go 的并发模型如此优秀。

### CGI（Common Gateway Interface）

CGI 是最简单的服务器-程序通信方式：**每个请求，服务器fork一个进程，传递环境变量和标准输入，程序输出标准输出作为响应**。问题很明显——每次请求都要启动进程，开销巨大。

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "net/http/cgi"
)

func main() {
    // cgi.Serve 接收一个 http.Handler，然后通过 CGI 协议为每个请求执行它
    // 相当于把 Go 的 Handler 暴露为 CGI 脚本
    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain; charset=utf-8")
        fmt.Fprintln(w, "这是一个 CGI 程序！")
        fmt.Fprintf(w, "请求方法: %s\n", r.Method)
        fmt.Fprintf(w, "脚本名称: %s\n", r.URL.Path)
        fmt.Fprintf(w, "查询字符串: %s\n", r.URL.RawQuery)
    })

    log.Println("CGI 服务器演示（实际是在本进程中模拟 CGI）")
    log.Println("使用 cgi.Serve 包装 Handler 作为 CGI 脚本运行")
    log.Println("")
    log.Println("真实场景：把 Go 程序编译成二进制，上传到支持 CGI 的 Web 服务器（如 Apache + mod_cgi）")

    // 在本进程中模拟 CGI 响应（演示用）
    // 实际使用时，部署 CGI 程序到服务器的 cgi-bin 目录
    fmt.Println("\n--- CGI 模拟输出 ---")
    fmt.Println("Content-Type: text/plain; charset=utf-8")
    fmt.Println()
    handler.ServeHTTP(
        &cgiResponseWriter{headers: make(map[string]string)},
        &http.Request{Method: "GET", URL: &urlWrap{Path: "/hello.cgi", RawQuery: "name=Alice"}},
    )
}

type urlWrap struct {
    Path      string
    RawQuery  string
}

func (u *urlWrap) String() string { return u.Path + "?" + u.RawQuery }

// 简化模拟
type cgiResponseWriter struct {
    headers map[string]string
    written bool
}

func (w *cgiResponseWriter) Header() http.Header { return http.Header(w.headers) }
func (w *cgiResponseWriter) Write(p []byte) (int, error) {
    if !w.written {
        fmt.Println("Content-Type: text/plain; charset=utf-8")
        fmt.Println()
        w.written = true
    }
    fmt.Print(string(p))
    return len(p), nil
}
func (w *cgiResponseWriter) WriteHeader(int) {}
```

### FastCGI

FastCGI 是 CGI 的改进版——不再每次fork进程，而是启动**长期运行的进程**，通过 socket（Unix socket 或 TCP）复用连接。性能比 CGI 好很多，但仍然需要额外进程管理。

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "net/http/fcgi"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "这是 FastCGI 程序响应！")
    })

    log.Println("FastCGI 演示")
    log.Println("")
    log.Println("真实场景：使用 fcgi.Serve 启动 FastCGI 进程")
    log.Println("然后配置 Web 服务器（ Nginx + fastcgi_pass 或 Apache + mod_fcgid）连接到该 socket")
    log.Println("")
    log.Println("Go 生态中，标准库没有直接提供 FastCGI 客户端（连接 FastCGI 服务器）")
    log.Println("如果需要，可以用 golang.org/x/sync/fcgiproxy 或第三方库")

    // fcgi.Serve 会阻塞，将 mux 作为 FastCGI 进程运行
    // 实际使用时，Web 服务器会通过 socket 连接到这个进程
    //
    // 演示用，实际运行会报错（需要 Web 服务器端配置）
    // err := fcgi.Serve(nil, mux)  // nil = 使用默认的 TCP socket :9000
    // if err != nil {
    //     log.Fatalf("FastCGI 启动失败：%v", err)
    // }
}
```

### CGI vs FastCGI vs Go net/http

```
┌──────────────────────────────────────────────────────────────┐
│              CGI vs FastCGI vs Go net/http                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   CGI                                                        │
│   ┌──────┐    fork+exec     ┌──────────┐                    │
│   │ Nginx │ ──────────────► │ CGI 进程  │ (每次请求都新建)    │
│   └──────┘                  └──────────┘                    │
│                               进程创建开销大                   │
│                                                              │
│   FastCGI                                                    │
│   ┌──────┐    socket       ┌──────────┐                     │
│   │ Nginx │ ──────────────► │ FastCGI  │ (长期运行)          │
│   └──────┘                  │ 进程池   │                    │
│                              └──────────┘                    │
│                              连接复用，性能好                  │
│                                                              │
│   Go net/http                                                │
│   ┌──────┐    goroutine    ┌──────────┐                     │
│   │ 客户端│ ──────────────► │ Go HTTP  │ (每个请求一个       │
│   └──────┘                  │ Server   │  goroutine)        │
│                              └──────────┘                    │
│                              轻量、并发、原生                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

> **历史小知识**：CGI 诞生于 1993 年，FastCGI 在 1996 年诞生。随着 Web 应用越来越复杂，CGI/FastCGI 逐渐被直接嵌入 Web 服务器的应用服务器模式（如 mod_php, Tomcat, WSGI）取代。而 Go 的 net/http 直接用 Goroutine 处理并发，比 FastCGI 更轻量——因为 Goroutine 比进程/线程轻得多，创建成本接近为零。

---

## 本章小结

这一章我们深入探索了 Go 标准库 `net/http` 的方方面面，从最基础的 HTTP 服务器搭建，到高级的 HTTPS、mTLS、中间件和优雅关闭。让我们来回顾一下核心知识点：

### 核心概念

| 概念 | 说明 |
|------|------|
| **HTTP 请求-响应** | 客户端发请求，服务器回响应，是互联网的基础通信模式 |
| **Handler** | 处理请求的业务逻辑，实现了 `ServeHTTP(ResponseWriter, *Request)` |
| **ServeMux** | 路由器，根据 URL 路径分发请求到对应的 Handler |
| **ResponseWriter** | Handler 用来写入响应的接口 |

### 常用 API

| API | 用途 |
|-----|------|
| `http.HandleFunc(pattern, handler)` | 注册函数作为 Handler |
| `http.Handle(pattern, handler)` | 注册实现了 Handler 接口的对象 |
| `http.ListenAndServe(addr, handler)` | 启动 HTTP 服务器 |
| `http.NewServeMux()` | 创建自定义路由器 |
| `http.Server` | 服务器配置（超时、连接数等） |
| `http.FileServer(dir)` | 静态文件服务器 |
| `http.StripPrefix(prefix, h)` | 剥离路径前缀 |
| `http.TimeoutHandler(h, d, msg)` | 超时包装器 |

### 中间件模式

中间件是 `func(http.Handler) http.Handler` 类型的函数，通过返回包装后的 Handler 实现装饰器模式。常见的中间件包括日志、认证、Recovery、CORS、限流等。

### HTTPS 和安全

- `http.ListenAndServeTLS(certFile, keyFile, handler)` 启动 HTTPS
- 通过 `tls.Config` 配置 TLS 版本、密码套件、SNI 等
- mTLS 需要 `ClientAuth: tls.RequireAndVerifyClientCert` 并配置 `ClientCAs`

### 高级主题

- **优雅关闭**：`Server.Shutdown(ctx)` 允许处理完现有请求后再退出
- **Context 传递**：`Request.WithContext(ctx)` 创建带新 Context 的请求副本
- **CGI/FastCGI**：`net/http/cgi` 和 `net/http/fcgi` 支持传统协议

### Go net/http 的设计哲学

Go 的 HTTP 设计始终遵循**简单、实用、正交**的原则：
- 接口极简（只有 `ServeHTTP` 一个方法）
- 功能正交（路由、Handler、响应写入各司其职）
- 标准库即框架（不需要第三方框架就能构建生产级服务）

下一章我们将探索 Go 中的 **JSON 处理（encoding/json）**，敬请期待！

> **继续学习的建议**：
> 1. 尝试用 `net/http` 构建一个 RESTful API，支持 CRUD 操作
> 2. 实现一个带 JWT 认证的中间件
> 3. 学习如何用 Go 写一个反向代理（`httputil.ReverseProxy`）
> 4. 探索 Go 1.22+ 的路由改进（`ServeMux` 增加了方法匹配）
