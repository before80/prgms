+++
title = "第 22 章：HTTP 客户端——net/http（续）"
weight = 220
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 22 章：HTTP 客户端——net/http（续）

> 「上一章我们学会了建服务器，这一章我们学会做客户。做一个好的 HTTP 客户端，可比当一个舔狗要复杂多了。」

---

## 22.1 net/http 客户端解决什么问题

HTTP 客户端，简而言之，就是**主动发起请求**的那一方。你每天刷网页、调 API、下文件，背后都是 HTTP 客户端在默默干活。

### 它能做什么

| 场景 | 说明 |
|------|------|
| 获取网页内容 | 爬虫、SSR 渲染内容抓取 |
| 调用 REST API | 前后端分离、微服务间通信 |
| 下载文件 | 图片、文档、二进制文件 |

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	// 最简单的例子：抓取一个网页
	resp, err := http.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Println("网络错误：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Println("响应状态：", resp.Status)
	fmt.Println("响应体长度：", len(body), "字节")
}
```

```
响应状态： 200 OK
响应体长度： 329 字节
```

### 核心概念图

```mermaid
sequenceDiagram
	participant C as HTTP 客户端
	participant S as HTTP 服务器
	C->>S: 发起请求 (GET/POST/PUT/DELETE...)
	S->>C: 返回响应 (状态码 + Body + Header)
```

**专业词汇解释：**

- **HTTP 客户端（Client）**：主动发起请求的一方，负责建立连接、发送请求、处理响应。在 TCP/IP 模型中位于应用层。
- **REST API**：一种基于 HTTP 协议的 API 设计风格，使用 GET/POST/PUT/DELETE 等动词操作资源。

---

## 22.2 net/http 客户端核心原理

Go 的 HTTP 客户端有三驾马车：`http.Client`、`http.Transport`、`Response.Body`。搞清楚它们的关系，就搞清楚了半个 net/http。

### http.Client —— 请求的发起者

`Client` 是整个客户端的核心，它管理着请求的发送逻辑、超时控制、Cookie 管理等。

```go
type Client struct {
	Transport  RoundTripper   // 实际执行请求的运输层
	CheckRedirect func(*Request) error  // 重定向策略
	Jar         CookieJar     // Cookie 管理
	Timeout     time.Duration // 超时控制
}
```

### Transport —— 连接池的管理者

`Transport` 负责**建立 TCP 连接、管理连接池、TLS 握手**。它会复用已建立的连接，避免每次请求都重新建联（那是 TCP 三次握手的噩梦）。

```go
type Transport struct {
	MaxIdleConns        int   // 最大空闲连接数
	MaxIdleConnsPerHost int   // 每个主机最大空闲连接数
	IdleConnTimeout     time.Duration // 空闲连接超时
	// ... 更多配置
}
```

### Response.Body —— 数据的载体

`Response.Body` 是一个 `io.ReadCloser`，包含响应的主体内容。**记住，它必须被关闭**，否则会引发连接泄漏——就像水龙头没关紧，时间久了地板就泡坏了。

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", "https://httpbin.org/get", nil)

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close() // 重要！必须关闭

	fmt.Println("状态码：", resp.StatusCode)
	fmt.Println("Content-Type：", resp.Header.Get("Content-Type"))
}
```

```
状态码： 200
Content-Type： application/json
```

### 核心原理图

```mermaid
flowchart LR
	A[http.Client] --> B[Transport<br/>连接池]
	B --> C[TCP 连接]
	C --> D[Response.Body<br/>必须 Close]
```

**专业词汇解释：**

- **RoundTripper**：接口，定义「执行单个 HTTP 请求」的抽象。`Transport` 是它的默认实现。
- **连接池（Connection Pool）**：复用已建立的连接，避免频繁创建/销毁 TCP 连接的性能开销。
- **io.ReadCloser**：`io.Reader` + `io.Closer` 的组合，既可以读数据，又可以关闭资源。

---

## 22.3 http.DefaultClient：默认客户端

Go 为我们提供了一个**开箱即用**的默认客户端：

```go
var DefaultClient = &Client{}
```

### 问题所在

`http.DefaultClient` 最大的问题是——**没有默认超时**。这意味着：

- 如果服务器卡住了，你的程序可能会**永久阻塞**
- 如果网络断了，你的程序会**无限等待**

这在生产环境中是灾难性的。

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

