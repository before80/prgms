+++
title = "第4章 文档"
date = 2026-08-18T21:50:00+08:00
weight = 60
type = "docs"
description = "文档 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/documentation.html](https://rust-lang.github.io/api-guidelines/documentation.html)

# 文档

## Crate 级文档详尽并含示例 (C-CRATE-DOC) {#c-crate-doc}

参见 [RFC 1687]。

[RFC 1687]: https://github.com/rust-lang/rfcs/pull/1687

## 所有项都有 rustdoc 示例 (C-EXAMPLE) {#c-example}

每个公开的模块、trait、结构体、枚举、函数、方法、宏与类型定义都应有一个行使其功能的示例。

本指南应在合理范围内应用。

指向另一项上适用示例的链接可能就足够了。例如，若恰好只有一个函数使用某一类型，在函数或类型二者之一
上写一个示例，并从另一处链接过去，可能是合适的。

示例的目的并不总是展示 *如何使用* 该项。可以预期读者理解如何调用函数、对枚举做匹配以及其他基本任务。
相反，示例往往意在展示 *为何有人想要使用* 该项。

```rust
// 这将是使用 clone() 的糟糕示例。它机械地展示了 *如何* 调用
// clone()，但完全没有展示 *为何* 有人会想要这样做。
fn main() {
    let hello = "hello";

    hello.clone();
}
```

## 示例使用 `?`，不用 `try!`，不用 `unwrap` (C-QUESTION-MARK) {#c-question-mark}

无论喜欢与否，示例代码常被用户原样复制。对错误做 unwrap 应是用户需要有意识做出的决定。

组织可能失败的示例代码的一种常见方式如下。以 `#` 开头的行在 `cargo test` 构建示例时会被编译，
但不会出现在用户可见的 rustdoc 中。

