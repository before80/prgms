+++
title = "11.2 控制测试的运行方式"
date = 2026-08-05T08:44:00+08:00
weight = 47
type = "docs"
description = "控制并行、输出、筛选与忽略测试的运行方式"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 控制测试的运行方式


> 原文链接: [https://doc.rust-lang.org/stable/book/ch11-02-running-tests.html](https://doc.rust-lang.org/stable/book/ch11-02-running-tests.html)


## 控制测试的运行方式

　　正如 `cargo run` 会编译代码再运行生成的二进制，`cargo test` 会以测试模式编译代码并运行生成的测试二进制。`cargo test` 生成的二进制的默认行为是：并行运行所有测试，并捕获测试运行期间产生的输出，使其不显示出来，从而更容易阅读与测试结果相关的输出。不过，你可以通过命令行选项改变这些默认行为。

　　有些命令行选项交给 `cargo test`，有些交给生成的测试二进制。要分隔这两类参数，先列出交给 `cargo test` 的参数，再写分隔符 `--`，然后写交给测试二进制的参数。运行 `cargo test --help` 可显示可用于 `cargo test` 的选项；运行 `cargo test -- --help` 可显示分隔符之后可用的选项。这些选项也记录在 [_The `rustc` Book_ 的 “Tests” 一节][tests]中。

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### 并行或串行运行测试

　　运行多个测试时，默认它们通过线程并行运行，因此能更快完成并更早得到反馈。因为测试同时运行，你必须确保测试之间不相互依赖，也不依赖任何共享状态——包括共享环境，例如当前工作目录或环境变量。

　　例如，假设每个测试都运行一些代码：在磁盘上创建名为 _test-output.txt_ 的文件并向其中写入数据，然后读取该文件并断言它包含某个特定值，而每个测试期望的值不同。因为测试同时运行，一个测试可能在另一个测试写入与读取之间覆盖该文件。第二个测试就会失败——不是因为代码不正确，而是因为测试在并行运行时互相干扰。一种解决办法是让每个测试写入不同文件；另一种是一次只运行一个测试。

　　若不想并行运行测试，或想更细粒度地控制所用线程数，可以把 `--test-threads` 标志以及想使用的线程数发给测试二进制。例如：

```console
$ cargo test -- --test-threads=1
```

　　我们把测试线程数设为 `1`，告诉程序不要使用任何并行。用一个线程运行测试会比并行更慢，但若测试共享状态，它们就不会互相干扰。

### 显示函数输出

　　默认情况下，若测试通过，Rust 的测试库会捕获打印到标准输出的任何内容。例如，若在测试中调用 `println!` 且测试通过，我们不会在终端看到 `println!` 的输出，只会看到表明测试通过的那一行。若测试失败，我们会在失败信息的其余部分中看到打印到标准输出的内容。

　　例如，示例 11-10 有一个傻傻的函数：打印其参数的值并返回 10，以及一个会通过的测试和一个会失败的测试。

**文件名：`src/lib.rs`**
```rust
fn prints_and_returns_10(a: i32) -> i32 {
    println!("I got the value {a}");
    10
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn this_test_will_pass() {
        let value = prints_and_returns_10(4);
        assert_eq!(value, 10);
    }

    #[test]
    fn this_test_will_fail() {
        let value = prints_and_returns_10(8);
        assert_eq!(value, 5);
    }
}
```

**示例 11-10：针对调用 `println!` 的函数的测试**

　　用 `cargo test` 运行这些测试时，会看到如下输出：

```console
$ cargo test
   Compiling silly-function v0.1.0 (file:///projects/silly-function)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running unittests src/lib.rs (target/debug/deps/silly_function-160869f38cff9166)

running 2 tests
test tests::this_test_will_fail ... FAILED
test tests::this_test_will_pass ... ok

failures:

---- tests::this_test_will_fail stdout ----
I got the value 8

thread 'tests::this_test_will_fail' (6019863) panicked at src/lib.rs:19:9:
assertion `left == right` failed
  left: 10
 right: 5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::this_test_will_fail

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　注意：这段输出中完全看不到通过测试运行时打印的 `I got the value 4`——该输出已被捕获。失败测试的输出 `I got the value 8` 出现在测试摘要输出的相应部分，那里也显示了测试失败的原因。

　　若也想看到通过测试的打印值，可以用 `--show-output` 告诉 Rust 同时显示成功测试的输出：

```console
$ cargo test -- --show-output
```

　　再次用 `--show-output` 标志运行示例 11-10 中的测试时，会看到如下输出：

```console
$ cargo test -- --show-output
   Compiling silly-function v0.1.0 (file:///projects/silly-function)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.60s
     Running unittests src/lib.rs (target/debug/deps/silly_function-160869f38cff9166)

running 2 tests
test tests::this_test_will_fail ... FAILED
test tests::this_test_will_pass ... ok

successes:

---- tests::this_test_will_pass stdout ----
I got the value 4


successes:
    tests::this_test_will_pass

failures:

---- tests::this_test_will_fail stdout ----
I got the value 8

thread 'tests::this_test_will_fail' (6022313) panicked at src/lib.rs:19:9:
assertion `left == right` failed
  left: 10
 right: 5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::this_test_will_fail

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

### 按名称运行测试子集 {#running-a-subset-of-tests-by-name}

　　完整测试套件有时会跑很久。若你正在处理某个特定区域的代码，可能只想运行与之相关的测试。可以把想运行的测试名称作为参数传给 `cargo test`，以选择运行哪些测试。

　　为演示如何运行测试子集，我们先为 `add_two` 函数创建三个测试，如示例 11-11 所示，再选择运行其中哪些。

**文件名：`src/lib.rs`**
```rust
pub fn add_two(a: u64) -> u64 {
    a + 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_two_and_two() {
        let result = add_two(2);
        assert_eq!(result, 4);
    }

    #[test]
    fn add_three_and_two() {
        let result = add_two(3);
        assert_eq!(result, 5);
    }

    #[test]
    fn one_hundred() {
        let result = add_two(100);
        assert_eq!(result, 102);
    }
}
```

**示例 11-11：三个名称不同的测试**

　　若像之前那样不传任何参数运行测试，所有测试会并行运行：

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.62s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 3 tests
test tests::add_three_and_two ... ok
test tests::add_two_and_two ... ok
test tests::one_hundred ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

#### 运行单个测试

　　可以把任意测试函数的名称传给 `cargo test`，只运行该测试：

```console
$ cargo test one_hundred
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.69s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::one_hundred ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 2 filtered out; finished in 0.00s
```

　　只有名为 `one_hundred` 的测试运行了；另外两个测试名称不匹配。测试输出通过在末尾显示 `2 filtered out` 告诉我们还有更多测试未运行。

　　不能用这种方式指定多个测试名称；传给 `cargo test` 的只有第一个值会被使用。不过有办法运行多个测试。

#### 筛选以运行多个测试

　　我们可以指定测试名称的一部分，任何名称匹配该值的测试都会运行。例如，因为有两个测试的名称包含 `add`，可以运行 `cargo test add` 来运行那两个：

```console
$ cargo test add
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 2 tests
test tests::add_three_and_two ... ok
test tests::add_two_and_two ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.00s
```

　　该命令运行了名称中含有 `add` 的所有测试，并过滤掉了名为 `one_hundred` 的测试。另外注意：测试所在的模块会成为测试名称的一部分，因此可以通过按模块名筛选来运行某模块中的所有测试。

### 除非特别请求，否则忽略测试 {#ignoring-tests-unless-specifically-requested}

　　有时少数特定测试执行起来非常耗时，因此你可能希望在多数 `cargo test` 运行中排除它们。与其把想运行的全部测试都列成参数，不如用 `ignore` 属性标注耗时测试以排除它们，如下所示：

<span class="filename">文件名：src/lib.rs</span>

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    #[ignore]
    fn expensive_test() {
        // code that takes an hour to run
    }
}
```

　　在 `#[test]` 之后，我们为想排除的测试加上 `#[ignore]` 行。现在运行测试时，`it_works` 会运行，但 `expensive_test` 不会：

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.60s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 2 tests
test tests::expensive_test ... ignored
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　`expensive_test` 函数被列为 `ignored`。若只想运行被忽略的测试，可以用 `cargo test -- --ignored`：

```console
$ cargo test -- --ignored
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::expensive_test ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　通过控制运行哪些测试，可以确保 `cargo test` 的结果很快返回。当你到达适合检查 `ignored` 测试结果、且有时间等待的阶段时，可以改为运行 `cargo test -- --ignored`。若想运行所有测试（无论是否被忽略），可以运行 `cargo test -- --include-ignored`。
