+++
title = "第36章 文档"
weight = 360
date = "2026-03-23T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第36章 文档

## 36.1 文档注释

> 📝 **文档**，听起来是个无聊透顶的话题对吧？写文档被认为是"程序员最讨厌的事情之一"，和"命名"并列第一。但是！你知道吗，优秀的文档可以让一个项目从"无人问津"变成"人手一份"；而糟糕的文档则可以让一个优秀的项目变成"无人能懂"的孤岛。这一章，我们就来聊聊 Go 语言的文档之道。

Go 语言的文档是**代码的一部分**，而不是事后的补充。这听起来有点反直觉，但 Go 团队从一开始就设计了一套将文档集成到代码中的机制。**godoc** 就是这个机制的产物——它能从一个 Go 包中提取注释，并生成漂亮的 HTML 文档。

### 36.1.1 注释格式

Go 的文档注释有一套约定俗成的格式。掌握了它，你的代码注释就能自动变成 API 文档：

```go
package greeting

// Hello 返回一个向指定名字打招呼的字符串
// 它会在名字前面加上 "Hello, "，后面加上 "!"
//
// 示例:
//
//	fmt.Println(greeting.Hello("张三"))
//	// 输出: Hello, 张三!
func Hello(name string) string {
    return "Hello, " + name + "!"
}
```

**关键规则**：

1. **注释要紧跟在要文档化的声明之前**，中间不能有空行
2. **注释要以被文档化的元素名开头**——比如上面的 `// Hello 返回...`，这里 `Hello` 就是函数名
3. **第一行要简洁**，能概括整体功能
4. **后面可以跟详细说明**，用空行分隔
5. **可以包含示例代码**，用 `//` 或多行注释都可以

```go
// Add 将两个整数相加并返回结果
//
// 这是一个非常基础的数学运算函数，没什么特别的。
// 但如果你恰好需要把两个数加在一起，它就能派上用场了！
//
// 参数:
//   - a: 第一个加数
//   - b: 第二个加数
//
// 返回值:
//   - a + b 的结果
//
// 注意: 本函数不进行溢出检查，如果结果超出 int 范围，后果自负！
func Add(a, b int) int {
    return a + b
}
```

### 36.1.2 段落组织

当你的文档需要描述多个方面的内容时，使用**空行**来分隔不同的段落。Go 的文档工具会将每个空行分隔的部分视为独立的段落。

```go
// Serve 处理传入的 HTTP 请求并返回响应
//
// Serve 会根据请求的 URL 路径来决定如何响应：
//
// 静态资源路径 (/static/*)
//   请求会被路由到静态文件服务器，
//   文件从配置的根目录提供。
//
// API 路径 (/api/*)
//   请求会被路由到 REST API 处理器。
//   返回 JSON 格式的响应。
//
// 其他路径
//   返回 404 Not Found 错误。
//
// 响应格式:
//
//	成功: {"status": "ok", "data": ...}
//	失败: {"status": "error", "message": "错误描述"}
//
// 错误处理:
//
// 如果在处理请求时发生内部错误，Serve 会：
//   1. 记录错误日志
//   2. 返回 500 Internal Server Error
//   3. 不会向客户端暴露内部错误详情
func Serve(w http.ResponseWriter, r *http.Request) {
    // 实现略
}
```

> 📝 **小技巧**：在文档中使用制表符（Tab）来缩进，可以让生成的 HTML 文档更加美观。Go 的文档工具会保留缩进，并将其渲染为 `<pre>` 代码块。

---

## 36.2 包文档

> 📦 包（Package）是 Go 代码组织的基本单位。每个 `.go` 文件都属于一个包，而一个目录下的所有 `.go` 文件共同构成一个包。**包文档**就是对这个包的总体描述。

包文档的规则很简单：**放在 `doc.go` 文件中**，或者**放在包中任何文件的顶部**（通常放在 `doc.go` 或 `package.go` 中）。

