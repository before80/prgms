+++
title = "第2章 编写一个猜数字游戏"
date = 2026-08-05T08:44:00+08:00
weight = 8
type = "docs"
description = "动手实现猜数字游戏，练习 let、match 与外部 crate"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 编写一个猜数字游戏 {#programming-a-guessing-game}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch02-00-guessing-game-tutorial.html](https://doc.rust-lang.org/stable/book/ch02-00-guessing-game-tutorial.html)


　　让我们通过一起完成一个动手项目来跳进 Rust！本章会通过在真实程序中使用它们，向你介绍一些常见的 Rust 概念。你会学到 `let`、`match`、方法、关联函数、外部 crate 等等！在后续章节中，我们会更详细地探索这些想法。在本章中，你只需练习这些基础。

　　我们将实现一个经典的初学者编程问题：猜数字游戏。玩法是这样的：程序会生成一个 1 到 100 之间的随机整数，然后提示玩家输入猜测。输入猜测后，程序会指出猜测是太小还是太大。若猜测正确，游戏会打印祝贺信息并退出。

## 搭建新项目 {#setting-up-a-new-project}

　　要搭建新项目，请进入你在第 1 章创建的 *projects* 目录，并用 Cargo 新建一个项目，像这样：

```console
$ cargo new guessing_game
$ cd guessing_game
```

　　第一条命令 `cargo new` 把项目名（`guessing_game`）作为第一个参数。第二条命令切换到新项目的目录。

　　看看生成的 *Cargo.toml* 文件：


<span class="filename">文件名：Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"

[dependencies]
```

　　正如你在第 1 章所见，`cargo new` 会为你生成一个「Hello, world!」程序。查看 *src/main.rs* 文件：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

　　现在让我们用 `cargo run` 命令一步编译并运行这个「Hello, world!」程序：

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/guessing_game`
Hello, world!
```

　　当你需要在项目上快速迭代时，`run` 命令很方便——就像我们在这个游戏中会做的那样：在进入下一次迭代之前，快速测试每一次迭代。

　　重新打开 *src/main.rs* 文件。本章的所有代码你都会写在这个文件里。

## 处理一次猜测 {#processing-a-guess}

　　猜数字游戏程序的第一部分会请求用户输入、处理该输入，并检查输入是否符合预期形式。首先，我们允许玩家输入一次猜测。把示例 2-1 中的代码输入到 *src/main.rs*。

**文件名：`src/main.rs`**
```rust
use std::io;

fn main() {
    println!("Guess the number!");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

**示例 2-1：获取用户猜测并打印它的代码**

　　这段代码包含大量信息，让我们逐行过一遍。要获取用户输入然后把结果打印为输出，我们需要把 `io`（输入/输出）库引入作用域。`io` 库来自标准库，也就是 `std`：

```rust
use std::io;
```

　　默认情况下，Rust 会把标准库中定义的一组项引入每个程序的作用域。这组项称为*前奏*（prelude），你可以在[标准库文档][prelude]中看到其中的全部内容。

　　若你想用的类型不在 prelude 中，就必须用 `use` 语句显式把它引入作用域。使用 `std::io` 库会为你提供许多有用的功能，包括接受用户输入的能力。

　　正如你在第 1 章所见，`main` 函数是程序的入口点：

```rust
fn main() {
```

　　`fn` 语法声明一个新函数；圆括号 `()` 表示没有参数；花括号 `{` 开始函数体。

　　你在第 1 章也学过，`println!` 是把字符串打印到屏幕的宏：

```rust
    println!("Guess the number!");

    println!("Please input your guess.");
```

　　这段代码会打印游戏说明，并提示用户输入猜测。

### 用变量存储值 {#storing-values-with-variables}

　　接下来，我们创建一个*变量*来存储用户输入，像这样：

```rust
    let mut guess = String::new();
```

　　现在程序开始变得有趣了！这一小行里发生了很多事。我们用 `let` 语句创建变量。再举一个例子：

```rust
let apples = 5;
```

　　这一行创建了一个名为 `apples` 的新变量，并把它绑定到值 `5`。在 Rust 中，变量默认不可变，意味着一旦我们给变量一个值，该值就不会改变。我们会在第 3 章的[「变量与可变性」][variables-and-mutability]一节详细讨论这个概念。要使变量可变，我们在变量名前面加上 `mut`：

```rust
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> 注意：`//` 语法开始一条一直持续到行末的注释。Rust 会忽略注释中的所有内容。我们会在[第 3 章][comments]更详细地讨论注释。

　　回到猜数字游戏程序，你现在知道 `let mut guess` 会引入一个名为 `guess` 的可变变量。等号（`=`）告诉 Rust 我们现在想把某个东西绑定到该变量。等号右边是 `guess` 所绑定的值，它是调用 `String::new` 的结果，该函数返回一个新的 `String` 实例。[`String`][string] 是标准库提供的字符串类型，是一段可增长的、UTF-8 编码的文本。

　　`::new` 这一行中的 `::` 语法表示 `new` 是 `String` 类型的关联函数。*关联函数*（associated function）是在某个类型上实现的函数，这里是 `String`。这个 `new` 函数创建一个新的空字符串。你会在许多类型上找到 `new` 函数，因为这是「创建某种新值」的函数的常用名字。

　　总的来说，`let mut guess = String::new();` 这一行创建了一个可变变量，当前绑定到一个新的空 `String` 实例。呼！

### 接收用户输入 {#receiving-user-input}

　　回想一下，我们在程序第一行用 `use std::io;` 引入了标准库的输入/输出功能。现在我们从 `io` 模块调用 `stdin` 函数，这将允许我们处理用户输入：

```rust
    io::stdin()
        .read_line(&mut guess)
```

　　若我们没有在程序开头用 `use std::io;` 导入 `io` 模块，仍然可以通过把这次函数调用写成 `std::io::stdin` 来使用该函数。`stdin` 函数返回一个 [`std::io::Stdin`][iostdin] 实例，这是表示终端标准输入句柄的类型。

　　接下来，`.read_line(&mut guess)` 这一行在标准输入句柄上调用 [`read_line`][read_line] 方法以获取用户输入。我们还把 `&mut guess` 作为参数传给 `read_line`，告诉它把用户输入存到哪个字符串里。`read_line` 的完整工作是：取出用户在标准输入中键入的任何内容，并把它追加到字符串中（而不覆盖其内容），因此我们把该字符串作为参数传入。字符串参数需要是可变的，这样方法才能改变字符串的内容。

　　`&` 表示这个参数是一个*引用*（reference），它让你能让代码的多个部分访问同一份数据，而不必把该数据在内存中复制多次。引用是复杂特性，而 Rust 的一大优势就是使用引用既安全又容易。你不必了解其中太多细节就能完成本程序。眼下你只需知道：与变量一样，引用默认不可变。因此，你需要写 `&mut guess` 而不是 `&guess` 来使其可变。（第 4 章会更彻底地解释引用。）

### 用 `Result` 处理潜在失败 {#handling-potential-failure-with-result}

　　我们仍在处理这一行代码。我们现在讨论的是第三行文本，但请注意它仍是同一条逻辑代码行的一部分。下一部分是这个方法：

```rust
        .expect("Failed to read line");
```

　　我们本可以把这段代码写成：

```rust
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

　　不过，一行太长难以阅读，因此最好拆开。当你用 `.method_name()` 语法调用方法时，引入换行和其他空白来拆分长行往往是明智的。现在让我们讨论这一行做什么。

　　如前所述，`read_line` 会把用户输入的任何内容放进我们传给它的字符串，但它也会返回一个 `Result` 值。[`Result`][result] 是一种[*枚举*][enums]（enumeration），常简称为 *enum*，是一种可以处于多种可能状态之一的类型。我们把每种可能状态称为一个*变体*（variant）。

　　[第 6 章][enums]会更详细地介绍枚举。这些 `Result` 类型的目的是编码错误处理信息。

　　`Result` 的变体是 `Ok` 和 `Err`。`Ok` 变体表示操作成功，并包含成功生成的值。`Err` 变体表示操作失败，并包含关于如何或为何失败的信息。

　　`Result` 类型的值与任何类型的值一样，都定义了方法。`Result` 的实例有一个你可以调用的 [`expect` 方法][expect]。若这个 `Result` 实例是 `Err` 值，`expect` 会使程序崩溃，并显示你作为参数传给 `expect` 的消息。若 `read_line` 方法返回 `Err`，很可能是底层操作系统出错的结果。若这个 `Result` 实例是 `Ok` 值，`expect` 会取出 `Ok` 所保存的返回值，并只把该值返回给你以便使用。在本例中，该值是用户输入的字节数。

　　若不调用 `expect`，程序仍能编译，但你会得到警告：

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
warning: unused `Result` that must be used
  --> src/main.rs:10:5
   |
10 |     io::stdin().read_line(&mut guess);
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |
   = note: this `Result` may be an `Err` variant, which should be handled
   = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
   |
10 |     let _ = io::stdin().read_line(&mut guess);
   |     +++++++

warning: `guessing_game` (bin "guessing_game") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.59s
```

　　Rust 警告你没有使用 `read_line` 返回的 `Result` 值，表明程序尚未处理可能的错误。

　　消除警告的正确方式是实际编写错误处理代码，但在我们的例子中，我们只想在出问题时让程序崩溃，因此可以使用 `expect`。你会在[第 9 章][recover]学到如何从错误中恢复。

### 用 `println!` 占位符打印值 {#printing-values-with-println-placeholders}

　　除了结尾的花括号，到目前为止的代码中只剩一行需要讨论：

```rust
    println!("You guessed: {guess}");
```

　　这一行打印现在包含用户输入的字符串。`{}` 这组花括号是占位符：可以把 `{}` 想成小螃蟹钳子，把一个值夹在原处。打印变量的值时，变量名可以写在花括号内。打印求值表达式的结果时，在格式字符串中放置空花括号，然后在格式字符串后面跟一个逗号分隔的表达式列表，按相同顺序打印到每个空花括号占位符中。在一次 `println!` 调用中打印变量和表达式结果看起来会像这样：

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

　　这段代码会打印 `x = 5 and y + 2 = 12`。

### 测试第一部分 {#testing-the-first-part}

　　让我们测试猜数字游戏的第一部分。用 `cargo run` 运行它：


```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

　　到这一步，游戏的第一部分完成了：我们从键盘获取输入，然后打印它。

## 生成秘密数字 {#generating-a-secret-number}

　　接下来，我们需要生成一个用户要猜的秘密数字。秘密数字每次都应不同，这样游戏玩多次才有趣。我们使用 1 到 100 之间的随机数，这样游戏不会太难。Rust 的标准库尚未包含随机数功能。不过，Rust 团队提供了一个带有该功能的 [`rand` crate][randcrate]。

### 用 Crate 增强功能 {#increasing-functionality-with-a-crate}

　　请记住，crate 是一组 Rust 源码文件的集合。我们一直在构建的项目是一个二进制 crate，即可执行文件。`rand` crate 是一个库 crate，它包含旨在被其他程序使用的代码，不能单独执行。

　　Cargo 对外部 crate 的协调正是 Cargo 真正闪光的地方。在我们能编写使用 `rand` 的代码之前，需要修改 *Cargo.toml* 文件，把 `rand` crate 列为依赖。现在打开该文件，在 Cargo 为你创建的 `[dependencies]` 节标题下方底部添加下面这一行。请务必像我们这里一样精确指定 `rand` 以及这个版本号，否则本教程中的代码示例可能无法工作：


<span class="filename">文件名：Cargo.toml</span>

```toml
[dependencies]
rand = "0.10.1"
```

　　在 *Cargo.toml* 文件中，跟在某个标题后面的所有内容都属于该节，直到另一个节开始。在 `[dependencies]` 中，你告诉 Cargo 项目依赖哪些外部 crate，以及需要这些 crate 的哪些版本。在本例中，我们用语义化版本说明符 `0.10.1` 指定 `rand` crate。Cargo 理解[语义化版本控制][semver]（有时称为 *SemVer*），这是书写版本号的标准。说明符 `0.10.1` 实际上是 `^0.10.1` 的简写，表示至少是 0.10.1 但低于 0.11.0 的任何版本。

　　Cargo 认为这些版本的公共 API 与版本 0.10.1 兼容，这一规范确保你会得到仍能与本章代码一起编译的最新补丁版本。任何 0.11.0 或更高的版本都不保证具有与后续示例相同的 API。

　　现在，在不改动任何代码的情况下，让我们构建项目，如示例 2-2 所示。


```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

**示例 2-2：将 `rand` crate 添加为依赖后运行 `cargo build` 的输出**

　　你可能会看到不同的版本号（但多亏 SemVer，它们都会与代码兼容！）和不同的行（取决于操作系统），且各行顺序可能不同。

　　当我们包含外部依赖时，Cargo 会从*注册表*（registry）获取该依赖所需的一切的最新版本；注册表是来自 [Crates.io][cratesio] 的数据副本。Crates.io 是 Rust 生态系统中的人们发布开源 Rust 项目供他人使用的地方。

　　更新注册表之后，Cargo 会检查 `[dependencies]` 节，并下载所列的、尚未下载的任何 crate。在本例中，尽管我们只把 `rand` 列为依赖，Cargo 也会抓取 `rand` 为了工作而依赖的其他 crate。下载这些 crate 之后，Rust 会编译它们，然后在依赖可用的情况下编译项目。

　　若你立即再次运行 `cargo build` 且不做任何更改，除了 `Finished` 那一行之外不会得到任何输出。Cargo 知道它已经下载并编译了依赖，而你没有在 *Cargo.toml* 中对它们做任何更改。Cargo 也知道你没有更改代码，因此也不会重新编译代码。无事可做，它就直接退出。

　　若你打开 *src/main.rs* 文件，做一处琐碎的更改，然后保存并再次构建，你只会看到两行输出：


```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

　　这些行表明 Cargo 只根据你对 *src/main.rs* 文件的微小更改更新了构建。你的依赖没有改变，因此 Cargo 知道可以复用已经为它们下载和编译的内容。

#### 确保可复现的构建 {#ensuring-reproducible-builds}

　　Cargo 有一种机制，确保你或任何其他人每次构建代码时都能重建出相同的产物：在你另行指示之前，Cargo 只会使用你指定的依赖版本。例如，假设下周发布了 `rand` crate 的 0.10.2 版，该版本包含重要的 bug 修复，但也包含会破坏你代码的回归。为处理这种情况，Rust 在你首次运行 `cargo build` 时创建 *Cargo.lock* 文件，因此我们现在在 *guessing_game* 目录中有了这个文件。

　　当你首次构建项目时，Cargo 会弄清所有符合条件的依赖版本，然后把它们写入 *Cargo.lock* 文件。当你将来构建项目时，Cargo 会看到 *Cargo.lock* 文件存在，并将使用其中指定的版本，而不是再次做弄清版本的全部工作。这让你自动拥有可复现的构建。换句话说，多亏了 *Cargo.lock* 文件，你的项目会保持在 0.10.1，直到你显式升级。因为 *Cargo.lock* 文件对可复现构建很重要，它通常会与项目其余代码一起检入版本控制。

#### 更新 Crate 以获取新版本 {#updating-a-crate-to-get-a-new-version}

　　当你*确实*想更新某个 crate 时，Cargo 提供了 `update` 命令，它会忽略 *Cargo.lock* 文件，并弄清所有符合你在 *Cargo.toml* 中规范的最新版本。然后 Cargo 会把那些版本写入 *Cargo.lock* 文件。否则，默认情况下，Cargo 只会查找大于 0.10.1 且小于 0.11.0 的版本。若 `rand` crate 发布了两个新版本 0.10.2 和 0.999.0，运行 `cargo update` 时你会看到如下内容：


```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

　　Cargo 忽略了 0.999.0 发布版。此时，你也会注意到 *Cargo.lock* 文件的变化，指出你现在使用的 `rand` crate 版本是 0.10.2。要使用 `rand` 版本 0.999.0 或 0.999.*x* 系列中的任何版本，你必须把 *Cargo.toml* 文件更新成下面这样（实际上不要做这个更改，因为后续示例假定你使用的是 `rand` 0.10）：

```toml
[dependencies]
rand = "0.999.0"
```

　　下次运行 `cargo build` 时，Cargo 会更新可用 crate 的注册表，并根据你指定的新版本重新评估你的 `rand` 要求。

　　关于 [Cargo][doccargo] 和[其生态系统][doccratesio]还有很多可说，我们会在第 14 章讨论，但眼下这些就是你需要知道的全部。Cargo 让复用库变得非常容易，因此 Rustacean 能够编写由许多包组装而成的较小项目。

### 生成随机数 {#generating-a-random-number}

　　让我们开始使用 `rand` 来生成要猜的数字。下一步是更新 *src/main.rs*，如示例 2-3 所示。

**文件名：`src/main.rs`**
```rust
use std::io;

use rand::prelude::*;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::rng().random_range(1..=100);

    println!("The secret number is: {secret_number}");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

**示例 2-3：添加生成随机数的代码**

　　首先，我们添加一行 `use rand::prelude::*;`。`prelude` 模块包含 `rand` crate 中最常用的部分，而 `use` 使这些项在我们程序的作用域中可用。

　　接下来，我们在中间添加两行。在第一行中，我们调用 `rand::rng` 函数，它给我们将要使用的那个特定随机数生成器：一个对应当前执行线程的本地生成器，并由操作系统提供随机种子。然后，我们在随机数生成器上调用 `random_range` 方法。该方法由 `RngExt` 特征（trait）定义，该特征是我们用 `use rand::prelude::*;` 语句引入作用域的 `rand::prelude` 模块的一部分。`random_range` 方法接受一个范围表达式作为参数，并在该范围内生成一个随机数。我们这里使用的范围表达式形式为 `start..=end`，在上下界上都是闭区间，因此我们需要指定 `1..=100` 来请求 1 到 100 之间的数。

> 注意：你不会凭空知道该把什么引入作用域、该调用 crate 中的哪些方法和函数，因此每个 crate 都有带使用说明的文档。Cargo 的另一个巧妙功能是：运行 `cargo doc --open` 命令会在本地构建所有依赖提供的文档，并在浏览器中打开它。例如，若你对 `rand` crate 中的其他功能感兴趣，运行 `cargo doc --open`，然后点击左侧边栏中的 `rand`。

　　第二行新代码打印秘密数字。这在我们开发程序以便测试时很有用，但我们会从最终版本中删掉它。若程序一开始就打印答案，那就太不像游戏了！

　　试着多运行几次程序：


```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

　　你应得到不同的随机数，且它们都应是 1 到 100 之间的数。若有警告，可以安全地忽略。若有错误，请检查你的 *Cargo.toml* 中是否有 `rand = "0.10.1"`，因为未来版本的 `rand` 可能有不同的 API，但 `0.10` 系列中的任何版本都应能与本章代码一起工作。

## 比较猜测与秘密数字 {#comparing-the-guess-to-the-secret-number}

　　现在我们有了用户输入和随机数，就可以比较它们了。该步骤如示例 2-4 所示。注意这段代码目前还不能编译，我们会解释原因。

**文件名：`src/main.rs`**
```rust
use std::cmp::Ordering;
use std::io;

use rand::prelude::*;

fn main() {
    // --snip--

    println!("You guessed: {guess}");

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Too small!"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You win!"),
    }
}
```

**示例 2-4：处理比较两个数时可能的返回值**

　　首先，我们添加另一条 `use` 语句，把标准库中名为 `std::cmp::Ordering` 的类型引入作用域。`Ordering` 类型是另一个枚举，有变体 `Less`、`Greater` 和 `Equal`。这是比较两个值时可能出现的三种结果。

　　然后，我们在底部添加五行使用 `Ordering` 类型的新代码。`cmp` 方法比较两个值，可以在任何可比较的东西上调用。它接受你想与之比较的东西的引用：这里是把 `guess` 与 `secret_number` 比较。然后，它返回我们用 `use` 语句引入作用域的 `Ordering` 枚举的一个变体。我们用 [`match`][match] 表达式，根据用 `guess` 和 `secret_number` 中的值调用 `cmp` 所返回的 `Ordering` 变体，决定接下来做什么。

　　`match` 表达式由若干*分支*（arms）组成。一个分支由一个要匹配的*模式*（pattern），以及若交给 `match` 的值符合该分支的模式时应运行的代码组成。Rust 取出交给 `match` 的值，并依次查看每个分支的模式。模式和 `match` 构造是强大的 Rust 特性：它们让你表达代码可能遇到的各种情况，并确保你全部处理了它们。这些特性将分别在第 6 章和第 19 章详细介绍。

　　让我们用这里使用的 `match` 表达式走一遍例子。假设用户猜了 50，而这次随机生成的秘密数字是 38。

　　当代码把 50 与 38 比较时，`cmp` 方法会返回 `Ordering::Greater`，因为 50 大于 38。`match` 表达式得到 `Ordering::Greater` 值，并开始检查每个分支的模式。它查看第一个分支的模式 `Ordering::Less`，发现值 `Ordering::Greater` 与 `Ordering::Less` 不匹配，因此忽略该分支中的代码并移到下一个分支。下一个分支的模式是 `Ordering::Greater`，它*确实*匹配 `Ordering::Greater`！该分支中关联的代码会执行，并向屏幕打印 `Too big!`。`match` 表达式在第一次成功匹配后结束，因此在这种情况下不会查看最后一个分支。

　　不过，示例 2-4 中的代码还不能编译。让我们试一试：


```console
$ cargo build
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.0
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
error[E0308]: mismatched types
  --> src/main.rs:23:21
   |
23 |     match guess.cmp(&secret_number) {
   |                 --- ^^^^^^^^^^^^^^ expected `&String`, found `&{integer}`
   |                 |
   |                 arguments to this method are incorrect
   |
   = note: expected reference `&String`
              found reference `&{integer}`
note: method defined here
  --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/cmp.rs:1000:7

For more information about this error, try `rustc --explain E0308`.
error: could not compile `guessing_game` (bin "guessing_game") due to 1 previous error
```

　　错误的核心指出存在*类型不匹配*（mismatched types）。Rust 有强大的静态类型系统。不过，它也有类型推断。当我们写 `let mut guess = String::new()` 时，Rust 能推断出 `guess` 应该是 `String`，并不要求我们写出类型。另一方面，`secret_number` 是数字类型。Rust 的几种数字类型可以有 1 到 100 之间的值：`i32`，32 位数；`u32`，无符号 32 位数；`i64`，64 位数；以及其他。除非另行指定，Rust 默认使用 `i32`，这就是 `secret_number` 的类型——除非你在别处添加会使 Rust 推断出不同数值类型的类型信息。错误的原因是 Rust 无法比较字符串和数字类型。

　　最终，我们想把程序读入的 `String` 转换成数字类型，以便能在数值上与秘密数字比较。我们通过在 `main` 函数体中添加这一行来做到：

<span class="filename">文件名：src/main.rs</span>

```rust
    // --snip--

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    let guess: u32 = guess.trim().parse().expect("Please type a number!");

    println!("You guessed: {guess}");

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Too small!"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You win!"),
    }
```

　　这一行是：

```rust
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

　　我们创建了一个名为 `guess` 的变量。但是等等，程序不是已经有一个名为 `guess` 的变量了吗？确实有，但幸运的是 Rust 允许我们用新的值遮蔽（shadow）先前的 `guess` 值。*遮蔽*让我们复用 `guess` 变量名，而不必被迫创建两个唯一变量，例如 `guess_str` 和 `guess`。我们会在[第 3 章][shadowing]更详细地介绍这一点，但眼下请知道：当你想把值从一种类型转换成另一种类型时，经常会用到这个特性。

　　我们把这个新变量绑定到表达式 `guess.trim().parse()`。表达式中的 `guess` 指的是原先包含输入字符串的那个 `guess` 变量。`String` 实例上的 `trim` 方法会去掉开头和结尾的任何空白，在我们能把字符串转换成只能包含数值数据的 `u32` 之前必须这样做。用户必须按 <kbd>enter</kbd> 才能满足 `read_line` 并输入他们的猜测，这会在字符串中添加一个换行符。例如，若用户键入 <kbd>5</kbd> 并按 <kbd>enter</kbd>，`guess` 看起来像这样：`5\n`。`\n` 表示「换行」。（在 Windows 上，按 <kbd>enter</kbd> 会得到回车和换行，即 `\r\n`。）`trim` 方法去掉 `\n` 或 `\r\n`，结果就只剩 `5`。

　　[字符串上的 `parse` 方法][parse]把字符串转换成另一种类型。这里我们用它从字符串转换成数字。我们需要通过使用 `let guess: u32` 告诉 Rust 我们想要的确切数字类型。`guess` 后面的冒号（`:`）告诉 Rust 我们将标注该变量的类型。Rust 有几种内置数字类型；这里看到的 `u32` 是无符号 32 位整数。对于较小的正数，这是不错的默认选择。你会在[第 3 章][integers]学到其他数字类型。

　　此外，本示例程序中的 `u32` 标注以及与 `secret_number` 的比较意味着 Rust 会推断 `secret_number` 也应是 `u32`。于是，现在比较会在两个相同类型的值之间进行！

　　`parse` 方法只对可以在逻辑上转换成数字的字符起作用，因此很容易导致错误。例如，若字符串包含 `A👍%`，就没有办法把它转换成数字。因为它可能失败，`parse` 方法返回一个 `Result` 类型，很像 `read_line` 方法那样（前面在[「用 `Result` 处理潜在失败」](#handling-potential-failure-with-result)中讨论过）。我们会用同样的方式、再次使用 `expect` 方法来处理这个 `Result`。若 `parse` 因为无法从字符串创建数字而返回 `Err` 这个 `Result` 变体，`expect` 调用会使游戏崩溃并打印我们给它的消息。若 `parse` 能成功把字符串转换成数字，它会返回 `Result` 的 `Ok` 变体，而 `expect` 会从 `Ok` 值中返回我们想要的那个数字。

　　现在让我们运行程序：


```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

　　很好！即便在猜测前面加了空格，程序仍然弄清了用户猜的是 76。多运行几次程序，用不同类型的输入验证不同行为：猜对数字、猜一个太大的数、猜一个太小的数。

　　我们现在已经让游戏的大部分都能工作了，但用户只能猜一次。让我们通过添加循环来改变这一点！

## 用循环允许多次猜测 {#allowing-multiple-guesses-with-looping}

　　`loop` 关键字创建无限循环。我们会添加一个循环，给用户更多猜测数字的机会：

<span class="filename">文件名：src/main.rs</span>

```rust
    // --snip--

    println!("The secret number is: {secret_number}");

    loop {
        println!("Please input your guess.");

        // --snip--


        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => println!("You win!"),
        }
    }
}
```

　　如你所见，我们把从猜测输入提示开始的所有内容都移进了循环。请务必把循环内的各行再各缩进四个空格，然后再次运行程序。程序现在会永远询问另一次猜测，这实际上引入了一个新问题。看起来用户没法退出！

　　用户始终可以用键盘快捷键 <kbd>ctrl</kbd>-<kbd>C</kbd> 中断程序。但还有另一种方式可以退出这个无限循环，正如[「比较猜测与秘密数字」](#comparing-the-guess-to-the-secret-number)中关于 `parse` 的讨论所提到的：若用户输入非数字答案，程序会崩溃。我们可以利用这一点允许用户退出，如下所示：


```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　键入 `quit` 会退出游戏，但你会注意到，输入任何其他非数字输入也会如此。这至少可以说并不理想；我们还希望在猜对正确数字时游戏也停止。

### 猜对后退出 {#quitting-after-a-correct-guess}

　　让我们通过添加 `break` 语句，让游戏在用户获胜时退出：

<span class="filename">文件名：src/main.rs</span>

```rust
        // --snip--

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

　　在 `You win!` 之后添加 `break` 行，会在用户正确猜出秘密数字时让程序退出循环。退出循环也意味着退出程序，因为循环是 `main` 的最后一部分。

### 处理无效输入 {#handling-invalid-input}

　　为进一步改进游戏行为，与其在用户输入非数字时让程序崩溃，不如让游戏忽略非数字，以便用户可以继续猜测。我们可以通过修改把 `guess` 从 `String` 转换成 `u32` 的那一行来做到，如示例 2-5 所示。

**文件名：`src/main.rs`**
```rust
        // --snip--

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        // --snip--
```

**示例 2-5：忽略非数字猜测并请求另一次猜测，而不是让程序崩溃**

　　我们从 `expect` 调用切换到 `match` 表达式，以便从遇错崩溃转向处理错误。请记住，`parse` 返回 `Result` 类型，而 `Result` 是具有变体 `Ok` 和 `Err` 的枚举。我们在这里使用 `match` 表达式，就像对 `cmp` 方法的 `Ordering` 结果所做的那样。

　　若 `parse` 能成功把字符串变成数字，它会返回一个包含结果数字的 `Ok` 值。那个 `Ok` 值会匹配第一个分支的模式，而 `match` 表达式会直接返回 `parse` 产生并放在 `Ok` 值内的 `num` 值。那个数字最终会正好落在我们正在创建的新 `guess` 变量中我们想要的位置。

　　若 `parse` *不能*把字符串变成数字，它会返回一个包含更多错误信息的 `Err` 值。`Err` 值不匹配第一个 `match` 分支中的 `Ok(num)` 模式，但它匹配第二个分支中的 `Err(_)` 模式。下划线 `_` 是一个通配值；在本例中，我们是说想匹配所有 `Err` 值，无论它们内部有什么信息。于是，程序会执行第二个分支的代码 `continue`，它告诉程序进入 `loop` 的下一次迭代并请求另一次猜测。因此，实际上，程序忽略了 `parse` 可能遇到的所有错误！

　　现在程序中的一切都应如预期工作。让我们试一试：


```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

　　太棒了！再做一个小小的最终调整，我们就完成猜数字游戏了。回想一下，程序仍在打印秘密数字。这对测试很有用，但会毁了游戏。让我们删掉输出秘密数字的那条 `println!`。示例 2-6 展示了最终代码。

**文件名：`src/main.rs`**
```rust
use std::cmp::Ordering;
use std::io;

use rand::prelude::*;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::rng().random_range(1..=100);

    loop {
        println!("Please input your guess.");

        let mut guess = String::new();

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

**示例 2-6：完整的猜数字游戏代码**

　　到这一步，你已经成功构建了猜数字游戏。恭喜！

## 小结 {#summary}

　　这个项目以动手的方式向你介绍了许多新的 Rust 概念：`let`、`match`、函数、外部 crate 的使用等等。在接下来的几章中，你会更详细地学习这些概念。第 3 章涵盖大多数编程语言都有的概念，例如变量、数据类型和函数，并展示如何在 Rust 中使用它们。第 4 章探索所有权，这是使 Rust 有别于其他语言的特性。第 5 章讨论结构体与方法语法，第 6 章解释枚举如何工作。

[prelude]: https://doc.rust-lang.org/std/prelude/index.html
[variables-and-mutability]: ../common-programming-concepts/01-variables-and-mutability/#variables-and-mutability
[comments]: ../common-programming-concepts/04-comments/
[string]: https://doc.rust-lang.org/std/string/struct.String.html
[iostdin]: https://doc.rust-lang.org/std/io/struct.Stdin.html
[read_line]: https://doc.rust-lang.org/std/io/struct.Stdin.html#method.read_line
[result]: https://doc.rust-lang.org/std/result/enum.Result.html
[enums]: ../enums/
[expect]: https://doc.rust-lang.org/std/result/enum.Result.html#method.expect
[recover]: ../error-handling/02-recoverable-errors-with-result/
[randcrate]: https://crates.io/crates/rand
[semver]: https://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ../enums/02-match/
[shadowing]: ../common-programming-concepts/01-variables-and-mutability/#shadowing
[parse]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[integers]: ../common-programming-concepts/02-data-types/#integer-types
