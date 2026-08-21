+++
title = "34-? 操作符"
date = 2026-08-21T12:46:00+08:00
weight = 35
type = "docs"
description = "? 操作符 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_33.html](https://dhghomon.github.io/easy_rust/Chapter_33.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# ? 操作符

有一种更短的方法来处理`Result`(和`Option`)，它比`match`和`if let`更短。它叫做 "问号运算符"，就是`?`。在返回结果的函数后，可以加上`?`。这样就会:

- 如果是`Ok`，返回`Result`里面的内容。
- 如果是`Err`，则将错误传回。

换句话说，它几乎为你做了所有的事情。

我们可以用 `.parse()` 再试一次。我们将编写一个名为 `parse_str` 的函数，试图将 `&str` 变成 `i32`。它看起来像这样:

```rust
use std::num::ParseIntError;

fn parse_str(input: &str) -> Result<i32, ParseIntError> {
    let parsed_number = input.parse::<i32>()?; // 这里就是问号运算符
    Ok(parsed_number)
}

fn main() {}
```

这个函数接收一个 `&str`。如果是 `Ok`，则给出一个 `i32`，包裹在 `Ok` 中。如果是 `Err`，则返回 `ParseIntError`。然后我们尝试解析这个数字，并加上`?`。也就是 "检查是否错误，如果没问题就给出Result里面的内容"。如果有问题，就会返回错误并结束。但如果没问题，就会进入下一行。下一行是`Ok()`里面的数字。我们需要用`Ok`来包装，因为返回的是`Result<i32, ParseIntError>`，而不是`i32`。

现在，我们可以试试我们的函数。让我们看看它对`&str`的vec有什么作用。


```rust
fn parse_str(input: &str) -> Result<i32, std::num::ParseIntError> {
    let parsed_number = input.parse::<i32>()?;
    Ok(parsed_number)
}

fn main() {
    let str_vec = vec!["Seven", "8", "9.0", "nice", "6060"];
    for item in str_vec {
        let parsed = parse_str(item);
        println!("{:?}", parsed);
    }
}
```

这个打印:

```text
Err(ParseIntError { kind: InvalidDigit })
Ok(8)
Err(ParseIntError { kind: InvalidDigit })
Err(ParseIntError { kind: InvalidDigit })
Ok(6060)
```

我们是怎么找到`std::num::ParseIntError`的呢？一个简单的方法就是再 "问"一下编译器。

```rust
fn main() {
    let failure = "Not a number".parse::<i32>();
    failure.rbrbrb(); // ⚠️ 编译器：“rbrbrb() 是什么？？”
}
```

编译器不懂，说。

```text
error[E0599]: no method named `rbrbrb` found for enum `std::result::Result<i32, std::num::ParseIntError>` in the current scope
 --> src\main.rs:3:13
  |
3 |     failure.rbrbrb();
  |             ^^^^^^ method not found in `std::result::Result<i32, std::num::ParseIntError>`
```

所以`std::result::Result<i32, std::num::ParseIntError>`就是我们需要的签名。

我们不需要写 `std::result::Result`，因为 `Result` 总是 "在范围内"(在范围内 = 准备好使用)。Rust对我们经常使用的所有类型都是这样做的，所以我们不必写`std::result::Result`、`std::collections::Vec`等。

我们现在还没有处理文件这样的东西，所以?操作符看起来还不是太有用。但这里有一个无用但快速的例子，说明你如何在单行上使用它。与其用 `.parse()` 创建一个 `i32`，不如做更多。我们将创建一个 `u16`，然后把它变成 `String`，再变成 `u32`，然后再变成 `String`，最后变成 `i32`。

```rust
use std::num::ParseIntError;

fn parse_str(input: &str) -> Result<i32, ParseIntError> {
    let parsed_number = input.parse::<u16>()?.to_string().parse::<u32>()?.to_string().parse::<i32>()?; // 每次加 ? 以检查并向上传递错误
    Ok(parsed_number)
}

fn main() {
    let str_vec = vec!["Seven", "8", "9.0", "nice", "6060"];
    for item in str_vec {
        let parsed = parse_str(item);
        println!("{:?}", parsed);
    }
}
```

这打印出同样的东西，但这次我们在一行中处理了三个`Result`。稍后我们将对文件进行处理，因为它们总是返回`Result`，因为很多事情都可能出错。