```go
// Package json 实现了 JSON 数据的解析和序列化。
//
// 这个包提供了 RFC 7159 中定义的 JSON 规范。
//
// JSON 是一种轻量级的数据交换格式，易于人类阅读和编写，
// 同时也易于机器解析和生成。它基于 JavaScript 的一个子集，
// 但虽然是基于 JavaScript，却不依赖 JavaScript，
// 可以在各种编程语言中使用。
//
// 基本用法:
//
//	// 编码
//	data := map[string]interface{}{"name": "张三", "age": 25}
//	jsonData, err := json.Marshal(data)
//
//	// 解码
//	var result map[string]interface{}
//	err = json.Unmarshal(jsonData, &result)
//
// 本包支持：
//   - 基本类型（string, int, float, bool）的编解码
//   - 数组和切片的编解码
//   - 结构体的编解码（字段标签控制）
//   - 自定义类型（通过 MarshalJSON/UnmarshalJSON 方法）
//   - 流式读写（Encoder/Decoder）
//   - 递归解析（支持嵌套结构）
package json
```

**注意**：包文档的第一句话非常重要！很多工具（包括 `go doc` 命令）只会显示第一句话。所以第一句话要**言简意赅**，一句话说清楚这个包是干什么的。

```go
// Package fmt 实现了格式化 I/O，类似于 C 的 printf 和 scanf。
package fmt
```

上面这个例子完美展示了"一句话包文档"的艺术：**简洁 + 准确 + 让人知道是否需要继续往下看**。

---

## 36.3 符号文档

> 🔍 符号（Symbol）包括函数、方法、类型、变量、常量等。**符号文档**就是这些元素的说明文档。

### 36.3.1 函数文档

函数文档是最常见的符号文档。记住一个原则：**用一句话描述函数做什么，然后用详细说明补充。**

```go
// NewUser 创建一个新的用户对象
//
// 这个函数会：
//   1. 验证输入参数的合法性
//   2. 生成唯一的用户 ID（基于 UUID）
//   3. 对密码进行哈希处理
//   4. 返回初始化好的用户对象
//
// 如果验证失败，会返回错误：
//   - ErrInvalidName: 用户名为空或长度超过 50
//   - ErrInvalidEmail: 邮箱格式不正确
//   - ErrWeakPassword: 密码强度不足（少于 8 位）
//
// 示例:
//
//	user, err := NewUser("张三", "zhang@example.com", "password123")
//	if err != nil {
//	    log.Fatal(err)
//	}
//	fmt.Printf("创建用户成功: %s\n", user.ID)
func NewUser(name, email, password string) (*User, error) {
    // 实现略
    return nil, nil
}
```

### 36.3.2 类型文档

类型文档需要说明这个类型代表什么、有什么用、以及如何使用。

```go
// User 代表系统中的一个用户账户
//
// User 是所有用户相关操作的核心类型。它包含了用户的
// 基本信息和状态字段。
//
// 创建 User 的推荐方式是使用 NewUser 函数，
// 而不是直接结构体字面量，因为 NewUser 会自动处理：
//   - ID 生成
//   - 密码哈希
//   - 时间戳设置
//
// 类型定义：
//
//	type User struct {
//	    ID        string    // 唯一标识符 (UUID)
//	    Name      string    // 显示名称
//	    Email     string    // 邮箱地址
//	    Password  string    // 密码哈希（永远不要直接访问）
//	    CreatedAt time.Time // 账户创建时间
//	    UpdatedAt time.Time // 最后更新时间
//	    Status    UserStatus // 账户状态
//	}
//
// 示例:
//
//	user := &User{
//	    Name:  "张三",
//	    Email: "zhang@example.com",
//	}
type User struct {
    ID        string
    Name      string
    Email     string
    Password  string
    CreatedAt time.Time
    UpdatedAt time.Time
    Status    UserStatus
}
```

### 36.3.3 示例代码

示例代码是文档的精华！它不仅告诉用户"怎么用"，还展示了"能做什么"。Go 的测试框架对示例有特殊支持——示例可以直接作为测试运行。

