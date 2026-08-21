+++
title = "59-测试"
date = 2026-08-21T12:46:00+08:00
weight = 60
type = "docs"
description = "测试 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_58.html](https://dhghomon.github.io/easy_rust/Chapter_58.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 测试

现在我们已经了解了模块,就可以谈谈测试了。在Rust中测试你的代码是非常容易的，因为你可以在你的代码旁边写测试。

开始测试的最简单的方法是在一个函数上面添加`#[test]`。下面是一个简单的例子。

```rust
#[test]
fn two_is_two() {
    assert_eq!(2, 2);
}
```

但如果你试图在playground中运行它，它给出了一个错误。``error[E0601]: `main` function not found in crate `playground``. 这是因为你不使用 _Run_ 来进行测试，你使用 _Test_ 。另外，你不使用 `main()` 函数进行测试 - 它们在外面运行。要在Playground中运行这个，点击 _RUN_ 旁边的`···`，然后把它改为 _Test_ 。现在如果你点击它，它将运行测试。(如果你已经安装了 Rust，你将输入 `cargo test` 来做这个测试)

这里是输出:

```text
running 1 test
test two_is_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

让我们把`assert_eq!(2, 2)`改成`assert_eq!(2, 3)`，看看会有什么结果。当测试失败时，你会得到更多的信息。

```text
running 1 test
test two_is_two ... FAILED

failures:

---- two_is_two stdout ----
thread 'two_is_two' panicked at 'assertion failed: `(left == right)`
  left: `2`,
 right: `3`', src/lib.rs:3:5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    two_is_two

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out
```

`assert_eq!(left, right)`是Rust中测试一个函数的主要方法。如果它不工作，它将显示不同的值:左边有2，但右边有3。

`RUST_BACKTRACE=1`是什么意思？这是计算机上的一个设置，可以提供更多关于错误的信息。幸好playground也有:点击`STABLE`旁边的`···`，然后设置回溯为`ENABLED`。如果你这样做，它会给你*很多*的信息。

```text
running 1 test
test two_is_two ... FAILED

failures:

---- two_is_two stdout ----
thread 'two_is_two' panicked at 'assertion failed: 2 == 3', src/lib.rs:3:5
stack backtrace:
   0: backtrace::backtrace::libunwind::trace
             at /cargo/registry/src/github.com-1ecc6299db9ec823/backtrace-0.3.46/src/backtrace/libunwind.rs:86
   1: backtrace::backtrace::trace_unsynchronized
             at /cargo/registry/src/github.com-1ecc6299db9ec823/backtrace-0.3.46/src/backtrace/mod.rs:66
   2: std::sys_common::backtrace::_print_fmt
             at src/libstd/sys_common/backtrace.rs:78
   3: <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt
             at src/libstd/sys_common/backtrace.rs:59
   4: core::fmt::write
             at src/libcore/fmt/mod.rs:1076
   5: std::io::Write::write_fmt
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libstd/io/mod.rs:1537
   6: std::io::impls::<impl std::io::Write for alloc::boxed::Box<W>>::write_fmt
             at src/libstd/io/impls.rs:176
   7: std::sys_common::backtrace::_print
             at src/libstd/sys_common/backtrace.rs:62
   8: std::sys_common::backtrace::print
             at src/libstd/sys_common/backtrace.rs:49
   9: std::panicking::default_hook::{{closure}}
             at src/libstd/panicking.rs:198
  10: std::panicking::default_hook
             at src/libstd/panicking.rs:215
  11: std::panicking::rust_panic_with_hook
             at src/libstd/panicking.rs:486
  12: std::panicking::begin_panic
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libstd/panicking.rs:410
  13: playground::two_is_two
             at src/lib.rs:3
  14: playground::two_is_two::{{closure}}
             at src/lib.rs:2
  15: core::ops::function::FnOnce::call_once
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libcore/ops/function.rs:232
  16: <alloc::boxed::Box<F> as core::ops::function::FnOnce<A>>::call_once
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/liballoc/boxed.rs:1076
  17: <std::panic::AssertUnwindSafe<F> as core::ops::function::FnOnce<()>>::call_once
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libstd/panic.rs:318
  18: std::panicking::try::do_call
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libstd/panicking.rs:297
  19: std::panicking::try
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libstd/panicking.rs:274
  20: std::panic::catch_unwind
             at /rustc/c367798cfd3817ca6ae908ce675d1d99242af148/src/libstd/panic.rs:394
  21: test::run_test_in_process
             at src/libtest/lib.rs:541
  22: test::run_test::run_test_inner::{{closure}}
             at src/libtest/lib.rs:450
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.


failures:
    two_is_two

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out
```

