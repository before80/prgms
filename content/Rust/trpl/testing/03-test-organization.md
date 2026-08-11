+++
title = "11.3 测试组织"
date = 2026-08-05T08:44:00+08:00
weight = 48
type = "docs"
description = "组织单元测试与集成测试"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 测试组织


> 原文链接: [https://doc.rust-lang.org/stable/book/ch11-03-test-organization.html](https://doc.rust-lang.org/stable/book/ch11-03-test-organization.html)


## 测试组织

　　正如本章开头所说，测试是一门复杂的学科，不同的人使用不同的术语与组织方式。Rust 社区主要从两类思考测试：单元测试与集成测试。*单元测试*更小、更聚焦，一次隔离地测试一个模块，并且可以测试私有接口。*集成测试*完全位于你的库之外，以任何其他外部代码相同的方式使用你的代码：只用公共接口，并且每个测试可能锻炼多个模块。

　　编写这两类测试都很重要，以确保库的各个部分在分开时与合在一起时都按你的预期工作。

### 单元测试

　　单元测试的目的是：与其余代码隔离地测试每一代码单元，以便快速定位哪里在按预期工作、哪里没有。你会把单元测试放在 _src_ 目录下、与被测代码相同的各个文件中。惯例是在每个文件中创建一个名为 `tests` 的模块来容纳测试函数，并用 `cfg(test)` 标注该模块。

#### `tests` 模块与 `#[cfg(test)]`

　　`tests` 模块上的 `#[cfg(test)]` 注解告诉 Rust：仅在运行 `cargo test` 时才编译并运行测试代码，而不是在运行 `cargo build` 时。这样，当你只想构建库时可以节省编译时间，也因为测试未包含在内而节省最终编译产物的空间。你会看到：集成测试在不同目录中，因此不需要 `#[cfg(test)]` 注解。但因为单元测试与代码在同一文件中，你会用 `#[cfg(test)]` 指明它们不应包含在编译结果里。

　　回想本章第一节生成新 `adder` 项目时，Cargo 为我们生成了这段代码：

<span class="filename">文件名：src/lib.rs</span>

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

　　在自动生成的 `tests` 模块上，属性 `cfg` 表示 *configuration*（配置），告诉 Rust：只有在给定某个配置选项时才应包含后面的条目。本例中配置选项是 `test`，由 Rust 提供，用于编译与运行测试。通过使用 `cfg` 属性，Cargo 仅在我们主动用 `cargo test` 运行测试时才编译测试代码。这既包括带 `#[test]` 注解的函数，也包括该模块内可能存在的任何辅助函数。

#### 测试私有函数

　　测试社区中一直有争论：是否应直接测试私有函数；其他语言也往往难以或无法测试私有函数。无论你坚持哪种测试理念，Rust 的可见性规则都允许你测试私有函数。考虑示例 11-12 中带有私有函数 `internal_adder` 的代码。

**文件名：`src/lib.rs`**
```rust
pub fn add_two(a: u64) -> u64 {
    internal_adder(a, 2)
}

fn internal_adder(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn internal() {
        let result = internal_adder(2, 2);
        assert_eq!(result, 4);
    }
}
```

**示例 11-12：测试私有函数**

　　注意 `internal_adder` 函数并未标为 `pub`。测试只是普通 Rust 代码，`tests` 模块也只是另一个模块。正如我们在[「模块树中引用条目的路径」][paths]中所讨论的，子模块中的条目可以使用其祖先模块中的条目。在这个测试中，我们用 `use super::*` 把属于 `tests` 模块父模块的所有条目引入作用域，然后测试就可以调用 `internal_adder`。若你认为不应测试私有函数，Rust 里也没有任何东西会强迫你这么做。

### 集成测试

　　在 Rust 中，集成测试完全位于你的库之外。它们以任何其他代码相同的方式使用你的库，这意味着它们只能调用属于库公共 API 的函数。其目的是测试库的许多部分能否正确协同工作。单独工作正常的代码单元在集成时可能出问题，因此对集成代码的测试覆盖也很重要。要创建集成测试，首先需要一个 _tests_ 目录。

#### _tests_ 目录

　　我们在项目目录顶层、与 _src_ 并列处创建 _tests_ 目录。Cargo 知道要在该目录中查找集成测试文件。然后可以创建任意多个测试文件，Cargo 会把每个文件编译为独立的 crate。

　　我们来创建一个集成测试。在示例 11-12 的代码仍在 _src/lib.rs_ 中的情况下，创建 _tests_ 目录，并新建名为 _tests/integration_test.rs_ 的文件。目录结构应如下：

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

　　把示例 11-13 中的代码输入 _tests/integration_test.rs_ 文件。

**文件名：`tests/integration_test.rs`**
```rust
use adder::add_two;

#[test]
fn it_adds_two() {
    let result = add_two(2);
    assert_eq!(result, 4);
}
```

**示例 11-13：对 `adder` crate 中某个函数的集成测试**

　　_tests_ 目录中的每个文件都是单独的 crate，因此需要把我们的库引入每个测试 crate 的作用域。为此我们在代码顶部添加 `use adder::add_two;`，这在单元测试中并不需要。

　　我们不必用 `#[cfg(test)]` 标注 _tests/integration_test.rs_ 中的任何代码。Cargo 对 _tests_ 目录有特殊处理，仅在运行 `cargo test` 时才编译该目录中的文件。现在运行 `cargo test`：

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.31s
     Running unittests src/lib.rs (target/debug/deps/adder-1082c4b063a8fbe6)

running 1 test
test tests::internal ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_test.rs (target/debug/deps/integration_test-1082c4b063a8fbe6)

running 1 test
test it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　输出的三个部分分别包括单元测试、集成测试与文档测试。注意：若某一部分中有任何测试失败，后面的部分就不会运行。例如，若单元测试失败，就不会有集成测试与文档测试的输出，因为只有全部单元测试通过时才会运行那些测试。

　　单元测试的第一部分与我们一直看到的相同：每个单元测试一行（包括我们在示例 11-12 中添加的名为 `internal` 的测试），然后是单元测试的摘要行。

　　集成测试部分以 `Running tests/integration_test.rs` 一行开始。接下来是该集成测试中每个测试函数的一行，以及就在 `Doc-tests adder` 部分开始之前的集成测试结果摘要行。

　　每个集成测试文件都有自己的部分，因此若在 _tests_ 目录中添加更多文件，就会有更多集成测试部分。

　　我们仍可通过把测试函数名作为参数传给 `cargo test` 来运行特定的集成测试函数。要运行特定集成测试文件中的所有测试，使用 `cargo test` 的 `--test` 参数后跟文件名：

```console
$ cargo test --test integration_test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.64s
     Running tests/integration_test.rs (target/debug/deps/integration_test-82e7799c1bc62298)

running 1 test
test it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　该命令只运行 _tests/integration_test.rs_ 文件中的测试。

#### 集成测试中的子模块

　　随着集成测试增多，你可能想在 _tests_ 目录中创建更多文件来帮助组织；例如，可以按所测试的功能对测试函数分组。如前所述，_tests_ 目录中的每个文件都被编译为各自独立的 crate，这有助于创建更接近最终用户使用你 crate 方式的独立作用域。然而，这也意味着 _tests_ 目录中的文件并不共享你在第 7 章学到的、_src_ 中文件把代码拆成模块与文件时的相同行为。

　　当你有一组要在多个集成测试文件中使用的辅助函数，并试图按第 7 章[「把模块拆分到不同文件」][separating-modules-into-files]一节的步骤把它们提取到公共模块时，_tests_ 目录文件的不同行为最为明显。例如，若创建 _tests/common.rs_ 并在其中放一个名为 `setup` 的函数，我们可以在 `setup` 中加入希望从多个测试文件的多个测试函数中调用的代码：

<span class="filename">文件名：tests/common.rs</span>

```rust
pub fn setup() {
    // setup code specific to your library's tests would go here
}
```

　　再次运行测试时，即使该文件不包含任何测试函数，我们也没有从任何地方调用 `setup`，仍会在测试输出中看到针对 _common.rs_ 文件的新部分：

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.89s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::internal ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/common.rs (target/debug/deps/common-92948b65e88960b4)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_test.rs (target/debug/deps/integration_test-92948b65e88960b4)

running 1 test
test it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　让 `common` 出现在测试结果中并显示 `running 0 tests` 并不是我们想要的。我们只是想与其他集成测试文件共享一些代码。为避免 `common` 出现在测试输出中，不要创建 _tests/common.rs_，而是创建 _tests/common/mod.rs_。项目目录现在如下：

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

　　这是我们在第 7 章[「备选文件路径」][alt-paths]中提到的、Rust 也能理解的较旧命名约定。这样命名文件告诉 Rust 不要把 `common` 模块当作集成测试文件。当我们把 `setup` 函数代码移到 _tests/common/mod.rs_ 并删除 _tests/common.rs_ 后，测试输出中的那一部分就不再出现。_tests_ 目录子目录中的文件不会被编译为单独的 crate，也不会在测试输出中占有部分。

　　创建 _tests/common/mod.rs_ 之后，我们可以从任何集成测试文件中把它当作模块使用。下面是从 _tests/integration_test.rs_ 的 `it_adds_two` 测试中调用 `setup` 函数的例子：

<span class="filename">文件名：tests/integration_test.rs</span>

```rust
use adder::add_two;

mod common;

#[test]
fn it_adds_two() {
    common::setup();

    let result = add_two(2);
    assert_eq!(result, 4);
}
```

　　注意 `mod common;` 声明与我们在示例 7-21 中演示的模块声明相同。然后在测试函数中，我们可以调用 `common::setup()` 函数。

#### 针对二进制 Crate 的集成测试

　　若我们的项目是只包含 _src/main.rs_、没有 _src/lib.rs_ 的二进制 crate，就无法在 _tests_ 目录中创建集成测试，并用 `use` 语句把 _src/main.rs_ 中定义的函数引入作用域。只有库 crate 才会暴露其他 crate 可以使用的函数；二进制 crate 意在独立运行。

　　这也是提供二进制的 Rust 项目常有一个简洁的 _src/main.rs_、并调用位于 _src/lib.rs_ 中逻辑的原因之一。采用这种结构后，集成测试*可以*用 `use` 测试库 crate，使重要功能可用。若重要功能正常，_src/main.rs_ 中那少量代码通常也会正常，而且那少量代码不必测试。

## 小结

　　Rust 的测试特性提供了一种方式来指明代码应如何工作，以确保即使你做出改动，它仍按预期继续工作。单元测试分别锻炼库的不同部分，并可测试私有实现细节。集成测试检查库的许多部分能否正确协同，并用库的公共 API 以外部代码相同的方式测试代码。即便 Rust 的类型系统与所有权规则有助于防止某些种类的 bug，测试对于减少与代码预期行为相关的逻辑 bug 仍然重要。

　　让我们把本章与前面各章所学结合起来，做一个项目吧！

[paths]: ../../modules/03-paths-for-referring-to-an-item-in-the-module-tree/
[separating-modules-into-files]: ../../modules/05-separating-modules-into-different-files/
[alt-paths]: ../../modules/05-separating-modules-into-different-files/#alternate-file-paths
