+++
title = "02-解释器"
date = 2026-08-18T22:10:00+08:00
weight = 26
type = "docs"
description = "解释器 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/behavioural/interpreter.html](https://rust-unofficial.github.io/patterns/patterns/behavioural/interpreter.html)

# 解释器

## 描述 {#description}

如果某个问题经常出现，并且解决它需要冗长而重复的步骤，那么可以把问题实例表达为一种简单语言，再由解释器对象通过解释用该简单语言写成的句子来求解。

基本上，对任何一类问题，我们都会定义：

- 一种
  [领域特定语言](https://en.wikipedia.org/wiki/Domain-specific_language)，
- 该语言的文法，
- 一个用于求解问题实例的解释器。

## 动机 {#motivation}

我们的目标是把简单数学表达式翻译成后缀表达式（或
[逆波兰表示法](https://en.wikipedia.org/wiki/Reverse_Polish_notation)）。
为简单起见，表达式由十个数字 `0`, ..., `9` 和两种运算 `+`、`-` 组成。例如，表达式 `2 + 4` 被翻译成
`2 4 +`。

## 本问题的上下文无关文法 {#context-free-grammar-for-our-problem}

我们的任务是把中缀表达式翻译成后缀表达式。下面为 `0`, ..., `9`、`+` 和
`-` 上的中缀表达式集合定义上下文无关文法，其中：

- 终结符：`0`, `...`, `9`, `+`, `-`
- 非终结符：`exp`, `term`
- 开始符号是 `exp`
- 产生式规则如下

```ignore
exp -> exp + term
exp -> exp - term
exp -> term
term -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

**注意：** 根据后续用途，该文法还需要进一步变换。例如，我们可能需要消除左递归。更多细节请参见
[《编译原理：原理、技术与工具》](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
（又称龙书）。

## 解决方案 {#solution}

我们直接实现一个递归下降解析器。为简单起见，当表达式在句法上不正确时代码会 panic（例如按文法定义，`2-34` 或 `2+5-` 都是错误的）。

```rust
pub struct Interpreter<'a> {
    it: std::str::Chars<'a>,
}

impl<'a> Interpreter<'a> {
    pub fn new(infix: &'a str) -> Self {
        Self { it: infix.chars() }
    }

    fn next_char(&mut self) -> Option<char> {
        self.it.next()
    }

    pub fn interpret(&mut self, out: &mut String) {
        self.term(out);

        while let Some(op) = self.next_char() {
            if op == '+' || op == '-' {
                self.term(out);
                out.push(op);
            } else {
                panic!("Unexpected symbol '{op}'");
            }
        }
    }

    fn term(&mut self, out: &mut String) {
        match self.next_char() {
            Some(ch) if ch.is_digit(10) => out.push(ch),
            Some(ch) => panic!("Unexpected symbol '{ch}'"),
            None => panic!("Unexpected end of string"),
        }
    }
}

pub fn main() {
    let mut intr = Interpreter::new("2+3");
    let mut postfix = String::new();
    intr.interpret(&mut postfix);
    assert_eq!(postfix, "23+");

    intr = Interpreter::new("1-2+3-4");
    postfix.clear();
    intr.interpret(&mut postfix);
    assert_eq!(postfix, "12-3+4-");
}
```

## 讨论 {#discussion}

人们可能误以为解释器设计模式就是为形式语言设计文法并实现解析器。实际上，该模式关注的是以更具体的方式表达问题实例，并实现求解这些实例的函数/类/struct。Rust 语言有 `macro_rules!`，允许我们定义特殊语法以及如何把该语法展开为源代码的规则。

在下面的例子中，我们创建了一个简单的 `macro_rules!`，用于计算 `n`
维向量的[欧几里得长度](https://en.wikipedia.org/wiki/Euclidean_distance)。写 `norm!(x,1,2)` 可能比把 `x,1,2` 装进 `Vec` 再调用计算长度的函数更易于表达，也更高效。

```rust
macro_rules! norm {
    ($($element:expr),*) => {
        {
            let mut n = 0.0;
            $(
                n += ($element as f64)*($element as f64);
            )*
            n.sqrt()
        }
    };
}

fn main() {
    let x = -3f64;
    let y = 4f64;

    assert_eq!(3f64, norm!(x));
    assert_eq!(5f64, norm!(x, y));
    assert_eq!(0f64, norm!(0, 0, 0));
    assert_eq!(1f64, norm!(0.5, -0.5, 0.5, -0.5));
}
```

## 参见 {#see-also}

- [解释器模式](https://en.wikipedia.org/wiki/Interpreter_pattern)
- [上下文无关文法](https://en.wikipedia.org/wiki/Context-free_grammar)
- [macro_rules!](https://doc.rust-lang.org/rust-by-example/macros.html)
