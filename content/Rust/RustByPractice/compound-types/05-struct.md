+++
title = "05-结构体"
date = 2026-08-12T20:00:00+08:00
weight = 18
type = "docs"
description = "结构体 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/compound-types/struct.html](https://practice-rust-zh.beatai.org/compound-types/struct.html)

# 结构体

### 三种类型的结构体
1. 🌟 对于结构体，我们必须为其中的每一个字段都指定具体的值
```rust

// fix the error
struct Person {
    name: String,
    age: u8,
    hobby: String
}
fn main() {
    let age = 30;
    // let p = Person {
    //     name: String::from("sunface"),
    //     age,
    // };
    let _p = Person {
        name: String::from("sunface"),
        age,
        hobby: String::new()
    };
} 
```


2. 🌟 单元结构体没有任何字段。
```rust

struct Unit;
trait SomeTrait {
    // ...定义一些行为
}

// 我们并不关心结构体中有什么数据( 字段 )，但我们关心它的行为。
// 因此这里我们使用没有任何字段的单元结构体，然后为它实现一些行为
impl SomeTrait for Unit {  }
fn main() {
    let u = Unit;
    do_something_with_unit(u);
} 

// 填空，让代码工作
// fn do_something_with_unit(u: __) {   }
fn do_something_with_unit(u: Unit) {   }
```

3. 🌟🌟🌟 元组结构体看起来跟元组很像，但是它拥有一个结构体的名称，该名称可以赋予它一定的意义。由于它并不关心内部数据到底是什么名称，因此此时元组结构体就非常适合。

```rust

// 填空并修复错误
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);
fn main() {
    // let v = Point(__, __, __);
    let v = Point(0, 127, 255);
    check_color(v);
}

// fn check_color(p: Color) {
fn check_color(p: Point) {
    // let (x, _, _) = p;
    let Point(x, _, _) = p;
    assert_eq!(x, 0);
    assert_eq!(p.1, 127);
    assert_eq!(p.2, 255);
}
```

### 结构体上的一些操作
4. 🌟 你可以在实例化一个结构体时将它整体标记为可变的，但是 Rust 不允许我们将结构体的某个字段专门指定为可变的.

```rust

// 填空并修复错误，不要增加或移除代码行
struct Person {
    name: String,
    age: u8,
}
fn main() {
    let age = 18;
    // let p = Person {
    //     name: String::from("sunface"),
    //     age,
    // };
    let mut p = Person {
        name: String::from("sunface"),
        age,
    };

    // how can you believe sunface is only 18?
    p.age = 30;

    // 填空
    // __ = String::from("sunfei");
    p.name = String::from("sunfei");
}
```

5. 🌟 使用结构体字段初始化缩略语法可以减少一些重复代码
```rust
// 填空
struct Person {
    name: String,
    age: u8,
}
fn main() {}

fn build_person(name: String, age: u8) -> Person {
    Person {
        age,
        // __
        name
    }
}
```

6. 🌟 你可以使用结构体更新语法基于一个结构体实例来构造另一个
```rust
// 填空，让代码工作
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

fn main() {
    let u1 = User {
        email: String::from("someone@example.com"),
        username: String::from("sunface"),
        active: true,
        sign_in_count: 1,
    };

    let u2 = set_email(u1);
}

fn set_email(u: User) -> User {
    User {
        email: String::from("contact@im.dev"),
        // __
        ..u
    }
}
```

### 打印结构体
7. 🌟🌟 我们可以使用 `#[derive(Debug)]` 让[结构体变成可打印的](https://course.rs/basic/compound-type/struct.html#使用-derivedebug-来打印结构体的信息).

```rust
// 填空，让代码工作
// #[]
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let scale = 2;
    let rect1 = Rectangle {
        width: dbg!(30 * scale), // 打印 debug 信息到标准错误输出 stderr,并将 `30 * scale` 的值赋给 `width`
        height: 50,
    };

    dbg!(&rect1); // 打印 debug 信息到标准错误输出 stderr

    // println!(__, rect1); // 打印 debug 信息到标准输出 stdout
    println!("{:?}", rect1);
}
```

### 结构体的所有权
当解构一个变量时，可以同时使用 `move` 和引用模式绑定的方式。当这么做时，部分 `move` 就会发生：变量中一部分的所有权被转移给其它变量，而另一部分我们获取了它的引用。

在这种情况下，原变量将无法再被使用，但是它没有转移所有权的那一部分依然可以使用，也就是之前被引用的那部分。

#### 示例
```rust

fn main() {
    #[derive(Debug)]
    struct Person {
        name: String,
        age: Box<u8>,
    }

    let person = Person {
        name: String::from("Alice"),
        age: Box::new(20),
    };

    // 通过这种解构式模式匹配，person.name 的所有权被转移给新的变量 `name`
    // 但是，这里 `age` 变量却是对 person.age 的引用, 这里 ref 的使用相当于: let age = &person.age 
    let Person { name, ref age } = person;

    println!("The person's age is {}", age);

    println!("The person's name is {}", name);

    // Error! 原因是 person 的一部分已经被转移了所有权，因此我们无法再使用它
    //println!("The person struct is {:?}", person);

    // 虽然 `person` 作为一个整体无法再被使用，但是 `person.age` 依然可以使用
    println!("The person's age from person struct is {}", person.age);
}
```

#### 练习

8. 🌟🌟
```rust
// 修复错误
#[derive(Debug)]
struct File {
    name: String,
    data: String,
}
fn main() {
    let f = File {
        name: String::from("readme.md"),
        data: "Rust By Practice".to_string()
    };

    let _name = f.name;

    // 只能修改这一行
    // println!("{}, {}, {:?}",f.name, f.data, f);
    println!("{}", f.data);
} 
```


> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/compound-types/struct.md)找到答案(在 solutions 路径下) 
