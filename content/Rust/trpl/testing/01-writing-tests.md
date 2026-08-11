+++
title = "11.1 如何编写测试"
date = 2026-08-05T08:44:00+08:00
weight = 46
type = "docs"
description = "用 assert、should_panic 与 Result 编写测试"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 如何编写测试


> 原文链接: [https://doc.rust-lang.org/stable/book/ch11-01-writing-tests.html](https://doc.rust-lang.org/stable/book/ch11-01-writing-tests.html)


## 如何编写测试 {#how-to-write-tests}

　　*测试*是验证非测试代码是否按预期工作的 Rust 函数。测试函数的函数体通常执行这三步：

- 准备所需的任何数据或状态。
- 运行要测试的代码。
- 断言结果符合预期。

　　我们来看看 Rust 专门为编写执行这些操作的测试所提供的特性，包括 `test` 属性、若干宏，以及 `should_panic` 属性。

### 组织测试函数 {#the-anatomy-of-a-test-function}

　　最简单地说，Rust 中的测试就是用 `test` 属性标注的函数。属性是关于 Rust 代码片段的元数据；一个例子是我们在第 5 章与结构体一起使用的 `derive` 属性。要把函数变成测试函数，在 `fn` 前一行加上 `#[test]`。用 `cargo test` 命令运行测试时，Rust 会构建一个测试运行器二进制：它运行被标注的函数，并报告每个测试函数是通过还是失败。

　　每当我们用 Cargo 新建库项目时，都会自动为我们生成一个带有测试函数的测试模块。该模块为编写测试提供模板，这样你就不必每次开始新项目时都去查确切的结构与语法。你可以按需添加任意多个额外的测试函数与测试模块！

　　在真正测试任何代码之前，我们先通过试验模板测试来探索测试如何工作的一些方面。然后，我们会编写一些真实世界的测试：调用我们写的代码，并断言其行为正确。

　　我们创建一个名为 `adder`、用于把两个数相加的新库项目：

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

　　你的 `adder` 库中 _src/lib.rs_ 文件的内容应如示例 11-1 所示。

**文件名：`src/lib.rs`**

```rust
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

**示例 11-1：由 `cargo new` 自动生成的代码**


　　文件以示例 `add` 函数开头，以便我们有东西可测。

　　眼下我们只关注 `it_works` 函数。注意 `#[test]` 注解：该属性表明这是测试函数，因此测试运行器知道要把该函数当作测试对待。`tests` 模块中也可能有非测试函数，用于设置常见场景或执行常见操作，因此我们总需要指明哪些函数是测试。

　　示例函数体使用 `assert_eq!` 宏断言：`result`（调用 `add` 传入 2 与 2 的结果）等于 4。这个断言充当典型测试格式的示例。我们运行一下，看看这个测试是否通过。

　　`cargo test` 命令会运行项目中的所有测试，如示例 11-2 所示。

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.57s
     Running unittests src/lib.rs (target/debug/deps/adder-01ad14159ff659ab)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

**示例 11-2：运行自动生成测试的输出**

　　Cargo 编译并运行了测试。我们看到一行 `running 1 test`。下一行显示生成的测试函数名 `tests::it_works`，以及运行该测试的结果是 `ok`。总体摘要 `test result: ok.` 表示所有测试都通过了，而 `1 passed; 0 failed` 汇总了通过或失败的测试数量。

　　可以把测试标为忽略，使其在特定情况下不运行；我们会在本章稍后的[「除非特别请求，否则忽略测试」][ignoring]一节中介绍。因为这里还没这么做，摘要显示 `0 ignored`。我们也可以向 `cargo test` 命令传递参数，只运行名称匹配某字符串的测试；这叫做*筛选（filtering）*，我们会在[「按名称运行测试子集」][subset]一节中介绍。这里我们没有筛选正在运行的测试，因此摘要末尾显示 `0 filtered out`。

　　`0 measured` 统计用于测量性能的基准测试。截至撰写时，基准测试仅在 nightly Rust 中可用。更多信息见[关于基准测试的文档][bench]。

　　测试输出中从 `Doc-tests adder` 开始的下一部分是任何文档测试的结果。我们还没有任何文档测试，但 Rust 可以编译出现在 API 文档中的任何代码示例。这一特性有助于让文档与代码保持同步！我们将在第 14 章[「把文档注释当作测试」][doc-comments]一节讨论如何编写文档测试。眼下我们忽略 `Doc-tests` 输出。

　　我们开始按自己的需要定制测试。首先，把 `it_works` 函数名改成不同的名字，例如 `exploration`，像这样：

<span class="filename">文件名：src/lib.rs</span>

```rust
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exploration() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

　　然后再次运行 `cargo test`。输出现在显示 `exploration` 而不是 `it_works`：

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.59s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::exploration ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　现在我们再添加一个测试，但这次故意让它失败！测试函数中有东西 panic 时，测试就会失败。每个测试在新线程中运行；当主线程看到某个测试线程已死，该测试就被标为失败。第 9 章我们讲过，引发 panic 最简单的方式是调用 `panic!` 宏。把新测试写成名为 `another` 的函数，使你的 _src/lib.rs_ 文件如示例 11-3 所示。

**文件名：`src/lib.rs`**
```rust
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exploration() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    fn another() {
        panic!("Make this test fail");
    }
}
```

**示例 11-3：添加第二个会因调用 `panic!` 宏而失败的测试**

　　再次用 `cargo test` 运行测试。输出应如示例 11-4 所示：我们的 `exploration` 测试通过，`another` 失败。

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.72s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 2 tests
test tests::another ... FAILED
test tests::exploration ... ok

failures:

---- tests::another stdout ----

thread 'tests::another' (6019162) panicked at src/lib.rs:17:9:
Make this test fail
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::another

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

**示例 11-4：一个测试通过、一个测试失败时的测试结果**


　　`test tests::another` 那一行显示的是 `FAILED` 而不是 `ok`。在各个结果与摘要之间出现了两个新部分：第一部分显示每个测试失败的详细原因。本例中，细节是 `tests::another` 失败，因为它在 _src/lib.rs_ 文件第 17 行以消息 `Make this test fail` panic。下一部分只列出所有失败测试的名称，在测试很多、失败详情输出也很多时很有用。我们可以用失败测试的名称只运行该测试，以便更容易调试；更多运行测试的方式见[「控制测试的运行方式」][controlling-how-tests-are-run]一节。

　　摘要行显示在最后：总体而言，我们的测试结果是 `FAILED`。有一个测试通过，一个测试失败。

　　既然已经看过不同场景下的测试结果长什么样，我们再看看除 `panic!` 以外在测试中有用的一些宏。

### 用 `assert!` 检查结果

　　标准库提供的 `assert!` 宏在你想确保测试中某个条件求值为 `true` 时很有用。我们给 `assert!` 宏一个求值为布尔值的参数。若值为 `true`，什么都不发生，测试通过；若为 `false`，`assert!` 宏调用 `panic!` 使测试失败。使用 `assert!` 宏有助于检查代码是否按我们的意图工作。

　　第 5 章示例 5-15 中我们用过 `Rectangle` 结构体与 `can_hold` 方法，此处在示例 11-5 中重现。我们把这段代码放进 _src/lib.rs_ 文件，再用 `assert!` 宏为它写一些测试。

**文件名：`src/lib.rs`**
```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