// 正确的做法：创建自己的 Client 并设置超时
func main() {
	// 方式一：使用默认 Client（不推荐生产环境）
	// resp, err := http.DefaultClient.Get("https://httpbin.org/delay/10")

	// 方式二：自定义 Client（推荐）
	client := &http.Client{
		Timeout: 10 * time.Second, // 设置 10 秒超时
	}

	resp, err := client.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Println("请求超时或失败：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Println("请求成功，状态码：", resp.StatusCode)
}
```

```
请求成功，状态码： 200
```

### 最佳实践

```go
// 创建一个配置好超时的 Client
func NewClient(timeout time.Duration) *http.Client {
	return &http.Client{
		Timeout: timeout,
		Transport: &http.Transport{
			MaxIdleConns:        100,
			MaxIdleConnsPerHost: 10,
			IdleConnTimeout:      90 * time.Second,
		},
	}
}
```

**专业词汇解释：**

- **DefaultClient**：Go 标准库提供的全局默认 HTTP 客户端，没有任何超时设置。
- **生产环境（Production）**：指正式对外提供服务、承受真实流量的系统环境，对稳定性和性能要求极高。

---

## 22.4 http.Get：最简单的方式

对于最最最简单的场景，Go 提供了 `http.Get(url)` 这个一键发送 GET 请求的快捷函数。

### 函数签名

```go
func Get(url string) (resp *Response, err error)
```

### 示例

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	// 一行代码发送 GET 请求
	resp, err := http.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Println("网络错误：", err)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("读取响应失败：", err)
		return
	}

	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("响应体：%s\n", string(body))
}
```

```
状态码：200
响应体：{"args":{},"headers":{"Accept-Encoding":"identity",...},...}
```

### 底层原理

`http.Get` 底层等价于：

```go
http.DefaultClient.Get(url)
```

也就是说，它用的是那个**没有超时设置的默认客户端**。所以 `http.Get` 只适合写 demo、跑脚本，生产环境请自觉使用带超时的 `Client`。

**专业词汇解释：**

- **GET 请求**：HTTP 中最常见的请求方法，用于从服务器获取资源，通常不包含请求体。
- **快捷函数（Convenience function）**：封装了常用操作的高级函数，让 API 更简洁，但牺牲了部分灵活性。

---

## 22.5 http.Post：发送带请求体的请求

`http.Post` 用于发送 POST 请求，可以指定 Content-Type 和请求体。

### 函数签名

```go
func Post(url, contentType string, body io.Reader) (resp *Response, err error)
```

### 示例：发送 JSON 数据

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type User struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func main() {
	user := User{Name: "张三", Age: 18}
	jsonData, _ := json.Marshal(user)

	// 发送 POST 请求，Content-Type 为 application/json
	resp, err := http.Post(
		"https://httpbin.org/post",
		"application/json",
		bytes.NewReader(jsonData),
	)
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("响应体：%s\n", string(body))
}
```

```
状态码：200
响应体：{"args":{},"data":"{\"name\":\"张三\",\"age\":18}",...}
```

### 常见 Content-Type

| Content-Type | 用途 |
|---|---|
| `application/json` | JSON 数据 |
| `application/x-www-form-urlencoded` | 表单数据 |
| `multipart/form-data` | 文件上传 |

**专业词汇解释：**

- **Content-Type**：HTTP 请求头之一，告诉服务器请求体的数据格式。
- **io.Reader**：Go 中表示「数据源」的接口，任何实现了 `Read([]byte) (int, error)` 的类型都可以作为请求体。

---

## 22.6 http.PostForm：表单提交神器

如果只是提交一个普通的表单（key-value 对），`http.PostForm` 就是为你准备的。

### 函数签名

```go
func PostForm(url string, values url.Values) (resp *Response, err error)
```

### 示例

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
)

func main() {
	// 构造表单数据
	formData := url.Values{
		"username": {"张三"},
		"password": {"123456"},
	}

	// 自动设置 Content-Type 为 application/x-www-form-urlencoded
	resp, err := http.PostForm("https://httpbin.org/post", formData)
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("响应体：%s\n", string(body))
}
```

```
状态码：200
响应体：{"args":{},"form":{"password":"123456","username":"张三"},...}
```

它会自动帮你设置 `Content-Type`，不用手动操心——懒人必备。

**专业词汇解释：**

- **url.Values**：`map[string][]string` 的类型别名，用于表示 URL 查询参数或表单数据。
- **application/x-www-form-urlencoded**：传统的表单编码格式，用 `key=value&key2=value2` 的形式发送数据。

---

## 22.7 http.NewRequest：创建请求

当需要更多控制时（比如设置自定义 Header、指定方法），使用 `http.NewRequest`。

### 函数签名

```go
func NewRequest(method, url string, body io.Reader) (*Request, error)
```

### 示例：创建各种请求

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func main() {
	// GET 请求
	reqGet, _ := http.NewRequest("GET", "https://httpbin.org/get", nil)
	reqGet.Header.Set("Accept", "application/json")

	// POST 请求（带 JSON Body）
	payload, _ := json.Marshal(map[string]string{"name": "李四"})
	reqPost, _ := http.NewRequest("POST", "https://httpbin.org/post", bytes.NewReader(payload))
	reqPost.Header.Set("Content-Type", "application/json")
	reqPost.Header.Set("Authorization", "Bearer token123")

	// PUT 请求
	reqPut, _ := http.NewRequest("PUT", "https://httpbin.org/put", nil)
	reqPut.Header.Set("If-Match", `"version1"`)

	// DELETE 请求
	reqDel, _ := http.NewRequest("DELETE", "https://httpbin.org/delete", nil)

	// 执行请求
	client := &http.Client{Timeout: 10 * time.Second} // 10秒超时
	resp, _, err := client.Do(reqPost)
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("响应体：%s\n", string(body))
}
```

```
状态码：200
响应体：{"data":"{\"name\":\"李四\"}","headers":{"Authorization":"Bearer token123"...},...}
```

### NewRequest vs Get/Post

```mermaid
flowchart TD
	A[需要什么？] --> B{只需简单 GET？}
	B -->|是| C[http.Get 够用]
	B -->|否| D{需要自定义？}
	D -->|Header/方法/Body| E[http.NewRequest]
	D -->|表单数据| F[http.PostForm]
```

**专业词汇解释：**

- **Request**：Go 中表示 HTTP 请求的结构体，包含了方法、URL、Header、Body 等所有信息。
- **Authorization**：请求头，用于携带认证信息，常见格式有 `Bearer token` 和 `Basic base64(user:pass)`。

---

## 22.8 http.Client.Do：发送请求

`Client.Do` 是最核心的方法，它接收一个 `*Request`，执行请求，返回 `*Response`。

### 示例：完整流程

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	// 1. 创建请求
	req, err := http.NewRequest("GET", "https://httpbin.org/get", nil)
	if err != nil {
		fmt.Println("创建请求失败：", err)
		return
	}

	// 2. 设置请求头
	req.Header.Set("User-Agent", "MyGoClient/1.0")
	req.Header.Set("Accept", "application/json")

	// 3. 创建客户端
	client := &http.Client{
		Timeout: 10 * time.Second, // 10秒超时
	}

	// 4. 发送请求
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("发送请求失败：", err)
		return
	}
	defer resp.Body.Close() // 5. 重要：关闭响应体

	// 6. 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("读取响应失败：", err)
		return
	}

	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("响应体长度：%d 字节\n", len(body))
}
```

```
状态码：200
响应体长度：285 字节
```

### Do 之后必须处理响应体

这是新手最容易踩的坑——`Do` 之后如果不去读也不去关 `resp.Body`，会导致**连接泄漏**：

```go
// 错误示例：连接泄漏
resp, _ := client.Do(req)
fmt.Println(resp.StatusCode)
// 忘记 defer resp.Body.Close() ❌

// 正确示例
resp, _ := client.Do(req)
defer resp.Body.Close() // 必须关 ✅
```

**专业词汇解释：**

- **连接泄漏（Connection Leak）**：TCP 连接未被正确关闭，长时间积累会耗尽操作系统的文件描述符，导致程序崩溃。
- **defer**：Go 的延迟执行语句，在函数返回前执行，常用于资源清理。

---

## 22.9 http.Client.CheckRedirect：重定向策略

默认情况下，`http.Client` 会自动跟随 HTTP 重定向（301、302、303、307、308）。通过 `CheckRedirect` 可以自定义重定向策略。

### 函数签名

```go
CheckRedirect func(*Request) error
// 如果返回非 nil error，客户端停止跟随重定向
```

### 示例：禁止跟随重定向

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	client := &http.Client{
		// 返回 error 即可停止跟随重定向
		CheckRedirect: func(req *http.Request) error {
			fmt.Printf("即将跳转到：%s\n", req.URL)
			return fmt.Errorf("停止跟随重定向")
		},
	}

	resp, err := client.Get("https://httpbin.org/redirect-to?url=https://httpbin.org/get")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("最终状态码：%d\n", resp.StatusCode)
}
```

```
即将跳转到：https://httpbin.org/get
请求失败：停止跟随重定向
最终状态码：0
```

### 示例：限制重定向次数

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	maxRedirects := 3
	redirectCount := 0

	client := &http.Client{
		CheckRedirect: func(req *http.Request) error {
			redirectCount++
			fmt.Printf("第 %d 次重定向，目标：%s\n", redirectCount, req.URL)
			if redirectCount > maxRedirects {
				return fmt.Errorf("超过最大重定向次数 %d", maxRedirects)
			}
			return nil // 继续跟随
		},
	}

	resp, err := client.Get("https://httpbin.org/redirect/5")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("最终状态码：%d，重定向次数：%d\n", resp.StatusCode, redirectCount)
}
```

```
第 1 次重定向，目标：https://httpbin.org/redirect/4
第 2 次重定向，目标：https://httpbin.org/redirect/3
第 3 次重定向，目标：https://httpbin.org/redirect/2
第 4 次重定向，目标：https://httpbin.org/redirect/1
请求失败：超过最大重定向次数 3
```

**专业词汇解释：**

- **重定向（Redirect）**：服务器返回 3xx 状态码，告诉客户端去另一个 URL 获取资源。
- **301/302/303/307/308**：不同的重定向类型，区别在于请求方法是否改变（GET vs POST）以及缓存行为。

---

## 22.10 http.Client.Timeout：总超时

`Client.Timeout` 设置的是**从请求开始到响应体读取完毕**的整个过程超时，包括：

- DNS 解析
- TCP 连接建立
- TLS 握手
- 服务器处理时间
- 响应数据传输

### 示例

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"time"
)

