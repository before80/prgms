+++
title = "第 16 章：文件系统操作——os 包"
weight = 160
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 16 章：文件系统操作——os 包

> 🎭 "在 Go 的世界里，os 包就是那个永远在线的『万能中介』——操作系统想搞事情？找它！程序想撩操作系统？也找它！"

## 16.1 os 包解决什么问题

想象一下：你的 Go 程序是一个刚入职的小员工，而操作系统（OS）是那个掌控一切的大老板。os 包就是挂在小员工胸口的对讲机，让他能够：

- 📁 **读写文件** —— 告诉老板："我要读那个文件！"或"这个文件我不想要了！"
- 🌿 **获取环境变量** —— "老板，今天 PATH 是啥？"
- 🎮 **运行命令** —— "老板，帮我跑一下 `ls` 命令！"
- 📡 **处理信号** —— "老板想让我优雅地滚蛋？收到 SIGTERM，我这就收包走人！"

简单说，os 包就是 **Go 程序和操作系统之间的桥梁**，没有它，Go 代码就是一个只能自 high 的孤岛。

## 16.2 os 核心原理

os 包是 Go 标准库里最"底层"的平台抽象层。它就像一个精通多国语言的翻译官：

```go
// os 包的核心架构
//
//  ┌─────────────────────────────────────────┐
//  │           你的 Go 程序                  │
//  └─────────────────┬───────────────────────┘
//                    │ os 包 API
//  ┌─────────────────▼───────────────────────┐
//  │  os.File、os.XXX、exec.XXX、signal.XXX  │  ← 跨平台统一接口
//  └─────────────────┬───────────────────────┘
//                    │ 系统调用适配层
//  ┌─────────────────▼───────────────────────┐
//  │  unix.syscall / windows syscall         │  ← 平台特定实现
//  └─────────────────┬───────────────────────┘
//                    │ 最终握手
//  ┌─────────────────▼───────────────────────┐
//  │         Linux / macOS / Windows          │  ← 操作系统内核
//  └─────────────────────────────────────────┘
```

**专业词汇解释：**

- **系统调用（System Call）**：程序向操作系统内核请求服务的方式，比如 read、write、open、close 等
- **平台抽象层（Platform Abstraction Layer）**：隐藏不同操作系统差异，提供统一接口的设计模式
- **文件描述符（File Descriptor）**：操作系统内核为每个打开的文件分配的非负整数 ID

os 包的哲学是：**一次编写，随处编译（Compile Once, Run Anywhere）**——只要你别碰那些平台特定的花活儿。

## 16.3 os.Create：创建或截断文件

`os.Create` 是个急性子选手——要么创建新文件，要么把旧文件 **一刀切截断** 成零长度。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建或截断文件（权限 0644：所有者可读写，其他人可读）
    file, err := os.Create("hello.txt")
    if err != nil {
        panic(err) // 啊哦，出问题了
    }
    defer file.Close() // 记得关灯

    // 写入内容
    n, err := file.WriteString("Hello, os package!")
    fmt.Printf("写了 %d 个字节\n", n) // 写了 17 个字节
}
```

> ⚠️ **注意**：`os.Create` 总是 **截断** 现有文件！如果你想 **追加** 内容，请用 `os.OpenFile` 并指定 `O_APPEND`。

**专业词汇解释：**

- **截断（Truncate）**：将文件长度强制设为指定值，通常用于清空文件内容
- **文件权限（File Permission）**：0644 表示所有者可读写（6），其他人可读（4）

## 16.4 os.Open：打开已有文件（只读）

`os.Open` 是个保守派——它只负责 **只读打开** 文件，不负责创建，也不负责写入。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 只读方式打开文件
    file, err := os.Open("hello.txt")
    if err != nil {
        panic(err) // 文件不存在？等死吧
    }
    defer file.Close()

    // 读取全部内容
    data := make([]byte, 100)
    n, err := file.Read(data)
    if err != nil {
        panic(err)
    }
    fmt.Printf("读取了 %d 字节: %s\n", n, string(data[:n])) // 读取了 17 字节: Hello, os package!
}
```

**返回的 `*os.File` 只能读！** 想写？出门左转找 `os.OpenFile`。

## 16.5 os.OpenFile：最通用的打开方式

`os.OpenFile` 是文件打开家族的老大，支持 **6 种标志位** 的自由组合：

| 标志位 | 含义 | 场景 |
|--------|------|------|
| `O_RDONLY` | 只读 | 看文件 |
| `O_WRONLY` | 只写 | 写文件 |
| `O_RDWR` | 读写 | 边读边写 |
| `O_APPEND` | 追加模式 | 日志场景 |
| `O_CREATE` | 不存在则创建 | 确保文件存在 |
| `O_EXCL` | 配合 CREATE，必须不存在 | 原子创建，避免竞争 |
| `O_TRUNC` | 截断现有文件 | 清空重写 |

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 以追加+创建模式打开文件
    // 0666：默认权限（实际受 umask 影响）
    file, err := os.OpenFile("log.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
    if err != nil {
        panic(err)
    }
    defer file.Close()

    // 追加日志
    n, _ := file.WriteString("[2024-01-01] 系统启动\n")
    fmt.Printf("追加了 %d 字节\n", n) // 追加了 21 字节

    // 另一个常见用法：读写模式打开
    file2, _ := os.OpenFile("data.bin", os.O_RDWR|os.O_CREATE, 0644)
    defer file2.Close()
}
```

**小技巧**：标志位可以用 `|` 组合，就像搭积木一样！

## 16.6 os.File 的 Read：从当前位置读

`Read` 方法从文件的 **当前偏移量** 开始读取，移动指针。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, _ := os.Open("hello.txt")
    defer file.Close()

    // 创建一个 buf 用于存放读取的数据
    buf := make([]byte, 5) // 每次最多读 5 字节

    // 第一次读：从位置 0 开始，读 5 字节
    n1, _ := file.Read(buf)
    fmt.Printf("第1次读了 %d 字节: %q\n", n1, string(buf[:n1])) // 第1次读了 5 字节: "Hello"

    // 第二次读：从位置 5 开始（上次停下的地方）
    n2, _ := file.Read(buf)
    fmt.Printf("第2次读了 %d 字节: %q\n", n2, string(buf[:n2])) // 第2次读了 5 字节: ", os p"
}
```

**文件指针移动图解：**

```
文件内容: H e l l o ,   o s   p a c k a g e !
位置:     0 1 2 3 4 5 6 7 8 9 10 11 ...
                 ↑
                 第一 Read 停在这里

                 第二 Read 从这里开始 →
                              ↓
文件内容: H e l l o ,   o s   p a c k a g e !
位置:     0 1 2 3 4 5 6 7 8 9 10 11 ...
                             ↑
                             第二 Read 停在这里
```

## 16.7 os.File.ReadAt：从指定位置读（不移动位置）

`ReadAt` 是强迫症患者的最爱——从 **绝对位置** 读取指定字节数，读取前后指针纹丝不动。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, _ := os.Open("hello.txt")
    defer file.Close()

    buf := make([]byte, 5)

    // 从位置 0 开始读 5 字节
    n1, _ := file.ReadAt(buf, 0)
    fmt.Printf("位置0读: %d 字节, 内容: %q\n", n1, string(buf[:n1])) // 位置0读: 5 字节, 内容: "Hello"

    // 从位置 7 开始读 5 字节（同一文件，指针没动！）
    n2, _ := file.ReadAt(buf, 7)
    fmt.Printf("位置7读: %d 字节, 内容: %q\n", n2, string(buf[:n2])) // 位置7读: 5 字节, 内容: "os pa"

    // 再次从位置 0 读，结果和第一次一样！
    n3, _ := file.ReadAt(buf, 0)
    fmt.Printf("再次位置0读: %d 字节, 内容: %q\n", n3, string(buf[:n3])) // 再次位置0读: 5 字节, 内容: "Hello"
}
```

**Read vs ReadAt 的区别：**

| 方法 | 读从哪里 | 读后指针位置 |
|------|----------|--------------|
| `Read` | 当前位置 | 前进 |
| `ReadAt` | 指定偏移 | 不变 |

## 16.8 os.File.Write：写入内容

`Write` 从文件的 **当前偏移量** 开始写入，写多少指针就挪多少。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, _ := os.Create("output.txt")
    defer file.Close()

    // 写入字节 slice
    data := []byte{'G', 'o', ' ', '1', '.', '2', '0', '!', '\n'}
    n1, _ := file.Write(data)
    fmt.Printf("写了 %d 字节\n", n1) // 写了 9 字节

    // 写入字符串（更常用）
    n2, _ := file.WriteString("一起探索 Go 的 os 包吧！\n")
    fmt.Printf("写了 %d 字节\n", n2) // 写了 21 字节
}
```

