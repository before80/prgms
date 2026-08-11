+++
title = "14.3 Cargo 工作空间"
date = 2026-08-05T08:44:00+08:00
weight = 64
type = "docs"
description = "用 Cargo 工作空间管理多个相关包、共享依赖与统一测试"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# Cargo 工作空间 {#cargo}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch14-03-cargo-workspaces.html](https://doc.rust-lang.org/stable/book/ch14-03-cargo-workspaces.html)


## Cargo 工作空间

　　第 12 章我们构建过一个同时包含二进制 crate 与库 crate 的包。随着项目发展，你可能发现库 crate 越来越大，想把包进一步拆成多个库 crate。Cargo 提供了称为*工作空间*（workspaces）的功能，帮助管理一起开发的多个相关包。

### 创建工作空间

　　*工作空间*是一组共享同一份 *Cargo.lock* 与同一输出目录的包。我们来用工作空间做一个项目——代码会尽量简单，以便把注意力放在工作空间结构上。组织工作空间的方式有很多，这里只演示一种常见做法：工作空间包含一个二进制与两个库。提供主要功能的二进制会依赖这两个库；一个库提供 `add_one` 函数，另一个提供 `add_two` 函数。这三个 crate 同属一个工作空间。先为工作空间新建目录：

```console
$ mkdir add
$ cd add
```

　　接下来，在 *add* 目录中创建配置整个工作空间的 *Cargo.toml*。这个文件不会有 `[package]` 小节，而是以 `[workspace]` 小节开头，用来添加工作空间成员。我们也通过把 `resolver` 设为 `"3"`，在工作空间中使用 Cargo 解析器算法的最新版本：

<span class="filename">文件名：Cargo.toml</span>

```toml
[workspace]
resolver = "3"
```

　　然后在 *add* 目录中运行 `cargo new`，创建 `adder` 二进制 crate：


```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

　　在工作空间内运行 `cargo new` 时，还会自动把新创建的包加入工作空间 *Cargo.toml* 中 `[workspace]` 定义里的 `members` 键，像这样：

```toml
[workspace]
resolver = "3"
members = ["adder"]
```

　　此时可以运行 `cargo build` 构建工作空间。*add* 目录中的文件应类似这样：

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

　　工作空间在顶层只有一个 *target* 目录，编译产物都放在这里；`adder` 包没有自己的 *target* 目录。即便在 *adder* 目录内运行 `cargo build`，产物仍会进入 *add/target*，而不是 *add/adder/target*。Cargo 这样组织工作空间的 *target*，是因为其中的 crate 本就打算互相依赖。若每个 crate 各有 *target*，每个 crate 都得重新编译工作空间里的其他 crate，才能把产物放进自己的 *target*。共享一个 *target* 可以避免不必要的重复构建。

### 在工作空间中创建第二个包

　　接下来，在工作空间里再创建一个成员包，命名为 `add_one`。生成名为 `add_one` 的新库 crate：


```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

　　顶层 *Cargo.toml* 现在会在 `members` 列表中包含 *add_one* 路径：

<span class="filename">文件名：Cargo.toml</span>

```toml
[workspace]
resolver = "3"
members = ["adder", "add_one"]
```

　　你的 *add* 目录现在应有这些目录与文件：

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

　　在 *add_one/src/lib.rs* 中加入 `add_one` 函数：

<span class="filename">文件名：add_one/src/lib.rs</span>

```rust
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

　　现在可以让带有二进制的 `adder` 包依赖带有库的 `add_one` 包。首先，需要在 *adder/Cargo.toml* 中为 `add_one` 添加路径依赖。

<span class="filename">文件名：adder/Cargo.toml</span>

```toml
[dependencies]
add_one = { path = "../add_one" }
```

　　Cargo 不会假定工作空间里的 crate 会互相依赖，因此必须显式写明依赖关系。

　　接下来，在 `adder` crate 中使用来自 `add_one` crate 的 `add_one` 函数。打开 *adder/src/main.rs*，把 `main` 改成调用 `add_one`，如示例 14-7 所示。

**文件名：`adder/src/main.rs`**
```rust
fn main() {
    let num = 10;
    println!("Hello, world! {num} plus one is {}!", add_one::add_one(num));
}
```

**示例 14-7：在 `adder` crate 中使用 `add_one` 库 crate**

　　在顶层 *add* 目录运行 `cargo build`，构建整个工作空间！


```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

