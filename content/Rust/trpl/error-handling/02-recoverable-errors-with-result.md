+++
title = "9.2 用 Result 处理可恢复错误"
date = 2026-08-05T08:44:00+08:00
weight = 39
type = "docs"
description = "用 Result、match 与 ? 运算符处理可恢复错误"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 Result 处理可恢复错误 {#result}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch09-02-recoverable-errors-with-result.html](https://doc.rust-lang.org/stable/book/ch09-02-recoverable-errors-with-result.html)


## 用 `Result` 处理可恢复错误

　　多数错误还不至于要求程序完全停止。有时函数失败的原因很容易理解并做出响应。例如，若打开文件失败是因为文件不存在，你可能希望创建该文件，而不是终止进程。

　　回想第 2 章[「用 `Result` 处理可能的失败」][handle_failure]：`Result` 枚举定义为带有 `Ok` 与 `Err` 两个变体，如下所示：

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

　　`T` 和 `E` 是泛型类型参数：第 10 章会更详细讨论泛型。眼下你只需知道：`T` 表示成功时在 `Ok` 变体中返回的值的类型，`E` 表示失败时在 `Err` 变体中返回的错误的类型。正因为 `Result` 有这些泛型参数，我们才能在许多不同场景里使用 `Result` 及其方法——成功值与错误值的具体类型可以各不相同。

　　我们来调用一个可能失败、因而返回 `Result` 的函数。示例 9-3 尝试打开一个文件。

**文件名：`src/main.rs`**
```rust
use std::fs::File;

fn main() {
    let greeting_file_result = File::open("hello.txt");
}
```

**示例 9-3：打开文件**

　　`File::open` 的返回类型是 `Result<T, E>`。`File::open` 的实现把泛型参数 `T` 填成了成功值的类型 `std::fs::File`（文件句柄），错误值所用的 `E` 则是 `std::io::Error`。这意味着调用 `File::open` 既可能成功并返回可供读写的文件句柄，也可能失败：例如文件不存在，或没有访问权限。`File::open` 需要一种方式告诉我们成功还是失败，同时给出文件句柄或错误信息——而这正是 `Result` 枚举所表达的。

　　若 `File::open` 成功，变量 `greeting_file_result` 中的值会是包含文件句柄的 `Ok` 实例；若失败，则会是包含更多错误信息的 `Err` 实例。

　　我们需要在示例 9-3 的代码上继续，根据 `File::open` 的返回值采取不同行动。示例 9-4 展示了一种用 `match` 表达式处理 `Result` 的基本做法（第 6 章讨论过 `match`）。

**文件名：`src/main.rs`**
```rust
use std::fs::File;

fn main() {
    let greeting_file_result = File::open("hello.txt");

    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => panic!("Problem opening the file: {error:?}"),
    };
}
```

**示例 9-4：用 `match` 表达式处理可能返回的 `Result` 变体**

　　注意：与 `Option` 枚举一样，`Result` 及其变体已在 prelude 中，可直接使用，因此在 `match` 分支里不必写成 `Result::Ok` / `Result::Err`。

　　当结果是 `Ok` 时，这段代码会把 `Ok` 里的内部 `file` 值取出来，赋给变量 `greeting_file`。`match` 之后就可以用该文件句柄进行读写。

　　`match` 的另一分支处理从 `File::open` 得到 `Err` 的情况。本例中我们选择调用 `panic!` 宏。若当前目录下没有名为 _hello.txt_ 的文件并运行这段代码，会看到来自 `panic!` 的如下输出：

```console
$ cargo run
   Compiling error-handling v0.1.0 (file:///projects/error-handling)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.73s
     Running `target/debug/error-handling`

thread 'main' (6018048) panicked at src/main.rs:8:23:
Problem opening the file: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　一如既往，输出清楚地告诉我们出了什么问题。

### 针对不同错误进行匹配

　　示例 9-4 的代码无论 `File::open` 因何失败都会 `panic!`。但我们往往希望对不同失败原因采取不同行动：若因为文件不存在而失败，就创建文件并返回新文件的句柄；若因其他原因失败——例如没有打开权限——则仍希望像示例 9-4 那样 `panic!`。为此可加入内层 `match`，如示例 9-5 所示。

**文件名：`src/main.rs`**

```rust
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let greeting_file_result = File::open("hello.txt");

    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating the file: {e:?}"),
            },
            _ => {
                panic!("Problem opening the file: {error:?}");
            }
        },
    };
}
```

**示例 9-5：以不同方式处理不同种类的错误**

　　`File::open` 在 `Err` 变体中返回的值类型是 `io::Error`，这是标准库提供的结构体。它有一个 `kind` 方法，可调用以得到 `io::ErrorKind` 值。枚举 `io::ErrorKind` 由标准库提供，其变体表示 `io` 操作可能产生的不同错误种类。我们要用的是 `ErrorKind::NotFound`，表示要打开的文件尚不存在。因此我们既匹配 `greeting_file_result`，又在内层匹配 `error.kind()`。

　　内层 match 要检查的条件是：`error.kind()` 的返回值是否为 `ErrorKind` 的 `NotFound` 变体。若是，就用 `File::create` 尝试创建文件。但 `File::create` 也可能失败，所以内层 `match` 还需要第二个分支：无法创建文件时打印不同的错误消息。外层 `match` 的第二个分支保持不变，因此除“文件缺失”以外的任何错误都会让程序 panic。

> #### 不用 `match` 处理 `Result<T, E>` 的替代写法
>
> `match` 可真多！`match` 表达式很有用，但也相当底层。第 13 章你会学到闭包（closure），它们会与 `Result<T, E>` 上定义的许多方法一起使用。处理 `Result<T, E>` 时，这些方法往往比 `match` 更简洁。
>
> 例如，下面用闭包和 `unwrap_or_else` 方法写出与示例 9-5 相同的逻辑：
>
> 
>
> ```rust
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> 这段代码与示例 9-5 行为相同，却没有任何 `match`，读起来也更干净。读完第 13 章后可以再回来看这个例子，并在标准库文档中查阅 `unwrap_or_else`。处理错误时，还有许多类似方法能清理掉层层嵌套的庞大 `match`。

