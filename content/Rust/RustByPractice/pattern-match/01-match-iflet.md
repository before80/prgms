+++
title = "01-match, matches! 和 if let"
date = 2026-08-12T20:00:00+08:00
weight = 22
type = "docs"
description = "match, matches! 和 if let — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/pattern-match/match-iflet.html](https://practice-rust-zh.beatai.org/pattern-match/match-iflet.html)

# match, matches! 和 if let

### match
1. 🌟🌟
```rust
// 填空
enum Direction {
    East,
    West,
    North,
    South,
}

fn main() {
    let dire = Direction::South;
    match dire {
        Direction::East => println!("East"),
        // __  => { // 在这里匹配 South 或 North
        Direction::South | Direction::North => {
            // 在这里匹配 South 或 North
            println!("South or North");
        }
        // _ => println!(__),
        _ => println!("West"),
    };
}
```

2. 🌟🌟 `match` 是一个表达式，因此可以用在赋值语句中
```rust
fn main() {
    let boolean = true;

    // 使用 match 表达式填空，并满足以下条件
    //
    // boolean = true => binary = 1
    // boolean = false => binary = 0
    // let binary = __;
    let binary = match boolean {
        true => 1,
        false => 0,
    };

    assert_eq!(binary, 1);
}
```

3. 🌟🌟 使用 match 匹配出枚举成员持有的值
```rust
// 填空
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msgs = [
        Message::Quit,
        Message::Move{x:1, y:3},
        Message::ChangeColor(255,255,0)
    ];

    for msg in msgs {
        show_message(msg)
    }
}

fn show_message(msg: Message) {
    match msg {
        // __ => { // 这里匹配 Message::Move
        Message::Move {x:a, y:b} => { // 这里匹配 Message::Move
            assert_eq!(a, 1);
            assert_eq!(b, 3);
        },
        Message::ChangeColor(_, g, b) => {
            // assert_eq!(g, __);
            assert_eq!(g, 255);
            // assert_eq!(b, __);
            assert_eq!(b, 0);
        }
        // __ => println!("no data in these variants")
        _ => println!("no data in these variants")
    }
}
```

### matches!
[`matches!`](https://doc.rust-lang.org/stable/core/macro.matches.html) 看起来像 `match`, 但是它可以做一些特别的事情

4. 🌟🌟
```rust
fn main() {
    let alphabets = ['a', 'E', 'Z', '0', 'x', '9' , 'Y'];

    // 使用 `matches!` 填空
    for ab in alphabets {
        // assert!(__)
        assert!(matches!(ab, 'a'..='z' | 'A'..='Z' | '0'..='9'))
    }
}
```

5. 🌟🌟
```rust
enum MyEnum {
    Foo,
    Bar,
}

fn main() {
    let mut count = 0;

    let v = vec![MyEnum::Foo, MyEnum::Bar, MyEnum::Foo];
    for e in v {
        // if e == MyEnum::Foo { // 修复错误，只能修改本行代码
        if matches!(e, MyEnum::Foo) {
            count += 1;
        }
    }

    assert_eq!(count, 2);
}
```

### if let
在有些时候, 使用 `match` 匹配枚举有些太重了，此时 `if let` 就非常适合.

6. 🌟 
```rust

fn main() {
    let o = Some(7);

    // 移除整个 `match` 语句块，使用 `if let` 替代
    match o {
        Some(i) => {
            println!("This is a really long string and `{:?}`", i);
        }
        _ => {}
    };
}
```

7. 🌟🌟
```rust
// 填空
enum Foo {
    Bar(u8)
}

fn main() {
    let a = Foo::Bar(1);

    // __ {
    if let Foo::Bar(i) = a {
        println!("foobar 持有的值是: {}", i);
    }
}
```

8. 🌟🌟
```rust
enum Foo {
    Bar,
    Baz,
    Qux(u32)
}

fn main() {
    let a = Foo::Qux(10);

    // 移除以下代码，使用 `match` 代替
    // if let Foo::Bar = a {
    //     println!("match foo::bar")
    // } else if let Foo::Baz = a {
    //     println!("match foo::baz")
    // } else {
    //     println!("match others")
    // }
    match a {
        Foo::Baz => println!("match foo::bar"),
        Foo::Baz => println!("match foo::baz"),
        _ => println!("match others")
    }
}
```

### 变量遮蔽( Shadowing )
9. 🌟🌟
```rust

// 就地修复错误
fn main() {
    let age = Some(30);
    if let Some(age) = age { // 创建一个新的变量，该变量与之前的 `age` 变量同名
       assert_eq!(age, Some(30));
    } // 新的 `age` 变量在这里超出作用域
    
    match age {
        // `match` 也能实现变量遮蔽
        Some(age) =>  println!("age 是一个新的变量，它的值是 {}",age),
        _ => ()
    }
 }
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/pattern-match/match.md)找到答案(在 solutions 路径下) 
