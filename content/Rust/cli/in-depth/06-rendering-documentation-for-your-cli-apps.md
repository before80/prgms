+++
title = "06-为 CLI 应用生成文档"
date = 2026-08-01T10:33:00+08:00
weight = 26
type = "docs"
description = "渲染 CLI 帮助与文档"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 为 CLI 应用生成文档 {#rendering-documentation-for-your-cli-apps}


> 原文链接: [https://rust-cli.github.io/book/in-depth/docs.html](https://rust-cli.github.io/book/in-depth/docs.html)


CLI 的文档通常包括命令中的 `--help` 部分，以及一份手册（`man`）页。

两者都可以在使用 [`clap`](https://crates.io/crates/clap) 时通过 [`clap_mangen`](https://crates.io/crates/clap_mangen) crate 自动生成。

```rust
#[derive(Parser)]
pub struct Head {
    /// 要加载的文件
    pub file: PathBuf,
    /// 要打印多少行
    #[arg(short = "n", default_value = "5")]
    pub count: usize,
}
```

其次，你需要使用 `build.rs`，在编译时根据代码中对应用的定义生成手册文件。

需要注意几件事（例如你想如何打包二进制），但现在我们简单地把 `man` 文件放在 `src` 文件夹旁边。

```rust
use clap::CommandFactory;

#[path="src/cli.rs"]
mod cli;

fn main() -> std::io::Result<()> {
    let out_dir = std::path::PathBuf::from(std::env::var_os("OUT_DIR").ok_or_else(|| std::io::ErrorKind::NotFound)?);
    let cmd = cli::Head::command();

    let man = clap_mangen::Man::new(cmd);
    let mut buffer: Vec<u8> = Default::default();
    man.render(&mut buffer)?;

    std::fs::write(out_dir.join("head.1"), buffer)?;

    Ok(())
}
```

现在编译你的应用时，项目目录中会有一个 `head.1` 文件。

如果你用 `man` 打开它，就能欣赏到这份免费文档了。
