+++
title = "第43章 列表、导航与弹窗：多页面应用怎么搭"
weight = 430
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "List 与身份、选择删除移动、NavigationStack 路由、sheet 与 alert、TabView 多标签"
isCJKLanguage = true
draft = false
+++

# 第四十三章：列表、导航与弹窗：多页面应用怎么搭

> 一个能用的 App 基本就是"一列数据 + 一层层页面 + 偶尔蹦出来的弹窗"。SwiftUI 把这三件事的 API 都做得很短，短到你很容易忽略它们各自的坑。这一章只干一件事：把每个坑提前挖出来，让你第一次写列表就写对。

## 43.1 `List` 的三种写法

```swift
import SwiftUI

// 写法一：静态内容，一行一行写死
struct SettingsStatic: View {
    var body: some View {
        List {
            Section("账号") {
                Label("个人资料", systemImage: "person.crop.circle")
                Label("安全", systemImage: "lock")
            }
            Section("关于") {
                Label("版本 1.0", systemImage: "info.circle")
            }
        }
    }
}

// 写法二：数据驱动，元素遵循 Identifiable
struct Note: Identifiable, Hashable {
    let id = UUID()
    var title: String
}

struct NoteList: View {
    let notes: [Note]

    var body: some View {
        List(notes) { note in          // 不用写 id:，因为 Note 自带
            Text(note.title)
        }
    }
}

// 写法三：元素不带 id，自己指定"按什么认身份"
struct TagList: View {
    let tags = ["Swift", "SwiftUI", "并发"]

    var body: some View {
        List(tags, id: \.self) { tag in
            Text(tag)
        }
    }
}

// 界面效果：三种列表外观一致——分区标题 + 一行行内容
```

三种写法在屏幕上看不出差别，区别藏在"身份"上，下一节专门讲。

## 43.2 身份：SwiftUI 里最贵的一课

第 40 章提过身份决定"是不是同一个视图"。在列表里，身份的代价最直观——**身份变了，那行视图的状态就被丢掉重建。**

```swift
import SwiftUI

struct EditableRow: View {
    let title: String
    @State private var draft = ""

    var body: some View {
        TextField("给「\(title)」写备注", text: $draft)
    }
}

struct BadIdentity: View {
    @State private var items = ["苹果", "香蕉", "樱桃"]

    var body: some View {
        List {
            // ❌ 用会被编辑的字段当身份
            ForEach(items, id: \.self) { item in
                EditableRow(title: item)
            }
            Button("把「苹果」改名成「苹果（进口）」") {
                items[0] = "苹果（进口）"
            }
        }
    }
}

// 界面效果：如果你在「苹果」那行的输入框里打了备注，
// 点下面的按钮改名后，那一行的备注会消失——
// 因为在 SwiftUI 眼里，原来的 "苹果" 走了，新来了一个 "苹果（进口）"
```

正确做法是给元素一个**稳定且不随内容变化**的身份：

```swift
import SwiftUI

struct Item: Identifiable {
    let id = UUID()          // 身份在创建时定下，之后编辑内容也不变
    var name: String
}

struct GoodIdentity: View {
    @State private var items = [Item(name: "苹果"), Item(name: "香蕉")]

    var body: some View {
        List(items) { item in
            Text(item.name)   // 改名后身份不变，状态不会被丢
        }
    }
}
```

三条判据，帮你判断一个 `id` 是否合格：

| 问自己 | 不合格的例子 |
| --- | --- |
| 它会随用户编辑而变吗？ | `id: \.title`、`id: \.self`（元素内容会被改） |
| 它在列表里唯一吗？ | `id: \.category`（同分类有多个） |
| 它跨刷新稳定吗？ | `id: \.hashValue`、`id: \.offset` |

⚠️ 还有个"进阶版"坑：`ForEach(items.indices, id: \.self)` 看起来很方便，但**删除中间某一行后，后面所有下标都变了**，SwiftUI 会认为"最后一行没了"，于是把状态错位到别的行上。这个现象是"输入框内容跑到别的行去"的头号原因。要么用 `Identifiable`，要么用 `enumerated()` 配合稳定 id。

## 43.3 删除、移动、选择、刷新

