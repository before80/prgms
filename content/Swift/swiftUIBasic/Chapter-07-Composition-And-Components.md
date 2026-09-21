+++
title = "第 7 章 组件化：从一堆修饰符到一个零件"
weight = 70
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "把重复的修饰符、重复的布局、重复的交互各抽成一种东西：ViewModifier、@ViewBuilder 容器、Style 协议，以及怎么选"
isCJKLanguage = true
draft = false
+++

# 第 7 章：组件化

> 前六章解决的是"一个界面怎么正确做出来"。这一章解决另一个问题：**做第二个界面时，怎么不把第一个界面的代码抄一遍。**

## 7.1 先从最烦的事开始

写到一个真实 App 的中期，你的代码里会长出这种东西：

```swift
// 第 1 处
Text("余额").padding(12).background(.white, in: RoundedRectangle(cornerRadius: 10)).shadow(radius: 2)
// 第 2 处
Text("本月支出").padding(12).background(.white, in: RoundedRectangle(cornerRadius: 10)).shadow(radius: 2)
// 第 3 处……第 30 处
```

那个 `.padding(12).background(.white, in: RoundedRectangle(cornerRadius: 10)).shadow(radius: 2)` 就是**一个已经存在、但还没有名字的组件**。

第 1 章讲过"通用修饰符是包壳"（`ModifiedContent`），当时那只是理解布局的钥匙。现在它变成了一把工程上的刀：**既然是一层壳，就能给它起个名字。**

⚠️ 但要小心一个常见误区：**组件化不是"把重复的代码抽成函数"那么简单。** SwiftUI 里"重复的东西"分三类，抽法完全不同：

| 重复的是什么 | 抽成什么 | 本章位置 |
| --- | --- | --- |
| 一串**修饰符**（外观） | `ViewModifier` | 7.2 |
| 一段**布局结构**（容器） | 泛型容器视图 | 7.4 |
| 一套**交互行为**（控件长什么样、怎么响应） | `Style` 协议 | 7.5 |

抽错了类型，代码会变得比不抽更难维护。这一章就是把这三种分清楚。

## 7.2 `ViewModifier`：给一串修饰符起名字

### 最小可用形态

```swift
import SwiftUI

struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.white, in: RoundedRectangle(cornerRadius: 10))
            .shadow(color: .black.opacity(0.08), radius: 2, y: 1)
    }
}
```

用的时候：

```swift
Text("余额").modifier(CardStyle())
```

⚠️ **第 1 个反直觉点**：`body(content:)` 的参数叫 `content`，类型是 `Content`——它是**调用方的那个视图**。所以 `ViewModifier` 的本质不是"提取样式"，而是"**声明"我要把这个视图包起来"**。`content` 出现的位置决定了一切：

```swift
struct A: ViewModifier {
    func body(content: Content) -> some View {
        content.padding()          // 内边距加在内容外面 ✅
    }
}
struct B: ViewModifier {
    func body(content: Content) -> some View {
        Color.red.overlay(content) // content 变成了"叠上去的那层"
    }
}
```

💭 一个方便的记忆法：**`ViewModifier` 的 `body` 里，`content` 就是"你原来写的那个东西"。** 你把它放在哪，它就出现在哪。

### 加一层语法糖：`View` 扩展

`Text("余额").modifier(CardStyle())` 里的 `.modifier(...)` 有点啰嗦。惯例是再包一个扩展：

```swift
extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
}
```

现在可以用得跟内置修饰符一样：

```text
Text("余额").cardStyle()
Text("本月支出").cardStyle()
```

🔥 这一步是**社区标准做法**：`ViewModifier` 负责实现，`View` 扩展负责调用体验。库作者几乎都这么写。

⚠️ 命名建议：**给修饰符起一个"形容词"名字**（`cardStyle()`、`primaryButton()`），而不是"动作"名字（`addPaddingAndBackground()`）。因为调用点上它读起来是在描述结果，这和 SwiftUI 的声明式风格一致。

### 带参数的修饰符

```swift
struct BadgeStyle: ViewModifier {
    let color: Color
    var compact: Bool = false

    func body(content: Content) -> some View {
        content
            .font(compact ? .caption2 : .caption)
            .padding(.horizontal, compact ? 4 : 8)
            .padding(.vertical, 2)
            .background(color.opacity(0.15), in: Capsule())
            .foregroundStyle(color)
    }
}

extension View {
    func badge(_ color: Color = .blue, compact: Bool = false) -> some View {
        modifier(BadgeStyle(color: color, compact: compact))
    }
}
```

