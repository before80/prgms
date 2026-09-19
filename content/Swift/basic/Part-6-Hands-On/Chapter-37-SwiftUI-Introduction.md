+++
title = "第37章 SwiftUI 入门：声明式界面与状态"
weight = 370
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "第一次接触 SwiftUI：视图是值、App 骨架、@State/@Binding/@Observable 的分工与 .task 生命周期"
isCJKLanguage = true
draft = false
+++

# 第三十七章：SwiftUI 入门：声明式界面与状态

> SwiftUI 不是"用 Swift 写 UIKit"的另一种皮肤。它要求你换一种思考方式：描述界面在某份状态下的样子，而不是一步步命令界面怎么变。状态变了，界面重新计算。语法的简洁背后，是值类型、协议、属性包装器和隔离共同作用的结果。

这一章是"第一次接触"：把该装上的齿轮装满，让你能读懂 SwiftUI 代码、能跑起来、能在遇到 bug 时知道往哪儿看。想真正把界面写扎实（布局谈判、列表身份、表单校验、动画、异步、预览与发布），接着读后面的**第七篇**（第 40–47 章）。

## 37.1 第一个视图，以及它周围的骨架

Swift 里"界面"的最小完整单元不是一个视图，而是三样东西：入口、场景、视图。

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 12) {
            Text("Hello, SwiftUI")
                .font(.title)
            Text("声明式界面会让状态成为主角")
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// 界面效果：窗口里居中一块两行文字，第一行大标题，第二行灰色副标题
```

三层各自的职责别混淆：

| 层 | 类型 | 管什么 |
| --- | --- | --- |
| 入口 | `@main` 标注的 `App` | 程序的起点；一个可执行目标只允许有一个 |
| 场景 | `Scene`（这里是 `WindowGroup`） | 窗口、菜单、生命周期；macOS 上可以开多个窗口 |
| 视图 | `View` | 窗口里的内容 |

写界面时的常见方向性错误，就是**把窗口级的事情写进视图里**（比如"打开一个新窗口"这类操作应该找场景，而不是塞进某个 `body`）。

`body` 返回 `some View`。它隐藏了具体视图类型，但编译器知道真实类型，因此能生成高效的界面更新代码。

`body` 里能并列写视图、写 `if`、写 `ForEach`，靠的是 `@ViewBuilder` 这个**结果构建器**：`View` 协议把 `body` 需求标成了 `@ViewBuilder`，所以实现里不用自己再写一遍标注。`if` 的两个分支类型不同也不要紧，编译器会把它们包成一个二选一的内部类型（`_ConditionalContent`），再交给 `some View` 藏起来。想亲手做一个构建器、把块里的语句合成一个值，见第 15B.18 节。

```swift
import SwiftUI

struct StatusBadge: View {
    let on: Bool

    var body: some View {
        HStack {
            Image(systemName: on ? "checkmark.circle" : "xmark.circle")
            Text(on ? "已开启" : "已关闭")
            if on {
                Text("(刚刚更新)").font(.caption)
            }
        }
    }
}

// 界面效果：一行图标 + 文字；on 为 true 时末尾多一小段灰色小字
```

这段代码在普通函数里写不出来——普通函数体并列写三个表达式是语法错误。视图之所以可以，是因为它站在一块被结果构建器"接管"的代码块里。

### 怎么把 SwiftUI 代码跑起来

三个可选路径，按省事程度排列：

1. **Xcode 新建 App 工程**（最推荐）：自带预览，改一行立刻能看到界面；语言、部署目标在工程设置里调。
2. **把示例贴进已有工程的某个视图文件**：适合临时验证一段代码。
3. **命令行类型检查**：没有 Xcode 界面时，也能确认代码能不能编译：

```bash
$ xcrun --sdk macosx swiftc -typecheck -swift-version 6 View.swift
```

⚠️ 在命令行目标平台（比如纯 SwiftPM 的 macOS 命令行程序）里，SwiftUI 的界面**不会弹出来**——它需要真正的 App 生命周期。所以类型检查用来抓语法错误，看效果还是要去 Xcode。

## 37.2 `@State`：视图自己的小状态

会变的量放进 `@State`，界面上用到它的地方自然跟着更新：

```swift
import SwiftUI

struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("计数：\(count)")
            Button("加一") { count += 1 }
        }
    }
}

// 界面效果：初始显示"计数：0"；每点一次"加一"，数字加一
```

视图结构体本身是值类型，但 `@State` 会把存储放到 SwiftUI 管理的位置。点击按钮后 `count` 改变，SwiftUI 重新调用 `body`，界面显示新值。

这里有个值得想清楚的问题：**为什么不把 `count` 写成普通的 `var`？**

```swift
import SwiftUI

