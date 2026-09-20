+++
title = "第 12 章 绘制：Shape、Path 与 Canvas"
weight = 120
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "自己画系统没提供的图形：Shape 与 Path 的坐标系、stroke 与 strokeBorder 的实测差异、四种渐变、Canvas 的命令式绘制与性能边界"
isCJKLanguage = true
draft = false
+++

# 第 12 章：绘制

> 前十一章的界面都是"系统给的零件拼出来的"。这一章开始自己画——因为有些视觉效果，系统没提供现成的。

## 12.1 `Shape`：用代码描述一个图形

`Shape` 协议比 `View` 还简单，它只要求一件事：**给定一个矩形，给出一个 `Path`。**

```swift
import SwiftUI

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var p = Path()
        p.move(to: CGPoint(x: rect.midX, y: rect.minY))      // 顶点
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))   // 右下
        p.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))   // 左下
        p.closeSubpath()                                     // 回到起点，闭合
        return p
    }
}
```

用起来和内置形状完全一样：

```swift
Triangle()
    .fill(.blue)                       // 填充
    .frame(width: 120, height: 100)    // 尺寸由 frame 决定

Triangle()
    .stroke(.red, lineWidth: 3)        // 描边
    .frame(width: 120, height: 100)
```

🔥 **关键理解**：`Shape` 拿到的是**别人分配给它的矩形**（`rect`），它要在这个矩形**内部**描述自己。所以同一个 `Triangle` 可以是 10×10 也可以是 1000×1000——**永远不要在 `path(in:)` 里写死坐标**。

```swift
// 🛑 写死坐标：换个尺寸就错了
func path(in rect: CGRect) -> Path {
    var p = Path()
    p.move(to: CGPoint(x: 50, y: 0))       // 50 是从哪来的？
    ...
}

// ✅ 全部基于 rect 计算
func path(in rect: CGRect) -> Path {
    var p = Path()
    p.move(to: CGPoint(x: rect.midX, y: rect.minY))
    ...
}
```

### `Path` 的常用指令

| 指令 | 作用 |
| --- | --- |
| `move(to:)` | 抬笔移到某点（开始新子路径） |
| `addLine(to:)` | 画直线到某点 |
| `addQuadCurve(to:control:)` | 二次贝塞尔曲线（一个控制点） |
| `addCurve(to:control1:control2:)` | 三次贝塞尔曲线（两个控制点） |
| `addArc(center:radius:startAngle:endAngle:clockwise:)` | 圆弧 |
| `addEllipse(in:)` / `addRoundedRect(in:cornerRadius:)` | 内置形状 |
| `closeSubpath()` | 闭合当前子路径 |
| `addPath(_:)` | 把另一条路径并进来 |

### 一个实用例子：带缺口的卡片

```swift
struct TicketShape: Shape {
    var notchRadius: CGFloat = 12
    var notchPosition: CGFloat = 0.7         // 缺口在右边 70% 高度处

    func path(in rect: CGRect) -> Path {
        var p = Path()
        let r: CGFloat = 16                  // 圆角半径
        let notchY = rect.minY + rect.height * notchPosition

        // 从左上角开始，顺时针画（iOS 坐标系 y 向下）
        p.move(to: CGPoint(x: rect.minX + r, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX - r, y: rect.minY))
        p.addQuadCurve(to: CGPoint(x: rect.maxX, y: rect.minY + r),
                       control: CGPoint(x: rect.maxX, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX, y: notchY - notchRadius))
        // 用圆弧挖出缺口（顺时针 inward）
        p.addArc(center: CGPoint(x: rect.maxX, y: notchY),
                 radius: notchRadius,
                 startAngle: .degrees(-90), endAngle: .degrees(90),
                 clockwise: true)
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY - r))
        p.addQuadCurve(to: CGPoint(x: rect.maxX - r, y: rect.maxY),
                       control: CGPoint(x: rect.maxX, y: rect.maxY))
        p.addLine(to: CGPoint(x: rect.minX + r, y: rect.maxY))
        p.addQuadCurve(to: CGPoint(x: rect.minX, y: rect.maxY - r),
                       control: CGPoint(x: rect.minX, y: rect.maxY))
        p.closeSubpath()
        return p
    }
}
```

