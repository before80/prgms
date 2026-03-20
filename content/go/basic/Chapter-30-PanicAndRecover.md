+++
title = "第30章 异常机制"
weight = 300
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第30章 异常机制

> panic和recover是Go的"核武器"——不是用来处理普通错误的。它们是最后的手段，用于真正不可恢复的情况。

**记住这个原则：**
- 普通错误 → 用 `error` 返回值
- 真正不可恢复的错误 → 用 `panic`

## 30.1 panic

### 30.1.1 什么是 panic

panic是Go的"紧急刹车"：
- 触发后，程序会立即停止当前函数的执行
- 开始"解栈"（unwind），执行defer函数
- 如果没有被recover捕获，程序会崩溃

```go
package main

import "fmt"

// 模拟可能出错的函数
func mightPanic(flag bool) {
    if flag {
        panic("出错了！这是个故意的panic")
    }
    fmt.Println("正常执行完成")
}

func main() {
    fmt.Println("=== 情况1：正常执行 ===")
    mightPanic(false)

    fmt.Println("\n=== 情况2：触发panic ===")
    // 用defer+recover捕获
    defer func() {
        if r := recover(); r != nil {
            fmt.Printf("✗ 捕获到panic: %v\n", r)
        }
    }()

    mightPanic(true)  // 这里会panic
    fmt.Println("这行不会执行")
}
```

### 30.1.2 panic 的传播过程

panic会沿着调用栈向上传播，每一层都会执行defer：

```go
package main

import "fmt"

func level3() {
    fmt.Println("level3: 开始执行...")
    panic("level3出错了！")  // 触发panic
    fmt.Println("level3: 这行不会执行")
}

func level2() {
    fmt.Println("level2: 开始执行...")
    level3()
    fmt.Println("level2: 不会执行到这里")
}

func level1() {
    fmt.Println("level1: 开始执行...")
    level2()
    fmt.Println("level1: 不会执行到这里")
}

func main() {
    fmt.Println("main: 开始...")

    defer func() {
        if r := recover(); r != nil {
            fmt.Printf("\nmain: 捕获到panic: %v\n", r)
        }
    }()

    level1()
    fmt.Println("main: 不会执行到这里")

    // main: 开始...
    // level1: 开始执行...
    // level2: 开始执行...
    // level3: 开始执行...
    //
    // main: 捕获到panic: level3出错了！
}
```

### 30.1.3 什么会触发 panic

除了手动调用 `panic()`，还有一些情况会自动触发panic：

```go
package main

import "fmt"

func demonstratePanics() {
    // 1. 数组越界访问
    // arr := [3]int{1, 2, 3}
    // _ = arr[10]  // panic: index out of range

    // 2. 空指针解引用
    // var p *int
    // fmt.Println(*p)  // panic: invalid memory address or nil pointer dereference

    // 3. 向已关闭的channel发送数据
    // ch := make(chan int)
    // close(ch)
    // ch <- 1  // panic: send on closed channel

    // 4. 关闭已关闭的channel
    // ch := make(chan int)
    // close(ch)
    // close(ch)  // panic: close of closed channel

    fmt.Println("这些操作会触发panic，请注释掉上面的代码后尝试！")
}

func main() {
    demonstratePanics()
}
```

---

## 30.2 recover

### 30.2.1 recover 的作用

`recover` 可以"抓住"正在传播的panic，防止程序崩溃：

```go
package main

import "fmt"

func riskyFunction(flag bool) {
    if flag {
        panic("危险操作失败！")
    }
    fmt.Println("操作成功")
}

// 用recover包装：把panic变成error
func safeCall(fn func(bool), flag bool) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic被捕获: %v", r)
        }
    }()
    fn(flag)
    return nil
}

func main() {
    // 情况1：正常执行
    fmt.Println("--- 测试正常情况 ---")
    err := safeCall(riskyFunction, false)
    if err != nil {
        fmt.Printf("错误: %v\n", err)
    } else {
        fmt.Println("✓ 执行成功")
    }

    // 情况2：触发panic
    fmt.Println("\n--- 测试panic情况 ---")
    err = safeCall(riskyFunction, true)
    if err != nil {
        fmt.Printf("✗ 捕获到错误: %v\n", err)
    }

    // --- 测试正常情况 ---
    // 操作成功
    // ✓ 执行成功
    //
    // --- 测试panic情况 ---
    // ✗ 捕获到错误: panic被捕获: 危险操作失败！
}
```

