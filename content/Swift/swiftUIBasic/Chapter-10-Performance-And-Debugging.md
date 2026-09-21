+++
title = "第 10 章 性能与调试"
weight = 100
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "body 调用次数为什么是误导性指标、_printChanges 怎么用、Lazy 容器的真正边界、以及 SwiftUI 里真正值得优化的四件事"
isCJKLanguage = true
draft = false
+++

# 第 10 章：性能与调试

> 这一章要先把一个流传极广的说法拆掉：**"`body` 被调用太多次所以卡"**——这句话基本是错的。搞清楚为什么错，你才知道该优化什么。

## 10.1 先看实测：`body` 到底被调用几次

我写了一个带计数器的版本，在三种情形下数 `body` 的调用次数：

🔬 **实测结果**

| 情形 | `body` 调用次数 |
| --- | --- |
| 同一棵视图树，**反复布局 3 次** | `PlainParent: 1`、`Leaf: 1` |
| 连续**构建 5 棵全新视图树**（参数不同） | `PlainParent: 5`、`Leaf: 5` |

第一个结果最关键：**同一棵树反复布局，`body` 只跑了 1 次。**

💭 为什么？因为布局（`layoutSubtreeIfNeeded`）走的是**布局协议**（第 3 章那三步协商），它问的是视图已经算好的尺寸，**不需要重新执行 `body`**。`body` 只在"这个视图需要重新生成描述"时才跑——也就是它的输入（存储属性、读到的状态）变了的时候。

⚠️ 第二个结果（5 次）不代表"性能问题"。那 5 次是**5 棵不同的树**，每次构建本来就要算一次描述。这是正常的、无法避免的成本。

🔥 **所以"`body` 被调用了 N 次"这个数字本身说明不了任何问题。** 真正该问的是两个别的问题：

| 该问的问题 | 而不是 |
| --- | --- |
| 每次 `body` 执行时，**里面干了多少活**？ | `body` 被调用了几次？ |
| 有没有**昂贵的东西**被放进了 `body`？ | 视图结构体被创建了几个？ |

### `body` 的代价在哪

| 放进去的东西 | 代价 |
| --- | --- |
| `Text`、`HStack`、`.padding()` | ✅ 几乎为零——创建结构体而已 |
| `print` / 日志 | 🚧 便宜，但会污染控制台、也会拖慢（同步 I/O） |
| 排序/筛选一个大数组 | 🛑 **每次都重排**，这才是真瓶颈 |
| 格式化日期/数字 | 🚧 有成本，考虑缓存或交给 `Text` 的格式化（它是延迟求值的） |
| 发网络请求 / 读文件 | 🛑 绝对不能放在这里 |
| 构造一个 `DateFormatter` | 🛑 它很贵，必须做成 `static let` 复用 |

🔥 **一条经验规则**：`body` 里只做"摆布局、读状态"。任何"计算"都应该放进模型（`@Observable` 类）里，或者在属性变化时算一次存起来。

## 10.2 `Self._printChanges()`：找出"为什么刷新了"

这是 SwiftUI 自带的诊断方法，在 `body` 开头调用，它会把**这次 `body` 为什么被调用**打到控制台。

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        let _ = Self._printChanges()        // 🔥 只在调试时加，定位完就删
        VStack {
            Text("\(count)")
            Button("加一") { count += 1 }
        }
    }
}
```

输出形如：

```text
CounterView: _count changed.
```

| 输出里的原因 | 含义 | 你能做什么 |
| --- | --- | --- |
| `_count changed.` | 某个**具体属性**变了（这里是 `@State` 的 `_count`） | 正常，符合预期 |
| `@self changed.` | 这个视图**自身**被换了（父视图传了不同的值，或身份变了） | 检查是否传了每次都新建的值 |
| `@identity changed.` | **身份变了**（`.id()` 变了，或结构位置变了） | 回顾第 6 章——状态会被重建 |

⚠️ 三种原因要分清，因为**处理方式完全不同**：

- 看到具体属性名 → 说明状态变化传播正常，不用管；
- 看到 `@self changed` 但你觉得"什么都没变" → 多半是父视图传进来一个**每次新建的值**（比如 `ChildView(config: Config())`，或者传了个闭包字面量）；
- 看到 `@identity` → 找 `.id(...)`。

🔬 第 6 章里那个身份实验的原始输出就是这个格式：

```text
Child: @self, @identity, __n changed.
```

一行里三种原因同时出现——它告诉你"这个视图既被换了、身份也变了、而且状态也变了"。

💭 这是排查"界面莫名刷新"的**第一把工具**。它比任何第三方工具都直接，因为它来自框架内部。

## 10.3 让 SwiftUI 少干活的三个手段

### 手段一：`EquatableView` / `.equatable()`——让"内容相等"挡住重算

如果某个子视图的 `body` 很重，而它的输入**在值上相等**时不需要重算，可以让它遵守 `Equatable`：

```swift
struct Item: Identifiable, Hashable {
    let id = UUID()
    var title: String
    var subtitle: String
}

