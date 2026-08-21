+++
title = "06-枚举"
date = 2026-08-12T20:00:00+08:00
weight = 19
type = "docs"
description = "枚举 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/compound-types/enum.html](https://practice-rust-zh.beatai.org/compound-types/enum.html)

# 枚举
1. 🌟🌟 在创建枚举时，你可以使用显式的整数设定枚举成员的值。

```rust

// 修复错误
enum Number {
    Zero,
    One,
    Two,
}

enum Number1 {
    Zero = 0,
    One,
    Two,
}

// C语言风格的枚举定义
// enum Number2 {
//     Zero = 0.0,
//     One = 1.0,
//     Two = 2.0,
// }
enum Number2 {
    Zero = 0,
    One = 1,
    Two = 2,
}

fn main() {
    // 通过 `as` 可以将枚举值强转为整数类型
    // assert_eq!(Number::One, Number1::One);
    // assert_eq!(Number1::One, Number2::One);

    assert_eq!(Number::One as u8, Number1::One as u8);
    assert_eq!(Number1::One as u8, Number2::One as u8);
}
```

2. 🌟 枚举成员可以持有各种类型的值
```rust
// 填空
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    // let msg1 = Message::Move{__}; // 使用x = 1, y = 2 来初始化
    let _msg1 = Message::Move { x: 1, y: 2 }; // 使用x = 1, y = 2 来初始化
    // let msg2 = Message::Write(__); // 使用 "hello, world!" 来初始化
    let _msg2 = Message::Write("hello, world!".to_string()); // 使用 "hello, world!" 来初始化
}
```

3. 🌟🌟 枚举成员中的值可以使用模式匹配来获取
```rust
// 仅填空并修复错误
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::Move{x: 1, y: 2};

    // if let Message::Move{__} = msg {
    //     assert_eq!(a, b);
    // } else {
    //     panic!("不要让这行代码运行！");
    // }

    if let Message::Move{x: a, y: b} = msg {
        assert_eq!(a, b);
    } else {
        panic!("不要让这行代码运行！");
    }
}
```

4. 🌟🌟 使用枚举对类型进行同一化

```rust
// 填空，并修复错误
#[derive(Debug)]
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    // let msgs: __ = [
    //     Message::Quit,
    //     Message::Move{x:1, y:3},
    //     Message::ChangeColor(255,255,0)
    // ];
    let msgs: [Message; 3] = [
        Message::Quit,
        Message::Move{x:1, y:3},
        Message::ChangeColor(255,255,0)
    ];

    for msg in msgs {
        show_message(msg)
    }
}

fn show_message(msg: Message) {
    // println!("{}", msg);
    println!("{:?}", msg);
}
```

5. 🌟🌟 Rust 中没有 `null`，我们通过 `Option<T>` 枚举来处理值为空的情况
```rust
// 填空让 `println` 输出，同时添加一些代码不要让最后一行的 `panic` 执行到
fn main() {
    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);

    // if let __ = six {
    //     println!("{}", n)
    // }

    if let Some(n) = six {
        println!("{}", n);
        return
    }

    panic!("不要让这行代码运行！");
}

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        // __ => None,
        None => None,
        // __ => Some(i + 1),
        Some(i) => Some(i + 1),
    }
}
```


6. 🌟🌟🌟🌟 使用枚举来实现链表.

```rust

// 填空，让代码运行
use crate::List::*;

enum List {
    // Cons: 链表中包含有值的节点，节点是元组类型，第一个元素是节点的值，第二个元素是指向下一个节点的指针
    Cons(u32, Box<List>),
    // Nil: 链表中的最后一个节点，用于说明链表的结束
    Nil,
}

// 为枚举实现一些方法
impl List {
    // 创建空的链表
    fn new() -> List {
        // 因为没有节点，所以直接返回 Nil 节点
        // 枚举成员 Nil 的类型是 List
        Nil
    }

    // 在老的链表前面新增一个节点，并返回新的链表
    // fn prepend(self, elem: u32) -> __ {
    fn prepend(self, elem: u32) -> List {
        Cons(elem, Box::new(self))
    }

    // 返回链表的长度
    fn len(&self) -> u32 {
        match *self {
            // 这里我们不能拿走 tail 的所有权，因此需要获取它的引用
            // Cons(_, __ tail) => 1 + tail.len(),
            Cons(_, ref tail) => 1 + tail.len(),
            // 空链表的长度为 0
            Nil => 0
        }
    }

    // 返回链表的字符串表现形式，用于打印输出
    fn stringify(&self) -> String {
        match *self {
            Cons(head, ref tail) => {
                // 递归生成字符串
                // format!("{}, {}", head, tail.__())
                format!("{}, {}", head, tail.stringify())
            },
            Nil => {
                format!("Nil")
            },
        }
    }
}

fn main() {
    // 创建一个新的链表(也是空的)
    let mut list = List::new();

    // 添加一些元素
    list = list.prepend(1);
    list = list.prepend(2);
    list = list.prepend(3);

    // 打印列表的当前状态
    println!("链表的长度是: {}", list.len());
    println!("{}", list.stringify());
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/compound-types/enum.md)找到答案(在 solutions 路径下) 
