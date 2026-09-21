+++
title = "第 11 章 可访问性与适配"
weight = 110
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "把字号调到最大、打开旁白、切换深色模式之后，你的界面还站得住吗——动态字体、语义标签、颜色与动效偏好、尺寸类适配"
isCJKLanguage = true
draft = false
+++

# 第 11 章：可访问性与适配

> 前面十章都在让界面"在你自己的机器上好看"。这一章处理一件更实际的事：**换一个用户、换一套系统设置，它还站得住吗。**
>
> 💭 这不是"加分项"。把字号调大是很多人的日常需求，旁白是视障用户唯一的入口——这些功能坏了，等于对一部分用户直接关门。

## 11.1 动态字体：不写死字号

SwiftUI 最贴心的一点是：**用系统的语义字号（`.title`、`.body`、`.caption`）时，动态字体自动生效**，你什么都不用做。

```swift
VStack(alignment: .leading) {
    Text("标题").font(.title)          // ✅ 跟随系统字号设置
    Text("正文").font(.body)           // ✅
    Text("说明").font(.caption)        // ✅
}
```

⚠️ 而**写死数值**就断掉了这条链：

```swift
Text("正文").font(.system(size: 17))   // 🚧 永远是 17pt，用户调大字号它不变
```

| 写法 | 跟随动态字体 |
| --- | --- |
| `.font(.body)`、`.font(.title)` | ✅ 自动 |
| `.font(.system(.body, design: .rounded))` | ✅ 自动（保留语义样式） |
| `.font(.system(size: 17))` | ❌ 固定值 |
| `.font(.custom("MyFont", size: 17))` | ❌ 固定值（要配合 `relativeTo:`） |
| `.font(.custom("MyFont", size: 17, relativeTo: .body))` | ✅ 相对缩放 |

🔥 **判据**：**宁可写 `.body` 也不要写 `17`。** 需要自定义字体时，用 `relativeTo:` 把缩放接回来。

### 空间也要跟着缩放

字号变大了，间距和内边距如果不跟着变，界面会挤爆。`@ScaledMetric` 就是干这个的：

```swift
struct Badge: View {
    @ScaledMetric(relativeTo: .body) private var padding: CGFloat = 8
    @ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 16

    var body: some View {
        HStack(spacing: padding) {
            Image(systemName: "star").font(.system(size: iconSize))
            Text("精选").font(.body)
        }
        .padding(.horizontal, padding)
        .background(.yellow.opacity(0.3), in: Capsule())
    }
}
```

`8` 和 `16` 是"标准字号下的值"，系统会按用户的设置等比放大。这样字号和间距同步变化，布局比例保持住。

### 测试方法：把字号调到最大

| 平台 | 怎么调 |
| --- | --- |
| iOS 模拟器 | 设置 → 辅助功能 → 显示与文字大小 → 更大字体 |
| Xcode 预览 | 用 `.environment(\.dynamicTypeSize, .accessibility3)` 直接改 |
| macOS | 系统设置 → 辅助功能 → 显示 → 文字大小 |

预览里最省事：

```swift
#Preview("正常字号") {
    Badge()
}
#Preview("超大字号") {
    Badge().environment(\.dynamicTypeSize, .accessibility3)
}
```

🔥 **养成习惯：每个自建组件都配一个"超大字号"预览。** 它能在你写代码的当下就暴露布局问题，比等到测试阶段便宜一百倍。

### 大字号下的布局策略

字号一大，横排就放不下了。这正是第 4 章讲的 `ViewThatFits` 的主场：

```swift
struct ResponsiveRow: View {
    let title: String
    let detail: String

    var body: some View {
        ViewThatFits {
            HStack {                              // 首选：横排
                Text(title)
                Spacer()
                Text(detail).foregroundStyle(.secondary)
            }
            VStack(alignment: .leading) {         // 放不下：改竖排
                Text(title)
                Text(detail).foregroundStyle(.secondary)
            }
        }
    }
}
```

