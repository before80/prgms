+++
title = "2 `no_std`"
date = 2026-08-11T11:30:00+08:00
weight = 295
type = "docs"
description = "`no_std` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/no_std.html](https://google.github.io/comprehensive-rust/bare-metal/no_std.html)

# 2 `no_std`

<table>
<tr>
<th>

`core`

</th>
<th>

`alloc`

</th>
<th>

`std`

</th>
</tr>
<tr valign="top">
<td>

- 切片、`&str`、`CStr`
- `NonZeroU8`…
- `Option`、`Result`
- `Display`、`Debug`、`write!`…
- `Iterator`
- `Error`
- `panic!`、`assert_eq!`…
- `NonNull` 以及常见的指针相关函数
- `Future` 与 `async`/`await`
- `fence`、`AtomicBool`、`AtomicPtr`、`AtomicU32`…
- `Duration`

</td>
<td>

- `Box`、`Cow`、`Arc`、`Rc`
- `Vec`、`BinaryHeap`、`BtreeMap`、`LinkedList`、`VecDeque`
- `String`、`CString`、`format!`

</td>
<td>

- `HashMap`
- `Mutex`、`Condvar`、`Barrier`、`Once`、`RwLock`、`mpsc`
- `File` 以及 `fs` 的其余部分
- `println!`、`Read`、`Write`、`Stdin`、`Stdout` 以及 `io` 的其余部分
- `Path`、`OsString`
- `net`
- `Command`、`Child`、`ExitCode`
- `spawn`、`sleep` 以及 `thread` 的其余部分
- `SystemTime`、`Instant`

</td>
</tr>
</table>

> - `HashMap` 依赖随机数生成器（RNG）。
> - `std` 会重新导出 `core` 与 `alloc` 的内容。