```swift
import SwiftUI

struct ManageList: View {
    @State private var rows = ["草稿", "待审", "已发布"]
    @State private var selection: String?

    var body: some View {
        List(selection: $selection) {
            ForEach(rows, id: \.self) { row in
                Text(row)
                    .swipeActions(edge: .trailing) {
                        Button("删除", role: .destructive) {
                            rows.removeAll { $0 == row }
                        }
                        Button("置顶") {
                            rows.removeAll { $0 == row }
                            rows.insert(row, at: 0)
                        }
                        .tint(.indigo)
                    }
            }
            .onDelete { offsets in rows.remove(atOffsets: offsets) }
            .onMove { from, to in rows.move(fromOffsets: from, toOffset: to) }
        }
        .refreshable {
            try? await Task.sleep(for: .seconds(1))   // 模拟网络刷新
        }
    }
}

// 界面效果：左滑一行出现「删除」和「置顶」；
// 下拉列表出现刷新指示器，一秒后收起
```

两点补充：

- `.onDelete` / `.onMove` 只有写在 `ForEach` 上才生效（它需要"一组可编辑的行"这个概念）。写在 `List` 上无效。
- 用 `.swipeActions` 自定义按钮时，`role: .destructive` 会让按钮自动变红，而且**滑动删除时系统不会自动向数据源发 `onDelete`**——你得在按钮动作里自己删数据。这是最容易"界面删了数据没删"的地方。

关于选中：在 iOS 上单指点击默认是"点一下触发跳转"，要让整行变成"可选中"，需要 `List(selection:)` 并配合编辑模式（`EditButton()` 或 `\.editMode` 环境值）；在 macOS 上选中是默认行为。这类平台差异在第二篇讲条件编译时提过思路，实际写的时候以真机/预览为准。

## 43.4 分区、搜索与分组

```swift
import SwiftUI

struct Inbox: View {
    @State private var query = ""
    private let all = ["发票 3 月", "发票 4 月", "会议纪要", "报销单"]

    private var results: [String] {
        query.isEmpty ? all : all.filter { $0.localizedCaseInsensitiveContains(query) }
    }

    var body: some View {
        NavigationStack {
            List {
                Section("搜索结果") {
                    if results.isEmpty {
                        Text("没有匹配项").foregroundStyle(.secondary)
                    } else {
                        ForEach(results, id: \.self) { Text($0) }
                    }
                }
            }
            .searchable(text: $query, prompt: "搜索文件")
            .navigationTitle("收件箱")
            // 内容为空时给一个比空白更友好的界面
            .overlay {
                if all.isEmpty {
                    ContentUnavailableView("空空如也", systemImage: "tray", description: Text("新文件会自动出现在这里"))
                }
            }
        }
    }
}

// 界面效果：顶部出现系统搜索框；输入「发票」后列表只剩两条；
// 数据为空时中部显示图标 + 一句说明
```

`Section` 除了给标题，还能给页脚（`Section { ... } header: { } footer: { }`）。`ContentUnavailableView` 是这几版新增的标准空状态组件，比手搓一张灰色图省事得多。

## 43.5 `NavigationStack`：一条路径，一层页面

先看最常用的"点进去"，它同时引入了两个概念：**路由值**和**目的地声明**。

```swift
import SwiftUI

struct Fruit: Identifiable, Hashable {
    let id = UUID()
    var name: String
    var note: String
}

struct FruitRoot: View {
    private let fruits = [
        Fruit(name: "苹果", note: "脆的"),
        Fruit(name: "香蕉", note: "软的"),
    ]

    var body: some View {
        NavigationStack {
            List(fruits) { fruit in
                // 注意：这里传的是"值"，不是目标视图
                NavigationLink(value: fruit) {
                    Label(fruit.name, systemImage: "leaf")
                }
            }
            .navigationTitle("水果")
            // 目的地只声明一次，任何 push 这个类型的值都会走到这里
            .navigationDestination(for: Fruit.self) { fruit in
                VStack(spacing: 12) {
                    Text(fruit.name).font(.largeTitle)
                    Text(fruit.note).foregroundStyle(.secondary)
                }
                .navigationTitle(fruit.name)
            }
        }
    }
}

// 界面效果：列表两行；点「苹果」滑入详情页，标题变「苹果」
```

