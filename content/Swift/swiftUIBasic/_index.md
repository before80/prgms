+++
title = "SwiftUI 入门实战"
linkTitle = "SwiftUI 实战"
weight = 2
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "十三章动手路线：从「视图是值」到绘制与特效，把 SwiftUI 的机制一路打通；凡涉及尺寸与对齐的结论都附实测数字"
isCJKLanguage = true
draft = false
+++

# SwiftUI 入门实战：十三章打通声明式界面

> 这不是又一份"从 View 讲到 NavigationStack"的教程。你的 [Swift 基础部分]({{< relref "../basic/_index.md" >}}) 第七篇（第 40–47 章）已经把 SwiftUI 的概念铺完了，[SwiftUI 官方文档整理]({{< relref "../SwiftUI/_index.md" >}}) 则是一本按 API 分类的字典。
>
> 这一份走第三条路：**只讲那些必须先想通的事，并且每讲一个规则，尽量给一个实测数字。**

## 为什么是这些章

SwiftUI 的表面门槛极低——`Text("你好")` 就出字，半小时能做出能跑的界面。真正的门槛在下面这些事上，它们**互相咬合**，缺一个都会卡住：

| 章 | 一句话 | 不学会怎样 |
| --- | --- | --- |
| [01 视图是值]({{< relref "Chapter-01-Views-Are-Values.md" >}}) | `View` 是结构体，`body` 是计算属性 | 会把视图当控件去"改"，然后奇怪为什么改了没用 |
| [02 状态是源头]({{< relref "Chapter-02-State-Is-The-Source.md" >}}) | 数据变了界面才会变，反过来不行 | 写出"列表点了不刷新"，然后卡三天 |
| [03 布局是一次谈判]({{< relref "Chapter-03-Layout-Is-A-Negotiation.md" >}}) | 父提尺寸 → 子报尺寸 → 父定位子 | 永远在靠猜加 `frame`，改一处崩三处 |
| [04 对齐与容器]({{< relref "Chapter-04-Alignment-And-Containers.md" >}}) | 对齐是"和谁对齐"，不是"往哪儿挪" | 两个高度不同的图怎么都对不齐 |
| [05 动画的本质]({{< relref "Chapter-05-Animation-Is-Interpolation.md" >}}) | 动画是两个状态值之间的补间 | 写了 `.animation` 却不动，或者全都在乱动 |
| [06 手势与身份]({{< relref "Chapter-06-Gestures-And-Identity.md" >}}) | 手势改状态，身份决定视图是否被复用 | 拖拽卡顿、列表复用出错、动画莫名其妙 |
| [07 组件化]({{< relref "Chapter-07-Composition-And-Components.md" >}}) | 重复的修饰符/布局/交互，各抽成一种东西 | 同一个样式抄 30 遍，改一次漏三处 |
| [08 列表与导航]({{< relref "Chapter-08-Lists-And-Navigation.md" >}}) | 身份决定行状态属于谁；页面是一叠值 | 删一行后别的行状态串了；导航没法编程控制 |
| [09 数据落地]({{< relref "Chapter-09-Data-And-Persistence.md" >}}) | 用 enum 建三态；I/O 别进视图 | 用三个布尔变量描述一件事，非法状态满天飞 |
| [10 性能与调试]({{< relref "Chapter-10-Performance-And-Debugging.md" >}}) | `body` 调用次数不重要，里面干了什么才重要 | 凭直觉优化，改了半天没变快 |
| [11 可访问性与适配]({{< relref "Chapter-11-Accessibility-And-Adaptation.md" >}}) | 字号、旁白、颜色、动效偏好都是需求 | 一部分用户根本用不了你的界面 |
| [12 绘制]({{< relref "Chapter-12-Drawing-And-Shapes.md" >}}) | `Shape` 描述路径，`Canvas` 批量绘制 | 系统没提供的图形就做不出来 |
| [13 视觉特效]({{< relref "Chapter-13-Visual-Effects.md" >}}) | 材质、混合、`visualEffect` 的正确用法 | 自己 blur 冒充毛玻璃，又贵又不像 |

## 这一份的特别之处：数字都是量出来的

SwiftUI 是视觉框架，但"看起来是什么样"很难用嘴说清。所以本教程里凡是涉及**尺寸、对齐、绘制**的结论，都附了实测数字。

测量方法：在无窗口模式下加载视图（`NSHostingController`），然后用 **`GeometryReader` 读取框架真实分配的尺寸和位置**。

⚠️ 这里有个方法论教训值得单独说：最初我用"把视图渲染进位图、逐像素扫描色块边界"的办法，结果**得出了错误结论**——因为位图只能反映画布范围内的内容，一旦视图溢出容器，我就把"可见的那一段"当成了"实际尺寸"，于是误以为 SwiftUI 会压缩固定宽度的视图。改用 `GeometryReader` 读真实分配值之后才发现：**它根本不压缩，是让内容溢出。**

第 03 章那一节保留了这次纠错的完整记录，因为**这个错误本身很有教学价值**——它示范了"用一个会骗人的测量手段去验证结论"有多危险。

### 一部分结论我无法实测，正文里都标注了

无界面环境能做的事有边界。以下几类断言我**明确标注了是"推导 / 文档化行为"而不是实测**：

