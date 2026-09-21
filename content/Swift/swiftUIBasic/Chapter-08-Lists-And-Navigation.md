+++
title = "第 8 章 列表与导航：多页面应用怎么搭"
weight = 80
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "List 的三种写法、身份在滚动视图里的真实后果、增删改查、NavigationStack 的路径与 programmatic 导航、弹窗家族的分工"
isCJKLanguage = true
draft = false
+++

# 第 8 章：列表与导航

> 前面七章讲的是"怎么把一个界面做对"。这一章开始讲 App：**一堆页面怎么组织，数据怎么变成一行行看得见的东西。**
>
> ⚠️ 这一章也是第 6 章"身份"最实战的考场——列表是唯一一个"身份选错会出真 bug"的地方。

## 8.1 `List` 的三种写法

`List` 是 SwiftUI 里最重要的容器。它同时提供三件别的东西给不了的东西：**平台原生外观**（iOS 上是那种分组圆角列表）、**懒加载**（只渲染可见行）、以及**一整套行为**（滑动删除、拖动排序、选择、编辑模式）。

它有三种写法：

```text
// ① 手动列出每一行：适合静态内容或少量行
List {
    Text("第一行")
    Text("第二行")
}

// ② ForEach 遍历一个集合：最常用
List {
    ForEach(items) { item in
        Text(item.name)
    }
}

// ③ 直接传集合：语法糖，等价于 ②
List(items) { item in
    Text(item.name)
}
```

三种写法都能用，但**有一件事只有 ② 能做**：给行加 `.onDelete` / `.onMove`。因为这两个修饰符要加在 `ForEach` 上，而不是 `List` 上：

```swift
struct Task: Identifiable {
    let id = UUID()
    var name: String
}

struct Demo: View {
    @State private var items: [Task] = [
        Task(name: "第一行"),
        Task(name: "第二行"),
    ]

    var body: some View {
        List {
            ForEach(items) { item in
                Text(item.name)
            }
            .onDelete { offsets in items.remove(atOffsets: offsets) }   // ← 加在 ForEach 上
            .onMove { from, to in items.move(fromOffsets: from, toOffset: to) }
        }
    }
}
```

⚠️ 顺序细节：`.onDelete` 必须写在 `ForEach` 后面、`List` 的闭包**里面**。写到 `List` 外面不生效（也不报错，只是没反应）。

## 8.2 身份：这一章真正的主题

`ForEach` 需要一个东西来判断"这是不是同一行"——就是**身份**。有三种给法：

| 写法 | 什么时候用 | 风险 |
| --- | --- | --- |
| `ForEach(items)` | `items` 元素遵守 `Identifiable` | ✅ 推荐 |
| `ForEach(items, id: \.someKeyPath)` | 没有 `Identifiable`，但有天然唯一键 | ✅ 好用 |
| `ForEach(items.indices, id: \.self)` 或 `id: \.offset` | 没有唯一键 | 🛑 **危险** |

### 为什么"用下标当 id"是危险的

这是 SwiftUI 里最经典的一个坑，值得用第 6 章的模型推一遍：

```swift
struct Item: Identifiable {
    let id = UUID()
    var name: String
}

// 🛑 用下标当身份（虽然能编译、能显示，但身份不稳定）
ForEach(Array(items.enumerated()), id: \.offset) { index, item in
    Row(item: item)
}
```

现在 `items` 是 `[A, B, C]`，你删掉了 `B`。新的列表是 `[A, C]`。对 SwiftUI 来说发生了什么？

| 位置 | 删除前 | 删除后 | SwiftUI 的判断 |
| --- | --- | --- | --- |
| id = 0 | A | A | 同一个视图，内容没变 |
| id = 1 | B | **C** | **同一个视图，内容从 B 变成了 C** |
| id = 2 | C | （消失） | 视图消失 |

问题出在第 2 行：**SwiftUI 认为"id=1 那一行还在，只是内容换了"**，于是它会**复用那一行的状态**。如果 `Row` 里有 `@State private var isExpanded = false`、或者有输入框，那个状态就"继承"给了 C。

🔥 **症状**：删除一行后，另一行莫名其妙变成"展开"状态，或者输入框里残留着上一行的文字。

