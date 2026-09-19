+++
title = "Swift 基础部分"
weight = 1
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "从安装 Swift 6.3 到并发、测试、SwiftUI 与服务端开发的完整入门路线"
isCJKLanguage = true
draft = false

+++

# Swift 快速入门：从第一行代码到真实项目

> 这是一套面向“已经会编程、但第一次系统学习 Swift”的教程。它不假设你熟悉 Apple 生态，也不要求你先买一台新设备。语言、内存、并发、工程、测试和实战会按学习顺序展开，示例尽量给出可运行结果。前七篇按“你接下来要做什么”编排，最后的第八篇换成另一种切法——按“概念家族”把散落的知识点收口。

## 学习基线

- 语言版本：Swift 6.3.x，书中示例以 Swift 6.3.3 为基准。
- 语言模式：示例按 Swift 6 模式编写；涉及并发迁移时会说明语言模式差异。
- 源文件编码：所有示例都按 UTF-8 保存。Swift 只接受 UTF-8，第 2 章第一节会把这条规则和常见报错讲清楚。
- 学习方式：先读每一节的文字，再运行代码块，最后看“本章小结”和“易错点速查”。
- 代码约定：示例结果写在同一个代码块里，以 `// prints:` 标注；错误示例会用 `text` 代码块单独展示。

## 建议路线

| 阶段 | 章节 | 目标 |
| --- | --- | --- |
| [第一篇 起步]({{< relref "Part-1-Getting-Started/_index.md" >}}) | 第 1–3 章 | 安装工具链、理解源码结构、创建 SwiftPM 项目 |
| [第二篇 语言主干]({{< relref "Part-2-Language-Core/_index.md" >}}) | 第 4–15、15B 章 | 常量、字符串、集合、控制流、函数、闭包、错误处理与语法糖 |
| [第三篇 自定义类型与抽象]({{< relref "Part-3-Types-and-Abstraction/_index.md" >}}) | 第 16–26 章 | 枚举、结构体、类、协议、泛型、宏 |
| [第四篇 内存与并发]({{< relref "Part-4-Memory-and-Concurrency/_index.md" >}}) | 第 27–32 章 | 值语义、ARC、所有权、async/await、actor |
| [第五篇 工程与质量]({{< relref "Part-5-Engineering-and-Quality/_index.md" >}}) | 第 33–35 章 | 包管理、测试、调试与性能 |
| [第六篇 动手做]({{< relref "Part-6-Hands-On/_index.md" >}}) | 第 36–39 章 | 命令行工具、SwiftUI、综合项目、服务端 Swift |
| [第七篇 SwiftUI]({{< relref "Part-7-SwiftUI/_index.md" >}}) | 第 40–47 章 | 视图心智模型、状态管理、布局、导航、表单、动画、异步数据与发布 |
| [第八篇 概念专题]({{< relref "Part-8-Concept-Tour/_index.md" >}}) | 第 48–52 章 | 序列协议族、数值与格式化、属性与下标全形态、标准库算法、反射与内存布局 |

## 全书目录

每一篇都有自己的首页（篇导读 + 章节清单），章的源文件也放在对应的篇目录下。

### [第一篇 起步]({{< relref "Part-1-Getting-Started/_index.md" >}})

1. [装上 Swift 6.3，把第一行代码跑起来]({{< relref "Part-1-Getting-Started/Chapter-01-Install-and-First-Code.md" >}})
2. [一段 Swift 源码的解剖]({{< relref "Part-1-Getting-Started/Chapter-02-Anatomy-of-Source-Code.md" >}})
3. [SwiftPM 与第一个项目]({{< relref "Part-1-Getting-Started/Chapter-03-SwiftPM-and-First-Project.md" >}})

### [第二篇 语言主干]({{< relref "Part-2-Language-Core/_index.md" >}})

