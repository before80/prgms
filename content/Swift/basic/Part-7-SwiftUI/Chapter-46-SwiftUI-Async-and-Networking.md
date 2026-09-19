+++
title = "第46章 异步、网络与生命周期：数据从哪来"
weight = 460
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "task 修饰符的生命周期、三态建模、async let 并发、URLSession 请求、取消与去抖"
isCJKLanguage = true
draft = false
+++

# 第四十六章：异步、网络与生命周期：数据从哪来

> 真实的应用里，界面上大部分数据都不是"你造的"，而是"你去要来的"。要数据这件事有三个绕不开的性质：**会慢、会失败、可能在你不要它的时候还在跑。** 这一章就围绕这三点，把 SwiftUI 里处理异步数据的标准做法立起来。

## 46.1 `.task` 不是 `onAppear` 的异步版

新手最常见的写法是在 `onAppear` 里起一个 `Task { }`。它能跑，但你会丢掉三样东西：

```swift
import SwiftUI

struct NaiveView: View {
    @State private var text = "加载中"

    var body: some View {
        Text(text)
            .onAppear {
                // ❌ 这个任务跟视图没有隶属关系：
                // 视图消失后它还在跑；视图再次出现又会起一个新的
                Task {
                    text = await fetchTitle()
                }
            }
    }

    func fetchTitle() async -> String { "标题" }
}
```

换成 `.task`：

```swift
import SwiftUI

struct TaskView: View {
    @State private var text = "加载中"

    var body: some View {
        Text(text)
            .task {
                // ✅ 视图消失时，这个任务会被自动取消
                text = await fetchTitle()
            }
    }

    func fetchTitle() async -> String { "标题" }
}

// 界面效果：进入页面时显示"加载中"，请求回来后变成"标题"
```

两者的差别可以列成一张表：

| | `onAppear` + `Task { }` | `.task { }` |
| --- | --- | --- |
| 视图消失时 | 任务继续跑（泄漏风险） | **自动取消** |
| 视图再次出现 | 每次都起新任务 | 每次都重新起任务（但旧的已取消） |
| 属于哪个隔离域 | 需要自己标注 `@MainActor` | 自动继承视图的隔离域（`body` 所在的 `MainActor`） |
| 能不能依赖某个值 | 不能，得自己写 `onChange` | 能，用 `.task(id:)` |

一句话结论：**只要是在视图生命周期里发起的异步工作，就用 `.task`。** `onAppear` 留给纯粹同步的副作用（比如埋点）。

## 46.2 `.task(id:)`：值一变，旧任务自动取消，新任务自动开始

这是 `.task` 相比"`onAppear` + `onChange` + 手动取消"最省事的地方：

```swift
import SwiftUI

struct DebouncedSearch: View {
    @State private var query = ""
    @State private var results: [String] = []

    var body: some View {
        List(results, id: \.self) { Text($0) }
            .searchable(text: $query, prompt: "搜索")
            // id 一变化，上一次任务就被取消，然后立刻开始新的
            .task(id: query) {
                do {
                    try await Task.sleep(for: .milliseconds(300))   // 输入停顿 300ms 才真的请求
                } catch {
                    return                                          // 被新输入打断，安静退出
                }
                results = query.isEmpty ? [] : ["\(query) 的结果 A", "\(query) 的结果 B"]
            }
    }
}

// 界面效果：快速连打几个字母时不会每个字母都请求；
// 停手 300 毫秒后才出现「xx 的结果 A / B」两条
```

这段代码里有一个非常值得单独拎出来的模式：**用 `Task.sleep` 当"去抖"，用 `catch { return }` 当"被打断就放弃"。** 三行代码就实现了完整的去抖，不需要引入计时器、不需要额外的状态变量。

`.task(id:)` 的 `id` 必须是 `Equatable`。常见的几个用法：

| `id` 用 | 效果 |
| --- | --- |
| `query` | 搜索去抖、联动请求 |
| `selectedID`（选中的记录） | 切换详情时自动重新加载 |
| `isPresented` | 弹窗打开时才加载内容 |

## 46.3 三态建模：加载中 / 成功 / 失败

界面加载数据时，永远只有三种（加上"还没开始"是四种）状态。把它们建模成一个枚举，`switch` 一次写完，界面就不可能漏掉某一种。

