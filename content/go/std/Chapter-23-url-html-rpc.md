+++
title = "第23章：URL、HTML 与 RPC"
weight = 230
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第23章：URL、HTML 与 RPC

> "互联网的三大基石：URL 让人找到东西，HTML 让人看懂东西，RPC 让人调用东西。三者合一，天下我有。"
> —— 某位不愿透露姓名的 Go 语言爱好者

在互联网的浩瀚宇宙中，URL 是宇宙坐标，HTML 是网页的皮肤，RPC 是服务间对话的暗号。本章我们将一起探索 Go 语言标准库中处理这三驾马车的神器：`net/url`、`net/html`、`html/template` 和 `net/rpc`。准备好了吗？系好安全带，我们发车！

---

## 23.1 net/url 包解决什么问题：URL 包含协议、域名、路径、查询参数

你有没有想过，当你输入 `https://example.com:8080/path/to/file?key=value&name=张三` 这样的网址时，背后发生了什么？浏览器是如何解析出协议（https）、域名（example.com）、端口（8080）、路径（/path/to/file）和查询参数（key=value&name=张三）的？

答案是：它需要一个 URL 解析器，而 Go 的 `net/url` 包就是干这个的！

**专业词汇解释：**

- **URL（Uniform Resource Locator）**：统一资源定位符，互联网上的地址门牌号
- **协议（Scheme）**：http、https、ftp 等通信协议，就像快递公司
- **域名（Domain）**：网站的名称，如 example.com
- **路径（Path）**：资源在服务器上的位置，像文件夹路径
- **查询参数（Query）**：URL 中 `?` 后面的键值对，用于传递额外信息

简单来说，`net/url` 包就是 URL 的"拆快递"工具，把一个完整的 URL 字符串拆成各个零件，让你随心所欲地访问和修改。

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	// 这就是传说中的 URL，一个互联网地址的"全聚德"
	rawURL := "https://example.com:8080/path/to/file?key=value&name=张三"

	// 解析它！
	u, err := url.Parse(rawURL)
	if err != nil {
		fmt.Println("解析失败：", err)
		return
	}

	fmt.Println("协议（Scheme）：", u.Scheme)       // https
	fmt.Println("主机（Host）：", u.Host)           // example.com:8080
	fmt.Println("路径（Path）：", u.Path)           // /path/to/file
	fmt.Println("查询（RawQuery）：", u.RawQuery)   // key=value&name=%E5%BC%A0%E4%B8%89
}
```

---

## 23.2 net/url 核心原理：URL 结构，Scheme、User、Host、Path、RawQuery、Fragment

理解了 URL 能解决什么问题后，让我们深入看看 `url.URL` 这个结构体都包含哪些字段。这些字段就像 URL 的"基因图谱"，决定了 URL 的所有特征。

**专业词汇解释：**

- **Scheme**：协议部分，如 http、https、ftp
- **User**：用户名信息（可选，包含用户名和密码）
- **Host**：主机名和端口，如 example.com:8080
- **Path**：路径部分，如 /path/to/file
- **RawQuery**：原始查询字符串，如 key=value&name=xxx
- **Fragment**：锚点部分，如 URL 末尾的 #section

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	// 解析一个包含用户名、密码、端口、路径、查询和锚点的完整 URL
	rawURL := "https://admin:123456@example.com:8080/path/to/file?key=value#top"

	u, err := url.Parse(rawURL)
	if err != nil {
		fmt.Println("解析失败：", err)
		return
	}

	// 打印 URL 结构的所有字段
	fmt.Println("=== URL 结构大揭秘 ===")
	fmt.Println("完整字符串：", u.String())
	fmt.Println("协议 Scheme：", u.Scheme)           // https
	fmt.Println("用户信息 User：", u.User)           // admin:123456
	fmt.Println("主机 Host：", u.Host)             // example.com:8080
	fmt.Println("路径 Path：", u.Path)             // /path/to/file
	fmt.Println("查询 RawQuery：", u.RawQuery)     // key=value
	fmt.Println("锚点 Fragment：", u.Fragment)       // top

	// 如果 User 不为空，还可以单独获取用户名和密码
	if u.User != nil {
		fmt.Println("用户名：", u.User.Username())  // admin
		password, _ := u.User.Password()
		fmt.Println("密码：", password)            // 123456
	}
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                        URL 结构分解图                            │
├─────────────────────────────────────────────────────────────────┤
│  https://admin:123456@example.com:8080/path/to/file?key=value#top│
│  ┌─┘  └────┘└─────────────┘└─┘└────────────┘└──────┘└─────┘└────┤
│  Scheme   User             Host    Path      RawQuery   Fragment│
│  ────   ─────           ───────  ─────      ───────    ────────│
│  协议    用户:密码         主机:端口  路径       查询参数    锚点   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 23.3 url.Parse：解析 URL

`url.Parse` 是 `net/url` 包的入口函数，它把一个字符串 URL 解析成 `*url.URL` 结构体。这个过程就像拆快递，帮你把一个包裹里的东西一件件拿出来。

**专业词汇解释：**

- **Parse**：解析，把字符串转换成结构化数据的过程
- **Escape**：转义，把特殊字符转换成 URL 安全格式
- **Unescape**：反转义，把转义后的字符还原

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	// 基本解析
	u1, err := url.Parse("https://example.com/path")
	if err != nil {
		fmt.Println("错误：", err)
	} else {
		fmt.Printf("解析成功：%+v\n", u1)
	}

	// 解析相对路径（会自动转成绝对路径）
	u2, err := url.Parse("/path/to/resource")
	if err != nil {
		fmt.Println("错误：", err)
	} else {
		fmt.Printf("相对路径解析：%+v\n", u2)
	}

	// 解析带查询参数的 URL
	u3, err := url.Parse("https://search.com?q=golang&page=1")
	if err != nil {
		fmt.Println("错误：", err)
	} else {
		fmt.Printf("查询参数解析：%+v\n", u3)
		fmt.Println("查询参数：", u3.RawQuery)
	}

	// 解析非法 URL（会返回错误）
	_, err = url.Parse("://invalid")
	if err != nil {
		fmt.Println("非法 URL 错误（预期）：", err)
	}
}
```

---

## 23.4 URL.User：Userinfo，用户名和密码

在 URL 中，用户信息格式通常是 `username:password@`，比如 `ftp://admin:secret@ftp.example.com/`。`url.User` 类型专门用来处理这部分信息。

**专业词汇解释：**

- **Userinfo**：用户信息结构，包含用户名和可选密码
- **Username()**：获取用户名
- **Password()**：获取密码（返回密码和是否存在的布尔值）

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	// URL 中包含用户名和密码
	rawURL := "https://admin:password123@example.com:21/remote.php/dav/files/admin/"

	u, err := url.Parse(rawURL)
	if err != nil {
		fmt.Println("解析失败：", err)
		return
	}

	fmt.Println("=== WebDAV URL 解析 ===")
	fmt.Println("完整 URL：", rawURL)
	fmt.Println("协议：", u.Scheme)
	fmt.Println("主机：", u.Host)
	fmt.Println("路径：", u.Path)

	// 分析用户信息
	if u.User != nil {
		fmt.Println("\n=== 用户信息 ===")
		fmt.Println("用户名：", u.User.Username())

		// 获取密码（注意：密码可能不存在）
		if pwd, ok := u.User.Password(); ok {
			fmt.Println("密码：", pwd)
		} else {
			fmt.Println("密码：未设置")
		}
	} else {
		fmt.Println("用户信息：未设置")
	}

	// 创建一个带用户信息的 URL
	u2 := &url.URL{
		Scheme: "ssh",
		User:   url.UserPassword("git", "ghp_xxxxx"),
		Host:   "github.com",
		Path:   "/golang/go",
	}
	fmt.Println("\n构建的 URL：", u2.String())
}
```

---

## 23.5 URL.Host：主机和端口

`URL.Host` 字段包含主机名和端口号，格式是 `hostname:port`。有时候我们需要单独获取主机名或端口，这就需要用到 `Host` 和 `port` 的分离技巧。

**专业词汇解释：**

- **Host**：主机加端口，如 example.com:8080
- **Hostname()**：仅获取主机名（不含端口）
- **Port()**：仅获取端口号（不含主机名，如果没写端口则返回空字符串）

```go
package main