💭 另一个常用手段是读环境值自己判断：

```swift
struct Header: View {
    let title: String
    let detail: String

    @Environment(\.dynamicTypeSize) private var typeSize

    var isLargeText: Bool { typeSize >= .accessibility1 }

    var body: some View {
        if isLargeText {
            VStack(alignment: .leading) {          // 大字用竖排
                Text(title)
                Text(detail).foregroundStyle(.secondary)
            }
        } else {
            HStack {                                // 正常字号用横排
                Text(title)
                Spacer()
                Text(detail).foregroundStyle(.secondary)
            }
        }
    }
}
```

⚠️ 但**优先用 `ViewThatFits`**——它按"实际能不能放下"判断，比按"字号阈值"判断更准确（因为同样的字号在不同宽度下结果不同）。

## 11.2 语义标签：让旁白能读懂你的界面

旁白（VoiceOver）用户看不到你的界面，只能听。所以**每一个有意义的元素都要能被读出来**。

### 系统控件通常已经做好了

```text
Button("保存") { save() }                    // ✅ 自动读作"保存，按钮"
Toggle("静音", isOn: $muted)                 // ✅ 自动读作"静音，开关，关闭"
Slider(value: $volume, in: 0...1)            // ✅ 自动读作"滑块，50%"
Text("你好")                                  // ✅ 直接读文本
```

🔥 **用系统控件，无障碍基本是白送的。** 这是第 7 章"能用 `ButtonStyle` 就别自己拼按钮"的又一个理由。

### 需要自己标的情况

**① 图片（尤其是有信息量的）**

```swift
Image(systemName: "star.fill")
    .accessibilityLabel("已收藏")               // ← 图标本身读不出含义
```

**② 纯装饰性的元素，应该隐藏**

```swift
Image("divider-decoration")
    .accessibilityHidden(true)                  // ← 别让旁白念它
```

**③ 用多个元素拼出来的"一个"语义单位**

```swift
HStack {
    Image(systemName: "person.circle")
    VStack(alignment: .leading) {
        Text("张三")
        Text("工程师").font(.caption)
    }
}
.accessibilityElement(children: .combine)       // ← 合成一个元素来读
.accessibilityLabel("张三，工程师")
```

⚠️ 不加 `.combine` 的话，旁白会把它拆成三个元素分别读——用户要滑三次才能跳过一个人。这在列表里是灾难。

**④ 值得补充说明的地方**

```swift
Button("删除") { delete() }
    .accessibilityHint("会同时删除该笔记的所有附件")     // 读了标签之后再说一句
```

### 四个修饰符的分工

| 修饰符 | 作用 | 什么时候用 |
| --- | --- | --- |
| `.accessibilityLabel(_:)` | **是什么**（替代默认读数） | 图标、自定义控件 |
| `.accessibilityValue(_:)` | **当前值** | 自定义滑块、进度 |
| `.accessibilityHint(_:)` | **做什么**（操作后会怎样） | 有副作用/不可逆的操作 |
| `.accessibilityHidden(_:)` | 完全隐藏 | 纯装饰元素 |

💭 记忆法：**Label 是名词，Value 是形容词，Hint 是动词。**

⚠️ 别滥用 `Hint`——它会让每次聚焦都多读一句。只在"后果不明显"时才加。

### 加一个"旁白开关"来检查

```text
@Environment(\.accessibilityVoiceOverEnabled) private var voiceOver
```

一般不直接用它来改布局，但可以用它做**调试提示**：开发期打开旁白，模拟器里用"辅助功能检查器"（Xcode → Open Developer Tool → Accessibility Inspector）能直接看到每个元素被读成什么。**这是检查无障碍最快的办法**，不用真的开旁白。

## 11.3 不要只靠颜色传达信息

有一类用户看不见红色/绿色（色觉障碍），还有一类用户开了"增强对比度"。**颜色不能是唯一的信息载体。**

