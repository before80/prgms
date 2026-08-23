+++
title = "02-迭代器 Iterator"
date = 2026-08-12T20:00:00+08:00
weight = 57
type = "docs"
description = "迭代器 Iterator — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/functional-programing/iterator.html](https://practice-rust.beatai.org/functional-programing/iterator.html)

# 迭代器 Iterator

迭代器模式让我们能依次对序列中的每一项执行操作。迭代器负责遍历每一项的逻辑，并判断序列何时结束。

## for 与迭代器
```rust
fn main() {
    let v = vec![1, 2, 3];
    for x in v {
        println!("{}",x)
    }
}
```

上面的代码里，你可能把 `for` 当成简单循环，但它实际上是在遍历迭代器。

默认情况下，`for` 会对集合调用 `into_iter`，将其转换为迭代器。因此下面的代码与上面等价：
```rust
fn main() {
    let v = vec![1, 2, 3];
    for x in v.into_iter() {
        println!("{}",x)
    }
}
```


1. 🌟

```rust
/* 使用迭代器重构以下代码 */
fn main() {
    let arr = [0; 10];
    for i in 0..arr.len() {
        println!("{}",arr[i]);
    }
}
```

2. 🌟 创建迭代器最简单的方式之一是使用区间：`a..b`。
```rust
/* 填空 */
fn main() {
    let mut v = Vec::new();
    for n in __ {
       v.push(n);
    }

    assert_eq!(v.len(), 100);
}
```

## next 方法
所有迭代器都实现了标准库中定义的 `Iterator` trait：
```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // 省略了带默认实现的方法
}
```

我们可以直接在迭代器上调用 `next` 方法。


3. 🌟🌟

```rust
/* 填空并修复错误。尽可能使用两种方式 */
fn main() {
    let v1 = vec![1, 2];

    assert_eq!(v1.next(), __);
    assert_eq!(v1.next(), __);
    assert_eq!(v1.next(), __);
}
```

## into_iter、iter 和 iter_mut
上一节提到，`for` 会对集合调用 `into_iter` 将其转为迭代器。但这并不是唯一方式。

`into_iter`、`iter`、`iter_mut` 都能把集合变成迭代器，但方式不同：

- `into_iter` 会消耗集合，循环结束后集合不能再使用，因为所有权已在循环中转移。
- `iter` 在每次迭代中借用集合中的元素，循环后集合仍可重用。
- `iter_mut` 在每次迭代中可变借用集合中的元素，允许在原地修改集合。


4. 🌟

```rust
/* 让代码工作 */
fn main() {
    let arr = vec![0; 10];
    for i in arr {
        println!("{}", i);
    }

    println!("{:?}",arr);
}
```


5. 🌟

```rust
/* 填空 */
fn main() {
    let mut names = vec!["Bob", "Frank", "Ferris"];

    for name in names.__{
        *name = match name {
            &mut "Ferris" => "There is a rustacean among us!",
            _ => "Hello",
        }
    }

    println!("names: {:?}", names);
}
```


6. 🌟🌟

```rust
/* 填空 */
fn main() {
    let mut values = vec![1, 2, 3];
    let mut values_iter = values.__;

    if let Some(v) = values_iter.__{
        __
    }

    assert_eq!(values, vec![0, 2, 3]);
}
```


## 创建自定义迭代器
我们不仅可以从集合类型创建迭代器，还可以为自己的类型实现 `Iterator` trait。

**示例**
```rust
struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Counter {
        Counter { count: 0 }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < 5 {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

fn main() {
    let mut counter = Counter::new();

    assert_eq!(counter.next(), Some(1));
    assert_eq!(counter.next(), Some(2));
    assert_eq!(counter.next(), Some(3));
    assert_eq!(counter.next(), Some(4));
    assert_eq!(counter.next(), Some(5));
    assert_eq!(counter.next(), None);
}
```


