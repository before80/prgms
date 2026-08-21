+++
title = "64-接受用户输入"
date = 2026-08-21T12:46:00+08:00
weight = 65
type = "docs"
description = "接受用户输入 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_63.html](https://dhghomon.github.io/easy_rust/Chapter_63.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 接受用户输入

一个简单的方法是用`std::io::stdin`来接受用户的输入。这意味着 "标准输入"，也就是来自键盘的输入。用`stdin()`可以获得用户的输入，但是接下来你就会想用`.read_line()`把它放到`&mut String`中。下面是一个简单的例子，但它既能工作，也不能工作:

```rust
use std::io;

fn main() {
    println!("Please type something, or x to escape:");
    let mut input_string = String::new();

    while input_string != "x" { // 这部分行为不对
        input_string.clear(); // 先清空 String。否则会一直往上追加
        io::stdin().read_line(&mut input_string).unwrap(); // 从用户读入 stdin，放进字符串
        println!("You wrote {}", input_string);
    }
    println!("See you later!");
}
```

下面是一个输出输出的样子。

```text
Please type something, or x to escape:
something
You wrote something

Something else
You wrote Something else

x
You wrote x

x
You wrote x

x
You wrote x
```

它接受我们的输入，然后把它还给我们，它甚至知道我们输入了`x`。但它并没有退出程序。唯一的办法是关闭窗口，或者输入ctrl和c。让我们把`println!`中的`{}`改为`{:?}`，以获得更多的信息(如果你喜欢那个宏，也可以使用`dbg!(&input_string)`)。现在它说

```text
Please type something, or x to escape:
something
You wrote "something\r\n"
Something else
You wrote "Something else\r\n"
x
You wrote "x\r\n"
x
You wrote "x\r\n"
```



