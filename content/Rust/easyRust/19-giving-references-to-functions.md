+++
title = "19-向函数传递引用"
date = 2026-08-21T12:46:00+08:00
weight = 20
type = "docs"
description = "向函数传递引用 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_18.html](https://dhghomon.github.io/easy_rust/Chapter_18.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 向函数传递引用

引用对函数非常有用。Rust中关于值的规则是:一个值只能有一个所有者。

这段代码将无法工作:

```rust
fn print_country(country_name: String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Austria");
    print_country(country); // 我们打印 "Austria"
    print_country(country); // ⚠️ 挺好玩，再来一次！
}
```

它不能工作，因为`country`被破坏了。下面是如何操作的。

- 第一步，我们创建`String`，称为`country`。`country`是所有者。
- 第二步:我们把`country`给`print_country`。`print_country`没有`->`，所以它不返回任何东西。`print_country`完成后，我们的`String`现在已经死了。
- 第三步:我们尝试把`country`给`print_country`，但我们已经这样做了。我们已经没有`country`可以给了。

我们可以让`print_country`给`String`回来，但是有点尴尬。

```rust
fn print_country(country_name: String) -> String {
    println!("{}", country_name);
    country_name // 在这里返回它
}

fn main() {
    let country = String::from("Austria");
    let country = print_country(country); // 现在必须用 let 把 String 接回来
    print_country(country);
}
```

现在打印出来了。

```text
Austria
Austria
```

更好的解决方法是增加`&`。

```rust
fn print_country(country_name: &String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Austria");
    print_country(&country); // 我们打印 "Austria"
    print_country(&country); // 挺好玩，再来一次！
}
```

现在 `print_country()` 是一个函数，它接受 `String` 的引用: `&String`。另外，我们给country一个引用，写作`&country`。这表示 "你可以看它，但我要保留它"。

现在让我们用一个可变引用来做类似的事情。下面是一个使用可变变量的函数的例子:

```rust
fn add_hungary(country_name: &mut String) { // 首先说明函数接受可变引用
    country_name.push_str("-Hungary"); // push_str() 向 String 追加 &str
    println!("Now it says: {}", country_name);
}

fn main() {
    let mut country = String::from("Austria");
    add_hungary(&mut country); // 我们也需要传入可变引用。
}
```

此打印`Now it says: Austria-Hungary`。

所以得出结论:

- `fn function_name(variable: String)`接收了`String`，并拥有它。如果它不返回任何东西，那么这个变量就会在函数里面死亡。
- `fn function_name(variable: &String)` 借用 `String` 并可以查看它
- `fn function_name(variable: &mut String)`借用`String`，可以更改。

下面是一个看起来像可变引用的例子，但它是不同的。

```rust
fn main() {
    let country = String::from("Austria"); // country 不可变，但我们要打印 Austria-Hungary。怎么做到？
    adds_hungary(country);
}

fn adds_hungary(mut country: String) { // 做法是：adds_hungary 接收 String 并声明为可变！
    country.push_str("-Hungary");
    println!("{}", country);
}
```

这怎么可能呢？因为`mut country`不是引用。`adds_hungary`现在拥有`country`。(记住，它占用的是`String`而不是`&String`)。当你调用`adds_hungary`的那一刻，它就完全成了country的主人。`country`与`String::from("Austria")`没有关系了。所以，`adds_hungary`可以把`country`当作可变的，这样做是完全安全的。

还记得我们上面的员工Powerpoint和经理的情况吗？在这种情况下，就好比员工只是把自己的整台电脑交给了经理。员工不会再碰它，所以经理可以对它做任何他想做的事情。
