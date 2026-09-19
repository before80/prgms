+++
title = "第30章 并发（一）：async/await、Task 与结构化并发"
weight = 300
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十章：并发（一）：`async/await`、`Task` 与结构化并发

> 异步不是“多开几个线程”这么简单，而是让程序在等待网络、磁盘或计时器时，能去做别的事。Swift 用 `async/await` 把这种等待写进代码结构，又用结构化并发保证子任务不会像断线风筝一样失控。

## 30.1 `async` 与 `await`

异步函数在参数列表后写 `async`，调用它要写 `await`：

```swift
func fetchName() async -> String {
    "Nova"
}

@main
struct App {
    static func main() async {
        print(await fetchName())
        // prints: Nova
    }
}
```

`await` 是一个可能的暂停点。函数暂停时不会阻塞线程，等结果准备好后再继续。暂停不代表“换了一条线程”，也不代表一定并发执行。

> 本章及后面两章的并发示例都用 `@main` 作为入口。它必须放进 SwiftPM 可执行目标的源文件里运行（原因见 3.6）；拿单个 `.swift` 文件当脚本跑，会报 `'main' attribute cannot be used in a module that contains top-level code`。想快速验证，也可以把 `@main struct App { ... }` 换成顶层 `let name = await fetchName()` 这种写法。

会抛错的异步函数写 `async throws`：

```swift
enum LoadError: Error { case empty }

func load(_ text: String) async throws -> Int {
    guard !text.isEmpty else { throw LoadError.empty }
    return text.count
}
```

## 30.2 `async let`：并行等待多个独立结果

几个互不依赖的异步任务，用 `async let` 同时开工，再一起收结果：

```swift
func fetchUser() async throws -> String {
    try await Task.sleep(for: .milliseconds(10))
    return "Mia"
}

func fetchScore() async throws -> Int {
    try await Task.sleep(for: .milliseconds(10))
    return 95
}

@main
struct App {
    static func main() async throws {
        async let user = fetchUser()
        async let score = fetchScore()
        let result = try await (user, score)
        print(result.0, result.1)
        // prints: Mia 95
    }
}
```

两个子任务先启动，随后在 `tuple` 处一起等待。不要为了并行而并行：只有任务彼此独立时，`async let` 才有价值。

先花两句话把 `Task.sleep(for: .milliseconds(10))` 拆开，因为这套写法后面会反复出现：

- `Task.sleep` 是"睡一会儿"，它**会抛错**——任务在这期间被取消就抛 `CancellationError`，所以前面必须写 `try`。
- `for:` 接收的是 `Duration`，Swift 5.7 起标准库自带的"时长"类型。`.milliseconds(10)` 是隐式成员写法（第 15B.13 节），完整写法是 `Duration.milliseconds(10)`。

```swift
let pause: Duration = .milliseconds(10)
print(pause + .seconds(1), type(of: pause))
// prints: 1.01 seconds Duration

try await Task.sleep(nanoseconds: 10_000_000)   // 老写法：10 毫秒，要自己数零
print("醒了")
// prints: 醒了
```

老 API 用纳秒整数，`10_000_000` 到底是 10 毫秒还是 100 毫秒得数一遍；`Duration` 版本把单位写在明面上，还能直接相加相乘——这就是它值得多打几个字的原因。

## 30.3 `Task`：从同步世界进入异步世界

同步函数不能直接写 `await`，可以创建任务：

```swift
@main
struct App {
    static func main() async {
        let task = Task { await fetchName() }
        print(await task.value)
        // prints: Nova
    }
}
```

`Task { ... }` 继承当前上下文的一部分（例如 actor 隔离），适合从同步入口启动异步工作。`Task.detached { ... }` 完全不继承当前上下文，通常只在底层库或明确需要独立任务时使用。

```swift
let detached = Task.detached { 21 * 2 }
print(await detached.value)
// prints: 42
```

## 30.4 任务取消：协作式，不是强杀

任务取消是协作式的。调用 `cancel()` 只是设置取消标记，任务内部必须检查：

```swift
let task = Task { () throws -> String in
    try Task.checkCancellation()
    return "完成"
}

task.cancel()
print(task.isCancelled)
// prints: true
```

`Task.checkCancellation()` 在已取消时抛出 `CancellationError`。长时间运行的循环也可以主动检查：

```swift
func countUp() async throws {
    for value in 0..<100 {
        try Task.checkCancellation()
        if value == 3 { print("到达 3") }
    }
}
```

取消不是"立刻死亡"，它是沿着任务树传递的一个标记，所以取消后的等待通常以 `CancellationError` 的形式被你接住：

```swift
let sleeper = Task {
    try await Task.sleep(for: .seconds(10))
}
sleeper.cancel()
do {
    try await sleeper.value
} catch {
    print(error is CancellationError)
    // prints: true
}
```

这里也解释了 `Task.cancel()` 为什么不需要 `try`：它只负责**请求**取消，把标记挂上去；什么时候响应，由被取消的任务在下一个暂停点或检查点自己决定。

