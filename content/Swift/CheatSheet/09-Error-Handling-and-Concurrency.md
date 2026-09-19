+++
title = "09 错误处理与并发"
linkTitle = "09 错误与并发"
weight = 90
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "throws / try / Result 与 async / await / actor / Sendable 的完整速查"
isCJKLanguage = true
draft = false
+++

# 09 错误处理与并发

## 错误处理

Swift 用 `throws` 表示"这个函数可能失败"，用 `try` 表示"我知道它可能失败"。这比异常好查，比返回码好读。

```swift
enum ParseError: Error, Equatable {
    case empty
    case invalid(String)
}

struct Line {
    let x: Double, y: Double

    static func parse(_ text: String) throws -> Line {
        let parts = text.split(separator: ",")
        guard parts.count == 2 else { throw ParseError.invalid(text) }
        guard let x = Double(parts[0]), let y = Double(parts[1]) else {
            throw ParseError.invalid(text)
        }
        return Line(x: x, y: y)
    }
}

do {
    let line = try Line.parse("3,4")
    print(line.x + line.y)
} catch ParseError.empty {
    print("输入为空")
} catch let ParseError.invalid(text) {
    print("格式错误：\(text)")
} catch {
    print("其他错误：\(error)")
}
// prints: 7.0
```

### 五个关键字

| 关键字 | 含义 |
| --- | --- |
| `throws` | 函数声明可能抛错；错误类型默认是 `any Error` |
| `try` | 调用抛错函数时必须写，是给别人看的标记 |
| `try?` | 失败就变成 `nil`，**吞掉错误详情** |
| `try!` | 失败就崩溃，只在测试或绝对不可能失败时用 |
| `rethrows` | 只有闭包参数抛错时我才抛错 |

```swift
func throwing() throws -> Int { 1 }

print((try? throwing()) as Any)
// prints: Optional(1)
print(try! throwing())
// prints: 1

// rethrows：只有当传进来的闭包会抛错时，这个函数才算会抛错
func run(_ body: () throws -> Void) rethrows { try body() }

try run { print(try throwing()) }
// prints: 1
```

### `catch` 的四种抓法

`catch` 和 `case` 一样，能接各种模式。四种写法解决的问题分别是"是不是这一类""是不是这个 case""当成值拿来用""再加个条件"：

| 写法 | 抓什么 | 拿到手的是什么 |
| --- | --- | --- |
| `catch { }` | 什么都抓 | `error`（`any Error`） |
| `catch is MyError { }` | 只抓某一类 | 什么都不给，纯粹筛类型 |
| `catch MyError.timeout(let s) { }` | 精确到一个 case | 关联值 `s` |
| `catch let e as MyError { }` | 某一类 + 绑定 | 已转型的 `e` |
| `catch let e where 条件 { }` | 带条件的筛选 | `e` |

```swift
enum NetError: Error { case timeout(Int), refused }

func run(_ n: Int) throws {
    if n == 1 { throw NetError.timeout(30) }
    if n == 2 { throw NetError.refused }
}

for n in 1...3 {
    do {
        try run(n)
        print("n=\(n) 成功")
    } catch is NetError {                       // 只判类型
        print("n=\(n) 是网络错误")
    } catch {
        print("其他")
    }
}
// prints:
//   n=1 是网络错误
//   n=2 是网络错误
//   n=3 成功

do { try run(1) } catch NetError.timeout(let s) { print("超时 \(s) 秒") }
// prints: 超时 30 秒

do { try run(2) } catch let e as NetError { print("当成值拿到:", e) }
// prints: 当成值拿到: refused

do { try run(1) } catch let e where e is NetError { print("带 where:", e) }
// prints: 带 where: timeout(30)
```

🔥 `catch is MyError` 是最省事的一种：不用起名字，也不想用这个错误，只想把它和别的错误分开处理。

### defer：收尾清理

```swift
func cleanup() {
    defer { print("清理") }
    print("主体")
}
cleanup()
// prints: 主体
//         清理
```

⚠️ `defer` 的清理代码在**离开作用域**时执行，包括通过 `throws` 抛出的路径，但不包括 `fatalError` 和进程被杀。

### 类型化抛出 🆕

Swift 6 允许声明具体的错误类型，于是 `catch` 必须穷尽——和 `switch` 一样的待遇：