```go
// Package strconv 提供了在字符串和基本数据类型之间转换的功能。
//
// 示例:
//
//	// 字符串转整数
//	n, err := strconv.Atoi("123")
//	fmt.Println(n) // 123
//
//	// 整数转字符串
//	s := strconv.Itoa(456)
//	fmt.Println(s) // "456"
//
//	// 字符串转浮点数
//	f, err := strconv.ParseFloat("3.14", 64)
//	fmt.Println(f) // 3.14
//
//	// 浮点数转字符串
//	s = strconv.FormatFloat(3.14, 'f', 2, 64)
//	fmt.Println(s) // "3.14"
package strconv
```

**带注释的示例更佳**：

```go
// Add 将两个数相加并返回结果
//
// 示例:
//
//	// 基本用法
//	result := Add(1, 2)
//	fmt.Println(result) // 3
//
//	// 支持负数
//	result = Add(-1, 1)
//	fmt.Println(result) // 0
//
//	// 支持大数（请注意溢出）
//	result = Add(2147483647, 1) // 可能溢出
func Add(a, b int) int {
    return a + b
}
```

---

## 36.4 godoc 工具

> 📚 `godoc` 是 Go 标准库提供的文档工具。它可以从源代码中提取注释，生成 HTML 文档，让你的代码"自己会说话"。

Go 1.14 之前，`godoc` 是一个独立的工具；从 Go 1.14 开始，`godoc` 的核心功能被集成到了 `go doc` 命令中。

```bash
# 查看某个包的文档
go doc json

# 查看某个函数的具体文档
go doc json.Marshal

# 查看某个函数的具体文档
go doc json.Unmarshal

# 启动本地文档服务器（Go 1.13 之前）
godoc -http=:8080
```

**`go doc` 命令的常用选项**：

```bash
# 显示更多细节（包括未导出的成员，但通常用 -short)
go doc -all fmt

# 显示源码（使用 -src）
go doc -src fmt.Sprintf

# 简短的文档（只显示第一行）
go doc -short json

# 显示自定义包的文档（需要先 cd 到包目录）
go doc ./mypackage
```

**一个完整的示例**：

```bash
# 假设我们有一个项目 myproject
cd myproject

# 查看整个包的文档
go doc

# 查看特定类型的文档
go doc MyStruct

# 查看特定方法的文档
go doc MyStruct.MethodName
```

> 💡 **提示**：`go doc` 会使用**折叠显示**。如果你只想看第一行概要，加 `-short` 标志。

---

## 36.5 文档工具链

> 🔧 Go 的文档生态非常丰富，从简单的命令行工具到完整的 API 文档平台，应有尽有。这一节我们来看看常用的文档工具。

### 36.5.1 pkgsite

**pkgsite** 是 Go 官方推荐的文档网站生成工具，也是 `pkg.go.dev` 使用的技术栈。它可以让你在本地搭建一个和 `pkg.go.dev` 一样的文档网站。

```bash
# 安装 pkgsite
go install golang.org/x/pkgsite/cmd/pkgsite@latest

# 在你的模块根目录启动 pkgsite
cd /path/to/your/module
pkgsite
```

启动后，打开浏览器访问 `http://localhost:8080`，你就能看到完整的文档网站了！

**pkgsite 的特点**：
- 官方出品，质量有保证
- 和 `pkg.go.dev` 完全一致的界面
- 支持本地模块和远程模块
- 自动索引和搜索

### 36.5.2 示例测试即文档

Go 的测试框架有一个独特的功能：**示例测试**。这些示例既可以作为文档展示，又可以作为测试自动运行！

```go
package greeting

import "fmt"

// ExampleHello 展示了 Hello 函数的基本用法
func ExampleHello() {
    fmt.Println(Hello("张三"))
    // Output: Hello, 张三!
}
```

**运行示例测试**：

```bash
go test -v -run Example
```

输出会显示：

```
=== RUN   ExampleHello
--- PASS: ExampleHello (0.00s)
PASS
```

如果示例的输出和注释中的 `// Output:` 不匹配，测试就会失败。这确保了示例文档永远是正确的！

### 36.5.3 Swagger/OpenAPI

