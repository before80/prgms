+++
title = "第29章 错误机制"
weight = 290
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第29章 错误机制

> Go的错误处理独树一帜！错误就是普通的返回值，没有异常机制。这不是缺陷，而是Go的设计哲学——**错误是值，应该被显式处理**。

想象你点外卖：
- **异常模式**：外卖小哥直接把外卖扔给你，不管你在不在家
- **Go模式**：外卖小哥打电话告诉你"到了"，你决定怎么取

## 29.1 error 接口

### 29.1.1 error 接口定义

Go的错误处理基于这个简单接口：

```go
package main

import "fmt"

type ValidationError struct {
    Field string  // 出错的字段
    Msg   string  // 错误信息
}

// 实现error接口：只要有Error()方法就行
func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Msg)
}

func main() {
    // 创建自定义错误
    err := &ValidationError{Field: "email", Msg: "格式不正确"}

    fmt.Printf("错误类型: %T\n", err) // 错误类型: *main.ValidationError
    fmt.Printf("错误信息: %v\n", err) // 错误信息: email: 格式不正确
}
```

**error接口定义：**
```go
type error interface {
    Error() string
}
```

就这么简单！任何实现了 `Error() string` 方法的类型都是error。

### 29.1.2 简单错误创建

用 `errors.New()` 创建简单错误：

```go
package main

import (
    "errors"
    "fmt"
)

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("除数不能为零")  // 返回错误
    }
    return a / b, nil  // 返回nil表示没有错误
}

func main() {
    // 正常情况
    if result, err := divide(10, 2); err == nil {
        fmt.Printf("10 / 2 = %d\n", result) // 10 / 2 = 5
    }

    // 错误情况
    if result, err := divide(10, 0); err != nil {
        fmt.Printf("除法失败: %v\n", err) // 除法失败: 除数不能为零
    }
}
```

---

## 29.2 错误创建

### 29.2.1 自定义错误类型

对于复杂的错误场景，可以创建自定义错误类型：

```go
package main

import "fmt"

type CustomError struct {
    Field string  // 出错字段
    Msg   string  // 错误消息
}

func (e *CustomError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Msg)
}

// ValidateEmail 验证邮箱
func ValidateEmail(email string) error {
    if email == "" {
        return &CustomError{Field: "email", Msg: "不能为空"}
    }
    if len(email) < 5 || len(email) > 100 {
        return &CustomError{Field: "email", Msg: "长度必须在5-100之间"}
    }
    return nil
}

func main() {
    testCases := []string{"", "a@b", "valid@example.com"}

    for _, email := range testCases {
        err := ValidateEmail(email)
        if err != nil {
            fmt.Printf("'%s' 验证失败: %v\n", email, err)
        } else {
            fmt.Printf("'%s' ✓ 验证通过\n", email)
        }
    }

    // '' 验证失败: email: 不能为空
    // 'a@b' ✓ 验证通过
    // 'valid@example.com' ✓ 验证通过
}
```

### 29.2.2 错误包装（重要！）

用 `fmt.Errorf` 和 `%w` 可以包装错误，保留错误链：

```go
package main

import (
    "errors"
    "fmt"
)

// 定义基础错误
var ErrNotFound = errors.New("资源不存在")

// 查找用户（包装错误）
func findUser(id int) error {
    if id <= 0 {
        return fmt.Errorf("无效的用户ID %d: %w", id, ErrNotFound)
    }
    return nil
}

func main() {
    err := findUser(-1)

    fmt.Printf("错误信息: %v\n", err) // 错误信息: 无效的用户ID -1: 资源不存在

    // 检查错误链：是否包含ErrNotFound
    if errors.Is(err, ErrNotFound) {
        fmt.Println("✓ 确实是资源不存在的问题") // ✓ 确实是资源不存在的问题
    }

    // 检查其他错误
    if errors.Is(err, errors.New("其他错误")) {
        fmt.Println("包含其他错误")
    } else {
        fmt.Println("✗ 不包含其他错误") // ✗ 不包含其他错误
    }
}
```

---

## 29.3 错误检查

### 29.3.1 errors.Is

`errors.Is` 检查错误链中是否有指定的错误：

```go
package main

import (
    "errors"
    "fmt"
)

var (
    ErrDatabase = errors.New("数据库错误")
    ErrTimeout  = errors.New("超时错误")
)

// 模拟错误链
func queryDB() error {
    return fmt.Errorf("查询失败: %w", ErrDatabase)
}

func handleRequest() error {
    return fmt.Errorf("处理请求失败: %w", queryDB())
}

func main() {
    err := handleRequest()

    fmt.Printf("完整错误: %v\n", err)
    // 完整错误: 处理请求失败: 查询失败: 数据库错误

    // 检查是否包含数据库错误
    if errors.Is(err, ErrDatabase) {
        fmt.Println("✓ 包含数据库错误") // ✓ 包含数据库错误
    }

    // 检查是否包含超时错误
    if errors.Is(err, ErrTimeout) {
        fmt.Println("包含超时错误")
    } else {
        fmt.Println("✗ 不包含超时错误") // ✗ 不包含超时错误
    }
}
```

### 29.3.2 errors.As

`errors.As` 类型断言错误链中的错误类型：

