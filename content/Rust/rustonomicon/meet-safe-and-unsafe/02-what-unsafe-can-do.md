+++
title = "1.2 Unsafe 能做什么"
date = 2026-08-06T17:08:00+08:00
weight = 4
type = "docs"
description = "Unsafe Rust 相对 Safe Rust 多出的能力"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Unsafe 能做什么


> 原文链接: [https://doc.rust-lang.org/nomicon/what-unsafe-does.html](https://doc.rust-lang.org/nomicon/what-unsafe-does.html)


　　Unsafe Rust 与 Safe Rust 的唯一区别在于，你可以：

* 解引用裸指针
* 调用 `unsafe` 函数（包括 C 函数、编译器内建 intrinsic、原始分配器）
* 实现 `unsafe` trait
* 访问或修改可变静态变量
* 访问 `union` 的字段

　　就这些。这些操作被 relegated 到 Unsafe，是因为误用任意一项都会导致令人畏惧的未定义行为。触发未定义行为等于赋予编译器对你的程序为所欲为的权限。你*绝对不应*触发未定义行为。

　　与 C 不同，Rust 中未定义行为的范围相当有限。核心语言主要关心防止下列情况：

* 解引用（对指针使用 `*`）悬垂或未对齐的指针（见下文）
* 违反[指针别名规则][]
* 用错误的调用 ABI 调用函数，或从错误 unwind ABI 的函数中 unwind
* 造成[数据竞争][race]
* 执行当前执行线程不支持的 [target features][] 所编译的代码
* 产生无效值（单独或作为 `enum`/`struct`/数组/元组等复合类型的字段）：
  * `bool` 不是 0 或 1
  * `enum` 的判别式无效
  * `fn` 指针为 null
  * `char` 不在 [0x0, 0xD7FF] 与 [0xE000, 0x10FFFF] 范围内
  * `!`（该类型所有值均无效）
  * 从[未初始化内存][]读出的整数（`i*`/`u*`）、浮点（`f*`）或裸指针，或 `str` 中的未初始化内存
  * 悬垂、未对齐或指向无效值的引用/`Box`
  * 元数据无效的宽引用、`Box` 或裸指针：
    * 若 `dyn Trait` 的元数据不是指向与指针/引用实际动态 trait 匹配的 `Trait` vtable 的指针，则无效
    * 若 slice 长度不是有效 `usize`（即不得从未初始化内存读出），则 slice 元数据无效
  * 具有自定义无效值的类型取到其中之一，例如 null 的 [`NonNull`]（请求自定义无效值是不稳定特性，但 `NonNull` 等稳定 libstd 类型会用到）

　　关于「未定义行为」的更详细说明，见 [Reference][behavior-considered-undefined]。

　　「产生」值发生在赋值、传入函数/原语操作或从函数/原语操作返回值时。

　　若引用/指针为 null，或其指向的字节并非全部属于同一分配（因而必须属于*某*分配），则称该引用/指针「悬垂」。所指向的字节跨度由指针值与 pointee 类型大小决定。因此若跨度为空，「悬垂」与「null」相同。注意 slice 与字符串指向整个范围，故长度元数据绝不能过大（尤其分配及 slice/字符串不能大于 `isize::MAX` 字节）。若这太麻烦，可考虑裸指针。

　　就这些。这是 Rust 内建的未定义行为原因。当然，unsafe 函数与 trait 可声明程序必须维持的任意其他约束以避免未定义行为。例如分配器 API 声明对未分配内存 dealloc 是未定义行为。

　　不过，违反这些约束通常会 transitively 导致上述问题之一。另一些约束也可能来自编译器内建对代码如何优化的特殊假设。例如 `Vec` 与 `Box` 使用要求指针始终非 null 的内建。

　　Rust 对其他可疑操作 otherwise 相当宽松。Rust 认为下列行为「安全」：

* 死锁
* 存在[竞争条件][race]
* 内存泄漏
* 整数溢出（用 `+` 等内建运算符）
* abort 程序
* 删除生产数据库

　　更详细信息见 [Reference][behavior-not-considered-unsafe]。

　　然而，真正做出这些事的程序*很可能*不正确。Rust 提供大量工具使这些情况少见，但认为在范畴上防止它们不现实。

[pointer aliasing rules]: references.html
[uninitialized memory]: uninitialized.html
[race]: races.html
[target features]: ../reference/attributes/codegen.html#the-target_feature-attribute
[`NonNull`]: ../std/ptr/struct.NonNull.html
[behavior-considered-undefined]: ../reference/behavior-considered-undefined.html
[behavior-not-considered-unsafe]: ../reference/behavior-not-considered-unsafe.html
