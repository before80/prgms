+++
title = "21-error-handling"
date = 2026-07-28T14:49:00+08:00
weight = 210
type = "docs"
description = "面向 Go 初学者讲清 Rust 错误值、错误传播与 panic 的边界"
isCJKLanguage = true
draft = false

+++

# 错误处理 (Error Handling)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，因此会直接对比 Go 的 `error`、`panic` 和早返回习惯。
>
> 你会看到：什么时候用 `Option`，什么时候用 `Result`，什么时候该显式失败，什么时候该让程序直接停下。

开头先记住一条总规则：Rust 不是只有“报错”这一种失败通道，而是把“值缺席”“可恢复错误”“程序不变量被破坏”拆成了三套机制。你越早把这三件事分开，后面的 API 设计和读错编译器提示都会轻松很多。

## Q1. `Option<T>` 和 `Result<T, E>` 到底怎么分工？ {#q1}
**Tags:** `hot` `Option` `Result`
**适用版本:** Rust 1.0+

**一句话答案：** `Option<T>` 表示“可能没有值”，`Result<T, E>` 表示“失败时还要告诉你为什么失败”。

**解答：** `Option<T>` 更像 Go 里 `(v, ok)` 的语义：有值就 `Some(v)`，没值就 `None`。`Result<T, E>` 更像 `(v, err)`：成功是 `Ok(v)`，失败是 `Err(e)`。如果调用方需要根据失败原因决定重试、降级、提示用户，那就不要偷懒写成 `Option`。

```rust
fn first_even(values: &[i32]) -> Option<i32> {
    values.iter().copied().find(|n| n % 2 == 0)
}

fn parse_port(input: &str) -> Result<u16, std::num::ParseIntError> {
    input.parse::<u16>()
}

fn main() {
    assert_eq!(first_even(&[1, 3, 4, 7]), Some(4));
    assert_eq!(first_even(&[1, 3, 5]), None);

    println!("{:?}", parse_port("8080"));
    println!("{:?}", parse_port("abc"));
}
```

```rust
use std::fs;

fn read_port_bad(path: &str) -> Option<u16> {
    let text = fs::read_to_string(path).ok()?;
    text.trim().parse::<u16>().ok()
}

fn main() {
    let _ = read_port_bad("missing.txt");
}
```

第二个例子的问题不是“会不会崩”，而是“信息被吃掉了”。调用方拿到 `None` 时不知道是文件不存在、没有权限，还是端口字符串写错了。

**Go 对比：**
- Go 里常见两套形态：`v, ok := m[k]` 对应 `Option`，`v, err := f()` 对应 `Result`。
- Rust 把这两套语义拆成了不同类型，因此 API 一眼就能看出“值可能缺席”还是“会有错误对象”。
- Go 程序员最容易犯的错是把所有失败都先压成“空值”，结果后面无法分流处理。

**记忆点：**
- 缺席不是错误，用 `Option`。
- 失败原因重要时，用 `Result`。
- 不要为了省事把 `Result` 先 `.ok()` 掉。

## Q2. `?` 运算符到底替你省掉了什么代码？ {#q2}
**Tags:** `hot` `?` `Result`
**适用版本:** `Result` 的 `?` 自 Rust 1.13+；`Option` 的 `?` 自 Rust 1.22+

**一句话答案：** `?` 会在成功时拿出内部值，在失败时立刻把错误返回给调用者。

**解答：** 对 `Result` 来说，`expr?` 相当于“`Ok(v)` 就继续，`Err(e)` 就 `return Err(...)`”；对 `Option` 来说则是“`Some(v)` 就继续，`None` 就提前返回 `None`”。它最接近 Go 里反复写的 `if err != nil { return ..., err }`。

```rust
use std::fs;
use std::io;

fn first_line(path: &str) -> Result<String, io::Error> {
    let text = fs::read_to_string(path)?;
    Ok(text.lines().next().unwrap_or("").to_string())
}

fn main() {
    println!("{:?}", first_line("Cargo.toml"));
}
```

```rust
fn first_char_upper(input: &str) -> Option<char> {
    let ch = input.chars().next()?;
    Some(ch.to_ascii_uppercase())
}

fn main() {
    assert_eq!(first_char_upper("rust"), Some('R'));
    assert_eq!(first_char_upper(""), None);
}
```

如果你看到 `? couldn't convert the error` 之类的报错，意思通常不是 `?` 本身坏了，而是当前函数的返回错误类型接不住内层错误，这时要么改返回类型，要么用 `map_err` / `From` 做转换。

**Go 对比：**
- Go 里的等价心智模型就是早返回：拿到错误马上退出当前函数。
- Rust 的不同点是这件事由类型系统驱动，能否传播、传播成什么类型，编译器都会检查。
- Go 里常见的“忘了处理 err”在 Rust 里通常会直接变成类型错误或 unused result 警告。

**记忆点：**
- `?` 不是“忽略错误”，而是“传播错误”。
- `Result` 和 `Option` 都能用 `?`，但返回类型必须匹配。
- 错误类型接不住时，先看是不是该做类型转换。

## Q3. 为什么 `main` 也能返回 `Result`？ {#q3}
**Tags:** `hot` `main` `Result`
**适用版本:** Rust 1.26+

**一句话答案：** 因为 `main` 可以返回实现了 `Termination` 的类型，而 `Result<(), E>` 就是其中一种常用选择。

**解答：** 这意味着二进制入口可以像普通函数一样使用 `?`，失败时由运行时统一打印错误并返回非零退出码。对命令行程序尤其方便，因为你不用把所有错误都手写成 `match`。

```rust
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = fs::read_to_string("Cargo.toml")?;
    println!("config bytes = {}", config.len());
    Ok(())
}
```

```rust
fn run(flag: bool) -> Result<(), String> {
    if flag {
        Ok(())
    } else {
        Err("启动条件不满足".to_string())
    }
}

fn main() -> Result<(), String> {
    run(true)?;
    Ok(())
}
```

实际工程里，库代码通常定义精确错误类型；应用入口则常用 `Box<dyn Error>` 或统一错误类型，先把“正常结束还是失败退出”处理好。

