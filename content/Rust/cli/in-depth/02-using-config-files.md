+++
title = "02-使用配置文件"
date = 2026-08-01T10:33:00+08:00
weight = 22
type = "docs"
description = "为 CLI 应用读写配置文件"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 使用配置文件 {#using-config-files}


> 原文链接: [https://rust-cli.github.io/book/in-depth/config-files.html](https://rust-cli.github.io/book/in-depth/config-files.html)


处理配置可能会很烦人，尤其是当你要支持多种操作系统，而它们各自对短期与长期文件有不同存放位置时。

对此有多种解决方案，有些比另一些更底层。

最容易用的 crate 是 [`confy`]。它只要求你给出应用名称，并用一个（实现了 `Serialize`、`Deserialize` 的）`struct` 指定配置布局，剩下的它会搞定！

```rust
#[derive(Debug, Serialize, Deserialize)]
struct MyConfig {
    name: String,
    comfy: bool,
    foo: i64,
}

fn main() -> Result<(), io::Error> {
    let cfg: MyConfig = confy::load("my_app")?;
    println!("{:#?}", cfg);
    Ok(())
}
```

用起来极其简单，当然你也因此牺牲了可配置性。但如果简单配置就够了，这个 crate 可能适合你！

[`confy`]: https://docs.rs/confy/0.3.1/confy/

## 配置环境

<aside class="todo">

**待办**

1. 评估现有的 crate
2. 命令行参数 + 多份配置 + 环境变量
3. [`configure`] 能否覆盖这一切？有没有好用的封装？

</aside>

[`configure`]: https://docs.rs/configure/0.1.1/configure/
