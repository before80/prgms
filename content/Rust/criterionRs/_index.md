+++
title = "Criterion.rs"
date = 2026-08-22T20:00:00+08:00
weight = 1
type = "docs"
description = "Criterion.rs 统计驱动微基准测试工具简介"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# Criterion.rs {#criterion-rs}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/criterion_rs.html](https://bheisler.github.io/criterion.rs/book/criterion_rs.html)


Criterion.rs 是一款基于统计学的微基准测试工具。它是 [Haskell 的 Criterion](https://hackage.haskell.org/package/criterion) 库的 Rust 移植版。

Criterion.rs 基准测试会在多次运行之间收集并存储统计信息，能够自动检测性能回归，也能衡量优化效果。

Criterion.rs 是免费开源的。你可以在 [GitHub](https://github.com/bheisler/criterion.rs) 上找到源码。问题和功能请求可提交到 [issue 跟踪器](https://github.com/bheisler/criterion.rs/issues)。

## API Docs ##

除本书外，你可能还想阅读 [API 文档](http://bheisler.github.io/criterion.rs/criterion/)。

## License ##

Criterion.rs 采用 [Apache 2.0](https://github.com/bheisler/criterion.rs/blob/master/LICENSE-APACHE) 与 [MIT](https://github.com/bheisler/criterion.rs/blob/master/LICENSE-MIT) 双许可证。

## Debug Output ##

要在 Criterion.rs 中启用调试输出，请定义环境变量 `CRITERION_DEBUG`。例如（在 bash 中）：

```bash
CRITERION_DEBUG=1 cargo bench
```

这将启用额外的调试输出。若使用 gnuplot，Criterion.rs 还会在生成的图表文件旁保存 gnuplot 脚本。向 Criterion.rs 提交 issue 时（尤其是报告绘图生成相关问题时），请启用此选项运行基准测试，并提供额外输出及相关的 gnuplot 脚本。