> 🐾 如果你在开发 REST API，**Swagger/OpenAPI** 是绕不开的话题。它是一种标准化的 API 描述格式，可以让 API "机器可读"，从而自动生成客户端代码、服务器代码、测试代码，甚至交互式文档。

#### 36.5.3.1 Swagger 简介

**Swagger** 是一套工具（编辑器、UI、代码生成器），而 **OpenAPI** 是描述 REST API 的规范（YAML 或 JSON 格式）。两者经常一起使用，所以经常被混为一谈。

**OpenAPI 文档示例**：

```yaml
openapi: 3.0.0
info:
  title: 用户管理 API
  version: 1.0.0
  description: 一个简单的用户管理 REST API

servers:
  - url: http://localhost:8080
    description: 本地开发服务器

paths:
  /users:
    get:
      summary: 获取用户列表
      operationId: listUsers
      tags:
        - users
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

#### 36.5.3.2 swaggo/swag 使用

**swag** 是一个 Go 语言的 Swagger 文档生成器。它通过解析代码中的注释来自动生成 OpenAPI 规范的 YAML/JSON 文件。

```bash
# 安装 swag 工具
go install github.com/swaggo/swag/cmd/swag@latest

# 在项目根目录初始化（生成 swagger.yaml）
swag init
```

**在代码中添加 Swagger 注释**：

```go
package main

// @title 用户管理 API
// @version 1.0
// @description 这是一个用户管理的 RESTful API
// @host localhost:8080
// @BasePath /
func main() {
    // 实现略
}

// @Summary 获取用户列表
// @Description 获取所有用户的列表
// @Tags users
// @Accept json
// @Produce json
// @Success 200 {array} User
// @Router /users [get]
func GetUsers() {
    // 实现略
}
```

**支持的注释标记**：

| 标记 | 说明 | 示例 |
|------|------|------|
| @title | API 标题 | @title 用户管理 API |
| @version | API 版本 | @version 1.0 |
| @host | API 主机 | @host localhost:8080 |
| @tag.name | 标签名称 | @tag.name users |
| @Summary | 操作摘要 | @Summary 获取用户列表 |
| @Param | 参数 | @Param id path int true "用户ID" |
| @Success | 成功响应 | @Success 200 {object} User |
| @Router | 路由 | @Router /users [get] |

#### 36.5.3.3 gin-swagger 集成

**gin-swagger** 是 Gin 框架的 Swagger 中间件，可以把生成的 Swagger UI 集成到你的 Gin 应用中。

```go
package main

import (
    "github.com/gin-gonic/gin"
    swaggerFiles "github.com/swaggo/files"
    ginSwagger "github.com/swaggo/gin-swagger"
    _ "myproject/docs"
)

// @title 用户管理 API
// @version 1.0
// @description 这是一个用户管理的 RESTful API
// @host localhost:8080
// @BasePath /
func main() {
    r := gin.Default()

    // 导入 swagger 路由
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

    r.Run(":8080")
}
```

访问 `http://localhost:8080/swagger/index.html`，就能看到交互式的 Swagger 文档界面了！

#### 36.5.3.4 API 注释规范

良好的 API 注释规范能让生成的文档更加清晰易读：

```go
// @Summary 创建订单
// @Description 创建一个新的订单
// @Tags orders
// @Accept json
// @Produce json
// @Param order body CreateOrderRequest true "订单信息"
// @Security BearerAuth
// @Success 201 {object} OrderResponse "订单创建成功"
// @Failure 400 {object} ErrorResponse "请求参数错误"
// @Router /orders [post]
func CreateOrder() {
    // 实现略
}
```

#### 36.5.3.5 自动生成文档

swag 工具可以自动从代码注释生成文档：

```bash
# 初始化（只需要执行一次）
swag init

# 解析特定目录（适用于大型项目）
swag init -g ./cmd/server/main.go -o ./docs

# 监听文件变化自动重新生成（开发时使用）
swag init -g ./cmd/server/main.go -o ./docs -w
```

生成的文件：

