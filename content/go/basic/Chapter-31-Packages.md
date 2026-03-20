+++
title = "第31章 包 Package"
weight = 310
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第31章 包 Package

> 包（Package），Go语言代码的"集装箱"。它把相关的代码组织在一起，方便复用和管理。

## 31.1 包的基本概念

### 31.1.1 为什么需要包

想象一个大型项目：
- 可能上百个文件
- 几十个功能模块
- 多人协作开发

没有包的话，所有代码都在一个文件夹里，会变成"代码地狱"！

包的作用：
1. **代码组织**：按功能划分，结构清晰
2. **命名空间**：不同包的同名类型不会冲突
3. **访问控制**：控制哪些内容对外可见
4. **复用**：一个包可以被多个项目复用

### 31.1.2 包声明

每个`.go`文件第一行必须声明自己属于哪个包：

```go
package main

import "fmt"

// main函数必须属于main包
func main() {
    fmt.Println("Hello, World!")
}
```

**包命名规则：**
- 必须放在源文件顶部
- 同一个目录的所有`.go`文件必须属于同一个包
- 包名通常是小写，简单明了

### 31.1.3 main 包

`main`包是程序的入口：
- 必须有 `main()` 函数
- 编译器会把 `main` 包编译成可执行文件

```go
package main

import "fmt"

func main() {
    fmt.Println("这是一个可执行程序！")
}
```

---

## 31.2 包的导入

### 31.2.1 基本导入

用 `import` 导入其他包：

```go
package main

import (
    "fmt"      // 格式化IO
    "math"     // 数学函数
)

func main() {
    fmt.Printf("圆周率 Pi = %.4f\n", math.Pi)   // 3.1416
    fmt.Printf("2的平方根 = %.4f\n", math.Sqrt(2)) // 1.4142
}
```

### 31.2.2 别名导入

当包名冲突或太长时，可以起别名：

```go
package main

import (
    f "fmt"           // fmt起别名f
    s "strings"      // strings起别名s
)

func main() {
    f.Println("别名导入演示")

    text := "hello world"
    f.Println("转大写:", s.ToUpper(text))   // HELLO WORLD
    f.Println("转小写:", s.ToLower(text))   // hello world
    f.Println("重复5次:", s.Repeat("a", 5)) // aaaaa
}
```

### 31.2.3 空白导入

用 `_` 导入包，只执行包的 `init()` 函数，不使用包的内容：

```go
package main

import (
    "fmt"
    _ "unsafe"  // 空白导入，执行unsafe包的初始化代码
)

func main() {
    fmt.Println("空白导入常用于：")
    fmt.Println("1. 注册驱动（如database/sql）")
    fmt.Println("2. 触发初始化代码")
    fmt.Println("3. 导入有副作用的包")
}
```

**空白导入的用途：**
- 导入有副作用的包（如注册驱动）
- 确保包的初始化代码执行
- SQLite驱动、图像处理库等

---

## 31.3 init 函数

### 31.3.1 init 自动调用

每个包可以有 `init()` 函数，在包被导入时自动执行：

```go
package main

import "fmt"

var initialized bool

// init 在包被导入时自动调用
func init() {
    initialized = true
    fmt.Println("init函数被调用，initialized =", initialized)
}

func main() {
    fmt.Println("main函数开始，initialized =", initialized)
    // init函数被调用，initialized = true
    // main函数开始，initialized = true
}
```

### 31.3.2 多个 init 函数

一个文件可以有多个 `init()`，按出现顺序执行：

```go
package main

import "fmt"

func init() {
    fmt.Println("第一个init()被调用")
}

func init() {
    fmt.Println("第二个init()被调用")
}

func init() {
    fmt.Println("第三个init()被调用")
}

func main() {
    fmt.Println("main()被调用")
}
```

**执行顺序：**
```
第一个init()被调用
第二个init()被调用
第三个init()被调用
main()被调用
```

### 31.3.3 init 的执行顺序

包按照依赖顺序初始化：

```go
package main

import "fmt"

func init() {
    fmt.Println("main包的init")
}

func main() {
    fmt.Println("main函数")
}
```

---

## 31.4 包结构

### 31.4.1 标准项目结构

一个典型的Go项目结构：

```
myproject/
├── cmd/
│   └── myapp/
│       └── main.go          # 程序入口
├── pkg/
│   ├── user/                # 用户模块
│   │   ├── user.go
│   │   └── user_test.go
│   └── order/               # 订单模块
│       ├── order.go
│       └── order_test.go
├── internal/                # 内部使用的包
│   └── config/
│       └── config.go
├── go.mod                   # 模块文件
└── README.md
```