这是因为键盘输入其实不只是`something`，而是`something`和`Enter`键。有一个简单的方法可以解决这个问题，叫做`.trim()`，它可以把所有的空白都去掉。顺便说一下，[这些字符](https://doc.rust-lang.org/reference/whitespace.html)都是空白字符。

```text
U+0009 (horizontal tab, '\t')
U+000A (line feed, '\n')
U+000B (vertical tab)
U+000C (form feed)
U+000D (carriage return, '\r')
U+0020 (space, ' ')
U+0085 (next line)
U+200E (left-to-right mark)
U+200F (right-to-left mark)
U+2028 (line separator)
U+2029 (paragraph separator)
```

这样就可以把`x\r\n`变成只剩`x`了。现在它可以工作了:

```rust
use std::io;

fn main() {
    println!("Please type something, or x to escape:");
    let mut input_string = String::new();

    while input_string.trim() != "x" {
        input_string.clear();
        io::stdin().read_line(&mut input_string).unwrap();
        println!("You wrote {}", input_string);
    }
    println!("See you later!");
}
```

现在可以打印了:

```text
Please type something, or x to escape:
something
You wrote something

Something
You wrote Something

x
You wrote x

See you later!
```



还有一种用户输入叫`std::env::Args`(env是环境的意思)。`Args`是用户启动程序时输入的内容。其实在一个程序中总是至少有一个`Arg`。我们写一个程序，只用`std::env::args()`来打印它们，看看它们是什么。

```rust
fn main() {
    println!("{:?}", std::env::args());
}
```

如果我们写`cargo run`，那么它的打印结果是这样的:

```text
Args { inner: ["target\\debug\\rust_book.exe"] }
```

让我们给它更多的输入，看看它的作用。我们输入 `cargo run but with some extra words` 。 它给我们:

```text
Args { inner: ["target\\debug\\rust_book.exe", "but", "with", "some", "extra", "words"] }
```

有意思。而当我们查看[Args的页面](https://doc.rust-lang.org/std/env/struct.Args.html)时，我们看到它实现了`IntoIterator`。这意味着我们可以.用所有我们知道的关于迭代器的方法来读取和改变它。让我们试试这个:

```rust
use std::env::args;

fn main() {
    let input = args();

    for entry in input {
        println!("You entered: {}", entry);
    }
}
```

现在它说:

```text
You entered: target\debug\rust_book.exe
You entered: but
You entered: with
You entered: some
You entered: extra
You entered: words
```

你可以看到，第一个参数总是程序名，所以你经常会想跳过它，比如这样:

```rust
use std::env::args;

fn main() {
    let input = args();

    input.skip(1).for_each(|item| {
        println!("You wrote {}, which in capital letters is {}", item, item.to_uppercase());
    })
}
```

这将打印:

```text
You wrote but, which in capital letters is BUT
You wrote with, which in capital letters is WITH
You wrote some, which in capital letters is SOME
You wrote extra, which in capital letters is EXTRA
You wrote words, which in capital letters is WORDS
```

`Args`的一个常见用途是用于用户设置。你可以确保用户写出你需要的输入，只有在正确的情况下才运行程序。这里有一个小程序，可以让字母变大(大写)或变小(小写)。

```rust
use std::env::args;

enum Letters {
    Capitalize,
    Lowercase,
    Nothing,
}

fn main() {
    let mut changes = Letters::Nothing;
    let input = args().collect::<Vec<_>>();

    if input.len() > 2 {
        match input[1].as_str() {
            "capital" => changes = Letters::Capitalize,
            "lowercase" => changes = Letters::Lowercase,
            _ => {}
        }
    }

    for word in input.iter().skip(2) {
      match changes {
        Letters::Capitalize => println!("{}", word.to_uppercase()),
        Letters::Lowercase => println!("{}", word.to_lowercase()),
        _ => println!("{}", word)
      }
    }

}
```

下面是它给出的一些例子。

输入: `cargo run please make capitals`:

```text
make capitals
```

输入:`cargo run capital`:

```text
// 这里什么都没有...
```

输入:`cargo run capital I think I understand now`:

```text
I
THINK
I
UNDERSTAND
NOW
```

输入:`cargo run lowercase Does this work too?`

```text
does
this
work
too?
```



除了用户给出的 `Args`，在 `std::env::args()` 中可用，还有系统变量`Vars`。这些都是用户没有输入的程序的基本设置。你可以用`std::env::vars()`把它们都看成一个`(String, String)`。这个有非常多，比如说:

```rust
fn main() {
    for item in std::env::vars() {
        println!("{:?}", item);
    }
}
```

运行这段代码，就能显示出你的用户会话的所有信息。它将显示这样的信息:

```text
("CARGO", "/playground/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo")
("CARGO_HOME", "/playground/.cargo")
("CARGO_MANIFEST_DIR", "/playground")
("CARGO_PKG_AUTHORS", "The Rust Playground")
("CARGO_PKG_DESCRIPTION", "")
("CARGO_PKG_HOMEPAGE", "")
("CARGO_PKG_NAME", "playground")
("CARGO_PKG_REPOSITORY", "")
("CARGO_PKG_VERSION", "0.0.1")
("CARGO_PKG_VERSION_MAJOR", "0")
("CARGO_PKG_VERSION_MINOR", "0")
("CARGO_PKG_VERSION_PATCH", "1")
("CARGO_PKG_VERSION_PRE", "")
("DEBIAN_FRONTEND", "noninteractive")
("HOME", "/playground")
("HOSTNAME", "f94c15b8134b")
("LD_LIBRARY_PATH", "/playground/target/debug/build/backtrace-sys-3ec4c973f371c302/out:/playground/target/debug/build/libsqlite3-sys-fbddfbb9b241dacb/out:/playground/target/debug/build/ring-cadba5e583648abb/out:/playground/target/debug/deps:/playground/target/debug:/playground/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/lib:/playground/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib")
("PATH", "/playground/.cargo/bin:/playground/.cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin")
("PLAYGROUND_EDITION", "2018")
("PLAYGROUND_TIMEOUT", "10")
("PWD", "/playground")
("RUSTUP_HOME", "/playground/.rustup")
("RUSTUP_TOOLCHAIN", "stable-x86_64-unknown-linux-gnu")
("RUST_RECURSION_COUNT", "1")
("SHLVL", "1")
("SSL_CERT_DIR", "/usr/lib/ssl/certs")
("SSL_CERT_FILE", "/usr/lib/ssl/certs/ca-certificates.crt")
("USER", "playground")
("_", "/usr/bin/timeout")
```

所以如果你需要这些信息，`Vars`就是你想要的。

获得单个`Var'的最简单方法是使用`env!`宏。你只要给它变量的名字，它就会给你一个`&str'的值。如果变量拼写错误或不存在，它就不起作用，所以如果你不确定，就用`option_env!`代替。如果我们在Playground上写这个:

```rust
fn main() {
    println!("{}", env!("USER"));
    println!("{}", option_env!("ROOT").unwrap_or("Can't find ROOT"));
    println!("{}", option_env!("CARGO").unwrap_or("Can't find CARGO"));
}
```

然后我们得到输出:

```text
playground
Can't find ROOT
/playground/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo
```

所以`option_env!`永远是比较安全的宏。如果你真的想让程序在找不到环境变量时崩溃，那么`env!`会更好。
