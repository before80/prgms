+++
title = "第 9 章 数据落地：三态、网络与持久化"
weight = 90
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "把「加载中/成功/失败」建对模；.task 与 .task(id:) 的分工；网络请求怎么写不搞乱 body；从 @AppStorage 到 SwiftData 的持久化选择"
isCJKLanguage = true
draft = false
+++

# 第 9 章：数据落地

> 前八章做出来的界面，数据都是硬编码的。这一章解决最后一块：**数据从哪来、存在哪、失败时怎么办。**
>
> 这一章也是第 2 章 `@Observable` 的收口——那个模型终于要装上真正的数据了。

## 9.1 三态建模：`if isLoading` 是错的

先看一段"能跑但会出问题"的代码：

```text
@State private var isLoading = false
@State private var items: [Item] = []
@State private var errorMessage: String?

var body: some View {
    if isLoading {
        ProgressView()
    } else if let errorMessage {
        Text(errorMessage)
    } else {
        List(items) { ... }
    }
}
```

这段代码的问题**不在语法，而在状态空间**：三个变量可以组合出 8 种状态，其中大多数是**没有意义的**——比如 `isLoading == true` 且 `items` 非空且 `errorMessage != nil`。界面该显示什么？没人知道。

🔥 **根本问题：这三个变量描述的是同一件事的三个互斥侧面，却用了三个独立的状态来存。** 于是"非法状态"在类型层面是允许的，就一定会有人（包括未来的你）写出非法组合。

### 用 `enum` 让非法状态无法表达

```swift
enum LoadState<Value> {
    case idle                 // 还没开始
    case loading              // 正在加载（可以带上"旧数据"以便刷新时还显示着）
    case loaded(Value)        // 成功了，数据在这儿
    case failed(String)       // 失败了，理由在这儿
}
```

现在**只有四种状态，且互斥**——不可能同时"加载中"又"有数据又报错"。这就是第 2 章那句"能用 enum 建模就别用一堆可选值"的具体兑现。

用起来：

```swift
struct ItemListView: View {
    @State private var state: LoadState<[String]> = .idle

    var body: some View {
        Group {
            switch state {
            case .idle:
                ContentUnavailableView("还没加载", systemImage: "tray")
            case .loading:
                ProgressView("加载中…")
            case .loaded(let items):
                List(items, id: \.self) { Text($0) }
            case .failed(let message):
                ContentUnavailableView {
                    Label("加载失败", systemImage: "exclamationmark.triangle")
                } description: {
                    Text(message)
                } actions: {
                    Button("重试") { Task { await load() } }
                }
            }
        }
        .task { await load() }
    }

    func load() async {
        state = .loading
        do {
            let items = try await fetchItems()
            state = .loaded(items)
        } catch {
            state = .failed(error.localizedDescription)
        }
    }

    func fetchItems() async throws -> [String] {
        try await Task.sleep(for: .milliseconds(300))     // 假装在联网
        return ["第一条", "第二条"]
    }
}
```

⚠️ 注意 `switch` 是**穷尽**的——以后你给 `LoadState` 加一个 `.refreshing`，编译器会立刻把所有没处理它的地方列出来。这是三个布尔变量永远给不了的保护。

💭 **关键提升**：把 `switch state` 写在一个 `Group` 里、每个 `case` 返回不同的视图，是 SwiftUI 里处理"多状态页面"的标准形状。它天然满足第 1 章讲的"分支必须穷尽"，也让 `body` 一眼能读完。

### 一个进阶细节：刷新时保留旧数据

朴素的 `.loading` 会在刷新时把已有内容清掉，用户看到"闪一下白屏"。更好的做法是让 `loading` 带上旧数据：

```swift
enum Refreshable<Value> {
    case initial                   // 首次加载：什么都不显示
    case loading(previous: Value?) // 刷新：可能还留着旧数据
    case loaded(Value)
    case failed(String, previous: Value?)
}
```

🝖 这个模式在真实项目里很值得用，但**先别急着上**——三态跑通了，再考虑四态。过早的复杂度也是一种 bug。

## 9.2 `.task`：不要用 `onAppear` + `Task`

界面出现时要发请求，很多人的第一反应是：

```swift
// 🛑 能跑，但有问题
.onAppear {
    Task { await load() }
}
```

问题在于：**这个 `Task` 和视图的生命周期没关系。** 视图消失了，任务还在跑；视图重新出现，又起一个新任务。你会得到重复请求、以及"任务回来时视图已经没了"的诡异状态。

正确的工具是 `.task`：

```text
.task { await load() }
```