```text
// 🚧 只靠颜色："哪个是失败的？"
HStack {
    Circle().fill(.green).frame(width: 8, height: 8)
    Text("构建通过")
}
HStack {
    Circle().fill(.red).frame(width: 8, height: 8)
    Text("构建失败")
}
```

**修法：加上形状或符号，让信息不依赖颜色。**

```swift
// ✅ 图标本身就带语义
Label("构建通过", systemImage: "checkmark.circle.fill").foregroundStyle(.green)
Label("构建失败", systemImage: "xmark.octagon.fill").foregroundStyle(.red)
```

系统还给了环境值让你检查用户的偏好：

```text
@Environment(\.accessibilityDifferentiateWithoutColor) private var noColor
@Environment(\.colorSchemeContrast) private var contrast

if noColor {
    // 用户要求"不要只靠颜色区分"→ 加符号
}
```

⚠️ **深色模式也算适配的一部分**，而且比颜色无障碍更高频。三个要点：

| 要点 | 说明 |
| --- | --- |
| 用语义颜色 | `.primary` / `.secondary` / `.background` / `.separator` 会自动适配；`.white` / `.black` 不会 |
| 别用固定的灰色 | `Color(white: 0.9)` 在深色下几乎看不见 |
| 图片/图标要检查 | 单色图标用 `.foregroundStyle(.primary)` 而不是写死颜色 |

```swift
// ✅ 语义颜色
Text("副标题").foregroundStyle(.secondary)
// 🚧 写死颜色
Text("副标题").foregroundStyle(Color(white: 0.6))
```

💭 预览同样能测：`#Preview { MyView().preferredColorScheme(.dark) }`。

## 11.4 动效偏好：至少两个

第 5 章提过一次，这里补全——**有两类用户需要你降低动效**：

```swift
struct AnimatedThing: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var expanded = false

    var animation: Animation? {
        reduceMotion ? nil : .spring(duration: 0.4)
    }

    var body: some View {
        VStack {
            Button(expanded ? "收起" : "展开") {
                withAnimation(animation) { expanded.toggle() }
            }
            if expanded { Text("展开了") }
        }
    }
}
```

| 环境值 | 含义 | 你该做什么 |
| --- | --- | --- |
| `\.accessibilityReduceMotion` | 减少动态效果（前庭功能障碍用户需要） | 把动画换成 `nil` 或极短的淡入淡出 |
| `\.accessibilityReduceTransparency` | 减少透明度（材质变不透明） | 别用 `.ultraThinMaterial` 之类的半透明做关键信息背景 |

⚠️ `withAnimation` 接受 `Animation?`，传 `nil` 就是"不做动画"——这让上面那个 `animation` 计算属性可以直接用，不需要 `if/else` 分支。

🔥 **这不是可选项**：强动画会让部分用户真的头晕、恶心。做"尊重减弱动效"的成本只有两行代码。

## 11.5 尺寸类与多平台适配

同一个 App 在 iPhone 竖屏、iPhone 横屏、iPad 分屏、Mac 窗口上的宽度差异很大。SwiftUI 用**尺寸类**（Size Class）来描述这个差异：

```swift
struct Sidebar: View { var body: some View { Text("侧栏") } }
struct Detail: View { var body: some View { Text("详情") } }

struct AdaptiveLayout: View {
    @Environment(\.horizontalSizeClass) private var horizontal

    var body: some View {
        if horizontal == .regular {
            HStack {                              // iPad / Mac：左右分栏
                Sidebar()
                Detail()
            }
        } else {
            VStack {                              // iPhone 竖屏：上下堆叠
                Detail()
            }
        }
    }
}
```

| 尺寸类 | 典型场景 |
| --- | --- |
| `.compact` | iPhone 竖屏的宽度、iPhone 横屏的高度 |
| `.regular` | iPad 宽度、Mac 窗口、iPhone 横屏的宽度 |
| `nil` | 环境里没有这个信息（要按 `.regular` 处理） |