**示例 11-5：第 5 章的 `Rectangle` 结构体及其 `can_hold` 方法**

　　`can_hold` 方法返回布尔值，因此非常适合用 `assert!` 宏。在示例 11-6 中，我们写一个测试来锻炼 `can_hold`：创建一个宽为 8、高为 7 的 `Rectangle` 实例，并断言它能容纳另一个宽为 5、高为 1 的 `Rectangle` 实例。

**文件名：`src/lib.rs`**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn larger_can_hold_smaller() {
        let larger = Rectangle {
            width: 8,
            height: 7,
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };

        assert!(larger.can_hold(&smaller));
    }
}
```

**示例 11-6：检查较大矩形是否确实能容纳较小矩形的 `can_hold` 测试**

　　注意 `tests` 模块内的 `use super::*;` 一行。`tests` 模块是普通模块，遵循我们在第 7 章[「模块树中引用条目的路径」][paths-for-referring-to-an-item-in-the-module-tree]一节中介绍的常规可见性规则。因为 `tests` 是内部模块，需要把外层模块中被测代码引入内层模块的作用域。这里我们使用 glob，因此外层模块中定义的任何东西都对该 `tests` 模块可用。

　　我们把测试命名为 `larger_can_hold_smaller`，并创建了所需的两个 `Rectangle` 实例。然后调用 `assert!` 宏，并把调用 `larger.can_hold(&smaller)` 的结果传给它。该表达式应返回 `true`，因此我们的测试应通过。来验证一下！

```console
$ cargo test
   Compiling rectangle v0.1.0 (file:///projects/rectangle)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/rectangle-6584c4561e48942e)

running 1 test
test tests::larger_can_hold_smaller ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests rectangle

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　确实通过了！我们再添加另一个测试，这次断言较小矩形不能容纳较大矩形：

<span class="filename">文件名：src/lib.rs</span>

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn larger_can_hold_smaller() {
        // --snip--

    }

    #[test]
    fn smaller_cannot_hold_larger() {
        let larger = Rectangle {
            width: 8,
            height: 7,
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };

        assert!(!smaller.can_hold(&larger));
    }
}
```

　　因为此时 `can_hold` 函数的正确结果是 `false`，我们需要在把它传给 `assert!` 宏之前取反。这样，若 `can_hold` 返回 `false`，我们的测试就会通过：

```console
$ cargo test
   Compiling rectangle v0.1.0 (file:///projects/rectangle)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/rectangle-6584c4561e48942e)

running 2 tests
test tests::larger_can_hold_smaller ... ok
test tests::smaller_cannot_hold_larger ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests rectangle

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　两个测试都通过了！现在看看在代码中引入 bug 时测试结果会怎样。我们改 `can_hold` 方法的实现：比较宽度时把大于号（`>`）换成小于号（`<`）：

```rust
// --snip--
impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width < other.width && self.height > other.height
    }
}
```

　　现在运行测试会产生如下结果：

```console
$ cargo test
   Compiling rectangle v0.1.0 (file:///projects/rectangle)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/rectangle-6584c4561e48942e)

running 2 tests
test tests::larger_can_hold_smaller ... FAILED
test tests::smaller_cannot_hold_larger ... ok

failures:

---- tests::larger_can_hold_smaller stdout ----

thread 'tests::larger_can_hold_smaller' (6020788) panicked at src/lib.rs:28:9:
assertion failed: larger.can_hold(&smaller)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::larger_can_hold_smaller

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　我们的测试抓住了这个 bug！因为 `larger.width` 是 `8`，`smaller.width` 是 `5`，`can_hold` 中对宽度的比较现在返回 `false`：8 并不小于 5。

### 用 `assert_eq!` 与 `assert_ne!` 测试相等性

　　验证功能的常见方式是：测试被测代码的结果是否等于你期望它返回的值。你可以用 `assert!` 宏并传入使用 `==` 运算符的表达式来做到这一点。不过这种测试太常见，标准库提供了一对宏——`assert_eq!` 与 `assert_ne!`——以便更方便地执行。这两个宏分别比较两个参数是否相等或不相等。断言失败时，它们还会打印这两个值，从而更容易看出测试*为何*失败；相比之下，`assert!` 宏只表明 `==` 表达式得到了 `false`，而不打印导致 `false` 的那些值。

　　在示例 11-7 中，我们编写名为 `add_two` 的函数，把它的参数加 `2`，再用 `assert_eq!` 宏测试该函数。

**文件名：`src/lib.rs`**
```rust
pub fn add_two(a: u64) -> u64 {
    a + 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_adds_two() {
        let result = add_two(2);
        assert_eq!(result, 4);
    }
}
```

**示例 11-7：用 `assert_eq!` 宏测试函数 `add_two`**

　　来确认它能通过！

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　我们创建变量 `result`，保存调用 `add_two(2)` 的结果。然后把 `result` 与 `4` 作为参数传给 `assert_eq!` 宏。该测试的输出行是 `test tests::it_adds_two ... ok`，其中的 `ok` 表示测试通过！

　　我们在代码中引入一个 bug，看看 `assert_eq!` 失败时是什么样。把 `add_two` 的实现改成加 `3`：

```rust
pub fn add_two(a: u64) -> u64 {
    a + 3
}
```

　　再次运行测试：

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::it_adds_two ... FAILED

failures:

---- tests::it_adds_two stdout ----

thread 'tests::it_adds_two' (6020955) panicked at src/lib.rs:12:9:
assertion `left == right` failed
  left: 5
 right: 4
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::it_adds_two

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　我们的测试抓住了这个 bug！`tests::it_adds_two` 测试失败了，消息告诉我们失败的断言是 `left == right`，以及 `left` 与 `right` 的值分别是什么。这条消息有助于开始调试：`left` 参数（调用 `add_two(2)` 的结果）是 `5`，而 `right` 参数是 `4`。可以想象，在有很多测试时这会特别有帮助。

　　注意：在某些语言与测试框架中，相等性断言函数的参数叫做 `expected` 与 `actual`，且参数顺序很重要。但在 Rust 中，它们叫做 `left` 与 `right`，我们指定期望值与代码产生值的顺序并不重要。可以把这个测试中的断言写成 `assert_eq!(4, result)`，失败消息同样会显示 `` assertion `left == right` failed ``。

　　若我们给 `assert_ne!` 的两个值不相等，它会通过；若相等则会失败。该宏在我们不确定值*会是*什么、但知道值绝*不应该是*什么时最有用。例如，若测试某个保证会以某种方式改变输入的函数，但改变方式取决于运行测试的星期几，最好断言的或许是：函数输出不等于输入。

　　实际上，`assert_eq!` 与 `assert_ne!` 宏分别使用运算符 `==` 与 `!=`。断言失败时，这些宏用调试格式打印其参数，这意味着被比较的值必须实现 `PartialEq` 与 `Debug` trait。所有原始类型以及多数标准库类型都实现了这些 trait。对于你自己定义的结构体与枚举，需要实现 `PartialEq` 才能断言这些类型相等，还需要实现 `Debug` 以便在断言失败时打印值。因为这两个 trait 都是可派生 trait（第 5 章示例 5-12 提过），通常只需在结构体或枚举定义上加上 `#[derive(PartialEq, Debug)]` 注解。关于这些及其他可派生 trait 的更多细节，见附录 C [「可派生的 Trait」][derivable-traits]。

### 添加自定义失败消息

　　你也可以为 `assert!`、`assert_eq!` 与 `assert_ne!` 宏添加可选参数，作为与失败消息一起打印的自定义消息。必需参数之后指定的任何参数都会传给 `format!` 宏（第 8 章[「用 `+` 运算符或 `format!` 宏拼接」][concatenating]中讨论过），因此你可以传入包含 `{}` 占位符的格式字符串以及填入这些占位符的值。自定义消息有助于记录断言的含义；测试失败时，你会更清楚代码出了什么问题。

　　例如，假设我们有一个按名字问候人的函数，并想测试传入函数的名字会出现在输出中：

<span class="filename">文件名：src/lib.rs</span>

```rust
pub fn greeting(name: &str) -> String {
    format!("Hello {name}!")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greeting_contains_name() {
        let result = greeting("Carol");
        assert!(result.contains("Carol"));
    }
}
```

　　这个程序的需求尚未谈妥，而且我们相当确定问候语开头的 `Hello` 文本会变。我们决定不想在需求变化时更新测试，因此与其检查与 `greeting` 函数返回值完全相等，不如只断言输出包含输入参数的文本。

　　现在我们通过改 `greeting` 以排除 `name` 来引入一个 bug，看看默认的测试失败是什么样：

```rust
pub fn greeting(name: &str) -> String {
    String::from("Hello!")
}
```

　　运行该测试会产生如下结果：

```console
$ cargo test
   Compiling greeter v0.1.0 (file:///projects/greeter)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.91s
     Running unittests src/lib.rs (target/debug/deps/greeter-170b942eb5bf5e3a)

running 1 test
test tests::greeting_contains_name ... FAILED

failures:

---- tests::greeting_contains_name stdout ----

thread 'tests::greeting_contains_name' (6021143) panicked at src/lib.rs:12:9:
assertion failed: result.contains("Carol")
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::greeting_contains_name

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　这个结果只表明断言失败以及断言所在行。更有用的失败消息会打印来自 `greeting` 函数的值。我们添加由格式字符串组成的自定义失败消息，并用从 `greeting` 函数实际得到的值填入占位符：

```rust
    #[test]
    fn greeting_contains_name() {
        let result = greeting("Carol");
        assert!(
            result.contains("Carol"),
            "Greeting did not contain name, value was `{result}`"
        );
    }
```

　　现在运行测试时，我们会得到更有信息量的错误消息：

```console
$ cargo test
   Compiling greeter v0.1.0 (file:///projects/greeter)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.93s
     Running unittests src/lib.rs (target/debug/deps/greeter-170b942eb5bf5e3a)

running 1 test
test tests::greeting_contains_name ... FAILED

failures:

---- tests::greeting_contains_name stdout ----

thread 'tests::greeting_contains_name' (6021333) panicked at src/lib.rs:12:9:
Greeting did not contain name, value was `Hello!`
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::greeting_contains_name

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　我们可以在测试输出中看到实际得到的值，这有助于调试发生了什么，而不是我们期望发生什么。

### 用 `should_panic` 检查 Panic

　　除了检查返回值，检查代码是否按我们期望的方式处理错误条件也很重要。例如，考虑第 9 章示例 9-13 中创建的 `Guess` 类型。使用 `Guess` 的其他代码依赖于这一保证：`Guess` 实例只包含 1 到 100 之间的值。我们可以写一个测试，确保尝试用该范围外的值创建 `Guess` 实例时会发生 panic。

　　做法是为测试函数添加属性 `should_panic`。若函数内的代码 panic，测试通过；若不 panic，测试失败。

　　示例 11-8 展示了一个测试：检查 `Guess::new` 的错误条件是否在我们期望时发生。

**文件名：`src/lib.rs`**
```rust
pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!("Guess value must be between 1 and 100, got {value}.");
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic]
    fn greater_than_100() {
        Guess::new(200);
    }
}
```

**示例 11-8：测试某个条件会引发 `panic!`**

　　我们把 `#[should_panic]` 属性放在 `#[test]` 属性之后、它所适用的测试函数之前。看看这个测试通过时的结果：

```console
$ cargo test
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running unittests src/lib.rs (target/debug/deps/guessing_game-57d70c3acb738f4d)

running 1 test
test tests::greater_than_100 - should panic ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests guessing_game

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　看起来不错！现在通过移除“值大于 100 时 `new` 会 panic”的条件，在代码中引入一个 bug：

```rust
// --snip--
impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 {
            panic!("Guess value must be between 1 and 100, got {value}.");
        }

        Guess { value }
    }
}
```

　　运行示例 11-8 中的测试时，它会失败：

```console
$ cargo test
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.62s
     Running unittests src/lib.rs (target/debug/deps/guessing_game-57d70c3acb738f4d)