### 31.4.2 internal 包

`internal` 目录是Go的"私有保护"机制：

```
myproject/
├── cmd/
│   └── app/
│       └── main.go
└── internal/
    └── utils/      # 只能被myproject内部的包导入
        └── util.go
```

其他外部项目无法导入 `myproject/internal/utils`。

### 31.4.3 cmd 和 pkg 目录

- `cmd/`：应用程序入口
- `pkg/`：库代码，可被外部导入

---

## 31.5 可见性规则

### 31.5.1 导出与未导出

Go的访问控制很简单：
- **首字母大写**：导出（exported），其他包可以访问
- **首字母小写**：未导出（unexported），只能在本包内访问

```go
package mylib

// Public 类型：其他包可以访问
type Public struct {
    Name string  // 导出字段
    age  int     // 未导出字段
}

// publicFunc：未导出，只能在mylib包内调用
func publicFunc() {}

// PublicFunc：导出，其他包可以调用
func PublicFunc() {}
```

```go
package main

import "mylib"

func main() {
    // 可以访问导出的内容
    p := mylib.Public{Name: "Alice"}

    // 无法访问未导出的内容
    // p.age  // 编译错误！
    // mylib.publicFunc()  // 编译错误！
}
```

---

## 31.6 go mod 依赖管理

### 31.6.1 初始化模块

```bash
# 创建新模块
go mod init github.com/username/project

# 已有项目，初始化go.mod
go mod init myproject
```

生成 `go.mod` 文件：
```
module github.com/username/project

go 1.21

require (
    github.com/some/pkg v1.2.3
)
```

### 31.6.2 添加依赖

```bash
# 添加单个依赖
go get github.com/gin-gonic/gin

# 添加特定版本
go get github.com/gin-gonic/gin@v1.9.0

# 升级到最新版本
go get github.com/gin-gonic/gin@latest
```

### 31.6.3 整理依赖

```bash
# 自动添加缺失的依赖，删除未使用的
go mod tidy
```

---

## 31.7 包的测试

### 31.7.1 测试文件命名

Go的测试文件有特殊命名规则：
- 文件名以 `_test.go` 结尾
- 放在被测试文件的同一个包目录下

```
mypkg/
├── mypkg.go          # 源代码
├── mypkg_test.go     # 测试代码
└── util.go           # 另一个源文件
└── util_test.go      # 对应的测试
```

### 31.7.2 编写测试

```go
package main

import "testing"

// TestAdd 测试加法函数
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d, want 5", result)
    }
}

// TestAddNegative 测试负数情况
func TestAddNegative(t *testing.T) {
    result := Add(-1, -2)
    if result != -3 {
        t.Errorf("Add(-1, -2) = %d, want -3", result)
    }
}
```

### 31.7.3 运行测试

```bash
# 运行当前目录所有测试
go test -v

# 运行指定测试
go test -v -run TestAdd

# 查看覆盖率
go test -cover

# 生成覆盖率报告
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

---

## 31.8 常见问题

### 31.8.1 包循环依赖

Go不允许循环依赖！

```go
// a.go
package a
import "b"

// b.go
package b
import "a"  // 错误！循环依赖
```

**解决方案：重构代码，把共同依赖提取到新包。**

### 31.8.2 同名冲突

两个包有相同名称时，用别名解决：

```go
package main

import (
    myfmt "fmt"      // 冲突时用别名
    other "some/pkg"
)

func main() {
    myfmt.Println("使用别名")
}
```

---

## 本章小结

本章我们学习了包机制：

**包的核心概念：**
- 包是Go代码组织的基本单位
- 每个`.go`文件必须属于某个包
- `main`包是程序入口

**包的导入：**
- 基本导入：`import "packageName"`
- 别名导入：`pkg "path"`
- 空白导入：`_ "driver"`（只执行init）

**可见性规则：**
- 首字母大写 = 导出（其他包可访问）
- 首字母小写 = 未导出（仅本包可访问）

**初始化顺序：**
```
import --> 变量初始化 --> init() --> main()
```

**go mod 命令：**
| 命令 | 作用 |
|------|------|
| `go mod init` | 初始化模块 |
| `go get` | 添加依赖 |
| `go mod tidy` | 整理依赖 |
| `go mod download` | 下载依赖 |

**测试：**
- 测试文件以 `_test.go` 结尾
- 使用 `testing` 包
- `go test -v` 运行测试

