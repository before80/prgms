+++
title = "01-测试"
date = 2026-08-18T08:45:00+08:00
weight = 34
type = "docs"
description = "测试 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes/testing.html](https://doc.rust-lang.org/reference/attributes/testing.html)

r[attributes.testing]
# 测试

下列[属性][attributes]用于指定执行测试的函数。以“test”模式编译 crate 时，会一并构建测试函数以及用于执行测试的测试框架。启用测试模式同时也会启用 [`test` 条件编译选项][`test` conditional compilation option]。

<!-- template:attributes -->
r[attributes.testing.test]
## `test` 属性

r[attributes.testing.test.intro]
*`test` [属性][attributes]*将函数标记为作为测试执行。

> [!EXAMPLE]
> ```rust
> # pub fn add(left: u64, right: u64) -> u64 { left + right }
> #[test]
> fn it_works() {
>     let result = add(2, 2);
>     assert_eq!(result, 4);
> }
> ```

r[attributes.testing.test.syntax]
`test` 属性使用 [MetaWord] 语法。

r[attributes.testing.test.allowed-positions]
`test` 属性只能应用于单态化的[自由函数][free functions]，且该函数不得接受参数，其返回类型须实现 [`Termination`] trait。

> **注意**
> 实现 [`Termination`] trait 的部分类型包括：
> * `()`
> * `Result<T, E> where T: Termination, E: Debug`

r[attributes.testing.test.duplicates]
对同一函数多次使用 `test` 时，仅第一次生效。

> **注意**
> `rustc` 会对第一次之后的使用发出 lint。将来这可能变成错误。

<!-- TODO: This is a minor lie. Currently rustc warns that duplicates are ignored, but it then generates multiple test entries with the same name. I would vote for rejecting this in the future. -->

r[attributes.testing.test.stdlib]
`test` 属性从标准库 prelude 导出为 [`std::prelude::v1::test`]。

r[attributes.testing.test.enabled]
这些函数仅在测试模式下编译。

> **注意**
> 通过向 `rustc` 传递 `--test` 参数或使用 `cargo test` 可启用测试模式。

r[attributes.testing.test.success]
测试框架会调用返回值的 [`report`] 方法，并根据结果 [`ExitCode`] 是否表示成功终止，将测试判定为通过或失败。
具体而言：
* 返回 `()` 的测试只要正常终止且不 panic 即通过。
* 返回 `Result<(), E>` 的测试只要返回 `Ok(())` 即通过。
* 返回 `ExitCode::SUCCESS` 的测试通过，返回 `ExitCode::FAILURE` 的测试失败。
* 不终止的测试既不算通过也不算失败。

> [!EXAMPLE]
> ```rust
> # use std::io;
> # fn setup_the_thing() -> io::Result<i32> { Ok(1) }
> # fn do_the_thing(s: &i32) -> io::Result<()> { Ok(()) }
> #[test]
> fn test_the_thing() -> io::Result<()> {
>     let state = setup_the_thing()?; // 预期成功
>     do_the_thing(&state)?;          // 预期成功
>     Ok(())
> }
> ```

<!-- template:attributes -->
r[attributes.testing.ignore]
## `ignore` 属性

r[attributes.testing.ignore.intro]
*`ignore` [属性][attributes]*可与 [`test` 属性][attributes.testing.test]一起使用，告知测试框架不要将该函数作为测试执行。

> [!EXAMPLE]
> ```rust
> #[test]
> #[ignore]
> fn check_thing() {
>     // …
> }
> ```

> **注意**
> `rustc` 测试框架支持 `--include-ignored` 标志以强制运行被忽略的测试。

r[attributes.testing.ignore.syntax]
`ignore` 属性使用 [MetaWord] 与 [MetaNameValueStr] 语法。

r[attributes.testing.ignore.reason]
`ignore` 属性的 [MetaNameValueStr] 形式可指定忽略该测试的原因。

> [!EXAMPLE]
> ```rust
> #[test]
> #[ignore = "not yet implemented"]
> fn mytest() {
>     // …
> }
> ```

r[attributes.testing.ignore.allowed-positions]
`ignore` 属性只能应用于带有 `test` 属性的函数。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[attributes.testing.ignore.duplicates]
对同一函数多次使用 `ignore` 时，仅第一次生效。

> **注意**
> `rustc` 会对第一次之后的使用发出 lint。将来这可能变成错误。

r[attributes.testing.ignore.behavior]
被忽略的测试在测试模式下仍会编译，但不会被执行。

<!-- template:attributes -->
r[attributes.testing.should_panic]
## `should_panic` 属性

r[attributes.testing.should_panic.intro]
*`should_panic` [属性][attributes]*使测试仅在其所应用于的[测试函数][attributes.testing.test]发生 panic 时才通过。

> [!EXAMPLE]
> ```rust
> #[test]
> #[should_panic(expected = "values don't match")]
> fn mytest() {
>     assert_eq!(1, 2, "values don't match");
> }
> ```

r[attributes.testing.should_panic.syntax]
`should_panic` 属性有以下形式：

- [MetaWord]
  > [!EXAMPLE]
  > ```rust,no_run
  > #[test]
  > #[should_panic]
  > fn mytest() { panic!("error: some message, and more"); }
  > ```

- [MetaNameValueStr] —— 给定字符串必须出现在 panic 消息中，测试才通过。
  > [!EXAMPLE]
  > ```rust,no_run
  > #[test]
  > #[should_panic = "some message"]
  > fn mytest() { panic!("error: some message, and more"); }
  > ```

- [MetaListNameValueStr] —— 与 [MetaNameValueStr] 语法相同，给定字符串必须出现在 panic 消息中。
  > [!EXAMPLE]
  > ```rust,no_run
  > #[test]
  > #[should_panic(expected = "some message")]
  > fn mytest() { panic!("error: some message, and more"); }
  > ```

r[attributes.testing.should_panic.allowed-positions]
`should_panic` 属性只能应用于带有 `test` 属性的函数。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[attributes.testing.should_panic.duplicates]
对同一函数多次使用 `should_panic` 时，仅第一次生效。

> **注意**
> `rustc` 会对第一次之后的使用发出面向未来兼容性的 lint 警告。将来这可能变成错误。

r[attributes.testing.should_panic.expected]
使用 [MetaNameValueStr] 形式，或带有 `expected` 键的 [MetaListNameValueStr] 形式时，给定字符串必须出现在 panic 消息的某处，测试才通过。

r[attributes.testing.should_panic.return]
测试函数的返回类型必须是 `()`。

[`Termination`]: std::process::Termination
[`report`]: std::process::Termination::report
[`test` conditional compilation option]: ../conditional-compilation.md#test
[attributes]: ../attributes.md
[`ExitCode`]: std::process::ExitCode
[free functions]: ../glossary.md#free-item