struct BrokenCounter: View {
    private var count = 0        // ❌ 普通存储属性

    var body: some View {
        VStack {
            Text("计数：\(count)")
            Button("加一") {
                // count += 1  ← 这里连编译都过不去
            }
        }
    }
}

// 报错：cannot assign to property: 'self' is immutable
// （在视图的 body 里，self 是只读的，改不了自己的存储属性）
```

即使编译器放行，结果也还是错的：每次 `body` 重算都会新建一个 `BrokenCounter` 结构体，`count` 回到 0。`@State` 解决的正是这两件事——既允许在语义上"改"，又把值存在结构体之外不被重置。

界面行为可以描述为：

```text
初始显示：计数：0
点击按钮后：计数：1
```

## 37.3 `@Binding`：让子视图修改父视图状态

可复用的子视图不拥有数据，只借用一份"能读能写"的引用：

```swift
import SwiftUI

struct ToggleRow: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("开启通知", isOn: $isOn)
    }
}

struct SettingsView: View {
    @State private var notifications = false

    var body: some View {
        Form {
            ToggleRow(isOn: $notifications)
            Text(notifications ? "通知已开启" : "通知已关闭")
                .foregroundStyle(.secondary)
        }
    }
}

// 界面效果：一行开关；拨动后下面那行灰字在"已开启/已关闭"之间切换
```

`@Binding` 不拥有状态，它提供一条读写通道。父视图用 `$notifications` 创建绑定，子视图负责展示和修改。这正是值语义视图之间安全共享状态的机制——子视图改的是**父视图那份数据**，而不是自己偷偷存了一份副本。

需要提醒的是 `$` 的含义：`notifications` 是 `Bool`，`$notifications` 是 `Binding<Bool>`。给控件传 `notifications` 会得到"只读、改不动"的效果，这也是"输入框打了字没反应"的头号原因。

## 37.4 `@Observable`：现代状态模型

数据一多、一跨页面，就该从散落的 `@State` 升级成一个模型类：

```swift
import SwiftUI
import Observation

@Observable
final class CartModel {
    var items: [String] = []
    var total = 0

    func add(_ item: String) {
        items.append(item)
        total += 1
    }
}

struct CartView: View {
    @State private var cart = CartModel()

    var body: some View {
        VStack {
            Text("商品数：\(cart.total)")
            Button("添加") { cart.add("书") }
        }
    }
}

// 界面效果：初始"商品数：0"；每点一次"添加"数字加一
```

注意两个角色的分工：`@State` 负责**持有**这个对象（谁拥有它的生命周期），`@Observable` 负责**通知**（哪些视图需要在它变化时重算）。两者缺一不可——只加 `@Observable` 而没有 `@State`，视图可能每次重算都造一个新对象；只加 `@State` 而类不可观察，改了数据界面不刷新。

`@Observable` 会追踪哪些属性被读取，并在它们变化时更新依赖它们的视图。它比旧式 `ObservableObject` 更细粒度（对象里十个属性，只有被读过的那一个变化才会触发重算），样板代码也更少。

⚠️ 追踪**不会穿透**：如果 `CartModel` 里还嵌了一个没标 `@Observable` 的类，改那个内层对象的属性不会触发刷新。

## 37.5 旧式 `ObservableObject` 与 `@StateObject`

已有项目里仍会看到另一套写法：

```swift
import SwiftUI

final class LegacyCart: ObservableObject {
    @Published var total = 0
}

struct LegacyView: View {
    @StateObject private var cart = LegacyCart()

    var body: some View {
        Text("总数：\(cart.total)")
    }
}
```

`@StateObject` 负责在视图生命周期内创建并持有对象；`@ObservedObject` 用于接收外部传入的对象；`@EnvironmentObject` 则从环境里取。它们和现代写法的对应关系是：

| 旧写法 | 现代写法 |
| --- | --- |
| `class X: ObservableObject` | `@Observable final class X` |
| `@Published var a` | `var a` |
| `@StateObject` | `@State` |
| `@ObservedObject` | 普通 `let` / `var` |
| `@EnvironmentObject` | `@Environment(X.self)` |

新项目优先考虑 `@Observable`，但维护旧代码时必须看得懂左边这一列。判断标准很简单：看到 `Published`、`Object` 这类字眼，就是旧写法。

## 37.6 列表、导航与异步任务

一个能点进去的两层界面，需要三样东西配合：数据带身份、导航栈、目的地声明。

```swift
import SwiftUI