取消会沿着结构化任务树向下传播。父任务取消时，子任务也会被标记为取消，但子任务仍然需要在自己的暂停点或检查点响应。

## 30.5 任务组：动态数量的结构化并发

`withTaskGroup` 适合运行时才知道要启动多少个子任务：

```swift
@main
struct App {
    static func main() async {
        let total = await withTaskGroup(of: Int.self, returning: Int.self) { group in
            for value in [1, 2, 3, 4] {
                group.addTask { value }
            }

            var sum = 0
            for await value in group {
                sum += value
            }
            return sum
        }

        print(total)
        // prints: 10
    }
}
```

任务组会等待所有子任务结束，并把结果按完成顺序交回来。需要抛出错误时使用 `withThrowingTaskGroup`；抛错后，尚未完成的任务会被取消。

两个关键动作记住就够了：`group.addTask { ... }` 往组里塞一个子任务，**闭包的返回值就是它的结果类型**；`for await value in group` 按"谁先完成谁先回来"的顺序取结果。

```swift
enum FetchError: Error { case negative }

func sum(_ numbers: [Int]) async throws -> Int {
    try await withThrowingTaskGroup(of: Int.self) { group in
        for n in numbers {
            group.addTask {
                guard n >= 0 else { throw FetchError.negative }
                return n
            }
        }
        var total = 0
        for try await value in group { total += value }
        return total
    }
}

print(try await sum([1, 2, 3]))
// prints: 6
do {
    _ = try await sum([1, -2])
    print("不该走到这里")
} catch {
    print("抛错了：\(error)")
}
// prints: 抛错了：negative
```

两个细节：闭合大括号里的 `try`（`try await withThrowingTaskGroup`）和循环里的 `for try await` 都省不掉——错误要么在这里被抛出，要么在更外层被接住；一旦有子任务抛错，任务组会自动取消其余还没跑完的子任务，这就是"结构化"的含义。

## 30.6 优先级与任务局部值

任务有优先级提示：

```swift
let urgent = Task(priority: .userInitiated) {
    "重要但不要靠它解决一切"
}
print(await urgent.value)
// prints: 重要但不要靠它解决一切
```

优先级是调度建议，不是抢占式保证。不要用它替代正确的依赖管理。

任务局部值可以像环境变量一样沿着异步调用链传递：

```swift
enum RequestContext {
    @TaskLocal static var requestID = "none"
}

@main
struct App {
    static func main() async {
        RequestContext.$requestID.withValue("abc") {
            print(RequestContext.requestID)
            // prints: abc
        }
    }
}
```

它比全局变量安全，因为值是绑定在当前任务链上的。

## 30.7 续体：桥接回调和 async/await

老 API 使用回调时，可以用 `withCheckedContinuation` 包装：

```swift
func legacyValue() async -> Int {
    await withCheckedContinuation { continuation in
        continuation.resume(returning: 42)
    }
}

@main
struct App {
    static func main() async {
        print(await legacyValue())
        // prints: 42
    }
}
```

会失败的回调用 `withCheckedThrowingContinuation`。每个续体必须且只能恢复一次；恢复两次会触发运行时错误，永不恢复则调用者永远等下去。

```swift
enum FetchError: Error { case negative }

func legacyDouble(_ value: Int, completion: @escaping (Result<Int, Error>) -> Void) {
    completion(value >= 0 ? .success(value * 2) : .failure(FetchError.negative))
}

func double(_ value: Int) async throws -> Int {
    try await withCheckedThrowingContinuation { continuation in
        legacyDouble(value) { result in
            continuation.resume(with: result)     // 一次且只一次
        }
    }
}

print(try await double(21))
// prints: 42
```

`resume(with:)` 接收一个 `Result`，成功就返回值、失败就抛出里面的错误——这正是把回调世界和 `async` 世界接起来最省力的写法。

## 30.8 本章小结

| 工具 | 作用 |
| --- | --- |
| `async` / `await` | 标记并等待异步操作 |
| `async let` | 并行启动固定数量的子任务 |
| `Task` | 从同步上下文启动异步任务 |
| `Task.detached` | 不继承上下文的独立任务 |
| `cancel()` | 请求取消，任务需协作响应 |
| 任务组 | 动态启动、等待并收集子任务 |
| 任务优先级 | 调度提示，不是绝对保证 |
| 续体 | 把回调 API 桥接成 async/await |

## 30.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 以为 `await` 一定会切换线程 | 它只表示可能暂停，执行位置由隔离规则决定 |
| 并发执行所有任务 | 只有独立工作才值得并发 |
| 调用 `cancel()` 后立刻认为任务已停止 | 取消需要任务内部协作响应 |
| 在任务组里泄漏子任务 | 结构化任务组会等待全部子任务 |
| 滥用 `Task.detached` | 它不继承上下文，常导致隔离和优先级问题 |
| 续体恢复多次或从不恢复 | 会导致崩溃或永久等待 |

## 30.10 下章预告

下一章进入隔离域和 actor。你会知道为什么多个任务同时改一块状态会出问题，也会知道 `Sendable`、`@MainActor`、`AsyncSequence` 如何把数据竞争挡在编译期。