struct ExpensiveRow: View, Equatable {
    let item: Item

    var body: some View {
        // 假设这里是复杂布局
        VStack(alignment: .leading) {
            Text(item.title).font(.headline)
            Text(item.subtitle).font(.caption)
        }
    }
    // 编译器自动合成 ==（只要所有存储属性都是 Equatable）
}

struct ListUsingIt: View {
    let items: [Item]

    var body: some View {
        List {
            ForEach(items) { item in
                ExpensiveRow(item: item).equatable()   // ← 包一层 .equatable()
            }
        }
    }
}
```

⚠️ **严格说清楚它做什么**：`.equatable()` 让 SwiftUI 在父视图重新求值时，**先用 `==` 比较新旧值**——相等就跳过这个子视图的 `body`。

⚠️ 而这**只在同一棵视图树内**有意义。🔬 我实测过：连续构建 5 棵**全新**的树时，`.equatable()` 版本和普通版本的 `body` 调用次数**完全一样**（都是 5 次）——因为新树没有"旧值"可比，必然要算。**所以别指望它加速首次渲染。**

💭 什么时候值得用：同一个列表**频繁局部更新**（比如每秒刷新一行行情），而你确认了那个子视图的 `body` 是热点（用 Instruments 测过）。

### 手段二：`Lazy` 容器——只渲染可见的部分

```swift
struct Row: View {
    let index: Int
    var body: some View { Text("#\(index)") }
}

struct LongList: View {
    var body: some View {
        ScrollView {
            LazyVStack {                       // ← Lazy：只为可见区域创建视图
                ForEach(0..<10_000, id: \.self) { i in
                    Row(index: i)
                }
            }
        }
    }
}
```

| 容器 | 行为 |
| --- | --- |
| `VStack` / `HStack` | **一次性创建所有子视图**，全部塞进内存 |
| `LazyVStack` / `LazyHStack` | 只为可见（及预取范围）创建，滚出去就回收 |
| `List` | 本身就是懒的，而且有平台原生外观 |

⚠️ **`Lazy` 的边界要清楚**：它省的是"视图创建与布局"，**不省"数据准备"**。如果你在 `ForEach` 的闭包外面先把 10000 条数据全部算好了，那部分开销一点没少。

```swift
// 🛑 数据先全算完了，Lazy 只帮你省了视图
let parsed = rawItems.map { expensiveParse($0) }
ScrollView { LazyVStack { ForEach(parsed) { Row($0) } } }

// ✅ 把解析也推迟到"这一行真正要显示时"
ScrollView {
    LazyVStack {
        ForEach(rawItems) { raw in
            Row(raw)               // 在 Row 的 body 里才解析
        }
    }
}
```

💭 另一个常见误用：**`LazyVStack` 里套 `GeometryReader` 做高度测量**。`GeometryReader` 会吞掉它需要的空间，导致懒加载容器无法正确估算高度，滚动条会乱跳。这种情况要么改成固定高度，要么用 `List`。

### 手段三：把"贵的东西"挪出 `body`

| 从 `body` 里搬走 | 搬到哪 |
| --- | --- |
| 排序 / 筛选 | 模型里，数据变化时算一次 |
| `DateFormatter` / `NumberFormatter` | `static let`（**只建一次**） |
| 图片解码 / 缩放 | 后台任务，结果存起来 |
| 网络请求 | `.task`（第 9 章） |

🔬 一个具体的例子——`DateFormatter` 的构造非常贵：

```swift
// 🛑 每次 body 都新建一个 Formatter
var body: some View {
    let f = DateFormatter()
    f.dateFormat = "yyyy-MM-dd"
    return Text(f.string(from: date))
}