struct Item: Identifiable, Hashable {
    let id = UUID()
    let name: String
}

struct ItemListView: View {
    let items = [Item(name: "第一项"), Item(name: "第二项")]

    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.name, value: item)
            }
            .navigationTitle("项目")
            .navigationDestination(for: Item.self) { item in
                Text("详情：\(item.name)")
            }
        }
    }
}

// 界面效果：一个标题为"项目"的列表，两行；点任意一行滑入详情页
```

两处容易被忽略但很关键：`Identifiable` 提供了稳定的 `id`（列表靠它认人），`Hashable` 则让 `Item` 能作为 `NavigationLink` 的路由值。少了 `Hashable`，`value:` 那个写法直接编译不过。

异步加载可以放在 `.task` 中：

```swift
import SwiftUI

struct LoadView: View {
    @State private var text = "加载中"

    var body: some View {
        Text(text)
            .task {
                try? await Task.sleep(for: .milliseconds(50))
                text = "加载完成"
            }
    }
}

// 界面效果：进入页面先是"加载中"，约 0.05 秒后变成"加载完成"
```

`.task` 会在视图出现时启动任务，并在视图消失时取消它。它比在 `onAppear` 里手动创建任务更容易管理生命周期：**视图走了，任务就跟着走**，不会出现"页面早关了，请求还在跑，回来还往已经消失的界面上写数据"。想根据某个值的变化重新触发（比如搜索框内容），用 `.task(id:)`，第 46 章有完整写法。

## 37.7 状态应该放在哪里

| 状态类型 | 推荐工具 |
| --- | --- |
| 只属于当前视图的简单值 | `@State` |
| 子视图需要修改父状态 | `@Binding` |
| 共享的现代模型对象 | `@Observable` + `@State` |
| 旧式共享模型对象 | `ObservableObject` + `@StateObject`/`@ObservedObject` |
| 系统环境值（`dismiss`、`colorScheme` 等） | `@Environment` |

状态提升得太高，会让无关视图频繁更新；状态放得太低，又无法共享。判断标准是：谁需要读、谁需要写、生命周期由谁拥有。

## 37.8 本章小结

| 概念 | 关键结论 |
| --- | --- |
| `View` | 用 `body` 描述界面，是值类型 |
| `App` / `Scene` | 入口与窗口层；一个目标只有一个 `@main` |
| `some View` | 隐藏具体视图类型但保留编译期信息 |
| `@ViewBuilder` | 让 `body` 里能写 `if`、`ForEach` 并并列多个视图 |
| `@State` | 视图拥有的可变状态，不允许直接改存储属性 |
| `@Binding` | 与父级状态双向连接，用 `$` 创建 |
| `@Observable` | 现代观察模型，属性级粒度，不穿透嵌套 |
| `ObservableObject` | 旧式观察模型，配 `@StateObject`/`@ObservedObject` |
| `.task` | 随视图生命周期启动和取消异步工作 |

## 37.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把 SwiftUI 视图当 UIKit 视图实例 | 视图是值描述，不是长期对象 |
| 在 `body` 里做重计算或副作用 | `body` 可能被频繁调用 |
| 用普通 `var` 存会变的界面状态 | 编译不过或每次重算被重置；用 `@State` |
| 给控件传值而不是传绑定 | 传 `$state`；否则输入是"只读"的 |
| 用 `@State` 保存共享模型却不加 `@Observable` | 数据改了界面不刷新 |
| 嵌套模型没标 `@Observable` 却指望刷新 | 追踪不穿透 |
| 让子视图直接修改父值 | 通过 `@Binding` 明确通道 |
| 把窗口级逻辑写进视图 | `Scene` 管窗口，视图只管内容 |
| 在命令行程序里期待 SwiftUI 弹窗 | 需要真正的 App 生命周期；命令行只能类型检查 |
| `.task` 中忘记取消和错误处理 | 视图消失会取消，错误仍需显式处理 |

## 37.10 下章预告

下一章做一个综合项目：支出记录器。模型、存储、异步、测试、命令行和错误处理会组合到一个可扩展的小系统里，展示如何把语言知识变成工程结构。

> 如果你打算认真做界面开发，建议在读完第 38 章的综合作品后，回到[第七篇 SwiftUI]({{< relref "../Part-7-SwiftUI/_index.md" >}})。这一章只是把 SwiftUI 的齿轮装上；第七篇用八章篇幅把视图心智模型、状态所有权、布局谈判、列表与导航、表单校验、动画、异步数据以及预览与发布逐个讲透。