> 💡 **小贴士**：`WriteString` 避免了你手动做 `[]byte(str)` 的转换，代码更简洁。

## 16.9 os.File.WriteAt：从指定位置写（不移动位置）

`WriteAt` 也是强迫症——在指定位置写入，指针原地不动。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建一个 30 字节的文件
    file, _ := os.Create("patch.txt")
    file.WriteString("ABCDEFGHIJKLMNOPQRSTUVWXYZ012345")
    file.Close()

    // 重新打开准备写
    file, _ = os.OpenFile("patch.txt", os.O_RDWR, 0644)
    defer file.Close()

    // 在位置 5 写入 "XXXX"
    n, _ := file.WriteAt([]byte("XXXX"), 5)
    fmt.Printf("在位置5写了 %d 字节\n", n) // 在位置5写了 4 字节

    // 读取全部验证
    data, _ := os.ReadFile("patch.txt")
    fmt.Printf("文件内容: %s\n", string(data))
    // 输出: ABCDEXXXXGHIJKLMNOPQRSTUVWXYZ012345
}
```

**效果对比：**

```
原内容:  ABCDEFGHIJKLMNOPQRSTUVWXYZ012345
位置:   012345...
                56789...
修改后:  ABCDEXXXXGHIJKLMNOPQRSTUVWXYZ012345
         01234XXXX56789...
                  ↑
                  写入位置 5
```

## 16.10 os.File.Seek：移动文件指针

`Seek` 是文件指针的 **操控器**，想让它去哪就去哪。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, _ := os.Open("hello.txt")
    defer file.Close()

    // 获取当前指针位置
    offset, _ := file.Seek(0, os.SEEK_CUR)
    fmt.Printf("当前位置: %d\n", offset) // 当前位置: 0

    // 往后跳 5 字节
    file.Seek(5, os.SEEK_SET) // SEEK_SET 从头算
    offset, _ = file.Seek(0, os.SEEK_CUR)
    fmt.Printf("跳到位置5后: %d\n", offset) // 跳到位置5后: 5

    // 再往后跳 3 字节
    file.Seek(3, os.SEEK_CUR) // SEEK_CUR 从当前位置算
    offset, _ = file.Seek(0, os.SEEK_CUR)
    fmt.Printf("再跳3字节: %d\n", offset) // 再跳3字节: 8

    // 跳到文件末尾
    file.Seek(0, os.SEEK_END)
    offset, _ = file.Seek(0, os.SEEK_CUR)
    fmt.Printf("文件末尾位置: %d\n", offset) // 文件末尾位置: 17
}
```

**Seek 的三个模式：**

| 模式 | 含义 | 基准点 |
|------|------|--------|
| `SEEK_SET` | 从文件开头算 | 0 |
| `SEEK_CUR` | 从当前位置算 | 当前指针 |
| `SEEK_END` | 从文件末尾算 | 文件长度 |

> 🎯 **妙用**：`Seek(0, SEEK_END)` 能快速获取文件长度！

## 16.11 os.File.Sync：强制同步到磁盘

`Sync` 是个强迫症患者——它确保所有"还在内存里游泳"的数据被 **立刻踹到磁盘** 上。

```go
package main

import (
    "fmt"
    "os"
    "time"
)

func main() {
    file, _ := os.Create("important.txt")
    defer file.Close()

    file.WriteString("关键数据，必须落盘！")

    // 告诉操作系统：哥们儿，这数据很重要，现在就给我写磁盘！
    if err := file.Sync(); err != nil {
        panic(err)
    }
    fmt.Println("数据已同步到磁盘，稳了！")

    // 对于重要文件，建议每次写完都 sync 一下
    // 但注意：这会有性能开销，别滥用
    time.Sleep(100 * time.Millisecond)
}
```

**专业词汇解释：**

- **缓冲区（Buffer）**：操作系统为了性能，在内存中缓存的待写入磁盘的数据
- **页缓存（Page Cache）**：Linux 内核的文件系统缓存机制
- **数据丢失风险**：程序崩溃时，未 sync 的数据可能还在内存缓冲区里，会丢失

> ⚠️ **性能警告**：频繁 Sync 会严重影响性能，因为磁盘 I/O 比内存慢几个数量级。除非你真的需要 **事务级别** 的数据安全性。

## 16.12 os.File.Truncate：截断文件

`Truncate` 是个裁缝——不管文件原来多长，强制把它 **裁成指定长度**。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建一个 100 字节的文件
    file, _ := os.Create("long.txt")
    file.Write(make([]byte, 100))
    file.Close()

    // 截断到 10 字节
    file, _ = os.OpenFile("long.txt", os.O_RDWR, 0644)
    file.Truncate(10)

    // 查看结果
    info, _ := file.Stat()
    fmt.Printf("截断后文件大小: %d 字节\n", info.Size()) // 截断后文件大小: 10 字节
    file.Close()

    // 也可以直接对文件路径截断，不需要先 Open
    os.Truncate("long.txt", 5)
    info, _ = os.Stat("long.txt")
    fmt.Printf("再次截断到: %d 字节\n", info.Size()) // 再次截断到: 5 字节
}
```

**两种截断场景：**

- **变短**：数据被无情切除
- **变长**（超过原长度）：文件被扩展，新增部分填 `0`

## 16.13 os.File.Close：关闭文件

`Close` 是每个打开文件都必须执行的 **收尾工作**。忘了关？小心文件描述符泄漏！

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, err := os.Open("hello.txt")
    if err != nil {
        panic(err)
    }

    // 读取数据
    data := make([]byte, 100)
    n, _ := file.Read(data)

    // 重要：关闭文件
    err = file.Close()
    if err != nil {
        fmt.Println("关闭文件失败:", err)
    }

    fmt.Printf("读完了，文件也关了，共 %d 字节\n", n)

    // defer 是最常用的自动关闭模式
    // defer 确保函数退出前一定会执行 Close
    file2, _ := os.Open("hello.txt")
    defer file2.Close()
    // ... 其他操作 ...
}
```

**文件描述符泄漏的症状：**

```go
// ❌ 错误示例：忘记关闭
func badExample() {
    for i := 0; i < 100000; i++ {
        file, _ := os.Open("somefile.txt")
        // 忘记 file.Close()！
        // 循环 10 万次后，你会用光系统所有的文件描述符
    }
}

// ✅ 正确示例：使用 defer
func goodExample() {
    for i := 0; i < 100000; i++ {
        file, _ := os.Open("somefile.txt")
        defer file.Close() // defer 会为每次迭代创建新调用，累积太多 defer 也不是好事
        // 更好的做法是把 Close 放在函数末尾，或使用其他模式
    }
}
```

## 16.14 os.File.Stat：获取文件元信息

`Stat` 返回文件的 **元数据**（metadata），包括大小、权限、修改时间等。但 **不读文件内容**。

```go
package main

import (
    "fmt"
    "os"
    "time"
)

func main() {
    // 获取文件元信息
    info, err := os.Stat("hello.txt")
    if err != nil {
        panic(err)
    }

    fmt.Printf("文件名: %s\n", info.Name())
    fmt.Printf("文件大小: %d 字节\n", info.Size())
    fmt.Printf("权限模式: %o\n", info.Mode())
    fmt.Printf("最后修改: %s\n", info.ModTime().Format(time.RFC3339))
    fmt.Printf("是目录吗: %t\n", info.IsDir())

    // 也可以对符号链接进行追踪（默认行为）
    // Stat 会自动解析符号链接，返回链接目标的信息
}
```

**返回的 `FileInfo` 包含：**

| 方法 | 返回值 | 含义 |
|------|--------|------|
| `Name()` | string | 文件名（不含路径） |
| `Size()` | int64 | 文件大小（字节） |
| `Mode()` | FileMode | 权限和类型标志 |
| `ModTime()` | time.Time | 最后修改时间 |
| `IsDir()` | bool | 是否为目录 |

## 16.15 os.FileInfo：Name、Size、Mode、ModTime、IsDir

`FileInfo` 是文件的 **身份证**，记录了文件的所有基本信息。