```swift
enum NetError: Error { case timeout, refused }

func ping() throws(NetError) -> Int { throw .timeout }

do {
    _ = try ping()
} catch .timeout {
    print("超时")
} catch .refused {
    print("被拒绝")
}
// prints: 超时
```

🔥 类型化抛出把"这个函数到底会抛什么"写进了签名，调用方不用再靠猜或者 `switch error as? ...`。库的边界上值得用，内部小函数上写 `throws` 就够了。

### Result：把错误当值

需要把成功或失败**存起来、传出去、放进数组**时，用 `Result`：

```swift
// 承接上文：enum ParseError 已定义
func parse(_ text: String) throws -> Int {
    guard let value = Int(text) else { throw ParseError.invalid(text) }
    return value
}

let ok: Result<Int, any Error> = Result { try parse("42") }
switch ok {
case .success(let v): print("成功 \(v)")
case .failure(let e): print("失败 \(e)")
}
// prints: 成功 42

let bad = Result { try parse("x") }
print((try? bad.get()) as Any)
// prints: nil
```

⚠️ `Result(catching:)` 对**类型化抛出**很挑：闭包抛出的类型必须与 `Failure` **完全一致**，否则报 `invalid conversion of thrown error type 'any Error' to 'ParseError'`。注意这里比的是签名上的类型，不是"实际会抛什么"——上面那个 `parse` 只写 `throws` 时，它的错误类型就是 `any Error`，光给闭包加 `throws(ParseError)` 标注救不回来（报 `thrown expression type 'any Error' cannot be converted to error type 'ParseError'`）。

两条路都行得通：让被调函数本身也类型化抛出，或者把 `Failure` 放回 `any Error`：

```swift
// 承接上文：enum ParseError、func parse(_:) throws -> Int 都已定义
func parseTyped(_ text: String) throws(ParseError) -> Int {
    guard let value = Int(text) else { throw ParseError.invalid(text) }
    return value
}

// 路一：函数与闭包的抛出类型都写成 ParseError
let typed: Result<Int, ParseError> = Result(catching: { () throws(ParseError) -> Int in
    try parseTyped("42")
})
print(typed)
// prints: success(42)

// 路二：被调函数只写 throws，那 Failure 就用 any Error
let loose: Result<Int, any Error> = Result { try parse("42") }
print(loose)
// prints: success(42)
```

### 给用户看的错误信息

同一件事——"读一个文件，可能失败"——三种风格各有适用场景：

{{< tabpane text=true persist=disabled >}}

{{% tab header="throws（最常用）" %}}

```swift
enum FileError: Error { case missing(String) }

func read(_ path: String) throws -> String {
    guard path.hasSuffix(".txt") else { throw FileError.missing(path) }
    return "内容"
}

do {
    print(try read("a.txt"))
} catch {
    print("失败：\(error)")
}
// prints: 内容
```

适合"调用方必须处理、处理不了就继续往上抛"的场景。🔥

{{% /tab %}}

{{% tab header="Result（把错误当值）" %}}

```swift
enum FileError: Error { case missing(String) }

func read(_ path: String) -> Result<String, FileError> {
    path.hasSuffix(".txt") ? .success("内容") : .failure(.missing(path))
}

let results = ["a.txt", "b.md"].map(read)
print(results.map { (try? $0.get()) ?? "—" })
// prints: ["内容", "—"]
```

适合"要收集一批结果、要存进数组、要稍后再处理"的场景。

{{% /tab %}}

{{% tab header="typed throws（签名说清楚）" %}}

```swift
enum FileError: Error { case missing(String) }

func read(_ path: String) throws(FileError) -> String {
    guard path.hasSuffix(".txt") else { throw .missing(path) }
    return "内容"
}

do {
    print(try read("a.md"))
} catch .missing(let path) {
    print("找不到 \(path)")
}
// prints: 找不到 a.md
```

适合库的公开边界：调用方不用猜会抛什么，`catch` 还必须穷尽。

{{% /tab %}}

{{< /tabpane >}}

`Error` 的 `localizedDescription` 默认只说"操作无法完成"。要实现 `LocalizedError` 才有像样的话术：

```swift
// 承接上文：enum ParseError 已定义
import Foundation

extension ParseError: LocalizedError {
    var errorDescription: String? {
        switch self {
        case .empty:               "输入为空"
        case .invalid(let text):   "无法解析：\(text)"
        }
    }
}

print(ParseError.invalid("abc").errorDescription ?? "")
// prints: 无法解析：abc
```

