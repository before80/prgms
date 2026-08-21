+++
title = "29-解构"
date = 2026-08-21T12:46:00+08:00
weight = 30
type = "docs"
description = "解构 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_28.html](https://dhghomon.github.io/easy_rust/Chapter_28.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 解构

我们再来看一些解构。你可以通过使用`let`倒过来从一个结构体或枚举中获取值。我们了解到这是`destructuring`，因为你得到的变量不是结构体的一部分。现在你分别得到了它们的值。首先是一个简单的例子。

```rust
struct Person { // 为人物做一个简单结构体
    name: String,
    real_name: String,
    height: u8,
    happiness: bool
}

fn main() {
    let papa_doc = Person { // 创建变量 papa_doc
        name: "Papa Doc".to_string(),
        real_name: "Clarence".to_string(),
        height: 170,
        happiness: false
    };

    let Person { // 解构 papa_doc
        name: a,
        real_name: b,
        height: c,
        happiness: d
    } = papa_doc;

    println!("They call him {} but his real name is {}. He is {} cm tall and is he happy? {}", a, b, c, d);
}
```

这个打印:`They call him Papa Doc but his real name is Clarence. He is 170 cm tall and is he happy? false`

你可以看到，这是倒过来的。首先我们说`let papa_doc = Person { fields }`来创建结构。然后我们说 `let Person { fields } = papa_doc` 来解构它。

你不必写`name: a`--你可以直接写`name`。但这里我们写 `name: a` 是因为我们想使用一个名字为 `a` 的变量。

现在再举一个更大的例子。在这个例子中，我们有一个 `City` 结构。我们给它一个`new`函数来创建它。然后我们有一个 `process_city_values` 函数来处理这些值。在函数中，我们只是创建了一个 `Vec`，但你可以想象，我们可以在解构它之后做更多的事情。

```rust
struct City {
    name: String,
    name_before: String,
    population: u32,
    date_founded: u32,
}

impl City {
    fn new(name: String, name_before: String, population: u32, date_founded: u32) -> Self {
        Self {
            name,
            name_before,
            population,
            date_founded,
        }
    }
}

fn process_city_values(city: &City) {
    let City {
        name,
        name_before,
        population,
        date_founded,
    } = city;
        // 现在可以分别使用这些值了
    let two_names = vec![name, name_before];
    println!("The city's two names are {:?}", two_names);
}

fn main() {
    let tallinn = City::new("Tallinn".to_string(), "Reval".to_string(), 426_538, 1219);
    process_city_values(&tallinn);
}
```

这将打印出`The city's two names are ["Tallinn", "Reval"]`。
