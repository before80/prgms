+++
title = "第31章 并发（二）：隔离域、actor 与 Sendable"
weight = 310
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十一章：并发（二）：隔离域、`actor` 与 `Sendable`

> 并发真正困难的部分不是“同时跑”，而是“同时改”。多个任务一起修改同一份状态，结果可能比抽奖还不透明。Swift 用隔离域把可变状态关进单行道，用 `actor` 和 `Sendable` 在编译期抓住大多数数据竞争。

## 31.1 数据竞争从哪里来

两个任务同时执行下面的 `value += 1`，可能都先读到 0，再各自写回 1：

```swift
final class UnsafeCounter {
    var value = 0
}
```

最终结果可能少加一次，甚至出现更复杂的不一致。问题不在于“加法慢”，而在于读、改、写不是一个不可分割的操作。actor 的作用就是把这类访问串行化。

## 31.2 `actor`：受隔离保护的状态

`actor` 可以理解成“并发版的带锁对象”，只不过这把锁由编译器替你守着：外部只能通过 `await` 跟它说话，它内部的状态永远不会被两个任务同时改。

```swift
actor Counter {
    private var value = 0

    func increment() {
        value += 1
    }

    func current() -> Int {
        value
    }
}

@main
struct App {
    static func main() async {
        let counter = Counter()
        await counter.increment()
        print(await counter.current())
        // prints: 1
    }
}
```

actor 内部状态只能通过 actor 隔离的方法访问。外部调用要 `await`，因为调用可能等待 actor 空闲。actor 一次只执行一个隔离任务，从而避免并发写冲突。

## 31.3 `@MainActor`：UI 的主舞台

`@MainActor` 是全局 actor，常见于 UI 代码：

```swift
@MainActor
final class ViewModel {
    var title = "首页"

    func update() {
        title = "已更新"
        print(title)
        // prints: 已更新
    }
}

@main
struct App {
    @MainActor
    static func main() {
        ViewModel().update()
    }
}
```

标注 `@MainActor` 的类型或方法，其隔离状态只能在主 actor 上访问。从其他隔离域调用时要 `await`，编译器会检查你是否不小心跨域碰了状态。

## 31.4 `Sendable`：跨隔离域传递的安全凭证

`Sendable` 表示值可以安全地跨隔离域传递：

```swift
struct Snapshot: Sendable {
    let value: Int
}

func consume(_ snapshot: Snapshot) {
    print(snapshot.value)
    // prints: 10
}

consume(Snapshot(value: 10))
```

不可变的 `let` 值类型通常很容易满足 `Sendable`。可变类一般不满足，因为两个任务可能同时修改同一实例。类只有在内部状态完全受保护或不可变时，才可能安全地声明 `Sendable`。

```swift
final class ImmutableBox: Sendable {
    let value: Int
    init(value: Int) { self.value = value }
}
```

这两个条件——`final` 和「只有不可变存储」——都是硬性要求，少一个编译器都会拦下来：

```text
error: non-final class 'Box' cannot conform to the 'Sendable' protocol
error: stored property 'value' of 'Sendable'-conforming class 'Mutable' is mutable
```

第一条的含义是：子类可以加属性和重写，编译器无法保证它仍然安全，所以要求 `final`。第二条更直白：能改的状态就可能被两个任务同时改。

如果类内部真的靠锁或 actor 保护着可变状态，可以用 `@unchecked Sendable` 明确接手责任。这相当于对编译器说“我知道规矩，我来保证”——写成注释说明保护机制，是给未来读代码的人留的活路。

## 31.5 隔离检查失败的典型错误

从非隔离上下文直接访问 actor 状态会报错：

```text
error: actor-isolated property 'value' can not be referenced from a nonisolated context
```

解决方式不是到处写 `await`，而是想清楚：

- 这段代码应该属于哪个隔离域？
- 访问状态的方法是否应该标 `@MainActor` 或放进 actor？
- 传递的数据是否满足 `Sendable`？