```text
Text("新增").badge(.green)
Text("3").badge(.red, compact: true)
```

💭 给参数**默认值**很重要——它让"最常用的那种"变成零参数调用，同时也保留了全部灵活性。

### 什么时候**不该**用 `ViewModifier`

| 情况 | 更好的做法 |
| --- | --- |
| 只有一处用到 | 别抽。抽了只会让你少看一层就要跳一次文件 |
| 抽完参数超过 4 个 | 它在表达"好几种不同的东西"，考虑拆成多个，或换成容器视图 |
| 需要读被包装视图的**布局结果** | `ViewModifier` 拿不到 content 的尺寸。用 `Layout`（第 4 章）或 `GeometryReader` |
| 需要往**上层**传信息 | 用 `PreferenceKey`（7.6 节） |

🔥 最后一条值得记：**`ViewModifier` 是"向下包"，不是"向上报"。** 数据流方向和它的能力绑定死了。

## 7.3 `@ViewBuilder`：让一个参数收下多个视图

从第 1 章开始你就一直在用 `@ViewBuilder`（`VStack { }` 里那个花括号就是它），但一直没说它到底是什么。

它的作用是：**允许这个参数接受"若干行视图"，然后自动打包成一个值。**

```text
@ViewBuilder var content: Content      // 声明长这样，Content 是泛型参数
```

如果没有 `@ViewBuilder`，你就只能传一个视图；有了它，可以写多行、`if`、`switch`、`ForEach`。

### 手动用一次

```swift
struct Row<Content: View>: View {              // ← 泛型参数
    var title: String
    @ViewBuilder var accessory: Content        // ← 存储属性用泛型参数

    var body: some View {
        HStack {
            Text(title)
            Spacer()
            accessory
        }
    }
}
```

调用方可以传 0 行、1 行或多行：

```swift
VStack {
    Row(title: "静音") { Image(systemName: "speaker.slash") }
    Row(title: "纯文本") { }                    // 什么都不传也合法
    Row(title: "两个图标") {
        Image(systemName: "star")
        Image(systemName: "heart")
    }
}
```

⚠️ 注意上面 `Row` 的声明里那**两个**关键点，缺一个都编译不过：

| 写法 | 结果 |
| --- | --- |
| `struct Row<Content: View>` + `@ViewBuilder var accessory: Content` | ✅ |
| `struct Row` + `@ViewBuilder var accessory: some View` | 🛑 `property declares an opaque return type, but has no initializer expression from which to infer an underlying type` |
| `struct Row` + `@ViewBuilder var accessory: some View { ... }` | ✅ 但这是**计算属性**，调用方传不了内容 |

### `@ViewBuilder` 支持哪些写法

| 你写的 | 打包成 | 类型确定吗 |
| --- | --- | --- |
| 一行 | 就是那个视图 | ✅ |
| 多行 | `TupleView<(...)>` | ✅ |
| `if`（无 else） | `Optional<A>` | ✅ |
| `if/else` | `_ConditionalContent<A, B>` | ✅ |
| `switch` | 嵌套的 `_ConditionalContent` | ✅ |
| 空 | `EmptyView` | ✅ |

⚠️ 关键限制：**分支数量有限制**。`_ConditionalContent` 是"二选一"的嵌套结构，所以：

- 2 个分支 → 1 层嵌套，没问题；
- 10 个分支 → 9 层嵌套，**类型检查器会变得很慢，甚至报"expression too complex"**。

🔥 分支超过 4~5 个时，改用 `switch` 里返回同一种包装类型、或者干脆查表：

```text
// 🛑 10 个 if/else 分支 —— 类型检查器要展开 9 层 ConditionalContent
@ViewBuilder var icon: some View {
    if kind == .a { Image(systemName: "a") }
    else if kind == .b { Image(systemName: "b") }
    // …… 再来 8 个
}

// ✅ 先算出名字，再走一个分支
var icon: some View {
    let name: String = switch kind {
        case .a: "a"
        case .b: "b"
        default: "questionmark"
    }
    Image(systemName: name)
}
```

💭 这是个**真实的编译性能陷阱**，不是风格洁癖。SwiftUI 项目里"某个文件编译特别慢"，十有八九是某个 `body` 里的深嵌套 `if/else`。

