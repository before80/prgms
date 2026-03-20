+++
title = "第24章 指针"
weight = 240
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第24章 指针

> 指针是Go语言的"遥控器"。它不直接持有数据，而是指向数据的"地址"。想象你有一把钥匙（指针），可以打开任意一扇门（内存地址），看到里面的东西（值）。

## 24.1 指针基础

### 24.1.1 什么是指针

指针本质上就是一个内存地址。在Go里：
- `*T` 表示指向T类型数据的指针
- `&` 操作符用于获取变量的地址
- `*` 操作符用于解引用，获取指针指向的值

```go
package main

import "fmt"

func main() {
    // 声明一个整型指针，初始值为nil（空指针）
    var p *int
    // 声明一个字符串指针
    var sp *string

    // nil指针的格式显示为<nil>
    fmt.Printf("p类型: %T, 值: %v\n", p, p) // p类型: *int, 值: <nil>
    fmt.Printf("sp类型: %T, 值: %v\n", sp, sp) // sp类型: *string, 值: <nil>
}
```

### 24.1.2 取地址与解引用

```go
package main

import "fmt"

func main() {
    x := 42       // 定义一个整型变量x
    y := "hello"  // 定义一个字符串变量y

    // 用&获取变量地址，赋值给指针
    px := &x      // px指向x的地址
    py := &y      // py指向y的地址

    // %p格式化输出地址（每次运行地址不同）
    fmt.Printf("x的地址: %p, x的值: %d\n", px, x) // x的地址: 0xc00000, x的值: 42
    fmt.Printf("y的地址: %p, y的值: %s\n", py, y) // y的地址: 0xc00000, y的值: hello

    // 通过指针修改原始变量的值（重要特性！）
    *px = 100     // 解引用px，将x的值改为100
    fmt.Printf("通过*px修改后，x的值 = %d\n", x)   // 通过*px修改后，x的值 = 100
}
```

### 24.1.3 nil 指针

nil是指针的"空值"，表示指针不指向任何地址。对nil指针解引用会panic。

```go
package main

import "fmt"

func main() {
    var p *int  // 声明但未初始化，默认是nil

    // nil指针可以用==和nil比较
    if p == nil {
        fmt.Println("p是nil指针，还没有指向任何地址") // p是nil指针，还没有指向任何地址
    }

    // 安全检查：解引用前先判断是否为nil
    if p != nil {
        fmt.Println(*p)
    } else {
        fmt.Println("p是nil，不能解引用，会panic！") // p是nil，不能解引用，会panic！
    }
}
```

---

## 24.2 指针操作

### 24.2.1 指针赋值

把指针赋值给另一个指针，两者指向同一个地址，修改任意一个会影响原变量。

```go
package main

import "fmt"

func main() {
    x := 42
    px := &x   // px指向x
    py := px   // py也指向x（拷贝的是地址，不是值）

    fmt.Printf("px指向: %d, 地址: %p\n", *px, px) // px指向: 42, 地址: 0xc00000
    fmt.Printf("py指向: %d, 地址: %p\n", *py, py) // py指向: 42, 地址: 0xc00000

    // 通过py修改，px和x都会变化
    *py = 100
    fmt.Printf("修改后: *px=%d, *py=%d, x=%d\n", *px, *py, x) // 修改后: *px=100, *py=100, x=100
}
```

### 24.2.2 指针比较

指针可以比较：相同地址为true，不同变量地址即使值相同也为false。

```go
package main

import "fmt"

func main() {
    x := 42
    y := 42  // y的值和x相同，但地址不同

    px := &x
    py := &x   // py指向x，和px同地址
    pz := &y   // pz指向y，和px不同地址

    fmt.Printf("px == py: %v (同地址)\n", px == py) // px == py: true (同地址)
    fmt.Printf("px == pz: %v (不同地址)\n", px == pz) // px == pz: false (不同地址)

    // nil指针比较：两个nil指针相等
    var nil1, nil2 *int
    fmt.Printf("nil1 == nil2: %v (都是nil)\n", nil1 == nil2) // nil1 == nil2: true (都是nil)
}
```

---

## 24.3 指针与函数

### 24.3.1 值传递 vs 指针传递（重要！）

Go的参数传递都是**值传递**：
- 值传递：拷贝整个值，指针的话拷贝地址
- 但指针解引用后修改，会影响原变量