func main() {
	// 设置 3 秒超时
	client := &http.Client{
		Timeout: 3 * time.Second,
	}

	// 这个端点会延迟 5 秒才响应
	start := time.Now()
	resp, err := client.Get("https://httpbin.org/delay/5")
	if err != nil {
		fmt.Printf("请求超时！耗时：%v\n", time.Since(start))
		fmt.Println("错误原因：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("请求成功，耗时：%v，响应长度：%d\n", time.Since(start), len(body))
}
```

```
请求超时！耗时：3.002s
错误原因：Get "https://httpbin.org/delay/5": context deadline exceeded
```

### 超时分类

```mermaid
flowchart LR
	A[Client.Timeout] --> B[DNS 解析]
	A --> C[TCP 连接]
	A --> D[TLS 握手]
	A --> E[服务器处理]
	A --> F[响应传输]
```

**专业词汇解释：**

- **context deadline exceeded**：Go 的 `context` 包超时错误，表示超过了预设的时间限制。
- **DNS 解析**：将域名（如 `httpbin.org`）转换为 IP 地址的过程。

---

## 22.11 http.Transport：连接池配置

`Transport` 是实际管理连接池的家伙。如果 `Client` 是指挥官，那 `Transport` 就是负责铺路的后勤兵。

### 默认 Transport

每个 `Client` 如果不指定 `Transport`，就会使用默认的 `http.DefaultTransport`。

```go
var DefaultTransport RoundTripper = &Transport{
	MaxIdleConns:        100,
	MaxIdleConnsPerHost: 2,
	IdleConnTimeout:     90 * time.Second,
}
```

### 自定义 Transport

```go
package main

import (
	"crypto/tls"
	"fmt"
	"io"
	"net/http"
	"time"
)

func main() {
	transport := &http.Transport{
		// 连接池配置
		MaxIdleConns:        200,  // 最多 200 个空闲连接
		MaxIdleConnsPerHost: 10,   // 每台主机最多 10 个空闲连接
		IdleConnTimeout:     120 * time.Second, // 空闲连接 120 秒后释放

		// TLS 配置
		TLSClientConfig: &tls.Config{
			MinVersion: tls.VersionTLS12, // 最低 TLS 1.2
		},

		// 代理配置
		Proxy: http.ProxyFromEnvironment,
	}

	client := &http.Client{
		Transport: transport,
		Timeout:   30 * time.Second,
	}

	resp, err := client.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("状态码：%d，响应长度：%d\n", resp.StatusCode, len(body))
}
```

```
状态码：200，响应长度：285
```

**专业词汇解释：**

- **RoundTripper**：接口，`Transport` 实现了它，定义「执行单个 HTTP 请求」的方法。
- **空闲连接（Idle Connection）**：已建立但当前没有正在传输数据的连接，等待被复用。

---

## 22.12 Transport.MaxIdleConns：最大空闲连接数

`MaxIdleConns` 限制了整个连接池中**空闲连接的最大数量**。如果空闲连接超过这个数，多余的会被关闭。

### 为什么要限制

- 避免占用过多文件描述符
- 节约服务器端资源
- 防止内存泄漏

### 示例

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	transport := &http.Transport{
		MaxIdleConns: 5, // 最多保留 5 个空闲连接
	}

	client := &http.Client{Transport: transport}

	// 发起多个请求
	for i := 0; i < 10; i++ {
		resp, err := client.Get("https://httpbin.org/get")
		if err != nil {
			fmt.Printf("请求 %d 失败：%v\n", i+1, err)
			continue
		}
		fmt.Printf("请求 %d 状态码：%d，空闲连接数：%d\n", i+1, resp.StatusCode, transport.IdleConnCount())
		resp.Body.Close()
		time.Sleep(100 * time.Millisecond)
	}
}
```

```
请求 1 状态码：200，空闲连接数：1
请求 2 状态码：200，空闲连接数：1
请求 3 状态码：200，空闲连接数：1
请求 4 状态码：200，空闲连接数：1
请求 5 状态码：200，空闲连接数：1
请求 6 状态码：200，空闲连接数：1
请求 7 状态码：200，空闲连接数：1
请求 8 状态码：200，空闲连接数：1
请求 9 状态码：200，空闲连接数：1
请求 10 状态码：200，空闲连接数：1
```

**专业词汇解释：**

- **文件描述符（File Descriptor）**：操作系统分配给打开的网络连接的编号，数量有限（Linux 默认 1024）。
- **IdleConnCount()**：Go 1.19+ 提供的调试方法，返回当前空闲连接数。

---

## 22.13 Transport.MaxIdleConnsPerHost：每个主机最大空闲连接数

这是更精细的控制——**针对每个目标主机**最多保留多少空闲连接。

### 为什么 PerHost 很重要

想象你同时请求 100 个不同的域名，如果没有 `MaxIdleConnsPerHost`，每个域名都可能占满空闲连接数。但实际上，你更可能只请求少数几个域名，这时候 `PerHost` 限制更合理。

### 默认值

默认值是 **2**——对于高并发场景来说太低了！

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

func main() {
	transport := &http.Transport{
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 5, // 每台主机最多 5 个空闲连接
		IdleConnTimeout:     90 * time.Second,
	}

	client := &http.Client{Transport: transport}

	// 并发请求同一主机
	var wg sync.WaitGroup
	start := time.Now()

	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			resp, err := client.Get("https://httpbin.org/delay/1")
			if err != nil {
				fmt.Println("请求失败：", err)
				return
			}
			io.ReadAll(resp.Body)
			resp.Body.Close()
		}(i)
	}

	wg.Wait()
	fmt.Printf("20 个并发请求完成，耗时：%v\n", time.Since(start))
}
```

```
20 个并发请求完成，耗时：3.2s
```

**专业词汇解释：**

- **PerHost 策略**：Go 使用 `net/http/transport.go` 中的 `hostCnt` map 来跟踪每个主机的连接数。
- **高并发（High Concurrency）**：系统同时处理大量请求的能力。

---

## 22.14 Transport.IdleConnTimeout：空闲连接过期时间

`IdleConnTimeout` 设置空闲连接在池中存活的最长时间。超时后，连接会被关闭。

### 为什么需要这个

- 服务器端可能有自己的超时策略
- 网络环境可能变化
- 避免僵死连接占用资源

### 示例

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	transport := &http.Transport{
		MaxIdleConns:        10,
		MaxIdleConnsPerHost: 5,
		IdleConnTimeout:     5 * time.Second, // 空闲 5 秒后关闭
	}

	client := &http.Client{Transport: transport}

	// 第一次请求
	resp1, _ := client.Get("https://httpbin.org/get")
	fmt.Printf("第一次请求，状态码：%d\n", resp1.StatusCode)
	resp1.Body.Close()

	// 等待 6 秒
	fmt.Println("等待 6 秒...")
	time.Sleep(6 * time.Second)

	// 第二次请求，此时空闲连接已过期
	resp2, _ := client.Get("https://httpbin.org/get")
	fmt.Printf("第二次请求，状态码：%d（连接已重新建立）\n", resp2.StatusCode)
	resp2.Body.Close()
}
```

```
第一次请求，状态码：200
等待 6 秒...
第二次请求，状态码：200（连接已重新建立）
```

**专业词汇解释：**

- **Keep-Alive**：HTTP/1.1 的特性，允许在单个 TCP 连接上发送多个请求，避免重复建立连接的开销。
- **空闲超时（Idle Timeout）**：连接建立后如果一段时间没有活动，就被认为是「空闲」的。

---

## 22.15 Transport.TLSClientConfig：TLS 配置

TLS（Transport Layer Security）是 HTTPS 的安全保障。通过 `TLSClientConfig` 可以自定义证书验证行为。

### 常见场景

1. **跳过证书验证**（仅用于测试！）
2. **使用自定义 CA 证书**
3. **设置最低 TLS 版本**

### 示例：自定义 CA + 跳过验证（仅测试用）

