+++
title = "第六篇 动手做"
weight = 60
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "命令行工具、SwiftUI、综合项目与选读的服务端 Swift"
isCJKLanguage = true
draft = false
+++

# 第六篇：动手做

> 前面五篇攒的知识，在这里拧成能跑的东西。

三个作品的难度是往上走的：先用命令行工具把“参数解析 + 错误处理 + 测试”走一遍；再用 SwiftUI 进入声明式界面，理解 `@State`、`@Binding`、`@Observable` 各自解决什么问题；最后一个综合项目把模型、存储、异步、测试和命令行串成一个小系统。

最后留了一章选读的服务端 Swift：同一套语言，换一个运行环境，能做的事情比你想的多。

## 本篇章节

1. [命令行工具实战]({{< relref "Chapter-36-Command-Line-Tool-Workshop.md" >}})
2. [SwiftUI 入门]({{< relref "Chapter-37-SwiftUI-Introduction.md" >}})
3. [综合实战：支出记录器]({{< relref "Chapter-38-Capstone-Project.md" >}})
4. [选读：服务端 Swift]({{< relref "Chapter-39-Server-Side-Swift.md" >}})

> 第 37 章是 SwiftUI 的"第一次接触"，只够让你把界面跑起来。想把界面真正写扎实——状态放哪、布局怎么谈、列表与导航、表单校验、动画、异步数据、预览与发布——请接着读[第七篇 SwiftUI]({{< relref "../Part-7-SwiftUI/_index.md" >}})，那里有完整的八章。

## 读完你应该能

- 写出一个带参数解析、错误处理和测试的命令行工具。
- 用 SwiftUI 描述界面，并说清状态该放在哪一层。
- 把一个想法拆成模型、存储、界面和测试，而不是全塞进一个文件。
- 知道下一步想深入时，该去哪里找官方资料（见附录）。