**Go 对比：**
- Go 的 `main` 不能直接返回 `error`，所以大家常写 `if err := run(); err != nil { log.Fatal(err) }`。
- Rust 把这套模式内建进了 `main` 的返回约定里，因此入口函数也能自然使用 `?`。
- 如果你想自定义输出格式，Rust 也可以像 Go 一样手写 `run()` + `eprintln!` + `std::process::exit(1)`。

**记忆点：**
- 命令行程序入口优先考虑 `fn main() -> Result<(), E>`。
- `main` 返回 `Result` 的最大好处是能直接用 `?`。
- 库和应用入口的错误设计目标不一样。

## Q4. `unwrap()` 和 `expect()` 什么时候可以用？ {#q4}
**Tags:** `common` `unwrap` `expect`
**适用版本:** Rust 1.0+

**一句话答案：** 只有当失败代表程序逻辑被破坏，或者你正在写测试/原型代码时，才适合用它们。

**解答：** 这两个方法都会在 `None` 或 `Err` 时触发 **panic**（程序立即进入不可恢复失败流程）。`expect()` 比 `unwrap()` 多一个上下文字符串，因此更适合那些“按设计绝不该失败”的位置。

```rust
fn main() {
    let port: u16 = "8080".parse().expect("硬编码端口必须是合法 u16");
    println!("port = {port}");
}
```

```rust
fn user_name(input: Option<&str>) -> String {
    input.unwrap_or("anonymous").to_string()
}

fn main() {
    assert_eq!(user_name(Some("alice")), "alice");
    assert_eq!(user_name(None), "anonymous");
}
```

如果失败是外部输入导致的，比如读文件、访问网络、解析用户参数，优先考虑 `Result` 或默认值，而不是 `unwrap()`。

**Go 对比：**
- Go 里最像的写法是 `if err != nil { panic(err) }`。
- Rust 社区对 `unwrap()` 的容忍度和 Go 对 `panic()` 的容忍度类似：测试里常见，业务路径要谨慎。
- `expect()` 的提示语要写“为什么理论上不会失败”，而不是写“失败了”。

**记忆点：**
- 外部输入失败，不要 `unwrap()`。
- 不变量已保证时，可以 `expect()`。
- `expect()` 比裸 `unwrap()` 更利于排查。

## Q5. `panic!` 和返回 `Result` 的边界在哪？ {#q5}
**Tags:** `common` `panic` `Result`
**适用版本:** Rust 1.0+

**一句话答案：** 可恢复的失败用 `Result`，不该发生的程序错误才用 `panic!`。

**解答：** 如果调用方有办法处理失败，比如重试、跳过、提示用户、回滚事务，那就应该把失败建模成 `Result`。`panic!` 更像“程序已经处于错误状态，继续执行只会更糟”。

```rust
fn divide(a: i32, b: i32) -> Result<i32, &'static str> {
    if b == 0 {
        Err("除数不能为 0")
    } else {
        Ok(a / b)
    }
}

fn main() {
    println!("{:?}", divide(10, 2));
    println!("{:?}", divide(10, 0));
}
```

```rust
fn must_have_header(header: Option<&str>) -> &str {
    match header {
        Some(value) => value,
        None => panic!("内部协议错误：header 在进入此函数前必须已校验"),
    }
}

fn main() {
    println!("{}", must_have_header(Some("ok")));
}
```

把“用户输错了配置”写成 `panic!`，就像在 Go 里把业务校验失败全写成 `panic()` 一样，会让程序鲁棒性变差。

**Go 对比：**
- Go 的普遍约定也是：业务错误返回 `error`，真正的程序员错误才 `panic()`。
- Rust 更强调这条边界，因为 `panic!` 通常不在普通控制流里恢复。
- 如果库函数随便 panic，调用方会很难组合它。

**记忆点：**
- 业务失败可恢复，用 `Result`。
- 不变量破坏才 panic。
- 公共库 API 应尽量少 panic。

## Q6. `map_err`、`ok_or`、`transpose` 分别在什么场景下用？ {#q6}
**Tags:** `common` `map_err` `Option`
**适用版本:** `transpose` 自 Rust 1.33+

**一句话答案：** 它们都是“改壳不改值”的转换工具：改错误类型、把缺席转成错误、或把嵌套结构翻过来。

**解答：** `map_err` 用来改 `Err` 的类型；`ok_or` / `ok_or_else` 把 `Option` 变成 `Result`；`transpose` 常用在 `Option<Result<T, E>>` 和 `Result<Option<T>, E>` 之间转换。

```rust
fn parse_age(input: Option<&str>) -> Result<u8, String> {
    let text = input.ok_or_else(|| "缺少 age 字段".to_string())?;
    text.parse::<u8>()
        .map_err(|e| format!("age 不是合法整数: {e}"))
}

fn main() {
    println!("{:?}", parse_age(Some("18")));
    println!("{:?}", parse_age(None));
}
```

```rust
fn maybe_parse(input: Option<&str>) -> Result<Option<i32>, std::num::ParseIntError> {
    input.map(|s| s.parse::<i32>()).transpose()
}

fn main() {
    println!("{:?}", maybe_parse(Some("42")));
    println!("{:?}", maybe_parse(None));
}
```

如果你写出很多层 `match` 只是为了包一层类型，先看看是不是应该用这些组合子。

**Go 对比：**
- Go 没有标准库级别的等价组合子，通常是手写 `if err != nil` 和 `if !ok`。
- Rust 的组合子多，不是为了炫技巧，而是为了把“数据形状变化”写得清楚。
- Go 程序员转 Rust 时，最大的门槛不是语法，而是要习惯把这些小转换写成表达式。

**记忆点：**
- 改错误类型：`map_err`。
- 缺席变错误：`ok_or` / `ok_or_else`。
- 翻转嵌套：`transpose`。

## Q7. 怎么定义自己的错误类型，而不是到处返回 `String`？ {#q7}
**Tags:** `common` `custom-error`
**适用版本:** Rust 1.0+

**一句话答案：** 当调用方需要区分多类失败时，应该定义枚举错误类型，而不是把所有信息揉成字符串。

