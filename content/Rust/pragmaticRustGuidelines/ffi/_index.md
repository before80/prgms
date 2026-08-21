+++
title = "第5章 FFI"
date = 2026-08-18T18:10:00+08:00
weight = 70
type = "docs"
description = "FFI 指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/ffi/index.html](https://microsoft.github.io/rust-guidelines/guidelines/ffi/index.html)

# FFI

## 在 FFI 库之间隔离 DLL 状态 (M-ISOLATE-DLL-STATE) {#M-ISOLATE-DLL-STATE}

*本条守护：跨 DLL 边界的数据完整性与已定义行为。*

在同一应用中加载多个基于 Rust 的动态库（DLL）时，这些库之间只能共享「可移植」状态。
同样，在编写此类库时，你必须只接受或提供来自外部 DLL 的「可移植」数据。

此处的可移植指无论来源如何都安全且一致可处理的数据。按定义，这是 FFI 安全类型的子集。
一个类型是可移植的，若它是 `#[repr(C)]`（或同样定义良好），并且满足下列_全部_条件：

- 不得与任何 `static` 或线程局部有任何交互。
- 不得与任何 `TypeId` 有任何交互。
- 不得包含指向任何非可移植数据的任何值、指针或引用（指向非可移植数据内部的可移植数据是合法的，例如
  共享对 `Box` 中所持 ASCII 字符串的引用）。

_交互_ 指任何计算关系，因此也与类型的用法有关。在 DLL 之间发送 `u128` 可以，用它交换经 transmute 的 `TypeId` 则不行。

根本问题在于：Rust 编译器把每个 DLL 都当作全新的编译产物，相当于独立应用。这意味着每个 DLL：

- 有自己的一套 `static` 与线程局部变量，
- 任何 `#[repr(Rust)]` 类型（默认）的类型布局可能因编译而异，
- 有自己的一套唯一类型 ID，与任何其他 DLL 都不同。

尤其会影响：

- ⚠️ 任何已分配实例，例如 `String`、`Vec<u8>`、`Box<Foo>`、...
- ⚠️ 任何依赖其他 static 的库，例如 `tokio`、`log`，
- ⚠️ 任何非 `#[repr(C)]` 的结构体，
- ⚠️ 任何依赖一致 `TypeId` 的数据结构。

实践中，在库之间传递上述任何内容都会导致数据丢失、状态损坏，通常还有未定义行为。

请特别注意，这也可能适用于在 FFI 边界上不可见的类型与方法：

```rust
/// DLL1 中想要使用 DLL2 公共服务的方法
#[ffi_function]
fn use_common_service(common: &CommonService) {
    // 这里至少有两个问题：
    // - `CommonService`，或其深处嵌套的任何类型，在
    //   DLL2 中可能有不同的类型布局，导致立即的
    //   未定义行为（UB）⚠️
    // - 这里的 `do_work()` 看起来会在 DLL2 中调用，但
    //   实际执行的代码却来自 DLL1。这意味着此处调用的
    //   `do_work()` 会看到来自 DLL2 的数据结构，却使用
    //   DLL1 的 static ⚠️
    common.do_work();
}
```

## 业务逻辑属于核心 crate，FFI 只做转译 (M-FFI-TRANSLATES) {#M-FFI-TRANSLATES}

*本条守护：尽可能多的安全代码，以及清晰的关注点分离。*

当用 Rust 创建 FFI 库时，核心_业务逻辑_ crate `foo` 与胶水 crate `foo-ffi` 之间应有清晰的关注点分离。

任何操作性功能都属于核心 crate，并以惯用、安全、可测试的 Rust 表达。FFI crate 的存在只为在原生 Rust 与 C 构造之间转译；核心 crate 不得被互操作关注点污染，即便这意味着重复并略微调整类型与函数签名。例如，给定核心 crate `foo` 中的如下类型：

```rust
pub struct Message {
    destination: [u8; 8],
    data: Vec<u8>,
}

impl Message {
    pub fn new(destination: [u8; 8], data: Vec<u8>) -> Self { /* ... */ }
    pub fn transmit(&self) -> Result<(), TransmitError> { /* ... */ }
}
```

恰当的关注点分离可能会在 `foo-ffi` 中把构造与传输折叠成单个 FFI 入口点：

```rust
#[no_mangle]
pub unsafe extern "C" fn transmit_message(
    destination: *const [u8; 8],
    data: *const u8,
    data_len: usize,
) -> u8 {
    let data = std::slice::from_raw_parts(data, data_len).to_vec();
    match Message::new(*destination, data).transmit() {
        Ok(()) => 0,
        Err(_) => 1,
    }
}
```

然而，把 FFI 要求泄漏进 `foo` 本身是不恰当的：所有权、数据模型与签名在两个世界之间无法无缝转译。因跳过干净拆分而「节省」的时间，在后续重构中往往要加倍偿还。

```rust
#[repr(C)]
pub struct Message {
    pub destination: [u8; 8],
    pub data_ptr: *mut u8,
    pub data_len: usize,
    pub data_cap: usize,
}
```

## FFI crate 遵循既有命名约定 (M-FFI-NAMING) {#M-FFI-NAMING}

*本条守护：跨项目一眼可识别的 crate 角色。*

用于 FFI 的 crate 应遵循既有命名实践：

- `-sys` 用于定义调用现有（C 风格）库的项的 crate
- `-ffi` 用于定义被现有应用调用时的（C 风格）项的 crate

该方案有轻微变体（例如先前的 `-sys` crate 被废弃时用 `-sys2`，以及用 `-` 还是 `_`），但总体而言 `-ffi` 明确表示「导出」库，`-sys` 表示「导入」库。
