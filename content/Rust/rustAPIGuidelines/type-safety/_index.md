+++
title = "第7章 类型安全"
date = 2026-08-18T21:50:00+08:00
weight = 90
type = "docs"
description = "类型安全 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/type-safety.html](https://rust-lang.github.io/api-guidelines/type-safety.html)

# 类型安全

## Newtype 提供静态区分 (C-NEWTYPE) {#c-newtype}

Newtype 可以在静态层面区分同一底层类型的不同解释。

例如，一个 `f64` 值既可能表示英里数，也可能表示千米数。使用 newtype，我们可以跟踪其预期解释：

```rust
struct Miles(pub f64);
struct Kilometers(pub f64);

impl Miles {
    fn to_kilometers(self) -> Kilometers { /* ... */ }
}
impl Kilometers {
    fn to_miles(self) -> Miles { /* ... */ }
}
```

一旦将这两种类型分开，就可以静态确保不会把它们弄混。例如，函数

```rust
fn are_we_there_yet(distance_travelled: Miles) -> bool { /* ... */ }
```

不会被意外地用 `Kilometers` 值调用。编译器会提醒我们进行转换，从而避免某些 [catastrophic bugs]。

[catastrophic bugs]: http://en.wikipedia.org/wiki/Mars_Climate_Orbiter

## 参数通过类型传达含义，而非 `bool` 或 `Option` (C-CUSTOM-TYPE) {#c-custom-type}

优先

```rust
let w = Widget::new(Small, Round)
```

而不是

```rust
let w = Widget::new(true, false)
```

像 `bool`、`u8` 和 `Option` 这样的核心类型可以有许多种解释。

应使用特意设计的类型（无论是枚举、结构体还是元组）来传达解释和不变量。在上面的例子中，若不查看参数名，很难立刻明白 `true` 和 `false` 在传达什么，而 `Small` 和 `Round` 则更有提示性。

使用自定义类型也更容易在日后扩展选项，例如增加一个 `ExtraLarge` 变体。

关于用零成本方式为已有类型包上一层可区分名称，见 newtype 模式（[C-NEWTYPE]）。

[C-NEWTYPE]: #c-newtype

## 一组标志使用 `bitflags` 而非枚举 (C-BITFLAG) {#c-bitflag}

Rust 支持带有显式指定判别值的 `enum` 类型：

```rust
enum Color {
    Red = 0xff0000,
    Green = 0x00ff00,
    Blue = 0x0000ff,
}
```

当 `enum` 类型需要被序列化为与其他系统/语言兼容的整数值时，自定义判别值很有用。它们支持「类型安全」的 API：函数接受 `Color` 而非整数，即可保证得到格式正确的输入，即便随后把这些输入当作整数使用。

`enum` 允许 API 从多个选项中恰好请求一个。有时 API 的输入反而是一组标志的存在与否。在 C 代码中，这通常通过让每个标志对应特定的位来完成，从而用单个整数表示例如 32 或 64 个标志。Rust 的 [`bitflags`] crate 为这种模式提供了类型安全的表示。

[`bitflags`]: https://github.com/bitflags/bitflags

```rust
use bitflags::bitflags;

bitflags! {
    struct Flags: u32 {
        const FLAG_A = 0b00000001;
        const FLAG_B = 0b00000010;
        const FLAG_C = 0b00000100;
    }
}

fn f(settings: Flags) {
    if settings.contains(Flags::FLAG_A) {
        println!("doing thing A");
    }
    if settings.contains(Flags::FLAG_B) {
        println!("doing thing B");
    }
    if settings.contains(Flags::FLAG_C) {
        println!("doing thing C");
    }
}

fn main() {
    f(Flags::FLAG_A | Flags::FLAG_C);
}
```

## Builder 使复杂值的构造成为可能 (C-BUILDER) {#c-builder}

某些数据结构构造起来很复杂，因为构造过程需要：

* 大量输入
* 复合数据（例如切片）
* 可选的配置数据
* 在若干种风格之间选择

这很容易导致大量彼此不同、且各自带有许多参数的构造函数。

如果 `T` 是这样的数据结构，考虑引入一个 `T` 的 *builder*：

1. 引入一个单独的数据类型 `TBuilder`，用于逐步配置 `T` 值。在可能的情况下选择更好的名称：例如 [`Command`] 是 [child process] 的 builder，[`Url`] 可由 [`ParseOptions`] 创建。
2. builder 的构造函数应当只把构造 `T` 所*必需*的数据作为参数。
3. builder 应当提供一套便于配置的方法，包括逐步设置复合输入（如切片）。这些方法应当返回 `self` 以支持链式调用。
4. builder 应当提供一个或多个「*终结*」方法，用于实际构建 `T`。