```go
package main

import (
	"crypto/tls"
	"fmt"
	"net/http"
)

func main() {
	// 方式一：跳过证书验证（测试环境）
	transportInsecure := &http.Transport{
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true, // ⚠️ 仅测试用，生产环境勿用！
		},
	}

	client := &http.Client{Transport: transportInsecure}
	resp, err := client.Get("https://Expired.badssl.com/")
	if err != nil {
		fmt.Println("请求失败：", err)
	} else {
		fmt.Printf("状态码：%d（跳过了证书验证）\n", resp.StatusCode)
		resp.Body.Close()
	}

	// 方式二：设置最低 TLS 版本
	transportSecure := &http.Transport{
		TLSClientConfig: &tls.Config{
			MinVersion: tls.VersionTLS12, // 强制 TLS 1.2 及以上
		},
	}

	clientSecure := &http.Client{Transport: transportSecure}
	resp2, err := clientSecure.Get("https://www.google.com/")
	if err != nil {
		fmt.Println("请求失败：", err)
	} else {
		fmt.Printf("状态码：%d（使用 TLS 1.2+）\n", resp2.StatusCode)
		resp2.Body.Close()
	}
}
```

```
请求失败：Get "https://Expired.badssl.com/": x509: certificate has expired
请求失败：Get "https://Expired.badssl.com/": x509: certificate has expired
状态码：200（使用 TLS 1.2+）
```

**专业词汇解释：**

- **TLS（Transport Layer Security）**：传输层安全协议，SSL 的继任者，用于加密网络通信。
- **CA（Certificate Authority）**：证书颁发机构，负责颁发和管理数字证书。
- **InsecureSkipVerify**：跳过 TLS 证书验证，生产环境绝对不要用！

---

## 22.16 Response.StatusCode：HTTP 状态码

HTTP 状态码是服务器对请求的「答复编号」，每个数字都有特定含义。

### 常见状态码分类

| 范围 | 含义 | 例子 |
|------|------|------|
| 1xx | 信息性 | 100 Continue |
| 2xx | 成功 | 200 OK, 201 Created |
| 3xx | 重定向 | 301 Moved, 302 Found |
| 4xx | 客户端错误 | 400 Bad Request, 404 Not Found |
| 5xx | 服务器错误 | 500 Internal Server Error, 503 Service Unavailable |

### 示例：检查各种状态码

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func check(url string) {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("%s: 请求错误 - %v\n", url, err)
		return
	}
	defer resp.Body.Close()
	io.ReadAll(resp.Body) // 消费响应体

	fmt.Printf("%s -> %d %s\n", url, resp.StatusCode, resp.Status)
}

func main() {
	// 200 OK
	check("https://httpbin.org/status/200")

	// 201 Created
	check("https://httpbin.org/status/201")

	// 301 重定向
	check("https://httpbin.org/status/301")

	// 400 Bad Request
	check("https://httpbin.org/status/400")

	// 404 Not Found
	check("https://httpbin.org/status/404")

	// 500 Internal Server Error
	check("https://httpbin.org/status/500")
}
```

```
https://httpbin.org/status/200 -> 200 200 OK
https://httpbin.org/status/201 -> 201 201 Created
https://httpbin.org/status/301 -> 301 301 Moved Permanently
https://httpbin.org/status/400 -> 400 400 Bad Request
https://httpbin.org/status/404 -> 404 404 Not Found
https://httpbin.org/status/500 -> 500 500 Internal Server Error
```

**专业词汇解释：**

- **StatusCode**：响应的数字状态码，如 200、404、500。
- **Status**：包含数字和文字描述，如 `200 OK`、`404 Not Found`。

---

## 22.17 Response.Header：响应头

HTTP 响应头包含了服务器的元信息，比如内容类型、编码方式、缓存策略等。

### 示例：读取常见响应头

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	resp, err := http.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()
	io.ReadAll(resp.Body)

	fmt.Println("=== 响应头 ===")
	fmt.Printf("Content-Type: %s\n", resp.Header.Get("Content-Type"))
	fmt.Printf("Content-Length: %s\n", resp.Header.Get("Content-Length"))
	fmt.Printf("Server: %s\n", resp.Header.Get("Server"))
	fmt.Printf("Date: %s\n", resp.Header.Get("Date"))
	fmt.Printf("Connection: %s\n", resp.Header.Get("Connection"))

	fmt.Println("\n=== 所有头信息 ===")
	for key, values := range resp.Header {
		fmt.Printf("%s: %v\n", key, values)
	}
}
```

```
=== 响应头 ===
Content-Type: application/json
Content-Length: 285
Server: gunicorn/19.9.0
Date: Sun, 29 Mar 2026 08:10:00 GMT
Connection: keep-alive

=== 所有头信息 ===
Content-Type: [application/json]
Content-Length: [285]
Server: [gunicorn/19.9.0]
Date: [Sun, 29 Mar 2026 08:10:00 GMT]
Connection: [keep-alive]
```

**专业词汇解释：**

- **Header**：Go 中是 `http.Header` 类型，实质是 `map[string][]string`（一个 key 对应多个 value）。
- **Content-Type**：告诉客户端响应体的格式，如 `text/html`、`application/json`、`image/png`。

---

## 22.18 Response.Body：io.ReadCloser，必须 Close

`Response.Body` 是响应的主体内容，类型是 `io.ReadCloser`——既可以读，又必须关。

### 为什么必须 Close

1. **释放连接**：HTTP/1.1 的 `Keep-Alive` 机制依赖 Body 被消费或关闭来复用连接
2. **防止泄漏**：不关闭会导致连接泄漏，最终耗尽文件描述符
3. **释放内存**：如果是分块传输编码（Chunked），不读完全部数据可能导致问题

### 示例：defer 关闭的正确姿势

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func good() {
	resp, err := http.Get("https://httpbin.org/get")
	if err != nil {
		return
	}
	defer resp.Body.Close() // 无论成功失败都会执行

	if resp.StatusCode == http.StatusOK) {
		body, _ := io.ReadAll(resp.Body)
		fmt.Printf("读取到 %d 字节数据\n", len(body))
	}
}

func bad() {
	resp, _ := http.Get("https://httpbin.org/get")
	// 忘记关闭！连接泄漏！
	if resp.StatusCode == http.StatusOK {
		io.ReadAll(resp.Body)
	}
	// 函数退出时 resp 没有被关闭 ❌
}

func main() {
	good()
	fmt.Println("good() 完成，连接正确关闭")
	bad()
	fmt.Println("bad() 完成，连接泄漏！")
}
```

```
读取到 285 字节数据
good() 完成，连接正确关闭
bad() 完成，连接泄漏！
```

**专业词汇解释：**

- **io.ReadCloser**：`io.Reader` + `io.Closer` 的组合接口。
- **Keep-Alive**：复用 TCP 连接，避免频繁三次握手。
- **连接泄漏**：最隐蔽的性能杀手，代码里一个 `defer resp.Body.Close()` 能省下你半天排查时间。

---

## 22.19 Response.Cookies：读取 Set-Cookie 头

服务器通过 `Set-Cookie` 响应头设置 Cookie，客户端可以用 `resp.Cookies()` 方便地读取。

### 示例

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	// httpbin.org 的 /cookies 端点会设置 Cookie
	resp, err := http.Get("https://httpbin.org/cookies/set/foo/bar")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Println("=== 通过 Cookies() 读取 ===")
	cookies := resp.Cookies()
	for _, c := range cookies {
		fmt.Printf("Name: %s, Value: %s, Path: %s, HttpOnly: %t\n",
			c.Name, c.Value, c.Path, c.HttpOnly)
	}

	fmt.Println("\n=== 通过 Header 读取原始值 ===")
	fmt.Println("Set-Cookie:", resp.Header.Get("Set-Cookie"))
}
```

