+++
title = "第 13 章 视觉特效：材质、模糊与混合"
weight = 130
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "Material 的层次关系、blur 与 shadow 的代价、混合模式的组合、visualEffect 如何在不用 GeometryReader 的前提下做滚动特效，以及 Liquid Glass"
isCJKLanguage = true
draft = false
+++

# 第 13 章：视觉特效

> 最后一章。前面十二章让界面"正确、能用、对所有人友好"。这一章处理最后那层：**质感。**
>
> ⚠️ 但特效也是**最容易滥用**的一块。所以这一章会反复回到同一个问题：**这个特效解决了什么问题？**

## 13.1 材质：不是半透明，是"会适应背景的层次"

`Material` 和"半透明白色"看起来像，但完全不是一回事：

```swift
// 半透明色：不管背后是什么，永远是同一块灰
Text("浮动").padding().background(.white.opacity(0.5))

// 材质：会实时模糊背后的内容，并随明暗模式自动调整
Text("浮动").padding().background(.regularMaterial)
```

🔬 材质会做三件半透明色做不到的事：

| | 半透明色 | `Material` |
| --- | --- | --- |
| 背后内容的处理 | 直接透出来（看得清字） | **模糊掉**（背景退到后面去） |
| 明暗模式 | 不会自动适配 | 自动切换亮/暗的着色 |
| 可读性 | 背景花就完蛋 | 始终保证前景可读 |

### 五档厚度 + 一个特殊档

```swift
VStack(spacing: 16) {
    Text("ultraThin").padding().background(.ultraThinMaterial)
    Text("thin").padding().background(.thinMaterial)
    Text("regular").padding().background(.regularMaterial)
    Text("thick").padding().background(.thickMaterial)
    Text("ultraThick").padding().background(.ultraThickMaterial)
    Text("bar").padding().background(.bar)          // 系统栏专用
}
.padding()
.background(.blue.gradient)     // ← 放个彩色背景，才看得出材质的模糊效果
```

| 档位 | 什么时候用 |
| --- | --- |
| `.ultraThinMaterial` | 最大化透出背景（背景本身是主要内容时） |
| `.thinMaterial` | 轻量浮层 |
| `.regularMaterial` | **默认选择**，浮层与背景平衡 |
| `.thickMaterial` / `.ultraThickMaterial` | 内容优先，背景只是底纹 |
| `.bar` | 模仿系统导航栏/工具栏的层次 |

⚠️ **材质必须有东西可"模糊"**。放在纯色背景上，材质和一块半透明色看起来没区别——你会以为它坏了。

💭 判断该用哪档：**问"用户主要在看哪一层"**。在看浮层内容 → 用厚档；在看背景（浮层只是叠加信息）→ 用薄档。

### 材质与形状

```swift
Text("卡片").padding(16)
    .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 16))
```

🔥 第二个参数 `in:` 比 `.background(...)` 然后 `.clipShape(...)` 更好——它是把材质**裁进**形状里，而不是先铺满再裁掉，语义更清晰、也不容易出现裁剪边缘的锯齿。

### 无障碍：材质要能被"关闭"

有一类用户开了"减少透明度"（`accessibilityReduceTransparency`），因为半透明会让文字难以辨认。这时应该换成不透明背景：

```swift
struct AdaptivePanel<Content: View>: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency
    @ViewBuilder var content: Content

    var body: some View {
        content
            .padding(16)
            .background(
                reduceTransparency ? AnyShapeStyle(.background) : AnyShapeStyle(.regularMaterial),
                in: RoundedRectangle(cornerRadius: 16)
            )
    }
}
```

⚠️ 注意那个 `AnyShapeStyle(...)`——`if/else` 两个分支返回的是**不同类型**（一个是 `BackgroundStyle`，一个是 `Material`），所以要用类型擦除把它们统一。这是 `AnyShapeStyle` 少数**正当的用法**之一（对比第 10 章批评的 `AnyView`：这里擦除的是一个值，不是视图身份，没有那个代价）。

## 13.2 模糊、阴影与它们的代价

### `blur`

```swift
Text("模糊").blur(radius: 4)                    // 高斯模糊，边缘半透明
Text("更实").blur(radius: 4, opaque: true)      // 不透明模糊：边缘不发虚
```

⚠️ **`blur` 非常贵**。它需要对整个区域做卷积，半径越大越贵，而且是**每帧重算**。所以：