除非你真的找不到问题所在，否则你不需要使用回溯。但幸运的是你也不需要全部理解。 如果你继续阅读，你最终会看到第13行，那里写着`playground`--那是它提到的你的代码的位置。其他的都是关于Rust为了运行你的程序,在其他库中所做的事情。但是这两行告诉你，它看的是playground的第2行和第3行，这是一个提示，要检查那里。这里是那个部分:

```text
  13: playground::two_is_two
             at src/lib.rs:3
  14: playground::two_is_two::{{closure}}
             at src/lib.rs:2
```

编辑：Rust在2021年初改进了其回溯信息，只显示最有意义的信息。现在它更容易阅读。

```text
failures:

---- two_is_two stdout ----
thread 'two_is_two' panicked at 'assertion failed: `(left == right)`
  left: `2`,
 right: `3`', src/lib.rs:3:5
stack backtrace:
   0: rust_begin_unwind
             at /rustc/cb75ad5db02783e8b0222fee363c5f63f7e2cf5b/library/std/src/panicking.rs:493:5
   1: core::panicking::panic_fmt
             at /rustc/cb75ad5db02783e8b0222fee363c5f63f7e2cf5b/library/core/src/panicking.rs:92:14
   2: playground::two_is_two
             at ./src/lib.rs:3:5
   3: playground::two_is_two::{{closure}}
             at ./src/lib.rs:2:1
   4: core::ops::function::FnOnce::call_once
             at /rustc/cb75ad5db02783e8b0222fee363c5f63f7e2cf5b/library/core/src/ops/function.rs:227:5
   5: core::ops::function::FnOnce::call_once
             at /rustc/cb75ad5db02783e8b0222fee363c5f63f7e2cf5b/library/core/src/ops/function.rs:227:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.


failures:
    two_is_two

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s
```

现在我们再把回溯关闭，回到常规测试。现在我们要写一些其他函数，并使用测试函数来测试它们。这里有几个:

```rust
fn return_two() -> i8 {
    2
}
# [test]
fn it_returns_two() {
    assert_eq!(return_two(), 2);
}

fn return_six() -> i8 {
    4 + return_two()
}
# [test]
fn it_returns_six() {
    assert_eq!(return_six(), 6)
}
```

现在，都能运行:

```text
running 2 tests
test it_returns_two ... ok
test it_returns_six ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

这不是太难。

通常你会想把你的测试放在自己的模块中。要做到这一点，请使用相同的 `mod` 关键字，并在其上方添加 `#[cfg(test)]`(记住:`cfg` 的意思是 "配置")。你还要在每个测试上面继续写`#[test]`。这是因为以后当你安装Rust时，你可以做更复杂的测试。你将可以运行一个测试，或者所有的测试，或者运行几个测试。另外别忘了写`use super::*;`，因为测试模块需要使用上面的函数。现在它看起来会是这样的。

```rust
fn return_two() -> i8 {
    2
}
fn return_six() -> i8 {
    4 + return_two()
}

# [cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_returns_six() {
        assert_eq!(return_six(), 6)
    }
    #[test]
    fn it_returns_two() {
        assert_eq!(return_two(), 2);
    }
}
```

## 测试驱动的开发

在阅读Rust或其他语言时，你可能会看到 "测试驱动开发"这个词。这是编写程序的一种方式，有些人喜欢它，而有些人则喜欢其他的方式。"测试驱动开发"的意思是 "先写测试，再写代码"。当你这样做的时候，你会有很多关于你想要你的代码做的所有事情的测试代码。然后你开始写代码，并运行测试，看看你是否做对了。然后，当你添加和重写代码时，如果有什么地方出了问题，测试代码会一直在那里向你展示。这在Rust中是非常容易的，因为编译器给出了很多待修复内容的信息。让我们写一个测试驱动开发的小例子，看看它是什么样子的。

让我们想象一个接受用户输入的计算器。它可以加(+)，也可以减(-)。如果用户写 "5+6"，它应该返回11，如果用户写 "5+6-7"，它应该返回4，以此类推。所以我们先从测试函数开始。你也可以看到，测试中的函数名通常都相当长。这是因为你可能会运行很多测试，你想了解哪些测试失败了。