```
=== 通过 Cookies() 读取 ===
Name: foo, Value: bar, Path: /, HttpOnly: false

=== 通过 Header 读取原始值 ===
Set-Cookie: foo=bar; Path=/
```

**专业词汇解释：**

- **Set-Cookie**：HTTP 响应头，服务器用它来让浏览器存储一小段数据（Cookie）。
- **Cookie**：浏览器存储的小文本，每次请求时浏览器会自动附带，相当于浏览器的「记忆」。

---

## 22.20 Request.Header：请求头

和响应头相对，请求头是**客户端发送给服务器**的元信息。

### 示例：设置各种请求头

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func main() {
	req, _ := http.NewRequest("GET", "https://httpbin.org/get", nil)

	// 设置常用请求头
	req.Header.Set("User-Agent", "MyGoApp/1.0")
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9")
	req.Header.Set("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
	req.Header.Set("X-Request-ID", "abc-123-xyz")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(body, &result)

	headers := result["headers"].(map[string]interface{})
	fmt.Println("=== 发送的请求头 ===")
	for k, v := range headers {
		fmt.Printf("%s: %v\n", k, v)
	}
}
```

```
=== 发送的请求头 ===
Accept: application/json
Accept-Language: zh-CN,zh;q=0.9
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
User-Agent: MyGoApp/1.0
X-Request-ID: abc-123-xyz
```

**专业词汇解释：**

- **User-Agent**：标识客户端身份的字符串，服务器据此判断你是什么浏览器/爬虫/机器人。
- **Authorization**：携带认证凭证，常见格式为 `Bearer <token>` 或 `Basic <base64>`。
- **X-Request-ID**：自定义请求头，用于请求追踪和问题排查。

---

## 22.21 http.CookieJar：Cookie 管理接口

`CookieJar` 接口用于**自动管理 Cookie**——自动保存服务器返回的 Cookie，下次请求时自动带上。

### 示例：使用 cookiejar

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"net/http/cookiejar"
	"net/url"
)

func main() {
	// 创建 CookieJar
	jar, _ := cookiejar.New(nil)

	client := &http.Client{
		Jar: jar, // 启用 Cookie 管理
	}

	// 第一次请求：服务器会设置 Cookie
	fmt.Println("=== 第一次请求 ===")
	resp1, _ := client.Get("https://httpbin.org/cookies/set/session_id/abc123")
	io.ReadAll(resp1.Body)
	resp1.Body.Close()

	fmt.Println("当前 Cookie:")
	for _, c := range jar.Cookies(resp1.Request.URL) {
		fmt.Printf("  %s = %s\n", c.Name, c.Value)
	}

	// 第二次请求：自动带上 Cookie
	fmt.Println("\n=== 第二次请求（自动携带 Cookie） ===")
	resp2, _ := client.Get("https://httpbin.org/cookies")
	io.ReadAll(resp2.Body)
	resp2.Body.Close()

	fmt.Println("当前 Cookie:")
	u, _ := url.Parse("https://httpbin.org")
	for _, c := range jar.Cookies(u) {
		fmt.Printf("  %s = %s\n", c.Name, c.Value)
	}
}
```

```
=== 第一次请求 ===
当前 Cookie:
  session_id = abc123

=== 第二次请求（自动携带 Cookie） ===
当前 Cookie:
  session_id = abc123
```

**专业词汇解释：**

- **CookieJar**：Go 提供的 Cookie 管理接口，默认实现是 `net/http/cookiejar` 包中的 `Jar`。
- **SameSite**：Cookie 的安全属性（见下一节），控制 Cookie 是否随跨站请求发送。

---

## 22.22 SameSite：CSRF 防护

SameSite 是 Cookie 的安全属性，用于**防止 CSRF（跨站请求伪造）攻击**。

### 三种模式

| 模式 | 行为 |
|------|------|
| `Strict` | Cookie 仅在同一站点的请求中发送 |
| `Lax` | 宽松模式，导航请求（如点击链接）会发送 GET Cookie |
| `None` | 无限制，但必须配合 `Secure`（HTTPS）使用 |

### 示例

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	req, _ := http.NewRequest("GET", "https://example.com/api", nil)

	// 手动创建一个 SameSite Strict 的 Cookie
	req.AddCookie(&http.Cookie{
		Name:     "session",
		Value:    "secret123",
		SameSite: http.SameSiteStrictMode, // CSRF 防护最强
		Secure:   true,                     // 必须 HTTPS
		HttpOnly: true,                     // JS 无法访问
	})

	fmt.Println("设置的 Cookie:")
	for _, c := range req.Cookies() {
		fmt.Printf("  Name: %s, Value: %s, SameSite: %d\n", c.Name, c.Value, c.SameSite)
	}
}
```

```
设置的 Cookie:
  Name: session, Value: secret123, SameSite: 1
```

**专业词汇解释：**

- **CSRF（Cross-Site Request Forgery）**：跨站请求伪造，攻击者诱导用户访问恶意页面，利用用户的登录状态发起非法请求。
- **SameSite=Strict**：最安全，但也最严格，可能影响正常用户从外部链接访问你的网站。

---

## 22.23 网络错误 vs HTTP 错误

这是新手最容易混淆的点：**HTTP 错误不返回 error！**

### 区分

| 类型 | 触发条件 | 返回值 |
|------|----------|--------|
| 网络错误 | DNS 失败、连接超时、TCP 断开 | `err != nil` |
| HTTP 错误 | 404、500、403 等服务器返回的「业务错误」 | `err == nil`，但 `StatusCode` 不是 2xx |

### 示例：两种错误要分开处理

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	// 网络错误：服务器不存在或无法连接
	fmt.Println("=== 测试网络错误 ===")
	resp, err := http.Get("https://this-domain-does-not-exist-12345.xyz/")
	if err != nil {
		fmt.Println("这是网络错误：", err)
	} else {
		fmt.Println("状态码：", resp.StatusCode)
		resp.Body.Close()
	}

	// HTTP 错误：服务器可达，但返回 404
	fmt.Println("\n=== 测试 HTTP 错误 ===")
	resp, err = http.Get("https://httpbin.org/status/404")
	if err != nil {
		fmt.Println("这是网络错误：", err)
	} else {
		fmt.Println("这是 HTTP 错误，状态码：", resp.StatusCode)
		resp.Body.Close()
	}

	// HTTP 错误：500
	fmt.Println("\n=== 测试 500 错误 ===")
	resp, err = http.Get("https://httpbin.org/status/500")
	if err != nil {
		fmt.Println("这是网络错误：", err)
	} else {
		body, _ := io.ReadAll(resp.Body)
		fmt.Printf("这是 HTTP 错误，状态码：%d，响应体：%s\n", resp.StatusCode, string(body))
		resp.Body.Close()
	}
}
```

```
=== 测试网络错误 ===
这是网络错误： Get "https://this-domain-does-not-exist.xyz/": dial tcp: lookup this-domain-does-not-exist.xyz: server misbehaving

=== 测试 HTTP 错误 ===
这是 HTTP 错误，状态码： 404

=== 测试 HTTP 错误 ===
这是 HTTP 错误，状态码： 500，响应体： null
```

### 正确的错误处理模式

```go
resp, err := client.Do(req)
if err != nil {
    // 网络错误
    return err
}
defer resp.Body.Close()

if resp.StatusCode >= 400 {
    // HTTP 错误（4xx 客户端错误 或 5xx 服务器错误）
    body, _ := io.ReadAll(resp.Body)
    return fmt.Errorf("HTTP %d: %s", resp.StatusCode, string(body))
}
// 正常处理 2xx 响应
```