### `@ViewBuilder` 也能用在计算属性上

```swift
struct StatusView: View {
    var isOn: Bool

    @ViewBuilder
    private var indicator: some View {          // 注意：计算属性上也能标
        if isOn {
            Label("运行中", systemImage: "checkmark.circle.fill").foregroundStyle(.green)
        } else {
            Label("已停止", systemImage: "pause.circle").foregroundStyle(.secondary)
        }
    }

    var body: some View {
        HStack { indicator; Spacer() }
    }
}
```

🔥 这是**拆大 `body` 的首选手法**：一个 `body` 超过一屏时，把里面的段落抽成带 `@ViewBuilder` 的私有计算属性。比抽成子视图更轻——不需要传参数，直接读 `self` 的属性。

## 7.4 自定义容器：把布局结构也抽出来

`ViewModifier` 只能包装**一个**视图。如果要抽的是"**怎么排列多个子视图**"，就需要一个泛型容器：

```swift
struct SectionCard<Content: View>: View {
    var title: String
    @ViewBuilder var content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
            content                       // 调用方给的内容原样放进来
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.background, in: RoundedRectangle(cornerRadius: 12))
        .overlay(RoundedRectangle(cornerRadius: 12).stroke(.separator, lineWidth: 1))
    }
}
```

用法：

```swift
SectionCard(title: "本月概览") {
    Text("支出 ¥3,240")
    Text("收入 ¥12,000")
    Divider()
    Text("结余 ¥8,760").bold()
}
```

### 三个必须注意的点

**① 存储属性必须用泛型参数，不能用 `some View`。**

```swift
struct SectionCard<Content: View>: View {     // ← 泛型参数
    var title: String
    @ViewBuilder var content: Content          // ← 用 @ViewBuilder 收多行
    var body: some View { /* ... */ }
}
```

⚠️ 原因是：`some View` 是**不透明类型**，它需要一个初始化表达式来让编译器推断"到底是哪个类型"。而"由调用方传进来的内容"恰恰没有初始化表达式。所以：

```swift
// ✅ 计算属性 + some View：合法（有 body 表达式可供推断）
var badge: some View { Text("新") }

// ✅ 存储属性 + 泛型参数：合法（Content 是类型参数，由调用方确定）
struct Box<Content: View>: View {
    @ViewBuilder var content: Content
    var body: some View { content }
}

// 🛑 存储属性 + some View：不合法
struct Bad: View {
    @ViewBuilder var content: some View
    var body: some View { content }
}
```

```text
error: property declares an opaque return type, but has no initializer expression
       from which to infer an underlying type [#OpaqueTypeInference]
```

💭 一句话记：**`some View` 只配"有实现的"计算属性；要接收调用方传来的内容，必须写 `<Content: View>`。**

**② 用泛型会带来一个代价：类型膨胀。**

每个不同的 `Content` 都会生成不同的 `SectionCard<...>` 类型。如果 `SectionCard` 出现在一个 `List` 的 `ForEach` 里、每行的内容类型还不一样，编译器要为每种组合做类型检查。这就是"泛型容器用多了编译慢"的来源。

⚠️ 什么时候该换成 `AnyView`？**基本不该。** `AnyView` 会擦除类型、增加运行期开销、还让视图身份不稳定（影响动画和状态保留）。只有在"实在无法用泛型表达"时才用它，且要在注释里写明原因。

**③ 想让容器对子视图有更多控制，就上 `Layout`。**

泛型容器只能"把 content 放进去"。如果容器需要**逐个处理子视图**（比如自己做流式换行、或者给每个子视图加不同的间距），那就超出泛型容器的能力了——第 4 章的 `Layout` 协议才是那个工具。

| 需求 | 工具 |
| --- | --- |
| 把一段内容包起来，加点装饰 | `ViewModifier` |
| 接收若干行内容，按固定结构排列 | 泛型容器 + `@ViewBuilder` |
| 要按自己的算法摆放子视图 | `Layout` 协议 |
| 要做出 SwiftUI 里没有的**控件** | 7.5 的 `Style` 协议 |

## 7.5 `Style` 协议：自定义控件的"皮肤"

`Button`、`Toggle`、`Label`、`ProgressView` 这些控件都支持**换皮肤**，而且换皮肤之后**行为完全保留**（点击区域、高亮、无障碍、键盘支持等等）。