⚠️ 而这个 bug 在**没有状态的行**上完全看不出来——所以它经常在项目后期才冒出来，那时已经很难定位了。

### 正确的身份

```swift
struct Item: Identifiable {
    let id: UUID          // 注意是 let，不是 var
    var name: String
    var sku: String
}

struct A: View {
    let items: [Item]
    var body: some View {
        // ✅ 元素遵守 Identifiable，id 是稳定标识（通常来自模型 / 数据库）
        List {
            ForEach(items) { item in Text(item.name) }
        }
    }
}

struct B: View {
    let items: [Item]
    var body: some View {
        // ✅ 用业务上的天然唯一键
        List {
            ForEach(items, id: \.sku) { item in Text(item.name) }
        }
    }
}
```

⚠️ **`id` 必须是"跟着数据走"的**，要满足两条：

| 要求 | 为什么 |
| --- | --- |
| **稳定**：同一份数据每次生成的 id 相同 | 否则每次刷新都重建所有行状态 |
| **唯一**：不同数据不共享 id | 否则 SwiftUI 会当成同一行 |

🛑 两个常见的违例：

```swift
struct Item: Identifiable {
    var id = UUID()       // 🛑 id 是 var：改了它等于换了身份，状态会被重置
    var name: String
}

ForEach(items, id: \.name) { ... }   // 🛑 名字可能重复，也可能被改
```

💭 **一条经验法则**：**id 应该来自"这条数据在世界上是什么"，而不是"它现在排第几"。** 数据库主键、UUID、SKU 都是好的 id；下标、`name`、`Date()` 都是坏的。

⚠️ 诚实标注：上面这套"复用了错误的行状态"的后果是从第 6 章的身份模型**推导**出来的（状态属于身份，不随位置走），社区也有大量一致报告。但**本教程的无界面测量环境无法直接演示它**——复现需要真实的数据变更事件。所以这里给出的是机制层面的推理，不是实测截图。

## 8.3 增删改查：一套完整的行为

```swift
import SwiftUI

struct Task: Identifiable {
    let id = UUID()
    var title: String
    var done = false
}

struct TaskListView: View {
    @State private var tasks: [Task] = [
        Task(title: "读完第 8 章"),
        Task(title: "写一个列表页面"),
    ]

    var body: some View {
        NavigationStack {
            List {
                ForEach($tasks) { $task in            // ← 注意 $：拿到每一项的绑定
                    Toggle(task.title, isOn: $task.done)
                }
                .onDelete { tasks.remove(atOffsets: $0) }
                .onMove { tasks.move(fromOffsets: $0, toOffset: $1) }
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("添加", systemImage: "plus") {
                        tasks.append(Task(title: "新任务"))
                    }
                }
            }
        }
    }
}
```

三个要点：

| 写法 | 作用 |
| --- | --- |
| `ForEach($tasks) { $task in ... }` | 传**绑定集合**，于是每一项都能拿到 `Binding`，可以直接改属性 |
| `.onDelete { indexSet in ... }` | 滑动删除，参数是 `IndexSet`，用 `remove(atOffsets:)` 消费 |
| `.onMove { from, to in ... }` | 拖动排序，用 `move(fromOffsets:toOffset:)` |

🔥 `ForEach($tasks)` 这个写法很值得记：它让"列表里每一行都能就地编辑数据"变得非常干净。它要求集合元素是 `Identifiable`。

⚠️ 关于 `.onDelete` 的可用性：**它在滑动删除的平台上有效**（iOS、watchOS）。在 macOS 上列表行没有"滑动"，用户会用菜单或 Delete 键——所以**同一份代码在 macOS 上行为不同**，这不是 bug。要做跨平台，可以额外加一个工具栏按钮：

```text
ToolbarItem(placement: .primaryAction) {
    Button("删除已完成") {
        tasks.removeAll { $0.done }
    }
}
```

### 选择（Selection）

```swift
struct Picker: View {
    @State private var single: String?
    @State private var multiple = Set<String>()
    let items = ["一", "二", "三"]

    var body: some View {
        // 单选：Binding<SelectionValue?>
        List(items, id: \.self, selection: $single) { Text($0) }

        // 多选：Binding<Set<SelectionValue>>
        List(items, id: \.self, selection: $multiple) { Text($0) }
    }
}
```