**解答：** 自定义错误的价值在于“调用方还能继续做判断”。只返回 `String` 时，你只能打印；定义枚举后，你可以根据变体分支处理、重试或转换成更高层错误。

```rust
use std::fs;

#[derive(Debug)]
enum ConfigError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
    Empty,
}

fn load_port(path: &str) -> Result<u16, ConfigError> {
    let text = fs::read_to_string(path).map_err(ConfigError::Io)?;
    let trimmed = text.trim();
    if trimmed.is_empty() {
        return Err(ConfigError::Empty);
    }
    trimmed.parse::<u16>().map_err(ConfigError::Parse)
}

fn main() {
    let _ = load_port("port.txt");
}
```

```rust
#[derive(Debug)]
enum ConfigError {
    MissingFile,
    InvalidPort,
}

fn advice(err: ConfigError) -> &'static str {
    match err {
        ConfigError::MissingFile => "请先创建配置文件",
        ConfigError::InvalidPort => "请把端口改成 1..=65535 的整数",
    }
}

fn main() {
    println!("{}", advice(ConfigError::InvalidPort));
}
```

如果调用方未来可能根据失败类型做不同动作，就值得把错误从 `String` 升级成自定义类型。

**Go 对比：**
- Go 里常见做法是导出 sentinel error、包装 error，或定义自定义 error type。
- Rust 的枚举更适合这种“固定几类失败”的情况，因为匹配分支是语言级能力。
- 如果你发现自己在字符串里搜关键词判断错误类型，说明设计已经开始跑偏。

**记忆点：**
- `String` 只适合临时程序或最外层输出。
- 可分支处理的错误，优先用枚举。
- 错误类型的核心价值是“保留结构化信息”。

## Q8. `From` 为什么能让 `?` 自动做错误转换？ {#q8}
**Tags:** `common` `From` `?`
**适用版本:** Rust 1.0+

**一句话答案：** 因为 `?` 在传播 `Err` 时会尝试调用 `From::from(e)`，把内层错误转成当前函数承诺返回的错误类型。

**解答：** 这就是为什么一个函数里能连续 `?` 多种错误来源，只要目标错误类型实现了对应的 `From<源错误>`。这不是魔法，而是标准 trait 在起作用。

```rust
use std::fs;

#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
}

impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Io(err)
    }
}

impl From<std::num::ParseIntError> for AppError {
    fn from(err: std::num::ParseIntError) -> Self {
        AppError::Parse(err)
    }
}

fn read_number(path: &str) -> Result<i32, AppError> {
    let text = fs::read_to_string(path)?;
    Ok(text.trim().parse::<i32>()?)
}

fn main() {
    let _ = read_number("number.txt");
}
```

写出这两个 `From` 实现后，`read_to_string` 的 `io::Error` 和 `parse` 的 `ParseIntError` 都能自动汇总进 `AppError`。

**Go 对比：**
- Go 没有 `?`，也没有 `From` 这种统一错误转换协议，通常靠显式包装 `fmt.Errorf("...: %w", err)`。
- Rust 的优势在于转换规则写一次，后面所有 `?` 都能复用。
- 但如果转换后丢掉上下文，问题和 Go 里只包一句 “failed” 一样，信息仍然不够。

**记忆点：**
- `?` 遇到 `Err` 时会尝试 `From::from`。
- 自定义错误聚合多个来源时，`From` 很关键。
- 自动转换不等于自动补上下文。

## Q9. 怎样给错误补上下文，而不是只看到“文件读取失败”？ {#q9}
**Tags:** `common` `context`
**适用版本:** Rust 1.0+

**一句话答案：** 要么在转换时显式把上下文写进新错误里，要么在边界层附加“正在做什么”的信息。

**解答：** 好的错误信息应该同时回答两件事：底层发生了什么，以及高层当时正在做什么。否则排查时会看到一堆重复的 `No such file or directory`，却不知道是哪一步出的错。

```rust
use std::fs;

fn load_config(path: &str) -> Result<String, String> {
    fs::read_to_string(path).map_err(|e| format!("读取配置文件 {path} 失败: {e}"))
}

fn main() {
    println!("{:?}", load_config("app.toml"));
}
```

```rust
#[derive(Debug)]
enum LoadError {
    ReadConfig {
        path: String,
        source: std::io::Error,
    },
}

fn main() {
    let sample = LoadError::ReadConfig {
        path: "app.toml".to_string(),
        source: std::io::Error::from(std::io::ErrorKind::NotFound),
    };
    println!("{:?}", sample);
}
```

第一种写法简单，适合边界层；第二种写法更结构化，适合库或大型系统。

**Go 对比：**
- Go 里常见模式是 `fmt.Errorf("load config %s: %w", path, err)`。
- Rust 里也要补这种“我当时正在干什么”的信息，不然错误链就会很平。
- 只保留底层错误对象，不补业务语境，排查体验并不会比 Go 更好。

**记忆点：**
- 错误要写“做什么时失败”，不只写“失败了”。
- 边界层可字符串包装，库层更适合结构化错误。
- 上下文越靠近出错现场越准确。

## Q10. `Box<dyn Error>` 适合用在什么位置？ {#q10}
**Tags:** `common` `dyn Error`
**适用版本:** Rust 1.0+

**一句话答案：** 它适合“把很多错误类型统一塞进一个返回口”的地方，尤其是应用入口和胶水层，不适合需要精确分支的库 API。

**解答：** `Box<dyn Error>` 把具体错误装箱成 trait object，调用方不再关心底层到底是 `io::Error`、解析错误还是你自己的错误枚举。这样写很省事，但也意味着丢掉了静态匹配能力。

```rust
use std::error::Error;
use std::fs;

fn run() -> Result<usize, Box<dyn Error>> {
    let text = fs::read_to_string("Cargo.toml")?;
    Ok(text.lines().count())
}

fn main() -> Result<(), Box<dyn Error>> {
    println!("{}", run()?);
    Ok(())
}
```

```rust
#[derive(Debug)]
enum DomainError {
    InvalidState,
    Timeout,
}

fn classify(err: DomainError) -> &'static str {
    match err {
        DomainError::InvalidState => "可以提示用户重试",
        DomainError::Timeout => "可以走重试策略",
    }
}

fn main() {
    println!("{}", classify(DomainError::Timeout));
}
```