💭 画形状时**建议先在纸上标出各个点的坐标关系**，再翻译成 `rect.minX + r` 这样的表达式。直接写代码很容易把方向搞反——iOS 坐标系 **y 轴向下**，所以 `minY` 是顶部。

## 12.2 `stroke` 与 `strokeBorder`：一个实测出来的差别

这是绘制里最容易踩的一个坑，而且**光看代码看不出来**——必须量。

🔬 **实测**：画布 100×100，形状是一个 60×60 的 `Rectangle` 居中，线宽 10。

| 写法 | 可见横向范围 | 宽度 |
| --- | --- | --- |
| `Rectangle().stroke(.red, lineWidth: 10)` | 15.0–85.0 pt | **70** |
| `Rectangle().strokeBorder(.red, lineWidth: 10)` | 20.0–80.0 pt | **60** |
| `Rectangle().fill(.red)`（对照） | 20.0–80.0 pt | 60 |

真相是：

| | 线画在哪 | 结果 |
| --- | --- | --- |
| `.stroke(...)` | **以路径为中心**，向两侧各扩一半 | 向外溢出 5pt、向内占 5pt → 总宽 60 + 5×2 = **70** |
| `.strokeBorder(...)` | **完全画在形状内部** | 总宽还是 **60** |

🔥 **结论**：想让描边**不超出你给的 frame**，用 `.strokeBorder`。

⚠️ 而 `.strokeBorder` 只对遵守 `InsettableShape` 的形状可用。`Rectangle`、`RoundedRectangle`、`Circle`、`Capsule`、`Ellipse` 都支持；**你自己写的 `Shape` 默认不支持**——要加 `InsettableShape` 一致性（多一个 `inset(by:)` 方法）。自定义形状用不了 `.strokeBorder` 时，可以用 `.stroke` 配合内缩的 frame 来模拟：

```swift
Triangle()
    .stroke(.red, lineWidth: 10)
    .padding(5)                 // ← 手动留出线宽的一半
    .frame(width: 120, height: 100)
```

💭 这个坑为什么值得单列一节：**它不报错、不警告，只是让图形比预期大了一圈**。当你发现"两个形状怎么都对不齐"时，先检查是不是一个用了 `stroke`、一个用了 `fill`。

## 12.3 渐变：四种类型

SwiftUI 提供四种渐变，写法统一成 `.xxxGradient(colors:...)`：

```swift
VStack(spacing: 12) {
    // ① 线性：从一点到另一点
    Rectangle().fill(.linearGradient(
        colors: [.blue, .purple],
        startPoint: .topLeading, endPoint: .bottomTrailing))

    // ② 径向：从中心向外（半径用绝对点数）
    Rectangle().fill(.radialGradient(
        colors: [.yellow, .orange],
        center: .center, startRadius: 0, endRadius: 80))

    // ③ 角向：绕中心一圈
    Rectangle().fill(.angularGradient(
        colors: [.red, .yellow, .green, .blue, .red],
        center: .center, startAngle: .zero, endAngle: .degrees(360)))

    // ④ 椭圆径向：半径用"比例"表示
    Rectangle().fill(.ellipticalGradient(
        colors: [.mint, .teal],
        center: .center, startRadiusFraction: 0, endRadiusFraction: 0.8))
}
.frame(height: 400)
```

⚠️ 两个容易记错的参数：

| 类型 | 半径怎么给 |
| --- | --- |
| `.radialGradient` | `startRadius` / `endRadius`：**绝对点数** |
| `.ellipticalGradient` | `startRadiusFraction` / `endRadiusFraction`：**相对于视图尺寸的比例（0~1）** |