```
/// ```rust
/// # use std::error::Error;
/// #
/// # fn main() -> Result<(), Box<dyn Error>> {
/// your;
/// example?;
/// code;
/// #
/// #     Ok(())
/// # }
/// ```
```

## 函数文档包含错误、panic 与安全性考量 (C-FAILURE) {#c-failure}

错误条件应记录在 "Errors" 小节中（rustdoc 规范章节名保持英文）。这也适用于 trait 方法——
允许或预期实现返回错误的 trait 方法，应使用 "Errors" 小节进行文档说明。

例如在标准库中，[`std::io::Read::read`] trait 方法的某些实现可能返回错误。

[`std::io::Read::read`]: https://doc.rust-lang.org/std/io/trait.Read.html#tymethod.read

```
/// 从该源拉取一些字节到指定缓冲区，返回
/// 读取了多少字节。
///
/// ... 更多信息 ...
///
/// # Errors
///
/// 若此函数遇到任何形式的 I/O 或其他错误，将返回错误
/// 变体。若返回了错误，则必须保证未读取任何字节。
```

Panic 条件应记录在 "Panics" 小节中（rustdoc 规范章节名保持英文）。这也适用于 trait 方法——
允许或预期实现会 panic 的 trait 方法，应使用 "Panics" 小节进行文档说明。

在标准库中，[`Vec::insert`] 方法可能 panic。

[`Vec::insert`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.insert

```
/// 在向量中位置 `index` 处插入一个元素，将其后所有
/// 元素向右移动。
///
/// # Panics
///
/// 若 `index` 越界则 panic。
```

不必记录所有可设想的 panic 情形，尤其当 panic 发生在调用方提供的逻辑中时。例如，为下面代码中的
`Display` panic 做文档似乎过分。但有疑虑时，宁可多记录一些 panic 情形。

```rust
/// # Panics
///
/// 若 `T` 的 `Display` 实现发生 panic，此函数会 panic。
pub fn print<T: Display>(t: T) {
    println!("{}", t.to_string());
}
```

不安全函数应使用 "Safety" 小节进行文档说明（rustdoc 规范章节名保持英文），解释调用方为正确使用
该函数须维护的所有不变量。

不安全的 [`std::ptr::read`] 要求调用方做到以下各点。

[`std::ptr::read`]: https://doc.rust-lang.org/std/ptr/fn.read.html

```
/// 从 `src` 读取值而不移动它。这会使
/// `src` 中的内存保持不变。
///
/// # Safety
///
/// 除了接受原始指针外，此操作不安全是因为它在语义上
/// 将值移出 `src` 而不阻止对 `src` 的进一步使用。
/// 若 `T` 不是 `Copy`，则必须注意确保在数据再次被覆盖之前
/// （例如用 `write`、`zero_memory` 或 `copy_memory`）不使用
/// `src` 处的值。注意 `*src = foo` 也算一次使用，
/// 因为它会尝试 drop 先前位于 `*src` 的值。
///
/// 指针必须对齐；若未对齐请使用 `read_unaligned`。
```

## 正文包含指向相关内容的超链接 (C-LINK) {#c-link}

常规链接可用通常的 markdown 语法 `[text](url)` 内联添加。指向其他类型的链接可通过用
``[`text`]`` 标记它们，然后在 docstring 末尾新行添加链接目标 ``[`text`]: <target>``，
其中 `<target>` 如下所述。

指向同一类型内方法的链接目标通常如下：

```md
[`serialize_struct`]: #method.serialize_struct
```

指向其他类型的链接目标通常如下：

```md
[`Deserialize`]: trait.Deserialize.html
```

链接目标也可指向父模块或子模块：

```md
[`Value`]: ../enum.Value.html
[`DeserializeOwned`]: de/trait.DeserializeOwned.html
```

本指南由 RFC 1574 在 ["Link all the things"] 标题下正式推荐。

["Link all the things"]: https://github.com/rust-lang/rfcs/blob/master/text/1574-more-api-documentation-conventions.md#link-all-the-things

## Cargo.toml 包含所有常用元数据 (C-METADATA) {#c-metadata}

`Cargo.toml` 的 `[package]` 部分应包含以下值：

- `authors`
- `description`
- `license`
- `repository`
- `keywords`
- `categories`

此外，还有两个可选的元数据字段：

- `documentation`
- `homepage`

默认情况下，*crates.io* 会链接到该 crate 在 [*docs.rs*] 上的文档。仅当文档托管在 *docs.rs*
以外的地方时才需要设置 `documentation` 元数据，例如因为该 crate 链接到 *docs.rs* 构建环境中
不可用的共享库。

[*docs.rs*]: https://docs.rs

仅当该 crate 有有别于源码仓库或 API 文档的独特网站时，才应设置 `homepage` 元数据。不要让
`homepage` 与 `documentation` 或 `repository` 的值冗余。例如，serde 将 `homepage` 设为
*https://serde.rs*，一个专用网站。

## 发行说明记录所有重要变更 (C-RELNOTES) {#c-relnotes}

crate 的用户可以阅读发行说明，以了解该 crate 每个已发布版本中变更的摘要。发行说明的链接，
或说明本身，应包含在 crate 级文档和/或 Cargo.toml 中链接的仓库中。

破坏性变更（如 [RFC 1105] 所定义）应在发行说明中明确标出。

若使用 Git 跟踪 crate 的源码，发布到 *crates.io* 的每个版本都应有对应的标签，标识所发布的提交。
对非 Git 的 VCS 工具也应使用类似流程。

```bash
# 为当前提交打标签
GIT_COMMITTER_DATE=$(git log -n1 --pretty=%aD) git tag -a -m "Release 0.3.0" 0.3.0
git push --tags
```

推荐使用带注释的标签，因为若存在任何带注释的标签，某些 Git 命令会忽略未注释的标签。

[RFC 1105]: https://github.com/rust-lang/rfcs/blob/master/text/1105-api-evolution.md

### 示例

- [Serde 1.0.0 发行说明](https://github.com/serde-rs/serde/releases/tag/v1.0.0)
- [Serde 0.9.8 发行说明](https://github.com/serde-rs/serde/releases/tag/v0.9.8)
- [Serde 0.9.0 发行说明](https://github.com/serde-rs/serde/releases/tag/v0.9.0)
- [Diesel 变更日志](https://github.com/diesel-rs/diesel/blob/master/CHANGELOG.md)

## Rustdoc 不展示无帮助的实现细节 (C-HIDDEN) {#c-hidden}

Rustdoc 应包含用户完整使用该 crate 所需的一切，且仅此而已。用正文解释相关实现细节没问题，
但它们不应成为文档中的真实条目。

尤其要对哪些 impl 在 rustdoc 中可见保持选择——用户完整使用该 crate 所需的全部，但不要更多。
在下面的代码中，`PublicError` 的 rustdoc 默认会显示 `From<PrivateError>` impl。我们选择用
`#[doc(hidden)]` 隐藏它，因为用户的代码中永远不会有 `PrivateError`，因此该 impl 对他们永远不相关。

```rust
// 此错误类型返回给用户。
pub struct PublicError { /* ... */ }

// 此错误类型由某些私有辅助函数返回。
struct PrivateError { /* ... */ }

// 启用 `?` 运算符的使用。
#[doc(hidden)]
impl From<PrivateError> for PublicError {
    fn from(err: PrivateError) -> PublicError {
        /* ... */
    }
}
```

[`pub(crate)`] 是从公共 API 中移除实现细节的另一大利器。它允许项在所属模块之外使用，
但不能在同一 crate 之外使用。

[`pub(crate)`]: https://github.com/rust-lang/rfcs/blob/master/text/1422-pub-restricted.md