我们想象一下，一个名为`math()`的函数就可以完成所有的工作。它将返回一个 `i32`(我们不会使用浮点数)。因为它需要返回一些东西，所以我们每次都只返回 `6`。然后我们将写三个测试函数。当然，它们都会失败。现在的代码是这样的。

```rust
fn math(input: &str) -> i32 {
    6
}

# [cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_plus_one_is_two() {
        assert_eq!(math("1 + 1"), 2);
    }
    #[test]
    fn one_minus_two_is_minus_one() {
        assert_eq!(math("1 - 2"), -1);
    }
    #[test]
    fn one_minus_minus_one_is_two() {
        assert_eq!(math("1 - -1"), 2);
    }
}
```

它给了我们这个信息。

```text
running 3 tests
test tests::one_minus_minus_one_is_two ... FAILED
test tests::one_minus_two_is_minus_one ... FAILED
test tests::one_plus_one_is_two ... FAILED
```

以及``thread 'tests::one_plus_one_is_two' panicked at 'assertion failed: `(left == right)` ``的所有信息。我们不需要在这里全部打印出来。

现在要考虑如何创建计算器。我们将接受任何数字，以及符号`+-`。我们将允许空格，但不允许其他任何东西。所以，让我们从包含所有数值的`const`开始。然后我们将使用 `.chars()` 按字符进行迭代，并使用 `.all()` 确保它们都在里面。

然后，我们将添加一个会崩溃的测试。要做到这一点，添加 `#[should_panic]` 属性:现在如果它崩溃，测试将成功。

现在代码看起来像这样:

```rust
const OKAY_CHARACTERS: &str = "1234567890+- "; // 别忘了末尾的空格

fn math(input: &str) -> i32 {
    if !input.chars().all(|character| OKAY_CHARACTERS.contains(character)) {
        panic!("Please only input numbers, +-, or spaces");
    }
    6 // 暂时仍返回 6
}

# [cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_plus_one_is_two() {
        assert_eq!(math("1 + 1"), 2);
    }
    #[test]
    fn one_minus_two_is_minus_one() {
        assert_eq!(math("1 - 2"), -1);
    }
    #[test]
    fn one_minus_minus_one_is_two() {
        assert_eq!(math("1 - -1"), 2);
    }

    #[test]
    #[should_panic]  // 这是新测试 — 它应该 panic
    fn panics_when_characters_not_right() {
        math("7 + seven");
    }
}
```

现在，当我们运行测试时，我们得到这样的结果。

```text
running 4 tests
test tests::one_minus_two_is_minus_one ... FAILED
test tests::one_minus_minus_one_is_two ... FAILED
test tests::panics_when_characters_not_right ... ok
test tests::one_plus_one_is_two ... FAILED
```

一个成功了! 我们的`math()`函数现在只能接受好的输入了。


下一步是编写实际的计算器。这就是先有测试的有趣之处:实际的代码要晚很多。首先，我们将把计算器的逻辑放在一起。我们要做到以下几点。

- 所有的空位都应该被删除。这在`.filter()`中很容易实现。
- 所有输入应该变成一个`Vec`。`+`不需要成为输入，但是当程序看到`+`时，应该知道这个数字已经完成了。例如，输入`+`应该这样做:
    1) 看到`1`，把它推到一个空字符串中。
    2) 看到另一个1，把它推入字符串中(现在是 "11")。
    3) 看到一个`+`，知道这个数字已经结束。它会把字符串推入vec中，然后清空字符串。
- 程序必须计算出`-`的数量。奇数(1，3，5...)表示减法，偶数(2，4，6...)表示加法。所以 "1--9"应该是10，而不是-8。
- 程序应该删除最后一个数字后面的任何东西。`5+5+++++----`是由`OKAY_CHARACTERS`中的所有字符组成的，但它应该变成`5+5`。`.trim_end_matches()`就很简单了，你把`&str`末尾符合的东西都去掉。

顺便说一下，`.trim_end_matches()`和`.trim_start_matches()`曾经是`trim_right_matches()`和`trim_left_matches()`。但后来人们注意到有些语言是从右到左(波斯语、希伯来语等)，所以左右都是错的。你可能还能在一些代码中看到旧的名字，但它们是一样的)。)

