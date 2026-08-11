+++
title = "12.4 用测试驱动开发增加功能"
date = 2026-08-05T08:44:00+08:00
weight = 53
type = "docs"
description = "用 TDD 实现 search 函数并验证搜索行为"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用测试驱动开发增加功能


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-04-testing-the-librarys-functionality.html](https://doc.rust-lang.org/stable/book/ch12-04-testing-the-librarys-functionality.html)


## 用测试驱动开发增加功能

　　既然搜索逻辑已放在 *src/lib.rs* 中、与 `main` 分离，为核心功能写测试就容易多了。我们可以直接用各种参数调用函数并检查返回值，而不必从命令行调用二进制。

　　本节用测试驱动开发（test-driven development，TDD）为 `minigrep` 添加搜索逻辑，步骤如下：

1. 写一个会失败的测试并运行，确认它因你预期的原因失败。
2. 编写或修改刚好够让新测试通过的代码。
3. 重构刚添加或修改的代码，并确保测试继续通过。
4. 从第 1 步重复！

　　TDD 只是众多写软件的方式之一，但它有助于推动代码设计。先写测试再写让测试通过的代码，有助于在整个过程中保持较高的测试覆盖率。

　　我们将用测试驱动实现真正在文件内容中搜索查询字符串、并产生匹配行列表的功能。该功能放在名为 `search` 的函数中。

### 编写失败的测试

　　在 *src/lib.rs* 中，像 [第 11 章][ch11-anatomy] 那样添加带测试函数的 `tests` 模块。测试函数规定我们希望 `search` 具备的行为：接收查询与待搜索文本，只返回文本中包含查询的那些行。示例 12-15 展示了该测试。

**文件名：`src/lib.rs`**
```rust
// --snip--

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}
```

**示例 12-15：为期望拥有的 `search` 功能创建失败测试**

　　该测试搜索字符串 `"duct"`。待搜索文本有三行，其中只有一行包含 `"duct"`（注意开头双引号后的反斜杠告诉 Rust 不要在这个字符串字面量内容开头放换行符）。我们断言 `search` 返回的值只包含预期的那一行。

　　若现在运行测试，会失败，因为 `unimplemented!` 宏会以 “not implemented” 消息 panic。按照 TDD 原则，先迈一小步：给 `search` 定义成总是返回空向量，让调用时不再 panic，如示例 12-16。然后测试应能编译，但因空向量不等于包含 `"safe, fast, productive."` 的向量而失败。

**文件名：`src/lib.rs`**
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    vec![]
}
```

**示例 12-16：定义刚好够让调用不 panic 的 `search`**

　　现在讨论为何要在 `search` 的签名中显式定义生命周期 `'a`，并把它用于 `contents` 参数和返回值。回顾 [第 10 章][ch10-lifetimes]：生命周期参数指明哪个参数的生命周期与返回值的生命周期相关联。这里我们表明：返回的向量应包含引用参数 `contents` 中切片的字符串切片（而不是参数 `query`）。

　　换句话说，我们告诉 Rust：`search` 返回的数据存活时间与传入的 `contents` 参数中的数据一样长。这很重要！切片*所引用*的数据必须在引用有效期间保持有效；若编译器误以为我们在对 `query` 而不是 `contents` 做字符串切片，安全检查就会出错。

　　若忘记生命周期标注就编译该函数，会得到这样的错误：

```console
$ cargo build
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
error[E0106]: missing lifetime specifier
 --> src/lib.rs:1:51
  |
1 | pub fn search(query: &str, contents: &str) -> Vec<&str> {
  |                      ----            ----         ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `query` or `contents`
help: consider introducing a named lifetime parameter
  |
1 | pub fn search<'a>(query: &'a str, contents: &'a str) -> Vec<&'a str> {
  |              ++++         ++                 ++              ++

For more information about this error, try `rustc --explain E0106`.
error: could not compile `minigrep` (lib) due to 1 previous error
```

　　Rust 无法知道输出需要依赖两个参数中的哪一个，因此必须显式告知。注意帮助文本建议给所有参数和输出类型指定相同生命周期参数——那是错的！因为 `contents` 才包含全部文本，我们要返回其中匹配的部分，所以只有 `contents` 应通过生命周期语法与返回值关联。

