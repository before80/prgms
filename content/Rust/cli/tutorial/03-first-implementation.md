+++
title = "03-第一次实现"
date = 2026-08-01T10:33:00+08:00
weight = 13
type = "docs"
description = "实现第一版 grep 风格工具"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 第一次实现 _grrs_ {#first-implementation}


> 原文链接: [https://rust-cli.github.io/book/tutorial/impl-draft.html](https://rust-cli.github.io/book/tutorial/impl-draft.html)


在上一章讲完命令行参数之后，
我们已经有了输入数据，
可以开始编写真正的工具了。
目前 `main` 函数里只有这一行：

```rust
    let args = Cli::parse();
```

可以把临时放在那里、用来演示程序能正常工作的 `println` 删掉了。

先打开我们拿到的那个文件。

```rust
    let content = std::fs::read_to_string(&args.path).expect("could not read file");
```

<aside>

**说明：**
看到这里的 [`.expect`] 方法了吗？
这是一个快捷函数：当值（此处是输入文件）
无法读取时，程序会立即退出。
不太优雅，
在下一章[更友好的错误报告](04-nicer-error-reporting/)中，
我们会看看如何改进。

[`.expect`]: https://doc.rust-lang.org/1.39.0/std/result/enum.Result.html#method.expect

</aside>

接下来，遍历各行，
并打印每一行包含我们模式的内容：

```rust
    for line in content.lines() {
        if line.contains(&args.pattern) {
            println!("{}", line);
        }
    }
```

## 收尾 {#wrapping-up}

你的代码现在应如下所示：

```rust
use clap::Parser;

/// 在文件中搜索模式并显示包含它的行。
#[derive(Parser)]
struct Cli {
    /// 要查找的模式
    pattern: String,
    /// 要读取的文件路径
    path: std::path::PathBuf,
}

fn main() {
    let args = Cli::parse();
    let content = std::fs::read_to_string(&args.path).expect("could not read file");

    for line in content.lines() {
        if line.contains(&args.pattern) {
            println!("{}", line);
        }
    }
}
```

试一试：`cargo run -- main src/main.rs` 现在应该能工作了！

<aside class="exercise">

**读者练习：**
这不是最佳实现，因为
无论文件多大，都会把整个文件读进内存。
找一种办法优化它！
（一个思路是使用 [`BufReader`]，
而不是 `read_to_string()`。）

[`BufReader`]: https://doc.rust-lang.org/1.39.0/std/io/struct.BufReader.html

</aside>