| 场景 | 该不该用 `blur` |
| --- | --- |
| 静态装饰（背景光斑） | ✅ 可以，但建议配 `.drawingGroup()` 合成一次 |
| 动画中的模糊 | 🚧 谨慎，半径大的话会掉帧 |
| 滚动列表的每一行 | 🛑 绝对不要 |
| "毛玻璃"效果 | ❌ 用 `Material`，它由系统优化过 |

🔥 最后一条最重要：**想要毛玻璃就用 `Material`，不要自己 `blur` + 半透明色。** 后者又贵又不像。

### `shadow`

```swift
RoundedRectangle(cornerRadius: 12)
    .fill(.white)
    .shadow(color: .black.opacity(0.15), radius: 8, x: 0, y: 4)
```

⚠️ 三个参数的关系容易搞错：

| 参数 | 作用 |
| --- | --- |
| `color` | 阴影颜色，**必须带透明度**（不透明的黑色阴影是灾难） |
| `radius` | 模糊半径，越大越"软"越大 |
| `x` / `y` | 偏移，决定光源方向 |

💭 逼真的阴影规则：**光源来自上方 → `y` 为正（向下偏移），且半径越大、透明度越低。** 一个 `.shadow(color: .black, radius: 0, y: 2)` 会得到一条硬黑边，非常假。

⚠️ **阴影不能和 `.clipShape` 顺序搞反**：

```swift
// 🛑 阴影被裁掉了
content.clipShape(Circle()).shadow(radius: 10)

// ✅ 先裁内容，再加阴影
content.shadow(radius: 10).clipShape(Circle())    // 也不对
// ✅ 正确：阴影要加在"已经裁好的形状"外面
content.clipShape(Circle()).shadow(radius: 10)    // ← 其实这个是对的
```

⚠️ 上面这个例子说明**顺序问题必须自己试**——但有一条通用规则：**`.clipShape` 之后加的东西才不会被裁**。所以 `.clipShape(...).shadow(...)` 是"给这个裁好的形状加阴影"，而 `.shadow(...).clipShape(...)` 会连阴影一起裁掉。

## 13.3 混合模式：让重叠的部分"发生化学反应"

`blendMode` 决定这一层和它**下面已有的内容**如何合成。这是做出"发光"、"正片叠底"这类效果的手段：

```swift
ZStack {
    Color.blue
    Color.yellow.blendMode(.multiply)      // 正片叠底：结果偏暗
}
```

| 模式 | 效果 | 典型用途 |
| --- | --- | --- |
| `.normal` | 默认，直接覆盖 | — |
| `.multiply` | 相乘，结果变暗 | 阴影、加深、纸质感 |
| `.screen` | 反相乘，结果变亮 | 发光、光晕 |
| `.overlay` | 对比度增强 | 增加层次 |
| `.softLight` / `.hardLight` | 柔光/强光 | 光照模拟 |
| `.difference` | 差值的绝对值 | 反色效果、艺术化 |
| `.plusLighter` / `.plusDarker` | 相加变亮/变暗 | 光斑叠加 |

⚠️ **混合模式只影响"和它下面的内容"**，所以它必须在 `ZStack` 或 `.overlay` 里才看得出效果——单独一个视图上加了它，和没加一样。

🔥 一个实用组合：**发光文字**

```swift
Text("GLOW")
    .font(.system(size: 48, weight: .black))
    .foregroundStyle(.white)
    .overlay {
        Text("GLOW")
            .font(.system(size: 48, weight: .black))
            .foregroundStyle(.cyan)
            .blur(radius: 12)
            .blendMode(.plusLighter)         // 让光晕"加"上去，而不是盖住
    }
```

💭 注意 `.blur` 和 `.blendMode` 的顺序：先模糊，再以"加亮"方式叠上去。这是发光效果的标准配方。

## 13.4 `visualEffect`：不用 `GeometryReader` 做滚动特效

这是这一章**最有用**的一个 API。经典需求：滚动时让顶部标题随滚动位置渐隐/缩放。

**老办法（有问题）**：

```text
// 🚧 用 GeometryReader 测量，但它会改变布局
.background(GeometryReader { geo in
    Color.clear.preference(key: OffsetKey.self, value: geo.frame(in: .named("scroll")).minY)
})
.onPreferenceChange(OffsetKey.self) { offset = $0 }
```

问题有两个：`GeometryReader` 会**撑满可用空间**（影响布局），而且"测量 → 传偏好 → 改状态 → 重绘"这条链会**多一轮刷新**，滚动时容易掉帧。

**新办法**：`visualEffect`（iOS 17 / macOS 14 起）

