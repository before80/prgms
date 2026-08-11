+++
title = "2 术语表"
date = 2026-08-11T11:30:00+08:00
weight = 577
type = "docs"
description = "02-术语表 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/glossary.html](https://google.github.io/comprehensive-rust/glossary.html)

# 2 术语表

以下术语表旨在简要定义众多 Rust 术语。对于译文，它也有助于将术语与英文原文对应起来。

<style>
h1#glossary ~ ul {
    list-style: none;
    padding-inline-start: 0;
}

h1#glossary ~ ul > li {
    /* Simplify with "text-indent: 2em hanging" when supported:
       https://caniuse.com/mdn-css_properties_text-indent_hanging */
    padding-left: 2em;
    text-indent: -2em;
}

h1#glossary ~ ul > li:first-line {
    font-weight: bold;
}
</style>

- allocate:\
  在[堆](memory-management/review.md)上进行动态内存分配。
- array:\
  固定大小、元素类型相同、在内存中连续存储的集合。见[数组](tuples-and-arrays/arrays.md)。
- associated type:\
  与特定 trait 关联的类型，用于定义类型之间的关系。
- Bare-metal Rust:\
  底层 Rust 开发，常部署到无操作系统的系统。见[Bare-metal Rust](bare-metal.md)。
- block:\
  见[块](control-flow-basics/blocks-and-scopes.md)与 _scope_（作用域）。
- borrow:\
  见[借用](borrowing/shared.md)。
- borrow checker:\
  检查所有[借用](borrowing/borrowck.md)是否有效的 Rust 编译器组件。
- brace:\
  `{` 与 `}`，也称 _curly brace_（花括号），用于界定[_块_](control-flow-basics/blocks-and-scopes.md)。
- channel:\
  用于在[线程](concurrency/channels.md)之间安全传递消息。
- concurrency:\
  同时执行多个任务或进程。见[Rust 并发欢迎页](concurrency/welcome.md)。
- constant:\
  程序执行期间不改变的值。见[const](user-defined-types/const.md)。
- control flow:\
  程序中各语句或指令的执行顺序。见[控制流基础](control-flow-basics.md)。
- crash:\
  程序意外且未处理的失败或终止。见[panic](error-handling/panics.md)。
- enumeration:\
  保存若干命名常量之一的数据类型，可能带有关联元组或结构体。见[enum](user-defined-types/enums.md)。
- error:\
  偏离预期行为的意外条件或结果。见[错误处理](error-handling.md)。
- error handling:\
  管理并响应程序执行期间发生[错误](error-handling.md)的过程。
- function:\
  执行特定任务的可复用代码块。见[函数](control-flow-basics/functions.md)。
- garbage collector:\
  自动释放不再使用的对象所占内存的机制。见[内存管理方式](memory-management/approaches.md)。
- generics:\
  允许用类型占位符编写代码、从而在不同数据类型间复用的特性。见[泛型](generics.md)。
- immutable:\
  创建后不可更改。见[变量](types-and-values/variables.md)。
- integration test:\
  验证系统不同部分或组件之间交互的测试类型。见[其他测试类型](testing/other.md)。
- library:\
  程序可调用的预编译例程或代码集合。见[模块](modules.md)。
- macro:\
  Rust [宏](control-flow-basics/macros.md) 名称中常有 `!`。当普通函数不够用时使用宏。典型例子是 `format!`，它接受可变数量的参数，而 Rust 函数不支持这一点。
- `main` function:\
  Rust 程序从 [`main` 函数](types-and-values/hello-world.md) 开始执行。
- match:\
  Rust 的控制流构造，允许对表达式值进行[模式匹配](pattern-matching.md)。
- memory leak:\
  程序未能释放不再需要的内存，导致内存使用逐渐增长。见[内存管理方式](memory-management/approaches.md)。
- method:\
  与 Rust 中对象或类型关联的函数。见[方法](methods-and-traits/methods.md)。
- module:\
  包含函数、类型或 trait 等定义以组织代码的命名空间。见[模块](modules.md)。