### Never：一个值都没有的类型

`Never` 是标准库里一个**空类型**——它一个值都不存在。凡是"函数保证不会正常返回"，返回值就写 `Never`：

```swift
enum MyError: Error { case bad }

func fail(_ msg: String) -> Never {   // 永远不返回
    fatalError(msg)
}

func parse(_ s: String) throws -> Int {
    guard let n = Int(s) else { throw MyError.bad }
    return n
}
```

它真正好用的地方是**给编译器递话**。`Result<Int, Never>` 表示"这个操作要么成功、要么根本不该有失败分支"，于是 `switch` 里只写 `.success` 就穷尽了——不需要 `default`：

```swift
let alwaysOK: Result<Int, Never> = Result { 1 + 1 }
print(alwaysOK)
// prints: success(2)

func describe<T>(_ r: Result<T, Never>) -> T {
    switch r {
    case .success(let v): return v      // failure 分支不存在，不写也不报错
    }
}
print(describe(alwaysOK))
// prints: 2
```

| 场景 | 写法 |
| --- | --- |
| 一定崩 | `fatalError()`、`preconditionFailure()` 返回 `Never`，所以能放在 `guard` 的 `else` 里 |
| 一定不返回 | 自己写 `-> Never` 的函数，也能放在 `guard` 的 `else` 里 |
| 不会失败的结果 | `Result<T, Never>`，用 `switch` 时省掉 `default` |
| 空的 `switch` | 对 `Never` 类型的值做 `switch`，一个 `case` 都不用写 |

⚠️ `Never` 不是"错误类型"，别把 `-> Never` 当成"会抛错"的意思。它表达的是"这条路径压根回不来"，`fatalError` 之外的进程退出函数也是这个类型。

## 并发的三条主线

Swift 6 的并发模型只有三个概念，理解了就能读懂 90% 的报错：

| 概念 | 解决的问题 |
| --- | --- |
| `async` / `await` | 不阻塞线程地等待 |
| `actor` / `@MainActor` | 保护可变共享状态 |
| `Sendable` | 标记"能安全跨线程传"的类型 |

### async / await

异步函数用 `async` 标记，调用处用 `await`：

```swift
func fetchValue(_ id: Int) async -> Int {
    try? await Task.sleep(for: .milliseconds(10))
    return id * 10
}

print(await fetchValue(3))
// prints: 30
```

`await` 的意思是"这里可能挂起，让出线程去干别的"，**不是**"开一个新线程"。Swift 的并发跑在协作式线程池上，任务数量可以远多于线程数。

⚠️ 只有 `async` 函数里才能 `await`。想在同步代码里进入异步世界，用 `Task { }`。

#### `try`、`await`、`async let` 的排列顺序

这几样经常挤在同一行，顺序是定死的：**`try` 在前，`await` 在后**。

```swift
func risky(_ n: Int) async throws -> Int { n * 2 }

func use() async throws {
    do {
        print(try await risky(1))
    } catch { print("失败") }

    print((try? await risky(2)) ?? 0)

    async let a = risky(3)          // 声明时不用写 try
    print(try await a)              // 取值时才 try await

    let stream = AsyncThrowingStream<Int, any Error> { c in
        c.yield(1); c.yield(2); c.finish()
    }
    var sum = 0
    for try await v in stream { sum += v }
    print(sum)
}
try await use()
// prints:
//   2
//   4
//   6
//   3
```

| 写法 | 结果 |
| --- | --- |
| `try await f()` | ✅ 标准顺序 |
| `try? await f()` / `try! await f()` | ✅ |
| `await try f()` | ⚠️ 实测只给警告：`'try' must precede 'await'` |
| `async let x = f()` | ✅ 声明处不写 `try`，取值处写 `try await x` |
| `for try await x in seq` | ✅ 同样 `try` 在前 |

⚠️ 和 `??` 一起用时还有一个更隐蔽的坑：**`try?` 的作用范围比你想的大**。

```swift
func f() throws -> Int { 1 }

print(try? f() ?? 0, type(of: try? f() ?? 0))
// prints: Optional(1) Optional<Int>
print((try? f()) ?? 0, type(of: (try? f()) ?? 0))
// prints: 1 Int
```

