+++
title = "9 延伸阅读"
date = 2026-08-23T16:26:00+08:00
weight = 11
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_9.html](https://tfpk.github.io/lifetimekata/chapter_9.html)

关于生命周期，最好的信息来源是 Rust 参考（Rust Reference）和
Rustonomicon。如果你要完成某个项目，确实需要非常深入的生命周期知识，
参考文档里会有这些内容。不过大多数时候，
当你觉得自己需要理解某种复杂的生命周期细节时，
你可能会发现其实存在更简单的替代方案。

 - [Rust 参考（生命周期省略）](https://doc.rust-lang.org/reference/lifetime-elision.html)
 - [Rust 参考（总览）](https://doc.rust-lang.org/reference/)
 - [Rustonomicon（生命周期）](https://doc.rust-lang.org/nomicon/lifetimes.html)

# 其他有用的生命周期资料

- [常见的 Rust 生命周期误解](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md)
- [Crust of Rust：生命周期标注](https://www.youtube.com/watch?v=rAl-9HwD858)

## 型变与子类型

本指南完全没有涉及「型变」（variance）这一主题，它描述的是生命周期之间如何相互替换。
型变在理论上很重要，但对日常理解生命周期帮助不大，因此没有纳入本书。

你可以在 [Rustonomicon（子类型）](https://doc.rust-lang.org/nomicon/subtyping.html) 中阅读更多内容。

## 脑筋急转弯 1：为什么这个程序不能工作：

如果你对通过一道非常难的练习来检验自己对生命周期和泛型的理解感兴趣，
下面的练习可能会很有意思。

它本应是练习 5 中代码的另一种实现方式。
不幸的是，它并不能工作。本书作者在写完五章之后，
花了 20 分钟才想明白（所以他也
向你发起挑战，看你能不能做得更好！）

```rust
use std::collections::HashSet;

struct Difference<'first, 'second> {
    first_only: Vec<&'first str>,
    second_only: Vec<&'second str>
}

fn find_difference<'fst, 'snd>(sentence1: &'fst str, sentence2: &'snd str) -> Difference<'fst, 'snd> {
    let sentence_1_words: HashSet<&str> = sentence1.split(" ").collect();
    let sentence_2_words: HashSet<&str> = sentence2.split(" ").collect();

    Difference {
        first_only: (&sentence_1_words - &sentence_2_words).into_iter().collect(),
        second_only: (&sentence_2_words - &sentence_1_words).into_iter().collect(),
    }

}

fn main() {
    let first_sentence = String::from("I love the surf and the sand.");
    let second_sentence = String::from("I hate the surf and the sand.");

    let first_only = {
        let third_sentence = String::from("I hate the snow and the sand.");
        let diff = find_difference(&first_sentence, &third_sentence);
        diff.first_only
    };

    assert_eq!(first_only, vec!["hate", "surf"]);

    let second_only = {
        let third_sentence = String::from("I hate the snow and the sand.");
        let diff = find_difference(&third_sentence, &second_sentence);
        diff.second_only
    };

    assert_eq!(second_only, vec!["snow"]);
}
```

关于这个问题的更多信息，请阅读 [这个 Rust issue](https://github.com/rust-lang/rust/issues/73788)。
