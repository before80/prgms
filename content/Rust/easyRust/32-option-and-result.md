+++
title = "32-Option 和 Result"
date = 2026-08-21T12:46:00+08:00
weight = 33
type = "docs"
description = "Option 和 Result — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_31.html](https://dhghomon.github.io/easy_rust/Chapter_31.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Option 和 Result

我们现在理解了枚举和泛型，所以我们可以理解`Option`和`Result`。Rust使用这两个枚举来使代码更安全。

我们将从`Option`开始。

## Option

当你有一个可能存在，也可能不存在的值时，你就用`Option`。当一个值存在的时候就是`Some(value)`，不存在的时候就是`None`，下面是一个坏代码的例子，可以用`Option`来改进。

```rust
    // ⚠️
fn take_fifth(value: Vec<i32>) -> i32 {
    value[4]
}

fn main() {
    let new_vec = vec![1, 2];
    let index = take_fifth(new_vec);
}
```

当我们运行这段代码时，它崩溃。以下是信息。

```text
thread 'main' panicked at 'index out of bounds: the len is 2 but the index is 4', src\main.rs:34:5
```

崩溃的意思是，程序在问题发生之前就停止了。Rust看到函数想要做一些不可能的事情，就会停止。它 "解开堆栈"(从堆栈中取值)，并告诉你 "对不起，我不能这样做"。

所以现在我们将返回类型从`i32`改为`Option<i32>`。这意味着 "如果有的话给我一个`Some(i32)`，如果没有的话给我一个`None`"。我们说`i32`是 "包"在一个`Option`里面，也就是说它在一个`Option`里面。你必须做一些事情才能把这个值弄出来。

```rust
fn take_fifth(value: Vec<i32>) -> Option<i32> {
    if value.len() < 5 { // .len() 返回 vec 的长度。
                         // 长度至少要是 5。
        None
    } else {
        Some(value[4])
    }
}

fn main() {
    let new_vec = vec![1, 2];
    let bigger_vec = vec![1, 2, 3, 4, 5];
    println!("{:?}, {:?}", take_fifth(new_vec), take_fifth(bigger_vec));
}
```

这个打印的是`None, Some(5)`。这下好了，因为现在我们再也不崩溃了。但是我们如何得到5的值呢？

我们可以用 `.unwrap()` 在一个Option中获取值，但要小心 `.unwrap()`。这就像拆礼物一样:也许里面有好东西，也许里面有一条愤怒的蛇。只有在你确定的情况下，你才会想要`.unwrap()`。如果你拆开一个`None`的值，程序就会崩溃。

```rust
// ⚠️
fn take_fifth(value: Vec<i32>) -> Option<i32> {
    if value.len() < 5 {
        None
    } else {
        Some(value[4])
    }
}

fn main() {
    let new_vec = vec![1, 2];
    let bigger_vec = vec![1, 2, 3, 4, 5];
    println!("{:?}, {:?}",
        take_fifth(new_vec).unwrap(), // 这个是 None。.unwrap() 会 panic！
        take_fifth(bigger_vec).unwrap()
    );
}
```

消息是: 
```text
thread 'main' panicked at 'called `Option::unwrap()` on a `None` value', src\main.rs:14:9
```

但我们不需要使用`.unwrap()`。我们可以使用`match`。那么我们就可以把我们有`Some`的值打印出来，如果有`None`的值就不要碰。比如说

```rust
fn take_fifth(value: Vec<i32>) -> Option<i32> {
    if value.len() < 5 {
        None
    } else {
        Some(value[4])
    }
}

fn handle_option(my_option: Vec<Option<i32>>) {
  for item in my_option {
    match item {
      Some(number) => println!("Found a {}!", number),
      None => println!("Found a None!"),
    }
  }
}

fn main() {
    let new_vec = vec![1, 2];
    let bigger_vec = vec![1, 2, 3, 4, 5];
    let mut option_vec = Vec::new(); // 新建一个 vec 来存放这些 Option
                                     // 这个 vec 的类型是 Vec<Option<i32>>，即 Option<i32> 的向量。

    option_vec.push(take_fifth(new_vec)); // 把 "None" 推进 vec
    option_vec.push(take_fifth(bigger_vec)); // 把 "Some(5)" 推进 vec

    handle_option(option_vec); // handle_option 查看 vec 中的每个 Option。
                               // 若是 Some 就打印值；若是 None 则不处理。
}
```

这个打印:

```text
Found a None!
Found a 5!
```