```
docs/
├── docs.go      # 包含 Swagger 文档的 Go 代码
├── swagger.json # JSON 格式的 OpenAPI 文档
└── swagger.yaml # YAML 格式的 OpenAPI 文档
```

#### 36.5.3.6 UI 界面定制

如果默认的 Swagger UI 不够用，可以进行定制：

```go
// 定制 Swagger UI 配置
func customSwaggerConfig() *ginSwagger.Config {
    return &ginSwagger.Config{
        URL:          "/swagger/doc.json",
        DeepLinking:  true,
        DocExpansion: "list",
        Filter:       true,
        ShowExtensions: true,
    }
}
```

### 36.5.4 其他 API 文档工具

#### 36.5.4.1 Redoc

**Redoc** 是一个纯前端的 API 文档渲染器，不需要后端服务。

```html
<!DOCTYPE html>
<html>
<head>
    <title>API 文档</title>
</head>
<body>
    <redoc spec-url="swagger.yaml"></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

**特点**：
- 响应式设计，移动端友好
- 纯前端，无需服务器
- 支持深色模式

#### 36.5.4.2 Postman 文档

**Postman** 不仅是一个 API 测试工具，还提供文档功能。

**特点**：
- 与 API 测试紧密结合
- 支持团队协作
- 可以直接发送请求测试
- 支持环境变量

#### 36.5.4.3 Stoplight Studio

**Stoplight Studio** 是一个可视化的 API 设计工具，支持：
- OpenAPI 规范的可视化编辑
- 模拟服务器（Mock Server）
- 文档自动生成

---

## 36.6 文档最佳实践

> 💎 这一节我们来聊聊如何写出高质量的文档。有句老话说得好："代码是写给人看的，顺带机器执行"。文档更是如此——它是直接给人看的！所以，文档的质量直接决定了你的代码是否容易被他人使用。

### 36.6.1 注释完整性

好的注释应该回答三个问题：**是什么（What）**、**为什么（Why）**、**怎么用（How）**。

```go
// Queue 是一个先进先出（FIFO）的队列实现
//
// 为什么需要这个类型？
//   标准库的 container/list 过于通用，有时候我们只需要一个简单的队列。
//   这个实现专门针对队列场景进行了优化，性能更好，API 更直观。
//
// 如何使用：
//   q := NewQueue()       // 创建队列
//   q.Enqueue(1)         // 入队
//   v := q.Dequeue()     // 出队
//   q.IsEmpty()          // 判空
//
// 线程安全：
//   本类型不是线程安全的。如果需要并发使用，请使用sync包进行同步。
type Queue struct {
    items []interface{}
}
```

### 36.6.2 示例覆盖

每个公开的 API 都应该有至少一个示例。示例是最好的文档——"一图胜千言，一例胜千言"。

```go
// Package sorter 提供了常用的排序算法
//
// 示例:
//
//	// 对整数切片排序
//	ints := []int{5, 2, 8, 1, 9}
//	sorter.BubbleSort(ints)
//	fmt.Println(ints) // [1 2 5 8 9]
//
//	// 对字符串切片排序
//	strs := []string{"banana", "apple", "cherry"}
//	sorter.QuickSort(strs)
//	fmt.Println(strs) // [apple banana cherry]
package sorter
```

### 36.6.3 README 规范

`README.md` 是项目的门面。一个好的 README 应该包含：

````markdown
# 项目名称

一行描述：这是一个用来做什么的项目。

## 特性

- 特性1：具体说明
- 特性2：具体说明
- 特性3：具体说明

## 安装

```bash
go get github.com/username/project
```

## 快速开始

简要说明如何使用这个项目，最好有代码示例。

## 使用示例

更详细的使用示例，展示核心功能。

## 配置

如果项目需要配置，说明配置选项。

## API 文档

指向更详细的 API 文档。

## 贡献指南

如何参与项目贡献。

## 许可证

MIT / Apache 2.0 / 等等。

## 联系方式

作者邮箱、联系方式等。
````

### 36.6.4 架构文档

对于复杂的项目，仅有 API 文档是不够的。还需要**架构文档**来说明系统的整体设计和各组件之间的关系。

````markdown
## 架构设计

### 系统组件

```
┌─────────────────────────────────────────────────────────┐
│                      API Gateway                        │
│                   (路由、认证、限流)                      │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌───────────┐   ┌───────────┐   ┌───────────┐
│ User Svc  │   │ Order Svc│   │Product Svc│
│   用户    │   │   订单    │   │   商品    │
└─────┬─────┘   └─────┬─────┘   └─────┬─────┘
      │               │               │
      └───────────────┼───────────────┘
                      ▼
            ┌─────────────────┐
            │   PostgreSQL     │
            │   (主数据库)      │
            └─────────────────┘
