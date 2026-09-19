+++
title = "第35章 调试与性能：断言、日志与优化属性"
weight = 350
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十五章：调试与性能：断言、日志与优化属性

> 程序不按预期工作时，最没用的做法是到处 `print` 然后凭感觉猜。有效的调试靠分层证据：断言守住内部不变量，日志记录关键路径，断点检查运行状态，性能工具给出具体数字。先测量，再优化。

## 35.1 断言：让错误尽早出现

`assert` 是写给“未来的自己”看的检查：条件不成立就当场停下，而且只在调试构建里保留。

```swift
func average(_ values: [Int]) -> Double {
    assert(!values.isEmpty, "平均值不能对空数组调用")
    return Double(values.reduce(0, +)) / Double(values.count)
}

print(average([1, 2, 3]))
// prints: 2.0
```

`assert` 只在调试构建生效，适合内部一致性检查。`precondition` 在调试和发布构建都生效，适合调用方必须遵守的约束：

```swift
func index(_ values: [Int], at index: Int) -> Int {
    precondition(values.indices.contains(index), "索引越界")
    return values[index]
}
```

`fatalError` 表示程序进入不可恢复状态。断言不是用户输入校验；用户输入应该通过 `throws`、可选值或返回错误处理。

三个函数各有一个“立刻触发”的兄弟版本，专门用在 `guard`、`switch` 这类必须结束控制流的场合——它们返回 `Never`，所以编译器知道后面的代码不可达：

```swift
func load(_ name: String) -> Int {
    guard !name.isEmpty else {
        preconditionFailure("名字不能为空")
    }
    return name.count
}

print(load("swift"))
// prints: 5
```

对照关系很简单：`assert` 对应 `assertionFailure`，`precondition` 对应 `preconditionFailure`，`fatalError` 本身就是 `Never`。

## 35.2 编译期位置信息

Swift 提供常用字面量：

| 字面量 | 内容 |
| --- | --- |
| `#file` | 当前文件完整路径 |
| `#fileID` | 模块名与文件名 |
| `#line` | 当前行号 |
| `#column` | 当前列号 |
| `#function` | 当前函数名 |

日志函数可以接收这些信息并设置默认值：

```swift
func log(_ message: String, file: String = #fileID, line: Int = #line) {
    print("\(file):\(line) \(message)")
}

log("开始加载")
// 输出形如：Chapter35-Debugging-and-Performance.swift:15 开始加载
```

实际输出中的文件和行号由调用位置决定。默认参数让调用者不需要手动传这些信息。

## 35.3 日志与 `os.Logger`

打印适合临时排查，正式应用通常使用 `Logger`：

```swift
import os

let logger = Logger(subsystem: "com.example.app", category: "network")
logger.info("开始请求")
logger.error("请求失败")
```

日志有级别、分类和隐私控制。不要把密码、令牌、完整用户数据直接写进日志；既有安全风险，也会让日志体积失控。

## 35.4 断点与调试器

断点比 `print` 更适合检查运行时状态：

- 在可疑行暂停，查看变量、调用栈和线程。
- 设置条件断点，只在特定输入下暂停。
- 使用异常断点，在错误抛出的第一时间停下。
- 使用符号断点定位某个方法何时被调用。

调试并发问题时，调用栈和任务状态比单线程时期更复杂。先记录隔离域、任务和 actor，再判断是逻辑错误还是数据竞争。

## 35.5 计时与性能度量

最基础的计时方式是 `ContinuousClock`：

```swift
import Foundation

let clock = ContinuousClock()
let elapsed = clock.measure {
    _ = (0..<100_000).reduce(0, +)
}
print(elapsed > .zero)
// prints: true
```

`measure` 适合粗粒度比较；真正的性能分析应使用 Instruments、`xctrace`、Swift Package 的性能测试和系统级采样工具。关注 CPU、内存分配、系统调用、锁竞争和 I/O，而不是只盯着一行代码。

内存开销同样可以量化。`MemoryLayout` 在编译期给出类型的实际布局，调优大数组或自定义存储时很有用：

```swift
print(MemoryLayout<Int>.size, MemoryLayout<Int>.stride)
// prints: 8 8
print(MemoryLayout<Bool>.size, MemoryLayout<Bool>.stride)
// prints: 1 1
```

`size` 是类型自身占用的字节数，`stride` 是数组里相邻元素的间距——两者不同，说明存在对齐填充。想减少内存占用时，先看 `stride`，再看是否需要换更紧凑的表示。

## 35.6 优化属性

Swift 提供若干编译优化标记：

| 属性 | 作用 | 使用建议 |
| --- | --- | --- |
| `@inline(always)` | 要求内联，SIL 里是 `[always_inline]` | 仅热路径、极小函数；类方法必须同时是 `final` |
| `@inline(__always)` | 历史上更早的写法，倾向于内联但不强制（`[heuristic_always_inline]`） | 需要兼容旧工具链时用 |
| `@inline(never)` | 禁止内联 | 调试、控制代码体积 |
| `@inlinable` | 允许跨模块内联 | 公共库热路径，需谨慎暴露实现 |
| `@specialize` | 针对特定类型优化 | 泛型热路径 |
| `@export(interface)` | 导出接口信息 | 跨模块优化与 ABI 场景 |

不要在业务代码里到处写这些属性。先测量，确认瓶颈，再用最窄的标记改进。错误的优化会让二进制变大、编译变慢，甚至让性能更差。

两个容易踩的点各有各的报错方式。`@inline(always)` 只能用在**静态派发**的位置（`final` 方法、`static` 方法、扩展里的方法），放在可被重写的类方法上会直接报错：

```text
error: '@inline(always)' on class methods requires 'f()' to be marked 'final'
```

而 `@inlinable` 会把函数体写进模块接口，所以它引用的其他符号也必须够“公开”——内部细节要用 `@usableFromInline` 标出来，否则报错 `'helper()' is internal and cannot be referenced from an '@inlinable' function`。换句话说，`@inlinable` 是在**承诺**：这段实现要作为 API 的一部分长期存在。

## 35.7 构建配置与性能

调试构建为了便于调试，会关闭大量优化；发布构建才接近真实性能：

```bash
swift build -c release
```

还可以使用全模块优化和更激进的优化选项，但要通过基准测试验证收益。性能测试要固定硬件、系统版本、构建配置和后台负载，否则数字只是在测天气。

## 35.8 本章小结

| 工具 | 用途 |
| --- | --- |
| `assert` | 调试构建中的内部不变量 |
| `precondition` | 所有构建中的调用约束 |
| `#fileID` 等 | 记录源码位置 |
| `Logger` | 分级、分类的结构化日志 |
| 断点 | 检查运行时状态和调用栈 |
| `measure` | 粗粒度耗时测量 |
| 优化属性 | 针对热路径的编译优化 |
| Release 构建 | 接近真实性能的构建模式 |

## 35.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 用断言校验用户输入 | 用户输入应该可恢复地处理 |
| 依赖 `assert` 在发布构建生效 | 它会被移除 |
| 用 `print` 记录长期日志 | 正式项目应使用日志系统 |
| 不测量就加优化属性 | 先找瓶颈，再优化 |
| 在调试构建比较性能 | 优化级别不同，结果不可比 |
| 只看平均耗时 | 还要看尾延迟、内存和分配 |

## 35.10 下章预告

第五篇结束。第六篇开始动手：先做一个命令行工具，再进入 SwiftUI、综合项目和服务端 Swift。语法知识到这里会真正变成可运行的作品。
