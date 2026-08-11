+++
title = "09-给嵌入式 C 开发者的提示"
date = 2026-08-01T10:38:00+08:00
weight = 137
type = "docs"
description = "给嵌入式 C 开发者的提示（Tips for embedded C developers）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 给嵌入式 C 开发者的提示 {#tips-for-embedded-c-developers}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/c-tips/](https://doc.rust-lang.org/stable/embedded-book/c-tips/)


本章汇总了一系列提示，可能对希望开始编写 Rust 的资深嵌入式 C 开发者有用。它会特别强调：你在 C 中已经习惯的做法，在 Rust 中有何不同。

## 预处理器 {#preprocessor}

在嵌入式 C 中，预处理器常用于多种目的，例如：

* 用 `#ifdef` 在编译期选择代码块
* 编译期数组大小与计算
* 用宏简化常见模式（以避免函数调用开销）

Rust 没有预处理器，因此许多此类用途会用其它方式解决。本节其余部分介绍预处理器的各种替代方案。

### 编译期代码选择 {#compile-time-code-selection}

在 Rust 中，与 `#ifdef ... #endif` 最接近的是 [Cargo features]。它们比 C 预处理器更规范：每个 crate 都会显式列出所有可能的 feature，且只能是开或关。当你把某个 crate 列为依赖时可以开启 feature，并且 feature 是可叠加的：只要依赖树中任意 crate 为另一个 crate 启用了某个 feature，该 feature 就会对该 crate 的所有用户生效。

[Cargo features]: https://doc.rust-lang.org/cargo/reference/manifest.html#the-features-section

例如，你可能有一个提供信号处理原语库的 crate。每个组件可能需要额外编译时间，或声明很大的常量表而你希望避免。你可以在 `Cargo.toml` 里为每个组件声明一个 Cargo feature：

```toml
[features]
FIR = []
IIR = []
```

然后在代码中用 `#[cfg(feature="FIR")]` 控制包含哪些内容。

```rust
/// 在顶层 lib.rs 中

#[cfg(feature="FIR")]
pub mod fir;

#[cfg(feature="IIR")]
pub mod iir;
```

同样，也可以仅在某个 feature *未*启用时包含代码块，或按任意 feature 组合是否启用来包含。

此外，Rust 还提供许多自动设置的条件，例如用 `target_arch` 按架构选择不同代码。有关条件编译支持的完整细节，请参阅 Rust 参考手册的 [条件编译] 章节。

[条件编译]: https://doc.rust-lang.org/reference/conditional-compilation.html

条件编译只作用于紧随其后的语句或代码块。若某个块在当前作用域中无法使用，则需要多次使用 `cfg` 属性。值得注意的是，多数情况下更好的做法是直接包含全部代码，让编译器在优化时删除死代码：这对你和用户都更简单，而且编译器通常能很好地去掉未使用的代码。

### 编译期大小与计算 {#compile-time-sizes-and-computation}

Rust 支持 `const fn`：保证可在编译期求值的函数，因此可用于需要常量的地方，例如数组大小。它可以与上文提到的 feature 一起使用，例如：

```rust
const fn array_size() -> usize {
    #[cfg(feature="use_more_ram")]
    { 1024 }
    #[cfg(not(feature="use_more_ram"))]
    { 128 }
}

static BUF: [u32; array_size()] = [0u32; array_size()];
```

这些功能自 Rust 1.31 起才进入稳定版，因此文档仍较稀疏。撰写本文时，`const fn` 可用的功能也非常有限；在未来的 Rust 版本中，预期会扩大 `const fn` 中允许的内容。

### 宏 {#macros}

Rust 提供极其强大的 [宏系统]。C 预处理器几乎直接作用于源代码文本，而 Rust 宏系统在更高层级上工作。Rust 宏有两种：*示例宏（macros by example）* 与 *过程宏（procedural macros）*。前者更简单且更常见；它们看起来像函数调用，可以展开为完整的表达式、语句、项或模式。过程宏更复杂，但能为 Rust 语言带来极强的扩展能力：它们可以把任意 Rust 语法变换成新的 Rust 语法。