`try? f() ?? 0` 会被解析成 `try? (f() ?? 0)`：`??` 先跟 `f()` 结合，于是右边那个 `0` 永远用不上（编译器会警告 `left side of nil coalescing operator '??' has non-optional type 'Int'`），整个表达式的类型也仍然是 `Int?`。想表达"失败了就用 0"，必须自己补一对括号。

### 并发执行：async let 与任务组

```swift
// 承接上文：func fetchValue(_:) async -> Int 已定义
func parallel() async -> [Int] {
    async let a = fetchValue(1)
    async let b = fetchValue(2)
    return await [a, b]
}
print(await parallel())
// prints: [10, 20]

func groupSum() async -> Int {
    await withTaskGroup(of: Int.self) { group in
        for i in 1...3 {
            group.addTask { await fetchValue(i) }
        }
        var total = 0
        for await value in group { total += value }
        return total
    }
}
print(await groupSum())
// prints: 60
```

| 工具 | 什么时候用 |
| --- | --- |
| `await f()` | 顺序执行，一步等一步 |
| `async let` | 固定数量、互不依赖的并行任务 🔥 |
| `withTaskGroup` | 数量不定、结果要收集 |
| `withThrowingTaskGroup` | 同上，但子任务会抛错 |
| `Task { }` | 从同步代码里启动异步工作 |
| `Task.detached { }` | 不继承当前上下文的任务，很少需要 🝖 |

⚠️ `async let` 的值该 `await` 就要 `await`。漏掉时会收到一条 `initialization of immutable value 'a' was never used` 的警告——注意它**不是**说任务被取消：子任务照样跑完，只是离开作用域时才被隐式等待、结果直接丢掉。所以白费的只有那个结果，代价却照付。

### actor：保护可变状态

```swift
actor BankAccount {
    private(set) var balance: Int = 0
    func deposit(_ amount: Int) { balance += amount }
    nonisolated var describe: String { "一个银行账户" }
}

let account = BankAccount()
await account.deposit(100)
print(await account.balance, account.describe)
// prints: 100 一个银行账户
```

规则速记：

| 规则 | 说明 |
| --- | --- |
| 外部访问可变状态要 `await` | 编译器替你排队，不会真的同时改 |
| `nonisolated` | 明确声明"这个成员不碰内部状态"，可以同步访问 |
| actor 内部可以直接互调 | 不需要 `await`，因为已经在同一隔离域 |
| actor 是引用类型 | 传的是引用，不是拷贝 |
| 不要 `await` 一个 actor 的 `nonisolated` 方法 | 它不是异步的 |

💭 actor 不是"加了锁的类"。它保证的是**同一时刻只有一个任务在改它的状态**，代价是调用点变成异步的。能用值类型解决的问题，别用 actor。

### @MainActor：把你按回主线程

```swift
@MainActor
final class ViewModel {
    var count = 0
    func bump() { count += 1 }
}

func useViewModel() async {
    let vm = await ViewModel()
    await vm.bump()
    print(await vm.count)
}
await useViewModel()
// prints: 1
```

`@MainActor` 可以标在类型、属性、方法上。UI 相关的一切都该在主线程，标上它以后，在别的线程碰它会直接编译报错——这比等到线上崩溃友好得多。

### 执行器：`@concurrent` 与 `nonisolated(nonsending)` 🆕

`async` 函数不是"一定在别的线程上跑"，它跑在**某个执行器**上。跑谁的执行器，取决于函数怎么声明：

| 写法 | 跑在哪个执行器 |
| --- | --- |
| 普通同步函数 | 调用方当前所在的地方 |
| `@MainActor func f()` | 主 actor |
| `nonisolated func f() async` | 全局并发执行器（Swift 6 语言模式的默认行为） |
| `@concurrent func f() async` | **强制**全局并发执行器 🆕 |
| `nonisolated(nonsending) func f() async` | **强制**跟着调用方 🆕 |

后两把扳手是 Swift 6.2 加的，专门用来消掉"我到底会不会被切走"这个疑问：

```swift
@concurrent
func heavy() async -> Int {
    // 不管谁调用，都切到全局并发执行器：CPU 密集型活儿放这里
    (1...1000).reduce(0, +)
}

nonisolated(nonsending)
func cheap() async -> Int {
    // 跟着调用方走：从 @MainActor 调就在主 actor 上，省掉一次线程跳转
    42
}
```