这种"传值 + 集中声明目的地"的写法，比旧版 `NavigationLink(destination:)` 好在两点：**目的地只写一次**，而且**导航状态可以被代码控制**（下面马上讲）。旧写法在简单的两层跳转里依然能用，但超过两层就会到处散落目标视图。

### 用代码控制导航：`path`

把路径交给一个 `@State` 数组，就能做到"点按钮跳三层""登录后清空返回栈"这类需求：

```swift
import SwiftUI

struct Step: Hashable {
    let index: Int
}

struct CheckoutFlow: View {
    @State private var path: [Step] = []

    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 16) {
                Button("开始结算") { path.append(Step(index: 1)) }
                Button("直接跳到第三步") { path = [Step(index: 1), Step(index: 2), Step(index: 3)] }
            }
            .navigationTitle("购物车")
            .navigationDestination(for: Step.self) { step in
                VStack(spacing: 16) {
                    Text("第 \(step.index) 步").font(.title)
                    Button("下一步") { path.append(Step(index: step.index + 1)) }
                    Button("回到根页面") { path.removeAll() }
                }
                .navigationTitle("步骤 \(step.index)")
            }
        }
    }
}

// 界面效果：点「直接跳到第三步」会一次性推入三层；
// 在任意一层点「回到根页面」直接弹回购物车
```

需要混合多种路由类型（商品、订单、设置各是一种）时，把 `[Step]` 换成 `NavigationPath`：

```swift
import SwiftUI

struct Product: Hashable { let id: Int }
struct Order: Hashable { let id: String }

struct MixedRouter: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List {
                Button("看商品") { path.append(Product(id: 1)) }
                Button("看订单") { path.append(Order(id: "A-9")) }
            }
            .navigationDestination(for: Product.self) { Text("商品 \($0.id)") }
            .navigationDestination(for: Order.self) { Text("订单 \($0.id)") }
        }
    }
}
```

`NavigationPath` 是类型擦除的容器，代价是取元素时必须再转回来（`path[0]` 得到的是 `AnyHashable`）。如果所有路由都是同一种类型，用 `[T]` 数组更舒服；**想让导航状态能被保存和恢复（比如 `Codable` 持久化），也要用数组或自定义 `Codable` 路径。**

## 43.6 弹窗家族：五种"浮在上面"的东西

SwiftUI 的弹窗 API 长得像，用途差别不小。一张表先分清：

| 组件 | 典型平台表现 | 用途 |
| --- | --- | --- |
| `.sheet` | 底部抽屉 / 弹出面板 | 次要任务、编辑表单 |
| `.fullScreenCover` | 全屏覆盖（iOS 专属，macOS 上不存在） | 沉浸式流程、引导页 |
| `.alert` | 居中对话框 | 必须让用户确认或知道的事 |
| `.confirmationDialog` | 底部动作列表（iOS）/ 弹出菜单 | 多个破坏性选项 |
| `.popover` | 气泡（iPad/macOS 上是锚定气泡，iPhone 上会退化成 sheet） | 附带说明、小工具 |

```swift
import SwiftUI

struct DrawerDemo: View {
    @State private var showEditor = false
    @State private var showConfirm = false
    @State private var showAlert = false
    @State private var name = "未命名"
    @State private var draft = ""

    var body: some View {
        VStack(spacing: 16) {
            Text("当前：\(name)").font(.headline)

            Button("编辑") {
                draft = name              // 打开前把当前值抄进草稿
                showEditor = true
            }

            Button("删除", role: .destructive) { showConfirm = true }
        }
        // 编辑面板
        .sheet(isPresented: $showEditor) {
            NavigationStack {
                Form {
                    TextField("名称", text: $draft)
                }
                .navigationTitle("编辑名称")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("取消") { showEditor = false }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("保存") {
                            name = draft        // 确认后才落库
                            showEditor = false
                        }
                    }
                }
            }
            .frame(minWidth: 260, minHeight: 160)
        }
        // 破坏性动作确认
        .confirmationDialog("确定删除吗？", isPresented: $showConfirm, titleVisibility: .visible) {
            Button("删除", role: .destructive) {
                name = "已删除"
                showAlert = true
            }
            Button("取消", role: .cancel) { }
        } message: {
            Text("这个操作不可撤销。")
        }
        // 结果告知
        .alert("已删除", isPresented: $showAlert) {
            Button("好") { }
        }
    }
}

// 界面效果：点「编辑」弹出带工具栏的编辑面板，保存后主界面标题更新；
// 点「删除」先弹确认，确认后弹一条结果提示
```