首先我们只想通过所有的测试。通过测试后，我们就可以 "重构"了。重构的意思是让代码变得更好，通常是通过结构、枚举和方法等方式。下面是我们使测试通过的代码。

```rust
const OKAY_CHARACTERS: &str = "1234567890+- ";

fn math(input: &str) -> i32 {
    if !input.chars().all(|character| OKAY_CHARACTERS.contains(character)) ||
       !input.chars().take(2).any(|character| character.is_numeric())
    {
        panic!("Please only input numbers, +-, or spaces.");
    }

    let input = input.trim_end_matches(|x| "+- ".contains(x)).chars().filter(|x| *x != ' ').collect::<String>(); // 去掉末尾的 + 和 -，以及所有空格
    let mut result_vec = vec![]; // 结果放这里
    let mut push_string = String::new(); // 每次推进去的字符串。循环里会反复复用。
    for character in input.chars() {
        match character {
            '+' => {
                if !push_string.is_empty() { // 字符串为空时，不要把 "" 推进 result_vec
                    result_vec.push(push_string.clone()); // 非空则是数字，推进 vec
                    push_string.clear(); // 然后清空字符串
                }
            },
            '-' => { // 如果遇到 -，
                if push_string.contains('-') || push_string.is_empty() { // 检查是否为空或已有 -
                    push_string.push(character) // 是的话就推进去
                } else { // 否则里面会有数字
                result_vec.push(push_string.clone()); // 就把数字推进 result_vec，清空，再推进 -
                push_string.clear();
                push_string.push(character);
                }
            },
            number => { // 这里的 number 表示「匹配到的其他任何东西」。名字是我们起的
                if push_string.contains('-') { // 可能要先把一些 - 推进去
                    result_vec.push(push_string.clone());
                    push_string.clear();
                    push_string.push(number);
                } else { // 否则就可以直接推进数字
                    push_string.push(number);
                }
            },
        }
    }
    result_vec.push(push_string); // 循环结束后再推一次。不用 .clone()，因为后面不再用它了

    let mut total = 0; // 该做运算了。从 total 开始
    let mut adds = true; // true = 加，false = 减
    let mut math_iter = result_vec.into_iter();
    while let Some(entry) = math_iter.next() { // 遍历各项
        if entry.contains('-') { // 若含 -，检查个数是奇还是偶
            if entry.chars().count() % 2 == 1 {
                adds = match adds {
                    true => false,
                    false => true
                };
                continue; // 跳到下一项
            } else {
                continue;
            }
        }
        if adds == true {
            total += entry.parse::<i32>().unwrap(); // 没有 '-' 就一定是数字，可以安全 unwrap
        } else {
            total -= entry.parse::<i32>().unwrap();
            adds = true;  // 减法之后，把 adds 重置为 true。
        }
    }
    total // 最后返回 total
}
   /// 再加几个测试，确认无误

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_plus_one_is_two() {
        assert_eq!(math("1 + 1"), 2);
    }
    #[test]
    fn one_minus_two_is_minus_one() {
        assert_eq!(math("1 - 2"), -1);
    }
    #[test]
    fn one_minus_minus_one_is_two() {
        assert_eq!(math("1 - -1"), 2);
    }
    #[test]
    fn nine_plus_nine_minus_nine_minus_nine_is_zero() {
        assert_eq!(math("9+9-9-9"), 0); // 这是新测试
    }
    #[test]
    fn eight_minus_nine_plus_nine_is_eight_even_with_characters_on_the_end() {
        assert_eq!(math("8  - 9     +9-----+++++"), 8); // 这是新测试
    }
    #[test]
    #[should_panic]
    fn panics_when_characters_not_right() {
        math("7 + seven");
    }
}
```

现在测试通过了!

```text
running 6 tests
test tests::one_minus_minus_one_is_two ... ok
test tests::nine_plus_nine_minus_nine_minus_nine_is_zero ... ok
test tests::one_minus_two_is_minus_one ... ok
test tests::eight_minus_nine_plus_nine_is_eight_even_with_characters_on_the_end ... ok
test tests::one_plus_one_is_two ... ok
test tests::panics_when_characters_not_right ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

你可以看到，在测试驱动的开发中，有一个来回的过程。它是这样的。

- 首先你要写出所有你能想到的测试
- 然后你开始写代码。
- 当你写代码的时候，你会有其他测试的想法。
- 你添加测试，你的测试随着你的发展而增长。你的测试越多，你的代码被检查的次数就越多。

当然，测试并不能检查所有的东西，认为 "通过所有测试=代码是完美的"是错误的。但是，测试对于你修改代码的时候是非常好的。如果你以后修改了代码，然后运行测试，如果其中一个测试不成功，你就会知道该怎么修复。

现在我们可以重写(重构)一下代码。一个好的方法是用clippy开始。如果你安装了Rust，那么你可以输入`cargo clippy`，如果你使用的是Playground，那么点击`TOOLS`，选择Clippy。Clippy会查看你的代码，并给你提示，让你的代码更简单。我们的代码没有任何错误，但它可以更好。

Clippy会告诉我们两件事。

```text
warning: this loop could be written as a `for` loop
  --> src/lib.rs:44:5
   |