如果调用方还需要 `match` 出具体失败类型，第二种精确错误类型通常比 `Box<dyn Error>` 更好。

**Go 对比：**
- Go 里的 `error` 接口天然就是动态分发，大家通过 `errors.Is` / `errors.As` 找回具体类型。
- Rust 默认更倾向于“能静态区分就静态区分”，`Box<dyn Error>` 是显式选择动态分发。
- 应用最外层常用，库公共接口要慎用。

**记忆点：**
- 入口层、胶水层适合 `Box<dyn Error>`。
- 需要精确分支时，优先具体错误类型。
- 动态统一换来方便，也会失去一部分类型信息。

## Q11. 错误链（error chain）有什么实际价值？ {#q11}
**Tags:** `common` `error-chain`
**适用版本:** Rust 1.0+

**一句话答案：** 错误链能同时保留高层语境和底层根因，让你既知道“哪一步失败了”，也知道“最终为什么失败”。

**解答：** Rust 的 `std::error::Error` trait 有 `source()`，就是为了把“当前错误由哪个更底层错误引起”串起来。真正有用的诊断信息，往往来自这条链，而不是某一层单独的错误字符串。

```rust
use std::error::Error;
use std::fmt;

#[derive(Debug)]
struct HighLevelError {
    msg: &'static str,
    source: std::io::Error,
}

impl fmt::Display for HighLevelError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.msg)
    }
}

impl Error for HighLevelError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

fn main() {
    let err = HighLevelError {
        msg: "加载配置失败",
        source: std::io::Error::from(std::io::ErrorKind::NotFound),
    };
    println!("{}", err);
    if let Some(source) = err.source() {
        println!("caused by: {}", source);
    }
}
```

这个模式的重点不在语法，而在信息分层：上层说业务动作，下层说系统细节。

**Go 对比：**
- Go 1.13 之后的 `%w`、`errors.Unwrap`、`errors.Is/As` 解决的是同一类问题。
- Rust 的 `source()` 也是为了保留包裹链，而不是只在最外层重新造一句新错误。
- 如果你每一层都把底层错误转成全新的字符串，错误链就断了。

**记忆点：**
- 高层描述动作，底层描述根因。
- 保留 `source()`，排查会快很多。
- 错误链一旦断掉，后面再想恢复几乎不可能。

## Q12. `catch_unwind` 和 `panic = "abort"` 分别该怎么理解？ {#q12}
**Tags:** `common` `panic` `catch_unwind`
**适用版本:** `catch_unwind` 自 Rust 1.9+

**一句话答案：** `catch_unwind` 只捕获“可展开（unwind）”的 panic；一旦把策略改成 `panic = "abort"`，进程会直接终止，`catch_unwind` 捕不到。

**解答：** 很多 Go 开发者会把 `catch_unwind` 想成 `recover()` 的近亲，但用途没有那么宽。Rust 的主流错误处理仍是 `Result`，`catch_unwind` 更多用于 FFI（**Foreign Function Interface，外部函数接口，用来和 C 等语言互调**）边界或宿主环境隔离。

默认 panic 策略是 `unwind`：运行时会沿栈展开，这时 `catch_unwind` 能收到 `Err`，调用方还有机会做隔离。

```rust
use std::panic::{self, AssertUnwindSafe};

fn main() {
    // 仅在 panic 策略为 unwind 时成立
    let result = panic::catch_unwind(AssertUnwindSafe(|| {
        panic!("boom");
    }));

    println!("caught = {}", result.is_err()); // true
}
```

如果你在 `Cargo.toml` 里改成 abort：

```toml
[profile.release]
panic = "abort"
```

含义就变了：panic 发生时**不走栈展开，直接终止进程**。于是：

1. 没有展开过程，析构和清理回调也不会按 unwind 路径跑完。
2. `catch_unwind` **捕不到**这次 panic——闭包里一旦 `panic!`，进程已经 abort，外层拿不到 `Err`，更谈不上“恢复后继续跑”。
3. 因此 `catch_unwind` 不是跨策略通用的异常网；它依赖 unwind，和 `panic = "abort"` 互斥。

`panic = "abort"` 常见于嵌入式或追求更小二进制体积的场景；选它就等于放弃“在进程内兜住 panic”的能力。业务失败请回到 `Result`，不要指望靠 `catch_unwind` 当 try/catch。

**Go 对比：**
- Go 的 `panic`/`recover` 是语言里明确的一套机制，常用于保护 goroutine 顶层。
- Rust 不鼓励把 panic 当业务异常系统，更多还是把它当“程序出大问题了”。
- 如果你真正想做的是普通失败传播，请回到 `Result`，不要绕去 `catch_unwind`。

**记忆点：**
- `catch_unwind` 只对 unwind 有效。
- `panic = "abort"` 下捕不到，进程直接终止。
- 业务失败用 `Result`，不要滥用 panic 机制。

## Q13. Rust 没有 exception，错误到底该怎么往上抛？ {#q13}
**Tags:** `hot` `Result` `?`
**适用版本:** Rust 1.0+（`?` 自 1.13+）

**一句话答案：** 用 `Result` 当返回值，在失败分支 `return Err(...)` 或直接写 `?`；没有“抛异常再由上层 catch”的通道。

**解答：** Rust 的可恢复错误就是普通值。函数签名写明 `-> Result<T, E>`，调用方要么处理 `Err`，要么继续往上返回。`?` 只是把“失败就提前 return”写短了，并不改变“错误是返回值”这一事实。

```rust
use std::fs;
use std::io;
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(ParseIntError),
}

impl From<io::Error> for AppError {
    fn from(e: io::Error) -> Self {
        Self::Io(e)
    }
}

impl From<ParseIntError> for AppError {
    fn from(e: ParseIntError) -> Self {
        Self::Parse(e)
    }
}

fn read_port(path: &str) -> Result<u16, AppError> {
    let text = fs::read_to_string(path)?; // Err 自动转成 AppError
    Ok(text.trim().parse()?)
}

fn main() {
    match read_port("port.txt") {
        Ok(port) => println!("port = {port}"),
        Err(e) => eprintln!("failed: {e:?}"),
    }
}
```