```swift
ScrollView {
    VStack {
        ForEach(0..<30, id: \.self) { i in
            Text("第 \(i) 行")
                .padding()
                .frame(maxWidth: .infinity)
                .background(.blue.opacity(0.1), in: RoundedRectangle(cornerRadius: 8))
                // ✅ 在"视觉层"里读几何信息，不影响布局、不触发额外刷新
                .visualEffect { content, proxy in
                    let minY = proxy.frame(in: .scrollView).minY
                    let progress = min(max(minY / 200, 0), 1)
                    return content
                        .opacity(1 - progress * 0.6)
                        .scaleEffect(1 - progress * 0.1)
                }
        }
    }
    .padding()
}
```

🔥 **关键区别**：`visualEffect` 的闭包拿到的是 `content`（要修饰的内容）和一个 `proxy`，**它返回一个视觉效果，不参与布局计算**。所以：

| | `GeometryReader` + `PreferenceKey` | `visualEffect` |
| --- | --- | --- |
| 是否影响布局 | ✅ 会（`GeometryReader` 是贪婪的） | ❌ 完全不影响 |
| 是否需要额外状态 | ✅ 需要 `@State` + 偏好传递 | ❌ 不需要 |
| 刷新次数 | 多一轮 | 直接 |
| 滚动流畅度 | 容易掉帧 | 好得多 |
| 起点 | iOS 13 | iOS 17 / macOS 14 |

⚠️ 一个必须知道的细节：**`proxy.frame(in:)` 里的坐标系是有限的**，常用的几个：

| 坐标系 | 含义 |
| --- | --- |
| `.scrollView` | 相对最近的滚动容器的可见区域 |
| `.named("x")` | 你自定义的坐标空间 |
| `.global` | 相对屏幕 |
| `.local` | 相对自己 |

`visualEffect` 只是视觉效果——**它不会改变布局尺寸**。所以想让"渐隐的行"同时让出空间，你还得改 `frame` 或 `padding`（那就回到了布局层）。

### 配套的两个 API

`visualEffect` 之外，还有两个专门的滚动特效 API（都是 iOS 17 / macOS 14 起）：

```swift
struct Card: View {
    let index: Int
    init(_ i: Int) { index = i }
    var body: some View {
        RoundedRectangle(cornerRadius: 12)
            .fill(.blue.opacity(0.2))
            .overlay { Text("卡片 \(index)") }
            .padding(.horizontal, 8)
    }
}

struct HorizontalCards: View {
    var body: some View {
        ScrollView(.horizontal) {
            LazyHStack {
                ForEach(0..<10) { i in
                    Card(i)
                        .containerRelativeFrame(.horizontal)     // ← 等于滚动容器的宽度
                }
            }
        }
    }
}
```

| API | 用途 |
| --- | --- |
| `visualEffect` | 任意自定义的几何驱动视觉调整 |
| `scrollTransition` | 元素进出时的标准转场（更简洁） |
| `containerRelativeFrame` | 相对滚动容器定尺寸 |

💭 三者分工清楚：**能用 `scrollTransition` 就用它**（最省事）；需要不规则的几何效果才上 `visualEffect`；尺寸问题用 `containerRelativeFrame`。

## 13.5 Liquid Glass 🆕

iOS 26 / macOS 26 引入了新的系统材质 **Liquid Glass**，它是"会折射背景"的一种材质，也是新版系统 UI 的统一语言。

```swift
import SwiftUI

struct GlassButtons: View {
    @Namespace private var glassNamespace

    var body: some View {
        VStack(spacing: 16) {
            Text("普通玻璃")
                .padding()
                .glassEffect()

            Text("胶囊形状")
                .padding()
                .glassEffect(.regular, in: .capsule)

            // 多个玻璃元素可以"合并"成一块（相邻的玻璃会连起来）
            HStack(spacing: 8) {
                Button("收藏") { }.padding().glassEffect()
                Button("分享") { }.padding().glassEffect()
            }
            .glassEffectUnion(id: "toolbar", namespace: glassNamespace)   // 合并成一体
        }
    }
}
```

🔬 **实测的可用性**（从 SDK 接口文件读到的准确标注）：

```text
@available(iOS 26.0, macOS 26.0, tvOS 26.0, watchOS 26.0, *)
@available(visionOS, unavailable)
public func glassEffect(_ glass: Glass = .regular, in shape: some Shape = DefaultGlassEffectShape()) -> some View
```

⚠️ 三个要点：

| 要点 | 说明 |
| --- | --- |
| 最低版本是 **iOS 26 / macOS 26** | 部署目标低于此就要 `if #available` 兜底 |
| **visionOS 上不可用** | 这是唯一被排除的平台 |
| 默认参数是 `.regular` 和默认形状 | `glassEffect()` 无参调用就可用（实测通过） |