44 |     while let Some(entry) = math_iter.next() { // 遍历各项
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ help: try: `for entry in math_iter`
   |
   = note: `#[warn(clippy::while_let_on_iterator)]` on by default
   = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#while_let_on_iterator

warning: equality checks against true are unnecessary
  --> src/lib.rs:53:12
   |
53 |         if adds == true {
   |            ^^^^^^^^^^^^ help: try simplifying it as shown: `adds`
   |
   = note: `#[warn(clippy::bool_comparison)]` on by default
   = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#bool_comparison
```

这是真的:`for entry in math_iter`比`while let Some(entry) = math_iter.next()`简单得多。而`for`循环实际上是一个迭代器，所以我们没有任何理由写`.iter()`。谢谢你，clippy! 而且我们也不需要做`math_iter`:我们可以直接写`for entry in result_vec`。

现在我们将开始一些真正的重构。我们将创建一个 `Calculator` 结构体，而不是单独的变量。这将拥有我们使用的所有变量。我们将改变两个名字以使其更加清晰。`result_vec`将变成`results`，`push_string`将变成`current_input`(current的意思是 "现在")。而到目前为止，它只有一种方法:new。

```rust
// 🚧
#[derive(Clone)]
struct Calculator {
    results: Vec<String>,
    current_input: String,
    total: i32,
    adds: bool,
}

impl Calculator {
    fn new() -> Self {
        Self {
            results: vec![],
            current_input: String::new(),
            total: 0,
            adds: true,
        }
    }
}
```

现在我们的代码其实比较长，但更容易读懂。比如，`if adds`现在是`if calculator.adds`，这就跟读英文完全一样。它的样子是这样的:

```rust
#[derive(Clone)]
struct Calculator {
    results: Vec<String>,
    current_input: String,
    total: i32,
    adds: bool,
}

impl Calculator {
    fn new() -> Self {
        Self {
            results: vec![],
            current_input: String::new(),
            total: 0,
            adds: true,
        }
    }
}

const OKAY_CHARACTERS: &str = "1234567890+- ";

fn math(input: &str) -> i32 {
    if !input.chars().all(|character| OKAY_CHARACTERS.contains(character)) ||
       !input.chars().take(2).any(|character| character.is_numeric()) {
        panic!("Please only input numbers, +-, or spaces");
    }

    let input = input.trim_end_matches(|x| "+- ".contains(x)).chars().filter(|x| *x != ' ').collect::<String>();
    let mut calculator = Calculator::new();

    for character in input.chars() {
        match character {
            '+' => {
                if !calculator.current_input.is_empty() {
                    calculator.results.push(calculator.current_input.clone());
                    calculator.current_input.clear();
                }
            },
            '-' => {
                if calculator.current_input.contains('-') || calculator.current_input.is_empty() {
                    calculator.current_input.push(character)
                } else {
                calculator.results.push(calculator.current_input.clone());
                calculator.current_input.clear();
                calculator.current_input.push(character);
                }
            },
            number => {
                if calculator.current_input.contains('-') {
                    calculator.results.push(calculator.current_input.clone());
                    calculator.current_input.clear();
                    calculator.current_input.push(number);
                } else {
                    calculator.current_input.push(number);
                }
            },
        }
    }
    calculator.results.push(calculator.current_input);

    for entry in calculator.results {
        if entry.contains('-') {
            if entry.chars().count() % 2 == 1 {
                calculator.adds = match calculator.adds {
                    true => false,
                    false => true
                };
                continue;
            } else {
                continue;
            }
        }
        if calculator.adds {
            calculator.total += entry.parse::<i32>().unwrap();
        } else {
            calculator.total -= entry.parse::<i32>().unwrap();
            calculator.adds = true;
        }
    }
    calculator.total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_plus_one_is_two() {
        assert_eq!(math("1 + 1"), 2);
    }
    #[test]
    fn one_minus_two_is_minus_one() {
        assert_eq!(math("1 - 2"), -1);
    }
    #[test]
    fn one_minus_minus_one_is_two() {
        assert_eq!(math("1 - -1"), 2);
    }
    #[test]
    fn nine_plus_nine_minus_nine_minus_nine_is_zero() {
        assert_eq!(math("9+9-9-9"), 0);
    }
    #[test]
    fn eight_minus_nine_plus_nine_is_eight_even_with_characters_on_the_end() {
        assert_eq!(math("8  - 9     +9-----+++++"), 8);
    }
    #[test]
    #[should_panic]
    fn panics_when_characters_not_right() {
        math("7 + seven");
    }
}
```

最后我们增加两个新方法。一个叫做 `.clear()`，清除 `current_input()`。另一个叫做 `push_char()`，把输入推到 `current_input()` 上。这是我们重构后的代码。

```rust
#[derive(Clone)]
struct Calculator {
    results: Vec<String>,
    current_input: String,
    total: i32,
    adds: bool,
}

impl Calculator {
    fn new() -> Self {
        Self {
            results: vec![],
            current_input: String::new(),
            total: 0,
            adds: true,
        }
    }

    fn clear(&mut self) {
        self.current_input.clear();
    }

    fn push_char(&mut self, character: char) {
        self.current_input.push(character);
    }
}

const OKAY_CHARACTERS: &str = "1234567890+- ";

fn math(input: &str) -> i32 {
    if !input.chars().all(|character| OKAY_CHARACTERS.contains(character)) ||
       !input.chars().take(2).any(|character| character.is_numeric()) {
        panic!("Please only input numbers, +-, or spaces");
    }

    let input = input.trim_end_matches(|x| "+- ".contains(x)).chars().filter(|x| *x != ' ').collect::<String>();
    let mut calculator = Calculator::new();

    for character in input.chars() {
        match character {
            '+' => {
                if !calculator.current_input.is_empty() {
                    calculator.results.push(calculator.current_input.clone());
                    calculator.clear();
                }
            },
            '-' => {
                if calculator.current_input.contains('-') || calculator.current_input.is_empty() {
                    calculator.push_char(character)
                } else {
                calculator.results.push(calculator.current_input.clone());
                calculator.clear();
                calculator.push_char(character);
                }
            },
            number => {
                if calculator.current_input.contains('-') {
                    calculator.results.push(calculator.current_input.clone());
                    calculator.clear();
                    calculator.push_char(number);
                } else {
                    calculator.push_char(number);
                }
            },
        }
    }
    calculator.results.push(calculator.current_input);

    for entry in calculator.results {
        if entry.contains('-') {
            if entry.chars().count() % 2 == 1 {
                calculator.adds = match calculator.adds {
                    true => false,
                    false => true
                };
                continue;
            } else {
                continue;
            }
        }
        if calculator.adds {
            calculator.total += entry.parse::<i32>().unwrap();
        } else {
            calculator.total -= entry.parse::<i32>().unwrap();
            calculator.adds = true;
        }
    }
    calculator.total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_plus_one_is_two() {
        assert_eq!(math("1 + 1"), 2);
    }
    #[test]
    fn one_minus_two_is_minus_one() {
        assert_eq!(math("1 - 2"), -1);
    }
    #[test]
    fn one_minus_minus_one_is_two() {
        assert_eq!(math("1 - -1"), 2);
    }
    #[test]
    fn nine_plus_nine_minus_nine_minus_nine_is_zero() {
        assert_eq!(math("9+9-9-9"), 0);
    }
    #[test]
    fn eight_minus_nine_plus_nine_is_eight_even_with_characters_on_the_end() {
        assert_eq!(math("8  - 9     +9-----+++++"), 8);
    }
    #[test]
    #[should_panic]
    fn panics_when_characters_not_right() {
        math("7 + seven");
    }
}
```

现在大概已经够好了。我们可以写更多的方法，但是像`calculator.results.push(calculator.current_input.clone());`这样的行已经很清楚了。重构最好是在你完成后还能轻松阅读代码的时候。你不希望只是为了让代码变短而重构:例如，`clc.clr()`就比`calculator.clear()`差很多。
