+++
title = "03-深入生命周期"
date = 2026-08-12T20:00:00+08:00
weight = 54
type = "docs"
description = "深入生命周期 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/lifetime/advance.html](https://practice-rust-zh.beatai.org/lifetime/advance.html)

# 深入生命周期

## 特征约束
就像泛型类型可以有约束一样，生命周期也可以有约束 ，如下所示：
- `T: 'a`，所有引用在 `T` 必须超过生命周期 `'a`
- `T: Trait + 'a`: `T` 必须实现特征 `Trait` 并且所有引用在 `T` 必须超过生命周期 `'a`

**示例**
```rust
use std::fmt::Debug; // 特征约束使用

#[derive(Debug)]
struct Ref<'a, T: 'a>(&'a T);
// `Ref` 包含对泛型类型 `T` 的引用，该泛型类型具有
// 未知的生命周期 `'a`. `T` 是约定任何
// 引用在 `T` 必须大于 `'a` 。此外，在生命周期
// 里 `Ref` 不能超过 `'a`。

// 使用 `Debug` 特征打印的通用函数。
fn print<T>(t: T) where
    T: Debug {
    println!("`print`: t is {:?}", t);
}

// 这里引用 `T` 使用 where `T` 实现
// `Debug` 和所有引用 `T` 都要比 `'a` 长
// 此外，`'a`必须要比函数声明周期长
fn print_ref<'a, T>(t: &'a T) where
    T: Debug + 'a {
    println!("`print_ref`: t is {:?}", t);
}

fn main() {
    let x = 7;
    let ref_x = Ref(&x);

    print_ref(&ref_x);
    print(ref_x);
}
```

1. 🌟
```rust
/* 使用生命周期注释结构体
1. `r` 和 `s` 必须是不同生命周期
2. `s` 的生命周期需要大于 'r'
*/
struct DoubleRef<T> {
    r: &T,
    s: &T
}
fn main() {
    println!("Success!")
}
```


2. 🌟🌟
```rust
/* 添加类型约束使下面代码正常运行 */
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a, 'b> ImportantExcerpt<'a> {
    fn announce_and_return_part(&'a self, announcement: &'b str) -> &'b str {
        println!("Attention please: {}", announcement);
        self.part
    }
}

fn main() {
    println!("Success!")
}
```

3. 🌟🌟
```rust
/* 添加类型约束使下面代码正常运行 */
fn f<'a, 'b>(x: &'a i32, mut y: &'b i32) {
    y = x;                      
    let r: &'b &'a i32 = &&0;   
}

fn main() {
    println!("Success!")
}
```

## HRTB（更高等级特征约束）(Higher-ranked trait bounds)
类型约束可能在生命周期中排名更高。这些约束指定了一个约束对于所有生命周期都为真。例如，诸如此类的约束 `for<'a> &'a T: PartialEq<i32>` 需要如下实现：

```rust
impl<'a> PartialEq<i32> for &'a T {
    // ...
}
```

然后可以用于将一个 `&'a T` 与任何生命周期进行比较 `i32` 。

这里只能使用更高级别的约束，因为引用的生命周期比函数上任何可能的生命周期参数都短。

4. 🌟🌟🌟
```rust
/* 添加 HRTB 使下面代码正常运行！ */
fn call_on_ref_zero<'a, F>(f: F) where F: Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}

fn main() {
    println!("Success!")
}
```
## NLL（非词汇生命周期）(Non-Lexical Lifetime)
在解释 NLL 之前，我们先看一段代码：
```rust
fn main() {
   let mut s = String::from("hello");

    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);

    let r3 = &mut s;
    println!("{}", r3);
}
```

根据我们目前的知识，这段代码会因为违反 Rust 中的借用规则而导致错误。

但是，如果您执行 `cargo run` ，那么一切都没问题，那么这里发生了什么？

编译器在作用域结束之前判断不再使用引用的能力称为 **非词法生命周期**（简称 **NLL** ）。

有了这种能力，编译器就知道最后一次使用引用是什么时候，并根据这些知识优化借用规则。

```rust
let mut u = 0i32;
let mut v = 1i32;
let mut w = 2i32;

// lifetime of `a` = α ∪ β ∪ γ
let mut a = &mut u;     // --+ α. lifetime of `&mut u`  --+ lexical "lifetime" of `&mut u`,`&mut u`, `&mut w` and `a`
use(a);                 //   |                            |
*a = 3; // <-----------------+                            |
...                     //                                |
a = &mut v;             // --+ β. lifetime of `&mut v`    |
use(a);                 //   |                            |
*a = 4; // <-----------------+                            |
...                     //                                |
a = &mut w;             // --+ γ. lifetime of `&mut w`    |
use(a);                 //   |                            |
*a = 5; // <-----------------+ <--------------------------+
```

## 再借用

学习了 NLL 之后，我们现在可以很容易地理解再借用了。

**示例**
```rust
#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn move_to(&mut self, x: i32, y: i32) {
        self.x = x;
        self.y = y;
    }
}

fn main() {
    let mut p = Point { x: 0, y: 0 };
    let r = &mut p;
    // 这里是再借用
    let rr: &Point = &*r;

    println!("{:?}", rr); // 这里结束再借用

    // 再借用结束，现在我们可以继续使用 `r`
    r.move_to(10, 10);
    println!("{:?}", r);
}
```


5. 🌟🌟
```rust
/* 通过重新排序一些代码使下面代码正常运行 */
fn main() {
    let mut data = 10;
    let ref1 = &mut data;
    let ref2 = &mut *ref1;

    *ref1 += 1;
    *ref2 += 2;

    println!("{}", data);
}
```


## 未约束的生命周期
在 [Nomicon - Unbounded Lifetimes](https://doc.rust-lang.org/nomicon/unbounded-lifetimes.html) 中查看更多信息。


## 更多省略规则

```rust
impl<'a> Reader for BufReader<'a> {
    // 'a 在以下方法中不使用
}

// 可以写为：
impl Reader for BufReader<'_> {
    
}
```

```rust
// Rust 2015
struct Ref<'a, T: 'a> {
    field: &'a T
}

// Rust 2018
struct Ref<'a, T> {
    field: &'a T
}
```


## 艰难的练习

6. 🌟🌟🌟🌟
```rust
/* 使下面代码正常运行 */
struct Interface<'a> {
    manager: &'a mut Manager<'a>
}

impl<'a> Interface<'a> {
    pub fn noop(self) {
        println!("interface consumed");
    }
}

struct Manager<'a> {
    text: &'a str
}

struct List<'a> {
    manager: Manager<'a>,
}

impl<'a> List<'a> {
    pub fn get_interface(&'a mut self) -> Interface {
        Interface {
            manager: &mut self.manager
        }
    }
}

fn main() {
    let mut list = List {
        manager: Manager {
            text: "hello"
        }
    };

    list.get_interface().noop();

    println!("Interface should be dropped here and the borrow released");

    use_list(&list);
}

fn use_list(list: &List) {
    println!("{}", list.manager.text);
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/lifetime/advance.md)找到答案(在 solutions 路径下)