| 内容 | 位置 | 为什么测不了 |
| --- | --- | --- |
| 列表身份选错会让行状态串位 | 第 08 章 | 需要真实的数据变更事件；每个 `NSHostingController` 都是独立的树 |
| 手势被系统取消时 `onEnded` 不触发 | 第 06 章 | 手势需要真实事件流（正文给了 SDK 里 `reset` 闭包的机制证据） |
| `.fixedSize()` 的确切效果 | 第 03 章 | 测出来的数字不稳定，所以不给数字 |
| 视觉效果的"好看程度" | 第 12、13 章 | 需要人眼判断 |

💭 标出来比含糊过去好。你如果发现哪一处描述与你的实际结果不符，那很可能是这些地方——贴给我，我改。

## 学习基线

- **语言**：Swift 6.4（本机工具链实测版本），示例按 Swift 6 语言模式（严格并发检查）编写。
- **框架版本**：凡是较新的 API 都标注了最低系统要求（`@Observable` 与 `visualEffect` 是 iOS 17、`glassEffect` 是 iOS 26）。
- **运行方式**：示例面向 Xcode + 预览。少量"纯逻辑"示例可以用命令行直接验证，正文里用 🔬 标出。
- **代码约定**：输出写在同一个代码块里用 `// prints:` 标注；⚠️ 易错点，🛑 编译错误示例，🚧 能编译但有代价，🔥 高频重点，🔬 实测。

## 和另外三份内容怎么配合

| 你在做什么 | 去哪一份 |
| --- | --- |
| 第一次学 SwiftUI，或者被布局/动画卡住了 | **本教程**，按顺序读，第 3 章最值得慢读 |
| 想知道"这个东西的完整概念体系" | [Swift 基础部分第七篇]({{< relref "../basic/_index.md" >}})，第 40–47 章 |
| 查某个 API 的签名和用法 | [SwiftUI 官方文档整理]({{< relref "../SwiftUI/_index.md" >}}) |
| 写 Swift 语法忘了怎么写 | [Swift 速查表]({{< relref "../CheatSheet/_index.md" >}}) |
| 程序崩了、结果不对 | [Swift 血泪速查]({{< relref "../CheatSheet/16-Pitfalls-and-Gotchas.md" >}}) |

---

## 十三章目录

**第一幕：把模型立起来**

1. [第 1 章 视图是值，不是控件]({{< relref "Chapter-01-Views-Are-Values.md" >}})
   `body` 为什么会被反复调用、`some View` 到底藏了什么、视图树是怎么被差分的
2. [第 2 章 状态是唯一的事实来源]({{< relref "Chapter-02-State-Is-The-Source.md" >}})
   `@State` / `@Binding` / `@Observable` / `@Environment` 的选择判据，以及"不刷新"bug 的定位法

**第二幕：布局（最容易劝退的部分）**

3. [第 3 章 布局是一次谈判]({{< relref "Chapter-03-Layout-Is-A-Negotiation.md" >}}) 🔥
   三步协商算法、`frame` 的四层含义、`Spacer` 与 `maxWidth` 的实测分配规则
4. [第 4 章 对齐与容器]({{< relref "Chapter-04-Alignment-And-Containers.md" >}})
   `alignment` 是与谁对齐、`overlay` 的尺寸与裁剪语义、`Grid` 与自定义 `Layout`

**第三幕：动起来**

5. [第 5 章 动画的本质]({{< relref "Chapter-05-Animation-Is-Interpolation.md" >}})
   动画 = 补间、`withAnimation` 与 `.animation(_:value:)` 的分工、为什么有的属性不动
6. [第 6 章 手势与身份]({{< relref "Chapter-06-Gestures-And-Identity.md" >}})
   `@GestureState` 与 `@State` 的分工、拖拽/缩放/旋转、身份如何决定视图的命运

**第四幕：工程化**

7. [第 7 章 组件化]({{< relref "Chapter-07-Composition-And-Components.md" >}})
   `ViewModifier`、泛型容器与 `@ViewBuilder`、`Style` 协议、`PreferenceKey`
8. [第 8 章 列表与导航]({{< relref "Chapter-08-Lists-And-Navigation.md" >}})
   `List` 三种写法、身份的实战后果、增删改查、`NavigationStack` 路径、弹窗家族
9. [第 9 章 数据落地]({{< relref "Chapter-09-Data-And-Persistence.md" >}})
   三态建模、`.task` 与 `.task(id:)`、网络请求、从 `@AppStorage` 到 `SwiftData`

**第五幕：质量**

10. [第 10 章 性能与调试]({{< relref "Chapter-10-Performance-And-Debugging.md" >}})
    `body` 调用次数为什么是误导性指标、`_printChanges`、Lazy 容器的边界
11. [第 11 章 可访问性与适配]({{< relref "Chapter-11-Accessibility-And-Adaptation.md" >}})
    动态字体、语义标签、颜色与动效偏好、尺寸类与平台差异

**第六幕：表现力**

12. [第 12 章 绘制]({{< relref "Chapter-12-Drawing-And-Shapes.md" >}})
    `Shape` 与 `Path`、`stroke` 与 `strokeBorder` 的实测差异、四种渐变、`Canvas`
13. [第 13 章 视觉特效]({{< relref "Chapter-13-Visual-Effects.md" >}})
    材质、模糊与阴影、混合模式、`visualEffect`、Liquid Glass

---

💭 **一句话建议**：如果你时间很紧，只读第 3 章。布局是 SwiftUI 里唯一"不看数字就学不会"的部分，也是绝大多数界面问题的根源。