running 1 test
test tests::greater_than_100 - should panic ... FAILED

failures:

---- tests::greater_than_100 stdout ----
note: test did not panic as expected at src/lib.rs:21:8

failures:
    tests::greater_than_100

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　这种情况下我们得不到很有帮助的消息，但看测试函数时会发现它标注了 `#[should_panic]`。我们得到的失败意味着：测试函数中的代码没有引发 panic。

　　使用 `should_panic` 的测试可能不够精确。即便测试因与我们期望不同的原因而 panic，`should_panic` 测试也会通过。为使 `should_panic` 测试更精确，可以为 `should_panic` 属性添加可选的 `expected` 参数。测试工具会确保失败消息包含所提供的文本。例如，考虑示例 11-9 中修改后的 `Guess` 代码：`new` 函数根据值过小还是过大会以不同消息 panic。

**文件名：`src/lib.rs`**
```rust
// --snip--

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 {
            panic!(
                "Guess value must be greater than or equal to 1, got {value}."
            );
        } else if value > 100 {
            panic!(
                "Guess value must be less than or equal to 100, got {value}."
            );
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "less than or equal to 100")]
    fn greater_than_100() {
        Guess::new(200);
    }
}
```

**示例 11-9：测试 `panic!` 的消息是否包含指定子串**