#### 出错时直接 Panic 的快捷方式

　　用 `match` 固然可行，但有时略显冗长，也不总能清楚表达意图。`Result<T, E>` 上定义了许多辅助方法，可完成各种更具体的任务。`unwrap` 方法的实现方式与我们在示例 9-4 中写的 `match` 类似：若 `Result` 是 `Ok`，就返回 `Ok` 里的值；若是 `Err`，就替我们调用 `panic!`。示例如下：

**文件名：`src/main.rs`**
```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```

　　若在没有 _hello.txt_ 的情况下运行，会看到 `unwrap` 内部调用 `panic!` 产生的错误信息：


```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

　　类似地，`expect` 方法还允许我们自定义 `panic!` 的错误消息。用 `expect` 代替 `unwrap` 并提供有意义的错误信息，能更好地传达意图，也更容易追踪 panic 来源。`expect` 的写法如下：

**文件名：`src/main.rs`**
```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")
        .expect("hello.txt should be included in this project");
}
```

　　我们像使用 `unwrap` 一样使用 `expect`：要么返回文件句柄，要么调用 `panic!`。`expect` 传给 `panic!` 的错误消息是我们传入的参数，而不是 `unwrap` 使用的默认消息。输出大致如下：


```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

　　在生产级代码里，多数 Rustacean 会选择 `expect` 而非 `unwrap`，并说明为何认为该操作应当始终成功。这样，一旦假设被打破，调试时就有更多上下文可用。

### 传播错误

　　当函数实现中调用了可能失败的操作时，你可以不在函数内部处理错误，而是把错误返回给调用方，由调用方决定如何处理。这叫做*传播（propagating）*错误：调用方往往掌握更多信息或逻辑来决定该如何应对，因而能获得更多控制权。

　　例如，示例 9-6 展示了一个从文件读取用户名的函数。若文件不存在或无法读取，函数会把这些错误返回给调用方。

