+++
title = "01-参数使用借用类型"
date = 2026-08-18T22:10:00+08:00
weight = 5
type = "docs"
description = "参数使用借用类型 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/coercion-arguments.html](https://rust-unofficial.github.io/patterns/idioms/coercion-arguments.html)

# 参数使用借用类型

## 描述 {#description}

在决定函数参数使用何种类型时，以解引用强制转换（deref coercion）的目标类型作为参数，
可以提高代码的灵活性。这样，函数就能接受更多的输入类型。

这并不局限于可切片类型或胖指针类型。实际上，你应当始终优先使用**借用类型**，
而不是**借用所有权类型**。例如用 `&str` 而不是 `&String`，用 `&[T]` 而不是 `&Vec<T>`，
或用 `&T` 而不是 `&Box<T>`。

使用借用类型可以避免在所有权类型本身已提供一层间接的情况下再增加间接层。
例如，`String` 已有一层间接，因此 `&String` 会有两层间接。我们改用 `&str` 即可避免这一点，
并在调用函数时让 `&String` 强制转换为 `&str`。

## 示例 {#example}

在本例中，我们将说明以 `&String` 作为函数参数与以 `&str` 作为函数参数的一些差异，
但这些思路同样适用于用 `&Vec<T>` 对比 `&[T]`，或用 `&Box<T>` 对比 `&T`。

考虑这样一个例子：我们希望判断一个单词是否包含三个连续的元音。
判断此事并不需要拥有该字符串，因此我们将接受引用。

代码可能看起来像这样：

```rust
fn three_vowels(word: &String) -> bool {
    let mut vowel_count = 0;
    for c in word.chars() {
        match c {
            'a' | 'e' | 'i' | 'o' | 'u' => {
                vowel_count += 1;
                if vowel_count >= 3 {
                    return true;
                }
            }
            _ => vowel_count = 0,
        }
    }
    false
}

fn main() {
    let ferris = "Ferris".to_string();
    let curious = "Curious".to_string();
    println!("{}: {}", ferris, three_vowels(&ferris));
    println!("{}: {}", curious, three_vowels(&curious));

    // 这样没问题，但下面两行会失败：
    // println!("Ferris: {}", three_vowels("Ferris"));
    // println!("Curious: {}", three_vowels("Curious"));
}
```

这样能正常工作，因为我们传入的参数类型是 `&String`。如果去掉最后两行的注释，
这个例子就会失败。这是因为 `&str` 类型不会强制转换为 `&String` 类型。
只需修改参数类型即可修复。

例如，若将函数声明改为：

```rust, ignore
fn three_vowels(word: &str) -> bool {
```

那么两个版本都能编译，并打印相同的输出。

```bash
Ferris: false
Curious: true
```

但还没完！事情不止于此。你很可能会对自己说：这无所谓，反正我永远不会把 `&'static str`
当作输入（就像我们使用 `"Ferris"` 时那样）。即便抛开这个特殊例子，你仍会发现，
使用 `&str` 会比使用 `&String` 带来更多灵活性。

现在考虑这样一个例子：有人给了我们一个句子，我们想判断句中是否有任何单词包含三个连续的元音。
我们大概应该复用已经定义好的函数，只需把句子中的每个单词喂进去即可。

这样的例子可能如下：

```rust
fn three_vowels(word: &str) -> bool {
    let mut vowel_count = 0;
    for c in word.chars() {
        match c {
            'a' | 'e' | 'i' | 'o' | 'u' => {
                vowel_count += 1;
                if vowel_count >= 3 {
                    return true;
                }
            }
            _ => vowel_count = 0,
        }
    }
    false
}

fn main() {
    let sentence_string =
        "Once upon a time, there was a friendly curious crab named Ferris".to_string();
    for word in sentence_string.split(' ') {
        if three_vowels(word) {
            println!("{word} has three consecutive vowels!");
        }
    }
}
```

使用参数类型声明为 `&str` 的函数运行此例，将得到

```bash
curious has three consecutive vowels!
```

然而，当函数的参数类型声明为 `&String` 时，这个例子无法运行。这是因为字符串切片是 `&str`
而不是 `&String`，转换为 `&String` 需要分配，且这种转换不是隐式的；而从 `String` 转到 `&str`
则既廉价又隐式。

## 参见 {#see-also}

- [Rust 语言参考：类型强制转换](https://doc.rust-lang.org/reference/type-coercions.html)
- 关于如何处理 `String` 和 `&str` 的更多讨论，参见 Herman J. Radtke III 的
  [这篇系列博客（2015）](https://web.archive.org/web/20201112023149/https://hermanradtke.com/2015/05/03/string-vs-str-in-rust-functions.html)
- [Steve Klabnik 的博文：《何时应使用 String 还是 &str？》](https://archive.ph/LBpD0)