上层想“接着抛”时，继续返回 `Result` 即可；想在边界消化错误，就 `match` / `if let Err`，不要指望有 try/catch。

**Go 对比：**
- Go 的 `if err != nil { return ..., err }` 和 Rust 的 `?` / 显式 `return Err` 是同一类早返回。
- 区别在于 Rust 把错误写进类型系统：忘了处理通常编不过。
- 别把 `panic!` 当成 Go 里少见的 `panic`/`recover` 业务通道来用。

**记忆点：**
- 往上抛 = 返回 `Err`，不是 exception。
- `?` 只是语法糖，语义仍是早返回。
- 边界层再决定打日志、转用户提示或退出码。

## Q14. anyhow 和 thiserror 分别适合什么场景？怎么选？ {#q14}
**Tags:** `hot` `anyhow` `thiserror`
**适用版本:** 需在 `Cargo.toml` 加依赖；生态常见组合

**一句话答案：** 应用/胶水层优先 `anyhow`（方便携带上下文）；库的公共 API 优先 `thiserror`（稳定、可匹配的错误类型）。

**解答：** 两者都不是标准库，但几乎是 Rust 错误处理的“默认搭档”。选型看调用方要不要按错误变体分支，以及你是否需要稳定的错误类型出现在对外签名里。

```toml
[dependencies]
anyhow = "1"
thiserror = "2"
```

```text
// 应用层：anyhow::Result + context（需依赖 anyhow）
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<String> {
    std::fs::read_to_string(path)
        .with_context(|| format!("读取配置 {path}"))
}

// 库 API：thiserror 生成 Display / Error（需依赖 thiserror）
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("读取配置 {path} 失败")]
    Read {
        path: String,
        #[source]
        source: std::io::Error,
    },
}
```

经验法则：二进制、服务入口、脚本式工具用 `anyhow`；要给下游 `match`、要保证错误形态不乱漂的库用 `thiserror`。同一工程里也很常见——库返回具体错误，二进制边界再 `anyhow::Error::from` 收口。

**Go 对比：**
- `anyhow` 更像到处 `fmt.Errorf("...: %w", err)` 的应用写法。
- `thiserror` 更像给包定义一组可文档化、可分支的错误值/类型。
- Go 没有强制“库错误要稳定类型”，Rust 库作者通常更在意这一点。

**记忆点：**
- 应用：`anyhow`；库：`thiserror`。
- 需要 `match` 变体时别把公共 API 收成 `anyhow::Error`。
- 两者可以在同一仓库分层共存。

## Q15. `?` 碰上 `Option` 为什么有时编译不过？怎么转 Result？ {#q15}
**Tags:** `hot` `?` `Option` `ok_or`
**适用版本:** `Option` 的 `?` 自 Rust 1.22+

**一句话答案：** `?` 要求“失败分支的类型”和函数返回类型一致；在返回 `Result` 的函数里对 `Option` 直接 `?`，类型对不上就会编不过，先用 `ok_or` / `ok_or_else` 转成 `Result`。

**解答：** 返回 `Option` 时，对另一个 `Option` 用 `?` 没问题——`None` 会提前返回 `None`。一旦函数签名是 `Result`，`None` 不能自动变成某个 `Err`，编译器就会拒绝。

```rust
fn first_digit(s: &str) -> Option<char> {
    s.chars().find(|c| c.is_ascii_digit())
}

// 返回 Option：Option 上的 ? 合法
fn parse_code_opt(s: &str) -> Option<u32> {
    let d = first_digit(s)?;
    d.to_digit(10)
}

// 返回 Result：先把 Option 转成 Result，再 ?
fn parse_code(s: &str) -> Result<u32, &'static str> {
    let d = first_digit(s).ok_or("缺少数字")?;
    d.to_digit(10).ok_or("非法数字")
}

fn main() {
    assert_eq!(parse_code_opt("ab7c"), Some(7));
    assert_eq!(parse_code("ab7c"), Ok(7));
    assert_eq!(parse_code("abc"), Err("缺少数字"));
}
```

反向也很常见：只有 `Result`、却想在 `Option` 管道里早退时，用 `.ok()?`（会丢掉错误信息）或先想清楚是否该改成全程 `Result`。

**Go 对比：**
- Go 的 `v, ok` 和 `v, err` 是两套习惯；混用时你得自己决定“没找到”算不算错误。
- Rust 用类型强制你做这次转换：`ok_or` 就是在说“缺席 = 这种错误”。
- 看到“`?` could not convert …”一类提示，先查函数返回类型，再查左边是 `Option` 还是 `Result`。

**记忆点：**
- `?` 不负责凭空发明 `Err`。
- `Option` → `Result`：`ok_or` / `ok_or_else`。
- 混用时以函数返回类型为准对齐。

## Q16. 什么时候该 log 掉错误，什么时候必须 `return Err`？ {#q16}
**Tags:** `common` `logging` `Result`
**适用版本:** Rust 1.0+

**一句话答案：** 只有当你是错误的最终处理边界（进程入口、请求边界、后台任务顶层）时才 log 并消化；中间层应 `return Err`，避免“打完日志还当成功继续跑”或重复刷同一条错。

**解答：** 日志回答“运维/排查能不能看见”，`return Err` 回答“调用方能不能做决策”。两者不互斥，但责任通常只在一层承担完整收口。

```rust
use std::fs;
use std::io;

fn read_token(path: &str) -> Result<String, io::Error> {
    // 中间层：只传播，不抢着打日志
    fs::read_to_string(path)
}

fn handle_request(path: &str) -> Result<(), String> {
    let token = read_token(path).map_err(|e| format!("读取 token 失败: {e}"))?;
    if token.trim().is_empty() {
        return Err("token 为空".into());
    }
    Ok(())
}

fn main() {
    // 边界层：决定日志 + 退出码 / 响应
    if let Err(e) = handle_request("token.txt") {
        eprintln!("request failed: {e}");
        std::process::exit(1);
    }
}
```

