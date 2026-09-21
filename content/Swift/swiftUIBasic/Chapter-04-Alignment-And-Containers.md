+++
title = "第 4 章 对齐与容器"
weight = 40
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "alignment 是「和谁对齐」而不是「往哪儿挪」：用实测坐标讲清 HStack 对齐、overlay 与 background、ZStack、Grid 与自定义 Layout"
isCJKLanguage = true
draft = false
+++

# 第 4 章：对齐与容器

> 第 3 章解决了"我该多大"。这一章解决"我和别人怎么摆在一起"。**对齐是 SwiftUI 里最容易被误解的一个词**——因为它不是你直觉里的"往哪儿挪"。

## 4.1 `alignment` 到底是什么：一条隐形的线

先看一个每个人都遇到过的场景：`HStack` 里放两个高度不同的东西。

```swift
HStack(alignment: .center, spacing: 0) {
    Color.red.frame(width: 20, height: 20)
    Color.blue.frame(width: 20, height: 40)
}
```

直觉会以为 `alignment` 是"红块往上挪还是往下挪"。**不是的。** 正确的理解是：

🔥 **`alignment` 指定的是"每个子视图内部的那条参考线"和"容器的那条参考线"对齐。**

`HStack(alignment: .center)` 的意思是：每个子视图拿出自己的**垂直中心线**，大家把这些中心线排在同一水平高度上。

### 用实测坐标验证

🔬 同一组视图，只改 `alignment`，实测每个方块的坐标（画布 120×60）：

**`alignment: .center`**

```text
红  x:40.0–60.0  y:20.0–40.0  (20.0×20.0)
蓝  x:60.0–80.0  y:10.0–50.0  (20.0×40.0)
```

红块中心 y = 30，蓝块中心 y = 30 —— **两条中心线重合**。红块自然就"上下各留 10pt"。

**`alignment: .top`**

```text
红  x:40.0–60.0  y:10.0–30.0  (20.0×20.0)
蓝  x:60.0–80.0  y:10.0–50.0  (20.0×40.0)
```

两者的**顶边**都是 y = 10。

**`alignment: .bottom`**

```text
红  x:40.0–60.0  y:30.0–50.0  (20.0×20.0)
蓝  x:60.0–80.0  y:10.0–50.0  (20.0×40.0)
```

两者的**底边**都是 y = 50。

| `alignment` | 对齐的那条线 | 红块 top | 红块 bottom |
| --- | --- | --- | --- |
| `.center` | 垂直中心 | 20 | 40 |
| `.top` | 顶边 | 10 | 30 |
| `.bottom` | 底边 | 30 | 50 |

💭 看第三列和第四列：**红块自己在动，而不是蓝块在动**——因为红块矮，它是"需要被摆放"的那一个。这就是"对齐"的真相：容器先确定自己的参考线位置，然后把每个子视图按各自的参考线贴上去。

## 4.2 `firstTextBaseline`：为什么它和 `.bottom` 不一样

`HStack` 还有一个特殊的对齐值 `.firstTextBaseline`。它的参考线不是边界，而是**文字的基线**（字母坐的那条线）：

```swift
HStack(alignment: .firstTextBaseline) {
    Text("标题").font(.largeTitle)
    Text("副标题").font(.caption)
}
```

这个组合下，两行字的**底部基线**会对齐，看起来才自然。如果用 `.bottom`，大标题和小字会底边贴底边，视觉上小字会"浮"在中间——非常难看。

⚠️ 但要注意：**`.firstTextBaseline` 只对"有文字基线"的子视图有意义**。给它塞两个 `Color` 方块，它会退化成 `.bottom`。🔬 这也是我实测到的：

| | 红块 top | 红块 bottom |
| --- | --- | --- |
| `.firstTextBaseline`（两个 Color） | 30 | 50 |
| `.bottom`（两个 Color） | 30 | 50 |

**完全一样。** 因为 `Color` 没有文字基线，`HStack` 就用了底边兜底。

🔥 实战建议：`HStack` 里混排"图标 + 文字 + 按钮"时，用 `.firstTextBaseline` 通常比 `.center` 更好看——因为人眼判断"对齐"看的是文字基线，不是几何中心。

## 4.3 `overlay` 与 `background`：尺寸谁说了算

这两个修饰符都是"在某个视图上再叠一层"，但很多人搞不清尺寸怎么算。规则其实很简单：

🔥 **`overlay` 和 `background` 都不会改变基座"报告"出来的尺寸。** 叠加层的大小由它自己决定，然后按 `alignment` 摆进基座的范围内。