这就是 `Style` 协议系列存在的理由——它是"组件化"里最容易被忽略、但收益最大的一类。

### `ButtonStyle`：让按钮长得不一样但行为一样

```swift
struct PressableButtonStyle: ButtonStyle {
    var tint: Color = .accentColor

    func makeBody(configuration: Configuration) -> some View {
        configuration.label                    // ← 按钮的内容（你写的那个 Label）
            .font(.headline)
            .foregroundStyle(.white)
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .background(tint, in: RoundedRectangle(cornerRadius: 10))
            .scaleEffect(configuration.isPressed ? 0.96 : 1)      // ← 按下状态
            .opacity(configuration.isPressed ? 0.9 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}
```

```swift
Button("确认支付") { pay() }
    .buttonStyle(PressableButtonStyle(tint: .green))
```

🔥 **`ButtonStyle` 的核心价值**：`configuration` 给你两样东西——

| 成员 | 是什么 |
| --- | --- |
| `configuration.label` | 调用方写的按钮内容（`Text`、`Label`、`HStack` 都行） |
| `configuration.isPressed` | 当前是否按下 |
| `configuration.role` | 按钮的语义角色（`.destructive` 等，可用来换配色） |

⚠️ 注意：`ButtonStyle` 里**不能**用 `.buttonStyle()` 改回默认样式（会递归），要"基于默认样式改"得用 `.buttonStyle(.bordered)` 之后再用 `.tint()` 之类的修饰符调整。

💭 `ButtonStyle` 比"自己写一个 `HStack` + `.onTapGesture`"好在哪？

| | 自定义 ButtonStyle | 自己拼 HStack + onTapGesture |
| --- | --- | --- |
| 点击区域 | 自动包含整个 label 及 padding | 要自己保证 |
| 按下高亮 | `configuration.isPressed` | 要自己用 `DragGesture` 模拟 |
| 无障碍语义 | 自动是"按钮" | 要自己加 `.accessibilityAddTraits(.isButton)` |
| 键盘/辅助设备 | 自动支持 | 通常缺失 |
| 与系统一致性 | 好 | 差 |

⚠️ 这张表是**这一章最值钱的东西**：很多人为了"按钮长得特别点"就自己拼一个，结果悄悄丢掉了无障碍和辅助设备支持。**能用 Style 就用 Style。**

### 其他 `Style` 协议

| 协议 | 用于 | `Configuration` 提供 |
| --- | --- | --- |
| `ButtonStyle` | `Button` | `label`、`isPressed`、`role` |
| `PrimitiveButtonStyle` | 需要自己触发动作的按钮（如长按） | `label`、`trigger()` |
| `ToggleStyle` | `Toggle` | `isOn`（Binding）、`label` |
| `LabelStyle` | `Label` | `icon`、`title` |
| `ProgressViewStyle` | `ProgressView` | 进度相关 |
| `TextFieldStyle` | `TextField` | 有限，通常直接用修饰符 |
| `ListStyle` / `PickerStyle` | `List` / `Picker` | 一般是枚举而非自定义协议 |

### `PrimitiveButtonStyle`：需要自己决定"什么时候算点击"

普通 `ButtonStyle` 只改外观，动作仍由系统触发。想控制**触发时机**（长按、双击、拖动一定距离才算），要用 `PrimitiveButtonStyle`：

```swift
struct LongPressButtonStyle: PrimitiveButtonStyle {
    var minimumDuration: Double = 0.6

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding(.horizontal, 20).padding(.vertical, 12)
            .background(.red.opacity(0.15), in: RoundedRectangle(cornerRadius: 10))
            .onLongPressGesture(minimumDuration: minimumDuration) {
                configuration.trigger()          // ← 由你决定何时真正触发
            }
    }
}
```

⚠️ 关键区别：**`PrimitiveButtonStyle` 必须自己调用 `configuration.trigger()`**，否则按钮永远不会响应。而普通 `ButtonStyle` 里**不要**试图调用它（它没有这个方法）。

## 7.6 往上层传信息：`PreferenceKey`

前面说过 `ViewModifier` 是"向下包"。那如果子视图想把信息**报给祖先**（比如"我有多宽"，好让父视图决定布局）怎么办？

答案是 `PreferenceKey`——一条**自下而上**的数据通道。经典用例：测量某个视图的宽度。