4. [常量、变量与数值]({{< relref "Part-2-Language-Core/Chapter-04-Constants-Variables-and-Numbers.md" >}})
5. [字符串与字符]({{< relref "Part-2-Language-Core/Chapter-05-Strings-and-Characters.md" >}})
6. [正则表达式]({{< relref "Part-2-Language-Core/Chapter-06-Regular-Expressions.md" >}})
7. [运算符与表达式]({{< relref "Part-2-Language-Core/Chapter-07-Operators-and-Expressions.md" >}})
8. [元组、类型别名与基础类型判断]({{< relref "Part-2-Language-Core/Chapter-08-Tuples-Typealias-and-Type-Checking.md" >}})
9. [可选值]({{< relref "Part-2-Language-Core/Chapter-09-Optionals.md" >}})
10. [集合]({{< relref "Part-2-Language-Core/Chapter-10-Collections.md" >}})
11. [控制流（一）]({{< relref "Part-2-Language-Core/Chapter-11-Control-Flow-Part-1.md" >}})
12. [控制流（二）：switch 与模式匹配]({{< relref "Part-2-Language-Core/Chapter-12-Control-Flow-Part-2.md" >}})
13. [函数]({{< relref "Part-2-Language-Core/Chapter-13-Functions.md" >}})
14. [闭包]({{< relref "Part-2-Language-Core/Chapter-14-Closures.md" >}})
15. [错误处理]({{< relref "Part-2-Language-Core/Chapter-15-Error-Handling.md" >}})
15B. [语法糖与特殊写法]({{< relref "Part-2-Language-Core/Chapter-15B-Sugar-and-Special-Forms.md" >}})

### [第三篇 自定义类型与抽象]({{< relref "Part-3-Types-and-Abstraction/_index.md" >}})

16. [枚举]({{< relref "Part-3-Types-and-Abstraction/Chapter-16-Enumerations.md" >}})
17. [结构体与值语义]({{< relref "Part-3-Types-and-Abstraction/Chapter-17-Structures-and-Value-Semantics.md" >}})
18. [类与继承]({{< relref "Part-3-Types-and-Abstraction/Chapter-18-Classes-and-Inheritance.md" >}})
19. [属性、方法与下标]({{< relref "Part-3-Types-and-Abstraction/Chapter-19-Properties-Methods-and-Subscripts.md" >}})
20. [初始化与反初始化]({{< relref "Part-3-Types-and-Abstraction/Chapter-20-Initialization-and-Deinitialization.md" >}})
21. [扩展与嵌套类型]({{< relref "Part-3-Types-and-Abstraction/Chapter-21-Extensions-and-Nested-Types.md" >}})
22. [协议]({{< relref "Part-3-Types-and-Abstraction/Chapter-22-Protocols.md" >}})
23. [泛型]({{< relref "Part-3-Types-and-Abstraction/Chapter-23-Generics.md" >}})
24. [类型系统补全]({{< relref "Part-3-Types-and-Abstraction/Chapter-24-Type-System-Toolbox.md" >}})
25. [访问控制、模块与条件编译]({{< relref "Part-3-Types-and-Abstraction/Chapter-25-Access-Control-Modules-and-Conditional-Compilation.md" >}})
26. [宏]({{< relref "Part-3-Types-and-Abstraction/Chapter-26-Macros.md" >}})

### [第四篇 内存与并发]({{< relref "Part-4-Memory-and-Concurrency/_index.md" >}})

27. [值语义、写时复制与 ARC]({{< relref "Part-4-Memory-and-Concurrency/Chapter-27-Value-Semantics-COW-and-ARC.md" >}})
28. [循环引用]({{< relref "Part-4-Memory-and-Concurrency/Chapter-28-Reference-Cycles.md" >}})
29. [内存安全与所有权]({{< relref "Part-4-Memory-and-Concurrency/Chapter-29-Memory-Safety-and-Ownership.md" >}})
30. [并发（一）：async/await 与结构化并发]({{< relref "Part-4-Memory-and-Concurrency/Chapter-30-Concurrency-Part-1.md" >}})
31. [并发（二）：隔离域、actor 与 Sendable]({{< relref "Part-4-Memory-and-Concurrency/Chapter-31-Concurrency-Part-2.md" >}})
32. [并发（三）：迁移与 Approachable Concurrency]({{< relref "Part-4-Memory-and-Concurrency/Chapter-32-Concurrency-Part-3.md" >}})

### [第五篇 工程与质量]({{< relref "Part-5-Engineering-and-Quality/_index.md" >}})