想象一下:你想打开一个文件，向它写入，然后关闭它。首先你需要成功找到这个文件(这就是一个`Result`)。然后你需要成功地写入它(那是一个`Result`)。对于`?`，你可以在一行上完成。

## When panic and unwrap are good

Rust有一个`panic!`的宏，你可以用它来让程序崩溃。它使用起来很方便。

```rust
fn main() {
    panic!("Time to panic!");
}
```

运行程序时，会显示信息`"Time to panic!"`。`thread 'main' panicked at 'Time to panic!', src\main.rs:2:3`

你会记得`src\main.rs`是目录和文件名，`2:3`是行名和列名。有了这些信息，你就可以找到代码并修复它。

`panic!`是一个很好用的宏，以确保你知道什么时候有变化。例如，这个叫做`prints_three_things`的函数总是从一个向量中打印出索引[0]、[1]和[2]。这没关系，因为我们总是给它一个有三个元素的向量。

```rust
fn prints_three_things(vector: Vec<i32>) {
    println!("{}, {}, {}", vector[0], vector[1], vector[2]);
}

fn main() {
    let my_vec = vec![8, 9, 10];
    prints_three_things(my_vec);
}
```

它打印出`8, 9, 10`，一切正常。

但试想一下，后来我们写的代码越来越多，忘记了`my_vec`只能有三个元素。现在`my_vec`在这部分有六个元素。

```rust
fn prints_three_things(vector: Vec<i32>) {
  println!("{}, {}, {}", vector[0], vector[1], vector[2]);
}

fn main() {
  let my_vec = vec![8, 9, 10, 10, 55, 99]; // 现在 my_vec 有六个元素
  prints_three_things(my_vec);
}
```

不会发生错误，因为[0]和[1]和[2]都在这个较长的`Vec`里面。但如果只能有三个元素呢？我们就不会知道有问题了，因为程序不会崩溃。我们应该这样做:

```rust
fn prints_three_things(vector: Vec<i32>) {
    if vector.len() != 3 {
        panic!("my_vec must always have three items") // 长度不是 3 时会 panic
    }
    println!("{}, {}, {}", vector[0], vector[1], vector[2]);
}

fn main() {
    let my_vec = vec![8, 9, 10];
    prints_three_things(my_vec);
}
```

现在我们知道，如果向量有6个元素，它应该要崩溃:

```rust
    // ⚠️
fn prints_three_things(vector: Vec<i32>) {
    if vector.len() != 3 {
        panic!("my_vec must always have three items")
    }
    println!("{}, {}, {}", vector[0], vector[1], vector[2]);
}

fn main() {
    let my_vec = vec![8, 9, 10, 10, 55, 99];
    prints_three_things(my_vec);
}
```

这样我们就得到了`thread 'main' panicked at 'my_vec must always have three items', src\main.rs:8:9`。多亏了`panic!`，我们现在记得`my_vec`应该只有三个元素。所以`panic!`是一个很好的宏，可以在你的代码中创建提醒。

还有三个与`panic!`类似的宏，你在测试中经常使用。它们分别是 `assert!`, `assert_eq!`, 和 `assert_ne!`.

下面是它们的意思。

- `assert!()`: 如果`()`里面的部分不是真的, 程序就会崩溃.
- `assert_eq!()`:`()`里面的两个元素必须相等。
- `assert_ne!()`:`()`里面的两个元素必须不相等。(*ne*表示不相等)

一些例子。

```rust
fn main() {
    let my_name = "Loki Laufeyson";

    assert!(my_name == "Loki Laufeyson");
    assert_eq!(my_name, "Loki Laufeyson");
    assert_ne!(my_name, "Mithridates");
}
```

这不会有任何作用，因为三个断言宏都没有问题。(这就是我们想要的)

如果你愿意，还可以加个提示信息。

```rust
fn main() {
    let my_name = "Loki Laufeyson";

    assert!(
        my_name == "Loki Laufeyson",
        "{} should be Loki Laufeyson",
        my_name
    );
    assert_eq!(
        my_name, "Loki Laufeyson",
        "{} and Loki Laufeyson should be equal",
        my_name
    );
    assert_ne!(
        my_name, "Mithridates",
        "You entered {}. Input must not equal Mithridates",
        my_name
    );
}
```

这些信息只有在程序崩溃时才会显示。所以如果你运行这个。