```go
package main

import "fmt"

// 值传递：参数是int，拷贝整个值
func incrementValue(x int) {
    x++                                      // 只是在函数内部修改了副本
    fmt.Printf("  incrementValue内: x = %d\n", x) // incrementValue内: x = 101
}

// 指针传递：参数是*int，拷贝地址，解引用后能修改原变量
func incrementPointer(x *int) {
    (*x)++                                   // 解引用后修改的是原变量
    fmt.Printf("  incrementPointer内: *x = %d\n", *x) // incrementPointer内: *x = 101
}

func main() {
    n := 100

    fmt.Printf("原始值: n = %d\n", n) // 原始值: n = 100

    fmt.Println("\n调用incrementValue（值传递）...")
    incrementValue(n)
    fmt.Printf("调用后: n = %d (未改变！)\n", n) // 调用后: n = 100 (未改变！)

    fmt.Println("\n调用incrementPointer（指针传递）...")
    incrementPointer(&n)   // 必须传地址
    fmt.Printf("调用后: n = %d (已改变！)\n", n) // 调用后: n = 101 (已改变！)
}
```

### 24.3.2 函数返回指针

函数可以返回指针，这是安全的（不是返回局部变量的地址）。

```go
package main

import "fmt"

// Go的GC会处理函数内部分配的内存，所以返回局部变量的指针是安全的
func newInt() *int {
    x := 42              // 在堆上分配（编译器优化）
    return &x           // 返回x的地址
}

func main() {
    p := newInt()
    fmt.Printf("newInt返回: %d\n", *p) // newInt返回: 42
}
```

### 24.3.3 指针接收者

方法可以使用指针接收者，这样调用时会自动传指针。

```go
package main

import "fmt"

type Counter struct {
    name  string
    count int
}

// 指针接收者：方法内部可以修改结构体字段
func (c *Counter) AddPointer(n int) {
    c.count += n
    fmt.Printf("[AddPointer] %s 计数: %d\n", c.name, c.count) // [AddPointer] 计数器 计数: 11
}

func main() {
    // 创建Counter实例，用指针方式调用方法
    counter := &Counter{name: "计数器", count: 0}

    fmt.Printf("初始值: count = %d\n", counter.count) // 初始值: count = 0

    counter.AddPointer(10)   // 指针自动传递
    counter.AddPointer(1)
    fmt.Printf("最终值: count = %d\n", counter.count) // 最终值: count = 11
}
```

---

## 24.4 指针模式

### 24.4.1 可选字段模式

在实际开发中，有些字段是可选的（比如用户配置）。用指针可以区分"未设置"和"空值"：

- 如果字段是 `*string` 类型，nil表示未设置，非nil表示已设置
- 如果字段是 `string` 类型，无法区分"未设置"和"空字符串""

```go
package main

import "fmt"

// Config 表示应用配置
// 用指针类型表示可选字段：nil = 未设置，有值 = 已设置
type Config struct {
    Host     string   // 必填：主机地址
    Port     int      // 必填：端口号
    Username *string  // 可选：用户名（nil表示不设置）
    Password *string  // 可选：密码（nil表示不设置）
}

// 打印配置，可选字段需要判断是否为nil
func printConfig(c *Config) {
    fmt.Printf("Host: %s\n", c.Host) // Host: localhost
    fmt.Printf("Port: %d\n", c.Port) // Port: 8080

    // 检查Username是否为nil
    if c.Username != nil {
        fmt.Printf("Username: %s\n", *c.Username) // Username: admin
    } else {
        fmt.Println("Username: (未设置)")
    }

    // 检查Password是否为nil
    if c.Password != nil {
        fmt.Println("Password: (已设置)") // Password: (已设置)
    } else {
        fmt.Println("Password: (未设置)")
    }
}

// 辅助函数：创建字符串指针
func strPtr(s string) *string {
    return &s
}

func main() {
    // 创建配置：只有必填字段和部分可选字段
    pwd := "secret123"   // 密码字符串
    c := &Config{
        Host:     "localhost",
        Port:     8080,
        Username: strPtr("admin"),  // 设置了用户名
        Password: &pwd,              // 设置了密码
    }
    printConfig(c)
}
```

**为什么用指针表示可选字段？**

| 字段类型 | nil表示 | 空值表示 | 区分度 |
|---------|---------|---------|--------|
| `string` | ❌无法表示 | "" | 无法区分"未设置"和"空字符串" |
| `*string` | nil（未设置） | ""（已设置空字符串） | ✅ 完全区分 |

### 24.4.2 链表节点模式

指针常用于链表等数据结构。每个节点包含数据和指向下一个节点的指针。