`\`\`

### 数据流

1. 客户端请求首先到达 API Gateway
2. Gateway 进行认证和限流
3. 请求被路由到相应的微服务
4. 微服务处理业务逻辑
5. 数据存储到 PostgreSQL 数据库

### 扩展点

- 如果需要缓存，可以在 Gateway 和服务之间添加 Redis
- 如果需要消息队列，可以在服务之间添加 Kafka
````

### 36.6.5 变更日志

维护一个清晰的变更日志，让用户知道每次版本更新都改变了什么：

```markdown
# Changelog

## [v2.1.0] - 2024-01-15

### 新增
- 支持 WebSocket 实时通信
- 新增 `Client.Subscribe()` 方法用于订阅事件

### 修复
- 修复了高并发下的连接泄漏问题
- 修复了某些情况下超时设置不生效的问题

### 优化
- 提升了 20% 的连接建立速度

## [v2.0.0] - 2023-12-01

### 重大变更
- 移除了已废弃的 `OldAPI` 方法
- 改变了 `Config` 结构体的字段名（`Host` -> `Address`）

### 新增
- 支持集群模式
- 新增 `LoadBalancer` 用于负载均衡

## [v1.0.0] - 2023-06-01

### 初始版本
- 基础 HTTP 服务器功能
- 路由中间件
- 基本日志记录
```

---

## 36.7 文档测试

> 🧪 Go 的测试框架不仅仅是用来测试代码的，它还可以用来测试**文档**！这一节我们就来看看如何利用测试框架来保证文档的正确性。

### 36.7.1 示例测试编写

Go 的示例测试是特殊的测试函数，它们以 `Example` 开头，并且不需要 `*testing.T` 参数：

```go
package greeting

import "fmt"

// ExampleHello 展示 Hello 函数的基本用法
func ExampleHello() {
    result := Hello("世界")
    fmt.Println(result)
    // Output: Hello, 世界!
}

// ExampleHello_multiple 展示不同输入的输出
func ExampleHello_multiple() {
    names := []string{"Alice", "Bob", "Charlie"}
    for _, name := range names {
        fmt.Println(Hello(name))
    }
    // Output:
    // Hello, Alice!
    // Hello, Bob!
    // Hello, Charlie!
}

// ExampleHello_empty 展示空输入的处理
func ExampleHello_empty() {
    result := Hello("")
    fmt.Println(result)
    // Output: Hello, !
}
```

### 36.7.2 可运行示例

示例不仅仅是文档，它们真的可以运行！这意味着你可以把示例代码放到测试文件中，确保它们永远是最新、最正确的：

```bash
# 运行所有示例测试
go test -v -run Example

# 运行特定包的示例测试
go test -v -run Example ./...
```

### 36.7.3 输出验证

Go 的示例测试会验证实际输出是否和注释中的 `// Output:` 匹配：

```go
func ExampleVerified() {
    data := []int{3, 1, 4, 1, 5, 9, 2, 6}
    sorted := BubbleSort(data)
    fmt.Println(sorted)
    // Output: [1 1 2 3 4 5 6 9]
    // 如果实际输出不是这个，测试会失败！
}
```

**不匹配的示例**：

```go
func ExampleBroken() {
    data := []int{3, 1, 4}
    sorted := BubbleSort(data)
    fmt.Println(sorted)
    // Output: [1 2 3 4]  <-- 这是错误的输出！
    // 如果 BubbleSort 实际返回 [1 3 4]，
    // 这个示例测试会失败，并显示：
    // "got [1 3 4]\nwant [1 2 3 4]"
}
```