import (
	"fmt"
	"net"
	"net/url"
)

func main() {
	urls := []string{
		"https://example.com",
		"https://example.com:8080",
		"https://example.com:443",
		"http://localhost:3000",
		"ftp://files.example.com:21",
	}

	fmt.Println("=== Host 与 Port 解析 ===")
	for _, rawURL := range urls {
		u, err := url.Parse(rawURL)
		if err != nil {
			fmt.Printf("错误：%s - %v\n", rawURL, err)
			continue
		}

		hostname := u.Hostname()
		port := u.Port()

		// 如果端口为空但协议有默认端口，使用默认端口
		if port == "" {
			port = getDefaultPort(u.Scheme)
		}

		fmt.Printf("URL: %s\n", rawURL)
		fmt.Printf("  Host字段: %s\n", u.Host)
		fmt.Printf("  主机名: %s\n", hostname)
		fmt.Printf("  端口: %s\n", port)
		fmt.Println()
	}
}

// 根据协议返回默认端口
func getDefaultPort(scheme string) string {
	switch scheme {
	case "http":
		return "80"
	case "https":
		return "443"
	case "ftp":
		return "21"
	case "ssh":
		return "22"
	default:
		return "未知"
	}
}
```

---

## 23.6 URL.Path：路径

`URL.Path` 是 URL 中表示资源路径的部分，从域名的第一个 `/` 开始，到 `?` 或 `#` 之前结束。它就像文件系统的路径，描述了资源在服务器上的位置。

**专业词汇解释：**

- **Path**：URL 中的路径部分
- **Clean()**：返回规范化后的路径（去除多余的 /.. 等）
- **EscapedPath()**：返回转义后的路径

```go
package main

import (
	"fmt"
	"net/url"
	"path"
)

func main() {
	urls := []string{
		"https://example.com/a/b/c",
		"https://example.com/a/../b/./c",
		"https://example.com/a%2Fb%2Fc", // 编码后的路径
		"https://example.com/%E4%B8%AD%E6%96%87", // 中文路径
	}

	fmt.Println("=== Path 路径解析 ===")
	for _, rawURL := range urls {
		u, err := url.Parse(rawURL)
		if err != nil {
			fmt.Printf("错误：%s - %v\n", rawURL, err)
			continue
		}

		fmt.Printf("原始URL: %s\n", rawURL)
		fmt.Printf("  Path: %s\n", u.Path)
		fmt.Printf("  EscapedPath: %s\n", u.EscapedPath())

		// 使用 path 包进行路径操作
		fmt.Printf("  Base (最后一段): %s\n", path.Base(u.Path))
		fmt.Printf("  Dir (目录): %s\n", path.Dir(u.Path))
		fmt.Println()
	}

	// 构建路径
	u := &url.URL{
		Scheme: "https",
		Host:   "api.example.com",
		Path:   "/v1/users/123/profile",
	}
	fmt.Println("构建的URL：", u.String())
}
```

---

## 23.7 URL.RawQuery：原始查询字符串

`RawQuery` 是 URL 中 `?` 后面的原始查询字符串部分，如 `key=value&name=%E5%BC%A0%E4%B8%89`。它以键值对的形式存储数据，用 `&` 分隔。

**专业词汇解释：**

- **RawQuery**：未解析的原始查询字符串
- **Query()**：返回解析后的 map[string][]string
- **QueryEscape**：转义查询参数中的特殊字符

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	rawURL := "https://search.example.com?q=golang&page=1&lang=zh&tag=并发编程&tag=网络编程"

	u, err := url.Parse(rawURL)
	if err != nil {
		fmt.Println("解析失败：", err)
		return
	}

	fmt.Println("=== RawQuery 原始查询字符串 ===")
	fmt.Println("完整URL：", rawURL)
	fmt.Println()
	fmt.Println("RawQuery（原始）：", u.RawQuery)
	fmt.Println()

	// 使用 Query() 解析成 map
	queryMap := u.Query()
	fmt.Println("Query（解析后）：")
	for key, values := range queryMap {
		fmt.Printf("  %s: %v\n", key, values)
	}

	// 单独获取某个参数
	fmt.Println("\n=== 单独获取参数 ===")
	fmt.Println("q 的值：", queryMap.Get("q"))      // golang
	fmt.Println("page 的值：", queryMap.Get("page")) // 1
	fmt.Println("lang 的值：", queryMap.Get("lang")) // zh
	fmt.Println("tag 的值：", queryMap.Get("tag"))  // 并发编程（第一个）
	fmt.Println("不存在的参数：", queryMap.Get("none")) // 空字符串
}
```

---

## 23.8 ResolveReference：解析相对 URL

有时候我们需要把相对路径（如 `/path/to/file`）解析成绝对 URL。`ResolveReference` 就是做这个的，它像一个"路径合并器"，把相对 URL 和基础 URL 组合起来。

**专业词汇解释：**

- **ResolveReference**：解析相对引用，返回绝对 URL
- **相对 URL**：相对于某个基准的 URL，如 `./data.json`
- **绝对 URL**：完整的、可以直接访问的 URL

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	base, _ := url.Parse("https://example.com/a/b/c/index.html")

	// 各种相对路径
	references := []string{
		"../data.json",           // 上一级目录
		"./extra/info.html",      // 同级目录
		"/docs/guide.pdf",        // 根路径
		"https://other.com/f",    // 绝对URL（会覆盖基础URL）
		".././g.js",              // 混合类型
		"?query=123",             // 仅查询参数
		"#section",               // 仅锚点
	}

	fmt.Println("基础URL：", base.String())
	fmt.Println()

	for _, ref := range references {
		// 解析相对URL
		rel, _ := url.Parse(ref)
		abs := base.ResolveReference(rel)

		fmt.Printf("相对路径: %s\n", ref)
		fmt.Printf("  解析结果: %s\n", abs.String())
		fmt.Println()
	}
}
```

---

## 23.9 Values：Query 参数，Query.Get、Query["key"]

`url.Values` 是 `map[string][]string` 的别名，专门用来处理查询参数。它提供了方便的方法来获取、设置和操作查询参数，就像一个参数瑞士军刀。

**专业词汇解释：**

- **Values**：查询参数的值集合，类型是 map[string][]string
- **Query.Get(key)**：获取单个值（如果多个返回第一个）
- **Query[key]**：直接访问值切片

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	// 从 URL 解析查询参数
	rawURL := "https://api.example.com/search?q=golang&page=1&page=2&tag=web&tag=api"

	u, err := url.Parse(rawURL)
	if err != nil {
		fmt.Println("解析失败：", err)
		return
	}

	values := u.Query()

	fmt.Println("=== Values 查询参数操作 ===")
	fmt.Println("URL：", rawURL)
	fmt.Println()

	// 使用 Get 方法获取单个值
	fmt.Println("使用 Query.Get()：")
	fmt.Println("  q：", values.Get("q"))      // golang
	fmt.Println("  page：", values.Get("page")) // 1（返回第一个）
	fmt.Println("  tag：", values.Get("tag"))  // web（返回第一个）

	// 直接访问 map
	fmt.Println("\n直接访问 map：")
	fmt.Println("  q：", values["q"])      // [golang]
	fmt.Println("  page：", values["page"]) // [1 2]
	fmt.Println("  tag：", values["tag"]) // [web api]

	// 构建新的查询参数
	fmt.Println("\n=== 构建查询参数 ===")
	buildQuery()
}