　　这个测试会通过，因为我们放在 `should_panic` 属性 `expected` 参数中的值是 `Guess::new` 函数 panic 消息的子串。我们本可以指定期望的完整 panic 消息，本例中会是 `Guess value must be less than or equal to 100, got 200`。选择指定多少取决于 panic 消息有多少是唯一或动态的，以及你希望测试有多精确。本例中，panic 消息的子串足以确保测试函数中的代码执行了 `else if value > 100` 分支。

　　要看带 `expected` 消息的 `should_panic` 测试失败时会怎样，我们再次通过交换 `if value < 1` 与 `else if value > 100` 块的函数体来引入 bug：

```rust
        if value < 1 {
            panic!(
                "Guess value must be less than or equal to 100, got {value}."
            );
        } else if value > 100 {
            panic!(
                "Guess value must be greater than or equal to 1, got {value}."
            );
        }
```

　　这次运行 `should_panic` 测试时，它会失败：

```console
$ cargo test
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/guessing_game-57d70c3acb738f4d)

running 1 test
test tests::greater_than_100 - should panic ... FAILED

failures:

---- tests::greater_than_100 stdout ----

thread 'tests::greater_than_100' (6021675) panicked at src/lib.rs:12:13:
Guess value must be greater than or equal to 1, got 200.
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
note: panic did not contain expected string
      panic message: "Guess value must be greater than or equal to 1, got 200."
 expected substring: "less than or equal to 100"

failures:
    tests::greater_than_100

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　失败消息表明：这个测试确实如我们期望那样 panic 了，但 panic 消息并未包含期望的字符串 `less than or equal to 100`。本例中我们实际得到的 panic 消息是 `Guess value must be greater than or equal to 1, got 200`。现在可以开始弄清 bug 在哪里了！

### 在测试中使用 `Result<T, E>`

　　到目前为止，我们的测试都在失败时 panic。我们也可以编写使用 `Result<T, E>` 的测试！下面是示例 11-1 中的测试改写成使用 `Result<T, E>`、在失败时返回 `Err` 而不是 panic 的版本：

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() -> Result<(), String> {
        let result = add(2, 2);

        if result == 4 {
            Ok(())
        } else {
            Err(String::from("two plus two does not equal four"))
        }
    }
}
```

