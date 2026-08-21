+++
title = "05-进一步深入特征"
date = 2026-08-12T20:00:00+08:00
weight = 30
type = "docs"
description = "进一步深入特征 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/generics-traits/advanced-traits.html](https://practice-rust-zh.beatai.org/generics-traits/advanced-traits.html)

# 进一步深入特征

## 关联类型
关联类型主要用于提升代码的可读性，例如以下代码 :
```rust
pub trait CacheableItem: Clone + Default + fmt::Debug + Decodable + Encodable {
  type Address: AsRef<[u8]> + Clone + fmt::Debug + Eq + Hash;
  fn is_null(&self) -> bool;
}
```

相比 `AsRef<[u8]> + Clone + fmt::Debug + Eq + Hash`， `Address` 的使用可以极大的减少其它类型在实现该特征时所需的模版代码.

1. 🌟🌟🌟
```rust

struct Container(i32, i32);

// 使用关联类型实现重新实现以下特征
// trait Contains {
//    type A;
//    type B;

trait Contains<A, B> {
    fn contains(&self, _: &A, _: &B) -> bool;
    fn first(&self) -> i32;
    fn last(&self) -> i32;
}

impl Contains<i32, i32> for Container {
    fn contains(&self, number_1: &i32, number_2: &i32) -> bool {
        (&self.0 == number_1) && (&self.1 == number_2)
    }
    // Grab the first number.
    fn first(&self) -> i32 { self.0 }

    // Grab the last number.
    fn last(&self) -> i32 { self.1 }
}

fn difference<A, B, C: Contains<A, B>>(container: &C) -> i32 {
    container.last() - container.first()
}

fn main() {
    let number_1 = 3;
    let number_2 = 10;

    let container = Container(number_1, number_2);

    println!("Does container contain {} and {}: {}",
        &number_1, &number_2,
        container.contains(&number_1, &number_2));
    println!("First number: {}", container.first());
    println!("Last number: {}", container.last());
    
    println!("The difference is: {}", difference(&container));
}
```

## 定义默认的泛型类型参数
当我们使用泛型类型参数时，可以为该泛型参数指定一个具体的默认类型，这样当实现该特征时，如果该默认类型可以使用，那用户再无需手动指定具体的类型。

2. 🌟🌟
```rust

use std::ops::Sub;

#[derive(Debug, PartialEq)]
struct Point<T> {
    x: T,
    y: T,
}

// 用三种方法填空: 其中两种使用默认的泛型参数，另外一种不使用
impl __ {
    type Output = Self;

    fn sub(self, other: Self) -> Self::Output {
        Point {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

fn main() {
    assert_eq!(Point { x: 2, y: 3 } - Point { x: 1, y: 0 },
        Point { x: 1, y: 3 });

    println!("Success!")
}
```

## 完全限定语法
在 Rust 中，两个不同特征的方法完全可以同名，且你可以为同一个类型同时实现这两个特征。这种情况下，就出现了一个问题：该如何调用这两个特征上定义的同名方法。为了解决这个问题，我们需要使用完全限定语法( Fully Qualified Syntax )。


#### 示例
```rust
trait UsernameWidget {
    fn get(&self) -> String;
}

trait AgeWidget {
    fn get(&self) -> u8;
}

struct Form {
    username: String,
    age: u8,
}

impl UsernameWidget for Form {
    fn get(&self) -> String {
        self.username.clone()
    }
}

impl AgeWidget for Form {
    fn get(&self) -> u8 {
        self.age
    }
}

fn main() {
    let form = Form{
        username: "rustacean".to_owned(),
        age: 28,
    };

    // 如果你反注释下面一行代码，将看到一个错误: Fully Qualified Syntax
    // 毕竟，这里有好几个同名的 `get` 方法
    // 
    // println!("{}", form.get());
    
    let username = UsernameWidget::get(&form);
    assert_eq!("rustacean".to_owned(), username);
    let age = AgeWidget::get(&form); // 你还可以使用以下语法 `<Form as AgeWidget>::get`
    assert_eq!(28, age);

    println!("Success!")
}
```

#### 练习题
3. 🌟🌟
```rust
trait Pilot {
    fn fly(&self) -> String;
}

trait Wizard {
    fn fly(&self) -> String;
}

struct Human;

impl Pilot for Human {
    fn fly(&self) -> String {
        String::from("This is your captain speaking.")
    }
}

impl Wizard for Human {
    fn fly(&self) -> String {
        String::from("Up!")
    }
}

impl Human {
    fn fly(&self) -> String {
        String::from("*waving arms furiously*")
    }
}

fn main() {
    let person = Human;

    assert_eq!(__, "This is your captain speaking.");
    assert_eq!(__, "Up!");

    assert_eq!(__, "*waving arms furiously*");

    println!("Success!")
}
```

## Supertraits
有些时候我们希望在特征上实现类似继承的特性，例如让一个特征 `A` 使用另一个特征 `B` 的功能。这种情况下，一个类型要实现特征 `A` 首先要实现特征 `B`， 特征 `B` 就被称为 `supertrait`

4. 🌟🌟🌟
```rust

trait Person {
    fn name(&self) -> String;
}

// Person 是 Student 的 supertrait .
// 实现 Student 需要同时实现 Person.
trait Student: Person {
    fn university(&self) -> String;
}

trait Programmer {
    fn fav_language(&self) -> String;
}

// CompSciStudent (computer science student) 是 Programmer 
// 和 Student 的 subtrait. 实现 CompSciStudent 需要先实现这两个 supertraits.
trait CompSciStudent: Programmer + Student {
    fn git_username(&self) -> String;
}

fn comp_sci_student_greeting(student: &dyn CompSciStudent) -> String {
    format!(
        "My name is {} and I attend {}. My favorite language is {}. My Git username is {}",
        student.name(),
        student.university(),
        student.fav_language(),
        student.git_username()
    )
}

struct CSStudent {
    name: String,
    university: String,
    fav_language: String,
    git_username: String
}

// 为 CSStudent 实现所需的特征
impl ...

fn main() {
    let student = CSStudent {
        name: "Sunfei".to_string(),
        university: "XXX".to_string(),
        fav_language: "Rust".to_string(),
        git_username: "sunface".to_string()
    };

    // 填空
    println!("{}", comp_sci_student_greeting(__));
}
```

## 孤儿原则
关于孤儿原则的详细介绍请参见[特征定义与实现的位置孤儿规则](https://course.rs/basic/trait/trait#特征定义与实现的位置孤儿规则) 和 [在外部类型上实现外部特征](https://course.rs/basic/trait/advance-trait.html#在外部类型上实现外部特征newtype)。


5. 🌟🌟
```rust
use std::fmt;

// 定义一个 newtype `Pretty`


impl fmt::Display for Pretty {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "\"{}\"", self.0.clone() + ", world")
    }
}

fn main() {
    let w = Pretty("hello".to_string());
    println!("w = {}", w);
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/generics-traits/advanced-trait.md)找到答案(在 solutions 路径下) 