这段代码里藏着两个实用模式，值得单独记住：

**一、"草稿 + 保存"模式。** 编辑类面板不要在打开时直接改主数据，而是先拷一份 `draft`，用户点保存才写回。这样"取消"天然成立——不用写任何回滚逻辑。

**二、`.frame(minWidth:minHeight:)` 给 sheet 一个尺寸。** 在 iPad/macOS 上，不带尺寸的 sheet 可能小得只剩一条缝；给个最小尺寸能让它在各平台都像回事。

`.fullScreenCover` 在 macOS 上不可用，写跨平台代码时要留意：

```swift
import SwiftUI

struct ImmersiveEntry: View {
    @State private var show = false

    var body: some View {
        Button("开始引导") { show = true }
            #if os(iOS)
            .fullScreenCover(isPresented: $show) { Text("全屏引导内容") }
            #else
            .sheet(isPresented: $show) { Text("全屏引导内容") }
            #endif
    }
}
```

## 43.7 标题、工具栏与多标签

```swift
import SwiftUI

struct ToolbarDemo: View {
    @State private var isFavorite = false

    var body: some View {
        NavigationStack {
            Text("正文")
                .navigationTitle("详情")
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button {
                            isFavorite.toggle()
                        } label: {
                            Label("收藏", systemImage: isFavorite ? "star.fill" : "star")
                        }
                    }
                    ToolbarItem(placement: .automatic) {
                        Button("分享") { }
                    }
                }
        }
    }
}

// 界面效果：标题栏右侧出现星标按钮，点亮后变实心；旁边一个"分享"按钮
```

⚠️ 工具栏里常被引用的 `EditButton()`（切换列表编辑模式）**只在 iOS 上可用**，macOS 上根本没有"编辑模式"这个概念。跨平台代码里要么用条件编译包住它，要么改用 macOS 也能用的自定义按钮，就像上面这样。

多标签用 `TabView`：

```swift
import SwiftUI

struct MainTabs: View {
    @State private var selection = 0

    var body: some View {
        TabView(selection: $selection) {
            Text("首页内容")
                .tabItem { Label("首页", systemImage: "house") }
                .tag(0)
            Text("消息内容")
                .tabItem { Label("消息", systemImage: "bubble") }
                .badge(3)
                .tag(1)
            Text("我的内容")
                .tabItem { Label("我的", systemImage: "person") }
                .tag(2)
        }
    }
}

// 界面效果：底部（或 macOS 顶部）三个标签，第二个带红色角标 3
```

⚠️ `TabView` 里每个标签的内容**默认会被同时保留**（切回来时状态还在），这和 `NavigationStack` 的 push/pop 语义不同。别把"每次进入都要重新加载"的逻辑写成 `onAppear`，那在标签切换时会反复触发；要"只加载一次"用 `.task`（第 46 章）。

## 43.8 一个可运行的多页面骨架

把本章零件装起来，就是一个像样的应用结构：