func buildQuery() {
	// 手动构建 Values
	v := url.Values{}

	v.Set("name", "张三")
	v.Add("tag", "技术")
	v.Add("tag", "编程")
	v.Set("page", "1")

	fmt.Println("构建的 Values：")
	fmt.Printf("  name: %v\n", v.Get("name"))
	fmt.Printf("  tag: %v\n", v["tag"])
	fmt.Printf("  page: %v\n", v.Get("page"))

	// 编码成查询字符串
	queryString := v.Encode()
	fmt.Println("\n编码后的查询字符串：", queryString)
	// name=%E5%BC%A0%E4%B8%89&tag=%E6%8A%80%E6%9C%AF&tag=%E7%BC%96%E7%A8%8B&page=1
}
```

---

## 23.10 QueryEscape、PathEscape：URL 编码

URL 只能包含有限的字符，对于特殊字符（如中文、空格、符号）需要进行编码。Go 提供了两套编码函数：`QueryEscape` 用于查询参数，`PathEscape` 用于路径。

**专业词汇解释：**

- **QueryEscape**：对查询字符串进行编码
- **PathEscape**：对路径进行编码
- **QueryUnescape**：解码查询字符串
- **PathUnescape**：解码路径
- **Percent-encoding**：URL 编码格式，把字符转换成 %XX 形式

```go
package main

import (
	"fmt"
	"net/url"
)

func main() {
	text := "Hello 世界! @#$%"

	fmt.Println("=== URL 编码与解码 ===")
	fmt.Println("原始字符串：", text)
	fmt.Println()

	// 查询字符串编码（会将空格编码为 + 或 %20）
	queryEscaped := url.QueryEscape(text)
	fmt.Println("QueryEscape：", queryEscaped)

	// 路径编码（会将空格编码为 %20）
	pathEscaped := url.PathEscape(text)
	fmt.Println("PathEscape：", pathEscaped)

	fmt.Println()

	// 解码
	queryUnescaped, _ := url.QueryUnescape(queryEscaped)
	pathUnescaped, _ := url.PathUnescape(pathEscaped)

	fmt.Println("QueryUnescape：", queryUnescaped)
	fmt.Println("PathUnescape：", pathUnescaped)

	// 实际应用：构建带中文参数的 URL
	fmt.Println("\n=== 实际应用 ===")

	// 场景：搜索中文关键词
	keyword := "Go语言教程"
	encoded := url.QueryEscape(keyword)
	searchURL := "https://www.google.com/search?q=" + encoded
	fmt.Println("Google 搜索 URL：", searchURL)

	// 场景：访问中文路径的文件
	filename := "文档/2024年度报告.pdf"
	fileURL := "https://files.example.com/" + url.PathEscape(filename)
	fmt.Println("文件下载 URL：", fileURL)
}
```

---

## 23.11 net/html 包：HTML 解析

`net/html` 包是 Go 标准库中的 HTML 解析器，它能把 HTML 字符串解析成一棵 DOM 树。DOM 树就像一棵倒过来的树，每个节点都是一个 HTML 元素。

**专业词汇解释：**

- **HTML（HyperText Markup Language）**：超文本标记语言，网页的结构骨架
- **DOM（Document Object Model）**：文档对象模型，HTML 的树形结构表示
- **Tokenization**：分词，把 HTML 文本分解成一个个标记
- **Parse Tree**：解析树，即 DOM 树

```go
package main

import (
	"fmt"
	"net/html"
	"strings"
)

func main() {
	htmlContent := `
	<!DOCTYPE html>
	<html>
	<head>
		<title>Go语言教程</title>
	</head>
	<body>
		<h1>欢迎学习Go</h1>
		<p>Go是一门简洁、高效的编程语言</p>
		<div class="container">
			<a href="https://golang.org">Go官网</a>
		</div>
	</body>
	</html>
	`

	fmt.Println("=== HTML 解析示例 ===")
	fmt.Println("解析 HTML 内容...")

	// 解析 HTML
	reader := strings.NewReader(htmlContent)
	doc, err := html.Parse(reader)
	if err != nil {
		fmt.Println("解析错误：", err)
		return
	}

	fmt.Println("解析成功！")
	fmt.Printf("根节点：%s\n", doc.Data)

	// 遍历打印结构
	fmt.Println("\n=== DOM 树结构 ===")
	printTree(doc, 0)
}

func printTree(n *html.Node, depth int) {
	// 缩进
	indent := strings.Repeat("  ", depth)

	if n.Type == html.ElementNode {
		fmt.Printf("%s<%s>\n", indent, n.Data)
	} else if n.Type == html.TextNode {
		text := strings.TrimSpace(n.Data)
		if text != "" {
			fmt.Printf("%sTEXT: %s\n", indent, text)
		}
	} else if n.Type == html.CommentNode {
		fmt.Printf("%s<!-- 注释 -->\n", indent)
	}

	// 递归遍历子节点
	for child := n.FirstChild; child != nil; child = child.NextSibling {
		printTree(child, depth+1)
	}
}
```

---

## 23.12 html.Parse：解析 HTML 为节点树

`html.Parse` 函数是 `net/html` 包的入口点，它接收一个 `io.Reader`，返回一个 `*html.Node`，这就是 DOM 树的根节点。

**专业词汇解释：**

- **html.Parse**：HTML 解析函数，返回 DOM 树根节点
- **io.Reader**：Go 的字节流接口
- **Node**：DOM 树中的节点

```go
package main

import (
	"fmt"
	"net/html"
	"strings"
)

