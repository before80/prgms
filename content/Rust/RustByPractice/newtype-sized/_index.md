+++
title = "第19章 newtype 和 Sized"
date = 2026-08-12T20:00:00+08:00
weight = 58
type = "docs"
description = "newtype 和 Sized — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/newtype-sized.html](https://practice-rust-zh.beatai.org/newtype-sized.html)

# newtype 和 Sized

## Newtype
孤儿规则要求：只有当 trait 或类型其一属于当前 crate 时，才能为类型实现该 trait。

**newtype 模式** 通过定义一个 **元组结构体** 新类型，帮助绕开这一限制。

1. 🌟
```rust
use std::fmt;

/* 定义 Wrapper 类型 */
__;

// Display 是外部 trait
impl fmt::Display for Wrapper {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

fn main() {
    // Vec 是外部类型，不能直接为 Vec 实现外部 trait Display
    let w = Wrapper(vec![String::from("hello"), String::from("world")]);
    println!("w = {}", w);
}
```

2. 🌟 隐藏原类型的方法
```rust
/* 让代码通过编译 */
struct Meters(u32);

fn main() {
    let i: u32 = 2;
    assert_eq!(i.pow(2), 4);

    let n = Meters(i);
    // `pow` 定义在 u32 上，直接调用会报错
    assert_eq!(n.pow(2), 4);
}
```

3. 🌟🌟 `newtype` 能在编译期保证传入的值类型正确
```rust
/* 让它工作 */
struct Years(i64);

struct Days(i64);

impl Years {
    pub fn to_days(&self) -> Days {
        Days(self.0 * 365)
    }
}


impl Days {
    pub fn to_years(&self) -> Years {
        Years(self.0 / 365)
    }
}

// 检查年龄（单位：年），必须接收 Years
fn old_enough(age: &Years) -> bool {
    age.0 >= 18
}

fn main() {
    let age = Years(5);
    let age_days = age.to_days();
    println!("Old enough {}", old_enough(&age));
    println!("Old enough {}", old_enough(&age_days));
}
```

4. 🌟🌟
```rust
use std::ops::Add;
use std::fmt::{self, format};

struct Meters(u32);
impl fmt::Display for Meters {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "There are still {} meters left", self.0)
    }
}

impl Add for Meters {
    type Output = Self;

    fn add(self, other: Meters) -> Self {
        Self(self.0 + other.0)
    }
}
fn main() {
    let d = calculate_distance(Meters(10), Meters(20));
    assert_eq!(format!("{}",d), "There are still 30 meters left");
}

/* 实现 calculate_distance  */
fn calculate_distance
```

## 类型别名 (Type alias)
类型别名可以提升代码可读性。

```rust
type Thunk = Box<dyn Fn() + Send + 'static>;

let f: Thunk = Box::new(|| println!("hi"));

fn takes_long_type(f: Thunk) {
    // --snip--
}

fn returns_long_type() -> Thunk {
    // --snip--
}
```

```rust
type Result<T> = std::result::Result<T, std::io::Error>;
```

与 newtype 不同，类型别名不会生成新类型，因此下面的代码合法：
```rust
type Meters = u32;

let x: u32 = 5;
let y: Meters = 5;

println!("x + y = {}", x + y);
```

5. 🌟
```rust
enum VeryVerboseEnumOfThingsToDoWithNumbers {
    Add,
    Subtract,
}

/* 填空 */
__

fn main() {
    // 可以用别名访问枚举值，避免冗长名字
    let x = Operations::Add;
}
```

6. 🌟🌟 Rust 有一些保留的别名，其中一个可在 `impl` 中使用。
```rust
enum VeryVerboseEnumOfThingsToDoWithNumbers {
    Add,
    Subtract,
}

impl VeryVerboseEnumOfThingsToDoWithNumbers {
    fn run(&self, x: i32, y: i32) -> i32 {
        match self {
            __::Add => x + y,
            __::Subtract => x - y,
        }
    }
}
```

## DST 与不定长类型
概念较复杂，这里不展开，可参考 [The Book](https://doc.rust-lang.org/book/ch19-04-advanced-types.html?highlight=DST#dynamically-sized-types-and-the-sized-trait)。

7. 🌟🌟🌟 动态长度数组属于 DST，无法直接使用
```rust
/* Make it work with const generics */
fn my_function(n: usize) -> [u32; usize] {
    [123; n]
}

fn main() {
    let arr = my_function();
    println!("{:?}",arr);
}
```

8. 🌟🌟 Slice 本身是 unsized，但它的引用是定长的。
```rust
/* Make it work with slice references */
fn main() {
    let s: str = "Hello there!";

    let arr: [u8] = [1, 2, 3];
}
```

9. 🌟🌟 Trait 也是 unsized 类型
```rust
/* 用两种方式让它工作 */
use std::fmt::Display;
fn foobar(thing: Display) {}    

fn main() {
}
```