[`Command`]: https://doc.rust-lang.org/std/process/struct.Command.html
[child process]: https://doc.rust-lang.org/std/process/struct.Child.html
[`Url`]: https://docs.rs/url/1.4.0/url/struct.Url.html
[`ParseOptions`]: https://docs.rs/url/1.4.0/url/struct.ParseOptions.html

当构建 `T` 涉及副作用（例如生成任务或启动进程）时，builder 模式尤其合适。

在 Rust 中，builder 模式有两种变体，区别在于对所有权的处理，如下所述。

### 非消耗式 builder（首选）

在某些情况下，构造最终的 `T` 并不需要消耗 builder 本身。下面这个 [`std::process::Command`] 的变体就是一个例子：

[`std::process::Command`]: https://doc.rust-lang.org/std/process/struct.Command.html

```rust
// 注意：实际的 Command API 并不使用拥有所有权的 String；
// 这是一个简化版本。

pub struct Command {
    program: String,
    args: Vec<String>,
    cwd: Option<String>,
    // 等等
}

impl Command {
    pub fn new(program: String) -> Command {
        Command {
            program: program,
            args: Vec::new(),
            cwd: None,
        }
    }

    /// 添加一个传给程序的参数。
    pub fn arg(&mut self, arg: String) -> &mut Command {
        self.args.push(arg);
        self
    }

    /// 添加多个传给程序的参数。
    pub fn args(&mut self, args: &[String]) -> &mut Command {
        self.args.extend_from_slice(args);
        self
    }

    /// 设置子进程的工作目录。
    pub fn current_dir(&mut self, dir: String) -> &mut Command {
        self.cwd = Some(dir);
        self
    }

    /// 将命令作为子进程执行，并返回该子进程。
    pub fn spawn(&self) -> io::Result<Child> {
        /* ... */
    }
}
```

注意，真正使用 builder 配置来生成进程的 `spawn` 方法，以共享引用接受 builder。这之所以可行，是因为生成进程并不需要配置数据的所有权。

因为终结方法 `spawn` 只需要引用，配置方法接受并返回 `self` 的可变借用。

#### 好处

由于全程使用借用，`Command` 可以方便地用于单行写法以及更复杂的构造：

```rust
// 单行写法
Command::new("/bin/cat").arg("file.txt").spawn();

// 复杂配置
let mut cmd = Command::new("/bin/ls");
if size_sorted {
    cmd.arg("-S");
}
cmd.arg(".");
cmd.spawn();
```

### 消耗式 builder

有时 builder 在构造最终类型 `T` 时必须转移所有权，这意味着终结方法必须接受 `self` 而非 `&self`。

```rust
impl TaskBuilder {
    /// 为即将创建的任务命名。
    pub fn named(mut self, name: String) -> TaskBuilder {
        self.name = Some(name);
        self
    }

    /// 重定向任务本地的 stdout。
    pub fn stdout(mut self, stdout: Box<io::Write + Send>) -> TaskBuilder {
        self.stdout = Some(stdout);
        self
    }

    /// 创建并执行一个新的子任务。
    pub fn spawn<F>(self, f: F) where F: FnOnce() + Send {
        /* ... */
    }
}
```

这里，`stdout` 配置涉及传递 `io::Write` 的所有权，该所有权必须在构造时（在 `spawn` 中）转移给任务。

当 builder 的终结方法需要所有权时，存在一个基本权衡：

* 如果其他 builder 方法接受/返回可变借用，复杂配置会很顺畅，但单行配置将变得不可能。

* 如果其他 builder 方法接受/返回拥有所有权的 `self`，单行写法仍然好用，但复杂配置会不太方便。

在「让简单的事情简单、让困难的事情成为可能」这一原则下，消耗式 builder 的所有方法都应当接受并返回拥有所有权的 `self`。于是客户端代码如下所示：

```rust
// 单行写法
TaskBuilder::new("my_task").spawn(|| { /* ... */ });

// 复杂配置
let mut task = TaskBuilder::new();
task = task.named("my_task_2"); // 必须重新赋值以保留所有权
if reroute {
    task = task.stdout(mywriter);
}
task.spawn(|| { /* ... */ });
```

单行写法与之前一样有效，因为所有权会穿过每一个 builder 方法，直到被 `spawn` 消耗。然而，复杂配置会更啰嗦：每一步都需要重新赋值 builder。