| | `.onAppear { Task { } }` | `.task { }` |
| --- | --- | --- |
| 任务与视图的关系 | 无关，自己管自己 | **绑定**：视图消失就自动取消 |
| 视图重新出现 | 又起一个（可能重复） | 重新起一个（符合预期） |
| 取消 | 要自己写 | 自动 |
| 支持 `async` | 不直接支持 | ✅ 就是异步闭包 |

🔥 `.task` **在视图消失时会自动取消任务**，这是它最重要的特性。你不需要写任何取消代码——但你的 `load()` 要能响应取消（用会抛 `CancellationError` 的 API，或定期 `Task.checkCancellation()`）。

### `.task(id:)`：值一变就重来

需要在"某个值变化时重新加载"的场景（切换分类、改变搜索词），用 `.task(id:)`：

```swift
struct SearchView: View {
    @State private var query = ""
    @State private var results: LoadState<[String]> = .idle

    var body: some View {
        List {
            switch results {
            case .loaded(let items): ForEach(items, id: \.self) { Text($0) }
            default: EmptyView()
            }
        }
        .searchable(text: $query)
        .task(id: query) {                    // ← query 一变，旧任务自动取消，新任务自动开始
            guard !query.isEmpty else { results = .idle; return }
            results = .loading
            do {
                try await Task.sleep(for: .milliseconds(200))     // 模拟防抖窗口
                results = .loaded(["\(query) 的结果 1", "\(query) 的结果 2"])
            } catch {
                results = .failed("已取消或失败")
            }
        }
    }
}
```

⚠️ `.task(id:)` 干的事**比你想的多**：它不只是"重新执行"，而是**先取消上一个任务**再执行新的。所以：

- 它天然自带**防抖**效果（旧请求还没回来就被取消）；
- 但你在闭包里必须**正确处理取消**，否则旧请求的结果可能覆盖新结果（经典的"搜索词是 A，显示的是 B 的结果"）。

💭 上面例子里的 `try await Task.sleep` 就是为了演示这一点：快速切换搜索词时，前面的任务会在 sleep 处被取消并抛错，于是不会去写 `results`。

### `.task` 与 `@Observable` 模型的分工

真实项目里，加载逻辑通常**不该写在视图里**。更干净的分工：

```swift
@Observable
final class ItemStore {
    enum Phase { case idle, loading, loaded([String]), failed(String) }
    private(set) var phase: Phase = .idle       // private(set)：外面只能读

    func load() async {
        phase = .loading
        do {
            let items = try await fetch()
            phase = .loaded(items)
        } catch is CancellationError {
            // 被取消就别改状态，交给下一次加载
        } catch {
            phase = .failed(error.localizedDescription)
        }
    }

    private func fetch() async throws -> [String] {
        try await Task.sleep(for: .milliseconds(300))
        return ["第一条", "第二条", "第三条"]
    }
}

struct ItemList: View {
    @State private var store = ItemStore()      // 视图持有模型

    var body: some View {
        List {
            switch store.phase {
            case .loaded(let items): ForEach(items, id: \.self) { Text($0) }
            case .loading: ProgressView()
            case .failed(let msg): Text(msg)
            case .idle: Text("准备中")
            }
        }
        .task { await store.load() }
    }
}
```

🔥 这个结构的价值：**视图退化成"把 phase 翻译成界面"，一点逻辑都不含。** 于是 `store` 可以被单元测试（不需要渲染），也能被预览复用（`#Preview { ItemList() }` 里塞一个假数据 store 就行）。

⚠️ `private(set) var phase` 这个写法很关键：它让视图**只能读、不能写**，保证了"状态只能由 store 自己改"。这比把 `phase` 写成公开可写要安全得多。

## 9.3 网络请求：写好那一次调用

网络代码本身在 [Swift 速查表第 9 章]({{< relref "../CheatSheet/09-Error-Handling-and-Concurrency.md" >}}) 有完整讲法，这里只讲"和 SwiftUI 配合"的部分。

```swift
struct Post: Codable, Identifiable {
    let id: Int
    let title: String
}

struct PostService {
    var baseURL = URL(string: "https://jsonplaceholder.typicode.com")!

    func posts() async throws -> [Post] {
        let url = baseURL.appending(path: "posts")
        var request = URLRequest(url: url)
        request.timeoutInterval = 15

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let http = response as? HTTPURLResponse else {
            throw URLError(.badServerResponse)
        }
        guard (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)      // 真实项目里带上状态码和响应体
        }
        return try JSONDecoder().decode([Post].self, from: data)
    }
}
```

### 四个必须处理的点