```go
package main

import (
    "fmt"
    "os"
    "strings"
    "time"
)

func main() {
    // 先创建测试文件
    os.WriteFile("demo.txt", []byte("Hello, FileInfo!"), 0644)

    info, _ := os.Stat("demo.txt")

    // Name：文件名（只含文件名，不含路径）
    fmt.Printf("Name: %s\n", info.Name()) // Name: demo.txt

    // Size：文件大小（字节）
    fmt.Printf("Size: %d bytes\n", info.Size()) // Size: 15 bytes

    // Mode：权限和类型
    fmt.Printf("Mode: %v\n", info.Mode())
    // 可能是 -rw-r--r-- 或类似

    // ModTime：最后修改时间
    fmt.Printf("ModTime: %s\n", info.ModTime().Format(time.UnixDate))
    // ModTime: Wed Mar 15 14:30:00 PST 2024（实际时间）

    // IsDir：是否为目录
    fmt.Printf("IsDir: %t\n", info.IsDir()) // IsDir: false

    // 额外福利：检查具体权限
    modeStr := info.Mode().String()
    fmt.Printf("权限字符串: %s\n", modeStr)

    // 检查是不是常规文件
    fmt.Printf("是常规文件: %t\n", info.Mode().IsRegular())
    // 是常规文件: true

    // 检查可读/可写/可执行
    fmt.Printf("可读: %t, 可写: %t, 可执行: %t\n",
        info.Mode()&0400 != 0,
        info.Mode()&0200 != 0,
        info.Mode()&0100 != 0)
}
```

## 16.16 os.Lstat：获取文件元信息，与 Stat 的区别

`Lstat` 和 `Stat` 的区别，就在于对 **符号链接（Symbolic Link）** 的态度：

- **Stat**：温柔地跟随符号链接，返回 **目标文件** 的信息
- **Lstat**：冷酷地拒绝跟随，返回 **符号链接本身** 的信息

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 先创建一个符号链接
    os.WriteFile("real.txt", []byte("我是真实文件"), 0644)
    os.Symlink("real.txt", "link.txt") // 创建 link.txt -> real.txt

    // Stat 跟随链接
    statInfo, _ := os.Stat("link.txt")
    fmt.Printf("Stat 返回:\n")
    fmt.Printf("  Name: %s\n", statInfo.Name()) // Name: real.txt（跟随了链接！）
    fmt.Printf("  Size: %d\n", statInfo.Size()) // Size: 15（目标文件大小）

    // Lstat 不跟随链接
    lstatInfo, _ := os.Lstat("link.txt")
    fmt.Printf("Lstat 返回:\n")
    fmt.Printf("  Name: %s\n", lstatInfo.Name()) // Name: link.txt（链接本身）
    fmt.Printf("  Size: %d\n", lstatInfo.Size()) // Size: 7（链接自己的大小，存储目标路径）
    fmt.Printf("  Mode: %v\n", lstatInfo.Mode())
    fmt.Printf("  是符号链接: %t\n", lstatInfo.Mode()&os.ModeSymlink != 0) // 是符号链接: true
}
```

**什么时候用 Lstat？**

- 当你需要 **检测符号链接本身** 而非其目标时
- 当你需要避免 **循环引用**（比如目录符号链接指向祖先目录）导致的无限递归时

## 16.17 os.Mode 类型：文件类型与权限位

`os.Mode` 是一个强大的位标志类型，可以 **同时存储文件类型和权限位**。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    info, _ := os.Stat("demo.txt")

    mode := info.Mode()

    // --- 文件类型判断（ModeType） ---
    fmt.Printf("是常规文件: %t\n", mode.IsRegular())      // true
    fmt.Printf("是目录: %t\n", mode.IsDir())             // false
    fmt.Printf("是符号链接: %t\n", mode&os.ModeSymlink != 0) // false

    // 各种文件类型常量
    fmt.Printf("模式类型: %v\n", mode.Type())            // 输出类似 ----rw---- 或 ---------
    fmt.Printf("是命名管道(FIFO): %t\n", mode&os.ModeNamedPipe != 0)
    fmt.Printf("是字符设备: %t\n", mode&os.ModeCharDevice != 0)
    fmt.Printf("是块设备: %t\n", mode&os.ModeDevice != 0)
    fmt.Printf("是套接字: %t\n", mode&os.ModeSocket != 0)

    // --- 权限位提取（ModePerm） ---
    fmt.Printf("\n权限位: %03o\n", mode.Perm()) // 八进制表示，如 0644

    // 单独提取各部分权限
    owner := (mode.Perm() & 0700) >> 6 // 所有者权限
    group := (mode.Perm() & 0070) >> 3 // 组权限
    other := mode.Perm() & 0007        // 其他用户权限
    fmt.Printf("所有者: %o, 组: %o, 其他: %o\n", owner, group, other)

    // 更直观的方式
    fmt.Printf("权限字符串: %s\n", mode.String())
}
```

**文件类型位：**

| 类型 | 值 | 说明 |
|------|-----|------|
| `os.ModeType` | `0170000` | 类型位掩码 |
| `os.ModeRegular` | `0100000` | 常规文件 |
| `os.ModeDir` | `0040000` | 目录 |
| `os.ModeSymlink` | `0120000` | 符号链接 |
| `os.ModeNamedPipe` | `0010000` | 命名管道 |
| `os.ModeSocket` | `0140000` | 套接字 |
| `os.ModeDevice` | `0060000` | 设备文件 |
| `os.ModeCharDevice` | `0020000` | 字符设备 |

**权限位（八进制）：**

```
权限位格式: rwx rwx rwx
            │   │   │
            │   │   └── 其他用户 (Other)
            │   └─────── 组 (Group)
            └────────── 所有者 (Owner)

r = 4 (读)
w = 2 (写)
x = 1 (执行)

常见权限组合:
0644 = rw-r--r--  (所有者可读写，其他人可读)
0755 = rwxr-xr-x  (所有者可读写执行，其他人可读执行)
0777 = rwxrwxrwx  (全员可读写执行，谨慎使用！)
```

## 16.18 os.Symlink：创建符号链接

符号链接是 Linux/Unix 的 **快捷方式**——一个文件，内容是另一个文件的路径。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建测试文件
    os.WriteFile("target.txt", []byte("我是目标文件的内容"), 0644)

    // 创建符号链接（类 Unix 系统）
    // Windows 用户注意：创建符号链接需要管理员权限或开发者模式
    err := os.Symlink("target.txt", "shortcut.txt")
    if err != nil {
        fmt.Printf("创建符号链接失败: %v\n", err)
        fmt.Println("Windows 用户：请开启开发者模式或以管理员运行")
        return
    }

    // 验证符号链接
    linkInfo, _ := os.Lstat("shortcut.txt")
    fmt.Printf("符号链接已创建: %s -> ???\n", linkInfo.Name())
    fmt.Printf("链接大小: %d 字节 (存储的是路径长度)\n", linkInfo.Size())
    fmt.Printf("是符号链接: %t\n", linkInfo.Mode()&os.ModeSymlink != 0)

    // 读取符号链接目标（需要 Readlink）
    target, _ := os.Readlink("shortcut.txt")
    fmt.Printf("指向目标: %s\n", target) // 指向目标: target.txt

    // 通过符号链接读取内容
    realInfo, _ := os.Stat("shortcut.txt") // Stat 会跟随链接
    fmt.Printf("通过链接读取大小: %d 字节\n", realInfo.Size())
}
```

> ⚠️ **Windows 注意事项**：在 Windows 上创建符号链接需要 SeCreateSymbolicLink 权限。普通用户可以开启"开发者模式"获得此权限，或者直接以管理员身份运行程序。

## 16.19 os.Readlink：读取符号链接目标

`Readlink` 返回符号链接指向的 **真实路径**（不是目标文件的内容）。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 准备环境
    os.WriteFile("original.txt", []byte("原始内容"), 0644)
    os.Symlink("original.txt", "symlink.txt")

    // 使用 Readlink 读取链接目标
    target, err := os.Readlink("symlink.txt")
    if err != nil {
        panic(err)
    }
    fmt.Printf("symlink.txt 指向: %s\n", target) // symlink.txt 指向: original.txt

    // 注意：Readlink 返回的是相对路径或绝对路径
    // 取决于创建时使用的是哪种路径

    // 绝对路径符号链接
    absPath, _ := os.Getwd()
    os.Symlink(absPath+"/original.txt", "abs_link.txt")
    absTarget, _ := os.Readlink("abs_link.txt")
    fmt.Printf("绝对路径链接指向: %s\n", absTarget)
}
```

**Readlink vs Stat 的区别：**

```go
// Readlink：只读链接本身，告诉你"它指向谁"
target, _ := os.Readlink("link.txt") // "somefile.txt"

// Stat：跟随链接，告诉你"它指向的文件长什么样"
info, _ := os.Stat("link.txt")       // FileInfo{somefile.txt 的大小、权限等}
```

## 16.20 os.Mkdir：创建目录