```swift
import SwiftUI

struct WidthKey: PreferenceKey {
    static var defaultValue: CGFloat { 0 }          // ⚠️ 用计算属性，别用存储属性（见下）
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())             // 多个子视图上报时怎么合并
    }
}

struct MeasuredWidth: View {
    @State private var width: CGFloat = 0

    var body: some View {
        Text("量我的宽度")
            .background(
                GeometryReader { geo in
                    Color.clear.preference(key: WidthKey.self, value: geo.size.width)
                }
            )
            .onPreferenceChange(WidthKey.self) { width = $0 }
            .overlay(alignment: .bottom) {
                Text("宽 \(width, specifier: "%.0f")pt")
                    .font(.caption2).foregroundStyle(.secondary)
            }
    }
}
```

⚠️ **Swift 6 严格并发下的一个真实陷阱**：`defaultValue` 如果写成**存储属性**，会直接报错：

```swift
struct WidthKey: PreferenceKey {
    static var defaultValue: CGFloat = 0            // 🛑
    // error: static property 'defaultValue' is not concurrency-safe because it is
    //        nonisolated global shared mutable state [#MutableGlobalVariable]
}
```

🔬 **正确写法是用计算属性**，因为协议只要求 `{ get }`：

```text
static var defaultValue: CGFloat { 0 }              // ✅ 零警告（放进 WidthKey 里）
```

💭 这个坑很典型：**协议要求只读的属性，就别写成可变存储属性。** 既满足协议，又避开共享可变状态。

### 什么时候该用 `PreferenceKey`

| 场景 | 说明 |
| --- | --- |
| 子视图尺寸/位置回报给祖先 | 经典用法，比如"高亮当前选中的 Tab 下划线" |
| 多个子视图汇总一个值 | `reduce` 就是干这个的（取最大、求和、收集数组） |
| 自定义容器的布局参数收集 | 比如 `FlowLayout` 想提前知道所有子视图宽度 |
| 滚动偏移 | 老代码常用；现在优先用 `onScrollGeometryChange` 之类的新 API |

⚠️ 但 **`PreferenceKey` 是有成本的**：它会让 SwiftUI 多做一轮"收集—归并—回传"。能不用就不用——很多时候 `Layout` 协议（第 4 章）或者把状态提到共同祖先更直接。

💭 判据：**如果信息本来就能通过"把状态放在共同祖先"解决，就别用 `PreferenceKey`。** 它适合的是"子视图的**几何信息**必须自下而上流动"这种天然逆向的场景。

## 7.7 三种抽法怎么选：一张决策表

| 你手上重复的东西长什么样 | 抽成 | 关键词 |
| --- | --- | --- |
| `xxx.padding().background().clipShape()` | `ViewModifier` + `View` 扩展 | `content` 放哪 |
| 多行内容要塞进一个固定结构 | 泛型容器 + `@ViewBuilder` | `<Content: View>` |
| 控件的**外观**（点击行为不变） | `ButtonStyle` / `ToggleStyle` / `LabelStyle` | `Configuration` |
| 控件的**触发时机** | `PrimitiveButtonStyle` | `configuration.trigger()` |
| 要按自己的算法摆放子视图 | `Layout`（第 4 章） | `sizeThatFits` / `placeSubviews` |
| 子视图的信息要报给祖先 | `PreferenceKey` | `reduce` |

再补三条工程经验：

| 经验 | 理由 |
| --- | --- |
| **抽之前先问"有第三处了吗"** | 两处重复抽出来，往往第三个用例一出现就得重写 |
| **名字用"形容词"** | `cardStyle()` 比 `addCardBackground()` 更像 SwiftUI |
| **优先用 `Style` 协议而不是自己拼控件** | 保住无障碍、键盘、辅助设备支持 |

## 7.8 完整可运行文件

把这一章的东西拼成一个能跑的例子：