| 点 | 为什么 |
| --- | --- |
| 检查 `HTTPURLResponse` 的 `statusCode` | `data(for:)` **不把 4xx/5xx 当错误**，它照常返回数据。不检查就会拿错误页去 `decode`，报一个莫名其妙的解码错 |
| 设 `timeoutInterval` | 默认超时很长，用户会以为卡死 |
| 解码失败要给有意义的错误 | `DecodingError` 的默认描述很难读，值得包装一层 |
| 大文件**不要**整个读进内存 | 用 `URLSession.bytes(for:)` 流式读 |

⚠️ 第一条是最高频的坑。很多人写：

```swift
let (data, _) = try await URLSession.shared.data(from: url)   // 🛑 忽略了 response
return try JSONDecoder().decode([Post].self, from: data)      // 404 时在这里报解码错
```

于是排查方向完全跑偏——你会去查数据模型，而真实原因是 URL 写错了。

### Swift 6 严格并发下的 `Sendable`

网络层最容易撞上的编译错误是 `Sendable`。规则很简单：

| 类型 | 是否需要操心 |
| --- | --- |
| `Codable` 结构体（全是值类型） | ✅ 自动满足 |
| 带可变状态的类 | ❌ 需要 `@Observable` + `@MainActor`，或加锁 |

🔥 最省事的做法：**把数据模型写成 `struct`，把 store 标 `@MainActor`。**

```swift
struct Post: Codable, Identifiable {
    let id: Int
    let title: String
}

struct PostService {
    func posts() async throws -> [Post] {
        // 真实实现见上文；这里用一行假数据代替网络
        [Post(id: 1, title: "示例")]
    }
}

@MainActor
@Observable
final class PostStore {
    private(set) var posts: [Post] = []
    private let service = PostService()

    func load() async throws {
        posts = try await service.posts()      // service 是无状态的 struct，跨 actor 传没问题
    }
}
```

`@MainActor` 保证所有状态改动都在主线程，也就顺带解决了"UI 更新必须在主线程"的问题——**你不需要写 `DispatchQueue.main.async`**。

## 9.4 持久化：四种选择

| 方案 | 适合存什么 | 复杂度 | 起点 |
| --- | --- | --- | --- |
| `@AppStorage` | 开关、少量偏好设置（`UserDefaults` 的封装） | ⭐ | iOS 14 |
| 文件（JSON / 二进制） | 你自己的结构化数据，量不大 | ⭐⭐ | 一直可用 |
| `SwiftData` | 关系型数据、需要查询/排序/迁移 | ⭐⭐⭐ | iOS 17 |
| 数据库（SQLite / GRDB 等） | 极致控制、跨平台、复杂查询 | ⭐⭐⭐⭐ | 第三方 |

💭 **选择判据**：先问"这些数据需要被**查询**吗？"

- 只是"存下来、读出来" → 文件足够；
- 需要"按条件筛选、排序、关联" → `SwiftData`；
- 只是几个开关 → `@AppStorage`。

### `@AppStorage`：几行就够

```swift
struct SettingsView: View {
    @AppStorage("showCompleted") private var showCompleted = true
    @AppStorage("sortOrder") private var sortOrder = "created"

    var body: some View {
        Form {
            Toggle("显示已完成", isOn: $showCompleted)
            Picker("排序", selection: $sortOrder) {
                Text("按创建时间").tag("created")
                Text("按标题").tag("title")
            }
        }
    }
}
```

🔥 它的好处是**完全透明**：读写就像一个普通属性，但值会自动存进 `UserDefaults`、下次启动还在。

⚠️ 三个限制：

| 限制 | 说明 |
| --- | --- |
| 只支持基本类型 | `Bool` / `Int` / `Double` / `String` / `URL` / `Data`，以及它们的可选与数组 |
| **不是数据库** | 存大数组或二进制会让启动变慢（`UserDefaults` 在启动时被整体读取） |
| 不适合敏感数据 | 它在明文 plist 里，密码/token 要用 Keychain |

### 文件：自己控制一切

```swift
struct FileStore {
    var directory: URL {
        // ⚠️ 用 Application Support 存"用户数据"，不要用 Documents（会被 iCloud 备份、也可能对用户可见）
        (try? FileManager.default.url(
            for: .applicationSupportDirectory,
            in: .userDomainMask,
            appropriateFor: nil,
            create: true
        )) ?? URL.temporaryDirectory
    }

    func save(_ items: [String]) throws {
        let url = directory.appending(path: "items.json")
        let data = try JSONEncoder().encode(items)
        try data.write(to: url, options: .atomic)      // ← .atomic：先写临时文件再替换
    }

    func load() throws -> [String] {
        let url = directory.appending(path: "items.json")
        guard FileManager.default.fileExists(atPath: url.path) else { return [] }
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode([String].self, from: data)
    }
}
```