⚠️ 选择值必须和 `id` 的类型一致。多选用 `Set`，单选用 `Optional`——**用错类型编译器会直接报错，这一点很友好**。

## 8.4 层级列表

`List` 原生支持折叠树，只要你的数据有"子节点"这个概念：

```swift
struct Folder: Identifiable {
    let id = UUID()
    var name: String
    var children: [Folder]? = nil        // nil 表示叶子节点
}

struct OutlineView: View {
    @State private var folders: [Folder] = [
        Folder(name: "文档", children: [
            Folder(name: "工作"),
            Folder(name: "个人"),
        ]),
        Folder(name: "下载"),
    ]

    var body: some View {
        List(folders, children: \.children) { folder in
            Label(folder.name, systemImage: folder.children == nil ? "doc" : "folder")
        }
    }
}
```

🔥 `children:` 参数是 KeyPath，指向"子节点数组"。`nil` 表示这一行不可展开。**系统会自动加上展开/折叠的箭头和动画**，不用自己写。

## 8.5 导航：`NavigationStack`

SwiftUI 的导航在 iOS 16 之后换成了 `NavigationStack`（老的 `NavigationView` 已不推荐）。它的模型非常清晰：**一个路径（path）→ 一叠页面**。

### 最简形态：由用户点击推入

```swift
struct Item: Identifiable, Hashable {
    let id = UUID()
    var name: String
}

struct ListNav: View {
    let items = [Item(name: "一"), Item(name: "二")]

    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.name, value: item)   // ← 推入一个"值"
            }
            .navigationDestination(for: Item.self) { item in
                Text(item.name).navigationTitle("详情")   // ← 值到页面的映射
            }
        }
    }
}
```

⚠️ 这个模型和老的 `NavigationLink(destination:)` 有本质区别：

| | `NavigationLink(value:)` + `navigationDestination` | `NavigationLink(destination:)`（老写法） |
| --- | --- | --- |
| 链接的是什么 | 一个**数据值** | 一个**已经构造好的视图** |
| 页面何时构造 | 真正被推入时 | 列表渲染时就构造了（浪费） |
| 能否编程导航 | ✅ 改 path 就行 | ❌ 很难 |
| 类型安全 | ✅ `navigationDestination(for:)` 按类型分发 | 弱 |

🔥 新写法的关键优势是**"导航状态可以是一个普通的值数组"**——这让"恢复到上次浏览位置"、"从通知直接跳到详情页"这类需求变得自然。

### 编程导航：操作 path

```swift
struct Item: Identifiable, Hashable {
    let id = UUID()
    var name: String
}

struct ShopView: View {
    let items = [Item(name: "苹果"), Item(name: "香蕉")]
    @State private var path: [Item] = []          // 用一个数组当路径

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(item.name, value: item)
            }
            .navigationDestination(for: Item.self) { item in
                Text(item.name).navigationTitle("详情")
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("直接看第一个") {
                        if let first = items.first {
                            path.append(first)          // ← 编程推入
                        }
                    }
                }
            }
        }
    }
}
```

| 操作 | 怎么写 |
| --- | --- |
| 推入一页 | `path.append(value)` |
| 返回一页 | `path.removeLast()` |
| 回到根 | `path.removeAll()` |
| 跳转多级 | `path = [a, b, c]` |
| 页面里拿"当前在哪" | 也读这个 `path` |

⚠️ `path` 的类型要和 `navigationDestination(for:)` 的类型对上：

- 路径里只有一种类型 → 用 `[Item]`，简单直接；
- 多种类型混着推 → 用 `NavigationPath`（类型擦除的容器），代价是读不出具体内容。

```text
@State private var path = NavigationPath()
// path.append(item); path.append("某个字符串"); 都能装
```

### 导航的三条纪律

| 纪律 | 说明 |
| --- | --- |
| `navigationDestination` 要写在**被推入区域的内部**，不是 `NavigationStack` 外面 | 写错位置会不生效，而且不报错 |
| 同一个 `NavigationStack` 里，`for:` 的类型要唯一 | 同类型注册两次，行为未定义 |
| 不要在 `navigationDestination` 里读"会随导航变化的 `@State`" | 页面构造时机可能和你想的不同 |

