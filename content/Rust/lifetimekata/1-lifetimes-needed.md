+++
title = "1 为何需要生命周期"
date = 2026-08-23T16:26:00+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_1.html](https://tfpk.github.io/lifetimekata/chapter_1.html)

上一节我们讨论了单个函数内部的生命周期概念。在那些例子中，根据花括号就能清楚看出变量或引用的代码区域。生命周期标注用于帮助编译器理解那些无法仅靠作用域括号推断的情况（例如跨函数边界，以及在结构体和枚举内部）。

理解生命周期标注的好起点，是先明白我们为什么真的需要它们。让我们通过一些例子来理解它们存在的原因：

需要显式标注生命周期的最简单函数例子，是返回两个整数中较大者引用的函数：

```rust
fn max_of_refs(a: &i32, b: &i32) -> &i32 {
    if *a > *b {
        a
    } else {
        b
    }
}
```

假设我们这样调用它：

```rust
fn complex_function(a: &i32) -> &i32 {
    let b = 2;
    max_of_refs(a, &b)
}

fn main() {
    let a = 1;
    let my_num = complex_function(&a);
    println!("{my_num}");
}
```

若你仔细推演这个例子，会发现 `my_num` 会是指向 `complex_function` 中某个变量（已不再存在）的引用。换句话说，`complex_function` 返回值的存活时间会长于 `b` 的存活时间。

你可能会说：「但编译器在运行时难道看不出这个程序显然不行吗？」嗯，因为我们用的是常量，编译器大概确实能判断这个程序不行。

但若是 `let a = rand::rand()` 或 `let b = read_number_from_stdin()` 呢？编译器不可能判断这个引用是否应该有效。

## 好吧，为什么不能直接禁止这种情况？

你接下来可能会想：「好吧，这类引用肯定都不安全；干脆禁止它们。」值得具体说明这种禁止是什么。最简单的禁止是「函数参数中不允许有引用」，但这可能有点过激（而且会彻底毁掉 Rust 的实用性）。

更合理的禁止——能覆盖这种情况——是：「任何有多个引用输入的函数，不得返回引用（或包含引用的类型）」。这避免了我们看到的那种「引用究竟来自哪里」不明确的问题，也会禁止上面的例子。

但这样好用吗？若你想要这样的函数呢：

```rust
fn only_if_greater(number: &i32, greater_than: &i32) -> Option<&i32> {
    if number > greater_than {
        Some(number)
    } else {
        None
    }
}
```

无论你如何调用这个函数，只要返回值是 `Some`，我们*始终*知道它指向 `number`，绝不会返回指向 `greater_than` 的引用。

更有趣的例子是 `split` 函数：接收一个字符串，按某个分隔符切分，返回该字符串各片段切片的向量。

```rust
fn split(text: &str, delimiter: &str) -> Vec<&str> {
    let mut last_split = 0;
    let mut matches: Vec<&str> = vec![];
    for i in 0..text.len() {
        if i < last_split {
            continue
        }
        if text[i..].starts_with(delimiter) {
            matches.push(&text[last_split..i]);
            last_split = i + delimiter.len(); 
        }
    }
    if last_split < text.len() {
        matches.push(&text[last_split..]);
    }
    
    matches
}
```

无论你如何调用这个函数，它返回的向量中的切片始终来自 `text`，绝不会来自 `delimiter`。

## 唉，编译器就不能自己推断吗？

此时你大概已经注意到，`matches.push` 只会被传入 `text` 的切片。因此你合理地期望编译器在这种情况下能自动推断生命周期。

在简单情况下或许可以。但你的编译器可能判定无法推断，或者推断成功……但要花六个月。

因此编译器需要更多信息。这些信息由生命周期标注提供。在详细讨论之前，这里有一个练习，希望能在我们处理语法之前巩固这些概念。

## 练习：判断哪些程序能工作，哪些会出错

在不使用任何生命周期语法的情况下，针对每个代码示例回答以下问题：

1. 哪些输入是引用？函数可能返回什么？
2. 哪些例子可能出现悬垂引用？

注意：这些代码示例无法通过编译；你需要阅读并思考。

确定答案后，点击代码块右上角的「眼睛」按钮可查看参考答案。

```rust

# // a 是唯一的输入引用。
# // 函数只能返回 a
fn identity(a: &i32) -> &i32 {
    a
}

# // 这里不会出现悬垂引用。
fn example_1() {
    let x = 4;
    let x_ref = identity(&x);
    assert_eq!(*x_ref, 4);
}

# // 这始终会导致悬垂引用。
fn example_2() {
    let mut x_ref: Option<&i32> = None;
    {
        let x = 7;
        x_ref = Some(identity(&x));
    }
    assert_eq!(*x_ref.unwrap(), 7);
}
```

```rust
# // `opt` 和 `otherwise` 的内容都是引用
# // 两者都可能被返回。
fn option_or(opt: Option<&i32>, otherwise: &i32) -> &i32 {
    opt.unwrap_or(otherwise)
}

# // 这里不可能出现悬垂引用。
fn example_1() {
    let x = 8;
    let y = 10;
    let my_number = Some(&x);
    assert_eq!(&x, option_or(my_number, &y));
}

# // 这始终是悬垂引用。
fn example_2() {
    let answer = {
        let y = 4;
        option_or(None, &y)
    };
    assert_eq!(answer, &4);
}

# // 这绝不会是悬垂引用。
fn example_3() {
    let y = 4;
    let answer = {
        option_or(None, &y)
    };
    assert_eq!(answer, &4);
}

# // 这始终是悬垂引用。
fn example_4() {
    let y = 4;
    let answer = {
        let x = 7;
        option_or(Some(&x), &y)
    };
    assert_eq!(answer, &7);
}
```