// ✅ 优先用 SwiftUI 的格式化（它内部处理好了）
var body: some View {
    Text(date, format: .dateTime.year().month().day())
}

// ✅ 或者复用一个 static formatter
private static let formatter: DateFormatter = {
    let f = DateFormatter()
    f.dateFormat = "yyyy-MM-dd"
    return f
}()
var body: some View {
    Text(Self.formatter.string(from: date))
}
```

## 10.4 `AnyView`：为什么它会拖慢

第 7 章提过一句"别为省事上 `AnyView`"，这里说清原因。

⚠️ 先说清楚：**下面这段能编译，问题全在性能和身份上。**

```swift
enum Kind { case a, b }

// 🚧 类型被擦除（不是编译错误，是代价）
func icon(for kind: Kind) -> AnyView {
    switch kind {
    case .a: AnyView(Image(systemName: "a"))
    case .b: AnyView(Image(systemName: "b"))
    }
}
```

`AnyView` 是一层**运行期的类型盒子**。它的代价有三层：

| 代价 | 说明 |
| --- | --- |
| 额外分配与间接调用 | 每次读取都要拆盒子 |
| **摧毁视图身份** | 盒子的具体类型对 SwiftUI 不可见，身份判断和差分效率下降 |
| 动画/转场可能失效 | 身份不稳定 → 该是"变形"的变成了"换了一个" |

🔥 **正解是用 `@ViewBuilder`**：它让编译器生成 `_ConditionalContent`（第 1 章讲过），类型信息完整保留、身份稳定。

```swift
enum Kind { case a, b }

// ✅ 类型信息保留
@ViewBuilder
func icon(for kind: Kind) -> some View {
    switch kind {
    case .a: Image(systemName: "a")
    case .b: Image(systemName: "b")
    }
}
```

⚠️ `AnyView` 唯一合理的场景：**类型确实无法在编译期表达**（比如从同构的配置数据动态构造视图树）。这时应该：
1. 在注释里写明为什么必须用它；
2. 用 `id(...)` 给它一个稳定身份；
3. 确认这是热点之外的地方。

## 10.5 工具：什么时候该用哪个

| 症状 | 先用什么 | 再用什么 |
| --- | --- | --- |
| 界面莫名刷新 | `Self._printChanges()` | 检查父视图传值、`.id()` |
| 滚动卡顿 | Instruments 的 **Time Profiler** | 看 `body` 里的排序/筛选 |
| 内存一直涨 | Xcode 的 **Memory Graph** | 找循环引用（第 10 章之外的内容见 [Swift 速查表]({{< relref "../CheatSheet/10-Memory-and-Value-Semantics.md" >}})） |
| 启动慢 | Instruments 的 **App Launch** | 看有没有在启动时读大文件 |
| 不确定哪里慢 | **先用 Time Profiler 测** | 别猜 |

🔥 **最重要的一条纪律：先测再改。**

SwiftUI 的性能直觉特别不准——因为框架做了大量你看不见的优化（差分、懒加载、图层合并），所以"看起来应该很慢"的代码常常很快，而"看起来没事"的代码（比如 `body` 里一个 `filter`）可能是真瓶颈。

💭 一个具体的反例：**把 `VStack` 改成 `LazyVStack` 常常不会变快，还会变慢。**
因为 `LazyVStack` 要维护"当前可见范围"的状态、滚动时不断创建/销毁视图；如果只有十几个元素，一次性创建反而更快更稳。**只有元素数量确实很大（几百以上）时才值得上 `Lazy`。**

### 一个可以在代码里用的简易计时

不方便开 Instruments 时，`ContinuousClock` 是最轻的测量手段（见 [Swift 速查表第 11 章]({{< relref "../CheatSheet/11-Standard-Library.md" >}})）：

```swift
let clock = ContinuousClock()
let elapsed = clock.measure {
    _ = (1...100_000).reduce(0, +)
}
print("耗时：\(elapsed)")
```

⚠️ 但它只能测**你包起来的那段代码**——用了它你就会漏掉"你没想到要看"的地方。真要定位瓶颈，还是 Instruments。

## 10.6 完整可运行文件

这个例子把三种诊断手段都放进去了：

```swift
import SwiftUI