## 8.6 弹窗家族：五种"浮在上面"的东西

SwiftUI 有一整套"临时出现在当前页面上方"的呈现方式。它们的分工经常被搞混：

| 工具 | 外观 | 用途 |
| --- | --- | --- |
| `.sheet` | 从底部推上来的整页 | 需要用户完成一件事（表单、设置） |
| `.fullScreenCover` | 全屏覆盖（iOS） | 需要完全占据注意力的流程（引导、相机） |
| `.popover` | 气泡指向来源（iPad / macOS 常用） | 轻量的上下文操作 |
| `.alert` | 居中的系统弹窗 | **必须让用户知道**的通知 / 二选一确认 |
| `.confirmationDialog` | 底部动作表（iOS） | 多个破坏性选项（删除/取消） |

### `sheet`：用 `item:` 还是 `isPresented:`

```swift
struct Item: Identifiable {
    let id = UUID()
    var name: String
}

struct SheetDemo: View {
    // 方式一：只控制"显示 / 隐藏"
    @State private var showSettings = false

    // 方式二：要展示"某一条具体数据"
    @State private var editing: Item?

    let item = Item(name: "样本")

    var body: some View {
        VStack {
            Button("设置") { showSettings = true }
                .sheet(isPresented: $showSettings) {
                    Text("设置页").padding()
                }

            Button("编辑") { editing = item }
                .sheet(item: $editing) { item in
                    Text("编辑：\(item.name)").padding()
                }
        }
    }
}
```

🔥 **优先用 `item:`**。原因是 `isPresented:` + 一个单独的 `@State var currentItem` 会引入一个真实 bug：

```swift
// 🛑 两个状态可能不同步
@State private var showEdit = false
@State private var editingItem: Item?

Button("编辑") { editingItem = item; showEdit = true }
    .sheet(isPresented: $showEdit) {
        EditView(item: editingItem!)      // ← 万一 editingItem 是 nil 就崩
    }
```

`.sheet(item:)` 把"显不显示"和"显示哪一条"合并成一个状态，**从结构上消除了不同步的可能**。而且它要求类型遵守 `Identifiable`，正好逼你给数据一个稳定身份（回到第 6 章）。

💭 一句话判据：**只要弹窗里需要"某一条数据"，就用 `item:`。**

### `alert` 与 `confirmationDialog`

```swift
struct DeleteDemo: View {
    @State private var confirmDelete = false
    @State private var deleted = false

    var body: some View {
        VStack {
            if deleted {
                Text("已删除")
            } else {
                Button("删除", role: .destructive) { confirmDelete = true }
                    .alert("确定删除？", isPresented: $confirmDelete) {
                        Button("删除", role: .destructive) { deleted = true }
                        Button("取消", role: .cancel) { }
                    } message: {
                        Text("这个操作无法撤销。")
                    }
            }
        }
    }
}
```

两者的选择：

| 场景 | 用哪个 |
| --- | --- |
| 需要用户读一句话并确认 | `.alert` |
| 需要用户读一句话并**选择**（比如"保存 / 不保存 / 取消"） | `.alert` |
| 多个操作选项，其中一个是破坏性的 | `.confirmationDialog` |
| 只是通知，不需要选择 | 别用弹窗——用页面内的提示条 |

⚠️ `role:` 不是装饰：`.destructive` 会让按钮变红（iOS）、`.cancel` 会绑定 Esc 键（macOS）并影响弹窗的默认行为。**该标的角色一定要标**，这是无障碍和平台一致性的基础。

## 8.7 完整可运行文件

下面这个例子是跨平台的（工具条用 `.primaryAction`，不依赖 iOS 专有的 `EditButton`）：