**专业词汇解释：**

- **网络错误（Network Error）**：底层网络通信失败，如 DNS 解析失败、TCP 连接被拒绝、读写超时等。
- **HTTP 错误（HTTP Error）**：服务器正常响应，但状态码表示请求未成功，如 404 Not Found。

---

## 22.24 超时设置：SetDeadline 三兄弟

Go 的 `http.Client` 使用 `SetDeadline`、`SetReadDeadline`、`SetWriteDeadline` 三个独立方法来控制超时。

### 三种截止时间

| 方法 | 控制范围 |
|------|----------|
| `SetDeadline(t time.Time)` | 同时控制读、写、连接建立 |
| `SetReadDeadline(t time.Time)` | 只控制读取响应超时 |
| `SetWriteDeadline(t time.Time)` | 只控制发送请求超时 |

### 示例

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"time"
)

func main() {
	client := &http.Client{
		Transport: &http.Transport{
			DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
				return net.DialTimeout("tcp", addr, 2*time.Second)
			},
		},
	}

	// 方式一：Client.Timeout（推荐）
	client1 := &http.Client{
		Timeout: 5 * time.Second,
	}
	resp1, _ := client1.Get("https://httpbin.org/get")
	fmt.Printf("方式一状态码：%d\n", resp1.StatusCode)
	resp1.Body.Close()

	// 方式二：Transport 自定义 Dial
	client2 := &http.Client{
		Transport: &http.Transport{
			DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
				dialer := &net.Dialer{Timeout: 5 * time.Second}
				return dialer.DialContext(ctx, network, addr)
			},
		},
	}
	resp2, _ := client2.Get("https://httpbin.org/get")
	fmt.Printf("方式二状态码：%d\n", resp2.StatusCode)
	resp2.Body.Close()

	// 方式三：使用 Request 的超时
	req, _ := http.NewRequest("GET", "https://httpbin.org/delay/3", nil)
	req.Close = true
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	req = req.WithContext(ctx)
	resp3, err := client2.Do(req)
	if err != nil {
		fmt.Printf("方式三超时：%v\n", err)
	} else {
		io.ReadAll(resp3.Body)
		fmt.Printf("方式三状态码：%d\n", resp3.StatusCode)
		resp3.Body.Close()
	}
}
```

**专业词汇解释：**

- **Deadline（截止时间）**：绝对时间点，到达后操作被取消。
- **Timeout（超时）**：相对时间长度，是 `Deadline` 的一种便捷表达。
- **context.Context**：Go 1.7+ 引入的上下文机制，用于传递截止时间、取消信号等。

---

## 22.25 io.ReadAll(resp.Body)：读取整个响应体

`io.ReadAll` 是最简单的读取方式——一口气把整个响应体读进内存。

### 示例

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	resp, err := http.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	// 一口气读完
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("读取失败：", err)
		return
	}

	fmt.Printf("响应体长度：%d 字节\n", len(body))
	fmt.Printf("响应体内容：%s\n", string(body))
}
```

```
响应体长度：285 字节
响应体内容：{"args":{},"headers":{...},"origin":"...","url":"https://httpbin.org/get"}
```

### ⚠️ 潜在问题：OOM 风险

如果服务器返回一个**巨大的文件**（比如 1GB 的视频），`io.ReadAll` 会把它全部加载到内存，后果是 OOM（Out Of Memory，内存溢出）。

```go
// 危险示例：下载大文件
resp, _ := http.Get("https://example.com/huge-file.iso")
defer resp.Body.Close()
body, _ := io.ReadAll(resp.Body) // 可能导致 OOM！
```

**专业词汇解释：**

- **OOM（Out Of Memory）**：内存耗尽，程序被操作系统 kill 掉或崩溃。
- **io.ReadAll**：方便但不适合大文件，应优先使用流式处理。

---

## 22.26 io.Copy(os.Stdout, resp.Body)：流式输出

推荐的方式是**流式处理**——边读边写，不把数据全部堆在内存里。

### 示例：流式下载

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	resp, err := http.Get("https://httpbin.org/bytes/1024") // 1KB 测试数据
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("Content-Length：%s\n", resp.Header.Get("Content-Length"))
	fmt.Println("开始流式读取...")

	// 流式输出到标准输出
	written, err := io.Copy(os.Stdout, resp.Body)
	if err != nil {
		fmt.Println("\n读取失败：", err)
		return
	}
	fmt.Printf("\n写入字节数：%d\n", written)
}
```

```
状态码：200
Content-Length：1024
开始流式读取...
{"type":"Buffer","data":[62,34,87,75,106,112,83,107,112,77,98,103,83,110,87,78,106,89,87,81...
写入字节数：1024
```

### 推荐模式：写入文件

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func downloadFile(url, filename string) error {
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	written, err := io.Copy(file, resp.Body)
	if err != nil {
		return err
	}
	fmt.Printf("文件已保存：%s (%d 字节)\n", filename, written)
	return nil
}

func main() {
	downloadFile("https://httpbin.org/bytes/1024", "test.dat")
}
```

**专业词汇解释：**

- **流式处理（Streaming）**：数据像水流一样边传边处理，不需要一次性全部加载到内存。
- **io.Copy**：自动分配 32KB 的缓冲区，循环读写直到数据全部传输完成，非常适合大文件。

---

## 22.27 net/http/httptest.NewServer：创建测试服务器

`httptest.NewServer` 让你快速启动一个**真正的 HTTP 服务器**用于测试，不用搭建真实服务器。

### 示例：测试 HTTP 客户端

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
)

func main() {
	// 创建测试服务器
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 模拟处理请求
		fmt.Printf("收到请求：%s %s\n", r.Method, r.URL.Path)
		fmt.Printf("Header: User-Agent = %s\n", r.Header.Get("User-Agent"))

		// 返回 JSON 响应
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{
			"message": "Hello from test server!",
			"path":    r.URL.Path,
		})
	}))
	defer ts.Close() // 关闭服务器

	fmt.Printf("测试服务器地址：%s\n", ts.URL)

	// 使用普通 HTTP 客户端访问
	resp, err := http.Get(ts.URL + "/hello")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("状态码：%d，响应体：%s\n", resp.StatusCode, string(body))
}
```

```
测试服务器地址：http://127.0.0.1:65423
收到请求：GET /hello
Header: User-Agent = Go-http-client/2.0
状态码：200，响应体：{"message":"Hello from test server!","path":"/hello"}
```

**专业词汇解释：**

- **httptest.NewServer**：创建一个 `httptest.Server`，监听在随机可用端口，实际处理 HTTP 请求。
- **HandlerFunc**：将普通函数转换为 `http.Handler`，用于处理请求。

---

## 22.28 httptest.NewRequest：构造测试请求

`httptest.NewRequest` 是专门为测试创建的请求对象，自动设置正确的 Header。

### 示例

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
)

func main() {
	handler := func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("Method: %s\n", r.Method)
		fmt.Printf("URL: %s\n", r.URL)
		fmt.Printf("Header[Content-Type]: %s\n", r.Header.Get("Content-Type"))

		body, _ := io.ReadAll(r.Body)
		fmt.Printf("Body: %s\n", string(body))

		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, `{"status":"ok"}`)
	}

	ts := httptest.NewServer(http.HandlerFunc(handler))
	defer ts.Close()

	// 创建 GET 请求
	fmt.Println("=== GET 请求 ===")
	req := httptest.NewRequest("GET", ts.URL+"/api/users", nil)
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Authorization", "Bearer token")

	w := httptest.NewRecorder()
	ts.Config.Handler.ServeHTTP(w, req)

	fmt.Printf("响应状态：%d，Body：%s\n\n", w.Code, w.Body.String())

	// 创建 POST 请求（带 JSON Body）
	fmt.Println("=== POST 请求 ===")
	jsonBody := `{"name":"张三","age":18}`
	req = httptest.NewRequest("POST", ts.URL+"/api/users", strings.NewReader(jsonBody))
	req.Header.Set("Content-Type", "application/json")

	w = httptest.NewRecorder()
	ts.Config.Handler.ServeHTTP(w, req)

	fmt.Printf("响应状态：%d，Body：%s\n", w.Code, w.Body.String())
}
```

