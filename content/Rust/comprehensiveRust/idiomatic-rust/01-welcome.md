+++
title = "1 欢迎"
date = 2026-08-11T11:30:00+08:00
weight = 388
type = "docs"
description = "01-欢迎 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/welcome.html](https://google.github.io/comprehensive-rust/idiomatic/welcome.html)

# 1 欢迎

[Rust 基础](../day1-morning/01-welcome-day-1.md)介绍了 Rust 语法与核心概念。现在我们更进一步：如何在项目中*有效地*使用 Rust？*地道*的 Rust 是什么样的？

本课程带有倾向性：我们会把你推向某些模式，并远离另一些。不过我们也认识到，有些项目可能有不同需求。我们始终提供必要信息，帮助你在自己项目的上下文与约束内做出知情决策。

> ⚠️ 本课程仍在**积极开发**中。
>
> 材料可能频繁变动，也可能存在尚未发现的错误。尽管如此，我们仍鼓励你浏览并提供早期反馈！

## 日程

含每次 10 分钟休息，本时段约需 14 小时 10 分钟。内容包括：

| 小节 | 时长 |
| --- | --- |
| API 设计基础 | 3 小时 15 分钟 |
| 利用类型系统 | 7 小时 30 分钟 |
| 多态 | 3 小时 5 分钟 |


> 课程将覆盖下列主题。每个主题可能因复杂度与相关性，占用一张或多张幻灯片。
>
> ## 目标受众
>
> 至少有 2–3 年 C、C++11 或更新版本、Java 7 或更新版本、Python 2 或 3、Go 或其它类似命令式语言编码经验的工程师。我们不期望你有 Swift、Kotlin、C# 或 TypeScript 等更现代或功能更丰富语言的经验。
>
> ### API 设计基础
>
> - 黄金法则：优先保证调用处（callsite）清晰可读。人们花在阅读调用处的时间，远多于阅读被调函数的声明。
> - 让 API 可预期
>   - 遵循命名约定（大小写约定，优先使用标准库中已有先例的词汇——例如方法应叫 `push` 而非 `push_back`，`is_empty` 而非 `empty` 等）
>   - 了解标准库中的词汇类型与 trait，并在 API 中使用它们。若某物感觉像基本类型/算法，先查标准库。
>   - 使用本课稍后讨论的成熟 API 设计模式（例如 newtype、owned/view 类型对、错误处理）
> - 编写有意义且有效的文档注释（例如：不要只是把方法名里的下划线换成空格；不要为了填满每个 markdown 标签而重复同一信息；提供用法示例）
>
> ### 借助类型系统
>
> - 简要回顾枚举、结构体与类型别名
> - Newtype 模式与封装：解析，不要校验（parse, don't validate）
> - 扩展 trait（extension traits）：当你只想提供额外行为时，避免用 newtype 模式
> - RAII、作用域守卫（scope guards）与 drop bomb：用 `Drop` 清理资源、触发动作或强制不变量
> - 「令牌」类型（token types）：迫使用户证明他们已执行特定操作
> - Typestate 模式：在编译期强制正确的状态转换
> - 用借用检查器强制与内存所有权无关的不变量
>   - 标准库中的 OwnedFd/BorrowedFd
>   - [Branded types](https://plv.mpi-sws.org/rustbelt/ghostcell/paper.pdf)
>
> ### 不要与借用检查器作对
>
> - 「拥有」类型与「视图」类型：`&str` 与 `String`，`Path` 与 `PathBuf` 等
> - 不要隐藏所有权要求：避免隐藏的 `.clone()`，学会爱上 `Cow`
> - 沿所有权边界拆分类型
> - 把所有权层次结构设计成树
> - 管理循环依赖的策略：引用计数、用索引代替引用
> - 内部可变性（Cell、RefCell）
> - 处理用户定义数据类型上的生命周期参数
>
> ### Rust 中的多态
>
> - Trait 与泛型函数的快速回顾
> - Rust 没有继承：这意味着什么？
>   - 用枚举做多态
>   - 用 trait 做多态
>   - 用组合
>   - 如何选择最合适的模式？
> - 使用泛型
>   - 函数中的泛型类型参数，还是作为参数的 trait 对象？
>   - Trait 约束不必引用泛型参数本身
>   - Trait 中的类型参数：应是泛型参数还是关联类型？
> - 宏：当 trait 不够用（或太复杂）时，用于 DRY 代码的有价值工具
>
> ### 错误处理
>
> - 错误的目的是什么？恢复 vs 报告。
> - Result vs Option
> - 设计良好的错误：
>   - 确定错误的作用域。
>   - 当错误向上流动、跨越作用域边界时，捕获额外上下文。
>   - 借助 `Error` trait 跟踪完整错误链。
>   - 借助 `thiserror` 减少定义错误类型时的样板代码。
>   - `anyhow`
> - 用 `Result<Result<T, RecoverableError>, FatalError>` 区分致命错误与可恢复错误。

