+++
title = "第28章 循环引用：weak、unowned 与闭包捕获"
weight = 280
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十八章：循环引用：`weak`、`unowned` 与闭包捕获

> 两个对象互相拉着对方的手，谁都不肯先走，内存就会一直涨。这不是玄学，而是 ARC 的必然结果。解决循环引用的工具只有几个，但每个都有明确的使用条件，弄清楚之后再也不会“看到 self 就加 weak”。

## 28.1 强引用环的形成

两个对象互相强引用，就变成了“你不走我也不走”。

```swift
final class Person {
    var apartment: Apartment?
    deinit { print("Person 释放") }
}

final class Apartment {
    var tenant: Person?
    deinit { print("Apartment 释放") }
}

do {
    let person = Person()
    let apartment = Apartment()
    person.apartment = apartment
    apartment.tenant = person
}
// 这一段跑完什么都不打印：两个 deinit 都没有被触发
```

`person` 持有 `apartment`，`apartment` 也持有 `person`。离开作用域后，外部引用消失了，但两者仍互相强引用，引用计数都不为零，所以 `deinit` 从未执行。

## 28.2 `weak`：自动变 `nil` 的引用

把其中一边改成 `weak`：

```swift
final class Person {
    var apartment: Apartment?
    deinit { print("Person 释放") }
}

final class Apartment {
    weak var tenant: Person?
    deinit { print("Apartment 释放") }
}

do {
    let person = Person()
    let apartment = Apartment()
    person.apartment = apartment
    apartment.tenant = person
}
// prints: Person 释放
// prints: Apartment 释放
```

释放顺序可能因实现和上下文略有不同，但两个对象都能被释放。

`weak` 的规则：

- 只能用于类实例。
- 必须是 `var`。
- 类型必须是可选值，因为对象释放后引用自动变成 `nil`。

弱引用不会增加引用计数。它适合“我的存在不决定对方是否存在的”关系，例如委托、父节点指向子节点、观察者。

## 28.3 委托模式：弱引用最经典的舞台

委托（delegate）是弱引用最正经的用武之地：协议要求“遵循者是类”，持有方用 `weak` 存它，于是被委托的对象不会因为“被持有”而活不下来。

```swift
protocol DownloadDelegate: AnyObject {
    func didFinish()
}

final class Downloader {
    weak var delegate: DownloadDelegate?

    func finish() {
        delegate?.didFinish()
    }
}

final class ViewController: DownloadDelegate {
    func didFinish() { print("UI 更新") }
}

let vc = ViewController()
let downloader = Downloader()
downloader.delegate = vc
downloader.finish()
// prints: UI 更新
```

委托通常不应该由下载器强持有，否则下载器死了、委托还在拉它，或者反过来形成环。`weak` 让这种关系自然单向。

## 28.4 `unowned`：确定对方不会先走

`unowned` 也不增加引用计数，但它不是可选值。对象释放后再访问会触发运行时错误：

```swift
final class Owner {
    var pet: Pet?
    deinit { print("Owner 释放") }
}

final class Pet {
    unowned let owner: Owner
    init(owner: Owner) { self.owner = owner }
    deinit { print("Pet 释放") }
}

do {
    let owner = Owner()
    let pet = Pet(owner: owner)
    owner.pet = pet
}
// prints: Owner 释放
// prints: Pet 释放
```

这里 `Pet` 的生命周期不可能长于 `Owner`，因此可以使用 `unowned`。如果这个前提不成立，就应该用 `weak`。

还要注意：`Owner` 的 `deinit` 执行时，`Pet` 可能还短暂存在。因此不要在需要访问 `owner` 的清理逻辑使用这种写法；一旦生命周期关系没有那么确定，`weak` 更安全。

> 选择规则：可能为 `nil` 用 `weak`；逻辑上永远有值且确定生命周期用 `unowned`；不确定就回到 `weak`。

## 28.5 闭包捕获强引用

闭包会捕获它用到的 `self`：

```swift
final class TimerLike {
    var count = 0
    var handler: (() -> Void)?

    func start() {
        handler = {
            self.count += 1
            print(self.count)
        }
    }

    deinit { print("TimerLike 释放") }
}

do {
    let timer = TimerLike()
    timer.start()
    timer.handler?()
}
// prints: 1
// 这里故意不打印释放，因为 timer 自己持有 handler，handler 又持有 timer
```

对象持有闭包，闭包又持有对象，循环就出现了。解决方式是捕获列表：

```swift
final class TimerLike {
    var count = 0
    var handler: (() -> Void)?

    func start() {
        handler = { [weak self] in
            guard let self else { return }
            self.count += 1
            print(self.count)
        }
    }

    deinit { print("TimerLike 释放") }
}

do {
    let timer = TimerLike()
    timer.start()
    timer.handler?()
}
// prints: 1
// prints: TimerLike 释放
```

`[weak self]` 让闭包不增加对象的引用计数。进入闭包后立刻 `guard let self`，后续代码可以像普通强引用一样写。

如果闭包和对象生命周期完全绑定，也可以写 `[unowned self]`。但一旦对象先释放，`unowned` 访问会崩溃，所以除非关系非常明确，优先 `weak`。

## 28.6 异步任务里的 `self`

异步闭包同样可能长期持有对象：

```swift
final class Loader {
    var value = 0

    func load() {
        Task { [weak self] in
            guard let self else { return }
            self.value = 42
            print(self.value)
        }
    }
}
```

并发章节会继续讨论任务生命周期。这里的规则不变：只要闭包被保存或被任务持有，就要检查它是否强引用了 `self`。

## 28.7 本章小结

| 引用方式 | 是否增加计数 | 类型要求 | 适用场景 |
| --- | --- | --- | --- |
| 强引用 | 是 | 任意 | 默认所有权 |
| `weak` | 否 | 类、可选值、`var` | 可能先释放的关系、委托 |
| `unowned` | 否 | 类、非可选 | 生命周期确定且不会先释放 |
| 捕获列表 | 控制闭包捕获 | 任意闭包 | 打破闭包与对象之间的环 |

## 28.8 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 看到 `self` 就加 `weak` | 只有存在环或生命周期不确定时才有必要 |
| 用 `weak` 修饰非可选属性 | 必须可选且是 `var` |
| 把 `unowned` 当默认选择 | 对象先释放会触发崩溃 |
| 闭包捕获 `self` 后忘记捕获列表 | 可能导致对象永远无法释放 |
| 捕获列表里写 `[weak self]` 后直接访问属性 | 必须先解包 `self` |
| 认为循环引用只会出现在两个对象之间 | 对象—闭包—对象也是经典环路 |

## 28.9 下章预告

下一章从内存安全进入所有权：独占访问、`borrowing`、`consuming`、不可复制类型和不可逃逸类型。它们是 Swift 6 系列中变化最快、也最能体现语言方向的部分。