### 30.2.2 recover 的位置

`recover` 必须在 `defer` 函数中调用才有效：

```go
package main

import "fmt"

func correctUsage() {
    defer func() {
        // 在defer中调用recover
        if r := recover(); r != nil {
            fmt.Printf("✓ 正确捕获: %v\n", r)
        }
    }()

    panic("测试panic")
}

func wrongUsage() {
    // 这个recover永远不会捕获到东西
    // 因为recover只在defer中才有效
    recover()  // 永远不会执行到这里
    panic("测试panic")
}

func main() {
    fmt.Println("正确用法:")
    correctUsage()

    fmt.Println("\n错误用法（不要学）:")
    // wrongUsage()  // 如果放开这行，程序会崩溃
    fmt.Println("wrongUsage被注释掉了，因为会导致崩溃")
}
```

### 30.2.3 恢复后继续执行

panic被捕获后，程序可以继续运行：

```go
package main

import "fmt"

func process(step int) (ok bool) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Printf("  步骤%d: panic被恢复: %v\n", step, r)
            ok = false
        }
    }()

    fmt.Printf("步骤%d: 开始处理...\n", step)

    if step == 2 {
        panic("步骤2出错了！")
    }

    fmt.Printf("步骤%d: 处理完成\n", step)
    return true
}

func main() {
    fmt.Println("=== 开始处理 ===")

    result1 := process(1)
    fmt.Printf("步骤1结果: %v\n\n", result1)

    result2 := process(2)  // 这里会panic，但会被捕获
    fmt.Printf("步骤2结果: %v\n\n", result2)

    result3 := process(3)  // 即使步骤2失败了，步骤3仍然执行
    fmt.Printf("步骤3结果: %v\n", result3)

    fmt.Println("\n=== 处理结束，程序继续运行 ===")

    // === 开始处理 ===
    // 步骤1: 开始处理...
    // 步骤1: 处理完成
    // 步骤1结果: true
    //
    // 步骤2: 开始处理...
    //   步骤2: panic被恢复: 步骤2出错了！
    // 步骤2结果: false
    //
    // 步骤3: 开始处理...
    // 步骤3: 处理完成
    // 步骤3结果: true
    //
    // === 处理结束，程序继续运行 ===
}
```

---

## 30.3 defer 与 panic

### 30.3.1 defer 的执行顺序

当panic发生时，defer按照"后进先出"的顺序执行：

```go
package main

import "fmt"

func demonstrateDefer() {
    fmt.Println("函数开始")

    defer fmt.Println("defer 1")
    defer fmt.Println("defer 2")
    defer fmt.Println("defer 3")

    fmt.Println("函数主体")

    // defer执行顺序：3 -> 2 -> 1（后进先出）
}

func main() {
    demonstrateDefer()

    // 函数开始
    // 函数主体
    // defer 3
    // defer 2
    // defer 1
}
```

### 30.3.2 panic 时的 defer 执行

```go
package main

import "fmt"

func level1() {
    fmt.Println("level1: 开始")
    defer fmt.Println("level1: defer (最后执行)")

    level2()
}

func level2() {
    fmt.Println("level2: 开始")
    defer fmt.Println("level2: defer")

    level3()
}

func level3() {
    fmt.Println("level3: 开始")
    defer fmt.Println("level3: defer (最先执行)")

    panic("level3触发了panic!")
}

func main() {
    defer fmt.Println("main: defer (最先注册的，最后执行)")

    level1()

    fmt.Println("main: 程序继续执行（panic被恢复了）")

    // level1: 开始
    // level2: 开始
    // level3: 开始
    // level3: defer (最先执行)
    // level2: defer
    // level1: defer (最后执行)
    // main: 程序继续执行（panic被恢复了）
}
```

---

## 30.4 实际应用模式

### 30.4.1 服务器错误处理

Web服务器中，可以用recover防止一个请求的panic影响其他请求：