```swift
import SwiftUI

// ① ViewModifier：一串修饰符起个名字
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.background, in: RoundedRectangle(cornerRadius: 12))
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(.separator, lineWidth: 1))
    }
}

extension View {
    func cardStyle() -> some View { modifier(CardStyle()) }
}

// ② 泛型容器：接收多行内容，按固定结构排列
struct SectionCard<Content: View>: View {
    var title: String
    @ViewBuilder var content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title).font(.headline)
            content
        }
        .cardStyle()
    }
}

// ③ ButtonStyle：换外观，保行为
struct PressableButtonStyle: ButtonStyle {
    var tint: Color = .accentColor

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline)
            .foregroundStyle(.white)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background(tint, in: RoundedRectangle(cornerRadius: 10))
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .opacity(configuration.isPressed ? 0.9 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}

// ④ LabelStyle：图标和标题的排法
struct CompactLabelStyle: LabelStyle {
    func makeBody(configuration: Configuration) -> some View {
        HStack(spacing: 4) {
            configuration.icon
            configuration.title
        }
        .font(.subheadline)
    }
}

// ⑤ PreferenceKey：子视图把宽度报给祖先
struct WidthKey: PreferenceKey {
    static var defaultValue: CGFloat { 0 }
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

struct Chapter07Demo: View {
    @State private var measured: CGFloat = 0

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {

                SectionCard(title: "本月概览") {
                    Label("支出 ¥3,240", systemImage: "arrow.up.right").labelStyle(CompactLabelStyle())
                    Label("收入 ¥12,000", systemImage: "arrow.down.left").labelStyle(CompactLabelStyle())
                    Divider()
                    Text("结余 ¥8,760").bold()
                }

                SectionCard(title: "测量的宽度") {
                    Text("这段文字的宽度会被量出来")
                        .background(
                            GeometryReader { geo in
                                Color.clear.preference(key: WidthKey.self, value: geo.size.width)
                            }
                        )
                    Text("实测宽 \(measured, specifier: "%.0f")pt")
                        .font(.caption).foregroundStyle(.secondary)
                }
                .onPreferenceChange(WidthKey.self) { measured = $0 }

                Button("确认支付") { }
                    .buttonStyle(PressableButtonStyle(tint: .green))

                Button(role: .destructive) { } label: {
                    Text("删除账户")
                }
                .buttonStyle(PressableButtonStyle(tint: .red))

                // 同一个 ButtonStyle，配上系统样式做对照
                Button("系统样式对照") { }
                    .buttonStyle(.borderedProminent)
            }
            .padding()
        }
    }
}

#Preview {
    Chapter07Demo()
}
```

> 📦 这一段是 `View` + `#Preview`，**没有 `@main`**：新建 `Chapter07.swift` 放进 Xcode 的 App 项目，再把 App 文件里的 `WindowGroup { ContentView() }` 改成 `WindowGroup { Chapter07Demo() }`；只想看效果就直接看 `#Preview`——预览不需要入口。

💭 跑起来重点看**最后两个按钮**：它们用了同一个 `PressableButtonStyle`，只是 `tint` 不同，但**点击、按下反馈、无障碍语义、键盘操作全都正常**——这就是"用 `ButtonStyle` 而不是自己拼 `HStack`"的价值。

## 7.9 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| 存储属性写 `@ViewBuilder var c: some View` | `property cannot have an opaque type` | 存储属性用 `<Content: View>` 泛型参数；`some View` 只配计算属性 |
| 一个 `body` 里堆 10 个 `if/else` 分支 | 类型检查器展开多层 `_ConditionalContent`，编译变慢甚至 "too complex" | 改成查表 + 一个分支，或拆成子视图 |
| 为了按钮好看，自己拼 `HStack` + `onTapGesture` | 悄悄丢掉无障碍语义、按下反馈、辅助设备支持 | 用 `ButtonStyle` |
| `PrimitiveButtonStyle` 里忘了 `configuration.trigger()` | 按钮永远不响应 | 在你认为该触发的地方显式调用 |
| 泛型容器到处用 | 每个组合都生成一个新类型，类型检查变慢 | 只在真的需要多行内容时用；别为省事上 `AnyView` |
| `PreferenceKey.defaultValue` 写成存储属性 | Swift 6 下报 `not concurrency-safe ... #MutableGlobalVariable` | 写成计算属性 `static var defaultValue: T { ... }` |
| 用 `PreferenceKey` 传普通状态 | 多一轮收集归并，绕远路 | 状态提到共同祖先就好 |
| 有一处重复就急着抽象 | 第三个用例出现时通常要重写 | 等第三处 |

## 7.10 下一章

到这里，"怎么把界面写对、写好、组装起来"这条线走完了。剩下两个大问题：

- **数据从哪来、存到哪去**——模型怎么持久化，网络请求的"加载中/成功/失败"三态怎么建得干净；
- **多个页面怎么组织**——`List`、`NavigationStack`、弹窗家族怎么配合，以及"什么才叫一个能用的列表"。

下一章先解决数据落地。