⚠️ **`nil` 是真的会出现的**（某些 macOS 场景、以及 widget 之类）。所以判据要写"是不是 `.regular`"或者"是不是 `.compact`"，**不要**写 `if horizontal == .regular ... else ...` 然后又假设 else 一定是 compact——`nil` 会掉进 else，行为可能不对。

💭 更省事的做法：**先试 `ViewThatFits`，不行再上尺寸类。** 因为"实际能放下多少"比"设备属于哪一类"更接近你的真实需求：

```swift
struct Adaptive: View {
    var body: some View {
        // ✅ 不关心设备，只关心"放得下吗"
        ViewThatFits {
            HStack { Text("侧栏"); Text("详情") }
            VStack { Text("详情") }
        }
    }
}
```

### 多平台的平台差异要显式处理

第 8 章实测过一个具体例子：`EditButton` 和 `.topBarLeading` 是 **iOS 专有**，在 macOS 上直接编译失败。

```swift
struct EditableList: View {
    @State private var isEditing = false

    var body: some View {
        List { Text("内容") }
            // ✅ 用条件编译处理平台差异
            #if os(iOS)
            .toolbar { ToolbarItem(placement: .topBarTrailing) { EditButton() } }
            #else
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button(isEditing ? "完成" : "编辑") { isEditing.toggle() }
                }
            }
            #endif
    }
}
```

⚠️ 更推荐的做法是**优先选跨平台的 API**，只在没有替代品时才上 `#if os(...)`：

| 需求 | 跨平台写法 | 平台专有 |
| --- | --- | --- |
| 工具栏按钮 | `.primaryAction` / `.secondaryAction` | `.topBarLeading`（iOS） |
| 进入编辑模式 | 自己用 `@State` 控制 | `EditButton`（iOS） |
| 底部操作表 | `.confirmationDialog` | `ActionSheet`（已弃用） |

🔥 判据：**能用跨平台 API 就用，用不了才条件编译。** 每多一处 `#if os`，你就多一份要分开维护的代码。

## 11.6 完整可运行文件

这个例子把动态字体、语义标签、颜色无障碍、动效偏好全放进去了：

```swift
import SwiftUI

struct AccessibleRow: View {
    let title: String
    let subtitle: String
    let isFavorite: Bool

    // 间距跟随字号缩放
    @ScaledMetric(relativeTo: .body) private var spacing: CGFloat = 8
    @ScaledMetric(relativeTo: .body) private var dot: CGFloat = 10

    var body: some View {
        HStack(spacing: spacing) {
            // 装饰性小圆点：不靠它传达信息，所以对旁白隐藏
            Circle()
                .fill(isFavorite ? .yellow : .clear)
                .frame(width: dot, height: dot)
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: 2) {
                Text(title).font(.body)
                Text(subtitle).font(.caption).foregroundStyle(.secondary)
            }

            Spacer()

            // ✅ 不只用颜色：图标本身带语义
            if isFavorite {
                Label("已收藏", systemImage: "star.fill")
                    .labelStyle(.iconOnly)
                    .foregroundStyle(.yellow)
                    .accessibilityLabel("已收藏")
            }
        }
        // 把这一行合成一个旁白元素，避免要滑三次
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(title)，\(subtitle)\(isFavorite ? "，已收藏" : "")")
    }
}

struct AccessibilityLab: View {
    @Environment(\.dynamicTypeSize) private var typeSize
    @Environment(\.colorScheme) private var scheme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.accessibilityDifferentiateWithoutColor) private var noColor
    @Environment(\.horizontalSizeClass) private var horizontal

    @State private var expanded = false

    var body: some View {
        NavigationStack {
            List {
                Section("当前环境") {
                    LabeledContent("动态字体", value: "\(typeSize)")
                    LabeledContent("配色", value: scheme == .dark ? "深色" : "浅色")
                    LabeledContent("减弱动效", value: reduceMotion ? "开" : "关")
                    LabeledContent("不用颜色区分", value: noColor ? "开" : "关")
                    LabeledContent("横向尺寸类", value: horizontal.map { "\($0)" } ?? "nil")
                }

                Section("自适应行（试试把字号调到最大）") {
                    AccessibleRow(title: "第一项", subtitle: "副标题在这里", isFavorite: true)
                    AccessibleRow(title: "第二项", subtitle: "这一条没有收藏", isFavorite: false)
                }

                Section("尊重减弱动效") {
                    Button(expanded ? "收起" : "展开") {
                        // reduceMotion 为真时 animation 是 nil —— 直接切换，不做动画
                        withAnimation(reduceMotion ? nil : .spring(duration: 0.4)) {
                            expanded.toggle()
                        }
                    }
                    if expanded {
                        Text("这一段是展开后才出现的。")
                            .transition(.opacity.combined(with: .move(edge: .top)))
                    }
                }
            }
            .navigationTitle("可访问性实验")
        }
    }
}

#Preview("标准") {
    AccessibilityLab()
}

#Preview("超大字号 + 深色") {
    AccessibilityLab()
        .environment(\.dynamicTypeSize, .accessibility3)
        .preferredColorScheme(.dark)
}
```