```swift
import SwiftUI
import Observation

struct Task: Identifiable, Hashable {
    let id = UUID()
    var title: String
    var done = false
}

@Observable
final class TaskStore {
    var tasks: [Task] = [Task(title: "写周报"), Task(title: "买咖啡豆")]
    func toggle(_ task: Task) {
        guard let i = tasks.firstIndex(where: { $0.id == task.id }) else { return }
        tasks[i].done.toggle()
    }
}

struct TaskListView: View {
    @Environment(TaskStore.self) private var store
    @State private var showingNew = false

    var body: some View {
        List {
            ForEach(store.tasks) { task in
                NavigationLink(value: task) {
                    HStack {
                        Image(systemName: task.done ? "checkmark.circle.fill" : "circle")
                            .foregroundStyle(task.done ? .green : .secondary)
                        Text(task.title).strikethrough(task.done)
                    }
                }
            }
        }
        .navigationTitle("待办")
        .navigationDestination(for: Task.self) { task in
            TaskDetailView(task: task)
        }
        .toolbar {
            Button("新建", systemImage: "plus") { showingNew = true }
        }
        .sheet(isPresented: $showingNew) {
            NewTaskSheet()
        }
    }
}

struct TaskDetailView: View {
    let task: Task
    @Environment(TaskStore.self) private var store

    var body: some View {
        VStack(spacing: 16) {
            Text(task.title).font(.title2)
            Button(task.done ? "标记未完成" : "标记完成") { store.toggle(task) }
        }
        .padding()
        .navigationTitle("详情")
    }
}

struct NewTaskSheet: View {
    @Environment(TaskStore.self) private var store
    @Environment(\.dismiss) private var dismiss
    @State private var title = ""

    var body: some View {
        NavigationStack {
            Form { TextField("任务名称", text: $title) }
                .navigationTitle("新建")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("取消") { dismiss() }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("添加") {
                            store.tasks.append(Task(title: title))
                            dismiss()
                        }
                        .disabled(title.trimmingCharacters(in: .whitespaces).isEmpty)
                    }
                }
        }
    }
}

@main
struct TasksApp: App {
    @State private var store = TaskStore()

    var body: some Scene {
        WindowGroup {
            NavigationStack { TaskListView() }
                .environment(store)
        }
    }
}

// 界面效果：一个待办列表，点任意一行进入详情；
// 右上角「新建」弹出表单，添加后新任务立刻出现在列表里
```

这个骨架体现的正是第 41 章的数据流：**数据放在环境的 `TaskStore` 里，列表读它、详情页改它、表单往它里面追加**，三个视图没有任何互相持有关系。

## 43.9 本章小结

| 概念 | 一句话 |
| --- | --- |
| `List` 三种写法 | 静态、`Identifiable`、手写 `id:`，差别在身份策略 |
| 身份 | 稳定且不可编辑；用错会让行状态错位或丢失 |
| `\.self` / `indices` 当 id | 内容或顺序一变身份就变，是经典陷阱 |
| `swipeActions` | 自定义滑动按钮，删除要自己在动作里改数据 |
| `onDelete` / `onMove` | 只对 `ForEach` 有效 |
| `searchable` / `ContentUnavailableView` | 搜索框与标准空状态 |
| `NavigationLink(value:)` + `navigationDestination` | 传值式路由，目的地集中声明 |
| `path` | `[T]` 或 `NavigationPath`，代码控制跳转与返回栈 |
| `sheet` / `alert` / `confirmationDialog` | 三种不同"浮层"语义，按用途选 |
| `TabView` | 多标签；内容默认保留，别用 `onAppear` 当"只加载一次" |

## 43.10 本章易错点速查

| 容易踩的地方 | 正确认识 |
| --- | --- |
| `ForEach(items, id: \.self)` 里允许编辑元素 | 内容一变身份就变，状态会重置；用 `Identifiable` |
| `ForEach(items.indices)` + 删除 | 下标整体前移，状态会错位到别的行 |
| `navigationDestination` 写在 `List` 内部的子视图上 | 应写在 `NavigationStack` 的直接内容上，否则跳转无效 |
| `NavigationLink(destination:)` 与 `NavigationLink(value:)` 混用 | 同一条路径里可能重复 push 同一个页面；统一用 value 更安全 |
| `swipeActions` 删除后数据还在 | 系统不会自动调 `onDelete`，要在动作里删 |
| 编辑面板直接改主数据 | 用"草稿 + 保存"模式，取消才不用写回滚 |
| `fullScreenCover` 在 macOS 上编译报错 | 它不可用于 macOS，用条件编译退回 `sheet` |
| 以为切标签回来会重新加载 | `TabView` 会保留内容；"只跑一次"的逻辑放 `.task` |
| 在 sheet 里忘了 `dismiss` | 用 `@Environment(\.dismiss)` 或自己控制 `isPresented` |

## 43.11 下章预告

列表、页面、弹窗都有了，还差"让用户往里填东西"。下一章讲表单：`Form` 的自动排版、`TextField` 的几种取值方式、`Picker`/`Toggle`/`Slider`、焦点管理，以及表单校验该放在哪里才不啰嗦。