```swift
import SwiftUI

enum LoadState<Value> {
    case idle
    case loading
    case loaded(Value)
    case failed(String)
}

struct FeedView: View {
    @State private var state: LoadState<[String]> = .idle

    var body: some View {
        Group {
            switch state {
            case .idle, .loading:
                ProgressView("加载中…")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)

            case .loaded(let items) where items.isEmpty:
                ContentUnavailableView("还没有内容", systemImage: "tray")

            case .loaded(let items):
                List(items, id: \.self) { Text($0) }

            case .failed(let message):
                ContentUnavailableView {
                    Label("加载失败", systemImage: "wifi.exclamationmark")
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
        try? await Task.sleep(for: .milliseconds(400))
        state = .loaded(["第一条", "第二条"])
    }
}

// 界面效果：先显示居中的"加载中…"，
// 约 0.4 秒后变成两行列表
```

为什么推荐枚举而不是"三个布尔/可选值"？对比一下就很清楚：

| 写法 | 问题 |
| --- | --- |
| `var isLoading = false` + `var items: [X]?` + `var error: String?` | 出现了"既在加载又有错误"这种非法组合，编译器不会拦你 |
| `enum LoadState` | 四种状态互斥，`switch` 必须穷尽，非法组合根本写不出来 |

这正是第 16 章枚举与第 24 章类型系统想告诉你的同一个道理：**让类型帮你排除掉不可能的情况。**

## 46.4 并发请求：`async let` 与任务组

如果一个页面要三份互不相关的数据，串行请求的总耗时就是三者相加。`async let` 让它们同时出发：

```swift
import Foundation

struct Profile: Sendable { let name: String }
struct Orders: Sendable { let count: Int }

func fetchProfile() async throws -> Profile {
    try await Task.sleep(for: .milliseconds(100))
    print("资料请求完成")
    return Profile(name: "Mia")
}

func fetchOrders() async throws -> Orders {
    try await Task.sleep(for: .milliseconds(40))
    print("订单请求完成")
    return Orders(count: 3)
}

async let profile = fetchProfile()
async let orders = fetchOrders()
let (p, o) = try await (profile, orders)
print("\(p.name) 有 \(o.count) 个订单")
// prints: 订单请求完成
// prints: 资料请求完成
// prints: Mia 有 3 个订单
```

请特别看一眼输出顺序：**慢的那个（100 毫秒）反而后打印，快的那个（40 毫秒）先打印。** 如果两个请求是串行的，顺序必然是先"资料"后"订单"（因为代码里先写）。输出顺序反过来，正是它们同时在跑的证明。

需要动态数量的并发（比如"每个 id 都要拉一次详情"）时，用任务组：

```swift
import Foundation

func fetchDetail(_ id: Int) async throws -> String {
    try await Task.sleep(for: .milliseconds(50))
    return "详情 \(id)"
}

func fetchAll(ids: [Int]) async throws -> [String] {
    try await withThrowingTaskGroup(of: String.self) { group in
        for id in ids {
            group.addTask { try await fetchDetail(id) }
        }
        var results: [String] = []
        for try await detail in group {
            results.append(detail)
        }
        return results.sorted()      // 完成顺序不确定，需要时自己排序
    }
}

let all = try await fetchAll(ids: [1, 2, 3, 4])
print(all)
// prints: ["详情 1", "详情 2", "详情 3", "详情 4"]
```

⚠️ 任务组的返回顺序是**完成顺序**，不是提交顺序。要稳定顺序就按 id 排序，或者让每个任务返回 `(id, value)` 再排。

## 46.5 网络请求：朴素但完整的一套

SwiftUI 不提供网络层，用的还是 `URLSession`。一个"能上生产"的请求函数需要做四件事：拼 URL、发请求、检查状态码、解码。缺一件都会在未来某天变成"界面莫名其妙没数据"。

```swift
import Foundation

struct Article: Identifiable, Decodable, Hashable {
    let id: Int
    let title: String
}

enum FeedError: LocalizedError {
    case badStatus(Int)
    case decoding

    var errorDescription: String? {
        switch self {
        case .badStatus(let code): "服务器返回了 \(code)"
        case .decoding: "返回的数据看不懂"
        }
    }
}

func fetchArticles(matching query: String, session: URLSession = .shared) async throws -> [Article] {
    var components = URLComponents(string: "https://example.com/api/articles")!
    if !query.isEmpty {
        components.queryItems = [URLQueryItem(name: "q", value: query)]
    }
    guard let url = components.url else { throw URLError(.badURL) }

    // 用 URLRequest 才能加超时、缓存策略、请求头
    var request = URLRequest(url: url)
    request.timeoutInterval = 10
    request.setValue("application/json", forHTTPHeaderField: "Accept")

    let (data, response) = try await session.data(for: request)

    guard let http = response as? HTTPURLResponse else { throw URLError(.badServerResponse) }
    guard (200..<300).contains(http.statusCode) else { throw FeedError.badStatus(http.statusCode) }

    do {
        return try JSONDecoder().decode([Article].self, from: data)
    } catch {
        throw FeedError.decoding        // 把底层解码错误换成用户看得懂的话
    }
}
```