func main() {
	// HTML 文档
	doc := `
	<!DOCTYPE html>
	<html lang="zh-CN">
	<head>
		<meta charset="UTF-8">
		<title>页面标题</title>
		<link rel="stylesheet" href="style.css">
	</head>
	<body>
		<div id="app">
			<h2 class="title">内容区域</h2>
			<p>第一段文字</p>
			<p>第二段文字</p>
		</div>
		<script src="app.js"></script>
	</body>
	</html>
	`

	fmt.Println("=== HTML 解析为节点树 ===")

	// 解析 HTML
	root, err := html.Parse(strings.NewReader(doc))
	if err != nil {
		fmt.Println("解析失败：", err)
		return
	}

	// 打印完整树（手动遍历节点）
	fmt.Println("\n完整 DOM 树：")
	var printNode func(*html.Node, int)
	printNode = func(n *html.Node, depth int) {
		indent := strings.Repeat("  ", depth)
		if n.Type == html.ElementNode {
			fmt.Printf("%s<%s>\n", indent, n.Data)
		} else if n.Type == html.TextNode {
			text := strings.TrimSpace(n.Data)
			if text != "" {
				fmt.Printf("%s  Text: %q\n", indent, text)
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			printNode(c, depth+1)
		}
		if n.Type == html.ElementNode {
			fmt.Printf("%s</%s>\n", indent, n.Data)
		}
	}
	printNode(root, 0)
}
```

---

## 23.13 html.Node 类型：Element、Text、Comment、Document、Doctype

`html.Node` 是一个非常重要的结构体，它有多种类型，代表 DOM 树中的不同节点。理解节点类型是解析 HTML 的基础。

**专业词汇解释：**

- **NodeType**：节点类型，用常量表示
- **ElementNode**：元素节点，如 `<div>`、`<p>`
- **TextNode**：文本节点，包含纯文本
- **CommentNode**：注释节点，如 `<!-- comment -->`
- **DocumentNode**：文档节点，整个文档的根
- **DoctypeNode**：文档类型声明，如 `<!DOCTYPE html>`

```go
package main

import (
	"fmt"
	"net/html"
	"strings"
)

func main() {
	htmlContent := `<!-- 这是一个注释 -->
	<!DOCTYPE html>
	<html>
	<head><title>Test</title></head>
	<body>
		<div>这是文本节点</div>
		<!-- 另一个注释 -->
	</body>
	</html>`

	fmt.Println("=== Node 类型解析 ===")

	root, _ := html.Parse(strings.NewReader(htmlContent))

	// 遍历所有节点并打印类型
	fmt.Println("\n节点类型分析：")
	walkNodes(root, func(n *html.Node) {
		typeName := nodeTypeName(n.Type)
		if n.Data != "" {
			fmt.Printf("  类型: %-15s 数据: %q\n", typeName, truncate(n.Data, 30))
		} else {
			fmt.Printf("  类型: %-15s\n", typeName)
		}
	})
}

func nodeTypeName(t html.NodeType) string {
	switch t {
	case html.ErrorNode:
		return "ErrorNode"
	case html.DocumentNode:
		return "DocumentNode"
	case html.ElementNode:
		return "ElementNode"
	case html.TextNode:
		return "TextNode"
	case html.CommentNode:
		return "CommentNode"
	case html.DoctypeNode:
		return "DoctypeNode"
	default:
		return "Unknown"
	}
}

func truncate(s string, maxLen int) string {
	if len(s) > maxLen {
		return s[:maxLen] + "..."
	}
	return s
}

func walkNodes(n *html.Node, fn func(*html.Node)) {
	fn(n)
	for child := n.FirstChild; child != nil; child = child.NextSibling {
		walkNodes(child, fn)
	}
}
```

---

## 23.14 Node.Attr：节点属性

HTML 元素可以有属性，如 `<a href="url" class="link">` 中的 `href` 和 `class`。`Node.Attr` 是一个切片，包含了元素的所有属性。

**专业词汇解释：**

- **Attr**：属性结构体，包含 Key 和 Val
- **Key**：属性名，如 href、class、id
- **Val**：属性值，如 https://example.com、button

```go
package main

import (
	"fmt"
	"net/html"
	"strings"
)

func main() {
	htmlContent := `
	<div class="container" id="main">
		<a href="https://golang.org" class="link" target="_blank">Go语言</a>
		<img src="go-logo.png" alt="Go Logo" width="100" height="100">
		<input type="text" name="username" placeholder="请输入用户名" disabled>
	</div>
	`

	fmt.Println("=== 节点属性解析 ===")

	root, _ := html.Parse(strings.NewReader(htmlContent))

	// 查找所有带属性的元素
	fmt.Println("\n查找带属性的元素：")
	findElementsWithAttrs(root, nil)
}

func findElementsWithAttrs(n *html.Node, targetTags []string) {
	if n.Type == html.ElementNode {
		hasAttrs := len(n.Attr) > 0
		if hasAttrs {
			fmt.Printf("\n<%s> 属性列表：\n", n.Data)
			for _, attr := range n.Attr {
				fmt.Printf("  [%s] = %q\n", attr.Key, attr.Val)
			}

			// 查找特定属性
			if href := getAttr(n, "href"); href != "" {
				fmt.Printf("  → 链接地址: %s\n", href)
			}
			if src := getAttr(n, "src"); src != "" {
				fmt.Printf("  → 图片地址: %s\n", src)
			}
			if class := getAttr(n, "class"); class != "" {
				fmt.Printf("  → CSS类名: %s\n", class)
			}
		}
	}

	for child := n.FirstChild; child != nil; child = child.NextSibling {
		findElementsWithAttrs(child, targetTags)
	}
}

// 获取特定属性值
func getAttr(n *html.Node, key string) string {
	for _, attr := range n.Attr {
		if attr.Key == key {
			return attr.Val
		}
	}
	return ""
}
```

---

## 23.15 Node.FirstChild、Node.NextSibling：DOM 树遍历

DOM 树是树形结构，要遍历它我们需要知道节点之间的关系。`FirstChild` 指向第一个子节点，`NextSibling` 指向下一个兄弟节点。

**专业词汇解释：**

- **FirstChild**：第一个子节点
- **NextSibling**：下一个兄弟节点
- **Parent**：父节点
- **LastChild**：最后一个子节点
- **PrevSibling**：上一个兄弟节点

```
┌─────────────────────────────────────────────────────────────────┐
│                        DOM 树结构示例                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                      ┌──────────┐                              │
│                      │   html    │  ← 根节点                     │
│                      └─────┬────┘                              │
│              ┌──────────────┼──────────────┐                    │
│              ↓              ↓              ↓                    │
│        ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│        │  head    │  │   body   │  │          │               │
│        └─────┬────┘  └─────┬────┘  └──────────┘               │
│              ↓             ↓                                   │
│        ┌──────────┐  ┌──────────┐                             │
│        │  title   │  │    h1    │  ← FirstChild                │
│        └──────────┘  └─────┬────┘                              │
│                            ↓                                    │
│                      ┌──────────┐                              │
│                      │  "Hello" │  ← TextNode                  │
│                      └──────────┘                              │
│                                                                 │
│  h1.NextSibling → p (段落)                                     │
│  p.NextSibling → div                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```go
package main

import (
	"fmt"
	"net/html"
	"strings"
)

func main() {
	htmlContent := `
	<html>
	<body>
		<h1>标题</h1>
		<p>第一个段落</p>
		<p>第二个段落</p>
		<div class="container">
			<span>嵌套元素</span>
		</div>
	</body>
	</html>
	`

	fmt.Println("=== DOM 树遍历 ===")

	root, _ := html.Parse(strings.NewReader(htmlContent))

	// 找到 body 节点
	body := findTag(root, "body")
	if body != nil {
		fmt.Println("找到 <body> 节点")
		fmt.Println("\n遍历 body 的直接子节点：")

		childNum := 0
		for child := body.FirstChild; child != nil; child = child.NextSibling {
			childNum++
			if child.Type == html.ElementNode {
				fmt.Printf("  子节点 %d: <%s>\n", childNum, child.Data)

				// 如果有子节点，打印其子节点
				if child.FirstChild != nil {
					for grandChild := child.FirstChild; grandChild != nil; grandChild = grandChild.NextSibling {
						if grandChild.Type == html.ElementNode {
							fmt.Printf("      孙节点: <%s>\n", grandChild.Data)
						} else if grandChild.Type == html.TextNode {
							text := strings.TrimSpace(grandChild.Data)
							if text != "" {
								fmt.Printf("      文本: %q\n", truncate(text, 20))
							}
						}
					}
				}
			}
		}
	}
}

// 查找指定标签的第一个节点
func findTag(n *html.Node, tag string) *html.Node {
	if n.Type == html.ElementNode && n.Data == tag {
		return n
	}
	for child := n.FirstChild; child != nil; child = child.NextSibling {
		if found := findTag(child, tag); found != nil {
			return found
		}
	}
	return nil
}

func truncate(s string, maxLen int) string {
	if len(s) > maxLen {
		return s[:maxLen] + "..."
	}
	return s
}
```

---

## 23.16 html/template 包解决什么问题：生成安全的 HTML，自动转义所有输出，防止 XSS

`html/template` 包是 Go 的 HTML 模板引擎，它最大的特点是**安全**。它会自动转义所有输出，防止 XSS（跨站脚本攻击）——这是 web 开发中最常见也最危险的安全漏洞之一。

**专业词汇解释：**

- **XSS（Cross-Site Scripting）**：跨站脚本攻击，黑客通过注入恶意脚本来攻击网站
- **HTML 转义**：把特殊字符（如 `<`、`>`、`&`）转换成安全的形式（如 `&lt;`、`&gt;`、`&amp;`）
- **模板引擎**：用数据填充模板生成最终文本的工具
- **Context-Aware Escaping**：上下文感知转义，根据输出位置自动选择转义方式

```go
package main

import (
	"fmt"
	"html/template"
	"strings"
)

func main() {
	fmt.Println("=== html/template 安全特性 ===")
	fmt.Println()

	// 模拟用户输入（可能包含恶意脚本）
	userInput := `<script>alert('黑客来了！')</script>`

	// 错误的方式：直接拼接 HTML（危险！）
	unsafeHTML := "<div>" + userInput + "</div>"
	fmt.Println("危险做法（直接拼接）：")
	fmt.Println("  输出：", unsafeHTML)
	fmt.Println()

	// 正确的方式：使用 template 包
	tmpl := template.Must(template.New("safe").Parse(
		`<div>{{.UserInput}}</div>`,
	))

	fmt.Println("安全做法（使用 template）：")
	if err := tmpl.Execute( map[string]string{
		"UserInput": userInput,
	}); err != nil {
		fmt.Println("错误：", err)
	}

	fmt.Println()

	// 演示上下文感知转义
	fmt.Println("=== 上下文感知转义 ===")
	showContextAwareEscaping()
}

// 演示不同上下文的转义方式
func showContextAwareEscaping() {
	data := map[string]string{
		"html":  `<div>"Hello"&'World'</div>`,
		"attr":  `onclick="alert('xss')"`,
		"url":   `?name=<script>alert(1)</script>`,
		"js":    `"; alert('hacked'); "`,
		"plain": `Hello <World> & "Friends"`,
	}

	tmpl := template.Must(template.New("context").Parse(`转义示例：
HTML上下文: {{.html}}
属性上下文: {{.attr}}
URL上下文: {{.url}}
纯文本: {{.plain}}
`))

	tmpl.Execute( data)
}
```

---

## 23.17 html/template 核心原理：{{.Field}}、{{if}}、{{range}}、{{with}}、{{template}}

`html/template` 的模板语法使用双花括号 `{{ }}` 包裹。常用的动作包括变量输出、条件判断、循环遍历、作用域切换和模板包含。

**专业词汇解释：**

- **{{.Field}}**：点操作，输出字段值
- **{{if}} / {{else}}**：条件判断
- **{{range}}**：循环遍历
- **{{with}}**：作用域切换
- **{{template}}**：模板包含

```go
package main

import (
	"fmt"
	"html/template"
	"strings"
)

func main() {
	// 准备数据
	data := struct {
		Title    string
		Users    []string
		IsActive bool
		Content  template.HTML
	}{
		Title:    "Go 模板教程",
		Users:    []string{"张三", "李四", "王五"},
		IsActive: true,
		Content:  template.HTML("<strong>安全的 HTML 内容</strong>"),
	}

	// 组合模板
	tmplStr := `
{{define "header"}}<h1>{{.Title}}</h1>{{end}}

{{template "header" .}}

{{if .IsActive}}
<p>状态：活跃用户</p>
{{else}}
<p>状态：非活跃</p>
{{end}}

<ul>
{{range .Users}}
<li>{{.}}</li>
{{end}}
</ul>

<div>{{.Content}}</div>
`

	tmpl := template.Must(template.New("demo").Parse(tmplStr))

	fmt.Println("=== 模板语法演示 ===")
	if err := tmpl.Execute( data); err != nil {
		fmt.Println("错误：", err)
	}
}
```

---

## 23.18 template.New、template.Parse、template.Execute：创建和执行模板

这是模板处理的三部曲：`New` 创建模板，`Parse` 解析模板字符串（或文件），`Execute` 执行模板输出结果。

**专业词汇解释：**

- **template.New**：创建一个新模板
- **template.Parse**：解析模板内容
- **template.Execute**：执行模板，输出到 io.Writer
- **template.Must**：如果解析出错则 panic，常用于初始化

```go
package main

import (
	"fmt"
	"html/template"
	"strings"
)

func main() {
	fmt.Println("=== 模板创建与执行 ===")
	fmt.Println()

	// 方法1：一步到位（最常用）
	fmt.Println("1. 一步创建和解析：")
	tmpl1 := template.Must(template.New("simple").Parse(
		`<p>Hello, {{.Name}}!</p>`,
	))
	tmpl1.Execute( map[string]string{"Name": "World"})

	// 方法2：分步进行
	fmt.Println("\n2. 分步创建和解析：")
	tmpl2 := template.New("step")
	tmpl2, err := tmpl2.Parse(`<p>今天是 {{.Date}}</p>`)
	if err != nil {
		fmt.Println("解析错误：", err)
		return
	}
	tmpl2.Execute( map[string]string{"Date": "2024-01-15"})

	// 方法3：从文件解析（实际应用中常用）
	fmt.Println("\n3. 从字符串模拟文件解析：")
	tmpl3 := template.Must(template.New("fromString").Parse(
		`<!DOCTYPE html>
<html>
<head><title>{{.Title}}</title></head>
<body>
	<h1>{{.Heading}}</h1>
	<p>{{.Body}}</p>
</body>
</html>`,
	))

	var output strings.Builder
	tmpl3.Execute(&output, map[string]string{
		"Title":    "动态页面",
		"Heading":  "欢迎光临",
		"Body":     "这是通过模板生成的内容",
	})

	fmt.Println("生成的 HTML：")
	fmt.Println(output.String())
}
```

---

## 23.19 {{if}}、{{else}}：条件判断

`{{if}}` 和 `{{else}}` 动作用于条件判断，根据数据的值决定输出什么内容。

**专业词汇解释：**

- **{{if}}**：条件开始
- **{{else}}**：备选分支
- **{{else if}}**：多层条件

```go
package main

import (
	"fmt"
	"html/template"
)

func main() {
	type User struct {
		Name   string
		Age    int
		Active bool
		Role   string
	}

	users := []User{
		{Name: "张三", Age: 25, Active: true, Role: "admin"},
		{Name: "李四", Age: 30, Active: false, Role: "user"},
		{Name: "王五", Age: 35, Active: true, Role: "moderator"},
	}

	tmpl := template.Must(template.New("condition").Parse(`
用户状态报告：
{{range .}}
姓名: {{.Name}}, 年龄: {{.Age}}
{{if .Active}}
  状态: ✅ 在线
  角色: {{.Role}}
{{else}}
  状态: ❌ 离线
{{end}}
---
{{end}}
`))

	fmt.Println("=== 条件判断演示 ===")
	tmpl.Execute( users)
}
```

---

## 23.20 {{range}}：循环遍历 slice、map、channel

`{{range}}` 动作用于遍历 slice、map 或 channel，就像 Go 代码中的 `for range` 循环。

**专业词汇解释：**

- **{{range}}**：循环开始
- **{{.}}**：在 range 内指向当前元素
- **{{$key}}**：索引或键
- **{{$value}}**：当前元素的值（可选）

```go
package main

import (
	"fmt"
	"html/template"
)

func main() {
	// 数据准备
	type Product struct {
		Name  string
		Price float64
	}

	data := struct {
		SliceDemo []int
		MapDemo   map[string]string
		StructDemo []Product
	}{
		SliceDemo: []int{10, 20, 30, 40, 50},
		MapDemo: map[string]string{
			"go":     "Go语言",
			"python": "Python语言",
			"rust":   "Rust语言",
		},
		StructDemo: []Product{
			{Name: "iPhone", Price: 8999},
			{Name: "iPad", Price: 4999},
			{Name: "MacBook", Price: 12999},
		},
	}

	tmpl := template.Must(template.New("range").Parse(`
=== 遍历 Slice ===
索引: 值
{{range $index, $value := .SliceDemo}}
  {{$index}}: {{$value}}
{{end}}

=== 遍历 Map ===
键: 值
{{range $key, $value := .MapDemo}}
  {{$key}} → {{$value}}
{{end}}

=== 遍历结构体切片 ===
商品列表：
{{range .StructDemo}}
  - {{.Name}} ¥{{.Price}}
{{end}}
`))

	fmt.Println("=== {{range}} 循环遍历 ===")
	tmpl.Execute( data)
}
```

---

## 23.21 {{with}}：作用域切换

`{{with}}` 动作用于切换当前作用域（点 `.`），当数据较深时特别有用，可以避免写一长串的点号。

**专业词汇解释：**

- **{{with}}**：切换到指定对象的作用域
- **{{.}}**：在 with 块内指向 with 的参数

```go
package main

import (
	"fmt"
	"html/template"
)

func main() {
	type Address struct {
		City    string
		Street  string
		ZipCode string
	}

	type Person struct {
		Name    string
		Age     int
		Address Address
	}

	person := Person{
		Name: "张三",
		Age:  30,
		Address: Address{
			City:    "北京",
			Street:  "中关村大街1号",
			ZipCode: "100000",
		},
	}

	// 不用 with - 需要写很多点
	tmpl1 := template.Must(template.New("without_with").Parse(`
=== 不用 with ===
姓名: {{.Name}}
年龄: {{.Age}}
城市: {{.Address.City}}
街道: {{.Address.Street}}
邮编: {{.Address.ZipCode}}
`))

	// 用 with - 更简洁
	tmpl2 := template.Must(template.New("with_with").Parse(`
=== 使用 with ===
姓名: {{.Name}}
{{with .Address}}
城市: {{.City}}
街道: {{.Street}}
邮编: {{.ZipCode}}
{{end}}
（离开 with 块后，{{.}} 恢复为原来的 Person）
`))

	fmt.Println("=== {{with}} 作用域切换 ===")
	tmpl1.Execute( person)
	fmt.Println()
	tmpl2.Execute( person)
}
```

---

## 23.22 {{template}}、{{block}}：模板包含和定义可覆盖的块

`{{template}}` 用于包含其他模板，`{{block}}` 则是在定义模板的同时提供默认实现，便于覆盖。

**专业词汇解释：**

- **{{template}}**：包含并执行另一个模板
- **{{define}}**：定义一个命名模板
- **{{block}}**：定义一个可覆盖的块

```go
package main

import (
	"fmt"
	"html/template"
	"strings"
)

func main() {
	// 定义一个包含布局的模板
	tmpl := template.Must(template.New("layout").Parse(`
{{define "base"}}
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>{{template "title" .}}</title>
</head>
<body>
	<header>{{template "header" .}}</header>
	<main>{{template "content" .}}</main>
	<footer>{{template "footer" .}}</footer>
</body>
</html>
{{end}}

{{define "title"}}默认标题{{end}}
{{define "header"}}<h2>默认头部</h2>{{end}}
{{define "footer"}}<p>版权所有 2024</p>{{end}}

{{define "content"}}<p>默认内容</p>{{end}}
`))

	// 使用 block 定义可覆盖的内容
	tmpl = template.Must(tmpl.Parse(`
{{block "title" .}}我的网站{{end}}
{{block "header" .}}<nav>导航栏</nav>{{end}}
{{block "content" .}}<article>文章内容</article>{{end}}
`))

	var output strings.Builder
	tmpl.ExecuteTemplate(&output, "base", map[string]string{"SiteName": "Go教程"})

	fmt.Println("=== 模板包含与覆盖 ===")
	fmt.Println(output.String())
}
```

---

## 23.23 FuncMap：自定义函数

`FuncMap` 允许你注册自定义函数，在模板中使用。这对于格式化、转换等操作非常有用。

**专业词汇解释：**

- **FuncMap**：函数映射，类型是 map[string]interface{}
- **FuncMap["name"]**：在模板中调用的函数名
- **template.FuncMap**：FuncMap 的别名

```go
package main

import (
	"fmt"
	"html/template"
	"strings"
	"time"
)

func main() {
	// 创建 FuncMap，注册自定义函数
	funcMap := template.FuncMap{
		// 字符串处理函数
		"upper": strings.ToUpper,
		"lower": strings.ToLower,
		"title": strings.Title,
		"trim":  strings.TrimSpace,

		// 格式化函数
		"formatDate": func(t time.Time) string {
			return t.Format("2006-01-02 15:04:05")
		},
		"formatPrice": func(price float64) string {
			return fmt.Sprintf("¥%.2f", price)
		},

		// 自定义逻辑
		"contains": strings.Contains,
		"replace":  strings.ReplaceAll,
	}

	// 创建带函数的模板
	tmpl := template.Must(template.New("funcs").Funcs(funcMap).Parse(`
=== 自定义函数演示 ===

字符串处理：
  原文本: {{.Text}}
  大写: {{upper .Text}}
  小写: {{lower .Text}}
  首字母大写: {{title .Text}}
  去空格: "{{trim .Text}}"

格式化：
  日期: {{formatDate .Now}}
  价格: {{formatPrice .Price}}

逻辑判断：
  包含 "Go": {{contains .Text "Go"}}
  替换: {{replace .Text "World" "Gopher"}}
`))

	type Data struct {
		Text  string
		Now   time.Time
		Price float64
	}

	d := Data{
		Text:  "hello world from golang",
		Now:   time.Now(),
		Price: 99.8,
	}

	fmt.Println("=== FuncMap 自定义函数 ===")
	tmpl.Execute( d)
}
```

---

## 23.24 自动 XSS 防护：html/template 会对所有输出做 HTML 转义

这是 `html/template` 最重要的特性！它会自动转义所有 `{{}}` 中的输出，防止 XSS 攻击。只需要把数据传给模板，不用担心注入问题。

**专业词汇解释：**

- **XSS（Cross-Site Scripting）**：跨站脚本攻击
- **HTML 转义**：把 `<` 变成 `&lt;`，`>` 变成 `&gt;` 等
- **Context-Aware**：上下文感知，不同位置转义不同

```go
package main

import (
	"fmt"
	"html/template"
)

func main() {
	// 模拟各种 XSS 攻击向量
	attackVectors := []struct {
		Name  string
		Value string
	}{
		{"脚本注入", `<script>alert('XSS')</script>`},
		{"事件处理器", `<img onerror="alert('hacked')" src="x">`},
		{"JavaScript 伪协议", `<a href="javascript:alert('XSS')">点击</a>`},
		{"引号注入", `"'><script>alert('XSS')</script>`},
		{"Unicode 编码", `\u003cscript\u003ealert('XSS')\u003c/script\u003e`},
	}

	tmpl := template.Must(template.New("xss_demo").Parse(`
=== XSS 防护演示 ===

原始攻击代码（故意不转义会导致问题）：
{{.Attack}}
---
{{.Description}}

使用 template 自动转义后：
{{.Value}}
`))

	for _, av := range attackVectors {
		fmt.Printf("\n--- 测试：%s ---\n", av.Name)
		tmpl.Execute( map[string]string{
			"Description": av.Name,
			"Attack":      "直接输出（危险）：" + av.Value,
			"Value":       av.Value,
		})
	}

	fmt.Println(`
=== 转义原理 ===
<  → &lt;
>  → &gt;
"  → &quot;
'  → &#39;
&  → &amp;
`)
}
```

---

## 23.25 html.EscapeString：转义 HTML 特殊字符

有时候你只需要转义单个字符串，不需要完整的模板引擎。`html.EscapeString` 就是为此设计的，它专门转义 HTML 特殊字符。

**专业词汇解释：**

- **html.EscapeString**：转义 HTML 特殊字符
- **html.UnescapeString**：反转义
- **template.HTML**：标记为信任的 HTML，不转义

```go
package main