### 用 `Gradient.Stop` 控制颜色停在哪

只给颜色数组时，系统把颜色**均匀分布**。想控制位置就用 `stops:`：

```swift
Rectangle()
    .fill(Gradient(stops: [
        .init(color: .blue, location: 0.0),
        .init(color: .blue, location: 0.4),      // 前 40% 保持纯蓝
        .init(color: .purple, location: 0.6),    // 40%~60% 之间过渡
        .init(color: .purple, location: 1.0),    // 后 40% 保持纯紫
    ]))
```

🔬 这个技巧在实际项目里非常常用——**两个 location 相同的相邻 stop 会形成一条"硬边界"**，而 location 相同的一对（如 0.4 和 0.4）则完全没有过渡。用它做进度条、双色背景、以及"模糊分隔线"都很好用。

### 渐变也能描边和当文字颜色

```swift
Text("渐变文字")
    .font(.largeTitle).bold()
    .foregroundStyle(.linearGradient(colors: [.pink, .orange],
                                     startPoint: .leading, endPoint: .trailing))

Circle()
    .strokeBorder(.angularGradient(colors: [.red, .yellow, .red], center: .center,
                                   startAngle: .zero, endAngle: .degrees(360)),
                  lineWidth: 8)
    .frame(width: 100, height: 100)
```

💭 `foregroundStyle` 接受任何 `ShapeStyle`——纯色、渐变、材质（第 13 章）都行。这比老的 `.foregroundColor` 强得多，新代码一律用 `foregroundStyle`。

## 12.4 `Canvas`：当 `Shape` 不够用时

`Shape` 只能描述**一条路径**。如果要画**很多个**独立的图形（粒子、图表、签名板），就该用 `Canvas`。

```swift
struct Sparkline: View {
    let values: [Double]

    var body: some View {
        Canvas { context, size in
            guard values.count > 1 else { return }
            let maxV = values.max() ?? 1
            let stepX = size.width / CGFloat(values.count - 1)

            var path = Path()
            for (i, v) in values.enumerated() {
                let point = CGPoint(
                    x: CGFloat(i) * stepX,
                    y: size.height * (1 - CGFloat(v / maxV))
                )
                if i == 0 { path.move(to: point) } else { path.addLine(to: point) }
            }

            context.stroke(path, with: .color(.blue),
                           style: StrokeStyle(lineWidth: 2, lineJoin: .round))
        }
        .frame(height: 60)
    }
}
```

`Canvas` 的闭包签名是 `(GraphicsContext, CGSize) -> Void`。第二个参数是**你能用的尺寸**，第一个参数 `context` 是你的"画笔"。

### `GraphicsContext` 的常用操作

| 操作 | 说明 |
| --- | --- |
| `context.stroke(path, with:style:)` | 描边 |
| `context.fill(path, with:)` | 填充 |
| `context.draw(_:at:anchor:)` | 画一个 `Text` 或 `Image` |
| `context.opacity = 0.5` | 设置后续绘制的不透明度 |
| `context.blendMode = .multiply` | 设置混合模式 |
| `context.clip(to:)` | 裁剪到某个路径 |
| `context.translateBy` / `rotate(by:)` / `scaleBy` | 变换坐标系（**有累积效果**） |
| `context.drawLayer { }` | 开一个"图层"，在里面改设置不影响外面 |

⚠️ **变换是有状态的**，这点和 `Shape` 很不一样：

```swift
Canvas { context, size in
    context.rotate(by: .degrees(45))       // 🚧 这会影响后面所有绘制
    context.fill(Path(CGRect(x: 0, y: 0, width: 50, height: 50)), with: .color(.red))

    // 想画不旋转的东西，得手动转回来，或者用 drawLayer 隔离
    context.drawLayer { layer in
        layer.rotate(by: .degrees(-45))
        layer.draw(Text("正的文字"), at: CGPoint(x: 50, y: 50))
    }
}
```