实测方法：写一个探针函数，函数体里调用 `MainActor.assertIsolated()`（不在主 actor 上就当场崩），再从 `@MainActor` 函数里调用它。

- 标了 `nonisolated(nonsending)` 的探针**通过**——确实留在主 actor 上；
- 把同一个函数改成普通 `nonisolated`，或标 `@concurrent`，断言当场崩（进程退出码 133）。

⚠️ 默认值还会继续变：Swift 6.2 提供了 `NonisolatedNonsendingByDefault` 这个 upcoming feature，打开之后**普通 `nonisolated async` 函数也会跟着调用方**，想强制切走就必须写 `@concurrent`——实测加上 `-enable-upcoming-feature NonisolatedNonsendingByDefault` 后，上面那个会崩的普通 `nonisolated` 探针就通过了。所以新代码里把"想不想被切走"写明确，比依赖默认值稳。

### Sendable：能不能跨线程传

```swift
import Synchronization

struct Config: Sendable { var name: String }   // 值类型，自动满足

final class Named: Sendable { let id = 3 }     // 只读 class，显式声明即可

final class Cache: @unchecked Sendable {       // 有可变状态，由你自己保证安全
    private let mutex = Mutex<[String: Int]>([:])
    func set(_ key: String, _ value: Int) { mutex.withLock { $0[key] = value } }
    func get(_ key: String) -> Int? { mutex.withLock { $0[key] } }
}

let cache = Cache()
cache.set("a", 1)
print(cache.get("a") ?? -1)
// prints: 1
```

| 类型 | 是否 `Sendable` |
| --- | --- |
| `struct`，成员都是 `Sendable` | ✅ 自动推断 |
| `enum` | ✅ 自动推断 |
| `final class`，成员全是不变的 `let` | ⚠️ **不会**自动推断，要显式写 `: Sendable` |
| `class` 有可变存储属性 | ❌ 需要加锁 + `@unchecked Sendable` |
| 闭包 | 捕获的值都是 `Sendable` 时才算 |

⚠️ `@unchecked Sendable` 是**你向编译器作出的承诺**。加了这个标记却忘了加锁，编译器不会再替你检查——这也是为什么它和 `nonisolated(unsafe)` 一起，被归到"能合法写出数据竞争的少数几处"里。看到这两个词，就该有人去读一遍那段加锁代码。

```swift
nonisolated(unsafe) var globalCounter = 0   // 全局可变状态：隔离检查到此为止，安全性靠你自己
```

`nonisolated(unsafe)` 比 `@unchecked Sendable` 更直接：它把全局变量、静态属性的隔离检查整个关掉。它存在的意义是让老代码能一步一步搬进 Swift 6，不是给你省事的开关。

### Mutex：新式的手动加锁 🆕

```swift
import Synchronization

let counter = Mutex(0)
counter.withLock { $0 += 1 }
counter.withLock { $0 += 1 }
print(counter.withLock { $0 })
// prints: 2
```

`Mutex` 来自 Swift 6 的 `Synchronization` 模块，比 `NSLock` 更轻，而且和 `Sendable` 配合得更干净。它要求 macOS 15 / iOS 18 以上。🚧

### Atomic：连锁都不想加的时候 🆕

`Synchronization` 还带来了一组原子类型，适合"就一个整数计数"这种简单共享状态：

```swift
import Synchronization

let counter = Atomic<Int>(0)
counter.add(1, ordering: .relaxed)
print(counter.load(ordering: .relaxed))
// prints: 1

let swapped = counter.compareExchange(expected: 1, desired: 20, ordering: .relaxed)
print(swapped.exchanged, swapped.original, counter.load(ordering: .relaxed))
// prints: true 1 20
```

| 操作 | 写法 |
| --- | --- |
| 读 | `a.load(ordering: .relaxed)` |
| 写 | `a.store(10, ordering: .relaxed)` |
| 加 / 减 | `a.add(1, ordering:)`、`a.subtract(1, ordering:)` |
| 比较并交换 | `a.compareExchange(expected:desired:ordering:)` → `(exchanged:original:)` |
| 换一个新值、拿回旧值 | `a.exchange(5, ordering:)` → 旧值 |
| 只增不减 / 只取更大 | `a.max(9, ordering:)`、`a.min(3, ordering:)` → `(oldValue:newValue:)` |
| 位运算改 | `a.bitwiseOr(0b1010, ordering:)`、`bitwiseAnd`、`bitwiseXor` 🝖 |

