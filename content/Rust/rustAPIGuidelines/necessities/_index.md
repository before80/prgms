+++
title = "第11章 必要事项"
date = 2026-08-18T21:50:00+08:00
weight = 130
type = "docs"
description = "必要事项 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/necessities.html](https://rust-lang.github.io/api-guidelines/necessities.html)

# 必要事项

## 稳定 crate 的公开依赖也是稳定的 (C-STABLE) {#c-stable}

crate 要成为稳定版本（>=1.0.0），其全部公开依赖也必须是稳定的。

公开依赖是指：当前 crate 的公开 API 中用到了其类型的那些 crate。

```rust
pub fn do_my_thing(arg: other_crate::TheirThing) { /* ... */ }
```

包含此函数的 crate 不能稳定发布，除非 `other_crate` 也已稳定。

要小心，公开依赖可能从意想不到的地方潜入。

```rust
pub struct Error {
    private: ErrorImpl,
}

enum ErrorImpl {
    Io(io::Error),
    // 即便 other_crate 不稳定也应该没问题，
    // 因为 ErrorImpl 是私有的。
    Dep(other_crate::Error),
}

// 糟糕！这会把 other_crate 放进当前 crate 的公开 API。
impl From<other_crate::Error> for Error {
    fn from(err: other_crate::Error) -> Self {
        Error { private: ErrorImpl::Dep(err) }
    }
}
```

## Crate 及其依赖使用宽松许可证 (C-PERMISSIVE) {#c-permissive}

Rust 项目产出的软件采用双重许可，可按 [MIT] 或 [Apache 2.0] 许可证使用。只求与 Rust 生态系统最大兼容的 crate，建议同样采用这种方式，并按下述做法操作。其他选项见下文。

本 API 指南并不详细解释 Rust 的许可证，但 [Rust FAQ] 中有少量说明。这些指南关注与 Rust 的互操作性，并非对许可选项的全面综述。

[MIT]: https://github.com/rust-lang/rust/blob/master/LICENSE-MIT
[Apache 2.0]: https://github.com/rust-lang/rust/blob/master/LICENSE-APACHE
[Rust FAQ]: https://github.com/dtolnay/rust-faq#why-a-dual-mitasl2-license

要将 Rust 许可证应用到你的项目，请在 `Cargo.toml` 中定义 `license` 字段为：

```toml
[package]
name = "..."
version = "..."
authors = ["..."]
license = "MIT OR Apache-2.0"
```

然后在仓库根目录添加 `LICENSE-APACHE` 与 `LICENSE-MIT` 文件，写入许可证全文（例如可从 choosealicense.com 获取 [Apache-2.0](https://choosealicense.com/licenses/apache-2.0/) 与 [MIT](https://choosealicense.com/licenses/mit/)）。

并在 README.md 靠近末尾处加入：

```
## 许可证

按你的选择，使用以下任一许可证授权

 * Apache License, Version 2.0
   ([LICENSE-APACHE](LICENSE-APACHE) 或 <http://www.apache.org/licenses/LICENSE-2.0>)
 * MIT license
   ([LICENSE-MIT](LICENSE-MIT) 或 <http://opensource.org/licenses/MIT>)

## 贡献

除非你另行明确说明，你有意提交以包含在本作品中的任何贡献，依 Apache-2.0 许可证所定义，均按上述双重许可授权，不含任何额外条款或条件。
```

除 MIT/Apache-2.0 双重许可外，Rust crate 作者另一种常见做法是只采用单一宽松许可证，例如 MIT 或 BSD。这种许可方案也与 Rust 的许可完全兼容，因为它所施加的限制不超出 Rust 的 MIT 许可证。

若希望与 Rust 达到完美的许可证兼容，不建议只选择 Apache 许可证。Apache 许可证虽是宽松许可证，但其限制超出 MIT 与 BSD，在某些场景下会劝退或阻止使用，因此仅 Apache 许可的软件，无法用于 Rust 运行时栈大部分都能使用的某些场合。

crate 依赖的许可证会影响该 crate 自身的分发限制，因此宽松许可的 crate 一般应只依赖同样宽松许可的 crate。