7. 🌟🌟🌟

```rust
struct Fibonacci {
    curr: u32,
    next: u32,
}

// 为 `Fibonacci` 实现 `Iterator`。
// `Iterator` trait 只需定义 `next` 方法。
impl Iterator for Fibonacci {
    // 可以用 Self::Item 引用该类型
    type Item = u32;
    
    /* 实现 next 方法 */
    fn next(&mut self)
}

// 返回斐波那契序列生成器
fn fibonacci() -> Fibonacci {
    Fibonacci { curr: 0, next: 1 }
}

fn main() {
    let mut fib = fibonacci();
    assert_eq!(fib.next(), Some(1));
    assert_eq!(fib.next(), Some(1));
    assert_eq!(fib.next(), Some(2));
    assert_eq!(fib.next(), Some(3));
    assert_eq!(fib.next(), Some(5));
}
```

## 消耗迭代器的方法
`Iterator` trait 有许多由标准库提供默认实现的方法。

### 消耗型适配器
其中一些方法会调用 `next` 来用完迭代器，因此称为*消耗型适配器*。


8. 🌟🌟

```rust

/* 填空并修复错误 */
fn main() {
    let v1 = vec![1, 2, 3];

    let v1_iter = v1.iter();

    // sum 会取得迭代器的所有权，并通过反复调用 next 遍历元素
    let total = v1_iter.sum();

    assert_eq!(total, __);

    println!("{:?}, {:?}",v1, v1_iter);
}
```


#### collect
除了把集合变成迭代器，我们还可以用 `collect` 把结果收集成集合，`collect` 会消耗迭代器。


9. 🌟🌟

```rust
/* 让代码工作 */
use std::collections::HashMap;
fn main() {
    let names = [("sunface",18), ("sunfei",18)];
    let folks: HashMap<_, _> = names.into_iter().collect();

    println!("{:?}",folks);

    let v1: Vec<i32> = vec![1, 2, 3];

    let v2 = v1.iter().collect();

    assert_eq!(v2, vec![1, 2, 3]);
}
```


### 迭代器适配器
能把一个迭代器变成另一个迭代器的方法称为*迭代器适配器*。可以链式调用多个适配器，以可读的方式完成复杂操作。

但**所有迭代器都是惰性的**，必须调用某个消耗型适配器，才能从迭代器适配器的调用中得到结果。


10. 🌟🌟

```rust
/* 填空 */
fn main() {
    let v1: Vec<i32> = vec![1, 2, 3];

    let v2: Vec<_> = v1.iter().__.__;

    assert_eq!(v2, vec![2, 3, 4]);
}
```


11. 🌟🌟

```rust
/* 填空 */
use std::collections::HashMap;
fn main() {
    let names = ["sunface", "sunfei"];
    let ages = [18, 18];
    let folks: HashMap<_, _> = names.into_iter().__.collect();

    println!("{:?}",folks);
}
```


#### 在迭代器适配器中使用闭包


12. 🌟🌟 

```rust
/* 填空 */
#[derive(PartialEq, Debug)]
struct Shoe {
    size: u32,
    style: String,
}

fn shoes_in_size(shoes: Vec<Shoe>, shoe_size: u32) -> Vec<Shoe> {
    shoes.into_iter().__.collect()
}

fn main() {
    let shoes = vec![
        Shoe {
            size: 10,
            style: String::from("sneaker"),
        },
        Shoe {
            size: 13,
            style: String::from("sandal"),
        },
        Shoe {
            size: 10,
            style: String::from("boot"),
        },
    ];

    let in_my_size = shoes_in_size(shoes, 10);

    assert_eq!(
        in_my_size,
        vec![
            Shoe {
                size: 10,
                style: String::from("sneaker")
            },
            Shoe {
                size: 10,
                style: String::from("boot")
            },
        ]
    );
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/functional-programing/iterator.md)找到答案（在 solutions 路径下）