四个要点：

- **`session.data(for:)` 而不是 `data(from:)`**：只有前者能带 `URLRequest`（超时、请求头、缓存策略）。
- **一定要检查 `HTTPURLResponse.statusCode`。** `data(for:)` 在收到 404/500 时**不会抛错**，它只负责"网络层面通了"。不检查状态码就去解码，用户看到的是"返回的数据看不懂"这种误导性提示。
- **解码失败要单独处理。** 后端口径变了，`DecodingError` 的原始信息对用户毫无意义。
- **`LocalizedError` + `errorDescription`** 让 `error.localizedDescription` 直接拿来显示，不用到处 `switch`。

### 取消与超时

`.task` 帮你取消，但**被取消的任务不会自动停止正在执行的 `URLSession` 请求**——它需要你配合。好消息是 `URLSession` 的异步方法本身就响应 Swift 并发取消：任务一取消，请求会被中断并抛出 `CancellationError` 或 `URLError(.cancelled)`。

想在界面上正确应对，只要记住一条：**区分"被取消"和"真失败"**。

```swift
import SwiftUI

struct CancelAware: View {
    @State private var state = "空"

    var body: some View {
        Text(state)
            .task {
                do {
                    state = try await slowThing()
                } catch is CancellationError {
                    // 被取消不是错误，界面保持原样，不要弹"加载失败"
                } catch {
                    state = "失败：\(error.localizedDescription)"
                }
            }
    }

    func slowThing() async throws -> String {
        try await Task.sleep(for: .seconds(5))
        return "结果"
    }
}

// 界面效果：页面停留 5 秒后显示"结果"；
// 如果中途离开，任务被取消，再回来重新计时，且全程不显示错误
```

至于"超时"，有两种做法。用 `URLRequest.timeoutInterval` 最简单（上面已经写了）；要点是"整个操作必须在 X 秒内结束"（比如一次并发请求的整体预算），就用任务组自己造：

```swift
import Foundation

/// 超时专用的错误类型，方便调用方精准捕获
struct TimeoutError: Error { }

func withTimeout<T: Sendable>(
    seconds: Double,
    operation: @escaping @Sendable () async throws -> T
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask { try await operation() }
        group.addTask {
            try await Task.sleep(for: .seconds(seconds))
            throw TimeoutError()
        }
        // 谁先完成就用谁，剩下的全部取消
        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}

func verySlow() async throws -> String {
    try await Task.sleep(for: .seconds(3))
    return "终于好了"
}

do {
    print(try await withTimeout(seconds: 0.3) { try await verySlow() })
} catch is TimeoutError {
    print("超时：0.3 秒内没拿到结果")
    // prints: 超时：0.3 秒内没拿到结果
} catch {
    print("其它错误：\(error)")
}
```

用一个自定义的 `TimeoutError` 而不是借用 `URLError(.timedOut)`，好处是调用方能精确区分"我等超时了"和"网络自己报错了"——后者往往需要给用户完全不同的提示。

⚠️ 注意 `group.next()!` 在那里是安全的（任务组里至少有一个子任务，一定会返回或抛错），但这个 `withTimeout` 有个取舍：被取消的那个操作**不一定立刻停下**，它只是失去了返回值。对 `URLSession` 这种尊重取消的 API 没问题，对纯 CPU 循环就要自己在循环里查 `Task.isCancelled`。

## 46.6 从网络到界面：把零件接起来

```swift
import SwiftUI
import Foundation

struct Article: Identifiable, Decodable, Hashable {
    let id: Int
    let title: String
}

enum LoadState<Value> {
    case idle, loading
    case loaded(Value)
    case failed(String)
}

@Observable
final class ArticleFeedModel {
    var state: LoadState<[Article]> = .idle
    private var session = URLSession.shared

    func load(query: String) async {
        if case .loaded = state {} else { state = .loading }
        do {
            let items = try await fetchArticles(matching: query, session: session)
            state = .loaded(items)
        } catch is CancellationError {
            // 取消：不动界面
        } catch {
            state = .failed(error.localizedDescription)
        }
    }

    private func fetchArticles(matching query: String, session: URLSession) async throws -> [Article] {
        guard var components = URLComponents(string: "https://example.com/api/articles") else {
            throw URLError(.badURL)
        }
        components.queryItems = query.isEmpty ? nil : [URLQueryItem(name: "q", value: query)]
        let (data, response) = try await session.data(from: components.url!)
        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode([Article].self, from: data)
    }
}

struct ArticleFeedView: View {
    @State private var model = ArticleFeedModel()
    @State private var query = ""

    var body: some View {
        NavigationStack {
            Group {
                switch model.state {
                case .idle, .loading: ProgressView()
                case .loaded(let items): List(items) { Text($0.title) }
                case .failed(let message): Text(message).foregroundStyle(.red)
                }
            }
            .navigationTitle("文章")
            .searchable(text: $query)
            .task(id: query) {
                do { try await Task.sleep(for: .milliseconds(300)) } catch { return }
                await model.load(query: query)
            }
        }
    }
}

// 界面效果：标题栏下是搜索框；输入关键词停顿后列表刷新；
// 网络失败时显示一行红字说明
```