　　`it_works` 函数现在的返回类型是 `Result<(), String>`。在函数体中，我们不再调用 `assert_eq!` 宏，而是在测试通过时返回 `Ok(())`，在失败时返回内含 `String` 的 `Err`。

　　把测试写成返回 `Result<T, E>`，就能在测试体中使用问号运算符：若其中任何操作返回 `Err` 变体，测试就应失败，这是一种便捷写法。

　　不能对使用 `Result<T, E>` 的测试使用 `#[should_panic]` 注解。要断言某个操作返回 `Err` 变体，*不要*对该 `Result<T, E>` 值使用问号运算符，而应使用 `assert!(value.is_err())`。

　　既然知道了几种编写测试的方式，接下来看看运行测试时发生了什么，并探索可与 `cargo test` 一起使用的不同选项。

[concatenating]: ../../common-collections/02-strings/#concatenating-with--or-format
[bench]: https://doc.rust-lang.org/unstable-book/library-features/test.html
[ignoring]: ../02-running-tests/#ignoring-tests-unless-specifically-requested
[subset]: ../02-running-tests/#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ../02-running-tests/
[derivable-traits]: ../../appendix/03-c-derivable-traits/
[doc-comments]: ../../more-about-cargo/02-publishing-to-crates-io/#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ../../modules/03-paths-for-referring-to-an-item-in-the-module-tree/