🔬 实测（基座是 60×10 的红块，`fittingSize` 即视图报告的尺寸）：

| 写法 | 报告的尺寸 |
| --- | --- |
| `红60x10` | 60×10 |
| `红60x10.overlay(蓝20x10)` | **60×10** |
| `红60x10.background(蓝20x10)` | **60×10** |
| `红60x10.overlay(蓝200x30)` | **60×10** |
| `红60x10.background(蓝200x30)` | **60×10** |

⚠️ 但"报告尺寸不变"**不等于"超出的部分会消失"**。实测一个比基座大得多的 overlay：

```text
红60x10.overlay(蓝200x30)
  报告尺寸      : 60 × 10
  实际可见范围  : x 50.0–250.0（宽 200）, y 25.0–55.0（高 30）
```

**叠加层完完整整地画了出来，只是"越界"了——它突破了基座 60×10 的范围。** 这正是上一章"溢出"的另一种形态：布局尺寸和视觉范围是两件事。

🔥 **想让它不要越界，必须显式加 `.clipped()`**（和很多人的直觉相反，**默认是不裁的**）：

```text
红60x10.overlay(蓝200x30).clipped()
  实际可见范围  : x 120.0–180.0（宽 60）, y 35.0–45.0（高 10）  ← 裁到基座范围内
```

💭 所以 `.clipped()` 的作用是"把越界的内容切掉"，不是"开启裁剪"这种默认行为。给图片加角标时不加它也没事（角标本来就在范围内）；但当叠加层可能超出时（比如一个长文本浮层），不加就会盖到邻居身上。

### 两者的区别只有"谁在上面"

| | `overlay` | `background` |
| --- | --- | --- |
| 绘制顺序 | 叠加层**在上面**，会挡住基座 | 叠加层**在下面**，被基座挡住 |
| 尺寸影响 | 无 | 无 |
| 默认对齐 | `.center` | `.center` |
| 典型用途 | 给图片加角标、给按钮加 loading 指示器 | 加背景色/背景图、加边框底线 |

🔬 实测的坐标能看清这一点（画布宽 200pt，基座红 60×10，叠蓝 20×10）：

```text
.background(蓝): 只看到红 x:70.0–130.0（蓝被红完全盖住）
.overlay(蓝):    红 x:70.0–130.0 + 蓝 x:90.0–110.0（蓝居中盖在红上）
```

### `alignment` 参数

```swift
Image(systemName: "photo")
    .overlay(alignment: .bottomTrailing) {
        Text("NEW")
            .font(.caption2)
            .padding(3)
            .background(.red, in: Capsule())
            .foregroundStyle(.white)
    }
```

这是"给图片右下角加角标"的标准写法。注意 `.bottomTrailing` 是 `Alignment` 类型，它同时指定了水平和垂直方向。

## 4.4 `ZStack`：和 `overlay` 的区别

`ZStack` 也是叠放，但它是**容器**，不是修饰符。区别在于：

| | `ZStack` | `.overlay` / `.background` |
| --- | --- | --- |
| 是什么 | 容器，装多个平级的子视图 | 修饰符，在**一个**视图上叠**一个**视图 |
| 尺寸 | **由最大的子视图决定**（会撑大） | 完全不改变基座尺寸 |
| 子视图数量 | 任意多个 | 一个（想叠多个就链式调用） |
| 典型用途 | 多层背景、自定义卡片、图层式布局 | 给已有视图加装饰 |

🔬 实测 `ZStack { 红60x10; 蓝20x30 }`（画布 200×40）：

```text
红  x:70.0–130.0  y:15.0–25.0  (60.0×10.0)
蓝  x:90.0–110.0  y:5.0–35.0   (20.0×30.0)
```

`ZStack` 的尺寸是 60×30——**宽取最大（60）、高取最大（30）**。红块被垂直居中在 30pt 的高度里，所以 y 是 15–25。

⚠️ 常见错误：想给一个视图加背景色，却用 `ZStack`，结果被背景视图的尺寸撑大了。**加背景用 `.background()`，只有真的要多层布局时才用 `ZStack`。**

💭 一个实用判据：**如果你发现自己在 `ZStack` 里写 `.frame(maxWidth: .infinity, maxHeight: .infinity)` 来"对齐"，那多半用 `.overlay` / `.background` 就够。**

## 4.5 `Grid`：需要"按列对齐"时用它

`HStack` 的问题在于**独立**：每一行自己算自己的宽度，两行的列对不齐。需要列对齐时用 `Grid`（iOS 16 / macOS 13 起）：