三个要点：

| 要点 | 为什么 |
| --- | --- |
| 用 `.applicationSupportDirectory` | `Documents` 在 iOS 上对用户可见、且进备份；`Application Support` 才是"App 自己的数据" |
| 写用 `.atomic` | 断电/崩溃时不会留下半个损坏的文件 |
| `load()` 要能处理"文件不存在" | 首次启动必然不存在，别当错误 |

⚠️ 文件读写是**阻塞**的。数据量大时别在主线程做——用 `Task.detached` 或者干脆用 `actor` 包起来：

```swift
actor FileStore {                     // actor 保证串行访问，避免并发写坏文件
    private let url: URL
    init(url: URL) { self.url = url }
    func save(_ items: [String]) throws {
        try JSONEncoder().encode(items).write(to: url, options: .atomic)
    }
}
```

### `SwiftData`：需要"查询"时才上

```swift
import SwiftData
import SwiftUI

@Model
final class Todo {
    var title: String
    var done: Bool
    var createdAt: Date

    // ⚠️ 必须写显式 init：@Model 不会替你合成一个可用的初始化器
    init(title: String, done: Bool = false, createdAt: Date = .now) {
        self.title = title
        self.done = done
        self.createdAt = createdAt
    }
}

struct TodoListView: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \Todo.createdAt, order: .reverse) private var todos: [Todo]

    var body: some View {
        List {
            ForEach(todos) { todo in
                Text(todo.title)
            }
            .onDelete { offsets in
                for i in offsets { context.delete(todos[i]) }
            }
        }
    }
}

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { TodoListView() }
            .modelContainer(for: Todo.self)          // ← 挂上容器，@Query 才有数据源
    }
}
```

四个关键点：

| 点 | 说明 |
| --- | --- |
| `@Model` 的类**必须写显式 `init`** | 🔬 实测：不写会报 `@Model requires an initializer be provided for 'Item'`（连 `var name: String = ""` 这种带默认值的也不行） |
| `@Query` 自动刷新 | 数据一变，视图自动更新，不用手动通知 |
| `@Query` 支持排序/筛选 | `@Query(filter:sort:)`，这是它比"自己存数组"强的地方 |
| `modelContainer` 必须挂在 App 上 | 忘了挂，`@Query` 拿不到数据（而且报错位置可能很偏） |

⚠️ `@Model` 生成的是**类**（引用类型），但 `@Query` 交给你的是 `[Todo]`，在视图里当值用就行。**不要**自己去 new 一个 `Todo` 然后期望它被保存——必须通过 `modelContext.insert(...)`。

## 9.5 完整可运行文件

这个例子用一个 `@Observable` store 管住三态，用文件做持久化（跨平台、无需 SwiftData）：

