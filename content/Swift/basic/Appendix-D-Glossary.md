+++
title = "附录D 术语表"
weight = 1030
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录D：术语表

> 术语不是用来吓人的，而是用来在一句话里准确表达复杂概念。遇到不熟的词，回到这里快速定位章节。

| 术语 | 含义 | 章节 |
| --- | --- | --- |
| ARC | 自动引用计数，管理类实例生命周期 | 第27章 |
| actor | 串行保护隔离状态的引用类型 | 第31章 |
| actor isolation | 隔离域，actor 内部状态的访问边界 | 第31章 |
| associatedtype | 协议中的关联类型 | 第22章 |
| async/await | 异步函数与等待语法 | 第30章 |
| autoclosure | 自动把表达式包成闭包 | 第14章 |
| BinaryInteger | 定长与不定长整数共同的协议族上层 | 第49章 |
| BOM | 字节顺序标记（U+FEFF）；出现在 UTF-8 源文件开头时被编译器忽略 | 第2章 |
| borrowing | 只借入不消耗参数的所有权修饰 | 第29章 |
| COW | 写时复制，修改时才分离共享存储 | 第27章 |
| Collection | 可重复遍历、有下标与 `count` 的序列协议 | 第48章 |
| capture list | 闭包捕获列表，控制捕获方式 | 第14、28章 |
| consuming | 把参数所有权交给被调函数 | 第29章 |
| CustomStringConvertible | 让类型决定 `description`，即 `"\(value)"` 的输出 | 第52章 |
| CustomDebugStringConvertible | 决定 `debugDescription`，即 `String(reflecting:)` 的输出 | 第52章 |
| Decimal | 十进制浮点数，用于金额等不能有二进制舍入误差的场景 | 第49章 |
| dump | 走反射把值打印成树，与 `print` 不同 | 第52章 |
| escape | 闭包或值逃离当前生命周期，见 `@escaping` | 第14、29章 |
| existential type | 存在类型，即 `any P` | 第22、24章 |
| escaping | 逃逸闭包，调用返回后仍存活 | 第14章 |
| FixedWidthInteger | 有固定位宽的整数协议，提供 `&+`、溢出检查等 | 第49章 |
| FormatStyle | 数字、货币、百分比、日期的格式化配置类型 | 第49章 |
| identifier | 标识符；可用中文与 emoji，但不做 Unicode 规范化 | 第2章 |
| IteratorProtocol | 迭代器协议，`for ... in` 真正调用的那一层 | 第48章 |
| key path | 键路径，把属性访问变成值（可当单参数函数使用） | 第15B、24章 |
| lazy 视图 | 把 `map`、`filter` 串成一条链、按需计算的视图，不缓存结果 | 第48、51章 |
| literal | 字面量，如 `42`、`"hi"`，由 `ExpressibleBy…Literal` 协议支撑 | 第15B、24章 |
| LosslessStringConvertible | 能从字符串无损还原成值的协议 | 第52章 |
| macro | 编译期展开的代码生成器，分自由宏与附着宏 | 第26章 |
| MainActor | 代表主线程的全局 actor，UI 代码的默认舞台 | 第31章 |
| Measurement | 带单位的量，如 5 km、30 °C | 第49章 |
| MemoryLayout | 查询类型的 `size` / `stride` / `alignment` 与字段偏移 | 第52章 |
| metatype | 元类型，`Int.self` 这类“类型的值” | 第24章 |
| Mirror | 只读反射工具，用于查看值的结构 | 第24、52章 |
| noncopyable | 不可复制类型，写作 `~Copyable` | 第29章 |
| Numeric | 支持四则运算的数值协议族根节点 | 第49章 |
| opaque type | 不透明类型，如 `some P` | 第22、23章 |
| ownership | 所有权，值的转移与借用规则 | 第29章 |
| pattern matching | 模式匹配，`switch` 的核心 | 第12章 |
| property wrapper | 属性包装器 | 第19章 |
| RandomAccessCollection | 能在 O(1) 内跳到任意位置的集合协议 | 第48章 |
| reduce(into:) | 把序列累积进一个可变容器，避免写时复制开销 | 第51章 |
| result builder | 结果构建器，DSL 里的声明式代码块；`@ViewBuilder` 是最出名的实例 | 第15B、22章 |
| Sendable | 可安全跨隔离域传递的标记 | 第31章 |
| Sequence | 能按顺序遍历一次的协议，`map` / `filter` 的落脚点 | 第48章 |
| source encoding | 源文件编码；Swift 只接受 UTF-8 | 第2章 |
| Span | 不拥有内存的连续元素视图 | 第29章 |
| stride | 生成等差数列的全局函数；`to:` 不含终点，`through:` 含 | 第51章 |
| structured concurrency | 结构化并发，父子任务的生命周期绑定 | 第30章 |
| sugar | 语法糖；写法更短但语义不变，如 `[Int]`、`if let x` | 第15B章 |
| task group | 任务组，动态派发并等待一组子任务 | 第30章 |
| tuple | 元组，临时组合多个值 | 第8章 |
| typed throws | 类型化抛出，写作 `throws(E)` | 第15章 |
| value semantics | 值语义，复制后互不影响 | 第17章 |
| view builder (`@ViewBuilder`) | SwiftUI 提供的结果构建器，让块里能写 `if`、`switch`、`ForEach` | 第15B.18节、第37章 |
| weak / unowned | 弱引用与无主引用，用来打断循环引用 | 第28章 |
| zip | 把两个序列配对成元组，以短的为准 | 第51章 |

