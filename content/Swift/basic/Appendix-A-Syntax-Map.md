+++
title = "附录A 语法地图：官方指南到章节"
weight = 1000
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录A：语法地图：官方指南到章节

> 本附录把 Swift 官方语言指南的主要主题映射到本书章节。复习时可以先看地图，再回到具体章节，而不是从头盲目重读。

## A.1 语言指南主题

| 官方主题 | 本书章节 | 关键词 |
| --- | --- | --- |
| Lexical Structure | 第2章 | 源文件编码（UTF-8）、空白、注释、标识符、关键字、字面量、运算符 |
| The Basics | 第2、4、8、9章 | 常量、变量、注释、数值、元组、可选值 |
| Basic Operators | 第7章 | 算术、比较、逻辑、区间、位运算、运算符重载 |
| Strings and Characters | 第5章 | `String`、`Character`、索引、切片、插值 |
| Collection Types | 第10章 | `Array`、`Dictionary`、`Set`、值语义 |
| Sequence / Collection 协议 | 第48章 | `IteratorProtocol`、`Sequence`、`Collection`、`RandomAccessCollection`、惰性视图 |
| 数值与格式化（非指南主题） | 第49章 | `Numeric`、`BinaryInteger`、`FixedWidthInteger`、`FloatingPoint`、`Decimal`、`FormatStyle` |
| Control Flow | 第11、12章 | `if`、`for`、`while`、`switch`、模式匹配 |
| Functions | 第13章 | 标签、默认值、可变参数、`inout`、函数类型 |
| Closures | 第14章 | 尾随闭包、捕获列表、逃逸、自动闭包 |
| Enumerations | 第16章 | 原始值、关联值、递归枚举、`CaseIterable` |
| Structures and Classes | 第17、18章 | 值语义、引用语义、继承、身份 |
| Properties | 第19章、第50章 | 存储、计算、观察器、`lazy`、类型属性、属性包装器 |
| Methods | 第19章 | 实例方法、类型方法、`mutating` |
| Subscripts | 第19章、第50章 | 下标声明与访问；多参数、静态、安全版重载、动态成员查找 |
| Inheritance | 第18章 | 重写、`super`、`final` |
| Initialization | 第20章 | 指定/便利初始化器、可失败初始化器、两阶段初始化 |
| Deinitialization | 第20章 | `deinit`、隔离反初始化 |
| Optional Chaining | 第9章 | `?.`、链式安全访问 |
| Error Handling | 第15章 | `throw`、`throws`、`do-catch`、`Result`、类型化抛出 |
| Concurrency | 第30、31、32章 | `async/await`、`Task`、actor、`Sendable` |
| Type Casting | 第8、24章 | `is`、`as?`、`as!`、元类型 |
| Nested Types | 第21章 | 类型内部命名空间 |
| Extensions | 第21章 | 计算属性、方法、协议遵循、条件扩展 |
| Protocols | 第22章 | 协议要求、关联类型、扩展、`some`/`any` |
| Generics | 第23章 | 泛型函数、泛型类型、约束、参数包 |
| Opaque and Boxed Protocol Types | 第22、23、24章 | `some`、`any`、类型擦除 |
| Automatic Reference Counting | 第27、28章 | ARC、强/弱/无主引用、循环引用 |
| Memory Safety | 第29章 | 独占访问、`borrowing`、`consuming`、`~Copyable` |
| Access Control | 第25章 | `open`、`public`、`package`、`internal`、`private` |
| Advanced Operators | 第7章 | 位运算、溢出运算、自定义运算符 |
| Macros | 第26章 | 自由宏、附着宏、编译器插件 |
| Result builders | 第15B.18节、第22.8节 | `@resultBuilder`、`@ViewBuilder`、块里的 `if` / `switch` / `for` |
| 标准库算法（非指南主题） | 第51章 | `zip`、`stride`、`sequence`、`reduce(into:)`、`Dictionary(grouping:by:)`、`lazy` |
| 反射与内存布局（非指南主题） | 第52章 | `CustomStringConvertible`、`LosslessStringConvertible`、`Mirror`、`MemoryLayout`、`withUnsafeBytes` |

## A.2 声明主题

| 声明 | 章节 | 说明 |
| --- | --- | --- |
| `import` | 第25章 | 模块导入与精确导入 |
| `let` / `var` | 第4章 | 常量与变量 |
| `func` | 第13章 | 函数与参数标签 |
| `enum` | 第16章 | 枚举与关联值 |
| `struct` | 第17章 | 结构体与值语义 |
| `class` | 第18章 | 类、继承与引用语义 |
| `protocol` | 第22章 | 能力描述与协议扩展 |
| `extension` | 第21章 | 为已有类型添加能力 |
| `init` / `deinit` | 第20章 | 初始化与反初始化 |
| `subscript` | 第19章 | 自定义下标 |
| `typealias` | 第8章 | 类型别名 |
| `associatedtype` | 第22、23章 | 协议关联类型 |
| `macro` | 第26章 | 宏声明 |
| `@main` | 第3章 | 程序入口 |

## A.3 表达式与模式

| 主题 | 章节 |
| --- | --- |
| 前缀、中缀、后缀运算符 | 第7章 |
| 三元与空合表达式 | 第7、9章 |
| `if` / `switch` 表达式 | 第11、12、15B章 |
| 闭包表达式 | 第14章 |
| 隐式成员表达式 | 第15B、16、18章 |
| 键路径表达式 | 第15B、24章 |
| 通配模式 | 第12、15B章 |
| 标识符与值绑定模式 | 第12章 |
| 元组模式 | 第12章 |
| 枚举用例模式 | 第12、16章 |
| 可选模式 | 第9、12章 |
| 类型转换模式 | 第8、12章 |
| 表达式模式 | 第7、12章 |
| 语法糖与特殊写法（省 `return`、隐式 `self`、绑定简写、`.init`、`callAsFunction`、字面量协议等） | 第15B章 |

## A.4 使用建议

复习时优先顺序：

1. 第 4、5、7、9、10 章：日常代码最常用的基础。
2. 第 11–15、15B 章：控制流、函数、闭包、错误处理，以及写法层面的语法糖。
3. 第 16–23 章：自定义类型、协议、泛型。
4. 第 27–32 章：内存与并发，决定代码能否在真实项目里稳定运行。
5. 第 33–39 章：工程、测试、调试和实战。
6. 第 48–52 章：概念专题。它们不教新语法，而是把序列协议、数值协议、属性与下标、标准库算法、反射这五个"家族"各自收成一页，适合当字典查。
