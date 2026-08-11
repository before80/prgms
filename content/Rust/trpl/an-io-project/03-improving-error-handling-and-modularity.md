+++
title = "12.3 重构以改进模块化与错误处理"
date = 2026-08-05T08:44:00+08:00
weight = 52
type = "docs"
description = "分离关注点、Config 结构体与 Result 错误处理重构"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 重构以改进模块化与错误处理


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-03-improving-error-handling-and-modularity.html](https://doc.rust-lang.org/stable/book/ch12-03-improving-error-handling-and-modularity.html)


## 重构以改进模块化与错误处理

　　为改进程序，我们要解决四个与程序结构及潜在错误处理相关的问题。第一，`main` 现在做两件事：解析参数和读取文件。随着程序增长，`main` 处理的独立任务会越来越多。职责越多，就越难推理、越难测试，也越难在不破坏某部分的前提下修改。最好分离功能，让每个函数只负责一项任务。

　　这一点也关联到第二个问题：虽然 `query` 和 `file_path` 是程序的配置变量，像 `contents` 这样的变量却用于执行程序逻辑。`main` 越长，需要管理的变量就越多；变量越多，就越难记住各自的作用。最好把配置变量归入一个结构，使其用途清晰。

　　第三个问题是：读取文件失败时我们用 `expect` 打印错误信息，但信息只是 `Should have been able to read the file`。读文件失败的原因可能有很多：例如文件不存在，或没有打开权限。眼下无论情况如何都打印同一条信息，对用户毫无帮助！

　　第四，我们用 `expect` 处理错误；若用户运行程序时未提供足够参数，会得到 Rust 的 `index out of bounds` 错误，并不能清楚说明问题。最好把所有错误处理代码放在一处，这样将来维护者若要改错误处理逻辑只需看一个地方。把错误处理集中起来，也能确保打印的信息对终端用户有意义。

　　下面通过重构来解决这四个问题。

### 在二进制项目中分离关注点 {#separation-of-concerns-for-binary-projects}

　　把多项任务的责任都塞进 `main` 的组织问题，在许多二进制项目中都很常见。因此，当 `main` 开始变大时，许多 Rust 程序员会把二进制程序的不同关注点拆开。这一过程通常包含下列步骤：

- 把程序拆成 *main.rs* 和 *lib.rs*，并把程序逻辑移到 *lib.rs*。
- 只要命令行解析逻辑还很小，就可以留在 `main` 中。
- 当命令行解析逻辑开始变复杂时，再从 `main` 提取到其他函数或类型中。

　　完成这一过程后，留在 `main` 中的职责应限于：

- 用参数值调用命令行解析逻辑
- 设置其他任何配置
- 调用 *lib.rs* 中的 `run` 函数
- 若 `run` 返回错误则处理该错误

　　这种模式旨在分离关注点：*main.rs* 负责运行程序，*lib.rs* 负责当前任务的全部逻辑。由于不能直接测试 `main`，这种结构通过把逻辑移出 `main`，让你能测试程序的全部逻辑。留在 `main` 中的代码会小到足以通过阅读来验证正确性。我们按这个过程改写程序。

#### 提取参数解析器

　　把解析参数的功能提取到 `main` 会调用的函数中。示例 12-5 展示了新的 `main` 开头：它调用我们将在 *src/main.rs* 中定义的新函数 `parse_config`。

**文件名：`src/main.rs`**
```rust
fn main() {
    let args: Vec<String> = env::args().collect();

    let (query, file_path) = parse_config(&args);

    // --snip--

}

fn parse_config(args: &[String]) -> (&str, &str) {
    let query = &args[1];
    let file_path = &args[2];

    (query, file_path)
}
```

**示例 12-5：从 `main` 中提取 `parse_config` 函数**

　　我们仍把命令行参数收集进向量，但不再在 `main` 里把索引 1 赋给 `query`、索引 2 赋给 `file_path`，而是把整个向量传给 `parse_config`。由 `parse_config` 决定哪个参数进哪个变量，再把值传回 `main`。`main` 里仍创建 `query` 和 `file_path` 变量，但不再负责弄清命令行参数与变量如何对应。

　　对这么小的程序，这次改动或许显得小题大做，但我们是以小步、增量的方式重构。改完后再运行程序，确认参数解析仍然正常。经常检查进度有助于在问题出现时定位原因。

#### 将配置值分组

　　还可以再迈一小步改进 `parse_config`。目前我们返回元组，却立刻又拆成各个部分——这往往说明抽象还不对。

　　另一个改进信号是函数名里的 `config`：它暗示返回的两个值相关，且都属于同一个配置值。目前除了把两者放进元组，数据结构并未传达这层含义；我们改为把两个值放进一个结构体，并为每个字段起有意义的名字。这样将来的维护者更容易理解各值如何关联、各自用途是什么。

　　示例 12-6 展示了对 `parse_config` 的改进。

**文件名：`src/main.rs`**
```rust
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = parse_config(&args);

    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);

    let contents = fs::read_to_string(config.file_path)
        .expect("Should have been able to read the file");

    // --snip--

}

struct Config {
    query: String,
    file_path: String,
}

fn parse_config(args: &[String]) -> Config {
    let query = args[1].clone();
    let file_path = args[2].clone();

    Config { query, file_path }
}
```

**示例 12-6：重构 `parse_config`，使其返回 `Config` 结构体实例**

　　我们添加了名为 `Config`、字段为 `query` 和 `file_path` 的结构体。`parse_config` 的签名现在表明它返回 `Config` 值。在函数体中，以前返回的是引用 `args` 中 `String` 的字符串切片；现在定义 `Config` 包含自有的 `String` 值。`main` 中的 `args` 拥有参数值的所有权，只是把它们借给 `parse_config`；若 `Config` 试图取得 `args` 中值的所有权，就会违反 Rust 的借用规则。

　　管理这些 `String` 数据的方式有多种；最简单但略低效的做法是对值调用 `clone`。这会为 `Config` 实例复制一份完整数据，比存储对字符串数据的引用更耗时、更占内存。不过克隆也让代码非常直接，因为不必管理引用的生命周期；在这种情况下，牺牲一点性能换取简单性是值得的权衡。

> ### 使用 `clone` 的权衡
>
> 许多 Rustacean 倾向于避免用 `clone` 解决所有权问题，因为它有运行时开销。在 [第 13 章][ch13]，你会学到这类情形下更高效的方法。但眼下复制几个字符串以便继续推进完全可以——这些复制只会发生一次，而且文件路径和查询字符串都很短。有一个略低效但能工作的程序，好过第一次就过度优化。随着对 Rust 更熟悉，你会更容易一开始就采用最高效的方案；现在调用 `clone` 完全可以接受。

　　我们更新了 `main`：把 `parse_config` 返回的 `Config` 实例放进名为 `config` 的变量，并把原先使用独立 `query` 和 `file_path` 变量的代码改为使用 `Config` 结构体上的字段。

　　现在代码更清楚地表明：`query` 和 `file_path` 相关，其用途是配置程序如何工作。任何使用这些值的代码都知道到 `config` 实例中、按用途命名的字段里去找。

#### 为 `Config` 创建构造函数

　　到目前为止，我们把解析命令行参数的逻辑从 `main` 抽到了 `parse_config`。这帮助我们看出 `query` 和 `file_path` 相关，且这种关系应在代码中体现。随后我们添加了 `Config` 结构体，为相关用途命名，并让 `parse_config` 能以结构体字段名返回这些值。

　　既然 `parse_config` 的目的就是创建 `Config` 实例，就可以把它从普通函数改成与 `Config` 关联的名为 `new` 的函数。这样更地道：标准库中像 `String` 这样的类型可通过调用 `String::new` 创建实例；同理，把 `parse_config` 改成与 `Config` 关联的 `new` 后，就可以通过 `Config::new` 创建实例。示例 12-7 展示需要的改动。

**文件名：`src/main.rs`**
```rust
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::new(&args);

    // --snip--
}

// --snip--


impl Config {
    fn new(args: &[String]) -> Config {
        let query = args[1].clone();
        let file_path = args[2].clone();

        Config { query, file_path }
    }
}
```

**示例 12-7：把 `parse_config` 改成 `Config::new`**

　　我们把 `main` 中对 `parse_config` 的调用改成 `Config::new`，把函数名改为 `new` 并移入 `impl` 块，使其与 `Config` 关联。再编译一次，确认能工作。

### 修复错误处理

　　现在着手修复错误处理。回想一下：若 `args` 向量少于三项，访问索引 1 或 2 会导致程序 panic。试着不带任何参数运行，会看到类似这样的结果：

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep`

thread 'main' (6023615) panicked at src/main.rs:27:21:
index out of bounds: the len is 1 but the index is 1
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　`index out of bounds: the len is 1 but the index is 1` 这类信息是写给程序员的，帮不了终端用户弄清该怎么做。我们来修好它。

#### 改进错误信息

　　在示例 12-8 中，我们在 `new` 里加入检查：在访问索引 1 和 2 之前确认切片足够长。若不够长，程序 panic 并显示更好的错误信息。

**文件名：`src/main.rs`**
```rust
    // --snip--
    fn new(args: &[String]) -> Config {
        if args.len() < 3 {
            panic!("not enough arguments");
        }
        // --snip--
```

**示例 12-8：增加对参数数量的检查**

　　这段代码类似于 [示例 9-13 中写的 `Guess::new` 函数][ch9-custom-types]：当 `value` 超出有效范围时调用 `panic!`。这里不是检查值域，而是检查 `args` 的长度至少为 `3`，之后函数体就可以假定该条件已满足。若 `args` 少于三项，条件为 `true`，我们调用 `panic!` 立即结束程序。

　　在 `new` 中加了这几行后，再不带参数运行，看看错误现在是什么样：

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep`

thread 'main' (6023776) panicked at src/main.rs:26:13:
not enough arguments
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　输出好多了：现在有了合理的错误信息。不过还有一些不想给用户看的多余信息。也许示例 9-13 用的技巧在这里并非最佳：调用 `panic!` 更适合编程问题，而不是用法问题，[正如第 9 章所讨论的][ch9-error-guidelines]。我们改用第 9 章学过的另一种技巧——[返回 `Result`][ch9-result]，以表示成功或错误。

#### 返回 `Result` 而不是调用 `panic!`

　　我们可以改为返回 `Result`：成功时包含 `Config` 实例，失败时描述问题。同时把函数名从 `new` 改为 `build`，因为许多程序员期望 `new` 永不失败。当 `Config::build` 与 `main` 通信时，可用 `Result` 表明出了问题。然后可以让 `main` 把 `Err` 变体转成对用户更实用的错误，而不会出现 `panic!` 带来的 `thread 'main'` 和 `RUST_BACKTRACE` 等周围文字。

　　示例 12-9 展示了现在称为 `Config::build` 的函数在返回值与函数体上需要的改动，以便返回 `Result`。注意在更新 `main` 之前这还无法编译，我们会在下一示例中更新 `main`。

**文件名：`src/main.rs`**
```rust
impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let file_path = args[2].clone();

        Ok(Config { query, file_path })
    }
}
```

**示例 12-9：从 `Config::build` 返回 `Result`**

　　`build` 在成功时返回含 `Config` 实例的 `Result`，在错误时返回字符串字面量。错误值始终是具有 `'static` 生命周期的字符串字面量。

　　函数体有两处改动：用户参数不够时不再调用 `panic!`，而是返回 `Err`；并把 `Config` 返回值包在 `Ok` 里。这些改动使函数符合新的类型签名。

　　从 `Config::build` 返回 `Err` 让 `main` 能处理 `build` 返回的 `Result`，并在出错时更干净地退出进程。

#### 调用 `Config::build` 并处理错误

　　要处理错误情况并打印对用户友好的信息，需要更新 `main` 以处理 `Config::build` 返回的 `Result`，如示例 12-10。我们还会亲手实现以非零错误码退出命令行工具的职责，而不再依赖 `panic!`。非零退出状态是一种约定，用来向调用我们程序的进程表明程序以错误状态退出。

**文件名：`src/main.rs`**
```rust
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        println!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    // --snip--
```

**示例 12-10：若构建 `Config` 失败则以错误码退出**

　　本示例使用了尚未详细讲过的方法：标准库为 `Result<T, E>` 定义的 `unwrap_or_else`。它允许我们定义自定义的、非 `panic!` 的错误处理。若 `Result` 是 `Ok`，行为类似 `unwrap`：返回 `Ok` 包装的内部值。若是 `Err`，则调用闭包中的代码——闭包是我们定义并作为参数传给 `unwrap_or_else` 的匿名函数。闭包会在 [第 13 章][ch13] 详细讲解。眼下只需知道：`unwrap_or_else` 会把 `Err` 的内部值（这里是示例 12-9 中添加的静态字符串 `"not enough arguments"`）传给我们写在竖线之间的参数 `err`。闭包运行时可使用该 `err` 值。

　　我们新增一行 `use`，把标准库的 `process` 引入作用域。错误情况下运行的闭包只有两行：打印 `err`，然后调用 `process::exit`。`process::exit` 会立即停止程序，并把传入的数字作为退出状态码返回。这与示例 12-8 基于 `panic!` 的处理类似，但不再有那些多余输出。试一下：

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/minigrep`
Problem parsing arguments: not enough arguments
```

　　很好！这对用户友好多了。

### 从 `main` 中提取逻辑

　　配置解析的重构完成后，转向程序逻辑。正如 [「在二进制项目中分离关注点」](#separation-of-concerns-for-binary-projects) 所述，我们将提取名为 `run` 的函数，容纳 `main` 中当前所有与设置配置或处理错误无关的逻辑。完成后，`main` 会简洁到易于通过阅读验证，而我们也能为其余全部逻辑编写测试。

　　示例 12-11 展示提取 `run` 函数这一小步增量改进。

**文件名：`src/main.rs`**
```rust
fn main() {
    // --snip--


    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);

    run(config);
}

fn run(config: Config) {
    let contents = fs::read_to_string(config.file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");
}

// --snip--
```

**示例 12-11：提取包含其余程序逻辑的 `run` 函数**

　　`run` 现在包含从读取文件开始的、`main` 中剩余的全部逻辑。它以 `Config` 实例为参数。

#### 从 `run` 返回错误

　　程序逻辑分离进 `run` 后，可以像示例 12-9 对 `Config::build` 那样改进错误处理。不再通过调用 `expect` 让程序 panic，`run` 在出错时返回 `Result<T, E>`。这样可以把错误处理逻辑进一步集中到 `main`，并以对用户友好的方式处理。示例 12-12 展示了 `run` 签名与函数体需要的改动。

**文件名：`src/main.rs`**
```rust
use std::error::Error;

// --snip--


fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    println!("With text:\n{contents}");

    Ok(())
}
```

**示例 12-12：把 `run` 函数改为返回 `Result`**

　　这里有三处重要改动。第一，把 `run` 的返回类型改成 `Result<(), Box<dyn Error>>`。该函数以前返回单元类型 `()`，成功时我们仍返回这个值。

　　对于错误类型，我们使用特征对象 `Box<dyn Error>`（并在顶部用 `use` 引入了 `std::error::Error`）。特征对象将在 [第 18 章][ch18] 讲解。眼下只需知道：`Box<dyn Error>` 表示函数会返回某个实现了 `Error` 特征的类型，但不必指明具体是哪一种。这让我们能在不同错误情形下返回不同类型的错误值。`dyn` 是 *dynamic*（动态）的缩写。

　　第二，我们去掉了对 `expect` 的调用，改用 [第 9 章][ch9-question-mark] 讲过的 `?` 运算符。出错时 `?` 不会 `panic!`，而是把错误值从当前函数返回给调用者处理。

　　第三，成功时 `run` 现在返回 `Ok` 值。签名中成功类型声明为 `()`，因此需要把单元类型值包在 `Ok` 里。`Ok(())` 语法起初可能有点怪，但像这样使用 `()` 是惯用写法，表示我们调用 `run` 只为副作用，并不需要它返回有用值。

　　运行这段代码时能编译，但会显示警告：

```console
$ cargo run -- the poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
warning: unused `Result` that must be used
  --> src/main.rs:19:5
   |
19 |     run(config);
   |     ^^^^^^^^^^^
   |
   = note: this `Result` may be an `Err` variant, which should be handled
   = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
   |
19 |     let _ = run(config);
   |     +++++++

warning: `minigrep` (bin "minigrep") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.71s
     Running `target/debug/minigrep the poem.txt`
Searching for the
In file poem.txt
With text:
I'm nobody! Who are you?
Are you nobody, too?
Then there's a pair of us - don't tell!
They'd banish us, you know.

How dreary to be somebody!
How public, like a frog
To tell your name the livelong day
To an admiring bog!
```

　　Rust 告诉我们忽略了 `Result` 值，而它可能表示发生了错误。我们没有检查是否真有错误，编译器提醒这里大概本该有错误处理代码！现在来修正。

#### 在 `main` 中处理 `run` 返回的错误

　　我们用与示例 12-10 处理 `Config::build` 类似、但略有不同的技巧来检查并处理错误：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    // --snip--


    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);

    if let Err(e) = run(config) {
        println!("Application error: {e}");
        process::exit(1);
    }
}
```

　　我们用 `if let` 而不是 `unwrap_or_else` 来检查 `run` 是否返回 `Err`，若是则调用 `process::exit(1)`。`run` 并不像 `Config::build` 那样返回我们想要 `unwrap` 的值。成功时 `run` 返回 `()`，我们只关心检测错误，不需要 `unwrap_or_else` 返回被解开的值（那也只是 `()`）。

　　两种情况下 `if let` 与 `unwrap_or_else` 的函数体相同：打印错误并退出。

### 把代码拆进库 crate

　　到目前为止，`minigrep` 项目看起来不错！现在把 *src/main.rs* 拆开，把部分代码放进 *src/lib.rs*。这样就能测试代码，并让 *src/main.rs* 职责更少。

　　我们把负责搜索文本的代码定义在 *src/lib.rs* 而不是 *src/main.rs*，这样我们（或任何使用 `minigrep` 库的人）就能在比 `minigrep` 二进制更多的场景下调用搜索函数。

　　首先在 *src/lib.rs* 中定义 `search` 函数签名，如示例 12-13，函数体调用 `unimplemented!` 宏。填入实现时再详细解释该签名。

**文件名：`src/lib.rs`**
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    unimplemented!();
}
```

**示例 12-13：在 *src/lib.rs* 中定义 `search` 函数**

　　我们在函数定义上使用了 `pub`，把 `search` 标为库 crate 公共 API 的一部分。现在有了可从二进制 crate 使用、也可测试的库 crate！

　　接着需要把 *src/lib.rs* 中定义的代码引入 *src/main.rs* 二进制 crate 的作用域并调用它，如示例 12-14。

**文件名：`src/main.rs`**
```rust
// --snip--
use minigrep::search;

fn main() {
    // --snip--

}

// --snip--


fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    for line in search(&config.query, &contents) {
        println!("{line}");
    }

    Ok(())
}
```

**示例 12-14：在 *src/main.rs* 中使用 `minigrep` 库 crate 的 `search` 函数**

　　添加 `use minigrep::search`，把库 crate 中的 `search` 引入二进制 crate 作用域。然后在 `run` 中不再打印文件内容，而是调用 `search`，传入 `config.query` 和 `contents`。`run` 再用 `for` 循环打印 `search` 返回的每一行匹配结果。这也是去掉 `main` 中显示查询与文件路径的 `println!` 的好时机，让程序只打印搜索结果（若无错误发生）。

　　注意：搜索函数会先把所有结果收集进返回的向量，然后才打印。搜索大文件时，由于不会边找到边打印，显示结果可能较慢；第 13 章会讨论用迭代器修复这一问题的可能方式。

　　呼！工作量不小，但为将来的成功打下了基础。现在错误处理容易多了，代码也更模块化。从现在起，几乎所有工作都会在 *src/lib.rs* 中完成。

　　利用这新获得的模块化，做一件旧代码很难、新代码却很容易的事：写一些测试！

[ch13]: ../../functional-features/
[ch9-custom-types]: ../../error-handling/03-to-panic-or-not-to-panic/#creating-custom-types-for-validation
[ch9-error-guidelines]: ../../error-handling/03-to-panic-or-not-to-panic/#guidelines-for-error-handling
[ch9-result]: ../../error-handling/02-recoverable-errors-with-result/
[ch18]: ../../oop/
[ch9-question-mark]: ../../error-handling/02-recoverable-errors-with-result/#a-shortcut-for-propagating-errors-the--operator
