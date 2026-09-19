+++
title = "第七篇 SwiftUI"
weight = 70
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "从心智模型到状态管理、布局、导航、表单、动画、异步数据和测试的 SwiftUI 实战路线"
isCJKLanguage = true
draft = false
+++

# 第七篇：SwiftUI

> 第六篇里的第 37 章让你先摸了一次 SwiftUI 的手感。这一篇把那只手完整地装回来：八章，从"视图到底是什么"一直走到"一个能上架的界面长什么样"。

SwiftUI 最迷人也最容易劝退的一点是：它看起来太简单。`Text("你好")` 就出字，`VStack { }` 就排版，新手半小时能做出能跑的界面，然后在一个"列表点了不刷新"的 bug 上卡三天。原因通常不在 API，而在心智模型——SwiftUI 不是"在屏幕上摆控件"，而是"用状态描述界面的样子，剩下的交给框架"。

这一篇的顺序是按"必须先想清楚的问题"排的：

1. 先建立模型：视图是值，状态是源头；
2. 再学怎么把状态放对位置，让数据只朝一个方向流；
3. 然后是布局——SwiftUI 的布局是"提要求 + 给答复"，和 CSS 的直觉完全不同；
4. 有了布局，才能讲列表、导航、弹窗这些"页面级"的东西；
5. 表单与输入是把用户数据送进状态模型的门；
6. 动画不是装饰，而是告诉用户"你的操作发生了什么"；
7. 异步数据与网络：加载中、失败、成功，三种状态怎么优雅地建模；
8. 最后是预览、测试、可访问性和打包——决定这个界面是"能跑"还是"能用"。

## 本篇章节

1. [SwiftUI 的心智模型]({{< relref "Chapter-40-SwiftUI-Mental-Model.md" >}})
2. [状态与数据流]({{< relref "Chapter-41-SwiftUI-State-and-Data-Flow.md" >}})
3. [布局与视图组合]({{< relref "Chapter-42-SwiftUI-Layout-and-Composition.md" >}})
4. [列表、导航与弹窗]({{< relref "Chapter-43-SwiftUI-List-and-Navigation.md" >}})
5. [表单与用户输入]({{< relref "Chapter-44-SwiftUI-Forms-and-Input.md" >}})
6. [动画与转场]({{< relref "Chapter-45-SwiftUI-Animations.md" >}})
7. [异步数据、网络与生命周期]({{< relref "Chapter-46-SwiftUI-Async-and-Networking.md" >}})
8. [预览、测试、可访问性与发布]({{< relref "Chapter-47-SwiftUI-Previews-Testing-and-Accessibility.md" >}})

## 读之前请确认

- 你已经写完过第二篇的语法、第三篇的类型，尤其是**协议、泛型、`@ViewBuilder` 那一小节**（第 15B.18 节）。
- 你手边有 Xcode（SwiftUI 预览要它），或者至少能跑 `xcrun --sdk macosx swiftc`。
- 本机工具链是 Swift 6.3 及以上；本篇示例用 macOS/iOS 都能跑的 API，遇到平台差异会明确写出来。

## 读完你应该能

- 说清"视图是值"意味着什么，以及为什么 `body` 每次都重新计算却不必担心性能。
- 判断一份状态该放在视图自己身上、父视图身上，还是放进 `@Observable` 模型里。
- 用 `NavigationStack`、`List`、`sheet` 组装多页面应用，而不是把所有逻辑塞进一个 `body`。
- 用 `withAnimation`、`transition` 把状态变化讲成一个用户看得懂的故事。
- 把一次网络请求拆成"加载中 / 成功 / 失败"三态，并在视图里优雅地呈现。
- 用 `#Preview` 和测试把界面代码也纳入质量流程。