```swift
Grid(alignment: .leading, horizontalSpacing: 12, verticalSpacing: 8) {
    GridRow {
        Text("姓名")
        Text("张三")
    }
    GridRow {
        Text("职位")
        Text("工程师")
    }
    GridRow {
        Text("城市")
        Text("上海")
    }
}
```

🔬 实测两行两列（各格宽度不同）：

```text
红  x:68.0–88.0   y:8.0–18.0    (20.0×10.0)   第1行第1列
绿  x:97.0–137.0  y:8.0–18.0    (40.0×10.0)   第1行第2列
蓝  x:63.0–93.0   y:22.0–32.0   (30.0×10.0)   第2行第1列
橙  x:107.0–127.0 y:22.0–32.0   (20.0×10.0)   第2行第2列
```

注意第 1 行的两列宽度是 20 和 40，第 2 行是 30 和 20。`Grid` 的处理是：

- **列宽取该列最宽的那个**：第 1 列 = max(20, 30) = 30，第 2 列 = max(40, 20) = 40；
- 于是第 1 列的 20pt 方块被**居中**在 30pt 的列里（红 x:68–88，而列的范围更宽）。

| 容器 | 什么时候用 |
| --- | --- |
| `HStack` | 一行、彼此独立，不需要跨行对齐 |
| `Grid` | 需要**列对齐**的表格式布局，行数不多 |
| `LazyVGrid` | 格子数量多、需要滚动，用 `GridItem` 定义列 |
| `List` | 有"行"的语义、需要滑动删除/选择等行为 |

⚠️ `LazyVGrid` 的列由 `GridItem` 描述，而 `GridItem` **只有三种**：`.fixed(宽)`、`.flexible(最小:最大:)`、`.adaptive(最小:最大:)`。它们都是"你指定宽度规则、框架算"，**没有"让这一列跟着内容变宽"这种模式**。要内容驱动的列宽就用 `Grid`。

## 4.6 自定义 `Layout`：当内置容器都不够用

如果你需要"先量所有子视图、再按自己的算法摆放"，就该实现 `Layout` 协议（iOS 16 / macOS 13 起）。它正好对应第 3 章的三步协商：

```swift
struct FlowLayout: Layout {                 // 一个会换行的横向流式布局
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let maxWidth = proposal.width ?? .infinity
        var x: CGFloat = 0, y: CGFloat = 0, lineHeight: CGFloat = 0
        for sub in subviews {
            let size = sub.sizeThatFits(.unspecified)      // 问每个子视图的理想尺寸
            if x + size.width > maxWidth, x > 0 {          // 放不下就换行
                x = 0; y += lineHeight + spacing; lineHeight = 0
            }
            x += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }
        return CGSize(width: maxWidth == .infinity ? x : maxWidth, height: y + lineHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x = bounds.minX, y = bounds.minY, lineHeight: CGFloat = 0
        for sub in subviews {
            let size = sub.sizeThatFits(.unspecified)
            if x + size.width > bounds.maxX, x > bounds.minX {
                x = bounds.minX; y += lineHeight + spacing; lineHeight = 0
            }
            sub.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            x += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }
    }
}
```

用法和内置容器一样：

```swift
FlowLayout(spacing: 8) {
    ForEach(["Swift", "SwiftUI", "布局", "自定义", "换行"], id: \.self) { tag in
        Text(tag).padding(.horizontal, 10).padding(.vertical, 5)
            .background(.blue.opacity(0.15), in: Capsule())
    }
}
```

🔥 写一次自定义 `Layout`，你对第 3 章的理解会从"知道规则"变成"掌握规则"——因为 `sizeThatFits` 就是你**替父视图做决定**，`placeSubviews` 就是你**替父视图分配位置**。

💭 但别急着到处用：`Layout` 的代价是**失去 SwiftUI 的自动优化**，而且调试麻烦。能用 `HStack`/`Grid`/`ViewThatFits` 解决就别自己写。

### `ViewThatFits`：更省事的"自适应"

如果你的需求只是"空间够就用横排、不够就换竖排"，用 `ViewThatFits`（iOS 16 / macOS 13 起）比自己写 `Layout` 简单得多：

```swift
ViewThatFits {
    HStack { Text("用户名"); TextField("请输入", text: .constant("")) }   // 首选
    VStack(alignment: .leading) { Text("用户名"); TextField("请输入", text: .constant("")) }  // 备选
}
```

它按顺序尝试每个子视图，**用第一个能放得下的**。做响应式布局时这是首选工具。

## 4.7 完整可运行文件