**文件名：`src/main.rs`**

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let username_file_result = File::open("hello.txt");

    let mut username_file = match username_file_result {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut username = String::new();

    match username_file.read_to_string(&mut username) {
        Ok(_) => Ok(username),
        Err(e) => Err(e),
    }
}
```

**示例 9-6：用 `match` 把错误返回给调用方的函数**

　　这个函数其实可以写得短得多，但我们先手动写详细版本，以便探索错误处理；最后再展示更短的写法。先看返回类型：`Result<String, io::Error>`。这意味着函数返回 `Result<T, E>`，其中 `T` 填成具体类型 `String`，`E` 填成具体类型 `io::Error`。

　　若函数顺利成功，调用方会收到包含 `String` 的 `Ok`——也就是从文件读出的 `username`。若遇到任何问题，调用方会收到包含 `io::Error` 实例的 `Err`，其中有更多问题细节。我们选择 `io::Error` 作为返回类型，是因为函数体里两个可能失败的操作——`File::open` 与 `read_to_string`——返回的错误值碰巧都是这个类型。

　　函数体先调用 `File::open`，再用与示例 9-4 类似的 `match` 处理 `Result`。若 `File::open` 成功，模式变量 `file` 中的文件句柄成为可变变量 `username_file` 的值，函数继续执行。在 `Err` 分支里，我们不调用 `panic!`，而是用 `return` 提前退出整个函数，并把现已在模式变量 `e` 中的 `File::open` 错误值作为本函数的错误值传回调用方。

　　于是，若已有文件句柄 `username_file`，函数再创建一个新的 `String`（变量 `username`），并对该句柄调用 `read_to_string`，把文件内容读入 `username`。`read_to_string` 也可能失败（即便 `File::open` 已成功），因此也返回 `Result`，我们需要再用 `match` 处理：若 `read_to_string` 成功，函数成功，返回包在 `Ok` 里的、现已在 `username` 中的用户名；若失败，就以与处理 `File::open` 返回值时相同的方式返回错误值。不过这里不必显式写 `return`，因为它是函数中的最后一个表达式。

　　调用这段代码的一方随后会处理：要么得到包含用户名的 `Ok`，要么得到包含 `io::Error` 的 `Err`。如何处理由调用方决定——例如可以 `panic!` 崩溃、使用默认用户名，或从文件以外的地方查找用户名。我们没有足够信息知道调用方真正想做什么，因此把全部成功或错误信息向上传播，由其妥善处理。

　　在 Rust 中，向上传播错误非常普遍，因此语言提供了 `?` 运算符来简化它。

#### `?` 运算符快捷方式 {#a-shortcut-for-propagating-errors-the--operator}

　　示例 9-7 展示了与示例 9-6 功能相同的 `read_username_from_file` 实现，但使用了 `?` 运算符。

**文件名：`src/main.rs`**

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username_file = File::open("hello.txt")?;
    let mut username = String::new();
    username_file.read_to_string(&mut username)?;
    Ok(username)
}
```

**示例 9-7：用 `?` 运算符把错误返回给调用方的函数**

　　放在 `Result` 值后面的 `?`，其定义几乎等同于我们在示例 9-6 中用来处理 `Result` 的那些 `match`：若 `Result` 是 `Ok`，表达式返回 `Ok` 里的值，程序继续；若是 `Err`，则像使用了 `return` 一样从整个函数返回该 `Err`，从而把错误传播给调用方。

　　示例 9-6 的 `match` 与 `?` 运算符有一点不同：对之使用 `?` 的错误值会经过标准库 `From` trait 中定义的 `from` 函数，用于把一种类型转换成另一种。当 `?` 调用 `from` 时，收到的错误类型会被转换成当前函数返回类型中定义的错误类型。这很有用：即便函数内部可能因多种不同原因失败，也可以用单一错误类型表示所有失败方式。

　　例如，可以把示例 9-7 中的 `read_username_from_file` 改成返回我们自定义的错误类型 `OurError`。若同时定义了 `impl From<io::Error> for OurError`，以便从 `io::Error` 构造 `OurError`，那么函数体中的 `?` 就会调用 `from` 完成错误类型转换，无需再写额外代码。