`Mkdir` 一次只能创建 **一级目录**，是个专注单个任务的好学生。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建单层目录（权限 0755）
    err := os.Mkdir("my_folder", 0755)
    if err != nil {
        // 如果目录已存在，会返回错误
        if os.IsExist(err) {
            fmt.Println("目录已经存在啦！")
        } else {
            panic(err)
        }
    } else {
        fmt.Println("目录创建成功！")
    }

    // 查看创建结果
    info, err := os.Stat("my_folder")
    if err == nil {
        fmt.Printf("目录名: %s, 是目录: %t\n", info.Name(), info.IsDir())
    }
}
```

> 📝 **权限说明**：`0755` 表示所有者可读写执行（7），组和其他可读执行（5）。注意：在 Windows 上，权限位会被忽略或有不同的解释。

## 16.21 os.MkdirAll：创建多级目录

`MkdirAll` 是 `Mkdir` 的升级版，支持 **一次性创建多级目录**（类似 `mkdir -p`）。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建嵌套目录，无论多深都能一次搞定
    path := "a/b/c/d/e"
    err := os.MkdirAll(path, 0755)
    if err != nil {
        panic(err)
    }
    fmt.Printf("创建目录树: %s\n", path)

    // 验证：逐级查看
    dirs := []string{"a", "a/b", "a/b/c", "a/b/c/d", "a/b/c/d/e"}
    for _, d := range dirs {
        info, err := os.Stat(d)
        if err == nil {
            fmt.Printf("  %s: 存在 ✓, 是目录: %t\n", d, info.IsDir())
        }
    }

    // MkdirAll 的特点：不会报错如果目录已存在
    err = os.MkdirAll("a/b/c", 0755) // 再次调用，不会报错
    if err == nil {
        fmt.Println("再次创建已存在的目录：成功（不报错）")
    }
}
```

**对比 Mkdir 和 MkdirAll：**

```go
// ❌ Mkdir：父目录不存在就失败
os.Mkdir("a/b/c", 0755) // 报错！因为 a/ 和 a/b/ 不存在

// ✅ MkdirAll：父目录不存在就一起创建
os.MkdirAll("a/b/c", 0755) // 成功！a/、a/b/、a/b/c/ 都会被创建
```

## 16.22 os.Remove：删除文件或空目录

`Remove` 是个挑剔的清洁工——只接受 **文件或空目录**，有东西的目录？不好意思，不收。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建测试文件
    os.WriteFile("to_delete.txt", []byte("删我吧"), 0644)

    // 删除文件
    err := os.Remove("to_delete.txt")
    if err != nil {
        panic(err)
    }
    fmt.Println("文件已删除 ✓")

    // 测试非空目录
    os.Mkdir("non_empty", 0755)
    os.WriteFile("non_empty/file.txt", []byte("我有内容"), 0644)

    err = os.Remove("non_empty")
    if err != nil {
        fmt.Printf("删除非空目录失败: %v\n", err) // 删除非空目录失败: remove non_empty: directory not empty
        fmt.Println("需要用 RemoveAll 才行！")
    }

    // 空目录可以删除
    os.Mkdir("empty_dir", 0755)
    os.Remove("empty_dir")
    fmt.Println("空目录已删除 ✓")
}
```

## 16.23 os.RemoveAll：递归删除目录及其内容

`RemoveAll` 是 `Remove` 的**无敌升级版**——不管目录里有多少东西，统统删掉，不留痕迹。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建一个复杂的目录结构
    os.MkdirAll("project/src/utils", 0755)
    os.MkdirAll("project/src/models", 0755)
    os.MkdirAll("project/docs", 0755)
    os.WriteFile("project/src/main.go", []byte("package main"), 0644)
    os.WriteFile("project/src/utils/helper.go", []byte("package utils"), 0644)
    os.WriteFile("project/README.md", []byte("# My Project"), 0644)

    fmt.Println("目录结构已创建")

    // 一行代码，删得干干净净
    err := os.RemoveAll("project")
    if err != nil {
        panic(err)
    }
    fmt.Println("整个目录树已删除 ✓")

    // 验证
    _, err = os.Stat("project")
    if os.IsNotExist(err) {
        fmt.Println("验证：project 目录已不存在")
    }
}
```

> ⚠️ **危险警告**：`RemoveAll` 是真正的"删库到跑路"命令。使用时务必小心，确认路径正确，否则后果自负！

## 16.24 os.Rename：重命名或移动

`Rename` 一专多能——既能 **重命名**，又能 **移动文件/目录**。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建测试文件
    os.WriteFile("old_name.txt", []byte("我需要改名"), 0644)

    // 重命名文件
    err := os.Rename("old_name.txt", "new_name.txt")
    if err != nil {
        panic(err)
    }
    fmt.Println("文件已重命名: old_name.txt → new_name.txt")

    // 移动到不同目录
    os.MkdirAll("target_dir", 0755)
    err = os.Rename("new_name.txt", "target_dir/moved.txt")
    if err != nil {
        panic(err)
    }
    fmt.Println("文件已移动: new_name.txt → target_dir/moved.txt")

    // 验证移动结果
    _, err = os.Stat("target_dir/moved.txt")
    if err == nil {
        fmt.Println("验证：文件已在目标位置")
    }

    // 注意：跨文件系统移动可能不是原子操作
    // 在同一文件系统内，Rename 通常是原子的
}
```

**Rename vs 直接操作：**

```go
// ❌ 手动移动（需要先复制再删除）
data, _ := os.ReadFile("a.txt")
os.WriteFile("b.txt", data)
os.Remove("a.txt")

// ✅ Rename（操作系统原生支持，可能更快）
os.Rename("a.txt", "b.txt")
```

## 16.25 os.WalkDir：遍历目录树

`WalkDir` 是 Go 1.16 引入的 **目录树遍历神器**，比旧的 `filepath.Walk` 更高效（不会 follow 符号链接）。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建测试目录结构
    os.MkdirAll("root/sub1/deep", 0755)
    os.MkdirAll("root/sub2", 0755)
    os.WriteFile("root/file1.txt", []byte("1"), 0644)
    os.WriteFile("root/sub1/file2.txt", []byte("2"), 0644)
    os.WriteFile("root/sub1/deep/file3.txt", []byte("3"), 0644)
    os.WriteFile("root/sub2/file4.txt", []byte("4"), 0644)

    // 遍历目录树
    fmt.Println("目录树结构：")
    err := os.WalkDir("root", func(path string, d os.DirEntry, err error) error {
        if err != nil {
            return err
        }

        // 计算缩进层级
        indent := ""
        for i := 0; i < len(path)-4; i++ { // "root/" 长度为 5
            indent += "  "
        }

        if d.IsDir() {
            fmt.Printf("%s📁 %s/\n", indent, d.Name())
        } else {
            info, _ := d.Info()
            fmt.Printf("%s📄 %s (%d bytes)\n", indent, d.Name(), info.Size())
        }
        return nil
    })

    if err != nil {
        panic(err)
    }

    // 清理测试数据
    os.RemoveAll("root")
}
```

**输出示例：**

```
目录树结构：
📁 root/
  📄 file1.txt (1 bytes)
  📁 sub1/
    📄 file2.txt (1 bytes)
    📁 deep/
      📄 file3.txt (1 bytes)
  📁 sub2/
    📄 file4.txt (1 bytes)
```

**WalkDir vs filepath.Walk：**

| 特性 | `os.WalkDir` | `filepath.Walk` |
|------|-------------|-----------------|
| Go 版本 | 1.16+ | 1.0+ |
| 符号链接 | 默认不跟随 | 可选择跟随 |
| 性能 | 更高效（DirEntry 缓存） | 一般 |
| 返回值 | `DirEntry` | `FileInfo` |

## 16.26 os.CreateTemp、os.MkdirTemp（Go 1.16+）：创建临时文件或目录

临时文件/目录是程序的 **一次性纸巾**——用完即弃，操作系统会自动帮你清理（如果你忘了删的话）。