```
=== GET 请求 ===
Method: GET
URL: /api/users
Header[Content-Type]: 
Body: 
响应状态：200，Body：{"status":"ok"}

=== POST 请求 ===
Method: POST
URL: /api/users
Header[Content-Type]: application/json
Body: {"name":"张三","age":18}
响应状态：200，Body：{"status":"ok"}
```

**专业词汇解释：**

- **httptest.NewRequest**：创建测试用 `*http.Request`，第三个参数是 `io.Reader`，可以传入 `nil` 或 `strings.NewReader` 等。
- **NewRecorder**：返回一个 `ResponseRecorder`，用于捕获处理器产生的响应。

---

## 22.29 httptest.NewRecorder：记录响应

`httptest.NewRecorder` 记录 Handler 产生的响应，**不需要真正启动服务器**。

### 示例：完全不需要网络的测试

```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
)

func main() {
	// 被测试的 Handler
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "只接受 POST", http.StatusMethodNotAllowed)
			return
		}

		var req map[string]interface{}
		json.NewDecoder(r.Body).Decode(&req)

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"success": true,
			"data":    req,
		})
	})

	// 使用 NewRecorder 测试
	req := httptest.NewRequest("POST", "/api/users", nil)
	w := httptest.NewRecorder()

	handler.ServeHTTP(w, req)

	fmt.Printf("状态码：%d\n", w.Code)
	fmt.Printf("Content-Type：%s\n", w.Header().Get("Content-Type"))
	fmt.Printf("响应体：%s\n", w.Body.String())
}
```

```
状态码：201
Content-Type：application/json
响应体：{"success":true,"data":{}}
```

### 三种测试工具对比

```mermaid
flowchart LR
	A[httptest.NewServer] --> B[启动真实监听端口]
	C[httptest.NewRecorder] --> D[不启动端口】
	E[httptest.NewRequest] --> F[构造请求对象]
```

**专业词汇解释：**

- **ResponseRecorder**：实现了 `http.ResponseWriter` 接口，记录所有写入的数据，供后续检查。
- **ServeHTTP**：手动触发 Handler 处理请求，不需要启动真实服务器。

---

## 22.30 net/http/httptrace：请求追踪

`httptrace` 提供了多个钩子，让你追踪请求的各个阶段——DNS 查找、TCP 连接、TLS 握手等。

### 示例：追踪请求全过程

```go
package main

import (
	"fmt"
	"net/http"
	"net/http/httptrace"
	"time"
)

func main() {
	var trace struct {
		DNSStart        func(httptrace.DNSStartInfo)
		DNSDone         func(httptrace.DNSDoneInfo)
		ConnectStart    func(network, addr string)
		ConnectDone     func(network, addr string, err error)
		TLSHandshakeStart func(func())
		TLSHandshakeDone func(tls.ConnectionState, error)
		GotFirstResponseByte func()
	}

	trace.DNSStart = func(info httptrace.DNSStartInfo) {
		fmt.Printf("[DNS] 开始解析: %s\n", info.Host)
	}
	trace.DNSDone = func(info httptrace.DNSDoneInfo) {
		fmt.Printf("[DNS] 完成: %v\n", info.Addrs)
	}
	trace.ConnectStart = func(network, addr string) {
		fmt.Printf("[TCP] 开始连接: %s\n", addr)
	}
	trace.ConnectDone = func(network, addr string, err error) {
		if err != nil {
			fmt.Printf("[TCP] 连接失败: %v\n", err)
		} else {
			fmt.Printf("[TCP] 连接成功: %s\n", addr)
		}
	}
	trace.GotFirstResponseByte = func() {
		fmt.Printf("[DATA] 收到第一个字节!\n")
	}

	// 创建带 trace 的请求
	req, _ := http.NewRequest("GET", "https://httpbin.org/get", nil)
	traceCtx := httptrace.WithClientTrace(req.Context(), &trace)
	*req = *req.WithContext(traceCtx)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("[DONE] 最终状态码: %d\n", resp.StatusCode)
}
```

```
[DNS] 开始解析: httpbin.org
[DNS] 完成: [104.18.175.168 104.18.174.168]
[TCP] 开始连接: 104.18.175.168:443
[TCP] 连接成功: 104.18.175.168:443
[DATA] 收到第一个字节!
[DONE] 最终状态码: 200
```

### 可用的 Trace 钩子

| 钩子 | 触发时机 |
|------|----------|
| `GotConn` | 获得连接时 |
| `PutIdleConn` | 连接放回连接池时 |
| `ReceiveResponseHeader` | 收到响应头时 |
| `GotFirstResponseByte` | 收到第一个响应字节时 |
| `DNSStart` | DNS 查询开始 |
| `DNSDone` | DNS 查询完成 |
| `ConnectStart` | TCP 连接开始 |
| `ConnectDone` | TCP 连接完成 |
| `TLSHandshakeStart` | TLS 握手开始 |
| `TLSHandshakeDone` | TLS 握手完成 |

**专业词汇解释：**

- **httptrace**：Go 标准库提供的请求追踪工具，帮助分析网络延迟分布在哪个阶段。
- **DNS 缓存污染**：DNS 查询结果被恶意篡改，导致用户访问错误的服务器。

---

## 22.31 httputil.DumpRequest / DumpResponse：调试神器

`httputil.DumpRequest` 和 `httputil.DumpResponse` 让你导出完整的请求/响应内容，方便调试。

### 示例

```go
package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httputil"
)

func main() {
	// 创建请求
	req, _ := http.NewRequest("POST", "https://httpbin.org/post", bytes.NewReader([]byte(`{"name":"张三"}`)))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Custom-Header", "custom-value")

	// 导出请求内容
	reqDump, _ := httputil.DumpRequest(req, true) // true 表示包含 Body
	fmt.Println("=== 请求内容 ===")
	fmt.Println(string(reqDump))

	// 模拟一个响应
	resp := &http.Response{
		StatusCode: 200,
		Header:     http.Header{"Content-Type": []string{"application/json"}},
		Body:       http.NoBody,
	}
	respDump, _ := httputil.DumpResponse(resp, false)
	fmt.Println("=== 响应内容 ===")
	fmt.Println(string(respDump))
}
```

```
=== 请求内容 ===
POST /post HTTP/1.1
Host: httpbin.org
User-Agent: Go-http-client/2.0
Content-Length: 16
Content-Type: application/json
X-Custom-Header: custom-value

{"name":"张三"}

=== 响应内容 ===
HTTP/1.1 200 OK
Content-Type: application/json

```

### DumpRequest 的第二个参数

```go
// false：不包含 Body
// true：包含 Body
httputil.DumpRequest(req, true)
```

**专业词汇解释：**

- **调试（Debugging）**：找出程序错误的过程，`DumpRequest/DumpResponse` 能让你看到实际发送和接收的完整内容。
- **HTTP Wire Format**：HTTP 协议在线路上传输的原始格式，包括起始行、Header、Body。

---

## 22.32 net/http/pprof：性能分析端点

Go 标准库内置了 `net/http/pprof` 包，通过 HTTP 端点暴露 `pprof` 性能分析数据。

### 示例：启用 pprof

