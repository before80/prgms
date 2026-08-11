+++
title = "7.2 中毒（Poisoning）"
date = 2026-08-06T17:08:00+08:00
weight = 37
type = "docs"
description = "锁中毒等策略"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 中毒（Poisoning）


> 原文链接: [https://doc.rust-lang.org/nomicon/poisoning.html](https://doc.rust-lang.org/nomicon/poisoning.html)


　　尽管所有 unsafe 代码*必须*保证最低限度的异常安全，但并非所有类型都保证*最大*异常安全。即使类型本身保证了，你的代码也可能赋予它额外语义。例如，整数当然具备异常安全，但本身没有语义；panic 的代码可能未能正确更新该整数，导致程序状态不一致。

　　这*通常*没问题，因为任何目睹异常的对象即将被销毁。例如，若你把 `Vec` 发送到另一线程而该线程 panic，`Vec` 处于奇怪状态也无关紧要——它会被 drop 并永远消失。然而有些类型特别擅长把值偷运过 panic 边界。

　　这些类型可以选择在目睹 panic 时显式*中毒*（poison）自身。中毒并不特指某种具体行为，一般只是阻止正常使用继续。最著名的例子是标准库的 `Mutex` 类型：若某个 `MutexGuard`（加锁时返回的对象）在 panic 期间被 drop，`Mutex` 会自我中毒。此后任何尝试加锁该 `Mutex` 的操作都会返回 `Err` 或 panic。

　　`Mutex` 的中毒并非 Rust 通常意义上的真正安全。它是一种安全护栏，防止盲目使用在已加锁时目睹 panic 的 `Mutex` 中取出的数据。此类 `Mutex` 中的数据很可能正处于修改中途，因此可能处于不一致或不完整状态。需注意，若实现正确，无法用此类类型违反内存安全——它至少必须满足最低异常安全！

　　然而，若 `Mutex` 中包含的 `BinaryHeap` 实际上并不满足堆性质，任何使用它的代码都不太可能符合作者意图。因此程序不应正常继续。不过，若你*非常*确定仍能对值*做点什么*，`Mutex` 也提供了无论如何获取锁的方法——毕竟*是*安全的，只是可能毫无意义。