⚠️ `Atomic` **没有** `withLock`（实测报 `value of type 'Atomic<Int>' has no member 'withLock'`）。它是"单个值上的原子操作"，不是"一段代码的锁"——要保护多行逻辑、多个变量，请用 `Mutex`。

⚠️ `ordering:` 是内存序，不是"随便挑一个"。日常计数用 `.relaxed` 就够；要靠这个变量**当发布信号**（"我改完这行，别人就该看到前面那些改动"）时，才需要 `.acquiring` / `.releasing` / `.acquiringAndReleasing` 这些更强的顺序。不确定就用 `Mutex`，它的 `withLock` 语义直白得多。🚧

### AsyncSequence：可以 await 的序列

```swift
let stream = AsyncStream<Int> { continuation in
    for i in 1...3 { continuation.yield(i) }
    continuation.finish()
}

var collected: [Int] = []
for await value in stream { collected.append(value) }
print(collected)
// prints: [1, 2, 3]
```

`AsyncStream` 是"把回调式 API 包成异步序列"的标准工具，处理通知、代理回调、socket 数据时特别顺手。

异步序列同样能接 `where` 过滤，和 `for-in` 一模一样；序列会抛错时，`try` 写在 `for` 后面：

```swift
let stream = AsyncStream<Int> { continuation in
    for i in 1...5 { continuation.yield(i) }
    continuation.finish()
}

var odds: [Int] = []
for await value in stream where value % 2 == 1 {   // 只要奇数
    odds.append(value)
}
print(odds)
// prints: [1, 3, 5]
```

| 写法 | 用在哪 |
| --- | --- |
| `for await x in seq` | 不抛错的异步序列 |
| `for try await x in seq` | 会抛错的异步序列（网络流、文件行读取） |
| `for await x in seq where 条件` | 边遍历边过滤 |

想在两个对象之间传递这条流（一个负责生产、一个负责消费）时，用 `makeStream()` 一次拿到"流 + 续写端"：

```swift
let (stream, continuation) = AsyncStream<Int>.makeStream()
continuation.yield(1)
continuation.yield(2)
continuation.finish()          // 不调它，for await 会一直等下去

var got: [Int] = []
for await v in stream { got.append(v) }
print(got)
// prints: [1, 2]
```

会失败的流用 `AsyncThrowingStream`，结束时把错误一起交出去：

```swift
enum Boom: Error { case go }

let (tstream, tcont) = AsyncThrowingStream<Int, Error>.makeStream()
tcont.yield(1)
tcont.finish(throwing: Boom.go)

do {
    var got: [Int] = []
    for try await v in tstream { got.append(v) }
    print(got)
} catch {
    print("流抛错了")
}
// prints: 流抛错了
```

| 需求 | 写法 |
| --- | --- |
| 不抛错的流 | `AsyncStream<Int> { continuation in ... }` 或 `AsyncStream<Int>.makeStream()` |
| 会抛错的流 | `AsyncThrowingStream<Int, Error>.makeStream()`、`finish(throwing:)` |
| 结束 | `continuation.finish()`；之后 `yield` 的值会被丢掉 |
| 限流 | `makeStream(bufferingPolicy: .bufferingNewest(10))` |
| 缓冲策略 | `.unbounded`（默认，不丢但吃内存）、`.bufferingNewest(n)`、`.bufferingOldest(n)` |

⚠️ `AsyncStream` 默认**无限缓冲**：生产者比消费者快多少，内存就涨多少。给通知、传感器这类"来得多、处理得慢"的数据源配上 `.bufferingNewest(n)`，比事后查内存曲线便宜得多。

### withCheckedContinuation：把回调式 API 接进 async

上一节是"多次回调"，这一节是"一次回调"。老 API 基本都是"干完了叫我"，想把它们变成 `await`，就用 continuation 接住那一次回调：

```swift
func loadValue(completion: @escaping @Sendable (Int) -> Void) {
    Task { completion(7) }        // 假装这是某个老 API 的异步回调
}

func loadValueAsync() async -> Int {
    await withCheckedContinuation { continuation in
        loadValue { value in
            continuation.resume(returning: value)     // 必须、且只能恢复一次
        }
    }
}

print(await loadValueAsync())
// prints: 7
```