import (
	"fmt"
	"html"
	"strings"
)

func main() {
	userInputs := []string{
		`<script>alert('XSS')</script>`,
		`Hello <World> & "Friends"`,
		`<a href="?q=Go&lang=zh">链接</a>`,
		`&& <script>document.cookie</script>`,
	}

	fmt.Println("=== html.EscapeString 转义 ===")
	fmt.Println()

	for _, input := range userInputs {
		escaped := html.EscapeString(input)
		unescaped, _ := html.UnescapeString(escaped)

		fmt.Printf("原始:     %q\n", input)
		fmt.Printf("转义后:   %q\n", escaped)
		fmt.Printf("反转义:   %q\n", unescaped)
		fmt.Println()
	}

	// 何时使用 html.EscapeString vs template.HTML
	fmt.Println("=== 使用场景 ===")
	fmt.Println("html.EscapeString: 需要手动转义时")
	fmt.Println("template.HTML: 确认安全，不需要转义时")
	fmt.Println("template.HTML 注释: \"在Go代码中明确表示信任的HTML内容\"")

	// 演示两种方式的区别
	demoBothApproaches()
}

func demoBothApproaches() {
	userContent := `<strong>用户提交的安全内容</strong>`

	// 方式1：转义后输出（安全）
	fmt.Println("\n方式1 - 转义输出：")
	fmt.Println(html.EscapeString(userContent))
	// 输出: &lt;strong&gt;用户提交的安全内容&lt;/strong&gt;

	// 方式2：使用 template.HTML（信任内容）
	fmt.Println("\n方式2 - 信任的 HTML：")
	fmt.Println(userContent)
	// 输出: <strong>用户提交的安全内容</strong>

	// 警告：永远不要对用户输入使用 template.HTML
	untrustedContent := `<script>alert('hack')</script>`
	fmt.Println("\n⚠️ 危险：不要对用户输入使用 template.HTML")
	fmt.Println("用户输入转义后：", html.EscapeString(untrustedContent))
}
```

---

## 23.26 net/rpc：RPC 远程过程调用

RPC（Remote Procedure Call）是分布式系统中的"魔法"，它让你像调用本地函数一样调用远程服务器上的函数。Go 的 `net/rpc` 包提供了简洁而强大的 RPC 实现。

**专业词汇解释：**

- **RPC（Remote Procedure Call）**：远程过程调用
- **Gob**：Go 特有的序列化格式（类似 JSON，但只有 Go 能用）
- **服务名**：RPC 服务的标识名称
- **方法名**：可远程调用的方法

```
┌─────────────────────────────────────────────────────────────────┐
│                     RPC 调用原理                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   客户端                                            服务端        │
│  ┌─────────┐                                     ┌─────────┐    │
│  │ 调用    │  ──── 网络请求 ────>                │ 收到    │    │
│  │ Add(1,2│                                     │ 请求    │    │
│  └─────────┘                                     └────┬────┘    │
│     ↑                                           ↓          │
│     │                                           调用本地     │
│     │                                           Add(1,2)     │
│     │                                           ↓          │
│  ┌─────────┐                                     ┌─────────┐    │
│  │ 返回    │  <─── 网络响应 ────                 │ 返回    │    │
│  │ 结果: 3 │                                     │ 结果: 3 │    │
│  └─────────┘                                     └─────────┘    │
│                                                                 │
│  客户端以为在调用本地函数，实际上是远程调用！                       │
└─────────────────────────────────────────────────────────────────┘
```

```go
package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc"
)