隔离规则的目的不是增加麻烦，而是让数据竞争在编译期可见。

## 31.6 `isolated` 参数与 `nonisolated`

函数可以把某个参数声明为 `isolated`，表示调用期间获得该 actor 的隔离：

```swift
actor Counter {
    var value = 0
}

func update(on counter: isolated Counter) {
    counter.value += 1
}

@main
struct App {
    static func main() async {
        let counter = Counter()
        await update(on: counter)
        print(await counter.value)
        // prints: 1
    }
}
```

`nonisolated` 表示该方法不占用 actor 隔离。它适合纯计算、读取 `let` 属性或不接触隔离状态的逻辑：

```swift
actor Device {
    let name: String
    init(name: String) { self.name = name }

    nonisolated func displayName() -> String {
        name.uppercased()
    }
}
```

## 31.7 actor 是可重入的

actor 方法在 `await` 处会暂停，并允许其他任务进入同一个 actor：

```swift
actor Loader {
    var state = "idle"

    func load() async {
        state = "loading"
        await Task.sleep(for: .milliseconds(10))
        state = "loaded"
    }
}
```

在 `await` 之前和之后，`state` 可能已经被其他调用改变。不要在暂停点之间假设“状态没变”。如果一段逻辑必须保持原子性，就不要在其中插入 `await`，或者把关键步骤重新设计成状态机。

## 31.8 AsyncSequence 与 `for await`

异步序列逐个产生值，使用 `for await` 消费：

```swift
@main
struct App {
    static func main() async {
        let stream = AsyncStream<Int> { continuation in
            continuation.yield(1)
            continuation.yield(2)
            continuation.yield(3)
            continuation.finish()
        }

        for await value in stream {
            print(value)
        }
        // prints: 1
        // prints: 2
        // prints: 3
    }
}
```

`AsyncSequence` 适合事件流、文件分块、网络数据和实时更新。它和同步 `Sequence` 的最大区别是：获取下一个元素本身可能是异步的。

构造闭包递给你的那个 `continuation` 是流的"入口"：`yield(_:)` 往里塞一个元素，`finish()` 表示"不会再有新元素了"。`finish()` 不是可写可不写的装饰——漏掉它，上面的 `for await` 就会一直等下去。

> 还有一个更进阶的方向：`distributed actor`。它用于跨进程、跨节点的分布式系统，需要搭配 `Distributed` 模块和具体的分布式 actor 系统实现。日常单机并发不需要它，等真的要做集群通信时再进入这一层。

## 31.9 本章小结

| 概念 | 作用 |
| --- | --- |
| actor | 串行保护内部可变状态 |
| `@MainActor` | 主线程/主 actor 隔离，常用于 UI |
| `Sendable` | 跨隔离域安全传递 |
| `isolated` 参数 | 让函数在指定 actor 的隔离下运行 |
| `nonisolated` | 不进入 actor 隔离 |
| 可重入 | actor 在暂停点允许其他调用进入 |
| `AsyncSequence` | 异步产生值，用 `for await` 消费 |

## 31.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 用锁的思路理解 actor | actor 是隔离域，不是普通互斥锁 |
| 以为 actor 方法一定同步执行完 | 遇到 `await` 会暂停并可能重入 |
| 给可变类随意标 `Sendable` | 必须证明内部状态被安全保护 |
| 到处使用 `@unchecked Sendable` | 这是“我保证安全”的承诺，出错后果由你负责 |
| 在 actor 中假设状态跨 `await` 不变 | 可重入会让状态被其他调用修改 |
| 把 AsyncSequence 当同步数组 | 下一个元素可能需要异步等待 |

## 31.11 下章预告

最后一章并发内容讲迁移：Swift 6 的严格并发检查、Approachable Concurrency、默认 MainActor 隔离、`@concurrent` 与 `sending`。目标是让已有项目能一步步走向数据竞争安全。