```go
package main

import "fmt"

type Request struct {
    ID   int
    Data string
}

type Response struct {
    Status  string
    Message string
}

// handleRequest 处理请求，用recover防止panic扩散
func handleRequest(req *Request) (resp *Response) {
    // defer + recover：捕获所有panic
    defer func() {
        if r := recover(); r != nil {
            resp = &Response{
                Status:  "error",
                Message: fmt.Sprintf("服务器内部错误: %v", r),
            }
        }
    }()

    // 正常处理逻辑
    if req.ID < 0 {
        panic("无效的请求ID")
    }

    if req.Data == "" {
        panic("请求数据为空")
    }

    return &Response{
        Status:  "success",
        Message: fmt.Sprintf("成功处理请求%d: %s", req.ID, req.Data),
    }
}

func main() {
    // 测试正常请求
    req1 := &Request{ID: 1, Data: "Hello"}
    resp1 := handleRequest(req1)
    fmt.Printf("请求1: [%s] %s\n", resp1.Status, resp1.Message)
    // 请求1: [success] 成功处理请求1: Hello

    // 测试panic请求（不会导致程序崩溃）
    req2 := &Request{ID: -1, Data: "World"}
    resp2 := handleRequest(req2)
    fmt.Printf("请求2: [%s] %s\n", resp2.Status, resp2.Message)
    // 请求2: [error] 服务器内部错误: 无效的请求ID

    req3 := &Request{ID: 2, Data: ""}
    resp3 := handleRequest(req3)
    fmt.Printf("请求3: [%s] %s\n", resp3.Status, resp3.Message)
    // 请求3: [error] 服务器内部错误: 请求数据为空

    fmt.Println("\n程序继续正常运行！")
}
```

### 30.4.2 库的错误封装

库函数可以用panic来报告"不可能发生"的错误：

```go
package main

import "fmt"

// 配置项（假设这些是必须配置的）
type Config struct {
    Host string
    Port int
}

// Validate 验证配置，如果配置错误则panic
// 这是"防御性编程"——配置错误应该被尽早发现
func (c *Config) Validate() {
    if c.Host == "" {
        panic("Config.Host不能为空")
    }
    if c.Port <= 0 || c.Port > 65535 {
        panic(fmt.Sprintf("Config.Port %d 超出有效范围", c.Port))
    }
}

// LoadConfig 加载配置（演示用）
func LoadConfig() (cfg *Config) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Printf("配置加载失败: %v\n", r)
            cfg = &Config{Host: "localhost", Port: 8080}  // 使用默认值
        }
    }()

    cfg = &Config{Host: "example.com", Port: 80}
    cfg.Validate()
    return cfg
}

func main() {
    cfg := LoadConfig()
    fmt.Printf("最终配置: %+v\n", cfg)
}
```

---

## 30.5 什么时候用 panic

### 30.5.1 使用 panic 的场景

| 场景 | 示例 | 替代方案 |
|------|------|----------|
| 编程错误 | 数组越界 | 检查索引 |
| 不可恢复 | 连接数据库失败 | 返回error |
| 致命错误 | 初始化失败 | 返回error |

**真的应该用panic的情况：**
1. **初始化失败**：`MustCompile`、`MustMarshalJSON`
2. **不可能发生**：使用`panic`作为"这里不应该到达"的标记
3. **严重的程序错误**：bug导致的崩溃，便于调试

### 30.5.2 不应该用 panic 的情况

```go
package main

import "fmt"

// ❌ 错误：普通错误用panic
func badExample(userID int) {
    if userID <= 0 {
        panic("userID必须大于0")  // 错误！应该返回error
    }
}

// ✅ 正确：普通错误返回error
func goodExample(userID int) error {
    if userID <= 0 {
        return fmt.Errorf("userID必须大于0，实际值: %d", userID)
    }
    return nil
}

func main() {
    fmt.Println("普通错误应该用error，不是panic！")
}
```

---

## 本章小结

本章我们学习了panic和recover：

**panic（紧急刹车）：**
- 触发后立即停止当前函数
- 沿着调用栈向上传播
- 执行所有defer函数
- 如果没被recover，程序崩溃

**recover（抓住刹车）：**
- 只能在defer函数中调用
- 抓住正在传播的panic
- 程序可以继续运行

**defer执行时机：**
- panic发生时会执行defer
- 多个defer按"后进先出"顺序执行

**使用原则：**
| 情况 | 处理方式 |
|------|----------|
| 普通错误 | 返回error |
| 初始化失败 | panic或error |
| 程序bug | panic |
| 服务器请求处理 | defer+recover |

**黄金法则：**
> panic用于真正的"不可能发生"的情况，而不是普通错误处理。