```go
package main

import (
    "fmt"
    "os"
    "path/filepath"
)

func main() {
    // CreateTemp：创建临时文件
    // 第一个参数：目录（空字符串表示使用系统临时目录）
    // 第二个参数：文件名模板（前缀 + 后缀）
    tempFile, err := os.CreateTemp("", "myapp_temp_*.txt")
    if err != nil {
        panic(err)
    }
    defer os.Remove(tempFile.Name()) // 用完记得删
    defer tempFile.Close()

    fmt.Printf("临时文件: %s\n", tempFile.Name())
    // 例如: /tmp/myapp_temp_1234567890.txt

    // 写入一些数据
    tempFile.WriteString("这是临时文件的内容")
    tempFile.Seek(0, os.SEEK_SET)

    // 读取验证
    data, _ := os.ReadFile(tempFile.Name())
    fmt.Printf("内容: %s\n", string(data))

    // MkdirTemp：创建临时目录
    tempDir, err := os.MkdirTemp("", "myapp_tempdir_*")
    if err != nil {
        panic(err)
    }
    defer os.RemoveAll(tempDir) // 递归删除整个目录树

    fmt.Printf("临时目录: %s\n", tempDir)

    // 在临时目录里创建文件
    tempFile2, _ := os.Create(filepath.Join(tempDir, "nested.txt"))
    tempFile2.WriteString("临时目录里的文件")
    tempFile2.Close()

    fmt.Printf("临时目录内容: %s\n", filepath.Join(tempDir, "nested.txt"))

    // 临时文件的命名规则
    // 系统临时目录: os.TempDir()
    // 模板中的 * 会被随机字符替换
}
```

**CreateTemp 和 MkdirTemp 的特点：**

- **原子性创建**：`O_EXCL` 标志确保不会与已有文件冲突
- **随机文件名**：模板中的 `*` 会被随机字符串替换
- **高并发安全**：多个 goroutine 同时调用不会产生冲突
- **自动清理建议**：用完最好手动删除，操作系统重启也会清理

## 16.27 os.TempDir：返回临时目录路径

`TempDir` 返回操作系统推荐的 **临时文件存放目录**。

```go
package main

import (
    "fmt"
    "os"
    "path/filepath"
)

func main() {
    // 获取系统临时目录
    tempDir := os.TempDir()
    fmt.Printf("系统临时目录: %s\n", tempDir)

    // 常见系统的临时目录
    // Linux/macOS: /tmp
    // Windows: C:\Users\用户名\AppData\Local\Temp

    // 在临时目录里创建文件（安全的做法）
    myTempFile := filepath.Join(tempDir, "myapp_unique_id.txt")
    os.WriteFile(myTempFile, []byte("临时数据"), 0644)
    defer os.Remove(myTempFile)

    fmt.Printf("在临时目录创建了: %s\n", myTempFile)

    // 注意：TempDir 返回的路径末尾没有分隔符
    // 拼接路径时请使用 filepath.Join
}
```

## 16.28 os.Chmod、os.Chown：修改文件权限、所有者

**注意**：这两个函数在 Windows 上支持有限，`Chown` 通常需要管理员权限。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 创建测试文件
    os.WriteFile("secret.txt", []byte("秘密内容"), 0644)

    // Chmod：修改权限
    // 把文件改成只有所有者可读写 (600)
    err := os.Chmod("secret.txt", 0600)
    if err != nil {
        fmt.Printf("Chmod 失败: %v\n", err)
        fmt.Println("（Windows 上权限修改可能不生效）")
    } else {
        info, _ := os.Stat("secret.txt")
        fmt.Printf("新权限: %o\n", info.Mode().Perm()) // 新权限: 600
    }

    // 批量修改权限（目录递归）
    os.MkdirAll("project", 0755)
    os.Chmod("project", 0755)

    // Chown：修改所有者（Unix 系统）
    // 注意：普通用户只能修改自己的文件
    // Chown 需要 root 权限（UID 0）
    err = os.Chown("secret.txt", os.Getuid(), os.Getgid())
    if err != nil {
        fmt.Printf("Chown 失败: %v (可能需要 root 权限)\n", err)
    }

    // 验证最终权限
    info, _ := os.Stat("secret.txt")
    fmt.Printf("最终权限: %s\n", info.Mode())

    // 清理
    os.Remove("secret.txt")
    os.RemoveAll("project")
}
```

**跨平台兼容代码：**

```go
func setPermissions(filename string, mode os.FileMode) error {
    err := os.Chmod(filename, mode)
    if err != nil {
        // Windows 上 chmod 可能失败，尝试忽略
        if os.IsPermission(err) {
            return nil // Windows 上权限行为不同
        }
        return err
    }
    return nil
}
```

## 16.29 os.Chtimes：修改文件访问时间和修改时间

`Chtimes` 让你能够 **伪造"案发现场"**——修改文件的访问时间和修改时间。

```go
package main

import (
    "fmt"
    "os"
    "time"
)

func main() {
    // 创建测试文件
    os.WriteFile("time_test.txt", []byte("时间测试"), 0644)

    // 模拟一个"古老"的文件
    oldTime := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
    err := os.Chtimes("time_test.txt", oldTime, oldTime)
    if err != nil {
        panic(err)
    }

    // 验证修改结果
    info, _ := os.Stat("time_test.txt")
    fmt.Printf("文件名: %s\n", info.Name())
    fmt.Printf("访问时间(Atime): %s\n", info.Atim().Time.Format(time.RFC3339))
    fmt.Printf("修改时间(Mtime): %s\n", info.Mtim().Time.Format(time.RFC3339))

    // 清理
    os.Remove("time_test.txt")
}
```

**专业词汇解释：**

- **Atime（Access Time）**：文件最后一次被读取的时间
- **Mtime（Modify Time）**：文件内容最后一次被修改的时间
- **Ctime（Change Time）**：文件元数据（权限、所有者等）最后一次改变的时间（在 Go 中不可直接修改）

## 16.30 os.Getwd、os.Chdir：获取和切换当前工作目录

**当前工作目录（Current Working Directory）** 是程序运行的"当前位置"基准点。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // Getwd：获取当前工作目录
    cwd, err := os.Getwd()
    if err != nil {
        panic(err)
    }
    fmt.Printf("当前目录: %s\n", cwd)

    // Chdir：切换当前工作目录
    originalDir := cwd

    // 切换到用户主目录
    homeDir, _ := os.UserHomeDir()
    err = os.Chdir(homeDir)
    if err != nil {
        panic(err)
    }

    newCwd, _ := os.Getwd()
    fmt.Printf("切换后目录: %s\n", newCwd)

    // 使用相对路径（相对于当前目录）
    os.WriteFile("relative_test.txt", []byte("在主目录创建"), 0644)
    fmt.Println("已在主目录创建文件")

    // 切回原目录
    os.Chdir(originalDir)
    fmt.Printf("切回原目录: %s\n", originalDir)

    // 清理
    os.Remove("relative_test.txt")
}
```

**路径解析示意：**

```
绝对路径：从根目录开始的完整路径
         /home/user/project/main.go
         ↑
         根目录

相对路径：从当前目录开始的路径
当前目录: /home/user
相对路径: project/main.go
完整路径: /home/user/project/main.go
```

## 16.31 os.Hostname：获取主机名

`Hostname` 返回计算机在网络中的 **名称**（也就是你在网络上被叫的名字）。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    hostname, err := os.Hostname()
    if err != nil {
        panic(err)
    }
    fmt.Printf("主机名: %s\n", hostname)

    // 主机名有什么用？
    // 1. 日志区分不同服务器
    // 2. 集群环境中标识节点
    // 3. 生成唯一的临时文件名（配合主机名更唯一）
}
```

## 16.32 os.IsExist、os.IsNotExist、os.IsPermission：判断错误类型

Go 的错误处理是 **值类型** 的，而 `os` 包贴心地提供了 **错误类型判断三剑客**。

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 场景 1：文件已存在
    os.WriteFile("test.txt", []byte("hello"), 0644)
    _, err := os.Create("test.txt") // 尝试创建已存在的文件

    if os.IsExist(err) {
        fmt.Println("错误原因：文件已存在")
    }

    // 场景 2：文件不存在
    _, err = os.Open("non_existent.txt")
    if os.IsNotExist(err) {
        fmt.Println("错误原因：文件不存在")
    }

    // 场景 3：权限不足
    // 注意：在某些 Unix 系统上，root 用户不会有权限问题
    _, err = os.Open("/root/protected.txt") // 尝试读 root 的文件
    if os.IsPermission(err) {
        fmt.Println("错误原因：权限不足")
    } else {
        fmt.Println("（可能是 root 用户或文件本身不存在）")
    }

    // 清理
    os.Remove("test.txt")
}
```

**三剑客的正确用法：**

```go
// ❌ 错误示例：字符串比较（脆弱）
if err.Error() == "file exists" { ... }

// ✅ 正确示例：使用 os 包提供的判断函数
if os.IsExist(err) { ... }
if os.IsNotExist(err) { ... }
if os.IsPermission(err) { ... }
```

**背后的原理**：Go 1.13+ 的 `errors.Is` 和 `errors.As` 函数配合 `os` 包的错误包装，使得这些判断函数能够正确处理嵌套错误。

## 16.33 exec.Command：创建命令对象

`exec` 包是 Go 调用 **外部命令** 的入口，而 `Command` 是创建命令对象的工厂函数。