---

## 36.8 文档国际化

> 🌍 如果你的项目面向全球用户，文档的多语言支持是必须的。这一节来看看如何做好文档国际化。

### 36.8.1 多语言文档

Go 官方推荐的做法是：**默认文档用英文写**，然后在 README 中用其他语言提供摘要。

```markdown
# My Awesome Project

[English](README.md) | [简体中文](README-zh-CN.md) | [日本語](README-ja.md)

This is the main documentation in English...
```

### 36.8.2 翻译工具

常用的文档翻译工具：

| 工具 | 说明 |
|------|------|
| DeepL | 高质量的机器翻译 |
| Google Translate | 便捷的翻译服务 |
| Crowdin | 专业的本地化平台 |
| GitLocalize | GitHub 集成的本地化工具 |

**翻译注意事项**：

1. **保持占位符不变**：如 `{{.Name}}`、`{id}` 等
2. **保留代码示例**：代码块不翻译
3. **维护术语表**：保持关键术语翻译一致

---

## 36.9 文档与版本

> 📌 文档和代码是配套的。代码有版本，文档也应该有版本；代码有废弃（deprecation），文档也要标记。

### 36.9.1 版本化文档

大型项目通常需要维护多个版本的文档：

```
docs/
├── v1/           # v1.x 的文档
│   ├── index.md
│   └── api.md
├── v2/           # v2.x 的文档
│   ├── index.md
│   └── api.md
└── v3/           # v3.x 的文档（最新）
    ├── index.md
    └── api.md
```

### 36.9.2 变更日志

维护变更日志的重要性我们前面已经说过了。这里推荐使用 **Semantic Versioning（语义化版本）**：

```
主版本号.次版本号.修订号

- 主版本号：当你做了不兼容的 API 修改
- 次版本号：当你新增加了向后兼容的功能
- 修订号：当你做了向后兼容的 bug 修复
```

### 36.9.3 废弃标记

当某个 API 需要被废弃时，文档中应该明确标记：

```go
// Deprecated: 请使用 NewClientV2 代替。
// NewClientV2 提供了更好的错误处理和更多的配置选项。
//
// 示例:
//
//	client, err := NewClientV2(cfg)
//	if err != nil {
//	    return nil, err
//	}
func NewClient(config *Config) (*Client, error) {
    // 实现略
}
```

---

## 本章小结

> 🎉 恭喜你完成了文档之旅！这一章我们探讨了如何让代码"自己说话"。

### 核心要点回顾

1. **文档是代码的一部分**：Go 语言内置了文档工具，注释可以直接生成 API 文档。

2. **示例是最好的文档**：可运行的示例不仅教人怎么用，还能自动验证正确性。

3. **工具链很重要**：从 `go doc` 到 `pkgsite`，从 Swagger 到 Redoc，有一堆工具可以帮你生成和维护文档。

4. **README 是项目的门面**：一个好的 README 应该让人一眼就知道这个项目是干什么的、怎么用。

5. **文档测试确保正确性**：示例测试可以把文档变成可验证的测试用例。

6. **国际化是大势**：如果你的用户群体是全球性的，多语言文档是必须的。

### 最佳实践清单

- ✅ 每个导出的函数、方法、类型都要有文档注释
- ✅ 文档注释的第一句话要言简意赅
- ✅ 为每个公开 API 编写可运行的示例
- ✅ 维护清晰的 README.md
- ✅ 使用版本化文档和变更日志
- ✅ 使用 Swagger/OpenAPI 描述 REST API
- ✅ 标记废弃的 API 并提供替代方案
- ✅ 定期审查和更新文档

> 💡 **最后一句话**：好的文档就像好的代码一样，需要细心呵护和持续改进。别等代码写完了再补文档——从写第一行代码开始，就顺便写文档。文档写得好，代码一定不会太差；代码写得烂，文档也救不了它。