[宏系统]: https://doc.rust-lang.org/book/ch19-06-macros.html

一般来说，凡是你可能使用过 C 预处理器宏的地方，多半可以看看示例宏能否胜任。它们可以在你的 crate 中定义，并轻松供本 crate 使用或导出给其他用户。请注意，由于它们必须展开为完整的表达式、语句、项或模式，C 预处理器宏的某些用法行不通，例如展开为变量名的一部分，或列表中不完整的一组项。

与 Cargo feature 一样，也值得考虑你是否真的需要宏。很多情况下普通函数更易理解，并且会内联成与宏相同的代码。`#[inline]` 与 `#[inline(always)]` [属性] 可进一步控制这一过程，但此处同样需要谨慎——编译器会在适当时自动内联同一 crate 中的函数，不当强制内联实际上可能导致性能下降。

[属性]: https://doc.rust-lang.org/reference/attributes.html#inline-attribute

完整解释 Rust 宏系统超出了本提示页的范围，建议查阅 Rust 文档以了解全部细节。

## 构建系统 {#build-system}

多数 Rust crate 使用 Cargo 构建（尽管并非必须）。它能处理传统构建系统中许多棘手问题。不过，你可能希望自定义构建过程。Cargo 为此提供了 [`build.rs` 脚本]。它们是可按需与 Cargo 构建系统交互的 Rust 脚本。

[`build.rs` 脚本]: https://doc.rust-lang.org/cargo/reference/build-scripts.html

构建脚本的常见用途包括：

* 提供构建期信息，例如将构建日期或 Git 提交哈希静态嵌入可执行文件
* 根据所选 feature 或其它逻辑在构建期生成链接脚本
* 更改 Cargo 构建配置
* 添加额外的静态库以供链接

目前尚不支持构建后脚本；传统上你可能用它自动从构建产物生成二进制文件，或打印构建信息。

### 交叉编译 {#cross-compiling}

使用 Cargo 作为构建系统也简化了交叉编译。多数情况下，只需告诉 Cargo `--target thumbv6m-none-eabi`，即可在 `target/thumbv6m-none-eabi/debug/myapp` 找到合适的可执行文件。

对于 Rust 原生不支持的平台，你需要自行为该目标构建 `libcore`。在这类平台上，可以用 [Xargo] 作为 Cargo 的替代，它会自动为你构建 `libcore`。

[Xargo]: https://github.com/japaric/xargo

## 迭代器与数组访问 {#iterators-vs-array-access}

在 C 中，你可能习惯按索引直接访问数组：

```c
int16_t arr[16];
int i;
for(i=0; i<sizeof(arr)/sizeof(arr[0]); i++) {
    process(arr[i]);
}
```

在 Rust 中这是反模式：按索引访问可能更慢（因为需要边界检查），并可能妨碍多种编译器优化。这一点很重要，值得重申：Rust 会对手动数组索引检查越界访问以保证内存安全，而 C 则会愉快地索引到数组之外。

请改用迭代器：

```rust,ignore
let arr = [0u16; 16];
for element in arr.iter() {
    process(*element);
}
```

迭代器提供了你在 C 中需要手动实现的强大功能，例如链式组合、zip、enumerate、求最小/最大值、求和等。迭代器方法也可以链式调用，从而写出非常易读的数据处理代码。

更多细节见 [《Rust 程序设计语言》中的迭代器] 与 [Iterator 文档]。

[《Rust 程序设计语言》中的迭代器]: https://doc.rust-lang.org/book/ch13-02-iterators.html
[Iterator 文档]: https://doc.rust-lang.org/core/iter/trait.Iterator.html

## 引用与指针 {#references-vs-pointers}