```go
package main

import (
    "fmt"
    "os/exec"
)

func main() {
    // 最简单的用法：执行系统命令
    cmd := exec.Command("echo", "Hello from exec!")

    // Windows 用户请用：
    // cmd := exec.Command("cmd", "/c", "echo Hello from exec!")

    fmt.Printf("命令: %s\n", cmd.String())
    fmt.Printf("程序: %s\n", cmd.Path)
    fmt.Printf("参数: %v\n", cmd.Args)

    // 注意：Command 返回的是 *exec.Cmd，不是直接执行
    // 需要调用 Run/Start/Output 等方法才会真正执行
}
```

**Command 的参数说明：**

```go
// exec.Command(program, args...)
// program: 命令程序路径或名称
// args...: 命令行参数（不包括程序名本身）

// 示例对比 shell 命令
// shell: echo "Hello" "World"
// Go:
exec.Command("echo", "Hello", "World")

// shell: ls -la /tmp
// Go:
exec.Command("ls", "-la", "/tmp")

// shell: python script.py --config config.yaml
// Go:
exec.Command("python", "script.py", "--config", "config.yaml")
```

## 16.34 exec.Cmd.Run：执行命令并等待

`Run` 是最简单的执行方式——**启动命令，等待完成，返回结果**。一步到位，同步阻塞。

```go
package main

import (
    "fmt"
    "os/exec"
)

func main() {
    // 创建命令
    cmd := exec.Command("go", "version")

    // Run：执行并等待完成
    // 如果命令退出码非 0，会返回 *exec.ExitError
    err := cmd.Run()
    if err != nil {
        fmt.Printf("命令执行失败: %v\n", err)
        // Windows 上可能是：exec: "go": executable file not found in %PATH%
        return
    }

    fmt.Println("命令执行成功！")

    // Run 不返回输出，如果需要输出请用 Output
}
```

**Run 的特点：**

- **同步阻塞**：会一直等到命令执行完毕才返回
- **不返回输出**：标准输出/标准错误直接传给父进程（你的终端）
- **退出码非 0**：会返回错误，可通过 `os/exec.ExitError` 获取更多信息

## 16.35 exec.Cmd.Start：启动命令，后台执行

`Start` 让你 **启动命令但不等待**，像启动一个后台任务一样。

```go
package main

import (
    "fmt"
    "os/exec"
    "time"
)

func main() {
    // 启动一个耗时命令
    cmd := exec.Command("sleep", "5") // 睡眠 5 秒

    fmt.Println("启动命令...")
    err := cmd.Start()
    if err != nil {
        panic(err)
    }

    fmt.Println("命令正在后台运行，我可以做其他事情！")

    // 模拟做其他事情
    for i := 1; i <= 3; i++ {
        fmt.Printf("我在处理任务 %d...\n", i)
        time.Sleep(1 * time.Second)
    }

    // 等待命令完成
    fmt.Println("等待命令结束...")
    err = cmd.Wait() // 这会阻塞直到命令完成
    fmt.Printf("命令结束了，错误: %v\n", err)
}
```

**Start + Wait 的组合让你：**

- 在命令执行期间 **并行做其他事情**
- 精确控制 **何时开始等待**
- 更灵活的 **任务管理**

## 16.36 exec.Cmd.Wait：等待命令完成

`Wait` 配合 `Start` 使用，等待命令 **完全退出** 并回收资源。

```go
package main

import (
    "fmt"
    "os/exec"
    "time"
)

func main() {
    cmd := exec.Command("bash", "-c", "echo 开始; sleep 2; echo 结束")

    err := cmd.Start()
    if err != nil {
        panic(err)
    }

    fmt.Println("等待命令完成...")

    // Wait 会阻塞直到进程退出
    err = cmd.Wait()

    if err != nil {
        fmt.Printf("命令退出状态: %v\n", err)
    } else {
        fmt.Println("命令正常退出")
    }

    // 注意：Wait 会消耗进程资源，必须在 Start 之后调用
    // 每个 Start 都应该有对应的 Wait
}
```

**Wait 的职责：**

1. **阻塞等待**进程退出
2. **回收进程**（防止僵尸进程）
3. **返回退出信息**（退出码、是否被信号终止等）

## 16.37 exec.Cmd.Output：执行命令并获取输出（stdout）

`Output` 是 `Run` 的升级版——执行命令并捕获 **标准输出**。

```go
package main

import (
    "fmt"
    "os/exec"
)

func main() {
    // 执行命令并获取输出
    cmd := exec.Command("go", "version")

    // Output 执行命令并返回标准输出
    output, err := cmd.Output()
    if err != nil {
        panic(err)
    }

    fmt.Printf("命令输出:\n%s", string(output))

    // Windows 示例
    cmd2 := exec.Command("cmd", "/c", "echo Hello && echo World")
    output2, _ := cmd2.Output()
    fmt.Printf("Windows 命令输出: %s", string(output2))
}
```

**Output vs Run：**

```go
// Run：不捕获输出，输出直接打印到终端
cmd := exec.Command("echo", "Hello")
cmd.Run() // 你会在终端看到 "Hello"

// Output：捕获输出，返回 []byte
cmd := exec.Command("echo", "Hello")
output, _ := cmd.Output()
fmt.Println(string(output)) // 程序自己打印 "Hello"
```

## 16.38 exec.Cmd.CombinedOutput：执行命令并获取输出（stdout+stderr）

`CombinedOutput` 捕获 **标准输出 + 标准错误** 的合并内容。

```go
package main

import (
    "fmt"
    "os/exec"
)

func main() {
    // 创建一个会同时输出 stdout 和 stderr 的命令
    cmd := exec.Command("bash", "-c", "echo 标准输出; echo 标准错误 >&2")

    // CombinedOutput 合并两者
    output, err := cmd.CombinedOutput()
    if err != nil {
        fmt.Printf("错误: %v\n", err)
    }

    fmt.Printf("合并输出:\n%s", string(output))
    // 输出可能类似：
    // 标准输出
    // 标准错误

    // 实际测试
    cmd2 := exec.Command("cmd", "/c", "dir nonexistent && echo 这不会执行")
    output2, err := cmd2.CombinedOutput()
    fmt.Printf("Windows 错误输出: %s\n错误: %v\n", string(output2), err)
}
```

**什么时候用 CombinedOutput：**

- 当你不关心 stdout 和 stderr 的区分时
- 当你需要完整捕获所有输出时
- 调试时查看完整的命令输出

## 16.39 exec.Cmd.Stdin、Stdout、Stderr：重定向标准输入输出

通过设置 `Cmd` 的 `Stdin`、`Stdout`、`Stderr` 字段，你可以 **完全控制命令的输入输出**。

```go
package main

import (
    "bytes"
    "fmt"
    "os/exec"
    "strings"
)

func main() {
    // 示例 1：自定义标准输入
    cmd := exec.Command("cat")
    cmd.Stdin = strings.NewReader("这是通过 stdin 输入的内容\n")
    output, _ := cmd.Output()
    fmt.Printf("cat 输出: %s", string(output))

    // 示例 2：自定义标准输出（写入 buffer）
    var stdout bytes.Buffer
    cmd2 := exec.Command("echo", "写入自定义 stdout")
    cmd2.Stdout = &stdout
    cmd2.Run()
    fmt.Printf("捕获到: %s", stdout.String())

    // 示例 3：同时重定向 stdout 和 stderr 到不同的 writer
    var stderr bytes.Buffer
    cmd3 := exec.Command("bash", "-c", "echo stdout; echo stderr >&2")
    cmd3.Stdout = &stdout
    cmd3.Stderr = &stderr
    cmd3.Run()
    fmt.Printf("stdout: %s", stdout.String())
    fmt.Printf("stderr: %s", stderr.String())

    // 示例 4：将命令输出重定向到文件
    outputFile, _ := os.Create("command_output.txt")
    defer outputFile.Close()
    cmd4 := exec.Command("ls", "-la")
    cmd4.Stdout = outputFile
    cmd4.Run()
    fmt.Println("输出已写入文件")
}
```

**常用的 io.Writer 和 io.Reader：**

| 类型 | 用途 | 示例 |
|------|------|------|
| `*bytes.Buffer` | 捕获到内存 | `var buf bytes.Buffer; cmd.Stdout = &buf` |
| `*os.File` | 写入文件 | `cmd.Stdout = file` |
| `os.Stdout` | 输出到终端 | `cmd.Stdout = os.Stdout` |
| `os.Stderr` | 输出到错误流 | `cmd.Stderr = os.Stderr` |
| `nil` | 丢弃输出 | `cmd.Stdout = nil` |