| 工具 | 什么时候用 |
| --- | --- |
| `withCheckedContinuation` | 不会失败的回调 |
| `withCheckedThrowingContinuation` | 会失败的回调：`continuation.resume(with: result)` 或 `resume(throwing:)` |
| `withUnsafeContinuation` | 想省掉运行期检查，只在性能敏感且确定写对时用 🝖 |

⚠️ continuation **必须恰好恢复一次**。忘了恢复，任务就永远挂着（`await` 处再也不回来）；恢复两次，`Checked` 版本会当场抓你——实测报 `SWIFT TASK CONTINUATION MISUSE: twice() tried to resume its continuation more than once`。这正是它比 `Unsafe` 版本多花一点开销换来的保护。

### 任务与取消

```swift
let t = Task { () -> Int in
    try await Task.sleep(for: .milliseconds(5))
    return 7
}
print(try await t.value)
// prints: 7

t.cancel()
print(Task.isCancelled)
// prints: false     当前任务（顶层代码）没有被取消
```

| 做什么 | 怎么写 |
| --- | --- |
| 启动任务 | `Task { ... }` |
| 等结果 | `try await task.value` |
| 取消 | `task.cancel()`（只是**请求**取消） |
| 检查取消 | `Task.isCancelled`、`try Task.checkCancellation()` |
| 睡一会儿 | `try await Task.sleep(for: .seconds(1))` |
| 让出执行权 | `await Task.yield()`，别的任务有机会先跑 |
| 指定优先级 | `Task(priority: .high) { ... }`、`Task.currentPriority` |
| 取消一整组 | 任务组里的 `group.cancelAll()` |
| 回主线程 | `await MainActor.run { ... }` |

```swift
let hi = Task(priority: .high) { () -> String in
    "优先级 \(Task.currentPriority.rawValue)"
}
print(await hi.value)
// prints: 优先级 25

let ok = Task { () -> Int in
    await Task.yield()          // 主动让一步，别把执行器占死
    return 7
}
print(await ok.value)
// prints: 7

let slow = Task { () -> String in
    do {
        try await Task.sleep(for: .seconds(5))
        return "睡醒了"
    } catch {
        return "被取消：\(error is CancellationError)"
    }
}
slow.cancel()
print(await slow.value)
// prints: 被取消：true     cancel 会让正在 sleep 的任务立刻抛 CancellationError
```

⚠️ `Task.currentPriority.rawValue` 实测 `.high` 是 `25`，但这个数字是实现细节，别背：代码里认 `.high`、`.userInitiated`、`.background` 这些符号。

任务组的三种口味，按"要不要结果、会不会抛错"来选：

| 工具 | 要不要结果 | 会不会抛错 | 典型场景 |
| --- | --- | --- | --- |
| `withTaskGroup` | 要 | 否 | 固定格式的并行请求、并行计算 |
| `withThrowingTaskGroup` | 要 | 是 | 子任务可能失败，失败要整体收摊 |
| `withDiscardingTaskGroup` | **不要** | 是 | 长跑服务：每个连接起一个任务，跑完就扔 🆕 |

```swift
await withDiscardingTaskGroup { group in
    for i in 1...3 { group.addTask { _ = i * 2 } }   // 结果没人要，跑完就释放
}
print("组跑完")
// prints: 组跑完
```

💭 `withDiscardingTaskGroup` 的价值在内存：普通任务组会把每个子任务的结果**攒到组结束**才释放，长跑服务里这些结果会一直堆着；discarding 版本子任务一结束就把资源收掉。子任务的返回值必须是 `Void`，所以写法上就是"干活，不汇报"。

⚠️ **取消是协作式的。** `cancel()` 不会打断正在运行的代码，它只是设一个标志。你的循环要主动检查 `Task.isCancelled`，或者调用会抛 `CancellationError` 的 API。

`withTaskCancellationHandler` 就是给"取消那一刻"挂一个回调——比如把底层网络连接关掉：

```swift
func work() async {
    await withTaskCancellationHandler {
        try? await Task.sleep(for: .milliseconds(20))
        print("正常跑完")
    } onCancel: {
        print("收到取消请求，赶紧收尾")     // 在别的线程上立刻执行
    }
}
await work()
// prints: 正常跑完
```

💭 `onCancel` 里**不能** `await`，它要能立刻返回——真正需要等待的清理放到后面的正常流程里做。

### @TaskLocal：给任务打个"随行标签"