33. [包与工程]({{< relref "Part-5-Engineering-and-Quality/Chapter-33-Packages-and-Engineering.md" >}})
34. [测试]({{< relref "Part-5-Engineering-and-Quality/Chapter-34-Testing.md" >}})
35. [调试与性能]({{< relref "Part-5-Engineering-and-Quality/Chapter-35-Debugging-and-Performance.md" >}})

### [第六篇 动手做]({{< relref "Part-6-Hands-On/_index.md" >}})

36. [命令行工具实战]({{< relref "Part-6-Hands-On/Chapter-36-Command-Line-Tool-Workshop.md" >}})
37. [SwiftUI 入门]({{< relref "Part-6-Hands-On/Chapter-37-SwiftUI-Introduction.md" >}})
38. [综合实战：支出记录器]({{< relref "Part-6-Hands-On/Chapter-38-Capstone-Project.md" >}})
39. [选读：服务端 Swift]({{< relref "Part-6-Hands-On/Chapter-39-Server-Side-Swift.md" >}})

### [第七篇 SwiftUI]({{< relref "Part-7-SwiftUI/_index.md" >}})

40. [SwiftUI 的心智模型]({{< relref "Part-7-SwiftUI/Chapter-40-SwiftUI-Mental-Model.md" >}})
41. [状态与数据流]({{< relref "Part-7-SwiftUI/Chapter-41-SwiftUI-State-and-Data-Flow.md" >}})
42. [布局与视图组合]({{< relref "Part-7-SwiftUI/Chapter-42-SwiftUI-Layout-and-Composition.md" >}})
43. [列表、导航与弹窗]({{< relref "Part-7-SwiftUI/Chapter-43-SwiftUI-List-and-Navigation.md" >}})
44. [表单与用户输入]({{< relref "Part-7-SwiftUI/Chapter-44-SwiftUI-Forms-and-Input.md" >}})
45. [动画与转场]({{< relref "Part-7-SwiftUI/Chapter-45-SwiftUI-Animations.md" >}})
46. [异步、网络与生命周期]({{< relref "Part-7-SwiftUI/Chapter-46-SwiftUI-Async-and-Networking.md" >}})
47. [预览、测试、可访问性与发布]({{< relref "Part-7-SwiftUI/Chapter-47-SwiftUI-Previews-Testing-and-Accessibility.md" >}})

### [第八篇 概念专题]({{< relref "Part-8-Concept-Tour/_index.md" >}})

48. [序列与集合协议：Sequence、Collection 与惰性求值]({{< relref "Part-8-Concept-Tour/Chapter-48-Sequence-and-Collection-Protocols.md" >}})
49. [数值协议与格式化：从 Numeric 到 FormatStyle]({{< relref "Part-8-Concept-Tour/Chapter-49-Numeric-Protocols-and-Formatting.md" >}})
50. [属性与下标全形态：一个概念家族的收口]({{< relref "Part-8-Concept-Tour/Chapter-50-Properties-and-Subscripts-Tour.md" >}})
51. [标准库算法工具箱：zip、stride 与 reduce(into:)]({{< relref "Part-8-Concept-Tour/Chapter-51-Standard-Library-Algorithms.md" >}})
52. [反射与内存布局：类型在运行时留下什么]({{< relref "Part-8-Concept-Tour/Chapter-52-Reflection-and-Memory-Layout.md" >}})

## 附录

- [附录A 语法地图：官方指南到章节]({{< relref "Appendix-A-Syntax-Map.md" >}})
- [附录B 标准库与 Foundation 的分界]({{< relref "Appendix-B-Standard-Library-and-Foundation.md" >}})
- [附录C @ 属性与 # 指令速查]({{< relref "Appendix-C-Attributes-and-Directives.md" >}})
- [附录D 术语表]({{< relref "Appendix-D-Glossary.md" >}})
- [附录E 版本差异与易错点清单]({{< relref "Appendix-E-Version-Differences.md" >}})
- [附录F 官方资料与延伸阅读]({{< relref "Appendix-F-Official-Resources.md" >}})

## 学完之后

不要急着背所有 API。真正值得带走的是：用值类型表达数据、用协议表达能力、用 actor 保护共享状态、用测试证明行为、用工具测量性能。语法会更新，这些判断不会。