补充几条容易混在一起的：

| 术语 | 含义 | 章节 |
| --- | --- | --- |
| implicit member | 隐式成员表达式，上下文已知类型时可写 `.red` | 第15B章 |
| if/switch expression | 表达式化的 `if` / `switch`，分支产出值（没有 `do` 表达式） | 第11、12、15B章 |
| callAsFunction | 让实例可以像函数一样被调用 | 第15B、24章 |
| trailing closure | 尾随闭包，把最后一个闭包参数移到圆括号外 | 第14、15B章 |

## D.1 中英对照速查

读完中文教程去翻官方文档时，最容易卡住的不是语法，而是“这个中文词在英文资料里叫什么”。这张表按概念归类，方便在官方文档里直接搜索：

| 中文 | 英文关键词 | 常出现在哪里 |
| --- | --- | --- |
| 可选值 / 解包 | optional, unwrap, force unwrap | TSPL「Optional Chaining」 |
| 可选绑定 | optional binding, `if let` | TSPL「Optional Binding」 |
| 值类型 / 引用类型 | value type, reference type | TSPL「Structures and Classes」 |
| 写时复制 | copy-on-write | 标准库文档、性能话题 |
| 所有权 / 借用 | ownership, borrow, consume | SE-0377、SE-0390 |
| 隔离域 / 参与者 | isolation, actor | Swift Concurrency 文档 |
| 结构化并发 | structured concurrency | Swift Concurrency 文档 |
| 逃逸闭包 | escaping closure, `@escaping` | TSPL「Closures」 |
| 属性包装器 | property wrapper | SE-0258 |
| 结果构建器 | result builder | SE-0289 |
| 视图构建器 | view builder, `@ViewBuilder` | SE-0289 与 SwiftUI 文档 |
| 不透明类型 / 存在类型 | opaque type, existential type | SE-0244、SE-0335 |
| 类型擦除 | type erasure | 泛型与协议话题 |
| 自由宏 / 附着宏 | freestanding macro, attached macro | Swift Macros 文档 |
| 序列 / 迭代器 | sequence, iterator | 标准库 `Sequence` / `IteratorProtocol` |
| 惰性求值 | lazy evaluation, lazy view | 标准库 `LazySequence` |
| 整数协议族 | integer protocols | `BinaryInteger`、`FixedWidthInteger` |
| 格式化 | format style | `FormatStyle`、Foundation 格式化文档 |
| 反射 | reflection, mirror | 标准库 `Mirror`、`dump` |
| 内存布局 / 填充 | memory layout, stride, alignment, padding | 标准库 `MemoryLayout` |
| 依赖注入 | dependency injection | 工程实践，非语言规范 |