## 16.40 exec.CommandContext：支持超时的命令执行

`CommandContext` 是 `Command` 的 **上下文感知版**，支持超时和取消。

```go
package main

import (
    "context"
    "fmt"
    "os/exec"
    "time"
)

func main() {
    // 创建带超时的上下文
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    // 使用 CommandContext 创建命令
    cmd := exec.CommandContext(ctx, "sleep", "10") // 睡眠 10 秒

    fmt.Println("启动命令（2秒后超时）...")

    // 执行命令
    err := cmd.Run()

    // 检查是否是超时错误
    if ctx.Err() == context.DeadlineExceeded {
        fmt.Println("⏰ 命令超时了！")
    } else if err != nil {
        fmt.Printf("命令执行出错: %v\n", err)
    } else {
        fmt.Println("命令正常完成")
    }
}
```

**超时执行流程：**

```
时间线:
0s        1s        2s        3s        10s
|----------|----------|----------|----------|
   Start()
              超时触发!
                 ↓
              ctx.DeadlineExceeded
                 ↓
              命令被 Kill
```

**CommandContext 的优势：**

1. **超时控制**：防止命令无限挂起
2. **优雅取消**：发送 SIGKILL/SIGTERM 终止进程
3. **级联取消**：父 context 取消时自动取消子命令

## 16.41 exec.Lookup：查找可执行文件路径

`LookPath`（不是 Lookup）是 `exec` 包提供的查找可执行文件路径的函数。

```go
package main

import (
    "fmt"
    "os/exec"
    "path/filepath"
)

func main() {
    // LookPath：在 PATH 环境变量中查找可执行文件
    path, err := exec.LookPath("go")
    if err != nil {
        fmt.Printf("找不到 go: %v\n", err)
        return
    }
    fmt.Printf("go 的路径: %s\n", path)

    // 也可以用于检查命令是否存在
    commands := []string{"go", "python", "node", "nonexistent_command"}
    for _, cmd := range commands {
        if fullPath, err := exec.LookPath(cmd); err == nil {
            fmt.Printf("✓ %s: %s\n", cmd, fullPath)
        } else {
            fmt.Printf("✗ %s: 未找到\n", cmd)
        }
    }

    // LookPath 还会解析符号链接
    // 它会返回真实路径而不是符号链接本身

    // 实战：确保命令存在再执行
    if path, err := exec.LookPath("git"); err == nil {
        fmt.Printf("找到 git: %s\n", path)
        // cmd := exec.Command(path, "status")
        // ...
    }
}
```

**LookupPath 的查找逻辑：**

1. 如果路径已包含 `/` 或 `\`，直接检查是否是文件
2. 否则在 `PATH` 环境变量的各目录中依次查找
3. 找到第一个匹配的可执行文件即返回

## 16.42 signal.Notify：注册信号处理器

信号（Signal）是操作系统发送给进程的通知，`signal.Notify` 让你 **拦截并处理** 这些信号。

```go
package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    // 创建一个用于接收信号的 channel
    sigChan := make(chan os.Signal, 1)

    // Notify：注册要监听的信号
    // 常见信号：
    // - syscall.SIGINT  (Ctrl+C)
    // - syscall.SIGTERM (优雅终止请求)
    // - syscall.SIGHUP  (终端挂起，常用于配置重载)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

    fmt.Println("程序运行中，按 Ctrl+C 发送 SIGINT，或等 5 秒自动退出...")

    // 等待信号
    sig := <-sigChan
    fmt.Printf("收到信号: %v\n", sig)

    // 根据信号类型做不同处理
    switch sig {
    case syscall.SIGINT:
        fmt.Println("收到 Ctrl+C，开始优雅关闭...")
        // 清理资源、关闭连接、保存状态...
    case syscall.SIGTERM:
        fmt.Println("收到终止请求，开始关闭...")
    }

    fmt.Println("程序退出")
}
```

**常见信号速查表：**

| 信号 | 值 | 含义 | 触发场景 |
|------|-----|------|----------|
| `SIGINT` | 2 | 中断 | Ctrl+C |
| `SIGTERM` | 15 | 终止 | `kill`（默认） |
| `SIGHUP` | 1 | 挂起 | 终端关闭、配置重载 |
| `SIGKILL` | 9 | 强制终止 | `kill -9`（不可捕获） |
| `SIGUSR1/2` | 10/12 | 用户自定义 | 应用自定义 |

## 16.43 signal.Ignore：忽略信号

`Ignore` 让指定信号 **完全被忽略**，进程假装什么都没发生。

```go
package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    // 忽略 SIGINT（Ctrl+C）
    signal.Ignore(syscall.SIGINT)

    fmt.Println("SIGINT 已被忽略，Ctrl+C 现在无效！")
    fmt.Println("5 秒后程序将正常退出...")

    // 这段代码里 Ctrl+C 完全无效
    for i := 5; i > 0; i-- {
        fmt.Printf("%d...\n", i)
        time.Sleep(1 * time.Second)
    }

    fmt.Println("程序结束")
}
```

> ⚠️ **注意**：`SIGKILL` 和 `SIGSTOP` 是无法忽略的——这是内核级别的硬性规定，Go 也没办法。

## 16.44 signal.Reset：重置信号处理到默认行为

`Reset` 撤销 `Notify` 和 `Ignore` 的效果，将信号处理 **恢复到系统默认值**。

```go
package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    sigChan := make(chan os.Signal, 1)

    // 先忽略 SIGINT
    signal.Ignore(syscall.SIGINT)
    fmt.Println("SIGINT 被忽略中...")

    // 模拟一段时间后恢复默认行为
    fmt.Println("3 秒后将恢复 SIGINT 默认行为...")

    // 重置 SIGINT 到默认处理
    signal.Reset(syscall.SIGINT)

    fmt.Println("SIGINT 已恢复默认！现在可以注册新的处理...")

    // 重新注册（此时 Notify 生效）
    signal.Notify(sigChan, syscall.SIGINT)

    fmt.Println("按 Ctrl+C 触发新的处理...")

    // 等待信号
    sig := <-sigChan
    fmt.Printf("收到信号 %v，程序退出\n", sig)
}
```

**信号处理状态图：**

```
Signal Notify:
默认行为 ──注册──> 自定义处理 ──Reset──> 默认行为

Signal Ignore:
默认行为 ──Ignore──> 忽略 ──Reset──> 默认行为
```

## 16.45 signal.NotifyContext：基于信号的 Context 取消

`NotifyContext` 是 Go 1.14+ 的新功能，将 **信号转换为 Context 取消**，让你能用 `select` 同时监听多个取消源。

```go
package main

import (
    "context"
    "fmt"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    // 创建基于信号的 Context
    // 当收到 SIGINT 或 SIGTERM 时，Context 会被取消
    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stop() // 在程序结束时停止信号监听

    fmt.Println("程序运行中，等待信号或超时...")

    // 使用 select 监听多个取消源
    select {
    case <-ctx.Done():
        fmt.Printf("Context 取消: %v\n", ctx.Err())
        // 通常是 syscall.SIGINT 或 syscall.SIGTERM
    case <-time.After(10 * time.Second):
        fmt.Println("10 秒超时，程序结束")
    }

    fmt.Println("清理并退出...")
}
```

**NotifyContext 的优势：**

```go
// ❌ 传统方式：分散的信号处理
sigChan := make(chan os.Signal, 1)
signal.Notify(sigChan, syscall.SIGINT)
// 然后需要在不同地方检查 sigChan

// ✅ NotifyContext 方式：统一的取消机制
ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT)
// 可以在任何支持 Context 的地方监听取消
```

## 16.46 user.Current：获取当前用户

`user.Current` 返回 **当前进程的用户信息**。

```go
package main

import (
    "fmt"
    "os/user"
)

func main() {
    // 获取当前用户
    currentUser, err := user.Current()
    if err != nil {
        panic(err)
    }

    fmt.Printf("用户名: %s\n", currentUser.Username)
    fmt.Printf("用户ID: %s\n", currentUser.Uid)
    fmt.Printf("主组ID: %s\n", currentUser.Gid)
    fmt.Printf("主目录: %s\n", currentUser.HomeDir)
    fmt.Printf("登录Shell: %s\n", currentUser.Name) // 在 Unix 上是 GECOS 字段（用户全名）

    // 注意：Windows 上的字段含义可能不同
    // Windows 上 Username 是 "DOMAIN\\user" 格式
}
```

**返回值 `User` 的字段：**

| 字段 | Linux/macOS | Windows |
|------|-------------|---------|
| `Username` | 登录名 | 用户名或 DOMAIN\\user |
| `Uid` | 用户 ID (string) | 无意义 |
| `Gid` | 主组 ID (string) | 无意义 |
| `HomeDir` | 主目录路径 | 用户目录 |
| `Name` | GECOS 字段（通常是真名） | 同 Username |

## 16.47 user.Lookup：根据用户名查询用户信息

`Lookup` 根据 **用户名** 查询用户信息。

```go
package main

