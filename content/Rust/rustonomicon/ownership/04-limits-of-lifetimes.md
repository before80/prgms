+++
title = "3.4 生命周期的局限"
date = 2026-08-06T17:08:00+08:00
weight = 14
type = "docs"
description = "生命周期检查的边界与不当缩减借用"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 生命周期的局限


> 原文链接: [https://doc.rust-lang.org/nomicon/lifetime-mismatch.html](https://doc.rust-lang.org/nomicon/lifetime-mismatch.html)


　　给定下列代码：

```rust,compile_fail
#[derive(Debug)]
struct Foo;

impl Foo {
    fn mutate_and_share(&mut self) -> &Self { &*self }
    fn share(&self) {}
}

fn main() {
    let mut foo = Foo;
    let loan = foo.mutate_and_share();
    foo.share();
    println!("{:?}", loan);
}
```

　　有人可能期望它能编译。我们调用 `mutate_and_share`，它临时可变借用 `foo`，但只返回共享引用。因此我们期望 `foo.share()` 成功，因为 `foo` 不应仍被可变借用。

　　然而编译时：

```text
error[E0502]: cannot borrow `foo` as immutable because it is also borrowed as mutable
  --> src/main.rs:12:5
   |
11 |     let loan = foo.mutate_and_share();
   |                --- mutable borrow occurs here
12 |     foo.share();
   |     ^^^ immutable borrow occurs here
13 |     println!("{:?}", loan);
```

　　发生了什么？我们得到与[上一节示例 2][ex2]完全相同的推理。脱糖程序如下：

```rust,ignore
struct Foo;

impl Foo {
    fn mutate_and_share<'a>(&'a mut self) -> &'a Self { &'a *self }
    fn share<'a>(&'a self) {}
}

fn main() {
    'b: {
        let mut foo: Foo = Foo;
        'c: {
            let loan: &'c Foo = Foo::mutate_and_share::<'c>(&'c mut foo);
            'd: {
                Foo::share::<'d>(&'d foo);
            }
            println!("{:?}", loan);
        }
    }
}
```

　　生命周期系统被迫把 `&mut foo` 扩展到生命周期 `'c`，因为 `loan` 的生命周期与 `mutate_and_share` 的签名。随后当我们试图调用 `share`，它看到我们试图 alias 那个 `&'c mut foo` 并报错！

　　按我们真正在意的引用语义，此程序显然正确，但生命周期系统粒度太粗，无法处理。

## 不当缩短的借用

　　下列代码编译失败，因为 Rust 看到变量 `map` 被借用两次，无法推断第一次借用在第二次之前已不需要。Rust 保守地回退到用整个作用域作为第一次借用。这最终会修复。

```rust,compile_fail
# use std::collections::HashMap;
# use std::hash::Hash;
fn get_default<'m, K, V>(map: &'m mut HashMap<K, V>, key: K) -> &'m mut V
where
    K: Clone + Eq + Hash,
    V: Default,
{
    match map.get_mut(&key) {
        Some(value) => value,
        None => {
            map.insert(key.clone(), V::default());
            map.get_mut(&key).unwrap()
        }
    }
}
```

　　因生命周期限制，`&mut map` 的生命周期与其他可变借用重叠，导致编译错误：

```text
error[E0499]: cannot borrow `*map` as mutable more than once at a time
  --> src/main.rs:12:13
   |
4  |   fn get_default<'m, K, V>(map: &'m mut HashMap<K, V>, key: K) -> &'m mut V
   |                  -- lifetime `'m` defined here
...
9  |       match map.get_mut(&key) {
   |       -     --- first mutable borrow occurs here
   |  _____|
   | |
10 | |         Some(value) => value,
11 | |         None => {
12 | |             map.insert(key.clone(), V::default());
   | |             ^^^ second mutable borrow occurs here
13 | |             map.get_mut(&key).unwrap()
14 | |         }
15 | |     }
   | |_____- returning this value requires that `*map` is borrowed for `'m`
```

[ex2]: lifetimes.html#示例别名可变引用
