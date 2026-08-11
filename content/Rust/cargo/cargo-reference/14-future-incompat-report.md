+++
title = "14-未来不兼容报告"
date = 2026-07-30T14:49:00+08:00
weight = 56
type = "docs"
description = "未来不兼容性报告机制"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 未来不兼容报告 {#future-incompat-report}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/future-incompat-report.html](https://doc.rust-lang.org/cargo/reference/future-incompat-report.html)


Cargo 会检查所有依赖中的未来不兼容（future-incompatible）警告。这些警告针对可能在将来变成硬错误的变更，届时依赖将无法在未来版本的 rustc 中构建。若发现任何警告，会显示一小段提示，说明已发现警告，并提供如何显示完整报告的说明。

例如，你可能在构建结束时看到类似内容：

```text
warning: the following packages contain code that will be rejected by a future
         version of Rust: rental v0.5.5
note: to see what the problems were, use the option `--future-incompat-report`,
      or run `cargo report future-incompatibilities --id 1`
```

可用 `cargo report future-incompatibilities --id ID` 命令显示完整报告，或在再次构建时加上 `--future-incompat-report` 标志。开发者随后应将其依赖更新到已修复该问题的版本，或与依赖的开发者协作解决问题。

## 配置 {#configuration}
此功能可通过 `.cargo/config.toml` 中的 [`[future-incompat-report]`][config] 段进行配置。目前支持的选项为：

```toml
[future-incompat-report]
frequency = "always"
```

`frequency` 支持的值为 `"always"` 与 `"never"`，用于控制是否在 `cargo build` / `cargo check` 结束时打印消息。

[config]: ../06-configuration/#future-incompat-report
