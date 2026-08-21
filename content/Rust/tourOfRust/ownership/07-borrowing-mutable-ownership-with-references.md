+++
title = "07-通过引用借用可变所有权"
date = 2026-08-17T22:00:00+08:00
weight = 51
type = "docs"
description = "通过引用借用可变所有权 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/49_zh-cn.html](https://tourofrust.com/49_zh-cn.html)

# 通过引用借用可变所有权

我们也可以使用 `&mut` 操作符来借用对一个资源的可变访问权限。 在发生了可变借用后，一个资源的所有者便不可以再次被借用或者修改。

内存细节：
* Rust 之所以要避免同时存在两种可以改变所拥有变量值的方式，是因为此举可能会导致潜在的数据争用（data race）。

## 示例代码

```rust
struct Foo {
    x: i32,
}

fn do_something(f: Foo) {
    println!("{}", f.x);
    // f 在这里被 dropped 释放
}

fn main() {
    let mut foo = Foo { x: 42 };
    let f = &mut foo;

    // do_something(foo);
    // 会报错: do_something(foo);
    // 因为 foo 已经被可变借用而无法取得其所有权

    // foo.x = 13;
    // 会报错: foo.x = 13;
    // 因为 foo 已经被可变借用而无法被修改

    f.x = 13;
    // f 会因为此后不再被使用而被 dropped 释放

    println!("{}", foo.x);

    // 现在修改可以正常进行因为其所有可变引用已经被 dropped 释放
    foo.x = 7;

    // 移动 foo 的所有权到一个函数中
    do_something(foo);
}
```