import (
    "fmt"
    "os/user"
)

func main() {
    // 查询 root 用户（Unix 系统）
    rootUser, err := user.Lookup("root")
    if err != nil {
        fmt.Printf("查找 root 用户失败: %v\n", err)
        return
    }

    fmt.Printf("root 用户信息:\n")
    fmt.Printf("  用户名: %s\n", rootUser.Username)
    fmt.Printf("  UID: %s\n", rootUser.Uid)
    fmt.Printf("  GID: %s\n", rootUser.Gid)
    fmt.Printf("  主目录: %s\n", rootUser.HomeDir)
    fmt.Printf("  用户全名: %s\n", rootUser.Name)

    // 查找当前用户
    currentUser, _ := user.Current()
    lookupUser, err := user.Lookup(currentUser.Username)
    if err == nil {
        fmt.Printf("\n验证当前用户: %s\n", lookupUser.Username)
    }
}
```

**Lookup vs Current：**

```go
// Current：获取当前进程的实际用户（快，直接读取 /etc/passwd 或系统 API）
user.Current()

// Lookup：根据用户名查询（可能触发 NSS 查找，如 LDAP、NIS 等）
user.Lookup("someuser")
```

## 16.48 user.LookupId：根据 UID 查询用户信息

`LookupId` 根据 **UID** 查询用户信息，作用和 `Lookup` 一样，只是用 ID 而不是名字。

```go
package main

import (
    "fmt"
    "os/user"
)

func main() {
    // 获取当前用户
    current, _ := user.Current()
    fmt.Printf("当前用户: %s (UID: %s)\n", current.Username, current.Uid)

    // 根据 UID 查询
    // UID 0 是 root
    root, err := user.LookupId("0")
    if err != nil {
        fmt.Printf("查找 UID 0 失败: %v\n", err)
        return
    }
    fmt.Printf("UID 0 对应的用户: %s\n", root.Username)

    // 根据当前用户 UID 查询
    sameUser, err := user.LookupId(current.Uid)
    if err != nil {
        panic(err)
    }
    fmt.Printf("UID %s = %s\n", current.Uid, sameUser.Username)

    // 常用 UID 参考
    uidMap := map[string]string{
        "0":   "root（超级管理员）",
        "1":   "daemon（系统守护进程）",
        "33":  "www-data（Web 服务器）",
        "1000": "第一个普通用户（通常）",
    }
    fmt.Println("\n常见 UID：")
    for uid, desc := range uidMap {
        if u, err := user.LookupId(uid); err == nil {
            fmt.Printf("  UID %s: %s (%s)\n", uid, u.Username, desc)
        }
    }
}
```

## 16.49 user.GroupIds：获取用户所属的组 ID 列表

`GroupIds` 返回用户所属的 **所有组 ID**，因为一个用户可以同时属于多个组。

```go
package main

import (
    "fmt"
    "os/user"
)

func main() {
    // 获取当前用户
    currentUser, err := user.Current()
    if err != nil {
        panic(err)
    }

    fmt.Printf("用户 %s 的组信息:\n", currentUser.Username)

    // 获取所有组 ID
    groupIds, err := currentUser.GroupIds()
    if err != nil {
        panic(err)
    }

    fmt.Printf("所属组 ID 数量: %d\n", len(groupIds))
    fmt.Printf("组 ID 列表: %v\n", groupIds)

    // 解析每个组 ID 获取组名
    for _, gid := range groupIds {
        // 根据 GID 查找组名
        // 这需要用到系统调用，这里仅展示概念
        fmt.Printf("  组 ID %s\n", gid)
    }

    // 实战：检查用户是否属于某个组
    func belongsToGroup(username, groupName string) bool {
        u, err := user.Lookup(username)
        if err != nil {
            return false
        }
        groups, _ := u.GroupIds()
        // 简化实现，实际应该查 /etc/group 或调用 getgrouplist
        for _, gid := range groups {
            g, err := user.LookupGroupId(gid)
            if err == nil && g.Name == groupName {
                return true
            }
        }
        return false
    }

    // 测试
    fmt.Printf("\n当前用户属于 sudo 组: %t\n",
        belongsToGroup(currentUser.Username, "sudo"))
}
```

**组 ID 的作用：**

- **权限继承**：文件属于某个组时，组内成员默认有权限访问
- **资源隔离**：不同组可以访问不同资源
- **协作共享**：同一项目组成员放同一组，共享文件权限

---

## 本章小结

本章我们深入探索了 Go 标准库中与 **操作系统交互** 的四大金刚：

### 📁 文件操作（os 包 + io）

| 函数/方法 | 作用 | 注意事项 |
|-----------|------|----------|
| `os.Create` | 创建或截断文件 | 会清空已有内容 |
| `os.Open` | 只读打开 | 文件不存在会报错 |
| `os.OpenFile` | 通用打开方式 | 配合 flags 使用 |
| `file.Read/ReadAt` | 读取文件 | Read 移动指针，ReadAt 不移动 |
| `file.Write/WriteAt` | 写入文件 | Write 移动指针，WriteAt 不移动 |
| `file.Seek` | 移动文件指针 | 三种模式 SEEK_SET/CUR/END |
| `file.Sync` | 强制刷盘 | 有性能开销，慎用 |
| `file.Truncate` | 截断文件 | 可增可减 |
| `file.Close` | 关闭文件 | **必须调用！** |
| `file.Stat` | 获取元信息 | 会跟随符号链接 |
| `file.Lstat` | 获取元信息 | 不跟随符号链接 |

### 📂 目录操作

| 函数 | 作用 |
|------|------|
| `os.Mkdir` | 创建单级目录 |
| `os.MkdirAll` | 创建多级目录（递归） |
| `os.Remove` | 删除文件或空目录 |
| `os.RemoveAll` | 递归删除目录树 |
| `os.Rename` | 重命名或移动 |
| `os.WalkDir` | 遍历目录树 |
| `os.CreateTemp` | 创建临时文件 |
| `os.MkdirTemp` | 创建临时目录 |
| `os.TempDir` | 获取临时目录路径 |

### 🎭 文件元数据

| 函数 | 作用 |
|------|------|
| `os.Chmod/Chown` | 修改权限/所有者 |
| `os.Chtimes` | 修改时间戳 |
| `os.Getwd/Chdir` | 获取/切换工作目录 |
| `os.Hostname` | 获取主机名 |
| `os.Mode` | 文件类型与权限位 |
| `os.IsExist/IsNotExist/IsPermission` | 错误类型判断 |

### 🚀 执行外部命令（exec 包）

| 函数/方法 | 作用 |
|-----------|------|
| `exec.Command` | 创建命令对象 |
| `cmd.Run` | 同步执行并等待 |
| `cmd.Start` | 启动（不等待） |
| `cmd.Wait` | 等待命令完成 |
| `cmd.Output` | 获取 stdout |
| `cmd.CombinedOutput` | 获取 stdout+stderr |
| `cmd.Stdin/Stdout/Stderr` | 重定向 IO |
| `exec.CommandContext` | 支持超时的命令 |

### 📡 信号处理（signal 包）

| 函数 | 作用 |
|------|------|
| `signal.Notify` | 注册信号处理器 |
| `signal.Ignore` | 忽略信号 |
| `signal.Reset` | 恢复默认行为 |
| `signal.NotifyContext` | 信号转 Context |

### 👤 用户管理（user 包）

| 函数 | 作用 |
|------|------|
| `user.Current` | 获取当前用户 |
| `user.Lookup` | 根据用户名查询 |
| `user.LookupId` | 根据 UID 查询 |
| `user.GroupIds` | 获取用户组 ID 列表 |

---

> 🎯 **最佳实践总结**：
> 1. **文件用完必关**：`defer file.Close()` 是你的好朋友
> 2. **错误要判断**：使用 `os.IsExist`、`os.IsNotExist` 等判断错误类型
> 3. **临时文件要清理**：使用 `defer os.Remove()` 或 `defer os.RemoveAll()`
> 4. **跨平台注意**：Windows 上的符号链接、权限、用户组等行为与 Unix 不同
> 5. **Context 是未来**：需要超时控制时用 `CommandContext`

掌握了这些，你就是 Go 程序里的 **"系统全能王"**！操作系统在你面前就是一本打开的书，想读就读，想写就写，想命令就命令。🎉