🔬 `drawLayer` 是隔离状态的标准做法：**在它内部的设置改动不会泄漏到外面。**

### `Canvas` 的性能边界

| 特点 | 说明 |
| --- | --- |
| ✅ 一个 `Canvas` = 一个视图 | 画 1000 个图形也不会创建 1000 个视图，开销远低于 `ForEach` |
| ✅ 支持 `symbols` 缓存 | 重复绘制的元素可以用 `Canvas(opaque:colorMode:rendersAsynchronously:)` + `resolve` 复用 |
| 🚧 **内容不可交互** | `Canvas` 里画的东西不是视图，**收不到点击**——要交互必须自己算坐标 |
| 🚧 **不参与无障碍** | 旁白读不到 `Canvas` 里的内容，需要额外用 `.accessibilityLabel` 描述整体 |
| ⚠️ 重绘成本 | `Canvas` 的内容变化会整块重画，不适合"只改一小部分"的场景 |

🔥 **判据**：

| 你要画什么 | 用什么 |
| --- | --- |
| 一条形状，能 `fill` / `stroke` | `Shape`（还能动画，见下） |
| 几十个以内、需要交互 | 用视图（`ForEach` + `Shape`） |
| 成百上千个、纯展示 | `Canvas` |
| 图表、粒子、签名板 | `Canvas` |

### `Shape` 能动画，`Canvas` 不能（天然）

这是两者最重要的区别。你的 `Shape` 只要遵守 `Animatable`（第 5 章那个机制），就能补间：

```swift
struct ProgressRing: Shape, Animatable {
    var progress: Double                     // 0...1

    var animatableData: Double {             // ← 框架反复喂中间值给这里
        get { progress }
        set { progress = newValue }
    }

    func path(in rect: CGRect) -> Path {
        var p = Path()
        p.addArc(center: CGPoint(x: rect.midX, y: rect.midY),
                 radius: min(rect.width, rect.height) / 2 - 4,
                 startAngle: .degrees(-90),
                 endAngle: .degrees(-90 + 360 * progress),
                 clockwise: false)
        return p
    }
}
```

用法是把它接到一个状态上：

```swift
struct RingDemo: View {
    @State private var value = 0.35

    var body: some View {
        ProgressRing(progress: value)
            .stroke(.blue, style: StrokeStyle(lineWidth: 8, lineCap: .round))
            .frame(width: 120, height: 120)
            .animation(.easeInOut(duration: 0.6), value: value)   // ← progress 一变就平滑补间
            .onTapGesture { value = value > 0.5 ? 0.2 : 0.95 }
    }
}
```

⚠️ **`Canvas` 没有 `animatableData`**，所以它不会自己补间。想在 `Canvas` 里做动画，得用 `TimelineView(.animation)` 自己按时间算每一帧：

```swift
TimelineView(.animation) { timeline in
    let t = timeline.date.timeIntervalSinceReferenceDate
    Canvas { context, size in
        let angle = t.truncatingRemainder(dividingBy: 2) / 2 * 360
        context.translateBy(x: size.width / 2, y: size.height / 2)
        context.rotate(by: .degrees(angle))
        context.fill(Path(CGRect(x: -4, y: -40, width: 8, height: 8)), with: .color(.orange))
    }
}
```

💭 `TimelineView(.animation)` 会在每个显示帧回调你——**这是最消耗资源的做法**，只在 `Shape` 表达不了的时候用（比如粒子系统、复杂的逐帧计算）。普通的"值变化 → 平滑过渡"一律用 `Shape` + `Animatable`。

## 12.5 完整可运行文件