```swift
import SwiftUI
import Observation

// 数据模型：值类型，Codable 让它能直接落盘
struct Note: Codable, Identifiable, Hashable {
    var id = UUID()
    var text: String
    var createdAt = Date.now
}

// 存储层：actor 保证串行写，避免并发冲突
actor NoteFileStore {
    private let url: URL

    init() {
        let dir = (try? FileManager.default.url(
            for: .applicationSupportDirectory, in: .userDomainMask,
            appropriateFor: nil, create: true
        )) ?? URL.temporaryDirectory
        self.url = dir.appending(path: "swiftuibasic-notes.json")
    }

    func load() throws -> [Note] {
        guard FileManager.default.fileExists(atPath: url.path) else { return [] }
        return try JSONDecoder().decode([Note].self, from: Data(contentsOf: url))
    }

    func save(_ notes: [Note]) throws {
        try JSONEncoder().encode(notes).write(to: url, options: .atomic)
    }
}

// 状态层：三态 + 增删改，视图一点都不碰 I/O
@MainActor
@Observable
final class NoteStore {
    enum Phase {
        case loading
        case ready
        case failed(String)
    }

    private(set) var phase: Phase = .loading
    private(set) var notes: [Note] = []
    private let store = NoteFileStore()

    func load() async {
        phase = .loading
        do {
            notes = try await store.load()
            phase = .ready
        } catch {
            phase = .failed(error.localizedDescription)
        }
    }

    func add(_ text: String) async {
        guard !text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        notes.insert(Note(text: text), at: 0)
        await persist()
    }

    func delete(at offsets: IndexSet) async {
        notes.remove(atOffsets: offsets)
        await persist()
    }

    private func persist() async {
        do {
            try await store.save(notes)
        } catch {
            phase = .failed("保存失败：\(error.localizedDescription)")
        }
    }
}

// 视图层：只负责把 phase 翻译成界面
struct NotesView: View {
    @State private var store = NoteStore()
    @State private var draft = ""

    var body: some View {
        NavigationStack {
            Group {
                switch store.phase {
                case .loading:
                    ProgressView("读取中…")

                case .ready:
                    if store.notes.isEmpty {
                        ContentUnavailableView(
                            "还没有笔记",
                            systemImage: "note.text",
                            description: Text("在下面输入第一条内容。")
                        )
                    } else {
                        List {
                            ForEach(store.notes) { note in
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(note.text)
                                    Text(note.createdAt, format: .dateTime.hour().minute())
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                            }
                            .onDelete { offsets in
                                Task { await store.delete(at: offsets) }
                            }
                        }
                    }

                case .failed(let message):
                    ContentUnavailableView {
                        Label("出错了", systemImage: "exclamationmark.triangle")
                    } description: {
                        Text(message)
                    } actions: {
                        Button("重试") { Task { await store.load() } }
                    }
                }
            }
            .navigationTitle("笔记")
            .safeAreaInset(edge: .bottom) {
                HStack {
                    TextField("写点什么…", text: $draft)
                        .textFieldStyle(.roundedBorder)
                        .onSubmit { submit() }
                    Button("添加") { submit() }
                        .buttonStyle(.borderedProminent)
                        .disabled(draft.trimmingCharacters(in: .whitespaces).isEmpty)
                }
                .padding()
                .background(.bar)
            }
        }
        .task { await store.load() }
    }

    private func submit() {
        let text = draft
        draft = ""
        Task { await store.add(text) }
    }
}

#Preview {
    NotesView()
}
```

💭 跑起来试三件事：

1. **输入并添加一条**，然后**完全退出 App 再打开**——数据还在（文件持久化生效）；
2. **快速连续添加多条**，看 `actor` 如何保证写入不打架；
3. **把文件删掉再启动**（或在 `load()` 里改成 `throw`），看 `.failed` 分支长什么样。

🔥 注意这个文件里**视图层一行 I/O 都没有**。`NotesView` 只做两件事：把 `phase` 翻译成界面、把用户输入交给 `store`。这就是"数据落地"章节最想让你带走的架构。

## 9.6 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| `isLoading` + `items` + `errorMessage` 三个独立状态 | 能组合出无意义的非法状态，界面行为不可预测 | 用 `enum` 三态建模 |
| `.onAppear { Task { await load() } }` | 任务和视图生命周期无关，重复请求、消失后还在跑 | 用 `.task { }`（自动取消） |
| `data(for:)` 不检查 `statusCode` | 4xx/5xx **不会抛错**，你会在 `decode` 处收到莫名其妙的错误 | 检查 `HTTPURLResponse.statusCode` |
| `.task(id:)` 里不处理取消 | 旧请求的结果覆盖新结果（搜索框显示错内容） | 用会抛 `CancellationError` 的 API，或主动检查 |
| 把网络请求写在 `body` 里 | 每次重绘都发一次 | 放进 store，由 `.task` 触发 |
| `@Model` 不写 `init` | 🔬 报 `@Model requires an initializer be provided for 'Item'`（带默认值也不行） | 显式写 `init` |
| 忘了 `.modelContainer` | `@Query` 拿不到数据 | 挂在 `App` 的 `Scene` 上 |
| 用 `Documents` 存 App 私有数据 | iOS 上对用户可见、且进 iCloud 备份 | 用 `.applicationSupportDirectory` |
| 写文件不加 `.atomic` | 崩溃时留下半个损坏文件 | `options: .atomic` |
| `UserDefaults` 存大数组 | 启动变慢（启动时整体读取） | 用文件或数据库 |
| 敏感数据放 `@AppStorage` | 明文 plist | 用 Keychain |
| 忘了 UI 更新要在主线程 | 各种诡异崩溃 | 给 store 标 `@MainActor`，就不用手写 `DispatchQueue.main` |

## 9.7 下一章

数据能落地了，App 就算"能用"。但"能用"和"好用"之间还差三件事，接下来三章分别处理：

- **第 10 章 性能与调试**：`body` 被调用多少次其实不重要，那**什么才重要**？怎么用工具找到真正的瓶颈。
- **第 11 章 可访问性与适配**：把字号调到最大、打开旁白、切换深色模式——你的布局还站得住吗？
- **第 12/13 章 绘制与特效**：`Shape`、`Canvas`、材质与混合模式，把界面从"整齐"做到"好看"。
