+++
title = "04-更友好的错误报告"
date = 2026-08-01T10:33:00+08:00
weight = 14
type = "docs"
description = "改进 CLI 错误处理与报告"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 更友好的错误报告 {#nicer-error-reporting}


> 原文链接: [https://rust-cli.github.io/book/tutorial/errors.html](https://rust-cli.github.io/book/tutorial/errors.html)


我们只能接受一个事实：错误总会发生。
与许多其它语言不同，
在使用 Rust 时很难忽视并回避这一点，
因为它没有异常。
所有可能的错误状态，常常编码在函数的返回类型里。

## Results {#results}

像 [`read_to_string`] 这样的函数并不直接返回字符串。
相反，它返回一个 [`Result`]，
其中要么是
一个 `String`，
要么是某种类型的错误。
此处是 [`std::io::Error`]。

[`read_to_string`]: https://doc.rust-lang.org/1.39.0/std/fs/fn.read_to_string.html
[`Result`]: https://doc.rust-lang.org/1.39.0/std/result/index.html
[`std::io::Error`]: https://doc.rust-lang.org/1.39.0/std/io/type.Result.html

怎么知道是哪一种？
因为 `Result` 是一个 `enum`，
可以用 `match` 检查它是哪个变体：

```rust,no_run
let result = std::fs::read_to_string("test.txt");
match result {
    Ok(content) => { println!("File content: {}", content); }
    Err(error) => { println!("Oh noes: {}", error); }
}
```

<aside>

**说明：**
不确定枚举是什么，或它们在 Rust 中如何工作？
[查看 Rust 书的这一章](https://doc.rust-lang.org/1.39.0/book/ch06-00-enums.html)
来跟上进度。

</aside>

## Unwrapping {#unwrapping}

现在我们能访问文件内容了，
但在 `match` 块之后并不能真正拿它做别的事。
为此，需要处理错误分支。
虽然 `match` 各臂必须返回同一类型是个挑战，
但有个巧妙的办法绕过：

```rust,no_run
let result = std::fs::read_to_string("test.txt");
let content = match result {
    Ok(content) => { content },
    Err(error) => { panic!("Can't deal with {}, just exit here", error); }
};
println!("file content: {}", content);
```

`match` 块之后可以使用 `content` 里的 String，但
如果 `result` 是错误，这个 String 就不会存在。
没关系，因为程序会在用到 `content` 之前就退出。

这看起来也许很激烈，
但非常方便。
如果你的程序需要读那个文件，而文件不存在时什么也做不了，
退出是合理的策略。
[`Result`] 上甚至有一个叫 `unwrap` 的快捷方法：

```rust,no_run
let content = std::fs::read_to_string("test.txt").unwrap();
```

## 不必 panic {#no-need-to-panic}

当然，中止程序不是处理错误的唯一方式。
与其用 `panic!`，我们可以直接 `return`：

```rust,no_run
# fn main() -> Result<(), Box<dyn std::error::Error>> {
let result = std::fs::read_to_string("test.txt");
let content = match result {
    Ok(content) => { content },
    Err(error) => { return Err(error.into()); }
};
# Ok(())
# }
```

不过，这会改变函数的返回类型。
此前示例里一直隐藏着一件事：
这段代码所在的函数签名。
而在这个带 `return` 的最后示例中，
它变得重要了。
下面是*完整*示例：

```rust,no_run
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = std::fs::read_to_string("test.txt");
    let content = match result {
        Ok(content) => { content },
        Err(error) => { return Err(error.into()); }
    };
    println!("file content: {}", content);
    Ok(())
}
```

我们的返回类型是 `Result`！
所以可以在第二个 match 臂里写 `return Err(error);`。
看到底部的 `Ok(())` 了吗？
它是函数的默认返回值，意思是：
“Result 正常，且没有内容”。

<aside>

**说明：**
为什么不写成 `return Ok(());`？
完全可以——那样也完全合法。
Rust 中任何块的最后一个表达式就是它的返回值，
习惯上会省略不必要的 `return`。

</aside>

## 问号运算符 {#question-mark}

就像调用 `.unwrap()` 是带 `panic!` 的错误臂 `match` 的快捷写法，
带 `return` 的错误臂 `match` 也有快捷写法：
`?`。

没错，就是一个问号。
你可以把它接在类型为 `Result` 的值后面，
Rust 会在内部把它展开成与我们刚写的
`match` 非常相似的代码。

试一试：

```rust,no_run
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string("test.txt")?;
    println!("file content: {}", content);
    Ok(())
}
```

非常简洁！

<aside>

**说明：**
这里还有几件事在发生，
要使用它并不需要全部理解。
例如，
`main` 函数里的错误类型是 `Box<dyn std::error::Error>`，
但上面我们看到 `read_to_string` 返回的是 [`std::io::Error`]。
之所以能工作，是因为 `?` 展开的代码会*转换*错误类型。

`Box<dyn std::error::Error>` 本身也是个有趣的类型。
它是一个可以容纳*任意*实现了标准 [`Error`][`std::error::Error`] trait 的类型的 `Box`。
这意味着所有错误都能放进这个盒子，
我们可以对所有通常返回 `Result` 的函数使用 `?`。

[`std::error::Error`]: https://doc.rust-lang.org/1.39.0/std/error/trait.Error.html

</aside>

## 提供上下文 {#providing-context}

在 `main` 里使用 `?` 得到的错误还可以，
但并不出色。
例如，
当你运行 `std::fs::read_to_string("test.txt")?`
而文件 `test.txt` 不存在时，
会得到这样的输出：

```text
Error: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

若代码里实际上并没有包含文件名，
就很难判断是哪个文件 `NotFound`。
有多种处理方式。

其一，可以创建自己的错误类型，
并用它构造自定义错误消息：

```rust
#[derive(Debug)]
struct CustomError(String);

fn main() -> Result<(), CustomError> {
    let path = "test.txt";
    let content = std::fs::read_to_string(path)
        .map_err(|err| CustomError(format!("Error reading `{}`: {}", path, err)))?;
    println!("file content: {}", content);
    Ok(())
}
```

运行后会得到自定义错误消息：

```text
Error: CustomError("Error reading `test.txt`: No such file or directory (os error 2)")
```

不太好看，
但之后可以为该类型调整调试输出。

这种模式非常常见。
不过有一个问题：
我们没有保存原始错误，
只保存了它的字符串表示。
流行的 [`anyhow`] 库对此有个漂亮的解法：
它的 [`Context`] trait 可以用来添加类似我们 `CustomError` 类型的描述。
此外，它还会保留原始错误，
于是我们得到一条指向根因的“错误消息链”。

[`anyhow`]: https://docs.rs/anyhow
[`Context`]: https://docs.rs/anyhow/1.0/anyhow/trait.Context.html

先导入 `anyhow` crate：在 `Cargo.toml` 的 `[dependencies]` 段加入
`anyhow = "1.0"`。

完整示例如下：

```rust
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let path = "test.txt";
    let content =
        std::fs::read_to_string(path).with_context(|| format!("could not read file `{}`", path))?;
    println!("file content: {}", content);
    Ok(())
}
```

这会打印错误：

```text
Error: could not read file `test.txt`

Caused by:
    No such file or directory (os error 2)
```

## 收尾 {#wrapping-up}

你的代码现在应如下所示：

```rust
use anyhow::{Context, Result};
use clap::Parser;

/// 在文件中搜索模式并显示包含它的行。
#[derive(Parser)]
struct Cli {
    /// 要查找的模式
    pattern: String,
    /// 要读取的文件路径
    path: std::path::PathBuf,
}

fn main() -> Result<()> {
    let args = Cli::parse();

    let content = std::fs::read_to_string(&args.path)
        .with_context(|| format!("could not read file `{}`", args.path.display()))?;

    for line in content.lines() {
        if line.contains(&args.pattern) {
            println!("{}", line);
        }
    }

    Ok(())
}
```