因为我们知道泛型，所以我们能够读懂`Option`的代码。它看起来是这样的:

```rust
enum Option<T> {
    None,
    Some(T),
}

fn main() {}
```

要记住的重要一点是:有了`Some`，你就有了一个类型为`T`的值(任何类型)。还要注意的是，`enum`名字后面的角括号围绕着`T`是告诉编译器它是通用的。它没有`Display`这样的trait或任何东西来限制它，所以它可以是任何东西。但是对于`None`，你什么都没有。

所以在`match`语句中，对于Option，你不能说。

```rust
// 🚧
Some(value) => println!("The value is {}", value),
None(value) => println!("The value is {}", value),
```

因为`None`只是`None`。

当然，还有更简单的方法来使用Option。在这段代码中，我们将使用一个叫做 `.is_some()` 的方法来告诉我们是否是 `Some`。(是的，还有一个叫做`.is_none()`的方法。)在这个更简单的方法中，我们不需要`handle_option()`了。我们也不需要Option的vec了。

```rust
fn take_fifth(value: Vec<i32>) -> Option<i32> {
    if value.len() < 5 {
        None
    } else {
        Some(value[4])
    }
}

fn main() {
    let new_vec = vec![1, 2];
    let bigger_vec = vec![1, 2, 3, 4, 5];
    let vec_of_vecs = vec![new_vec, bigger_vec];
    for vec in vec_of_vecs {
        let inside_number = take_fifth(vec);
        if inside_number.is_some() {
            // 得到 Some 时 .is_some() 返回 true，得到 None 时返回 false
            println!("We got: {}", inside_number.unwrap()); // 已经检查过，现在可以安全使用 .unwrap()
        } else {
            println!("We got nothing.");
        }
    }
}
```

这个将打印:

```text
We got nothing.
We got: 5
```

## Result

Result和Option类似，但这里的区别是。

- Option大约是`Some`或`None`(有值或无值)。
- Result大约是`Ok`或`Err`(还好的结果，或错误的结果)。

所以，`Option`是如果你在想:"也许会有，也许不会有。"也许会有一些东西，也许不会有。" 但`Result`是如果你在想: "也许会失败"

比较一下，这里是Option和Result的签名。

```rust
enum Option<T> {
    None,
    Some(T),
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}

fn main() {}
```

所以Result在 "Ok "里面有一个值，在 "Err "里面有一个值。这是因为错误通常包含描述错误的信息。

`Result<T, E>`的意思是你要想好`Ok`要返回什么，`Err`要返回什么。其实，你可以决定任何事情。甚至这个也可以。

```rust
fn check_error() -> Result<(), ()> {
    Ok(())
}

fn main() {
    check_error();
}
```

`check_error`说 "如果得到`Ok`就返回`()`，如果得到`Err`就返回`()`"。然后我们用`()`返回`Ok`。

编译器给了我们一个有趣的警告。

```text
warning: unused `std::result::Result` that must be used
 --> src\main.rs:6:5
  |
6 |     check_error();
  |     ^^^^^^^^^^^^^^
  |
  = note: `#[warn(unused_must_use)]` on by default
  = note: this `Result` may be an `Err` variant, which should be handled
```

这是真的:我们只返回了`Result`，但它可能是一个`Err`。所以让我们稍微处理一下这个错误，尽管我们仍然没有真正做任何事情。

```rust
fn give_result(input: i32) -> Result<(), ()> {
    if input % 2 == 0 {
        return Ok(())
    } else {
        return Err(())
    }
}

fn main() {
    if give_result(5).is_ok() {
        println!("It's okay, guys")
    } else {
        println!("It's an error, guys")
    }
}
```

打印出`It's an error, guys`。所以我们只是处理了第一个错误。

记住，轻松检查的四种方法是`.is_some()`、`is_none()`、`is_ok()`和`is_err()`。


有时，一个带有Result的函数会用`String`来表示`Err`的值。这不是最好的方法，但比我们目前所做的要好一些。

```rust
fn check_if_five(number: i32) -> Result<i32, String> {
    match number {
        5 => Ok(number),
        _ => Err("Sorry, the number wasn't five.".to_string()), // 这是我们的错误信息
    }
}

fn main() {
    let mut result_vec = Vec::new(); // 为结果新建一个 vec

    for number in 2..7 {
        result_vec.push(check_if_five(number)); // 把每个结果推进 vec
    }

    println!("{:?}", result_vec);
}
```

我们的Vec打印:

```text
[Err("Sorry, the number wasn\'t five."), Err("Sorry, the number wasn\'t five."), Err("Sorry, the number wasn\'t five."), Ok(5),
Err("Sorry, the number wasn\'t five.")]
```

就像Option一样，在`Err`上用`.unwrap()`就会崩溃。

```rust
    // ⚠️
fn main() {
    let error_value: Result<i32, &str> = Err("There was an error"); // 创建一个已经是 Err 的 Result
    println!("{}", error_value.unwrap()); // 对其 unwrap
}
```

程序崩溃，打印。

```text
thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: "There was an error"', src\main.rs:30:20
```

这些信息可以帮助你修正你的代码。`src\main.rs:30:20`的意思是 "在目录src的main.rs内，第30行和第20列"。所以你可以去那里查看你的代码并修复问题。

你也可以创建自己的错误类型，标准库中的Result函数和其他人的代码通常都会这样做。例如，标准库中的这个函数。

```rust
// 🚧
pub fn from_utf8(vec: Vec<u8>) -> Result<String, FromUtf8Error>
```

这个函数接收一个字节向量(`u8`)，并尝试创建一个`String`，所以Result的成功情况是`String`，错误情况是`FromUtf8Error`。你可以给你的错误类型起任何你想要的名字。

使用 `match` 与 `Option` 和 `Result` 有时需要很多代码。例如，`.get()` 方法在 `Vec` 上返回 `Option`。

```rust
fn main() {
    let my_vec = vec![2, 3, 4];
    let get_one = my_vec.get(0); // 用 0 获取第一个数字
    let get_two = my_vec.get(10); // 返回 None
    println!("{:?}", get_one);
    println!("{:?}", get_two);
}
```

此打印

```text
Some(2)
None
```

所以现在我们可以匹配得到数值。让我们使用0到10的范围，看看是否符合`my_vec`中的数字。

```rust
fn main() {
    let my_vec = vec![2, 3, 4];

    for index in 0..10 {
      match my_vec.get(index) {
        Some(number) => println!("The number is: {}", number),
        None => {}
      }
    }
}
```

这是好的，但是我们对`None`不做任何处理，因为我们不关心。这里我们可以用`if let`把代码变小。`if let`的意思是 "符合就做，不符合就不做"。`if let`是在你不要求对所有的东西都匹配的时候使用。

```rust
fn main() {
    let my_vec = vec![2, 3, 4];

    for index in 0..10 {
      if let Some(number) = my_vec.get(index) {
        println!("The number is: {}", number);
      }
    }
}
```

**重要的是要记住**。`if let Some(number) = my_vec.get(index)`的意思是 "如果你从`my_vec.get(index)`得到`Some(number)`"。

另外注意:它使用的是一个`=`。它不是一个布尔值。

`while let`就像`if let`的一个while循环。想象一下，我们有这样的气象站数据。

```text
["Berlin", "cloudy", "5", "-7", "78"]
["Athens", "sunny", "not humid", "20", "10", "50"]
```

我们想得到数字，但不想得到文字。对于数字，我们可以使用一个叫做 `parse::<i32>()` 的方法。`parse()`是方法，`::<i32>`是类型。它将尝试把 `&str` 变成 `i32`，如果可以的话就把它给我们。它返回一个 `Result`，因为它可能无法工作(比如你想让它解析 "Billybrobby"--那不是一个数字)。

我们还将使用 `.pop()`。这将从向量中取出最后一项。

```rust
fn main() {
    let weather_vec = vec![
        vec!["Berlin", "cloudy", "5", "-7", "78"],
        vec!["Athens", "sunny", "not humid", "20", "10", "50"],
    ];
    for mut city in weather_vec {
        println!("For the city of {}:", city[0]); // 在我们的数据里，每组第一项都是城市名
        while let Some(information) = city.pop() {
            // 意思是：一直 pop，直到弹不出来为止
            // 当向量长度为 0 时会返回 None
            // 然后循环停止。
            if let Ok(number) = information.parse::<i32>() {
                // 尝试解析名为 information 的变量
                // 这会返回 Result。若是 Ok(number) 就打印
                println!("The number is: {}", number);
            }  // 这里什么也不写，因为出错时我们不做任何事，直接丢弃
        }
    }
}
```

这将打印:

```text
For the city of Berlin:
The number is: 78
The number is: -7
The number is: 5
For the city of Athens:
The number is: 50
The number is: 10
The number is: 20
```