```swift
import SwiftUI

struct AlignmentLab: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {

                // ① 同一个 HStack，三种 alignment
                Group {
                    label("alignment: .center")
                    HStack(alignment: .center, spacing: 8) {
                        Color.red.frame(width: 30, height: 20)
                        Color.blue.frame(width: 30, height: 40)
                    }
                    label("alignment: .top")
                    HStack(alignment: .top, spacing: 8) {
                        Color.red.frame(width: 30, height: 20)
                        Color.blue.frame(width: 30, height: 40)
                    }
                    label("alignment: .bottom")
                    HStack(alignment: .bottom, spacing: 8) {
                        Color.red.frame(width: 30, height: 20)
                        Color.blue.frame(width: 30, height: 40)
                    }
                }

                // ② 基线对齐：文字混排的正确做法
                label("firstTextBaseline（文字混排）")
                HStack(alignment: .firstTextBaseline, spacing: 6) {
                    Text("标题").font(.largeTitle)
                    Text("副标题").font(.caption).foregroundStyle(.secondary)
                }

                // ③ overlay 加角标 vs ZStack 撑大
                label("overlay 角标（基座尺寸不变）")
                Color.gray.opacity(0.3)
                    .frame(width: 120, height: 80)
                    .overlay(alignment: .bottomTrailing) {
                        Text("NEW")
                            .font(.caption2).bold()
                            .padding(.horizontal, 6).padding(.vertical, 2)
                            .background(.red, in: Capsule())
                            .foregroundStyle(.white)
                            .padding(6)
                    }

                // ④ Grid 的列对齐
                label("Grid（列宽取该列最宽）")
                Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 8) {
                    GridRow { Text("姓名"); Text("张三") }
                    GridRow { Text("职位"); Text("iOS 工程师") }
                    GridRow { Text("城市"); Text("上海") }
                }

                // ⑤ ViewThatFits：够宽横排，不够竖排
                label("ViewThatFits")
                ViewThatFits {
                    HStack { Text("用户名"); TextField("请输入", text: .constant("")) }
                    VStack(alignment: .leading) { Text("用户名"); TextField("请输入", text: .constant("")) }
                }
                .frame(width: 320)
            }
            .padding()
        }
    }

    func label(_ s: String) -> some View {
        Text(s).font(.footnote).foregroundStyle(.secondary)
    }
}

#Preview {
    AlignmentLab()
}
```

> 📦 这一段是 `View` + `#Preview`，**没有 `@main`**：新建 `Chapter04.swift` 放进 Xcode 的 App 项目，再把 App 文件里的 `WindowGroup { ContentView() }` 改成 `WindowGroup { AlignmentLab() }`；只想看效果就直接看 `#Preview`——预览不需要入口。

💭 用 Xcode 预览跑起来，然后**把窗口拖窄**——你会看到 `ViewThatFits` 从横排切成竖排，而 `Grid` 的列宽始终对齐。这比读十遍规则都管用。

## 4.8 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| 以为 `alignment` 是"把视图往哪挪" | 它是"子视图的哪条线和容器的哪条线重合" | 想清楚要对齐的是哪条线 |
| 给两个 `Color` 用 `.firstTextBaseline` | 退化成 `.bottom`（没有文字基线） | 基线对齐只对文字类视图有意义 |
| 以为超出基座的 `overlay` 会被自动裁掉 | **默认不裁**。实测基座 60×10、叠加层 200×30：可见范围仍是 200×30，越界画了出来 | 需要裁就显式加 `.clipped()` |
| 想让背景色撑大视图 | `.background` 不改变基座报告的尺寸 | 需要撑大就用 `ZStack` + `.frame(maxWidth:.infinity)` |
| 给视图加背景却用了 `ZStack` | 被背景视图的尺寸撑大 | 加背景用 `.background()` |
| 在 `ZStack` 里塞 `.frame(maxWidth: .infinity)` 对齐 | 越写越绕 | 多半用 `.overlay`/`.background` 就够 |
| 用 `HStack` 做表格，列对不齐 | 每行独立算宽 | 用 `Grid` |
| 想让 `LazyVGrid` 的列按内容自适应宽度 | 它只有 `.fixed` / `.flexible` / `.adaptive` 三种，没有内容自适应 | 用 `Grid` |
| 为了自适应布局手写 `Layout` | 复杂且失去优化 | 先试 `ViewThatFits` |

## 4.9 下一章

现在视图的**位置和大小**都归你管了。但界面还是"死"的——状态一变，画面"啪"地跳过去。

下一章讲动画。而且你会发现：**动画不是给界面加装饰，而是"让状态变化被看懂"。** 它和第 3 章的布局规则直接相关——因为能动画的，正是那些参与布局计算的数值。
