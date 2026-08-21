+++
title = "27-循环"
date = 2026-08-21T12:46:00+08:00
weight = 28
type = "docs"
description = "循环 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_26.html](https://dhghomon.github.io/easy_rust/Chapter_26.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 循环

有了循环，你可以告诉 Rust 继续某事，直到你想让它停止。您使用 `loop` 来启动一个不会停止的循环，除非您告诉它何时`break`。

```rust
fn main() { // 这个程序永远不会停止
    loop {

    }
}
```

所以，我们要告诉编译器什么时候能停止:

```rust
fn main() {
    let mut counter = 0; // 将计数器设为 0
    loop {
        counter +=1; // 计数器加 1
        println!("The counter is now: {}", counter);
        if counter == 5 { // 当 counter == 5 时停止
            break;
        }
    }
}
```

这将打印:

```text
The counter is now: 1
The counter is now: 2
The counter is now: 3
The counter is now: 4
The counter is now: 5
```

如果你在一个循环里面有一个循环，你可以给它们命名。有了名字，你可以告诉 Rust 要从哪个循环中 `break` 出来。使用 `'` (称为 "tick") 和 `:` 来给它命名。

```rust
fn main() {
    let mut counter = 0;
    let mut counter2 = 0;
    println!("Now entering the first loop.");

    'first_loop: loop {
        // 给第一个循环起名
        counter += 1;
        println!("The counter is now: {}", counter);
        if counter > 9 {
            // 在这个循环内启动第二个循环
            println!("Now entering the second loop.");

            'second_loop: loop {
                // 现在进入了 'second_loop
                println!("The second counter is now: {}", counter2);
                counter2 += 1;
                if counter2 == 3 {
                    break 'first_loop; // 跳出 'first_loop，从而结束程序
                }
            }
        }
    }
}
```

这将打印:

```text
Now entering the first loop.
The counter is now: 1
The counter is now: 2
The counter is now: 3
The counter is now: 4
The counter is now: 5
The counter is now: 6
The counter is now: 7
The counter is now: 8
The counter is now: 9
The counter is now: 10
Now entering the second loop.
The second counter is now: 0
The second counter is now: 1
The second counter is now: 2
```

`while`循环是指在某件事情还在`true`时继续的循环。每一次循环，Rust 都会检查它是否仍然是 `true`。如果变成`false`，Rust会停止循环。

```rust
fn main() {
    let mut counter = 0;

    while counter < 5 {
        counter +=1;
        println!("The counter is now: {}", counter);
    }
}
```

`for`循环可以让你告诉Rust每次要做什么。但是在 `for` 循环中，循环会在一定次数后停止。`for`循环经常使用**范围**。你使用 `..` 和 `..=` 来创建一个范围。

- `..`创建一个**排他的**范围:`0..3`创建了`0, 1, 2`.
- `..=`创建一个**包含的**范围: `0..=3`创建`0, 1, 2`。`0..=3` = `0, 1, 2, 3`.

```rust
fn main() {
    for number in 0..3 {
        println!("The number is: {}", number);
    }

    for number in 0..=3 {
        println!("The next number is: {}", number);
    }
}
```

这个将打印:

```text
The number is: 0
The number is: 1
The number is: 2
The next number is: 0
The next number is: 1
The next number is: 2
The next number is: 3
```

同时注意到，`number`成为0..3的变量名。我们可以把它叫做 `n`，或者 `ntod_het___hno_f`，或者任何名字。然后，我们可以在`println!`中使用这个名字。

如果你不需要变量名，就用`_`。

```rust
fn main() {
    for _ in 0..3 {
        println!("Printing the same thing three times");
    }
}
```

这个打印:

```text
Printing the same thing three times
Printing the same thing three times
Printing the same thing three times
```

因为我们每次都没有给它任何数字来打印。

而实际上，如果你给了一个变量名却不用，Rust会告诉你:

```rust
fn main() {
    for number in 0..3 {
        println!("Printing the same thing three times");
    }
}
```

这打印的内容和上面一样。程序编译正常，但Rust会提醒你没有使用`number`:

```text
warning: unused variable: `number`
 --> src\main.rs:2:9
  |
2 |     for number in 0..3 {
  |         ^^^^^^ help: if this is intentional, prefix it with an underscore: `_number`
```

Rust 建议写 `_number` 而不是 `_`。在变量名前加上 `_` 意味着 "也许我以后会用到它"。但是只用`_`意味着 "我根本不关心这个变量"。所以，如果你以后会使用它们，并且不想让编译器告诉你，你可以在变量名前面加上`_`。

你也可以用`break`来返回一个值。
 你把值写在 `break` 之后，并使用 `;`。下面是一个用 `loop` 和一个断点给出 `my_number` 值的例子。

```rust
fn main() {
    let mut counter = 5;
    let my_number = loop {
        counter +=1;
        if counter % 53 == 3 {
            break counter;
        }
    };
    println!("{}", my_number);
}
```

这时打印出`56`。`break counter;`的意思是 "中断并返回计数器的值"。而且因为整个块以`let`开始，所以`my_number`得到值。

现在我们知道了如何使用循环，这里有一个更好的解决方案来解决我们之前的颜色 "匹配"问题。这是一个更好的解决方案，因为我们要比较所有的东西，而 "for"循环会查看每一项。

```rust
fn match_colours(rbg: (i32, i32, i32)) {
    println!("Comparing a colour with {} red, {} blue, and {} green:", rbg.0, rbg.1, rbg.2);
    let new_vec = vec![(rbg.0, "red"), (rbg.1, "blue"), (rbg.2, "green")]; // 把颜色放进 vec。里面是带颜色名的元组
    let mut all_have_at_least_10 = true; // 先设为 true。若有颜色小于 10 就改为 false
    for item in new_vec {
        if item.0 < 10 {
            all_have_at_least_10 = false; // 现在是 false
            println!("Not much {}.", item.1) // 并打印颜色名。
        }
    }
    if all_have_at_least_10 { // 检查是否仍为 true，是则打印
        println!("Each colour has at least 10.")
    }
    println!(); // 再空一行
}

fn main() {
    let first = (200, 0, 0);
    let second = (50, 50, 50);
    let third = (200, 50, 0);

    match_colours(first);
    match_colours(second);
    match_colours(third);
}
```

这个打印:

```text
Comparing a colour with 200 red, 0 blue, and 0 green:
Not much blue.
Not much green.

Comparing a colour with 50 red, 50 blue, and 50 green:
Each colour has at least 10.

Comparing a colour with 200 red, 50 blue, and 0 green:
Not much green.
```