　　其他编程语言不要求在签名中把参数与返回值关联起来，但这种做法会随时间变得越来越自然。你可以把本例与第 10 章 [「用生命周期校验引用」][validating-references-with-lifetimes] 一节中的例子对照阅读。

### 编写使测试通过的代码

　　目前测试失败是因为我们总返回空向量。要修复并实现 `search`，程序需要按下列步骤进行：

1. 遍历内容的每一行。
2. 检查该行是否包含查询字符串。
3. 若包含，加入要返回的列表。
4. 若不包含，什么也不做。
5. 返回匹配结果列表。

　　我们逐步实现，从遍历各行开始。

#### 用 `lines` 方法遍历各行

　　Rust 有一个便于按行迭代字符串的方法，名字正好叫 `lines`，用法如示例 12-17。注意此时尚无法编译。

**文件名：`src/lib.rs`**
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    for line in contents.lines() {
        // do something with line
    }
}
```

**示例 12-17：遍历 `contents` 中的每一行**

　　`lines` 方法返回一个迭代器。第 13 章会深入讨论迭代器。不过回想 [示例 3-5][ch3-iter]，你已见过用 `for` 循环配合迭代器对集合中每一项执行代码的写法。

#### 在每一行中搜索查询

　　接下来检查当前行是否包含查询字符串。幸好字符串有一个很方便的 `contains` 方法！在 `search` 中加入对 `contains` 的调用，如示例 12-18。注意此时仍无法编译。

**文件名：`src/lib.rs`**
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    for line in contents.lines() {
        if line.contains(query) {
            // do something with line
        }
    }
}
```

**示例 12-18：增加检查行是否包含 `query` 中字符串的功能**

　　此刻我们还在搭建功能。要让代码编译，需要按函数签名所声明的那样从函数体返回一个值。

#### 存储匹配的行

　　要完成该函数，需要一种方式存储想返回的匹配行。可以在 `for` 循环前创建一个可变向量，用 `push` 把 `line` 存进去；循环结束后返回该向量，如示例 12-19。

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

**示例 12-19：存储匹配的行以便返回**

　　现在 `search` 应只返回包含 `query` 的行，测试应通过。运行测试：

```console
$ cargo test
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.22s
     Running unittests src/lib.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 1 test
test tests::one_result ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests minigrep

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　测试通过了，说明它能工作！

　　此时可以考虑在保持测试通过、功能不变的前提下重构 `search` 的实现。当前代码不算差，但还没用上迭代器的一些有用特性。我们会在 [第 13 章][ch13-iterators] 回到这个例子，深入探索迭代器并改进它。

　　现在整个程序应该能工作了！先试一个在艾米莉·狄金森诗中应正好返回一行的词：*frog*。

```console
$ cargo run -- frog poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.38s
     Running `target/debug/minigrep frog poem.txt`
How public, like a frog
```

　　不错！再试一个会匹配多行的词，比如 *body*：

```console
$ cargo run -- body poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep body poem.txt`
I'm nobody! Who are you?
Are you nobody, too?
How dreary to be somebody!
```

　　最后确认：搜索诗中不存在的词（例如 *monomorphization*）时不应得到任何行：

```console
$ cargo run -- monomorphization poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep monomorphization poem.txt`
```

　　出色！我们构建了经典工具的迷你版，并学到许多如何组织应用的知识，也接触了文件输入输出、生命周期、测试和命令行解析。

　　为完善本项目，我们还将简要演示如何使用环境变量，以及如何打印到标准错误——两者在编写命令行程序时都很有用。

[validating-references-with-lifetimes]: ../../generics/03-lifetime-syntax/#validating-references-with-lifetimes
[ch11-anatomy]: ../../testing/01-writing-tests/#the-anatomy-of-a-test-function
[ch10-lifetimes]: ../../generics/03-lifetime-syntax/
[ch3-iter]: ../../common-programming-concepts/05-control-flow/#looping-through-a-collection-with-for
[ch13-iterators]: ../../functional-features/02-iterators/