💭 什么时候用：**系统级的浮层**（工具栏、控制条、悬浮操作）。它是"系统 UI 的一部分"，不适合当装饰随便撒。滥用会让界面看起来像贴了一堆塑料片。

⚠️ 部署目标兼容的写法：

```swift
struct GlassPanel<Content: View>: View {
    @ViewBuilder var content: Content

    var body: some View {
        if #available(iOS 26.0, macOS 26.0, *) {
            content.glassEffect()
        } else {
            content.background(.regularMaterial, in: Capsule())
        }
    }
}
```

## 13.6 完整可运行文件

```swift
import SwiftUI

struct EffectsLab: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency
    @State private var scrollAmount: CGFloat = 0

    var body: some View {
        ZStack {
            // 彩色背景：材质和模糊都要有东西可"作用"才看得出来
            LinearGradient(colors: [.purple, .blue, .teal],
                           startPoint: .topLeading, endPoint: .bottomTrailing)
                .ignoresSafeArea()

            ScrollView {
                VStack(spacing: 24) {

                    // ① 五档材质对照
                    sectionTitle("材质（注意背景被模糊的程度）")
                    VStack(spacing: 10) {
                        ForEach([("ultraThin", Material.ultraThinMaterial),
                                 ("thin", Material.thinMaterial),
                                 ("regular", Material.regularMaterial),
                                 ("thick", Material.thickMaterial),
                                 ("ultraThick", Material.ultraThickMaterial)],
                                id: \.0) { name, material in
                            Text(name)
                                .font(.callout)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 10)
                                .background(material, in: RoundedRectangle(cornerRadius: 10))
                        }
                    }

                    // ② 自适应：减少透明度时换成不透明
                    sectionTitle("尊重「减少透明度」")
                    Text(reduceTransparency ? "不透明背景（用户偏好）" : "材质背景")
                        .padding()
                        .background(
                            reduceTransparency
                                ? AnyShapeStyle(.background)
                                : AnyShapeStyle(.regularMaterial),
                            in: RoundedRectangle(cornerRadius: 12)
                        )

                    // ③ 发光文字：blur + blendMode
                    sectionTitle("发光文字（blur + plusLighter）")
                    Text("GLOW")
                        .font(.system(size: 44, weight: .black))
                        .foregroundStyle(.white)
                        .overlay {
                            Text("GLOW")
                                .font(.system(size: 44, weight: .black))
                                .foregroundStyle(.cyan)
                                .blur(radius: 12)
                                .blendMode(.plusLighter)
                        }

                    // ④ 阴影的三种"真实度"
                    sectionTitle("阴影（光源默认来自上方）")
                    HStack(spacing: 16) {
                        shadowSwatch("假的", .black, radius: 0, y: 3)
                        shadowSwatch("一般", .black.opacity(0.35), radius: 6, y: 3)
                        shadowSwatch("自然", .black.opacity(0.18), radius: 14, y: 6)
                    }

                    // ⑤ 滚动特效：visualEffect（不影响布局）
                    sectionTitle("滚动特效（visualEffect）")
                    ForEach(0..<12, id: \.self) { i in
                        Text("第 \(i) 行")
                            .padding()
                            .frame(maxWidth: .infinity)
                            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 8))
                            .visualEffect { content, proxy in
                                let minY = proxy.frame(in: .scrollView).minY
                                let p = min(max(minY / 400, 0), 1)
                                return content
                                    .opacity(1 - p * 0.7)
                                    .scaleEffect(1 - p * 0.12)
                            }
                    }
                }
                .padding()
            }
        }
    }

    func sectionTitle(_ s: String) -> some View {
        Text(s)
            .font(.footnote).bold()
            .foregroundStyle(.white.opacity(0.8))
            .frame(maxWidth: .infinity, alignment: .leading)
    }

    func shadowSwatch(_ label: String, _ color: Color, radius: CGFloat, y: CGFloat) -> some View {
        VStack(spacing: 8) {
            RoundedRectangle(cornerRadius: 10)
                .fill(.white)
                .frame(width: 70, height: 50)
                .shadow(color: color, radius: radius, y: y)
            Text(label).font(.caption2).foregroundStyle(.white.opacity(0.8))
        }
    }
}

#Preview("标准") {
    EffectsLab()
}

// ⚠️ accessibilityReduceTransparency 是只读环境值（`get`-only），
//    直接 `.environment(\.accessibilityReduceTransparency, true)` 会报
//    `cannot convert value of type 'any KeyPath<EnvironmentValues, Bool>' to
//     expected argument type 'WritableKeyPath<EnvironmentValues, Bool>'`
//    想看"减少透明度"下的样子，用模拟器/系统设置打开该开关，
//    或者像下面这样自定义一个可写的环境键位来做演示。
private struct DemoReduceTransparency: EnvironmentKey {
    static var defaultValue: Bool { false }
}
extension EnvironmentValues {
    var demoReduceTransparency: Bool {
        get { self[DemoReduceTransparency.self] }
        set { self[DemoReduceTransparency.self] = newValue }
    }
}