```swift
import SwiftUI

struct Task: Identifiable, Hashable {
    let id = UUID()
    var title: String
    var done = false
    var note: String = ""
}

struct TaskListView: View {
    @State private var tasks: [Task] = [
        Task(title: "读懂身份的规则"),
        Task(title: "给列表加上删除", done: true),
        Task(title: "试一次编程导航"),
    ]
    @State private var path: [Task] = []
    @State private var confirmingClear = false

    var body: some View {
        NavigationStack(path: $path) {
            List {
                Section("待办") {
                    ForEach($tasks) { $task in
                        NavigationLink(value: task) {
                            Label {
                                Text(task.title)
                                    .strikethrough(task.done)
                            } icon: {
                                Image(systemName: task.done ? "checkmark.circle.fill" : "circle")
                                    .foregroundStyle(task.done ? .green : .secondary)
                            }
                        }
                    }
                    .onDelete { tasks.remove(atOffsets: $0) }
                    .onMove { tasks.move(fromOffsets: $0, toOffset: $1) }
                }

                Section {
                    Button("清空全部", role: .destructive) {
                        confirmingClear = true
                    }
                }
            }
            .navigationTitle("任务")
            .navigationDestination(for: Task.self) { task in
                TaskDetail(task: task)
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("添加", systemImage: "plus") {
                        tasks.append(Task(title: "新任务"))
                    }
                }
                ToolbarItem(placement: .secondaryAction) {
                    Button("直接看第一个") {
                        if let first = tasks.first { path.append(first) }
                    }
                }
            }
            .alert("清空全部任务？", isPresented: $confirmingClear) {
                Button("清空", role: .destructive) { tasks.removeAll() }
                Button("取消", role: .cancel) { }
            } message: {
                Text("共 \(tasks.count) 条，无法撤销。")
            }
        }
    }
}

struct TaskDetail: View {
    let task: Task
    @State private var note = ""

    var body: some View {
        Form {
            Section("标题") { Text(task.title) }
            Section("备注") {
                TextField("写点什么", text: $note, axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle("详情")
    }
}

#Preview {
    TaskListView()
}
```

> 📦 这一段是 `View` + `#Preview`，**没有 `@main`**：新建 `Chapter08.swift` 放进 Xcode 的 App 项目，再把 App 文件里的 `WindowGroup { ContentView() }` 改成 `WindowGroup { TaskListView() }`；只想看效果就直接看 `#Preview`——预览不需要入口。

💭 跑起来重点试三件事：

1. **滑动删除一行**（或 macOS 上用工具栏按钮），然后确认剩下的行状态没问题；
2. **点"直接看第一个"**——这是纯编程导航，和点击列表行走的是同一条路径；
3. **拖动排序**，看身份是否稳定（行内容跟着数据走，不会串）。

## 8.8 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| `ForEach(items, id: \.offset)` | 删除后"id 还在、内容换了"，行状态被错误复用（如展开态串行、输入框残留） | 用 `Identifiable` 或天然唯一键 |
| `var id = UUID()`（`var`） | 改 id = 换身份，状态被重置 | `id` 用 `let` |
| `ForEach(items, id: \.name)` | 名字可重复 / 可修改 | 用主键 |
| `.onDelete` 写在 `List` 上 | 不生效，也不报错 | 写在 `ForEach` 上 |
| `.sheet(isPresented:)` + 单独的 `currentItem` | 两个状态可能不同步，`currentItem!` 会崩 | 用 `.sheet(item:)` |
| 破坏性按钮不标 `role: .destructive` | 没有红色提示、没有平台一致的默认行为 | 标上 `role` |
| `navigationDestination` 写在 `NavigationStack` 外面 | 不生效，不报错 | 写在里面的内容上 |
| 用 `NavigationView` | 老 API，不支持 `path` 编程导航 | 用 `NavigationStack` |
| 混用多种导航值类型却用 `[Item]` 当 path | 类型对不上，编译报错 | 用 `NavigationPath` |
| 依赖 `EditButton` / `.topBarLeading` | **iOS 专有**，macOS 上直接编译失败（实测 `'EditButton' is unavailable in macOS`） | 用 `.primaryAction` 等跨平台 placement，或加 `#if os(iOS)` |

## 8.9 下一章

列表和导航解决的是"数据怎么变成页面"。还剩最后一块：**数据本身从哪来、存在哪**。

下一章讲数据落地：怎么建模"加载中 / 成功 / 失败"三态、网络请求怎么写才不把 `body` 搞乱、以及持久化有哪些选择（从 `@AppStorage` 到 `SwiftData`）。