这个结构值得当成模板背下来：

- **模型持有 `LoadState`**，负责请求与错误翻译；
- **视图只 `switch` 状态**，一行网络代码都不写；
- **`.task(id: query)` 负责触发与取消**，去抖也在这一层。

三者职责不重叠，所以任何一处要改（换缓存策略、改去抖时长、加"空结果"界面）都不会牵动另外两处。

## 46.7 `AsyncImage`：三行显示远程图片

```swift
import SwiftUI

struct RemoteAvatar: View {
    let url: URL?

    var body: some View {
        AsyncImage(url: url) { phase in
            switch phase {
            case .empty:
                ProgressView()
            case .success(let image):
                image.resizable().scaledToFill()
            case .failure:
                Image(systemName: "person.crop.circle.badge.exclamationmark")
                    .foregroundStyle(.secondary)
            @unknown default:
                EmptyView()
            }
        }
        .frame(width: 64, height: 64)
        .clipShape(Circle())
    }
}

// 界面效果：一个圆形头像位；加载中显示转圈，
// 成功后显示图片，失败显示带感叹号的人像图标
```

`AsyncImage` 的优缺点都很鲜明：**它不缓存**（每次出现都会重新下载），也不能配请求头。需求简单时用它省事；生产项目里通常自己写一个带缓存的小组件，把 `URLSession` 换成带 `URLCache` 的配置即可。

## 46.8 本章小结

| 概念 | 一句话 |
| --- | --- |
| `.task` | 视图生命周期内的异步工作，视图消失自动取消 |
| `.task(id:)` | 依赖值变化时自动取消旧的、启动新的 |
| 去抖技巧 | `.task(id:)` + `Task.sleep` + `catch { return }` |
| 三态建模 | `enum LoadState` 让非法组合无法表达 |
| `async let` | 固定数量的并发请求，输出顺序能证明并发 |
| 任务组 | 动态数量的并发；结果按完成顺序返回 |
| `URLRequest` | 加超时、请求头、缓存策略；`data(for:)` 才有它 |
| 状态码检查 | `data(for:)` 对 4xx/5xx 不抛错，必须自己判断 |
| 取消 | `catch is CancellationError` 要和真失败分开处理 |
| 超时 | `timeoutInterval` 管单次请求；整体预算用任务组自己实现 |
| `AsyncImage` | 最省事的远程图片，但无缓存、不能配请求头 |

## 46.9 本章易错点速查

| 容易踩的地方 | 正确认识 |
| --- | --- |
| 用 `onAppear { Task { ... } }` | 任务与视图无隶属，会泄漏；用 `.task` |
| 在 `.task` 里直接改 `@State` 却担心线程 | `.task` 继承 `MainActor` 隔离，直接改是安全的 |
| 忘记处理取消 | 用户快速切页会看到"加载失败"闪一下；先 `catch is CancellationError` |
| 用 `data(for:)` 却以为 404 会抛错 | 不会；必须检查 `HTTPURLResponse.statusCode` |
| 把解码错误直接显示给用户 | `DecodingError` 的信息没有用户价值，要翻译 |
| 用三个可选/布尔表示加载状态 | 非法组合可表达；换 `enum LoadState` |
| 串行 `await` 多个请求 | 互不依赖就用 `async let` 或任务组并发 |
| 以为任务组按提交顺序返回 | 按完成顺序；要稳定顺序就自己排 |
| 把整个页面塞进 `AsyncImage` | 它不缓存；头像之类的小图才适合 |
| 在每个 `.task` 里都写一遍去抖 | 抽成一个小工具函数或模型方法 |

## 46.10 下章预告

到这里，一个功能完整、数据真实、动画得体的 App 已经能写出来了。最后一章处理"能不能交付"的问题：`#Preview` 怎么写才有用、SwiftUI 代码怎么测、可访问性为什么不是可选项，以及打包上架前值得过一遍的清单。