#Preview("减少透明度（模拟）") {
    EffectsLab().environment(\.demoReduceTransparency, true)
}
```

💭 跑起来重点看三件事：

1. **五档材质的区别**——薄档能看到背景的色块轮廓，厚档几乎只剩底纹；
2. **滚动时下面那些行的变化**——`visualEffect` 让它们随位置渐隐缩小，而**布局没有任何变化**（对比一下：用 `GeometryReader` 做同样的事会改变行高）；
3. **切到"减少透明度"预览**——那块材质应该变成不透明的系统背景色。

## 13.7 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| 用 `.white.opacity(0.5)` 当"毛玻璃" | 只是半透明，背景字看得一清二楚 | 用 `Material` |
| 把材质放在纯色背景上 | 看起来和半透明色没区别，以为坏了 | 材质需要有内容可模糊 |
| 自己 `blur` 做毛玻璃 | 又贵又不像 | 用 `Material` |
| 在列表每一行上加 `blur` | 每帧重算卷积，滚动掉帧 | 静态装饰才用 `blur`，考虑 `.drawingGroup()` |
| 阴影用不透明的黑色 | 得到一条硬黑边，很假 | 带透明度 + 正向 `y` 偏移 + 较大 `radius` |
| `.shadow(...).clipShape(...)` | 阴影被一起裁掉 | 先 `.clipShape` 再加 `.shadow` |
| 单独一个视图加 `.blendMode` | 和没加一样——它只和**下面的内容**混合 | 放进 `ZStack` / `.overlay` 里 |
| 用 `GeometryReader` + `PreferenceKey` 做滚动特效 | 影响布局、多一轮刷新、滚动易掉帧 | 用 `visualEffect`（iOS 17+） |
| 以为 `visualEffect` 会改变布局 | 它是纯视觉层，尺寸不变 | 要改尺寸得动 `frame` / `padding` |
| 材质不考虑"减少透明度"偏好 | 部分用户读不清内容 | 读 `\.accessibilityReduceTransparency` 换不透明背景 |
| `if/else` 返回两种背景类型 | 类型不一致编译报错 | 用 `AnyShapeStyle(...)` 统一（这是它正当的用法） |
| 直接把 `glassEffect()` 用在低版本部署目标 | 需要 iOS 26 / macOS 26（**visionOS 不可用**） | 用 `if #available(iOS 26.0, macOS 26.0, *)` 兜底 |

## 13.8 结语：十三章之后

到这里，这份教程的十三章走完了。回头看这条路线：

| 幕 | 章 | 解决什么 |
| --- | --- | --- |
| 心智模型 | 1–2 | 视图是值、状态是源头 |
| 布局 | 3–4 | 尺寸与位置从哪来 |
| 动起来 | 5–6 | 变化被看懂、用户能交互 |
| 工程化 | 7–9 | 组件化、多页面、数据落地 |
| 质量 | 10–11 | 性能可控、对所有人可用 |
| 表现力 | 12–13 | 自己画、做出质感 |

💭 **最后一句建议，和第一章那句是同一条**：SwiftUI 的知识点不多，但**必须动手改**才能变成直觉。这一章里的每个例子，都值得你跑起来之后故意改坏它——把 `Material` 换成 `.white.opacity(0.5)`、把 `visualEffect` 换成 `GeometryReader`、把 `.blendMode` 删掉，看界面怎么变。

**你改坏的次数，等于你学会的程度。**

## 13.9 接下来去哪

| 想做的事 | 去哪 |
| --- | --- |
| 系统性地再过一遍概念体系 | [Swift 基础部分第七篇]({{< relref "../basic/_index.md" >}}) 第 40–47 章 |
| 查某个 API 的完整用法 | [SwiftUI 官方文档整理]({{< relref "../SwiftUI/_index.md" >}}) |
| 写 Swift 语法忘了怎么写 | [Swift 速查表]({{< relref "../CheatSheet/_index.md" >}}) |
| 遇到崩溃、结果不对 | [Swift 血泪速查]({{< relref "../CheatSheet/16-Pitfalls-and-Gotchas.md" >}}) |