```swift
import SwiftUI

// ① 自定义 Shape：圆角 + 右侧缺口（票券）
struct TicketShape: Shape {
    var notchRadius: CGFloat = 10

    func path(in rect: CGRect) -> Path {
        var p = Path()
        let r: CGFloat = 14
        let notchY = rect.midY

        p.move(to: CGPoint(x: rect.minX + r, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX - r, y: rect.minY))
        p.addQuadCurve(to: CGPoint(x: rect.maxX, y: rect.minY + r),
                       control: CGPoint(x: rect.maxX, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX, y: notchY - notchRadius))
        p.addArc(center: CGPoint(x: rect.maxX, y: notchY),
                 radius: notchRadius,
                 startAngle: .degrees(-90), endAngle: .degrees(90),
                 clockwise: true)
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY - r))
        p.addQuadCurve(to: CGPoint(x: rect.maxX - r, y: rect.maxY),
                       control: CGPoint(x: rect.maxX, y: rect.maxY))
        p.addLine(to: CGPoint(x: rect.minX + r, y: rect.maxY))
        p.addQuadCurve(to: CGPoint(x: rect.minX, y: rect.maxY - r),
                       control: CGPoint(x: rect.minX, y: rect.maxY))
        p.closeSubpath()
        return p
    }
}

// ② 可动画的 Shape：环形进度
struct ProgressRing: Shape, Animatable {
    var progress: Double

    var animatableData: Double {
        get { progress }
        set { progress = newValue }
    }

    func path(in rect: CGRect) -> Path {
        var p = Path()
        let radius = min(rect.width, rect.height) / 2 - 6
        p.addArc(center: CGPoint(x: rect.midX, y: rect.midY),
                 radius: radius,
                 startAngle: .degrees(-90),
                 endAngle: .degrees(-90 + 360 * max(0, min(1, progress))),
                 clockwise: false)
        return p
    }
}

// ③ Canvas：画一组柱子（纯展示、数量可变）
struct BarChart: View {
    let values: [Double]

    var body: some View {
        Canvas { context, size in
            guard !values.isEmpty else { return }
            let maxV = values.max() ?? 1
            let gap: CGFloat = 4
            let barW = (size.width - gap * CGFloat(values.count - 1)) / CGFloat(values.count)

            for (i, v) in values.enumerated() {
                let h = size.height * CGFloat(v / maxV)
                let rect = CGRect(x: CGFloat(i) * (barW + gap),
                                  y: size.height - h,
                                  width: barW, height: h)
                // ⚠️ GraphicsContext 的渐变签名和 ShapeStyle 的**同名方法不一样**：
                //    它要 Gradient + CGPoint，而不是 colors + UnitPoint
                context.fill(
                    Path(roundedRect: rect, cornerRadius: 3),
                    with: .linearGradient(
                        Gradient(colors: [.blue, .cyan]),
                        startPoint: CGPoint(x: 0, y: size.height),
                        endPoint: CGPoint(x: 0, y: 0)
                    )
                )
            }
        }
        .frame(height: 120)
    }
}

struct DrawingLab: View {
    @State private var progress = 0.35

    var body: some View {
        ScrollView {
            VStack(spacing: 28) {

                // 票券形状 + 缺口
                TicketShape(notchRadius: 12)
                    .fill(.orange.gradient)
                    .frame(height: 90)
                    .overlay(alignment: .leading) {
                        Text("凭 证").font(.headline).padding(.leading, 20)
                    }

                // stroke vs strokeBorder 对照（画布宽度相同）
                VStack(spacing: 8) {
                    Text("stroke（线宽 10，向外溢出 5pt）").font(.caption).foregroundStyle(.secondary)
                    Rectangle().stroke(.red, lineWidth: 10).frame(height: 60)
                    Text("strokeBorder（完全在内部）").font(.caption).foregroundStyle(.secondary)
                    Rectangle().strokeBorder(.red, lineWidth: 10).frame(height: 60)
                }

                // 可动画的环形进度
                VStack(spacing: 12) {
                    ZStack {
                        Circle()
                            .stroke(.gray.opacity(0.2), lineWidth: 10)
                        ProgressRing(progress: progress)
                            .stroke(.blue, style: StrokeStyle(lineWidth: 10, lineCap: .round))
                        Text("\(Int(progress * 100))%").font(.title2).bold().monospacedDigit()
                    }
                    .frame(width: 140, height: 140)

                    HStack {
                        Button("25%") { withAnimation(.easeInOut(duration: 0.5)) { progress = 0.25 } }
                        Button("60%") { withAnimation(.easeInOut(duration: 0.5)) { progress = 0.6 } }
                        Button("100%") { withAnimation(.easeInOut(duration: 0.5)) { progress = 1 } }
                    }
                    .buttonStyle(.bordered)
                }

                // Canvas 柱状图
                VStack(alignment: .leading, spacing: 8) {
                    Text("Canvas 柱状图").font(.headline)
                    BarChart(values: [0.3, 0.7, 0.45, 0.9, 0.6, 0.8, 0.35])
                        .accessibilityLabel("柱状图，共 7 项，最高 90%")
                }
            }
            .padding()
        }
    }
}

#Preview {
    DrawingLab()
}
```