　　在示例 9-7 的语境下，`File::open` 调用末尾的 `?` 会把 `Ok` 里的值赋给变量 `username_file`；若出错，`?` 会提前退出整个函数，并把任何 `Err` 值交给调用方。`read_to_string` 末尾的 `?` 同理。

　　`?` 消除了大量样板代码，使函数实现更简洁。我们甚至可以在 `?` 之后立刻链式调用方法，如示例 9-8 所示。

**文件名：`src/main.rs`**

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username = String::new();

    File::open("hello.txt")?.read_to_string(&mut username)?;

    Ok(username)
}
```

**示例 9-8：在 `?` 运算符之后链式调用方法**

　　我们把创建新 `String`（`username`）移到了函数开头；这部分没变。不再创建变量 `username_file`，而是把对 `read_to_string` 的调用直接接在 `File::open("hello.txt")?` 的结果上。`read_to_string` 末尾仍有 `?`，当 `File::open` 与 `read_to_string` 都成功时仍返回包含 `username` 的 `Ok`，否则返回错误。功能再次与示例 9-6、9-7 相同，只是写法更符合人体工学。

　　示例 9-9 展示了用 `fs::read_to_string` 让代码更短的方式。

**文件名：`src/main.rs`**

```rust
use std::fs;
use std::io;

