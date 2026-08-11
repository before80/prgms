+++
title = "13.3 改进我们的 I/O 项目"
date = 2026-08-05T08:44:00+08:00
weight = 59
type = "docs"
description = "用迭代器去掉 clone 并简化 search 实现"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 改进我们的 I/O 项目 {#i-o}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch13-03-improving-our-io-project.html](https://doc.rust-lang.org/stable/book/ch13-03-improving-our-io-project.html)


## 改进我们的 I/O 项目

　　有了关于迭代器的新知识，我们可以改进第 12 章的 I/O 项目，让某些代码更清晰、更简洁。来看迭代器如何改进 `Config::build` 和 `search` 的实现。

### 用迭代器去掉 `clone`

　　在示例 12-6 中，我们加入了这样的代码：接收 `String` 值的切片，通过索引并克隆这些值来创建 `Config` 实例，从而让 `Config` 拥有这些值。示例 13-17 复现了示例 12-23 中 `Config::build` 的实现。

**文件名：`src/main.rs`**
```rust
impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let file_path = args[2].clone();

        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}
```

**示例 13-17：复现示例 12-23 中的 `Config::build` 函数**

　　当时我们说不必担心低效的 `clone` 调用，因为以后会去掉它们。现在就是那个“以后”！

　　这里需要 `clone`，是因为参数 `args` 是含 `String` 元素的切片，而 `build` 并不拥有 `args`。要返回拥有所有权的 `Config` 实例，就得从 `query` 和 `file_path` 字段克隆值，好让 `Config` 拥有自己的数据。

　　有了迭代器的新知识，可以把 `build` 改成取得迭代器的所有权作为参数，而不是借用切片。用迭代器功能替代检查切片长度并索引特定位置的代码。迭代器会依次访问各个值，从而让 `Config::build` 在做什么更清晰。

　　一旦 `Config::build` 取得迭代器所有权，并不再使用会借用的索引操作，就可以把 `String` 值从迭代器移入 `Config`，而不必调用 `clone` 做新分配。

#### 直接使用返回的迭代器

　　打开 I/O 项目的 *src/main.rs*，它应类似这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    // --snip--

}
```

　　首先把示例 12-24 中 `main` 的开头改成示例 13-18，这次使用迭代器。在更新 `Config::build` 之前这还无法编译。

**文件名：`src/main.rs`**
```rust
fn main() {
    let config = Config::build(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    // --snip--

}
```

**示例 13-18：把 `env::args` 的返回值传给 `Config::build`**

　　`env::args` 函数返回的就是迭代器！现在不再把迭代器的值收集进向量再把切片传给 `Config::build`，而是直接把 `env::args` 返回的迭代器的所有权传给 `Config::build`。

　　接下来更新 `Config::build` 的定义。把签名改成示例 13-19 的样子。由于还需要更新函数体，此时仍无法编译。

**文件名：`src/main.rs`**
```rust
impl Config {
    fn build(
        mut args: impl Iterator<Item = String>,
    ) -> Result<Config, &'static str> {
        // --snip--
```

**示例 13-19：更新 `Config::build` 的签名以期望迭代器**

　　标准库关于 `env::args` 的文档表明，它返回的迭代器类型是 `std::env::Args`，该类型实现了 `Iterator` 特征，并产生 `String` 值。

　　我们已把 `Config::build` 的参数 `args` 从 `&[String]` 改成带特征约束 `impl Iterator<Item = String>` 的泛型类型。这里使用的是第 10 章 [「把特征作为参数」][impl-trait] 一节讨论过的 `impl Trait` 语法，表示 `args` 可以是任何实现了 `Iterator` 且产生 `String` 项的类型。

　　因为我们取得了 `args` 的所有权，并将通过迭代可变地使用它，可以在 `args` 参数说明中加上 `mut` 使其可变。

#### 使用 `Iterator` 特征的方法

　　接下来修复 `Config::build` 的函数体。既然 `args` 实现了 `Iterator`，就可以对它调用 `next`！示例 13-20 把示例 12-23 的代码改成使用 `next`。

**文件名：`src/main.rs`**
```rust
impl Config {
    fn build(
        mut args: impl Iterator<Item = String>,
    ) -> Result<Config, &'static str> {
        args.next();

        let query = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a query string"),
        };

        let file_path = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a file path"),
        };

        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}
```

**示例 13-20：改用迭代器方法实现 `Config::build` 的函数体**

　　记住，`env::args` 返回值的第一项是程序名。我们要忽略它并取下一项，因此先调用 `next` 并丢弃返回值。然后再调用 `next`，取得要放进 `Config` 的 `query` 字段的值。若 `next` 返回 `Some`，用 `match` 取出值；若返回 `None`，说明参数不够，提前返回 `Err`。对 `file_path` 做同样处理。

### 用迭代器适配器让代码更清晰

　　I/O 项目中的 `search` 函数也可以利用迭代器。示例 13-21 复现了示例 12-19 中的实现。

**文件名：`src/lib.rs`**
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }

    results
}
```

**示例 13-21：示例 12-19 中 `search` 函数的实现**

　　用迭代器适配器方法可以把这段代码写得更简洁，也避免了可变的中间 `results` 向量。函数式编程风格倾向于尽量减少可变状态，使代码更清晰。去掉可变状态还可能为将来并行搜索留下空间，因为不必管理对 `results` 向量的并发访问。示例 13-22 展示了这一改动。

**文件名：`src/lib.rs`**
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents
        .lines()
        .filter(|line| line.contains(query))
        .collect()
}
```

**示例 13-22：在 `search` 实现中使用迭代器适配器方法**

　　回想 `search` 的目的：返回 `contents` 中所有包含 `query` 的行。与示例 13-16 中的 `filter` 例子类似，这里用 `filter` 适配器只保留 `line.contains(query)` 为 `true` 的行，再用 `collect` 把匹配行收集进另一个向量。简洁多了！也可以对 `search_case_insensitive` 做同样的迭代器改写。

　　若要进一步改进，可去掉对 `collect` 的调用，把返回类型改成 `impl Iterator<Item = &'a str>`，让 `search` 本身成为迭代器适配器并返回迭代器。注意测试也要相应更新！在改动前后用 `minigrep` 搜索大文件，观察行为差异。改动前，程序要收集完所有结果才会打印；改动后，每找到一行匹配就会打印，因为 `run` 中的 `for` 循环能利用迭代器的惰性。

### 在循环与迭代器之间选择

　　接下来自然会问：自己的代码该选哪种风格、为什么——示例 13-21 的原始实现，还是示例 13-22 的迭代器版本（假设仍在返回前收集全部结果，而不是直接返回迭代器）？多数 Rust 程序员更偏好迭代器风格。起初上手稍难，但一旦熟悉各种迭代器适配器及其作用，迭代器往往更容易理解。代码不再纠缠于循环细节和构建新向量，而是聚焦于循环的高层目标。这抽象掉了一些常见代码，更容易看清本段代码特有的概念，例如迭代器中每个元素必须满足的过滤条件。

　　但这两种实现真的等价吗？直觉上可能觉得底层循环会更快。下一节讨论性能。

[impl-trait]: ../../generics/02-traits/#traits-as-parameters