```rust
fn main() {
    let my_name = "Mithridates";

    assert_ne!(
        my_name, "Mithridates",
        "You enter {}. Input must not equal Mithridates",
        my_name
    );
}
```

它将显示:

```text
thread 'main' panicked at 'assertion failed: `(left != right)`
  left: `"Mithridates"`,
 right: `"Mithridates"`: You entered Mithridates. Input must not equal Mithridates', src\main.rs:4:5
```

所以它说 "你说左!=右，但左==右"。而且它显示我们的信息说`You entered Mithridates. Input must not equal Mithridates`。

当你在写程序的时候，想让它在出现问题的时候崩溃，`unwrap`是个好注意。当你的代码写完后，把`unwrap`改成其他不会崩溃的东西就好了。

你也可以用`expect`，它和`unwrap`一样，但是更好一些，因为它支持用户自定义信息。教科书通常会给出这样的建议:"如果你经常使用`.unwrap()`, 至少也要用`.expect()`来获得更好的错误信息."

这样会崩溃的:

```rust
   // ⚠️
fn get_fourth(input: &Vec<i32>) -> i32 {
    let fourth = input.get(3).unwrap();
    *fourth
}

fn main() {
    let my_vec = vec![9, 0, 10];
    let fourth = get_fourth(&my_vec);
}
```

错误信息是`thread 'main' panicked at 'called Option::unwrap() on a None value', src\main.rs:7:18`。

现在我们用`expect`来写自己的信息。

```rust
   // ⚠️
fn get_fourth(input: &Vec<i32>) -> i32 {
    let fourth = input.get(3).expect("Input vector needs at least 4 items");
    *fourth
}

fn main() {
    let my_vec = vec![9, 0, 10];
    let fourth = get_fourth(&my_vec);
}
```

又崩溃了，但错误比较多。`thread 'main' panicked at 'Input vector needs at least 4 items', src\main.rs:7:18`. `.expect()`因为这个原因比`.unwrap()`要好一点，但是在`None`上还是会崩溃。现在这里有一个错误的案例，一个函数试图unwrap两次。它需要一个`Vec<Option<i32>>`，所以可能每个部分都会有一个`Some<i32>`，也可能是一个`None`。

```rust
fn try_two_unwraps(input: Vec<Option<i32>>) {
    println!("Index 0 is: {}", input[0].unwrap());
    println!("Index 1 is: {}", input[1].unwrap());
}

fn main() {
    let vector = vec![None, Some(1000)]; // 这个向量含有 None，所以会 panic
    try_two_unwraps(vector);
}
```

消息是:``thread 'main' panicked at 'called `Option::unwrap()` on a `None` value', src\main.rs:2:32``。我们不检查行号，就不知道是第一个`.unwrap()`还是第二个`.unwrap()`。最好是检查一下长度，也不要unwrap。不过有了`.expect()`至少会好*一点*。下面是`.expect()`的情况：

```rust
fn try_two_unwraps(input: Vec<Option<i32>>) {
    println!("Index 0 is: {}", input[0].expect("The first unwrap had a None!"));
    println!("Index 1 is: {}", input[1].expect("The second unwrap had a None!"));
}

fn main() {
    let vector = vec![None, Some(1000)];
    try_two_unwraps(vector);
}
```

所以，这是好一点的。`thread 'main' panicked at 'The first unwrap had a None!', src\main.rs:2:32`. 我们也有行号，所以我们可以找到它。


如果你想一直有一个你想选择的值，也可以用`unwrap_or`。如果你这样做，它永远不会崩溃。就是这样的。


- 1)好，因为你的程序不会崩溃，但
- 2)如果你想让程序在出现问题时崩溃，也许不好。

但通常我们都不希望自己的程序崩溃，所以`unwrap_or`是个不错的方法。

```rust
fn main() {
    let my_vec = vec![8, 9, 10];

    let fourth = my_vec.get(3).unwrap_or(&0); // 若 .get 失败，就用 &0 作为值。
                                              // .get 返回引用，所以要用 &0 而不是 0
                                              // 若希望 fourth 是 0 而不是 &0，可写成带 * 的形式（如 let *fourth）
                                              // 但这里只是打印，所以无所谓

    println!("{}", fourth);
}
```

这将打印出 `0`，因为 `.unwrap_or(&0)` 给出了一个 0，即使它是 `None`。
