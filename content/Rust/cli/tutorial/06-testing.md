+++
title = "06-测试"
date = 2026-08-01T10:33:00+08:00
weight = 16
type = "docs"
description = "为 CLI 应用编写测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 测试 {#testing}


> 原文链接: [https://rust-cli.github.io/book/tutorial/testing.html](https://rust-cli.github.io/book/tutorial/testing.html)


经过几十年的软件开发，
人们发现了一条真理：
未测试的软件很少能正常工作。
许多人甚至会说，
大多数测过的软件也照样不行。
但我们都是乐观主义者，对吧？
为确保程序按你期望的去做，
明智的做法是测试它。

一个好的起点是
写一份 `README` 文件，
描述程序应做什么；
当你觉得准备好做新发布时，
再通读 `README`，确认
行为仍符合预期。
你还可以把练习做得更严格：
写下程序应对错误输入如何反应。

还有一个花哨的主意：
在写代码之前先写那份 `README`。

<aside>

**说明：**
如果你还没听过，
可以看看
[测试驱动开发] (TDD)。

[测试驱动开发]: https://en.wikipedia.org/wiki/Test-driven_development


</aside>

## 自动化测试 {#automated-testing}

好吧，这些都很美好，
但全靠手动？
那会花很多时间。
与此同时，
许多人已经享受让计算机替自己做事。
来谈谈如何自动化这些测试。

Rust 有内置的测试框架，
我们先写第一个测试：

```rust,ignore
# fn answer() -> i32 {
#   42
# }
#
#[test]
fn check_answer_validity() {
    assert_eq!(answer(), 42);
}
```

你几乎可以把这段代码放进包里的任意源文件，
`cargo test` 就会找到
并运行它。
关键是 `#[test]` 属性。
它让构建系统发现这类函数，
并把它们当作测试运行，
验证它们不会 panic。

<aside class="exercise">

**读者练习：**
让这个测试通过。

你最终应得到类似下面的输出：

```text
running 1 test
test check_answer_validity ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

</aside>

我们已经看到*如何*写测试，
还需要弄清测*什么*。
如你所见，为函数写断言
只需很少代码，
但 CLI 应用往往不止一个函数！
更糟的是，它常常要处理用户输入、
读文件、
写输出。

## 让代码可测试 {#making-your-code-testable}

测试功能有两种互补的方法。一种是
测试用来构建完整应用的那些小单元。
这些叫做“单元测试”。
另一种是从外部测试最终应用，
称为黑盒测试或集成测试。
我们先从第一种开始。

要弄清该测什么，
先看看程序有哪些功能。
`grrs` 应打印匹配给定模式的行，
所以我们就为*这一点*写单元测试。
我们要确保最重要的那段逻辑能工作，
并且方式不依赖于
周围那些设置代码，
比如 CLI 参数。

回到我们 `grrs` 的[第一次实现](03-first-implementation/)，
我们在 `main` 函数里加了这段代码：

```rust,ignore
// ...
for line in content.lines() {
    if line.contains(&args.pattern) {
        println!("{}", line);
    }
}
```

遗憾的是，这不太好测。
首先，它在 main 函数里，没法轻易调用。
解决办法是把这段代码挪进一个函数：

```rust,no_run
fn find_matches(content: &str, pattern: &str) {
    for line in content.lines() {
        if line.contains(pattern) {
            println!("{}", line);
        }
    }
}
```

现在可以在测试里调用这个函数，
看看它的输出是什么：

```rust,ignore
#[test]
fn find_a_match() {
    find_matches("lorem ipsum\ndolor sit amet", "lorem");
    assert_eq!( // 呃呃呃
```

或者说……能吗？
现在 `find_matches` 直接打印到 `stdout`，也就是终端。
测试里没法轻易捕获！
这在实现之后再写测试时经常出现：
我们写了一个牢牢嵌在使用上下文中的函数。

<aside class="note">

**说明：**
写小型 CLI 应用时完全没问题。
没必要让一切都可测！
重要的是想清楚
代码里哪些部分可能想写单元测试。
虽然我们会看到改这个函数使其可测很直接，
但并非总是如此。

</aside>

好，怎样让它可测？
我们需要以某种方式捕获输出。
Rust 标准库有一些处理 I/O（输入/输出）的漂亮抽象，
我们会用到其中一个：[`std::io::Write`]。
这是一个[trait][trpl-traits]，抽象了我们可以写入的东西，
包括字符串和 `stdout`。

[trpl-traits]: https://doc.rust-lang.org/book/ch10-02-traits.html
[`std::io::Write`]: https://doc.rust-lang.org/1.39.0/std/io/trait.Write.html

如果这是你第一次在 Rust 语境中听到 “trait”，
那你会有收获。
Trait 是 Rust 最强大的特性之一。
你可以把它想成 Java 里的接口，
或 Haskell 里的类型类，
取决于你更熟悉哪个。
它们让你抽象可由不同类型共享的行为。
使用 trait 的代码能
以非常通用、灵活的方式表达想法。
这也意味着它可能变得难读。
别被吓到。
即使使用 Rust 多年的人
也不总能立刻看懂泛型代码。
那种情况下，
想想具体用法会有帮助。
在我们的例子里，
抽象的行为是“写入它”。
实现（`impl`）它的类型示例
包括终端标准输出、
文件、
内存中的缓冲区，
或 TCP 网络连接。
在 [`std::io::Write` 的文档][`std::io::Write`]里向下滚动，
可以看到 “Implementors” 列表。

有了这些知识，
让我们给函数加第三个参数。
它可以是任意实现了 `Write` 的类型。
这样，
测试里可以提供一个简单的字符串（缓冲区），
并对它做断言。
下面是我们如何写出这个版本的 `find_matches`：

```rust
fn find_matches(content: &str, pattern: &str, mut writer: impl std::io::Write) {
    for line in content.lines() {
        if line.contains(pattern) {
            writeln!(writer, "{}", line);
        }
    }
}
```

新参数是 `mut writer`，
即一个可变的、我们称为 “writer” 的东西。
其类型是 `impl std::io::Write`，
可以读作
任意实现了 `Write` trait 的类型的占位符。
注意我们把早先用的 `println!(…)`
换成了 `writeln!(writer, …)`。
`println!` 与 `writeln!` 工作方式相同，
但它总是使用标准输出。

现在可以对输出做断言了：

```rust
#[test]
fn find_a_match() {
    let mut result = Vec::new();
    find_matches("lorem ipsum\ndolor sit amet", "lorem", &mut result);
    assert_eq!(result, b"lorem ipsum\n");
}
```

要在应用代码里使用它，
需要改 `main` 里对 `find_matches` 的调用，
加上第三个参数 [`&mut std::io::stdout()`][stdout]。
下面是一个 `main` 函数示例，
建立在前几章所见内容之上，
并使用我们抽出的 `find_matches` 函数：

```rust
fn main() -> Result<()> {
    let args = Cli::parse();
    let content = std::fs::read_to_string(&args.path)
        .with_context(|| format!("could not read file `{}`", args.path.display()))?;

    find_matches(&content, &args.pattern, &mut std::io::stdout());

    Ok(())
}
```

[stdout]: https://doc.rust-lang.org/1.39.0/std/io/fn.stdout.html

<aside class="note">

**说明：**
因为 `stdout` 期望字节（不是字符串），
我们使用 `std::io::Write` 而不是 `std::fmt::Write`。
结果是，
测试里给一个空向量作为 `writer`
（其类型会被推断为 `Vec<u8>`），
在 `assert_eq!` 里使用 `b"foo"`。
`b` 前缀使其成为*字节字符串字面量*，
因此类型是 `&[u8]` 而不是 `&str`。

</aside>

<aside class="note">

**说明：**
我们也可以让这个函数返回 `String`，
但那会改变它的行为。
它就不再直接写到终端，
而是把一切收集进字符串，
最后一次性倾倒所有结果。

</aside>

<aside class="exercise">

**读者练习：**
[`writeln!`] 返回 [`io::Result`]，
因为写入可能失败
（例如缓冲区已满且无法扩展）。
为 `find_matches` 添加错误处理。

[`writeln!`]: https://doc.rust-lang.org/1.39.0/std/macro.writeln.html
[`io::Result`]: https://doc.rust-lang.org/1.39.0/std/io/type.Result.html

</aside>

我们刚看到如何让这段代码可测。我们：

1. 识别出应用的核心部分之一。
2. 把它放进自己的函数。
3. 让它更灵活。

尽管目标是可测，
最终得到的结果
其实是一段非常符合惯用、可复用的 Rust 代码。
太棒了！

## 把代码拆成库与二进制目标 {#splitting-your-code-into-library-and-binary-targets}

这里还能再做一件事。
到目前为止，我们写的一切都在 `src/main.rs` 里。
这意味着当前项目只产出一个二进制，
但我们也可以这样把代码作为库提供：

1. 把 `find_matches` 函数放进新的 `src/lib.rs`。
2. 在 `fn` 前加 `pub`，让库的用户能访问
   （即 `pub fn find_matches`）。
3. 从 `src/main.rs` 移除 `find_matches`。
4. 在 `fn main` 里，给 `find_matches` 的调用加上 `grrs::` 前缀，
   变成 `grrs::find_matches(…)`。
   这意味着使用我们刚写的库里的函数！

Rust 处理项目的方式相当灵活，
早点想清楚
把什么放进 crate 的库部分是个好主意。
例如，你可以先为应用特定逻辑写一个库，
再像用其它库一样在 CLI 里使用它。
或者，若项目有多个二进制，
可以把公共功能放进该 crate 的库部分。

<aside class="note">

**说明：**
说到把一切都塞进 `src/main.rs`，
若继续这样，
会变得难读。
[模块系统]可以帮助你组织和结构化代码。

[模块系统]: https://doc.rust-lang.org/1.39.0/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html

</aside>


## 通过运行来测试 CLI 应用 {#testing-cli-applications-by-running-them}

到目前为止，我们费力测试的是应用的*业务逻辑*，
结果就是 `find_matches` 函数。
这很有价值，
也是迈向充分测试代码库的很好一步。
这类测试通常叫做“单元测试”。

还有很多代码我们没测：
所有为与外部世界交互而写的东西！
想象你写了 main 函数，
却不小心留了一个硬编码字符串，
而不是使用用户提供的路径参数。
我们也该为此写测试！
这一层测试常称为
集成测试或系统测试。

其核心仍是写函数，
并用 `#[test]` 标注它们。
差别只在于函数里做什么。
例如，我们会想用项目的主二进制，
像普通程序一样运行它。
我们会把这些测试放进新目录下的新文件：
`tests/cli.rs`。

<aside>

**说明：**
按约定，
`cargo` 会在 `tests/` 目录寻找集成测试。
类似地，
会在 `benches/` 找基准，
在 `examples/` 找示例。
这些约定也延伸到主源码：
库有 `src/lib.rs`，
主二进制是 `src/main.rs`，
若有多个二进制，
cargo 期望它们在 `src/bin/<name>.rs`。
遵循这些约定会让习惯阅读 Rust 代码的人
更容易发现你的代码库。

</aside>

`grrs` 是在文件中搜索字符串的小工具。
我们已经测过能找到匹配。
再想想还能测哪些功能。

我想出了这些：

- 文件不存在时会发生什么？
- 没有匹配时输出是什么？
- 忘了一个（或两个）参数时，程序是否以错误退出？

这些都是有效的测试用例。
此外，
还应包含一个成功路径的用例：
我们至少找到一个匹配，
并打印出来。

为让这类测试更容易，
我们将使用 [`assert_cmd`] crate。
它有许多便捷助手，
让我们能运行主二进制
并观察其行为。
我们还会加上 [`predicates`] crate，
它帮助我们编写断言，
供 `assert_cmd` 检验，
并带有很好的错误消息。
这些依赖不会加到主依赖列表，
而是加到 `Cargo.toml` 的 `dev-dependencies` 段。
它们只在开发 crate 时需要，
使用时不需要。

```toml
[dev-dependencies]
assert_cmd = "2.0.14"
predicates = "3.1.0"
```

[`assert_cmd`]: https://docs.rs/assert_cmd
[`predicates`]: https://docs.rs/predicates

听起来准备不少。
不过，
我们直接动手，
创建 `tests/cli.rs` 文件：

```rust
use assert_cmd::cargo::*; // 导入 cargo_bin_cmd! 宏与方法
use predicates::prelude::*; // 用于编写断言

#[test]
fn file_doesnt_exist() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = cargo_bin_cmd!("grrs");

    cmd.arg("foobar").arg("test/file/doesnt/exist");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("could not read file"));

    Ok(())
}

```

你可以用
`cargo test` 运行这个测试，
和上面写的测试一样。
第一次可能稍慢一些，
因为 `Command::cargo_bin("grrs")` 需要编译主二进制。

## 生成测试文件 {#generating-test-files}

我们刚看到的测试只检查：输入文件不存在时，
程序会写出错误消息。
这是重要的测试，
但也许不是最重要的。
让我们测试：是否真的会打印在文件中找到的匹配！

我们需要一份内容已知的文件，
才能知道程序*应当*返回什么，
并在代码里检查这一期望。
一个想法是向项目添加带自定义内容的文件，
并在测试中使用。
另一个是在测试中创建临时文件。
本教程中，
我们看看后一种做法。
它更灵活，也适用于其它情况；
例如，测试会修改文件的程序时。

要创建这些临时文件，
我们将使用 [`assert_fs`] crate。
把它加到 `Cargo.toml` 的 `dev-dependencies`：

```toml
assert_fs = "1.1.1"
```

[`assert_fs`]: https://docs.rs/assert_fs

下面是一个新测试用例：
创建临时文件
（“具名”以便拿到路径），
填入一些文本，
然后运行程序，
看是否得到正确输出。
可以写在另一个测试用例下面。
当变量 `file` 在函数末尾离开作用域时，
实际的临时文件会自动删除。

```rust
#[test]
fn find_content_in_file() -> Result<(), Box<dyn std::error::Error>> {
    let file = assert_fs::NamedTempFile::new("sample.txt")?;
    file.write_str("A test\nActual content\nMore content\nAnother test")?;

    let mut cmd = cargo_bin_cmd!("grrs");
    cmd.arg("test").arg(file.path());
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("A test\nAnother test"));

    Ok(())
}
```

<aside class="exercise">

**读者练习：**
为传入空字符串作为模式添加集成测试。
按需调整程序。

</aside>

## 测什么？ {#what-to-test}

虽然写集成测试确实挺有趣，
但写它们要花时间，
应用行为变化时更新它们也要时间。
为确保时间用得明智，
应问问自己该测什么。

一般来说，为用户可观察的各类行为
写集成测试是个好主意。
这意味着不必覆盖所有边界情况。
通常有各类行为的示例就够了，
边界情况交给单元测试。

最好也不要把测试焦点放在你无法主动控制的事情上。
测试 `--help` 的精确布局会是个坏主意，
因为它是替你生成的。
相反，你可能只想检查某些元素是否存在。

取决于程序的性质，
你也可以尝试加入更多测试技术。
例如，
如果你抽出了程序的一些部分，
发现自己在写大量示例用例作单元测试，
同时试图想出所有边界情况，
就该看看 [`proptest`]。
如果你有消费任意文件并解析它们的程序，
试着写一个[模糊测试器][fuzzer]来找边界情况里的 bug。

[`proptest`]: https://docs.rs/proptest
[fuzzer]: https://rust-fuzz.github.io/book/introduction.html

<aside>

**说明：**
本章所用的完整可运行源码
可在[本书仓库][src]中找到。

[src]: https://github.com/rust-cli/book/tree/master/src/tutorial/testing

</aside>
