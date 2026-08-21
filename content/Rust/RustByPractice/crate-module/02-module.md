+++
title = "02-模块 Module"
date = 2026-08-12T20:00:00+08:00
weight = 44
type = "docs"
description = "模块 Module — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/crate-module/module.html](https://practice-rust-zh.beatai.org/crate-module/module.html)

# 模块 Module
在 Rust 语言圣经中，我们已经深入讲解过[模块module](https://course.rs/basic/crate-module/module.html)，这里就不再赘述，直接开始我们的练习。

之前我们创建了一个 package `hello-package`，它的目录结构在经过多次修改后，变成了以下模样:

```shell
.
├── Cargo.toml
├── src
│   ├── lib.rs
│   └── main.rs
```

下面，我们来为其中的库包创建一些模块，然后在二进制包中使用这些模块。

1. 🌟🌟 根据以下的模块树描述实现模块 `front_of_house` :
```shell
库包的根(src/lib.rs)
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         ├── take_payment
         └── complain
```

```rust
// 填空
// in __.rs

mod front_of_house {
    // 实现此模块
}
```


2. 🌟🌟 让我们在库包的根中定义一个函数 `eat_at_restaurant`, 然后在该函数中调用之前创建的函数 `eat_at_restaurant`

```rust
// in lib.rs

// 填空并修复错误

// 提示：你需要通过 `pub` 将一些项标记为公有的，这样模块 `front_of_house` 中的项才能被模块外的项访问
mod front_of_house {
    /* ...snip... */
}

pub fn eat_at_restaurant() {
    // 使用绝对路径调用
    __.add_to_waitlist();

    // 使用相对路径调用
     __.add_to_waitlist();
}
```

3. 🌟🌟 我们还可以使用 `super` 来导入父模块中的项
```rust
// in lib.rs

mod back_of_house {
    fn fix_incorrect_order() {
        cook_order();
        // 使用三种方式填空
        //1. 使用关键字 `super`
        //2. 使用绝对路径
        __.serve_order();
    }

    fn cook_order() {}
}
```


### 将模块分离并放入独立的文件中
```rust
// in lib.rs
pub mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}

        pub fn seat_at_table() -> String {
            String::from("sit down please")
        }
    }

    pub mod serving {
        pub fn take_order() {}

        pub fn serve_order() {}

        pub fn take_payment() {}

        // 我猜你不希望顾客听到你在抱怨他们，因此让这个函数私有化吧
        fn complain() {} 
    }
}

pub fn eat_at_restaurant() -> String {
    front_of_house::hosting::add_to_waitlist();
    
    back_of_house::cook_order();

    String::from("yummy yummy!")
}

pub mod back_of_house {
    pub fn fix_incorrect_order() {
        cook_order();
        crate::front_of_house::serving::serve_order();
    }

    pub fn cook_order() {}
}
```

4. 🌟🌟🌟🌟 请将上面的模块和代码分离到以下目录文件中e :
```shell
.
├── Cargo.toml
├── src
│   ├── back_of_house.rs
│   ├── front_of_house
│   │   ├── hosting.rs
│   │   ├── mod.rs
│   │   └── serving.rs
│   ├── lib.rs
│   └── main.rs
```

```rust
// in src/lib.rs

// 待实现...
```

```rust
// in src/back_of_house.rs

// 待实现...
```


```rust
// in src/front_of_house/mod.rs

// 待实现...
```

```rust
// in src/front_of_house/hosting.rs

// 待实现...
```

```rust
// in src/front_of_house/serving.rs

// 待实现...
```

### 从二进制包中访问库包的代码
**请确保你已经完成了第四题，然后再继续进行.**

当到底此处时，你的项目结构应该如下所示: 
```shell
.
├── Cargo.toml
├── src
│   ├── back_of_house.rs
│   ├── front_of_house
│   │   ├── hosting.rs
│   │   ├── mod.rs
│   │   └── serving.rs
│   ├── lib.rs
│   └── main.rs
```

5. 🌟🌟🌟现在我们可以从二进制包中发起函数调用了.

```rust
// in src/main.rs

// 填空并修复错误
fn main() {
    assert_eq!(__, "sit down please");
    assert_eq!(__,"yummy yummy!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/crate-module/module.md)找到答案(在 solutions 路径下) 