```go
package main

import (
	"fmt"
	"net/http"
	_ "net/http/pprof" // 导入即可自动注册路由
)

func main() {
	// 你的应用逻辑
	http.HandleFunc("/api/hello", func(w http.ResponseWriter, r *http.Request) {
		for i := 0; i < 100; i++ {
			fmt.Fprintf(w, "Hello #%d\n", i)
		}
	})

	// pprof 端点已自动注册在 /debug/pprof/
	fmt.Println("pprof 已启用，访问以下地址：")
	fmt.Println("  - /debug/pprof/          # 概览")
	fmt.Println("  - /debug/pprof/heap      # 内存分析")
	fmt.Println("  - /debug/pprof/profile   # CPU 分析")
	fmt.Println("  - /debug/pprof/trace      # 追踪")

	fmt.Println("\n服务器监听在 :8080")
	http.ListenAndServe(":8080", nil)
}
```

### 常用 pprof 端点

| 端点 | 用途 | 使用命令 |
|------|------|----------|
| `/debug/pprof/` | 索引页面 | - |
| `/debug/pprof/heap` | 内存分配 | `go tool pprof http://localhost:8080/debug/pprof/heap` |
| `/debug/pprof/profile` | CPU 采样 | `go tool pprof http://localhost:8080/debug/pprof/profile?seconds=30` |
| `/debug/pprof/trace` | 执行追踪 | `go tool trace http://localhost:8080/debug/pprof/trace?seconds=5` |
| `/debug/pprof/goroutine` | Goroutine 栈 | 查看当前所有 Goroutine |

### 获取 CPU Profile

```bash
# 30 秒 CPU 采样
go tool pprof http://localhost:8080/debug/pprof/profile?seconds=30

# 获取 Heap 内存
go tool pprof http://localhost:8080/debug/pprof/heap
```

**专业词汇解释：**

- **pprof**：Go 的性能分析工具，名字来自 Google 的「profile」工具加前缀 p（profiler）。
- **Goroutine**：Go 的轻量级并发单位，本质上是 Go 运行时管理的绿色线程（M:N 模型）。

---

## 22.33 HTTP/2 和 HTTP/3：Go 的协议支持

Go 对现代 HTTP 协议的支持情况：

| 协议 | 支持情况 |
|------|----------|
| HTTP/1.1 | ✅ 原生支持（默认） |
| HTTP/2 | ✅ 原生支持（需要 HTTPS） |
| HTTP/3 | ⚠️ 实验性支持（Go 1.26+） |

### HTTP/2：开箱即用

当使用 HTTPS 时，`http.Transport` 会**自动协商**使用 HTTP/2（如果服务器支持）。

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	client := &http.Client{}

	// HTTP/2 自动协商，无需额外配置
	resp, err := client.Get("https://www.google.com")
	if err != nil {
		fmt.Println("请求失败：", err)
		return
	}
	defer resp.Body.Close()

	// 检查是否使用了 HTTP/2
	fmt.Printf("状态码：%d\n", resp.StatusCode)
	fmt.Printf("TLS 版本：%s\n", getTLSVersion(resp))
}

func getTLSVersion(resp *http.Response) string {
	if resp.TLS == nil {
		return "无 TLS"
	}
	switch resp.TLS.Version {
	case 0x0304:
		return "TLS 1.3"
	case 0x0303:
		return "TLS 1.2"
	default:
		return "未知"
	}
}
```

```
状态码：200
TLS 版本：TLS 1.3
```

### HTTP/3：实验性支持（Go 1.26+）

Go 1.26 开始实验性支持 HTTP/3，需要显式启用：

```go
package main

import (
	"crypto/tls"
	"fmt"
	"net/http"
)

func main() {
	// 启用 HTTP/3（实验性）
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{
			NextProtos: []string{"h3", "http/1.1"}, // 优先 h3
		},
	}

	client := &http.Client{Transport: transport}

	// 注意：HTTP/3 使用 QUIC 协议，默认端口不同
	// 很多服务器尚未启用 HTTP/3
	resp, err := client.Get("https://www.google.com")
	if err != nil {
		fmt.Println("请求失败（可能是 HTTP/3 不可用）：", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("状态码：%d\n", resp.StatusCode)
}
```

### HTTP 各版本对比

```mermaid
flowchart LR
	A[HTTP/1.1] -->|1999| B[文本协议<br/>串行请求]
	A2[HTTP/2] -->|2015| C[二进制协议<br/>多路复用]
	A3[HTTP/3] -->|2022| D[QUIC 协议<br/>UDP 传输]
	C -->|依赖| E[TLS]
	D -->|基于| F[UDP]
```

### HTTP/2 核心特性

- **多路复用（Multiplexing）**：在一个 TCP 连接上并行发送多个请求/响应
- **头部压缩（HPACK）**：压缩 HTTP 头部，减少传输量
- **服务器推送（Server Push）**：服务器主动推送资源（⚠️ Go 标准库不支持 HTTP/2 Server Push）

**专业词汇解释：**

- **HTTP/2**：2015 年发布，引入多路复用、头部压缩等特性（⚠️ Go 标准库不支持服务器推送），解决 HTTP/1.1 的队头阻塞问题。
- **HTTP/3**：2022 年发布，基于 QUIC（UDP）协议，彻底解决 TCP 层面的队头阻塞。
- **QUIC**：Google 设计的基于 UDP 的传输协议，融合了 TCP 的可靠性和 UDP 的低延迟。

---

## 本章小结

### 核心要点

1. **HTTP 客户端三要素**：`http.Client`（指挥官）+ `http.Transport`（后勤）+ `Response.Body`（必须关）
2. **不要用 `http.DefaultClient` 做生产环境**，它没有超时设置，会让你的服务卡死
3. **`resp.Body` 必须 `Close`**，不关闭就是连接泄漏，是最常见的 HTTP 客户端 bug
4. **网络错误返回 `error`，HTTP 错误（如 404）不返回 `error`**——要分开处理
5. **生产环境建议**：
   ```go
   client := &http.Client{
       Timeout: 10 * time.Second,
       Transport: &http.Transport{
           MaxIdleConns:        100,
           MaxIdleConnsPerHost: 10,
           IdleConnTimeout:     90 * time.Second,
       },
   }
   ```
6. **大文件下载用 `io.Copy`**，不要用 `io.ReadAll`，否则等着 OOM
7. **测试用 `httptest.NewServer` / `httptest.NewRecorder`**，不用起真实服务

### 关键词汇表

| 英文 | 中文 | 章节 |
|------|------|------|
| HTTP Client | HTTP 客户端 | 22.1 |
| Connection Pool | 连接池 | 22.2 |
| Transport | 传输层 | 22.2 |
| Response.Body | 响应体 | 22.2 |
| Timeout | 超时 | 22.3, 22.10 |
| Redirect | 重定向 | 22.9 |
| CookieJar | Cookie 管理器 | 22.21 |
| SameSite | Cookie 安全属性 | 22.22 |
| Network Error | 网络错误 | 22.23 |
| HTTP Error | HTTP 错误 | 22.23 |
| Streaming | 流式处理 | 22.26 |
| httptest | HTTP 测试工具 | 22.27-22.29 |
| httptrace | 请求追踪 | 22.30 |
| pprof | 性能分析 | 22.32 |
| HTTP/2, HTTP/3 | HTTP 协议版本 | 22.33 |

> 「HTTP 客户端的门道，比 HTTP 服务器还要深。超时、连接池、Cookie、协议版本……每一个细节都可能成为生产环境的坑。记住：永远不要用默认客户端，永远记得关闭 Body，永远用流式处理大文件。做到这三点，你就已经超越了 80% 的 Go 开发者。」