　　要从 *add* 目录运行二进制 crate，可以用 `-p` 参数加上包名，指定要运行工作空间中的哪个包：


```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

　　这会运行 *adder/src/main.rs* 中的代码，而它依赖 `add_one` crate。

### 在工作空间中依赖外部包

　　注意：工作空间只在顶层有一份 *Cargo.lock*，而不是每个 crate 目录各有一份。这能确保所有 crate 使用同一版本的依赖。若我们在 *adder/Cargo.toml* 与 *add_one/Cargo.toml* 中都加入 `rand` 包，Cargo 会把两者解析为同一个 `rand` 版本，并记录在这一份 *Cargo.lock* 中。让工作空间中的所有 crate 使用相同依赖，意味着它们彼此始终兼容。我们把 `rand` crate 加到 *add_one/Cargo.toml* 的 `[dependencies]` 小节，以便在 `add_one` crate 中使用它：


<span class="filename">文件名：add_one/Cargo.toml</span>

```toml
[dependencies]
rand = "0.10.1"
```

　　现在可以在 *add_one/src/lib.rs* 中加入 `use rand;`；在 *add* 目录运行 `cargo build` 构建整个工作空间时，会拉取并编译 `rand` crate。因为我们引入了 `rand` 却没有使用它，会得到一条警告：


```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

　　顶层 *Cargo.lock* 现在包含了 `add_one` 对 `rand` 的依赖信息。不过，即便工作空间某处用了 `rand`，其他 crate 也不能直接使用它，除非也在它们的 *Cargo.toml* 中加入 `rand`。例如，若在 `adder` 包的 *adder/src/main.rs* 中加入 `use rand;`，会得到错误：


```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

　　要修复这一点，编辑 `adder` 包的 *Cargo.toml*，同样把 `rand` 声明为依赖。构建 `adder` 包时，会把 `rand` 加入 *Cargo.lock* 中 `adder` 的依赖列表，但不会再额外下载 `rand` 的副本。只要各包指定的 `rand` 版本兼容，Cargo 就会确保工作空间中每个使用 `rand` 的 crate 都用同一版本，既节省空间，也保证工作空间内的 crate 彼此兼容。

　　若工作空间中的 crate 为同一依赖指定了不兼容的版本，Cargo 会分别解析它们，但仍会尽量解析出尽可能少的版本。

### 为工作空间添加测试

　　再做一个增强：在 `add_one` crate 内为 `add_one::add_one` 函数添加测试：

<span class="filename">文件名：add_one/src/lib.rs</span>

```rust
pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(3, add_one(2));
    }
}
```

　　现在在顶层 *add* 目录运行 `cargo test`。在这种结构的工作空间中运行 `cargo test`，会运行工作空间里所有 crate 的测试：


```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　输出的第一节显示 `add_one` crate 中的 `it_works` 测试通过；下一节显示 `adder` crate 中未找到测试；最后一节显示 `add_one` crate 中未找到文档测试。

　　也可以从顶层目录用 `-p` 标志并指定 crate 名，只运行工作空间中某一个 crate 的测试：


```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　这份输出表明 `cargo test` 只运行了 `add_one` crate 的测试，没有运行 `adder` crate 的测试。

　　若要把工作空间中的 crate 发布到 [crates.io](https://crates.io/)，每个 crate 需要单独发布。与 `cargo test` 类似，可以用 `-p` 标志并指定要发布的 crate 名，发布工作空间中的某一个 crate。

　　作为额外练习，请仿照 `add_one` crate，在这个工作空间中再添加一个 `add_two` crate！

　　随着项目变大，可以考虑使用工作空间：它让你处理更小、更易理解的组件，而不是一大坨代码。此外，若多个 crate 经常同时改动，把它们放在同一工作空间里，协作也会更轻松。