// 算术服务
type Calculator struct{}

func (c *Calculator) Add(args [2]int, reply *int) error {
	*reply = args[0] + args[1]
	return nil
}

func (c *Calculator) Multiply(args [2]int, reply *int) error {
	*reply = args[0] * args[1]
	return nil
}

func main() {
	// 注册 RPC 服务
	rpc.Register(&Calculator{})

	// 监听端口
	l, err := net.Listen("tcp", ":1234")
	if err != nil {
		log.Fatal("监听失败：", err)
	}

	fmt.Println("RPC 服务已启动，监听 :1234")
	fmt.Println("等待客户端连接...")

	// 接受连接
	for {
		conn, err := l.Accept()
		if err != nil {
			continue
		}
		// 处理 RPC 请求（这里简化处理）
		go rpc.ServeConn(conn)
	}
}
```

---

## 23.27 rpc.Register：注册 RPC 服务

`rpc.Register` 用于把一个对象的方法注册为 RPC 服务。注册后，这些方法就可以被远程客户端调用。

**专业词汇解释：**

- **rpc.Register**：注册服务
- **暴露方法**：方法签名必须符合规定格式
- **方法签名**：`func (t *T) MethodName(args *T1, reply *T2) error`

```go
package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc"
)

// 定义服务接口和数据结构
type Args struct {
	A, B int
}