日志追踪里最常见的问题：十几个函数调用一层层传 `requestID`。`@TaskLocal` 让这个值跟着任务走，不用改任何函数签名：

```swift
enum Trace {
    @TaskLocal static var id: String = "无"
}

func handle() {
    print(Trace.id)                     // 作用域外是默认值
    Trace.$id.withValue("req-1") {
        print("内部:", Trace.id)         // 作用域内是被绑定的值
    }
    print("外部:", Trace.id)             // 出来又变回默认值
}
handle()
// prints:
//   无
//   内部: req-1
//   外部: 无
```

| 要点 | 说明 |
| --- | --- |
| 声明方式 | `@TaskLocal static var`，必须带默认值 |
| 绑定方式 | `Trace.$id.withValue(值) { ... }`，注意是 `$` 那个投影 |
| 生效范围 | 闭包内部，以及它 `await` 出去的所有子任务；出来自动还原 |
| 同步版本 | 闭包不异步时**不用写 `await`**（实测加了 `await` 反而会警告 `no 'async' operations occur within 'await' expression`） |
| 典型用途 | 请求 ID、租户 ID、日志上下文 🔥 |

### 自定义全局 actor：不止有 @MainActor

`@MainActor` 是标准库给的一个全局 actor，你也可以自己造一个，把"必须串行"的那部分逻辑圈起来：

```swift
@globalActor
actor StoreActor {
    static let shared = StoreActor()
}

@StoreActor
final class Store {
    private(set) var rows: [String] = []
    func add(_ row: String) { rows.append(row) }
}

func load() async {
    let store = Store()                 // 创建不需要 await
    await store.add("a")                // 碰隔离状态才要
    print(await store.rows)
}
await load()
// prints: ["a"]
```

⚠️ 定义里那几行是固定套路：`@globalActor` + 一个 `actor` + 一个 `static let shared` 单例。名字写成别的（比如 `static let instance`）就会报 `type 'StoreActor' does not conform to protocol 'GlobalActor'`（实测）。

### 与 GCD 的对照

老代码里到处是 `DispatchQueue`。两者不是替代关系，但新代码基本不需要 GCD：

| 旧写法（GCD） | 新写法（Swift 并发） |
| --- | --- |
| `DispatchQueue.global().async { }` | `Task { }` |
| `DispatchQueue.main.async { }` | `await MainActor.run { }` 或 `@MainActor` |
| `DispatchQueue.main.asyncAfter(deadline:)` | `try await Task.sleep(for: .seconds(1))` |
| `DispatchGroup` | `withTaskGroup` |
| `DispatchSemaphore` | 别用；阻塞线程会影响整个线程池 ⚠️ |
| `NSLock` | `Mutex`（Swift 6）或 `actor` |

⚠️ **绝对不要在 `async` 代码里用信号量或 `sync` 阻塞。** 线程池的线程数是有限的（通常等于 CPU 核数），阻塞几个线程就可能让整个并发系统卡死，这种死锁极难复现。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| `try?` 吞掉错误详情 | 排查问题时信息全丢，能 `do-catch` 就别偷懒 |
| `try!` 用在不可控输入上 | 崩溃的经典来源 |
| `catch` 顺序写错 | 具体类型要放在通用的 `catch` 之前 |
| `defer` 里抛错 | 错误出不去：`defer { try f() }` 报 `call can throw, but errors cannot be thrown out of a defer body`；要在里面调会抛错的函数，得用 `try?` 或自己 `do-catch` 收掉 |
| `Result(catching:)` 与类型化抛出 | 抛出类型必须与 `Failure` 严格一致 |
| 用 `Task { }` 忘记 `await` 结果 | 任务会照常执行，但错误被静默丢弃 |
| `async let` 漏掉 `await` | 只会收到 `never used` 警告，子任务照样跑完，丢的是结果不是计算 |
| 在 `async` 函数里阻塞线程 | 要等就 `try await Task.sleep(for:)`；`Thread.sleep(forTimeInterval:)`（Foundation）和信号量会把线程占住不放，拖垮线程池 |
| `@unchecked Sendable` 当免死金牌 | 它只是"我保证"，编译器不再检查 |
| 以为 `cancel()` 会立刻停下 | 取消是协作式的，需要自己检查 |
| 在同步函数里访问 `@MainActor` 属性 | 编译报错，要 `await` 或把函数标成 `@MainActor` |