在 Rust 中，指针（称为 [_裸指针（raw pointers）_]）确实存在，但只在特定情况下使用，因为解引用它们始终被视为 `unsafe`——Rust 无法提供其通常对指针背后内容的保证。

[_裸指针（raw pointers）_]: https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html#dereferencing-a-raw-pointer

多数情况下，我们改用由 `&` 表示的 *引用（references）*，或由 `&mut` 表示的 *可变引用（mutable references）*。引用在行为上类似指针，可以解引用以访问底层值，但它们是 Rust 所有权系统的关键部分：Rust 会严格强制，在任意时刻对同一值只能有一个可变引用，*或者*多个不可变引用。

实践中这意味着你必须更仔细地考虑是否需要可变访问数据：在 C 中默认是可变的，你必须显式写 `const`；在 Rust 中则相反。

你可能仍会使用裸指针的一种情形是直接与硬件交互（例如，把缓冲区指针写入 DMA 外设寄存器）；此外，所有外设访问 crate 底层也使用它们，以便你读写内存映射寄存器。

## 易失访问 {#volatile-access}

在 C 中，个别变量可标记为 `volatile`，向编译器表明变量的值可能在两次访问之间发生变化。在嵌入式上下文中，易失变量常用于内存映射寄存器。

在 Rust 中，我们不是把变量标为 `volatile`，而是用特定方法执行易失访问：[`core::ptr::read_volatile`] 与 [`core::ptr::write_volatile`]。这些方法接受 `*const T` 或 `*mut T`（上文讨论的 *裸指针*），并执行易失读或写。

[`core::ptr::read_volatile`]: https://doc.rust-lang.org/core/ptr/fn.read_volatile.html
[`core::ptr::write_volatile`]: https://doc.rust-lang.org/core/ptr/fn.write_volatile.html

例如，在 C 中你可能这样写：

```c
volatile bool signalled = false;

void ISR() {
    // 发出中断已发生的信号
    signalled = true;
}

void driver() {
    while(true) {
        // 睡眠直到被信号唤醒
        while(!signalled) { WFI(); }
        // 复位信号指示
        signalled = false;
        // 执行等待该中断的某些任务
        run_task();
    }
}
```

在 Rust 中的等价写法会在每次访问时使用易失方法：

```rust,ignore
static mut SIGNALLED: bool = false;

#[interrupt]
fn ISR() {
    // 发出中断已发生的信号
    // （在真实代码中，应考虑更高层的原语，
    //  例如原子类型）。
    unsafe { core::ptr::write_volatile(&mut SIGNALLED, true) };
}

fn driver() {
    loop {
        // 睡眠直到被信号唤醒
        while unsafe { !core::ptr::read_volatile(&SIGNALLED) } {}
        // 复位信号指示
        unsafe { core::ptr::write_volatile(&mut SIGNALLED, false) };
        // 执行等待该中断的某些任务
        run_task();
    }
}
```

代码示例中有几点值得注意：
  * 我们可以把 `&mut SIGNALLED` 传给需要 `*mut T` 的函数，因为 `&mut T` 会自动转换为 `*mut T`（`*const T` 同理）
  * `read_volatile`/`write_volatile` 方法需要 `unsafe` 块，因为它们是 `unsafe` 函数。确保安全使用是程序员的责任：更多细节见这些方法的文档。

在你的代码中直接需要这些函数的情况很少见，因为更高层的库通常会替你处理。对于内存映射外设，外设访问 crate 会自动实现易失访问；而对于并发原语，则有更好的抽象可用（见 [并发章节]）。

[并发章节]: ../concurrency/

## 打包与对齐类型 {#packed-and-aligned-types}

在嵌入式 C 中，常告诉编译器某个变量必须有特定对齐，或某个结构体必须打包而非对齐，通常是为了满足特定硬件或协议要求。

在 Rust 中，这由结构体或联合体上的 `repr` 属性控制。默认表示不保证布局，因此不应用于与硬件或 C 互操作的代码。编译器可能重排结构体成员或插入填充，且行为可能随未来的 Rust 版本变化。

