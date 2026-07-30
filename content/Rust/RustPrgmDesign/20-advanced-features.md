+++
title = "20-高级特性"
date = 2026-07-28T14:49:00+08:00
weight = 200
type = "docs"
description = "unsafe Rust、高级 trait/类型、函数指针与宏等进阶特性精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第20章

# 高级特性

偶尔遇到、不必天天用；可作陌生语法时的查阅参考。

## 不安全 Rust

**unsafe Rust** 不强制部分内存安全保证，提供五种**超能力**（须在 `unsafe { }` 块或标记函数/trait 内使用）：

1. **解引用裸指针**：`*const T` / `*mut T`；可忽略借用规则、允许空指针、不保证有效内存。
2. **调用 unsafe 函数/方法**：C FFI、`slice::from_raw_parts_mut` 等。
3. **访问/修改可变静态变量**：`static mut`；多线程易数据竞争。
4. **实现 unsafe trait**：如手动为含裸指针的类型实现 `Send`/`Sync`。
5. **访问 `union` 字段**：与 C 互操作。

要点：

- `unsafe` **不关闭**借用检查；引用仍被检查。
- 尽量**封装**成安全抽象（如 `split_at_mut`）；`unsafe` 块越小越好。
- 裸指针：安全代码可**创建**，解引用须 `unsafe`；`&raw const/mut` 创建有效指针。
- **extern**：`unsafe extern "C" { fn abs(i: i32) -> i32; }` 调用外部代码；可用 `safe fn` 标记确实安全的 FFI 函数。
- 导出 Rust 给 C：`#[unsafe(no_mangle)] pub extern "C" fn ...`
- **Miri**（nightly）：运行时检测 UB；`cargo +nightly miri run/test`。

## 高级 trait

### 关联类型

trait 内占位类型，实现时指定一次。如 `Iterator::Item`。

- 泛型 trait 可多次 impl（如 `Iterator<String>`、`Iterator<u32>`）；关联类型**每类型只能 impl 一次**。

### 使用默认泛型类型参数和运算符重载

```rust
trait Add<Rhs = Self> {
    type Output;
    fn add(self, rhs: Rhs) -> Self::Output;
}
```

- 实现 `Add` 重载 `+`；可自定义 `Rhs`（如 `impl Add<Meters> for Millimeters`）。
- 默认类型参数：扩展 trait 不破坏现有代码；减少样板。

### 在同名方法之间消歧义

- 直接调用：类型自身方法优先。
- trait 方法：`Pilot::fly(&person)` 或 `<Type as Trait>::method(...)`。
- 关联函数（无 `self`）：须**完全限定语法** `<Dog as Animal>::baby_name()`。

### 使用超 trait

`trait OutlinePrint: Display { ... }`——实现子 trait 须先实现父 trait。

### 使用 newtype 模式在外部类型上实现外部 trait

- **孤儿规则**：trait 与类型至少一方须为本地。
- 元组结构体封装外部类型即可本地 impl 外部 trait；零运行时开销。
- 需全部方法时可 impl `Deref` 代理。

## 高级类型

### 使用 newtype 模式实现类型安全与抽象

- 防混用（单位类型 `Millimeters` vs `Meters`）。
- 隐藏实现（如 `People` 封装 `HashMap<i32, String>`）。

### 类型同义词与类型别名

```rust
type Kilometers = i32;   // 同义词，无新类型检查
type Thunk = Box<dyn Fn() + Send + 'static>;  // 缩短长类型
type Result<T> = std::result::Result<T, std::io::Error>;  // 固定 E
```

- 别名**不提供** newtype 的类型安全；主要用于可读性与 DRY。

### 从不返回的 never type

- **`!`**（never type）：无值；`panic!`、`loop {}`、`continue` 等发散表达式的类型。
- `!` 可**强制转换**为任意类型，使 `match` 各分支类型统一。

### 动态大小类型和 `Sized` trait

- **DST**：编译期大小未知，如 `str`、trait 对象。
- 不能 `let s: str`；须置于指针后：`&str`（ptr + len）、`Box<str>`、`&dyn Trait`。
- **`Sized`**：编译期大小已知；泛型隐式 `T: Sized`。
- 放宽：`fn generic<T: ?Sized>(t: &T)` 允许 DST 引用。

## 高级函数与闭包

### 函数指针

- 类型 `fn(i32) -> i32`（小写 `fn`），非 trait。
- 可传给期望闭包的函数（fn 实现 `Fn`/`FnMut`/`FnOnce`）。
- C 互操作、枚举构造函数作 `map` 参数常见。
- 完全限定：`String::to_string` 消除歧义。

### 返回闭包

- 闭包无具体类型，不能直接返回闭包类型。
- 单闭包：`impl Fn(...) -> ...`。
- 多闭包同签名：`Box<dyn Fn(...) -> ...>`（trait 对象）。

## 宏

### 宏和函数的区别

| | 宏 | 函数 |
|---|-----|------|
| 参数 | 可变数量 | 固定签名 |
| 执行时机 | **编译期**展开 | 运行时 |
| 能力 | 可为类型 impl trait | 不能 |
| 定义位置 | 调用前须可见 | 任意 |

### 用 `macro_rules!` 编写声明宏

- `#[macro_export]` 导出；`macro_rules! vec { ... }`。
- 模式匹配 **Rust 源码结构**（非值）；`$x:expr`、`$( ... ),*` 重复。
- 类似 `match`：`pattern => { 展开代码 }`。

### 过程宏

须独立 `proc-macro` crate；`TokenStream` 入/出。

| 类型 | 注解 | 用途 |
|------|------|------|
| 自定义 derive | `#[proc_macro_derive(HelloMacro)]` | `#[derive(...)]` 生成 impl |
| 类属性 | `#[proc_macro_attribute]` | 自定义属性（如 `#[route(GET, "/")]`） |
| 类函数 | `#[proc_macro]` | 像函数调用（如 `sql!(...)`） |

- 常用 `syn`（解析）+ `quote`（生成代码）；`stringify!` 编译期表达式转字符串。

## 总结

unsafe、高级 trait/类型、函数指针与宏覆盖 Rust 进阶角落；遇陌生语法时可回查本章。