```go
package main

import "fmt"

// ListNode 链表节点
// 包含一个值和一个指向下一个节点的指针
type ListNode struct {
    Value int      // 节点存储的值
    Next  *ListNode // 指向下一个节点的指针，nil表示没有下一个节点
}

// LinkedList 链表结构
// 包含头指针、尾指针和大小
type LinkedList struct {
    head *ListNode  // 链表头部
    tail *ListNode  // 链表尾部
    size int        // 节点数量
}

// NewLinkedList 创建一个空链表
func NewLinkedList() *LinkedList {
    return &LinkedList{}  // 空链表：head和tail都是nil
}

// Append 在链表末尾追加节点
func (l *LinkedList) Append(v int) {
    // 创建新节点
    newNode := &ListNode{Value: v}

    // 空链表：新节点既是头也是尾
    if l.tail == nil {
        l.head = newNode
        l.tail = newNode
    } else {
        // 非空链表：把新节点接到尾部后面
        l.tail.Next = newNode
        l.tail = newNode
    }
    l.size++
}

// Print 打印整个链表
func (l *LinkedList) Print() {
    fmt.Printf("链表 (size=%d): ", l.size)
    // 从头节点开始遍历，直到nil
    for curr := l.head; curr != nil; curr = curr.Next {
        fmt.Printf("%d", curr.Value)       // 打印当前节点的值
        if curr.Next != nil {
            fmt.Print(" -> ")              // 不是最后一个则打印箭头
        }
    }
    fmt.Println(" -> nil")                  // 以nil结尾
}

func main() {
    list := NewLinkedList()

    // 追加5个节点
    for _, v := range []int{1, 2, 3, 4, 5} {
        list.Append(v)
    }
    list.Print() // 链表 (size=5): 1 -> 2 -> 3 -> 4 -> 5 -> nil
}
```

**链表结构图：**

```
head                    tail
 |                       |
 v                       v
[1] -> [2] -> [3] -> [4] -> [5] -> nil
```

### 24.4.3 树节点模式（扩展）

指针同样适用于二叉树等更复杂的数据结构：

```go
package main

import "fmt"

// TreeNode 二叉树节点
type TreeNode struct {
    Value int
    Left  *TreeNode   // 左子树指针
    Right *TreeNode   // 右子树指针
}

// Insert 插入节点到二叉搜索树
func (n *TreeNode) Insert(v int) {
    if v < n.Value {
        // 比当前节点小，插入左子树
        if n.Left == nil {
            n.Left = &TreeNode{Value: v}
        } else {
            n.Left.Insert(v)
        }
    } else {
        // 比当前节点大（或相等），插入右子树
        if n.Right == nil {
            n.Right = &TreeNode{Value: v}
        } else {
            n.Right.Insert(v)
        }
    }
}

// InOrder 中序遍历（左子树 -> 根 -> 右子树）
func (n *TreeNode) InOrder() {
    if n == nil {
        return
    }
    if n.Left != nil {
        n.Left.InOrder()
    }
    fmt.Printf("%d ", n.Value)
    if n.Right != nil {
        n.Right.InOrder()
    }
}

func main() {
    // 构建一棵二叉搜索树
    //       5
    //      / \
    //     3   7
    //    / \   \
    //   1   4   9
    root := &TreeNode{Value: 5}
    root.Insert(3)
    root.Insert(4)
    root.Insert(7)
    root.Insert(1)
    root.Insert(9)

    fmt.Print("中序遍历: ") // 中序遍历: 1 3 4 5 7 9
    root.InOrder()
    fmt.Println()
}
```

---

## 24.5 指针的注意事项

### 24.5.1 指针的零值是 nil

声明指针但不初始化，它就是 nil：

```go
package main

import "fmt"

func main() {
    var p *int  // 默认值是nil
    fmt.Printf("未初始化的指针: %v\n", p) // 未初始化的指针: <nil>

    // 一定要先检查nil再解引用
    if p != nil {
        fmt.Println(*p)
    } else {
        fmt.Println("不能解引用nil指针！") // 不能解引用nil指针！
    }
}
```

### 24.5.2 不要对 nil 指针解引用

```go
package main

func main() {
    var p *int
    // 下面这行会panic！
    // println(*p) // panic: invalid memory address or nil pointer dereference
}
```

---

## 本章小结

本章我们学习了Go语言的指针：

**核心概念：**
- 指针是变量的地址，用 `*T` 表示
- `&` 取地址，`*` 解引用
- 指针的零值是 nil

**指针操作：**
- 指针赋值：两个指针可以指向同一个变量
- 指针比较：同地址为 true

**指针与函数：**
- 值传递：拷贝值，指针参数解引用后可以修改原变量
- 函数可以返回指针（Go的GC保证安全）

**常用模式：**
- 可选字段模式：用 `*string` 等表示"未设置"
- 链表/树结构：用指针连接节点

**黄金法则：**
> 解引用前一定要检查指针是否为 nil！

