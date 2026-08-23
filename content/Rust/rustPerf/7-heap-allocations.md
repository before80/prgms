+++
title = "7 堆分配"
date = 2026-08-23T13:57:00+08:00
weight = 8
type = "docs"
description = "减少堆分配"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 堆分配 {#heap-allocations}


> 原文链接: [https://nnethercote.github.io/perf-book/heap-allocations.html](https://nnethercote.github.io/perf-book/heap-allocations.html)


堆分配的开销适中。确切细节取决于使用的分配器，但每次分配（和释放）通常涉及获取全局锁、进行一些非平凡的数据结构操作，并可能执行系统调用。小分配不一定比大分配便宜。值得了解哪些 Rust 数据结构和操作会导致分配，因为避免它们可以大幅改善性能。

[Rust 容器速查表][Rust Container Cheat Sheet] 提供了常见 Rust 类型的可视化，是以下各节的绝佳配套资料。

[Rust Container Cheat Sheet]: https://docs.google.com/presentation/d/1q-c7UAyrUlM-eZyTo1pd8SZ0qwA_wYxmPZVOQkoDmH4/

## 性能分析

如果通用分析器显示 `malloc`、`free` 及相关函数是热点，那么尝试降低分配速率和/或使用替代分配器可能值得。

[DHAT] 是降低分配速率时使用的出色分析器。适用于 Linux 和一些其他 Unix 系统。它精确识别热点分配点及其分配速率。确切结果会有所不同，但在 rustc 上的经验表明，每百万条执行指令减少 10 次分配可以带来可测量的性能改善（例如约 1%）。

[DHAT]: https://www.valgrind.org/docs/manual/dh-manual.html

以下是 DHAT 的一些示例输出。
```text
AP 1.1/25 (2 children) {
  Total:     54,533,440 bytes (4.02%, 2,714.28/Minstr) in 458,839 blocks (7.72%, 22.84/Minstr), avg size 118.85 bytes, avg lifetime 1,127,259,403.64 instrs (5.61% of program duration)
  At t-gmax: 0 bytes (0%) in 0 blocks (0%), avg size 0 bytes
  At t-end:  0 bytes (0%) in 0 blocks (0%), avg size 0 bytes
  Reads:     15,993,012 bytes (0.29%, 796.02/Minstr), 0.29/byte
  Writes:    20,974,752 bytes (1.03%, 1,043.97/Minstr), 0.38/byte
  Allocated at {
    #1: 0x95CACC9: alloc (alloc.rs:72)
    #2: 0x95CACC9: alloc (alloc.rs:148)
    #3: 0x95CACC9: reserve_internal<syntax::tokenstream::TokenStream,alloc::alloc::Global> (raw_vec.rs:669)
    #4: 0x95CACC9: reserve<syntax::tokenstream::TokenStream,alloc::alloc::Global> (raw_vec.rs:492)
    #5: 0x95CACC9: reserve<syntax::tokenstream::TokenStream> (vec.rs:460)
    #6: 0x95CACC9: push<syntax::tokenstream::TokenStream> (vec.rs:989)
    #7: 0x95CACC9: parse_token_trees_until_close_delim (tokentrees.rs:27)
    #8: 0x95CACC9: syntax::parse::lexer::tokentrees::<impl syntax::parse::lexer::StringReader<'a>>::parse_token_tree (tokentrees.rs:81)
  }
}
```
描述此示例中的所有内容超出了本书的范围，但应该清楚 DHAT 提供了关于分配的丰富信息，例如发生的位置和频率、大小、存活时间以及访问频率。

## `Box`

[`Box`] 是最简单的堆分配类型。`Box<T>` 值是分配在堆上的 `T` 值。

[`Box`]: https://doc.rust-lang.org/std/boxed/struct.Box.html

有时值得将结构体或枚举字段中的一个或多个装箱，以使类型更小。（有关此内容的更多信息，请参阅[类型大小](../8-type-sizes/)一章。）

除此之外，`Box` 很直接，没有太多优化空间。

## `Rc`/`Arc`

[`Rc`]/[`Arc`] 与 `Box` 类似，但堆上的值附带两个引用计数。它们允许值共享，这是减少内存占用的有效方式。

[`Rc`]: https://doc.rust-lang.org/std/rc/struct.Rc.html
[`Arc`]: https://doc.rust-lang.org/std/sync/struct.Arc.html

然而，如果用于很少共享的值，它们可能通过堆分配原本不必堆分配的值而增加分配速率。
[**示例**](https://github.com/rust-lang/rust/pull/37373/commits/c440a7ae654fb641e68a9ee53b03bf3f7133c2fe)。

与 `Box` 不同，对 `Rc`/`Arc` 值调用 `clone` 不涉及分配，而只是增加引用计数。

## `Vec`

[`Vec`] 是一种堆分配类型，在优化分配次数和/或最小化浪费空间方面有很大空间。要做到这一点，需要了解其元素的存储方式。

[`Vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html

`Vec` 包含三个字：长度、容量和指针。如果容量非零且元素大小非零，指针将指向堆分配的内存；否则，它不会指向已分配的内存。

即使 `Vec` 本身未堆分配，元素（如果存在且大小非零）也总是在堆上。如果存在非零大小的元素，存放这些元素的内存可能比必要的大，为未来的额外元素提供空间。当前元素数量是长度，在不重新分配的情况下可容纳的元素数量是容量。

当向量需要超出当前容量增长时，元素将被复制到更大的堆分配中，旧的堆分配将被释放。

### `Vec` 增长

通过常见方式创建的新空 `Vec`（[`vec![]`](https://doc.rust-lang.org/std/macro.vec.html) 或 [`Vec::new`] 或 [`Vec::default`]）长度和容量为零，不需要堆分配。如果你反复将单个元素推入 `Vec` 末尾，它会定期重新分配。增长策略未作规定，但截至撰写时使用准倍增策略，产生以下容量：0、4、8、16、32、64，依此类推。（它直接从 0 跳到 4，而不是经过 1 和 2，因为这在实践中[避免了许多分配][avoids many allocations]。）随着向量增长，重新分配的频率会指数级下降，但可能浪费的多余容量会指数级增加。

[`Vec::new`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.new
[`Vec::default`]: https://doc.rust-lang.org/std/default/trait.Default.html#tymethod.default
[avoids many allocations]: https://github.com/rust-lang/rust/pull/72227

这种增长策略对于可增长数据结构是典型的，在一般情况下是合理的，但如果你事先知道向量的可能长度，通常可以做得更好。如果你有一个热点向量分配点（例如热点的 [`Vec::push`] 调用），值得使用 [`eprintln!`] 在该点打印向量长度，然后进行一些后处理（例如使用 [`counts`]）来确定长度分布。例如，你可能有许多短向量，或较少数量的很长向量，优化分配点的最佳方式会相应不同。

[`Vec::push`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.push
[`eprintln!`]: https://doc.rust-lang.org/std/macro.eprintln.html
[`counts`]: https://github.com/nnethercote/counts/

### 短 `Vec`

如果你有许多短向量，可以使用 [`smallvec`] crate 的 `SmallVec` 类型。`SmallVec<[T; N]>` 是 `Vec` 的直接替代，可以在 `SmallVec` 本身内存储 `N` 个元素，如果元素数量超过该值则切换到堆分配。（还要注意，`vec![]` 字面量必须替换为 `smallvec![]` 字面量。）
[**示例 1**](https://github.com/rust-lang/rust/pull/50565/commits/78262e700dc6a7b57e376742f344e80115d2d3f2)，
[**示例 2**](https://github.com/rust-lang/rust/pull/55383/commits/526dc1421b48e3ee8357d58d997e7a0f4bb26915)。

[`smallvec`]: https://crates.io/crates/smallvec

`SmallVec` 在适当使用时能可靠地降低分配速率，但其使用不保证改善性能。它比 `Vec` 在正常操作时稍慢，因为它必须始终检查元素是否在堆上分配。此外，如果 `N` 较高或 `T` 较大，则 `SmallVec<[T; N]>` 本身可能比 `Vec<T>` 更大，复制 `SmallVec` 值会更慢。一如既往，需要基准测试来确认优化是否有效。

如果你有许多短向量*且*精确知道它们的最大长度，[`arrayvec`] crate 的 `ArrayVec` 是比 `SmallVec` 更好的选择。它不需要回退到堆分配，因此稍快一些。
[**示例**](https://github.com/rust-lang/rust/pull/74310/commits/c492ca40a288d8a85353ba112c4d38fe87ef453e)。

[`arrayvec`]: https://crates.io/crates/arrayvec

### 较长的 `Vec`

如果你知道向量的最小或确切大小，可以使用 [`Vec::with_capacity`]、[`Vec::reserve`] 或 [`Vec::reserve_exact`] 预留特定容量。例如，如果你知道一个向量将增长到至少 20 个元素，这些函数可以立即通过单次分配提供容量至少为 20 的向量，而逐个推入元素将导致四次分配（容量为 4、8、16 和 32）。
[**示例**](https://github.com/rust-lang/rust/pull/77990/commits/a7f2bb634308a5f05f2af716482b67ba43701681)。

[`Vec::with_capacity`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.with_capacity
[`Vec::reserve`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.reserve
[`Vec::reserve_exact`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.reserve_exact

如果你知道向量的最大长度，上述函数还可以让你避免不必要地分配多余空间。类似地，[`Vec::shrink_to_fit`] 可用于最小化浪费的空间，但注意它可能导致重新分配。

[`Vec::shrink_to_fit`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.shrink_to_fit

## `String`

[`String`] 包含堆分配的字节。`String` 的表示和操作与 `Vec<u8>` 非常相似。许多与增长和容量相关的 `Vec` 方法在 `String` 中有对应方法，例如 [`String::with_capacity`]。

[`String`]: https://doc.rust-lang.org/std/string/struct.String.html
[`String::with_capacity`]: https://doc.rust-lang.org/std/string/struct.String.html#method.with_capacity

[`smallstr`] crate 的 `SmallString` 类型类似于 `SmallVec` 类型。

[`smallstr`]: https://crates.io/crates/smallstr

[`smartstring`] crate 的 `String` 类型是 `String` 的直接替代，对于少于三个字大小的字符串避免堆分配。在 64 位平台上，这是任何少于 24 字节的字符串，包括所有包含 23 个或更少 ASCII 字符的字符串。
[**示例**](https://github.com/djc/topfew-rs/commit/803fd566e9b889b7ba452a2a294a3e4df76e6c4c)。

[`smartstring`]: https://crates.io/crates/smartstring

注意，`format!` 宏产生一个 `String`，这意味着它执行一次分配。如果你可以通过使用字符串字面量来避免 `format!` 调用，就可以避免这次分配。
[**示例**](https://github.com/rust-lang/rust/pull/55905/commits/c6862992d947331cd6556f765f6efbde0a709cf9)。
[`std::format_args`] 和/或 [`lazy_format`] crate 可能对此有帮助。

[`std::format_args`]: https://doc.rust-lang.org/std/macro.format_args.html
[`lazy_format`]: https://crates.io/crates/lazy_format

## 哈希表

[`HashSet`] 和 [`HashMap`] 是哈希表。在分配方面，它们的表示和操作与 `Vec` 类似：它们有一个单一的连续堆分配，存放键和值，随着表增长而按需重新分配。许多与增长和容量相关的 `Vec` 方法在 `HashSet`/`HashMap` 中有对应方法，例如 [`HashSet::with_capacity`]。

[`HashSet`]: https://doc.rust-lang.org/std/collections/struct.HashSet.html
[`HashMap`]: https://doc.rust-lang.org/std/collections/struct.HashMap.html
[`HashSet::with_capacity`]: https://doc.rust-lang.org/std/collections/struct.HashSet.html#method.with_capacity

## `clone`

对包含堆分配内存的值调用 [`clone`] 通常涉及额外的分配。例如，对非空 `Vec` 调用 `clone` 需要为元素进行新的分配（但注意新 `Vec` 的容量可能与原 `Vec` 不同）。例外是 `Rc`/`Arc`，其中 `clone` 调用只是增加引用计数。

[`clone`]: https://doc.rust-lang.org/std/clone/trait.Clone.html#tymethod.clone

[`clone_from`] 是 `clone` 的替代。`a.clone_from(&b)` 等价于 `a = b.clone()`，但可能避免不必要的分配。例如，如果你想将一个 `Vec` 克隆到现有 `Vec` 之上，如果可能，现有 `Vec` 的堆分配将被重用，如下例所示。
```rust
let mut v1: Vec<u32> = Vec::with_capacity(99);
let v2: Vec<u32> = vec![1, 2, 3];
v1.clone_from(&v2); // 重用 v1 的分配
assert_eq!(v1.capacity(), 99);
```
尽管 `clone` 通常会导致分配，但在许多情况下使用它是合理的，且通常可以使代码更简单。使用分析数据来查看哪些 `clone` 调用是热点且值得花精力避免。

[`clone_from`]: https://doc.rust-lang.org/std/clone/trait.Clone.html#method.clone_from

有时 Rust 代码会包含不必要的 `clone` 调用，原因是 (a) 程序员错误，或 (b) 代码更改使之前必要的 `clone` 调用变得不必要。如果你看到一个似乎不必要的热点 `clone` 调用，有时可以直接删除。
[**示例 1**](https://github.com/rust-lang/rust/pull/37318/commits/e382267cfb9133ef12d59b66a2935ee45b546a61)，
[**示例 2**](https://github.com/rust-lang/rust/pull/37705/commits/11c1126688bab32f76dbe1a973906c7586da143f)，
[**示例 3**](https://github.com/rust-lang/rust/pull/64302/commits/36b37e22de92b584b9cf4464ed1d4ad317b798be)。

## `to_owned`

[`ToOwned::to_owned`] 为许多常见类型实现。它从借用数据创建拥有数据，通常通过克隆，因此经常导致堆分配。例如，它可以用于从 `&str` 创建 `String`。

[`ToOwned::to_owned`]: https://doc.rust-lang.org/std/borrow/trait.ToOwned.html#tymethod.to_owned

有时可以通过在结构体中存储对借用数据的引用而非拥有副本来避免 `to_owned` 调用（以及相关的 `clone` 和 `to_string` 调用）。这需要在结构体上添加生命周期标注，使代码更复杂，且仅当性能分析和基准测试表明值得时才应这样做。
[**示例**](https://github.com/rust-lang/rust/pull/50855/commits/6872377357dbbf373cfd2aae352cb74cfcc66f34)。

## `Cow`

有时代码处理借用和拥有数据的混合。想象一个错误消息向量，其中一些是静态字符串字面量，一些是用 `format!` 构造的。明显的表示是 `Vec<String>`，如下例所示。
```rust
let mut errors: Vec<String> = vec![];
errors.push("something went wrong".to_string());
errors.push(format!("something went wrong on line {}", 100));
```
这需要调用 `to_string` 将静态字符串字面量提升为 `String`，从而产生一次分配。

相反，你可以使用 [`Cow`] 类型，它可以持有借用或拥有的数据。借用值 `x` 用 `Cow::Borrowed(x)` 包装，拥有值 `y` 用 `Cow::Owned(y)` 包装。`Cow` 还为各种字符串、切片和路径类型实现 `From<T>` trait，因此通常也可以使用 `into`。（或 `Cow::from`，更长但代码更易读，因为类型更清晰。）以下示例将所有这些组合在一起。

[`Cow`]: https://doc.rust-lang.org/std/borrow/enum.Cow.html

```rust
use std::borrow::Cow;
let mut errors: Vec<Cow<'static, str>> = vec![];
errors.push(Cow::Borrowed("something went wrong"));
errors.push(Cow::Owned(format!("something went wrong on line {}", 100)));
errors.push(Cow::from("something else went wrong"));
errors.push(format!("something else went wrong on line {}", 101).into());
```
`errors` 现在持有借用和拥有数据的混合，而不需要任何额外分配。此示例涉及 `&str`/`String`，但其他配对如 `&[T]`/`Vec<T>` 和 `&Path`/`PathBuf` 也是可能的。

[**示例 1**](https://github.com/rust-lang/rust/pull/37064/commits/b043e11de2eb2c60f7bfec5e15960f537b229e20)，
[**示例 2**](https://github.com/rust-lang/rust/pull/56336/commits/787959c20d062d396b97a5566e0a766d963af022)。

如果数据是不可变的，以上全部适用。但 `Cow` 还允许在需要修改时将借用数据提升为拥有数据。[`Cow::to_mut`] 将获取拥有值的可变引用，必要时进行克隆。这称为「写时克隆」（clone-on-write），即 `Cow` 名称的由来。

[`Deref`]: https://doc.rust-lang.org/std/ops/trait.Deref.html
[`Cow::to_mut`]: https://doc.rust-lang.org/std/borrow/enum.Cow.html#method.to_mut

这种写时克隆行为在你有一些借用数据（如 `&str`）且大部分只读但偶尔需要修改时很有用。

[**示例 1**](https://github.com/rust-lang/rust/pull/50855/commits/ad471452ba6fbbf91ad566dc4bdf1033a7281811)，
[**示例 2**](https://github.com/rust-lang/rust/pull/68848/commits/67da45f5084f98eeb20cc6022d68788510dc832a)。

最后，由于 `Cow` 实现 [`Deref`]，你可以直接在其包含的数据上调用方法。

`Cow` 可能比较棘手，但通常值得投入。

## 复用集合

有时你需要分阶段构建一个集合（如 `Vec`）。通常通过修改单个 `Vec` 比构建多个 `Vec` 然后合并它们更好。

例如，如果你有一个可能多次调用的产生 `Vec` 的函数 `do_stuff`：
```rust
fn do_stuff(x: u32, y: u32) -> Vec<u32> {
    vec![x, y]
}
```
改为修改传入的 `Vec` 可能更好：
```rust
fn do_stuff(x: u32, y: u32, vec: &mut Vec<u32>) {
    vec.push(x);
    vec.push(y);
}
```
有时值得保留一个可复用的「主力」集合。例如，如果循环的每次迭代都需要一个 `Vec`，你可以在循环外声明 `Vec`，在循环体内使用它，然后在循环体末尾调用 [`clear`]（清空 `Vec` 而不影响其容量）。这以避免分配为代价，模糊了每次迭代对 `Vec` 的使用彼此无关这一事实。
[**示例 1**](https://github.com/rust-lang/rust/pull/77990/commits/45faeb43aecdc98c9e3f2b24edf2ecc71f39d323)，
[**示例 2**](https://github.com/rust-lang/rust/pull/51870/commits/b0c78120e3ecae5f4043781f7a3f79e2277293e7)。

[`clear`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.clear

类似地，有时值得在结构体中保留一个主力集合，供一个或多个反复调用的方法复用。

## 从文件读取行

[`BufRead::lines`] 使逐行读取文件变得容易：
```rust
# fn blah() -> Result<(), std::io::Error> {
# fn process(_: &str) {}
use std::io::{self, BufRead};
let mut lock = io::stdin().lock();
for line in lock.lines() {
    process(&line?);
}
# Ok(())
# }
```
但它产生的迭代器返回 `io::Result<String>`，这意味着文件的每一行都会分配内存。

[`BufRead::lines`]: https://doc.rust-lang.org/stable/std/io/trait.BufRead.html#method.lines

另一种方法是在 [`BufRead::read_line`] 的循环中使用主力 `String`：
```rust
# fn blah() -> Result<(), std::io::Error> {
# fn process(_: &str) {}
use std::io::{self, BufRead};
let mut lock = io::stdin().lock();
let mut line = String::new();
while lock.read_line(&mut line)? != 0 {
    process(&line);
    line.clear();
}
# Ok(())
# }
```
这将分配次数减少到最多几次，甚至可能只有一次。（确切次数取决于 `line` 需要重新分配多少次，这取决于文件中行长度的分布。）

这仅在循环体可以操作 `&str` 而非 `String` 时才有效。

[`BufRead::read_line`]: https://doc.rust-lang.org/stable/std/io/trait.BufRead.html#method.read_line

[**示例**](https://github.com/nnethercote/counts/commit/7d39bbb1867720ef3b9799fee739cd717ad1539a)。

## 使用替代分配器

也可以在不修改代码的情况下，仅通过使用不同的分配器来改善堆分配性能。详情见[替代分配器][Alternative Allocators]一节。

[Alternative Allocators]: ../2-build-configuration/#alternative-allocators
## 避免回退

为确保代码的分配次数和/或大小不会无意中增加，你可以使用 [dhat-rs] 的*堆使用测试*功能编写测试，检查特定代码片段是否分配了预期的堆内存量。

[dhat-rs]: https://crates.io/crates/dhat