struct Row: View, Equatable {
    let index: Int

    var body: some View {
        // 🔬 打开这行可以看到每次 body 执行
        // let _ = Self._printChanges()
        HStack {
            Text("#\(index)")
                .monospacedDigit()
            Spacer()
            Text(Date.now, format: .dateTime.hour().minute().second())
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}

struct PerformanceLab: View {
    @State private var count = 100
    @State private var useLazy = true
    @State private var tick = 0

    var body: some View {
        VStack(spacing: 0) {
            Form {
                Section("诊断实验") {
                    Stepper("元素数量：\(count)", value: $count, in: 10...5000, step: 10)
                    Toggle("使用 LazyVStack", isOn: $useLazy)
                    Text("元素少时把 Lazy 关掉，滚动会更顺——Lazy 不是免费的。")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
            .frame(height: 180)

            Divider()

            ScrollView {
                if useLazy {
                    LazyVStack(spacing: 8) {
                        ForEach(0..<count, id: \.self) { i in
                            Row(index: i).equatable()
                        }
                    }
                    .padding()
                } else {
                    VStack(spacing: 8) {
                        ForEach(0..<count, id: \.self) { i in
                            Row(index: i)
                        }
                    }
                    .padding()
                }
            }
        }
    }
}

#Preview {
    PerformanceLab()
}
```

> 📦 这一段是 `View` + `#Preview`，**没有 `@main`**：新建 `Chapter10.swift` 放进 Xcode 的 App 项目，再把 App 文件里的 `WindowGroup { ContentView() }` 改成 `WindowGroup { PerformanceLab() }`；只想看效果就直接看 `#Preview`——预览不需要入口。

💭 建议这样玩这个文件：

1. **把元素数量拉到 5000**，对比开/关 `LazyVStack` 的滚动流畅度；
2. **把数量降回 20**，再对比一次——你会发现这时关掉 Lazy 反而更顺；
3. **打开 `Row` 里那行 `_printChanges()`**，滚动时看控制台输出——你会发现滚动**不会**触发 `body`（因为懒加载容器复用了已有的行视图）。

## 10.7 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| 盯着"`body` 被调用了几次" | 🔬 反复布局**不会**重跑 `body`（实测 3 次布局 = 1 次调用）；这个数字本身无意义 | 关注 `body` 里的**工作量** |
| 在 `body` 里排序/筛选大数组 | 每次重算都排一次 | 放进模型，数据变化时算一次 |
| 在 `body` 里 `DateFormatter()` | 构造非常贵，每次都建 | 用 `Text(date, format:)`，或 `static let` 复用 |
| 所有列表都上 `LazyVStack` | 元素少时更慢（要维护可见范围），滚动可能更差 | 数量大（几百+）才用 |
| 在 `LazyVStack` 里用 `GeometryReader` 测高度 | 高度估算失败，滚动条乱跳 | 固定行高，或改用 `List` |
| 用 `AnyView` 做分支返回 | 摧毁视图身份、动画失效、多一层间接 | 用 `@ViewBuilder` |
| `EquatableView` 以为能加速首屏 | 🔬 跨树构建时调用次数完全一样（实测都是 5 次） | 它只在同一棵树内、值相等时省一次重算 |
| 凭直觉优化 | SwiftUI 有大量看不见的优化，直觉常常反 | 先用 Time Profiler 测 |
| 忘了删掉 `_printChanges()` | 控制台被刷爆、也有开销 | 定位完就删 |

## 10.8 下一章

性能讲完了。接下来的两章处理"这个界面除了你自己的机器，还能不能好好工作"：

- **第 11 章 可访问性与适配**：动态字体、旁白、深色模式、不同尺寸的屏幕——以及怎么在写代码的同时就把这些做好；
- **第 12/13 章 绘制与特效**：`Shape`、`Path`、`Canvas`、材质、混合模式——把界面从"整齐"做到"好看"。