```go
package main

import (
    "errors"
    "fmt"
)

// 自定义解析错误
type ParseError struct {
    Line   int    // 行号
    Column int    // 列号
    Text   string // 错误文本
}

func (e *ParseError) Error() string {
    return fmt.Sprintf("解析错误 at line %d, column %d: %s",
        e.Line, e.Column, e.Text)
}

// Parse 解析（返回自定义错误）
func Parse(input string) error {
    if input == "" {
        return &ParseError{
            Line:   1,
            Column: 1,
            Text:   "输入为空",
        }
    }
    return nil
}

func main() {
    err := Parse("")

    fmt.Printf("错误信息: %v\n", err)
    // 错误信息: 解析错误 at line 1, column 1: 输入为空

    // 尝试提取ParseError
    var parseErr *ParseError
    if errors.As(err, &parseErr) {
        fmt.Printf("✓ 解析错误详情: 行=%d, 列=%d, 文本=%s\n",
            parseErr.Line, parseErr.Column, parseErr.Text)
        // ✓ 解析错误详情: 行=1, 列=1, 文本=输入为空
    }

    // 尝试提取其他错误类型
    var dbErr *errors error
    if errors.As(err, &dbErr) {
        fmt.Println("是数据库错误")
    } else {
        fmt.Println("✗ 不是数据库错误") // ✗ 不是数据库错误
    }
}
```

---

## 29.4 错误处理模式

### 29.4.1 错误聚合

收集多个错误一起处理：

```go
package main

import "fmt"

// MultiError 聚合多个错误
type MultiError struct {
    errs []error
}

// Add 添加错误
func (m *MultiError) Add(err error) {
    if err != nil {
        m.errs = append(m.errs, err)
    }
}

// Error 实现error接口
func (m *MultiError) Error() string {
    if len(m.errs) == 0 {
        return ""
    }
    result := fmt.Sprintf("发现 %d 个错误:\n", len(m.errs))
    for i, e := range m.errs {
        result += fmt.Sprintf("  %d. %s\n", i+1, e.Error())
    }
    return result
}

func main() {
    m := &MultiError{}

    // 模拟多个验证错误
    m.Add(fmt.Errorf("用户名不能为空"))
    m.Add(fmt.Errorf("密码长度必须>=8位"))
    m.Add(fmt.Errorf("邮箱格式不正确"))

    if len(m.errs) > 0 {
        fmt.Println(m.Error())
    }

    // 发现 3 个错误:
    //   1. 用户名不能为空
    //   2. 密码长度必须>=8位
    //   3. 邮箱格式不正确
}
```

### 29.4.2 错误包装最佳实践

什么时候用 `errors.New`、`fmt.Errorf`、`自定义错误`：

```go
package main

import (
    "errors"
    "fmt"
)

// 1. 简单错误用 errors.New
var ErrNotFound = errors.New("资源不存在")

// 2. 带参数的错误用 fmt.Errorf
func userNotFound(id int) error {
    return fmt.Errorf("用户%d不存在: %w", id, ErrNotFound)
}

// 3. 需要携带更多信息的错误用自定义类型
type ValidationError struct {
    Field   string
    Message string
    Value   interface{}
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("验证失败 [%s]: %s (值: %v)", e.Field, e.Message, e.Value)
}

func main() {
    // 测试自定义错误
    err := &ValidationError{
        Field:   "age",
        Message: "必须在0-150之间",
        Value:   -5,
    }
    fmt.Printf("错误: %v\n", err)
    // 错误: 验证失败 [age]: 必须在0-150之间 (值: -5)
}
```

---

## 29.5 常见错误处理模式

### 29.5.1 忽略错误（要小心）

```go
package main

import "fmt"

func mightFail() error {
    return fmt.Errorf("some error")
}

func main() {
    // ❌ 忽略错误（可能造成问题）
    _ = mightFail()

    // ✅ 明确忽略（带注释说明原因）
    // 忽略EOF错误，因为我们已经处理完了
    _ = mightFail() // TODO: 处理这个错误
}
```

### 29.5.2 错误传递

```go
package main

import (
    "errors"
    "fmt"
)

func level3() error {
    return errors.New("底层错误")
}

func level2() error {
    return fmt.Errorf("中层: %w", level3())
}

func level1() error {
    return fmt.Errorf("顶层: %w", level2())
}

func main() {
    err := level1()

    fmt.Printf("顶层错误: %v\n", err)

    // 检查具体错误在哪一层
    if errors.Is(err, errors.New("底层错误")) {
        fmt.Println("✓ 追溯到了底层错误")
    }
}
```

---

## 本章小结

本章我们学习了错误处理：

**error接口：**
```go
type error interface {
    Error() string
}
```

**错误创建：**
- `errors.New()` - 简单错误
- `fmt.Errorf()` - 带格式的错误
- 自定义类型 - 携带更多信息的错误

**错误检查：**
- `errors.Is(err, target)` - 检查错误链中是否有目标错误
- `errors.As(err, &target)` - 从错误链中提取指定类型的错误

**错误包装：**
- `%w` 包装错误，保留错误链
- 错误链允许追溯根本原因

**黄金法则：**
> 错误是值，应该被显式处理。不要忽略错误，除非你确定它不重要。