该 log 的典型位置：`main`、HTTP handler 最外层、worker 循环的单次任务边界。必须 `return Err` 的位置：库函数、可复用的业务步骤、还可能被重试/降级/换路径的代码。既要日志又要传播时，优先“带上下文地返回”，让边界层统一打印，而不是每一层各打一遍。

**Go 对比：**
- Go 里同样忌讳每层 `log.Printf` 后再 `return err`，否则同一错误刷屏。
- 中间层 `return fmt.Errorf("...: %w", err)`，入口再 log，两边习惯一致。
- Rust 额外提醒：`unwrap`/`expect` 不是“记一笔日志”，那是直接崩。

**记忆点：**
- 中间层传播，边界层收口。
- 先问“调用方还要不要决策”，要就别只 log。
- 同一错误 ideally 只在一层完整落地（日志或用户可见提示）。

## Q17. `unwrap_or` / `unwrap_or_else` / `unwrap_or_default` 和 `?` 怎么选？ {#q17}
**Tags:** `hot` `unwrap_or` `?` `Option` `Result`
**适用版本:** Rust 1.0+（`unwrap_or_default` 自 1.28+）

**一句话答案：** 本地能给出合理默认值、失败不需要向上汇报时用 `unwrap_or*`；失败原因还要给调用方决策时用 `?`（或显式 `return Err`），不要互相顶替。

**解答：** 这三类方法和 `?` 回答的是不同问题。`unwrap_or(v)` / `unwrap_or_else(f)` / `unwrap_or_default()` 把“缺席或失败”**就地消化**成一个值；`?` 则是**把失败继续往上抛**。选错的典型症状：该降级成默认配置却 `?` 把整个请求打挂；该告诉用户“端口非法”却 `unwrap_or(8080)` 悄悄用了错配置。

```rust
fn display_name(raw: Option<&str>) -> String {
    // 缺席可以就地给默认：不需要向上报错
    raw.unwrap_or("anonymous").to_string()
}

fn cache_dir(raw: Option<String>) -> String {
    // 默认值贵时用 else，避免每次都构造
    raw.unwrap_or_else(|| String::from(".cache"))
}

fn retry_limit(raw: Option<u32>) -> u32 {
    // 类型实现了 Default 时用 default
    raw.unwrap_or_default()
}

fn main() {
    assert_eq!(display_name(None), "anonymous");
    assert_eq!(cache_dir(None), ".cache");
    assert_eq!(retry_limit(None), 0);
}
```

```rust
use std::num::ParseIntError;

fn parse_port(input: &str) -> Result<u16, ParseIntError> {
    // 解析失败必须向上汇报：用 ?
    input.parse::<u16>()
}

fn bind_address(port_text: &str) -> Result<String, ParseIntError> {
    let port = parse_port(port_text)?;
    Ok(format!("0.0.0.0:{port}"))
}

fn main() {
    assert_eq!(bind_address("8080").unwrap(), "0.0.0.0:8080");
    assert!(bind_address("abc").is_err());
}
```

