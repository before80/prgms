+++
title = "14-关于打印的更多信息"
date = 2026-08-21T12:46:00+08:00
weight = 15
type = "docs"
description = "关于打印的更多信息 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_13.html](https://dhghomon.github.io/easy_rust/Chapter_13.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 关于打印的更多信息

在Rust中，你几乎可以用任何你想要的方式打印东西。这里有一些关于打印的事情需要知道。

添加 `\n` 将会产生一个新行，而 `\t` 将会产生一个标签。

```rust
fn main() {
    // 注意：这里是 print!，不是 println!
    print!("\t Start with a tab\nand move to a new line");
}
```

这样就可以打印了。

```text
         Start with a tab
and move to a new line
```

`""`里面可以写过很多行都没有问题，但是要注意间距。

```rust
fn main() {
    // 注意：第一行之后必须从最左边开始写。
    // 如果直接写在 println! 下面，会多出空格
    println!("Inside quotes
you can write over
many lines
and it will print just fine.");

    println!("If you forget to write
    on the left side, the spaces
    will be added when you print.");
}
```

这个打印出来的。

```text
Inside quotes
you can write over
many lines
and it will print just fine.
If you forget to write
    on the left side, the spaces
    will be added when you print.
```

如果你想打印`\n`这样的字符(称为 "转义字符")，你可以多加一个`\`。

```rust
fn main() {
    println!("Here are two escape characters: \\n and \\t");
}
```

这样就可以打印了。

```text
Here are two escape characters: \n and \t
```

有时你有太多的 `"` 和转义字符，并希望 Rust 忽略所有的字符。要做到这一点，您可以在开头添加 `r#`，在结尾添加 `#`。

```rust
fn main() {
    println!("He said, \"You can find the file at c:\\files\\my_documents\\file.txt.\" Then I found the file."); // 这里我们用了五次 \
    println!(r#"He said, "You can find the file at c:\files\my_documents\file.txt." Then I found the file."#)
}
```

这打印的是同样的东西，但使用 `r#` 使人类更容易阅读。

```text
He said, "You can find the file at c:\files\my_documents\file.txt." Then I found the file.
He said, "You can find the file at c:\files\my_documents\file.txt." Then I found the file.
```

如果你需要在里面打印`#`，那么你可以用`r##`开头，用`##`结尾。如果你需要打印多个连续的`#`，可以在每边多加一个#。

下面是四个例子。

```rust
fn main() {

    let my_string = "'Ice to see you,' he said."; // 单引号
    let quote_string = r#""Ice to see you," he said."#; // 双引号
    let hashtag_string = r##"The hashtag #IceToSeeYou had become very popular."##; // 里面有一个 #，所以至少要用 ##
    let many_hashtags = r####""You don't have to type ### to use a hashtag. You can just use #.""####; // 里面有三个 ###，所以至少要用 ####

    println!("{}\n{}\n{}\n{}\n", my_string, quote_string, hashtag_string, many_hashtags);

}
```

这将打印:

```text
'Ice to see you,' he said.
"Ice to see you," he said.
The hashtag #IceToSeeYou had become very popular.
"You don't have to type ### to use a hashtag. You can just use #."
```

`r#`还有另一个用途:使用它，你可以使用关键字(如`let`、`fn`等)作为变量名。

```rust
fn main() {
    let r#let = 6; // 变量名是 let
    let mut r#mut = 10; // 变量名是 mut
}
```

`r#`之所以有这个功能，是因为旧版本的Rust的关键字比现在的Rust少。所以有了`r#`就可以避免以前不是关键字的变量名的错误。

又或者因为某些原因，你*确实*需要一个函数的名字，比如`return`。那么你可以这样写:

```rust
fn r#return() -> u8 {
    println!("Here is your number.");
    8
}

fn main() {
    let my_number = r#return();
    println!("{}", my_number);
}
```

这样打印出来的结果是:

```text
Here is your number.
8
```

所以你可能不需要它，但是如果你真的需要为一个变量使用一个关键字，那么你可以使用`r#`。



如果你想打印`&str`或`char`的字节，你可以在字符串前写上`b`就可以了。这适用于所有ASCII字符。这些是所有的ASCII字符。

```text
☺☻♥♦♣♠♫☼►◄↕‼¶§▬↨↑↓→∟↔▲▼123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
```

所以，当你打印这个

```rust
fn main() {
    println!("{:?}", b"This will look like numbers");
}
```

这就是结果:

```text
[84, 104, 105, 115, 32, 119, 105, 108, 108, 32, 108, 111, 111, 107, 32, 108, 105, 107, 101, 32, 110, 117, 109, 98, 101, 114, 115]
```

对于`char`来说，这叫做一个*字节*，对于`&str`来说，这叫做一个*字节字符串*。



如果你需要的话，也可以把`b`和`r`放在一起。

```rust
fn main() {
    println!("{:?}", br##"I like to write "#"."##);
}
```

