+++
title = "2.4-HTML 报告"
date = 2026-08-22T20:00:00+08:00
weight = 6
type = "docs"
description = "HTML 基准测试报告"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# HTML 报告 {#html-report}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/html_report.html](https://bheisler.github.io/criterion.rs/book/user_guide/html_report.html)


从 Criterion.rs 0.4.0 起，必须通过 `html_reports` [feature](https://doc.rust-lang.org/cargo/reference/features.html#dependency-features) 显式启用 HTML 报告：
```toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
```
Criterion.rs 可在 `target/criterion/reports/index.html` 生成展示基准测试结果的 HTML 报告。默认情况下，若可用则使用 [gnuplot](http://www.gnuplot.info/) 生成图表，否则使用 [plotters](https://github.com/38/plotters) crate。以下示例由 gnuplot 后端生成，plotters 生成的图表类似。

要查看示例报告，[点击此处](../../)。有关所显示图表与统计的更多细节，请参阅本书其他页面。