fn read_username_from_file() -> Result<String, io::Error> {
    fs::read_to_string("hello.txt")
}
```

**示例 9-9：用 `fs::read_to_string` 代替先打开再读取文件**

　　把文件读入字符串相当常见，因此标准库提供了便捷的 `fs::read_to_string`：打开文件、创建新 `String`、读取内容并放入该 `String`，然后返回它。当然，直接用 `fs::read_to_string` 就没法把错误处理的各个步骤都讲清楚，所以我们先用了较长写法。

#### 何处可以使用 `?` 运算符

　　`?` 运算符只能用在返回类型与 `?` 所作用的值兼容的函数中。因为 `?` 被定义为像示例 9-6 中的 `match` 那样从函数中提前返回一个值。在示例 9-6 里，`match` 使用的是 `Result`，提前返回的分支返回 `Err(e)`。函数的返回类型必须是 `Result`，才能与这种 `return` 兼容。

　　示例 9-10 展示了若在返回类型与 `?` 所作用值不兼容的 `main` 中使用 `?`，会得到怎样的错误。

**文件名：`src/main.rs`**
```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")?;
}
```

**示例 9-10：在返回 `()` 的 `main` 中使用 `?` 无法通过编译。**

　　这段代码打开文件，操作可能失败。`?` 跟在 `File::open` 返回的 `Result` 后面，但这个 `main` 的返回类型是 `()`，不是 `Result`。编译时会得到如下错误信息：

```console
$ cargo run
   Compiling error-handling v0.1.0 (file:///projects/error-handling)
error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option` (or another type that implements `FromResidual`)
 --> src/main.rs:4:48
  |
3 | fn main() {
  | --------- this function should return `Result` or `Option` to accept `?`
4 |     let greeting_file = File::open("hello.txt")?;
  |                                                ^ cannot use the `?` operator in a function that returns `()`
  |
help: consider adding return type
  |
3 ~ fn main() -> Result<(), Box<dyn std::error::Error>> {
4 |     let greeting_file = File::open("hello.txt")?;
5 +     Ok(())
  |

For more information about this error, try `rustc --explain E0277`.
error: could not compile `error-handling` (bin "error-handling") due to 1 previous error
```

　　该错误指出：只有在返回 `Result`、`Option` 或实现了 `FromResidual` 的其他类型的函数中，才允许使用 `?`。

　　要修复错误，有两个选择。一是在没有限制的前提下，把函数返回类型改成与你对之使用 `?` 的值兼容；二是用 `match` 或某个 `Result<T, E>` 方法，以合适的方式处理该 `Result<T, E>`。

　　错误信息还提到，`?` 也可用于 `Option<T>` 值。与在 `Result` 上使用 `?` 一样，只有在返回 `Option` 的函数中才能对 `Option` 使用 `?`。对 `Option<T>` 调用 `?` 的行为与对 `Result<T, E>` 类似：若值是 `None`，则在该点提前从函数返回 `None`；若是 `Some`，则表达式的结果是 `Some` 里的值，函数继续。示例 9-11 是一个在给定文本中查找第一行最后一个字符的函数示例。

```rust
fn last_char_of_first_line(text: &str) -> Option<char> {
    text.lines().next()?.chars().last()
}
```

**示例 9-11**


　　该函数返回 `Option<char>`，因为那里可能有字符，也可能没有。代码取得字符串切片参数 `text`，对其调用 `lines`，得到按行迭代的迭代器。由于只关心第一行，对迭代器调用 `next` 以取得第一个值。若 `text` 是空字符串，`next` 会返回 `None`，我们用 `?` 停止并从 `last_char_of_first_line` 返回 `None`。若 `text` 非空，`next` 返回包含第一行字符串切片的 `Some`。

　　`?` 取出该字符串切片后，我们对其调用 `chars` 得到字符迭代器。我们关心第一行的最后一个字符，因此调用 `last` 返回迭代器中的最后一项。这也是一个 `Option`，因为第一行可能是空字符串——例如 `text` 以空行开头但后面还有字符，如 `"\nhi"`。若第一行确有最后一个字符，则会在 `Some` 变体中返回。中间的 `?` 让我们能简洁表达这套逻辑，从而把函数写成一行。若不能对 `Option` 使用 `?`，就得用更多方法调用或 `match` 来实现。

　　注意：可以在返回 `Result` 的函数里对 `Result` 使用 `?`，也可以在返回 `Option` 的函数里对 `Option` 使用 `?`，但不能混用。`?` 不会自动把 `Result` 转成 `Option` 或反过来；那种情况下可用 `Result` 的 `ok` 方法或 `Option` 的 `ok_or` 方法显式转换。

　　到目前为止，我们用过的 `main` 都返回 `()`。`main` 很特殊：它是可执行程序的入口与出口，其返回类型受限制，程序才能按预期表现。

　　幸运的是，`main` 也可以返回 `Result<(), E>`。示例 9-12 是示例 9-10 的代码，但我们把 `main` 的返回类型改成了 `Result<(), Box<dyn Error>>`，并在末尾加上返回值 `Ok(())`。这段代码现在可以编译了。

**文件名：`src/main.rs`**

```rust
use std::error::Error;
use std::fs::File;

fn main() -> Result<(), Box<dyn Error>> {
    let greeting_file = File::open("hello.txt")?;

    Ok(())
}
```

**示例 9-12**


　　`Box<dyn Error>` 是一种 trait 对象，我们会在第 18 章[「用 Trait 对象抽象共享行为」][trait-objects]中讨论。眼下可以把 `Box<dyn Error>` 读作“任意种类的错误”。在错误类型为 `Box<dyn Error>` 的 `main` 中对 `Result` 使用 `?` 是允许的，因为任何 `Err` 值都可以提前返回。即便这个 `main` 函数体目前只会返回 `std::io::Error` 类型的错误，指定 `Box<dyn Error>` 也能保证：将来若在 `main` 中加入返回其他错误的代码，该签名仍然正确。

　　当 `main` 返回 `Result<(), E>` 时，若 `main` 返回 `Ok(())`，可执行文件以值 `0` 退出；若返回 `Err`，则以非零值退出。用 C 编写的可执行文件退出时返回整数：成功返回整数 `0`，出错返回非 `0` 整数。Rust 的可执行文件也返回整数，以兼容这一惯例。

　　`main` 可以返回任何实现了 [`std::process::Termination` trait][termination] 的类型，该 trait 包含返回 `ExitCode` 的函数 `report`。如何为自己的类型实现 `Termination`，请参阅标准库文档。

　　既然已经讨论了调用 `panic!` 与返回 `Result` 的细节，接下来回到这个话题：在哪些情况下该选哪一种。

[handle_failure]: ../../guessing-game/#handling-potential-failure-with-result
[trait-objects]: ../../oop/02-trait-objects/#using-trait-objects-to-abstract-over-shared-behavior
[termination]: https://doc.rust-lang.org/std/process/trait.Termination.html