💭 跑起来试四件事：

1. **点百分比按钮**，看环形的圆弧如何补间（这是 `Animatable` 在起作用）；
2. **对比两个红色矩形**——`stroke` 的那个明显更"胖"，因为线画到了框外；
3. **把 `ProgressRing` 的 `animatableData` 注释掉**，看动画立刻失效（这能让你记住它是干嘛的）；
4. **给 `BarChart` 传 100 个值**，感受 `Canvas` 一次画完的轻量。

## 12.6 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| 在 `path(in:)` 里写死坐标 | 换个尺寸就画错位置 | 全部用 `rect` 计算（`rect.midX` 等） |
| 用 `.stroke` 却想让它不超出边框 | 🔬 实测线会向外溢出半个线宽（60pt 形状 + 10pt 线 → 可见宽 70pt） | 用 `.strokeBorder`（需 `InsettableShape`），或手动 `.padding(线宽/2)` |
| 以为 `.strokeBorder` 自己写的形状也能用 | 它要求 `InsettableShape`，自定义 `Shape` 默认不满足 | 加 `InsettableShape` 一致性，或用内缩 + `.stroke` |
| `.radialGradient` 的半径写比例 | 它要**绝对点数** | 比例用 `.ellipticalGradient` 的 `xxxFraction` |
| `Canvas` 里改 `context.opacity` 后画别的 | 设置**一直生效**到闭包结束 | 用 `context.drawLayer { }` 隔离 |
| 想让 `Canvas` 里的图形响应点击 | `Canvas` 的内容不是视图，收不到事件 | 自己用坐标做命中判断，或者改用视图 |
| 指望 `Canvas` 自动动画 | `Canvas` 没有 `animatableData` | 用 `TimelineView(.animation)` 逐帧算，或改用 `Shape` |
| 用 `TimelineView(.animation)` 做普通过渡 | 每帧回调，最耗资源 | 值变化型动画用 `Shape` + `Animatable` |
| `Canvas` 里套用 `ShapeStyle` 的渐变写法 | 🔬 `GraphicsContext.Shading.linearGradient` 要 **`Gradient` + `CGPoint`**，而 `ShapeStyle` 上同名的方法要 **colors + `UnitPoint`**，搞混会报 `no exact matches` | 见 12.4 的柱状图例子 |
| `Canvas` 没写无障碍描述 | 旁白读到一片空白 | 加 `.accessibilityLabel(...)` |
| 用 `.foregroundColor` | 老 API，不能接收渐变/材质 | 用 `.foregroundStyle` |

## 12.7 下一章

能自己画了。最后一章把这些手段组合起来做"有质感"的界面：

**第 13 章 视觉特效**——材质（`Material`）、模糊与阴影、混合模式、`visualEffect`，以及怎么在不引入 `GeometryReader` 的前提下做出"滚动时标题渐隐"这类效果。