经验法则：默认值是业务上“正确的降级”，用 `unwrap_or*`；失败后调用方还要分支/重试/改提示，用 `?`。`unwrap_or_else` 适合默认值有开销或依赖外部状态；常量默认值用 `unwrap_or` 更直观。它和 [Q4](#q4) 的 `unwrap`/`expect` 也不同：后者是“不允许失败”，前者是“失败也给出值”。

**Go 对比：**
- Go 常见 `if err != nil { return ..., err }` 对应 `?`；本地 `v = default` 对应 `unwrap_or*`。
- Go 没有把这两种意图拆成方法名，全靠 `if` 结构表达。
- 转 Rust 时别把所有 `err != nil` 都改成 `unwrap_or`，信息会被吃掉。

**记忆点：**
- 能就地降级 → `unwrap_or*`。
- 还要向上决策 → `?`。
- `else` 管贵默认值，`default` 管 `Default` 类型。

## Q18. 多种错误源不用 anyhow 时，怎么用枚举统一？ {#q18}
**Tags:** `hot` `custom-error` `From` `Result`
**适用版本:** Rust 1.0+

**一句话答案：** 定义自己的错误枚举，为每种源错误实现 `From`，函数统一返回该枚举，再用 `?` 自动装箱；库代码优先这条路，而不是依赖 anyhow。

**解答：** [Q14](#q14) 里 anyhow 适合应用层“随便带上下文往上抛”。库、可分支处理的业务、或想少依赖时，应用枚举把 `io::Error`、`ParseIntError`、业务校验失败收成一种 `AppError`。关键是：每个变体承载一类失败，并实现 `From<源错误>`，这样 `?` 才能自动转换（见 [Q8](#q8)）。

```rust
use std::fs;
use std::io;
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(ParseIntError),
    EmptyConfig,
}

impl From<io::Error> for AppError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

impl From<ParseIntError> for AppError {
    fn from(value: ParseIntError) -> Self {
        Self::Parse(value)
    }
}

fn load_workers(path: &str) -> Result<usize, AppError> {
    let text = fs::read_to_string(path)?; // io::Error -> AppError
    let trimmed = text.trim();
    if trimmed.is_empty() {
        return Err(AppError::EmptyConfig);
    }
    Ok(trimmed.parse::<usize>()?) // ParseIntError -> AppError
}

fn main() {
    match load_workers("workers.txt") {
        Ok(n) => println!("workers={n}"),
        Err(AppError::EmptyConfig) => eprintln!("配置为空"),
        Err(e) => eprintln!("其他失败: {e:?}"),
    }
}
```

```rust
use std::fmt;
use std::io;

#[derive(Debug)]
enum AppError {
    Io(io::Error),
    BadInput(&'static str),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(e) => write!(f, "io: {e}"),
            Self::BadInput(msg) => write!(f, "bad input: {msg}"),
        }
    }
}

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io(e) => Some(e),
            Self::BadInput(_) => None,
        }
    }
}

impl From<io::Error> for AppError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

fn read_nonzero(path: &str) -> Result<String, AppError> {
    let text = std::fs::read_to_string(path)?;
    if text.trim().is_empty() {
        return Err(AppError::BadInput("empty file"));
    }
    Ok(text)
}

fn main() {
    let _ = read_nonzero("note.txt");
}
```

第二段补上 `Display` + `Error`，错误就能进日志框架、嵌进更高层 `source` 链。不想手写样板时，库侧常用 `thiserror`（见 [Q14](#q14)）；但“枚举 + `From` + `?`”这条心智模型不变。

**Go 对比：**
- Go 常见 `fmt.Errorf("%w", err)` 包一层，或自定义 `type MyError struct`。
- Rust 枚举把“固定几类失败”写成可穷尽匹配，比字符串/`errors.Is` 更直接。
- 应用入口仍可把枚举再转成动态错误，但库 API 尽量暴露具体类型。

**记忆点：**
- 一种源错误 → 一个枚举变体 + `From`。
- 统一返回类型后，`?` 负责转换。
- 库用枚举，应用才考虑 anyhow。

## Q19. `and_then` / `or_else` 和 `map` / `map_err` 怎么区分？ {#q19}
**Tags:** `hot` `and_then` `or_else` `map` `map_err`
**适用版本:** Rust 1.0+

**一句话答案：** `map`/`map_err` 只改 `Ok`/`Err` 里的**值类型**，外壳仍是一层 `Result`；`and_then`/`or_else` 的闭包自己再返回 `Result`，用来做“下一步可能失败”或“失败后换一条路”。

**解答：** 记住形状：`map(f)` 里 `f: T -> U`，结果是 `Result<U, E>`；`and_then(f)` 里 `f: T -> Result<U, E>`，避免 `Result<Result<U, E>, E>` 套娃。`map_err` 只改造错误值；`or_else` 在 `Err` 分支再尝试一次恢复，闭包也要返回 `Result`。

```rust
fn double_ok(x: Result<i32, &str>) -> Result<i32, &str> {
    // 成功值变形，失败原样保留
    x.map(|n| n * 2)
}

fn label_err(x: Result<i32, &str>) -> Result<i32, String> {
    // 只改错误类型/内容
    x.map_err(|e| format!("failed: {e}"))
}

fn main() {
    assert_eq!(double_ok(Ok(21)), Ok(42));
    assert_eq!(double_ok(Err("nope")), Err("nope"));
    assert_eq!(label_err(Err("boom")).unwrap_err(), "failed: boom");
}
```

```rust
fn parse_then_scale(input: &str) -> Result<i32, String> {
    input
        .parse::<i32>()
        .map_err(|e| e.to_string())
        // 下一步还可能失败：用 and_then，不要 map 后再手动展平
        .and_then(|n| {
            if n < 0 {
                Err(String::from("negative"))
            } else {
                Ok(n * 10)
            }
        }) // 闭包返回 Result，避免 Result<Result<...>>
}

fn fallback_port(primary: &str, backup: &str) -> Result<u16, String> {
    primary
        .parse::<u16>()
        .map_err(|e| e.to_string())
        // 失败才走备用：or_else
        .or_else(|_| backup.parse::<u16>().map_err(|e| e.to_string()))
}

fn main() {
    assert_eq!(parse_then_scale("4").unwrap(), 40);
    assert!(parse_then_scale("-1").is_err());
    assert_eq!(fallback_port("x", "8080").unwrap(), 8080);
}
```

和 [Q6](#q6) 的关系：`map_err`/`ok_or`/`transpose` 偏“改壳/翻形状”；本题的 `and_then`/`or_else` 偏“链式步骤”。看见 `map(|x| fallible(x))` 得到 `Result<Result<...>>` 时，几乎总该改成 `and_then`。

**Go 对比：**
- Go 就是连续 `if err != nil`；Rust 用组合子把成功/失败路径写成表达式。
- `and_then` ≈ “成功后再调一个返回 error 的函数”；`or_else` ≈ “失败后换个实现再试”。
- 别为了链式而链式：步骤一多，普通 `?` 早返回往往更清晰。

**记忆点：**
- `map`/`map_err`：改值，不增加一层失败。
- `and_then`：成功后再走一步可能失败的逻辑。
- `or_else`：失败后换路再试。

## Q20. `io::Error` 和 `ErrorKind` 日常怎么用？ {#q20}
**Tags:** `hot` `io::Error` `ErrorKind`
**适用版本:** Rust 1.0+

**一句话答案：** 把 `std::io::Error` 当“I/O 失败对象”传递/打印；要用 `match`/`if` 分支处理时，看 `err.kind()` 得到的 `ErrorKind`（如 `NotFound`、`PermissionDenied`），不要解析错误字符串。

**解答：** 文件、网络、管道几乎都会碰到 `io::Error`。它实现了 `std::error::Error`，可直接 `?` 进自定义错误（见 [Q18](#q18)）。**`ErrorKind`** 是错误的粗分类枚举，适合写“文件不存在就创建、权限不够就提示、其他再上抛”这类策略。构造错误用 `io::Error::new(kind, msg)` 或 `io::Error::from(kind)`。

```rust
use std::fs;
use std::io::{self, ErrorKind};

fn read_or_empty(path: &str) -> io::Result<String> {
    match fs::read_to_string(path) {
        Ok(text) => Ok(text),
        Err(err) if err.kind() == ErrorKind::NotFound => Ok(String::new()),
        Err(err) => Err(err),
    }
}

fn main() {
    // 文件不存在时得到空字符串，而不是把整个程序打挂
    let text = read_or_empty("maybe-missing.txt").unwrap();
    println!("len={}", text.len());
}
```

```rust
use std::io::{self, ErrorKind};

fn ensure_positive(n: i32) -> io::Result<i32> {
    if n <= 0 {
        // 业务校验也可复用 io::Error，当“伪 I/O 边界”时常见于小工具
        return Err(io::Error::new(
            ErrorKind::InvalidInput,
            "n must be positive",
        ));
    }
    Ok(n)
}

fn classify(err: &io::Error) -> &'static str {
    match err.kind() {
        ErrorKind::NotFound => "missing",
        ErrorKind::PermissionDenied => "denied",
        ErrorKind::AlreadyExists => "exists",
        ErrorKind::InvalidInput => "bad-input",
        _ => "other",
    }
}

fn main() {
    let err = ensure_positive(0).unwrap_err();
    assert_eq!(classify(&err), "bad-input");
    assert_eq!(err.to_string(), "n must be positive");
}
```

注意：`ErrorKind` 有稳定变体，也有可能随平台扩展；匹配时保留 `_` 分支。跨模块业务错误仍优先自定义枚举（[Q7](#q7)、[Q18](#q18)），不要把所有失败都硬塞进 `io::Error`，除非你真的在 I/O 边界。

**Go 对比：**
- 对应 `os.ErrNotExist`、`os.IsNotExist(err)`、`errors.Is(err, ...)` 这类判断。
- Rust 用 `err.kind() == ErrorKind::NotFound`，语义更集中在一个枚举上。
- 两边都忌讳 `strings.Contains(err.Error(), "not found")`。

**记忆点：**
- 传递/打印用 `io::Error`，分支用 `kind()`。
- 常见 kind：`NotFound`、`PermissionDenied`、`InvalidInput`。
- 业务分层错误仍优先自定义枚举。

## Q21. anyhow 的 `context` / `with_context` 标准写法是什么？ {#q21}
**Tags:** `hot` `anyhow` `context` `with_context`
**适用版本:** anyhow 1.x（应用层；与 [Q14](#q14) 选型配套）

**一句话答案：**
在 `Result` 上链式调用 `.context("固定说明")` 或 `.with_context(|| format!("...{var}"))`：失败时才附加「正在做什么」；成功路径零开销构造闭包字符串。这是 anyhow 应用层补语境的标准写法，比到处 `map_err(|e| format!(...))` 更整齐。

**解答：**
[Q9](#q9) 讲的是「要补上下文」的原则；[Q14](#q14) 讲 anyhow/thiserror 怎么选。本题只钉 **anyhow 怎么写**。

```toml
[dependencies]
anyhow = "1"
```

```text
use anyhow::{Context, Result};
use std::fs;
use std::path::Path;

fn read_config(path: &Path) -> Result<String> {
    // 静态说明：context
    fs::read_to_string(path).context("读取配置文件失败")
}

fn read_config_named(path: &Path) -> Result<String> {
    // 需要路径等变量：with_context（闭包，仅失败时执行）
    fs::read_to_string(path)
        .with_context(|| format!("读取配置 {}", path.display()))
}

fn load_app(path: &Path) -> Result<String> {
    let text = read_config_named(path)?;
    // 多层 context 会叠成错误链，排查时从外到内读
    let trimmed = text
        .parse::<u16>()
        .map(|_| text) // 示意：真实项目会解析成结构体
        .with_context(|| format!("解析配置 {}", path.display()))?;
    Ok(trimmed)
}
```

习惯：
- 能写死字符串 → `context("...")`
- 要插变量 / 稍贵格式化 → `with_context(|| ...)`
- 库的公共 API 仍优先 thiserror（见 [Q14](#q14)），别把 `anyhow::Error` 泄漏给下游要 `match` 的调用方

「❌」——成功也先 `format!` 再 `map_err`：浪费分配；用 `with_context` 把格式化推迟到失败。

**Go 对比：**
```go
return fmt.Errorf("读取配置 %s: %w", path, err)
```
- **Go 怎么做**：失败分支里 `fmt.Errorf` + `%w`。
- **Rust 为什么不同**：anyhow 把「包装」做成 `Result` 方法链，和 `?` 很搭。
- **Go 程序员易踩的坑**：只 `context("failed")` 不写关键变量，链很深却定位不到文件。

**记忆点：**
- 固定文案 → `context`；带变量 → `with_context`。
- 和 [Q9](#q9) 同目标，只是 anyhow 的标准 API。

## Q22. 用户可见错误和日志错误为什么要分开？ {#q22}
**Tags:** `common` `UX` `logging` `anyhow`
**适用版本:** Rust 1.0+；常与 anyhow / HTTP / CLI 边界一起用

**一句话答案：**
给用户/调用方看的是**安全、可行动**的短消息；写进日志/tracing 的是**完整诊断**（路径、内部码、source 链）。同一失败可以「对外友好 + 对内详细」，不要把 `Display` 整链直接弹给终端用户。

**解答：**
[Q16](#q16) 回答「该不该 log、该不该 `return Err`」；本题回答「**两套文案**怎么拆」。

```rust
#[derive(Debug)]
struct AppError {
    user_msg: String,
    // 真实项目里还会带 source / 错误码
}

fn open_avatar(path: &str) -> Result<Vec<u8>, AppError> {
    match std::fs::read(path) {
        Ok(bytes) => Ok(bytes),
        Err(e) => {
            // 对内：详细
            eprintln!("avatar read failed path={path} err={e}");
            // 对外：不泄露路径与系统细节
            Err(AppError {
                user_msg: "无法加载头像，请稍后重试".into(),
            })
        }
    }
}

fn main() {
    if let Err(e) = open_avatar("/var/app/secret/avatar.bin") {
        println!("对用户: {}", e.user_msg);
    }
}
```

anyhow 边界示意（text）：

```text
// HTTP/CLI 边界
if let Err(err) = run() {
    tracing::error!(error = %err, "request failed"); // 完整链给运维
    // 响应用户：StatusCode::INTERNAL_SERVER_ERROR + 固定文案
    // 不要把 err.to_string() 原样返回给浏览器
}
```

拆分原则：
- 用户：能做什么（重试、改输入、联系支持），无内部路径/SQL/token
- 日志：能定位（request id、path、source）
- 稳定对外错误码 / 枚举可以公开；实现细节只留在日志

**Go 对比：**
- 同样常见：`log.Printf("%+v", err)` 对内，`http.Error(..., "internal error", 500)` 对外。
- Rust 用类型或边界函数强制拆开，避免 `?` 一路把内部 `Display` 漏到响应。
- 别把 anyhow 全链 `to_string()` 当 API 正文。

**记忆点：**
- 对外短而安全；对内长而可诊。
- 边界层做一次映射，中间层别提前「对用户友好」丢诊断。