```rust
struct Foo {
    x: u16,
    y: u8,
    z: u16,
}

fn main() {
    let v = Foo { x: 0, y: 0, z: 0 };
    println!("{:p} {:p} {:p}", &v.x, &v.y, &v.z);
}

// 0x7ffecb3511d0 0x7ffecb3511d4 0x7ffecb3511d2
// 注意：为改善打包，顺序已变为 x, z, y。
```

为确保与 C 可互操作的布局，请使用 `repr(C)`：

```rust
#[repr(C)]
struct Foo {
    x: u16,
    y: u8,
    z: u16,
}

fn main() {
    let v = Foo { x: 0, y: 0, z: 0 };
    println!("{:p} {:p} {:p}", &v.x, &v.y, &v.z);
}

// 0x7fffd0d84c60 0x7fffd0d84c62 0x7fffd0d84c64
// 顺序得以保留，且布局不会随时间改变。
// `z` 按两字节对齐，因此 `y` 与 `z` 之间存在一字节填充。
```

为确保打包表示，请使用 `repr(packed)`：

```rust
#[repr(packed)]
struct Foo {
    x: u16,
    y: u8,
    z: u16,
}

fn main() {
    let v = Foo { x: 0, y: 0, z: 0 };
    // 引用必须始终对齐，因此为检查结构体字段的地址，
    // 我们使用 `std::ptr::addr_of!()` 获取裸指针，
    // 而不是直接打印 `&v.x`。
    let px = std::ptr::addr_of!(v.x);
    let py = std::ptr::addr_of!(v.y);
    let pz = std::ptr::addr_of!(v.z);
    println!("{:p} {:p} {:p}", px, py, pz);
}

// 0x7ffd33598490 0x7ffd33598492 0x7ffd33598493
// `y` 与 `z` 之间未插入填充，因此现在 `z` 未对齐。
```

注意，使用 `repr(packed)` 也会将该类型的对齐设为 `1`。

最后，要指定特定对齐，请使用 `repr(align(n))`，其中 `n` 是要对齐到的字节数（且必须是 2 的幂）：

```rust
#[repr(C)]
#[repr(align(4096))]
struct Foo {
    x: u16,
    y: u8,
    z: u16,
}

fn main() {
    let v = Foo { x: 0, y: 0, z: 0 };
    let u = Foo { x: 0, y: 0, z: 0 };
    println!("{:p} {:p} {:p}", &v.x, &v.y, &v.z);
    println!("{:p} {:p} {:p}", &u.x, &u.y, &u.z);
}

// 0x7ffec909a000 0x7ffec909a002 0x7ffec909a004
// 0x7ffec909b000 0x7ffec909b002 0x7ffec909b004
// 两个实例 `u` 与 `v` 被放在 4096 字节对齐上，
// 从其地址末尾的 `000` 可以看出。
```

注意我们可以把 `repr(C)` 与 `repr(align(n))` 组合，以获得对齐且与 C 兼容的布局。不允许把 `repr(align(n))` 与 `repr(packed)` 组合，因为 `repr(packed)` 将对齐设为 `1`。也不允许 `repr(packed)` 类型包含 `repr(align(n))` 类型。

有关类型布局的更多细节，请参阅 Rust 参考手册的 [类型布局] 章节。

[类型布局]: https://doc.rust-lang.org/reference/type-layout.html

## 其它资源 {#other-resources}

* 本书中：
    * [在 Rust 中使用一点 C](../interoperability/01-a-little-c-with-your-rust/)
    * [在 C 中使用一点 Rust](../interoperability/02-a-little-rust-with-your-c/)
* [Rust Embedded 常见问题](https://docs.rust-embedded.org/faq.html)
* [面向 C 程序员的 Rust 指针](http://blahg.josefsipek.net/?p=580)
* [我以前用指针——现在呢？](https://github.com/diwic/reffers-rs/blob/master/docs/Pointers.md)