type Quotient struct {
	Quo, Rem int
}

// 算术服务
type Arith int

// Add 方法：两数相加
func (t *Arith) Add(args *Args, reply *int) error {
	*reply = args.A + args.B
	return nil
}

// Multiply 方法：两数相乘
func (t *Arith) Multiply(args *Args, reply *int) error {
	*reply = args.A * args.B
	return nil
}

// Divide 方法：两数相除
func (t *Arith) Divide(args *Args, reply *Quotient) error {
	if args.B == 0 {
		return fmt.Errorf("除数不能为零")
	}
	reply.Quo = args.A / args.B
	reply.Rem = args.A % args.B
	return nil
}

func main() {
	// 创建服务实例
	arith := new(Arith)

	// 注册服务（服务名默认为 "Arith"）
	rpc.Register(arith)

	fmt.Println("=== rpc.Register 注册 RPC 服务 ===")
	fmt.Println("服务已注册，可远程调用的方法：")
	fmt.Println("  Arith.Add")
	fmt.Println("  Arith.Multiply")
	fmt.Println("  Arith.Divide")

	// 启动监听
	l, e := net.Listen("tcp", ":1234")
	if e != nil {
		log.Fatal("监听失败：", e)
	}

	fmt.Println("\n服务监听中：tcp://:1234")
	fmt.Println("（使用 HTTP 处理器时调用 rpc.HandleHTTP()）")

	// 持续监听
	for {
		conn, err := l.Accept()
		if err != nil {
			continue
		}
		go rpc.ServeConn(conn)
	}
}
```

---

## 23.28 rpc.HandleHTTP：注册 HTTP 处理器

`rpc.HandleHTTP` 把 RPC 服务注册为 HTTP 处理器，这样可以通过 HTTP 协议来传输 RPC 请求。配合 `net/http` 使用更灵活。

**专业词汇解释：**

- **rpc.HandleHTTP**：注册 HTTP 处理器
- **RPC over HTTP**：通过 HTTP 协议传输 RPC 请求
- **DefaultServer**：默认的 RPC 服务器

```go
package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"net/rpc"
)

// 问候服务
type Greeting int

func (g *Greeting) SayHello(name string, reply *string) error {
	*reply = fmt.Sprintf("你好，%s！欢迎学习 Go 语言！", name)
	return nil
}

func (g *Greeting) GetTime(unused struct{}, reply *string) error {
	*reply = "2024-01-15 10:30:00"
	return nil
}

func main() {
	// 注册服务
	greeting := new(Greeting)
	rpc.Register(greeting)

	// 注册 HTTP 处理器
	rpc.HandleHTTP()

	fmt.Println("=== rpc.HandleHTTP 注册 HTTP 处理器 ===")
	fmt.Println("RPC 服务已注册到 HTTP 处理器")

	// 启动 HTTP 服务器
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "RPC Server is running!")
	})

	fmt.Println("HTTP 服务监听：http://localhost:8080")
	fmt.Println("RPC 端点：http://localhost:8080/rpc")

	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

---

## 23.29 rpc.Client、rpc.Dial：客户端连接

要调用远程 RPC 服务，首先需要建立连接。`rpc.Dial` 函数用于拨号连接远程 RPC 服务，返回一个 `*rpc.Client`。

**专业词汇解释：**

- **rpc.Dial**：建立 RPC 连接
- **rpc.Client**：RPC 客户端
- **Close()**：关闭连接

```go
package main

import (
	"fmt"
	"log"
	"net/rpc"
)

func main() {
	// 连接到 RPC 服务器
	client, err := rpc.Dial("tcp", "localhost:1234")
	if err != nil {
		log.Fatal("连接失败：", err)
	}
	defer client.Close()

	fmt.Println("=== rpc.Dial 客户端连接 ===")
	fmt.Println("已连接到 RPC 服务器：localhost:1234")

	// 准备参数
	args := struct {
		A, B int
	}{10, 20}

	var reply int

	// 调用远程方法
	err = client.Call("Arith.Add", args, &reply)
	if err != nil {
		log.Fatal("调用失败：", err)
	}

	fmt.Printf("调用 Arith.Add(%d, %d) = %d\n", args.A, args.B, reply)

	// 调用乘法
	args2 := struct {
		A, B int
	}{6, 7}
	err = client.Call("Arith.Multiply", args2, &reply)
	if err != nil {
		log.Fatal("调用失败：", err)
	}
	fmt.Printf("调用 Arith.Multiply(%d, %d) = %d\n", args2.A, args2.B, reply)
}
```