> 📦 这一段是 `View` + `#Preview`，**没有 `@main`**：新建 `Chapter11.swift` 放进 Xcode 的 App 项目，再把 App 文件里的 `WindowGroup { ContentView() }` 改成 `WindowGroup { AccessibilityLab() }`；只想看效果就直接看 `#Preview`——预览不需要入口。

💭 建议这样验证：

1. **切到"超大字号 + 深色"预览**——看 `AccessibleRow` 会不会挤爆（`@ScaledMetric` 应该让间距跟着变大）；
2. **打开"辅助功能检查器"**（Xcode → Open Developer Tool），逐元素看旁白会读成什么；
3. **用预览的 `.environment(\.accessibilityReduceMotion, true)`** 再看一次展开动效是否变成瞬间切换。

## 11.7 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| `.font(.system(size: 17))` | 固定字号，用户调大字号时不变 | 用 `.font(.body)` 等语义样式 |
| `.font(.custom("X", size: 17))` | 同样固定 | 加 `relativeTo: .body` |
| 字号变大但间距写死 | 布局挤爆、文字截断 | 用 `@ScaledMetric` 让间距跟着缩放 |
| 只在标准字号下预览 | 大字号下的问题到最后才发现 | 每个组件配一个"超大字号"预览 |
| 装饰性图片不标隐藏 | 旁白会念出无意义的图 | `.accessibilityHidden(true)` |
| 多个元素拼一个语义单位却不合并 | 旁白要滑三次才能跳过一行 | `.accessibilityElement(children: .combine)` |
| 用颜色当唯一信息（红/绿点） | 色觉障碍用户读不出区别 | 加图标或形状，读 `\.accessibilityDifferentiateWithoutColor` |
| 写死 `.white` / `.black` / `Color(white:)` | 深色模式下看不见或刺眼 | 用 `.primary` / `.secondary` / `.background` |
| 忽略 `accessibilityReduceMotion` | 强动画会让部分用户头晕 | 为真时把 animation 传 `nil` |
| `if horizontal == .regular` 然后假设 else 是 compact | `nil` 会掉进 else，行为可能不对 | 判 "是不是 `.regular`"，或改用 `ViewThatFits` |
| 直接抄 iOS 专有 API | macOS 上**编译失败**（实测 `'EditButton' is unavailable in macOS`） | 优先跨平台 API，必要时 `#if os(...)` |

## 11.8 下一章

现在你的界面"功能完整、性能可控、对所有人可用"了。剩下最后一件事：**好看。**

接下来两章进入绘制与特效：

- **第 12 章 绘制**：`Shape`、`Path`、`Canvas`、渐变——自己画出系统没提供的图形；
- **第 13 章 特效**：材质、模糊、混合模式、`visualEffect`——把界面从"整齐"推到"有质感"。