这将打印出 `[73, 32, 108, 105, 107, 101, 32, 116, 111, 32, 119, 114, 105, 116, 101, 32, 34, 35, 34, 46]`。



还有一个Unicode转义，可以让你在字符串中打印任何Unicode字符: `\u{}`。`{}`里面有一个十六进制数字可以打印。下面是一个简短的例子，说明如何获得Unicode数字，以及如何再次打印它。

```rust
fn main() {
    println!("{:X}", '행' as u32); // 把 char 转成 u32 以得到十六进制值
    println!("{:X}", 'H' as u32);
    println!("{:X}", '居' as u32);
    println!("{:X}", 'い' as u32);

    println!("\u{D589}, \u{48}, \u{5C45}, \u{3044}"); // 试着用 Unicode 转义 \u 打印它们
}
```



我们知道，`println!`可以和`{}`(用于显示)或`{:?}`(用于调试)一起打印，再加上`{:#?}`就可以进行漂亮的打印。但是还有很多其他的打印方式。

例如，如果你有一个引用，你可以用`{:p}`来打印*指针地址*。指针地址指的是电脑内存中的位置。

```rust
fn main() {
    let number = 9;
    let number_ref = &number;
    println!("{:p}", number_ref);
}
```

这可以打印`0xe2bc0ffcfc`或其他地址。每次可能都不一样，这取决于你的计算机存储的位置。

或者你可以打印二进制、十六进制和八进制。

```rust
fn main() {
    let number = 555;
    println!("Binary: {:b}, hexadecimal: {:x}, octal: {:o}", number, number, number);
}
```

这将打印出`Binary: 1000101011, hexadecimal: 22b, octal: 1053`。

或者你可以添加数字来改变顺序。第一个变量将在索引0中，下一个在索引1中，以此类推。

```rust
fn main() {
    let father_name = "Vlad";
    let son_name = "Adrian Fahrenheit";
    let family_name = "Țepeș";
    println!("This is {1} {2}, son of {0} {2}.", father_name, son_name, family_name);
}
```

`father_name`在0位，`son_name`在1位，`family_name`在2位。所以它打印的是`This is Adrian Fahrenheit Țepeș, son of Vlad Țepeș`。


也许你有一个非常复杂的字符串要打印，`{}`大括号内有太多的变量。或者你需要不止一次的打印一个变量。那么在`{}`中添加名称就会有帮助。

```rust
fn main() {
    println!(
        "{city1} is in {country} and {city2} is also in {country},
but {city3} is not in {country}.",
        city1 = "Seoul",
        city2 = "Busan",
        city3 = "Tokyo",
        country = "Korea"
    );
}
```

这样就可以打印了。

```text
Seoul is in Korea and Busan is also in Korea,
but Tokyo is not in Korea.
```


如果你愿意，也可以在Rust中进行非常复杂的打印。下面展示怎样做：

{variable:padding alignment minimum.maximum}

要理解这一点，请看

1) 你想要一个变量名吗？先写出来，就像我们上面写{country}一样。
(如果你想做更多的事情，就在后面加一个`:`)
2) 你想要一个填充字符吗？例如，55加上三个 "填充零"就像00055。
3) padding的对齐方式(左/中/右)？
4) 你想要一个最小长度吗？(写一个数字就可以了) 
5) 你想要一个最大长度吗？(写一个数字，前面有一个`.`)

例如，我想写 "a"，左边有五个ㅎ，右边有五个ㅎ。

```rust
fn main() {
    let letter = "a";
    println!("{:ㅎ^11}", letter);
}
```

这样打印出来的结果是`ㅎㅎㅎㅎㅎaㅎㅎㅎㅎㅎ`。我们看看1)到5)的这个情况，就能明白编译器是怎么解读的：

- 你要不要变量名？`{:ㅎ^11}`没有变量名。`:`之前没有任何内容。
- 你需要一个填充字符吗？`{:ㅎ^11}` 是的:ㅎ"在`:`后面，有一个`^`。`<`表示变量在填充字符左边，`>`表示在填充字符右边，`^`表示在填充字符中间。
- 要不要设置最小长度？`{:ㅎ^11}`是:后面有一个11。
- 你想要一个最大长度吗？`{:ㅎ^11}` 不是:前面没有`.`的数字。

下面是多种类型的格式化的例子:


```rust
fn main() {
    let title = "TODAY'S NEWS";
    println!("{:-^30}", title); // 无变量名，用 - 填充，居中，共 30 个字符
    let bar = "|";
    println!("{: <15}{: >15}", bar, bar); // 无变量名，用空格填充，各 15 个字符，一个靠左一个靠右
    let a = "SEOUL";
    let b = "TOKYO";
    println!("{city1:-<15}{city2:->15}", city1 = a, city2 = b); // 变量名 city1 和 city2，用 - 填充，一个靠左一个靠右
}
```

它打印出来了。

```text
---------TODAY'S NEWS---------
|                            |
SEOUL--------------------TOKYO
```