---

## 23.30 rpc.Call：调用 RPC 方法

`rpc.Call` 是实际执行 RPC 调用的函数，它接收服务名.方法名、参数和结果指针，然后执行远程调用。

**专业词汇解释：**

- **rpc.Call**：同步调用 RPC 方法
- **Go()**：异步调用，返回 Call 对象
- **Call 结构体**：包含调用信息

```go
package main

import (
	"fmt"
	"log"
	"net/rpc"
)

// Args 用于传递参数
type Args struct {
	A, B int
}

// Quotient 用于返回除法结果
type Quotient struct {
	Quo, Rem int
}

func main() {
	// 连接服务器
	client, err := rpc.Dial("tcp", "localhost:1234")
	if err != nil {
		log.Fatal("连接失败：", err)
	}
	defer client.Close()

	fmt.Println("=== rpc.Call 调用 RPC 方法 ===")

	// 调用 1：加法
	args := Args{100, 200}
	var sum int
	err = client.Call("Arith.Add", args, &sum)
	if err != nil {
		log.Fatal("Add 调用失败：", err)
	}
	fmt.Printf("%d + %d = %d\n", args.A, args.B, sum)

	// 调用 2：乘法
	args2 := Args{15, 4}
	var product int
	err = client.Call("Arith.Multiply", args2, &product)
	if err != nil {
		log.Fatal("Multiply 调用失败：", err)
	}
	fmt.Printf("%d × %d = %d\n", args2.A, args2.B, product)

	// 调用 3：除法
	args3 := Args{17, 5}
	var quotient Quotient
	err = client.Call("Arith.Divide", args3, &quotient)
	if err != nil {
		log.Fatal("Divide 调用失败：", err)
	}
	fmt.Printf("%d ÷ %d = %d ... %d\n", args3.A, args3.B, quotient.Quo, quotient.Rem)

	// 异步调用示例
	fmt.Println("\n=== 异步调用 ===")
	call := client.Go("Arith.Add", Args{3, 4}, &sum, nil)
	<-call.Done // 等待完成
	fmt.Printf("异步调用结果：3 + 4 = %d\n", sum)
}
```

---

## 23.31 net/rpc/jsonrpc：JSON-RPC 1.0 实现，跨语言的 RPC

`net/rpc/jsonrpc` 提供了 JSON 格式的 RPC 实现，与标准 `net/rpc` 的 Gob 编码不同，JSON 是跨语言的，任何支持 JSON 的语言都可以调用。

**专业词汇解释：**

- **JSON-RPC**：使用 JSON 格式的 RPC 协议
- **跨语言**：可以被 JavaScript、Python、Java 等调用
- **协议版本**：JSON-RPC 1.0 和 2.0

```go
package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc"
	"net/rpc/jsonrpc"
)

// MathService 数学服务
type MathService struct{}

func (m *MathService) Add(args map[string]int, reply *int) error {
	*reply = args["a"] + args["b"]
	return nil
}

func (m *MathService) Say(args map[string]string, reply *string) error {
	*reply = fmt.Sprintf("Hello, %s!", args["name"])
	return nil
}

func main() {
	// 注册服务
	rpc.Register(&MathService{})

	// 监听
	l, err := net.Listen("tcp", ":1234")
	if err != nil {
		log.Fatal("监听失败：", err)
	}

	fmt.Println("=== JSON-RPC 服务器已启动 ===")
	fmt.Println("监听：localhost:1234")
	fmt.Println("使用 JSON 编码，支持跨语言调用！")

	// 使用 jsonrpc 处理连接
	for {
		conn, err := l.Accept()
		if err != nil {
			continue
		}
		go jsonrpc.ServeConn(conn)
	}
}
```

```go
// JSON-RPC 客户端示例
package main

import (
	"fmt"
	"log"
	"net/rpc/jsonrpc"
)

func main() {
	// 连接到 JSON-RPC 服务器
	client, err := jsonrpc.Dial("tcp", "localhost:1234")
	if err != nil {
		log.Fatal("连接失败：", err)
	}
	defer client.Close()

	fmt.Println("=== JSON-RPC 客户端 ===")

	// 调用 Add 方法
	args := map[string]int{"a": 100, "b": 200}
	var result int
	err = client.Call("MathService.Add", args, &result)
	if err != nil {
		log.Fatal("调用失败：", err)
	}
	fmt.Printf("Add(100, 200) = %d\n", result)

	// 调用 Say 方法
	args2 := map[string]string{"name": "Gopher"}
	var greeting string
	err = client.Call("MathService.Say", args2, &greeting)
	if err != nil {
		log.Fatal("调用失败：", err)
	}
	fmt.Printf("Say(Gopher) = %s\n", greeting)
}
```

---

## 本章小结

本章我们探索了 Go 语言标准库中处理 URL、HTML 和 RPC 的四大神器：

### 1. `net/url` 包 - URL 解析专家

`net/url` 包是 URL 处理的瑞士军刀，它能：
- 把 URL 字符串解析成结构化的 `*url.URL`
- 分别获取 Scheme、User、Host、Path、RawQuery、Fragment
- 构建和编码 URL，处理特殊字符
- 解析和操作查询参数（Query String）

**适用场景**：爬虫、API 客户端、URL 验证和修改。

### 2. `net/html` 包 - HTML 解析器

`net/html` 包能把 HTML 字符串解析成 DOM 树：
- `html.Parse` 返回根节点 `*html.Node`
- 节点类型包括 ElementNode、TextNode、CommentNode 等
- 通过 FirstChild 和 NextSibling 遍历树
- Attr 切片包含元素的所有属性

**适用场景**：网页解析、HTML 静态分析、数据提取。

### 3. `html/template` 包 - 安全模板引擎

`html/template` 是 Go 的 HTML 模板引擎：
- `{{.Field}}` 输出数据
- `{{if}}`、`{{range}}`、`{{with}}` 控制结构
- `{{template}}` 包含子模板
- **自动转义**：防止 XSS 攻击的核心特性
- FuncMap 支持自定义函数

**适用场景**：Web 开发、HTML 邮件生成、代码生成。

### 4. `net/rpc` 包 - 远程过程调用

`net/rpc` 包实现 RPC 通信：
- `rpc.Register` 注册服务
- `rpc.HandleHTTP` 注册 HTTP 处理器
- `rpc.Dial` 客户端连接
- `rpc.Call` 同步调用方法
- `net/rpc/jsonrpc` 提供跨语言的 JSON-RPC

**适用场景**：分布式系统内部通信、微服务间调用。

### 核心对比

| 包 | 用途 | 关键函数 | 安全特性 |
|---|---|---|---|
| `net/url` | URL 解析与构建 | `url.Parse`, `QueryEscape` | Query/Path 分开编码 |
| `net/html` | HTML 解析 | `html.Parse` | 无转义（需要手动） |
| `html/template` | HTML 生成 | `template.Parse`, `Execute` | 自动 XSS 转义 |
| `net/rpc` | 远程调用 | `Register`, `Dial`, `Call` | Gob/JSON 序列化 |

### 幽默总结

- URL 就像互联网的"门牌号"，`net/url` 就是读门牌号的放大镜
- HTML 是网页的"骨架"，`net/html` 是读骨架的 X 光机
- `html/template` 是网页的"裁缝"，量体裁衣还自带安全锁
- RPC 是程序员的"瞬间移动"，召唤远程函数就像召唤本地函数一样自然

> "学会了这些，你会发现互联网的世界不再神秘——URL 任你拆、HTML 任你扫、模板任你填、远程调用任你飞！"
