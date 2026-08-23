+++
title = "6 impl 上的生命周期"
date = 2026-08-23T16:26:00+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_6.html](https://tfpk.github.io/lifetimekata/chapter_6.html)

当结构体或枚举带有生命周期时，`impl` 块
的工作方式也会略有变化。

例如，假设我们想创建一个让用户
遍历一句话的结构体。你可能会从类似这样的代码开始：

```rust
// 首先是结构体：

/// 这个结构体记录我们在字符串中读到哪里了。
struct WordIterator<'s> {
    position: usize,
    string: &'s str
}

impl WordIterator {
    /// 基于字符串创建新的 WordIterator。
    fn new(string: &str) -> WordIterator {
        WordIterator {
            position: 0,
            string
        }
    }
    
    /// 返回下一个单词。如果没有剩余单词则返回 `None`。
    fn next_word(&mut self) -> Option<&str> {
        let start_of_word = &self.string[self.position..];
        let index_of_next_space = start_of_word.find(' ').unwrap_or(start_of_word.len());
        if start_of_word.len() != 0 {
            self.position += index_of_next_space + 1;
            Some(&start_of_word[..index_of_next_space]) 
        } else {
            None
        }
    }
}

fn main() {
    let text = String::from("Twas brillig, and the slithy toves // Did gyre and gimble in the wabe: // All mimsy were the borogoves, // And the mome raths outgrabe. ");
    let mut word_iterator = WordIterator::new(&text);
    
    assert_eq!(word_iterator.next_word(), Some("Twas"));
    assert_eq!(word_iterator.next_word(), Some("brillig,"));
    
}
```

在定义 `WordIterator` 结构体时，我们说它需要指定一个生命周期。
但当我们编写 impl 块时，却没有指定。Rust 要求我们这样做。

做法是先告诉 Rust 有一个生命周期，然后把它放到
我们的结构体上。来看看怎么做：

```rust
impl<'lifetime> for WordIterator<'lifetime> {
    // ...
}
```

值得注意的是，我们分两步完成——`impl<'lifetime>` 定义了一个生命周期 `'lifetime`。
它不对该生命周期做任何承诺，只是说它存在。
`WordIterator<'lifetime>` 则使用我们创建的生命周期，并说「`WordIterator` 中的引用必须存活 `lifetime`」。

现在，在 impl 块中的任何地方，我们都可以选择使用该生命周期。任何标注了 `'lifetime` 的引用
都必须与任何其他标注了 `'lifetime` 的引用具有相同的生命周期。

```rust
# /// 这个结构体记录我们在字符串中读到哪里了。
# struct WordIterator<'s> {
#     position: usize,
#     string: &'s str
# }

impl<'lifetime> WordIterator<'lifetime> {
    /// 基于字符串创建新的 WordIterator。
    fn new(string: &'lifetime str) -> WordIterator<'lifetime> {
        WordIterator {
            position: 0,
            string
        }
    }
    
    /// 返回下一个单词。如果没有剩余单词则返回 `None`。
    fn next_word(&mut self) -> Option<&str> {
        let start_of_word = &self.string[self.position..];
        let index_of_next_space = start_of_word.find(' ').unwrap_or(start_of_word.len());
        if start_of_word.len() != 0 {
            self.position += index_of_next_space + 1;
            Some(&start_of_word[..index_of_next_space]) 
        } else {
            None
        }
    }
}

# fn main() {
#     let text = String::from("Twas brillig, and the slithy toves // Did gyre and gimble in the wabe: // All mimsy were the borogoves, // And the mome raths outgrabe. ");
#     let mut word_iterator = WordIterator::new(&text);
#     
#     assert_eq!(word_iterator.next_word(), Some("Twas"));
#     assert_eq!(word_iterator.next_word(), Some("brillig,"));
#     
# }

```

## 生命周期省略，再探

我们之前讨论过两条生命周期省略规则。它们是：

1. 每个省略输入生命周期（即被「省略」）的地方，都会填入它自己的生命周期。
2. 如果所有输入引用上恰好只有一个生命周期，该生命周期会赋给*每一个*输出生命周期。

既然我们已经见过带有生命周期的 `impl` 块，再讨论一条：

3. 如果有多个输入生命周期位置，但其中一个是 `&self` 或
   `&mut self`，则 `self` 借用的生命周期会赋给所有被省略的输出生命周期。
   
这意味着即使你的参数中接收了许多引用，Rust 也会假定你返回的任何引用
都来自 `self`，而不是那些其他引用。

# 练习

在下面的代码中，我们使用 `'borrow` 生命周期来标注函数，而不仅仅是 `'lifetime` 生命周期。
`'borrow` 生命周期只存在于这个函数内部，只影响其参数和返回值的
借用。如前所述，`'lifetime` 还会约束结构体内部字符串的生命周期。

我们有四种方式可以实现这段代码。描述每种实现的效果。

具体来说：
 - 它们能编译吗？
 - 有没有与另一种完全相同的？
 - 有没有生命周期不够通用的情况？
 - 哪一种写法「最」正确？

### 示例 1
```rust
    /// 返回下一个单词。如果没有剩余单词则返回 `None`。
#    /// 这能编译。与示例 4 完全相同。
#    /// 这个函数有问题，因为下一个单词的存活时间与
#    /// 你对迭代器的借用一样长。要获取下一个单词，你
#    /// 必须放弃对当前单词的所有引用。
    fn next_word<'borrow>(&'borrow mut self) -> Option<&'borrow str> {
        // ...
    }
```

### 示例 2
```rust
    /// 返回下一个单词。如果没有剩余单词则返回 `None`。
#    /// 这能编译。与示例 3 完全相同。
    fn next_word<'borrow>(&'borrow mut self) -> Option<&'lifetime str> {
        // ...
    }
```

### 示例 3
```rust
    /// 返回下一个单词。如果没有剩余单词则返回 `None`。
#    /// 这能编译。这可能是最正确的写法，因为它最短，
#    /// 同时也能确保你可以保留返回的字符串，即使你
#    /// 多次调用这个函数。
    fn next_word(&mut self) -> Option<&'lifetime str> {
        // ...
    }
```

### 示例 4
```rust
    /// 返回下一个单词。如果没有剩余单词则返回 `None`。
#    /// 这能编译。如果展开，会与示例 1 相同。
    fn next_word(&mut self) -> Option<&str> {
        // ...
    }
```