- move:\
  Rust 中将值的所有权从一个变量转移到另一个变量。见[移动语义](memory-management/move.md)。
- mutable:\
  Rust 中允许[变量](types-and-values/variables.md)在声明后被修改的属性。
- ownership:\
  Rust 中定义代码哪一部分负责管理与值关联的内存的概念。见[所有权](memory-management/ownership.md)。
- panic:\
  Rust 中导致程序终止的不可恢复错误条件。见[Panics](error-handling/panics.md)。
- pattern:\
  可在 Rust 中与表达式匹配的值、字面量或结构组合。见[模式匹配](pattern-matching.md)。
- payload:\
  消息、事件或数据结构所携带的数据或信息。
- receiver:\
  Rust [方法](methods-and-traits/methods.md) 的第一个参数，表示调用该方法的对象实例。
- reference:\
  指向值的非拥有指针，借用而不转移所有权。引用可以是[共享（不可变）](references/shared.md)或[独占（可变）](references/exclusive.md)。
- reference counting:\
  跟踪对象引用数量、并在计数归零时释放对象的内存管理技术。见[Rc](smart-pointers/rc.md)。
- Rust:\
  注重安全、性能与并发的系统编程语言。见[什么是 Rust？](hello-world/what-is-rust.md)。
- safe:\
  指遵守 Rust 所有权与借用规则、从而避免内存相关错误的代码。见[Unsafe Rust](unsafe-rust.md)。
- slice:\
  对连续序列（如数组或 vector）的动态大小视图。与数组不同，slice 的大小在运行时确定。见[切片](references/slices.md)。
- scope:\
  变量有效且可用的程序区域。见[块与作用域](control-flow-basics/blocks-and-scopes.md)。
- standard library:\
  提供 Rust 基本功能的模块集合。见[标准库](std-types/std.md)。
- static:\
  Rust 中用于定义静态变量或具有 `'static` 生命周期项的关键字。见[static](user-defined-types/static.md)。
- string:\
  存储文本数据的数据类型。见[字符串](references/strings.md)。
- struct:\
  Rust 中将不同类型变量组合在同一名字下的复合数据类型。见[结构体](user-defined-types/named-structs.md)。
- test:\
  测试其他代码正确性的函数。Rust 有内置测试运行器。见[测试](testing.md)。
- thread:\
  程序中独立的执行序列，允许并发执行。见[线程](concurrency/threads.md)。
- thread safety:\
  确保程序在多线程环境中行为正确的属性。见[Send 与 Sync](concurrency/send-sync.md)。
- trait:\
  为未知类型定义的方法集合，提供 Rust 中实现多态的方式。见[Trait](methods-and-traits/traits.md)。
- trait bound:\
  要求类型实现你关心的某些 trait 的抽象。见[Trait 约束](generics/trait-bounds.md)。
- tuple:\
  包含不同类型变量的复合数据类型。元组字段无名称，通过序号访问。见[元组](tuples-and-arrays/tuples.md)。
- type:\
  指定 Rust 中某类值可执行哪些操作的分类。见[类型与值](types-and-values.md)。
- type inference:\
  Rust 编译器推断变量或表达式类型的能力。见[类型推断](types-and-values/inference.md)。
- undefined behavior:\
  Rust 中没有指定结果的行为或条件，常导致不可预测的程序行为。见[Unsafe Rust](unsafe-rust.md)。
- union:\
  可保存不同类型值但同一时刻仅保存其一的数据类型。见[联合体](unsafe-rust/unions.md)。
- unit test:\
  Rust 内置支持运行小型单元测试与较大集成测试。见[单元测试](testing/unit-tests.md)。
- unit type:\
  不持有数据的类型，写作无成员的元组。见[函数](control-flow-basics/functions.html)一节的讲师备注。
- unsafe:\
  Rust 中允许触发_未定义行为_的子集。见[Unsafe Rust](unsafe-rust/unsafe.md)。
- variable:\
  存储数据的内存位置。变量在 _scope_（作用域）内有效。见[变量](types-and-values/variables.md)。
