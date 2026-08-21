+++
title = "62-编写宏"
date = 2026-08-21T12:46:00+08:00
weight = 63
type = "docs"
description = "编写宏 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_61.html](https://dhghomon.github.io/easy_rust/Chapter_61.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 编写宏

编写宏是非常复杂的。你可能永远都不需要写宏，但有时你可能会想写，因为它们非常方便。写宏很有趣，因为它们几乎是不同的语言。要写一个宏，你实际上是用另一个叫`macro_rules!`的宏。然后你添加你的宏名称，并打开一个`{}`块。里面有点像`match`语句。

这里有一个只取`()`，然后返回6:

```rust
macro_rules! give_six {
    () => {
        6
    };
}

fn main() {
    let six = give_six!();
    println!("{}", six);
}
```

但这和`match`语句是不一样的，因为宏实际上不会编译任何东西。它只是接受一个输入并给出一个输出。然后编译器会检查它是否有意义。这就是为什么宏就像 "写代码的代码"。你会记得，一个真正的`match`语句需要给出相同的类型，所以这不会工作:

```rust
fn main() {
// ⚠️
    let my_number = 10;
    match my_number {
        10 => println!("You got a ten"),
        _ => 10,
    }
}
```

它会抱怨你在一种情况下要返回`()`，在另一种情况下要返回`i32`。

```text
error[E0308]: `match` arms have incompatible types
 --> src\main.rs:5:14
  |
3 | /     match my_number {
4 | |         10 => println!("You got a ten"),
  | |               ------------------------- this is found to be of type `()`
5 | |         _ => 10,
  | |              ^^ expected `()`, found integer
6 | |     }
  | |_____- `match` arms have incompatible types
```

但宏并不关心，因为它只是给出一个输出。它不是一个编译器--它是代码前的代码。所以你可以这样做:

```rust
macro_rules! six_or_print {
    (6) => {
        6
    };
    () => {
        println!("You didn't give me 6.");
    };
}

fn main() {
    let my_number = six_or_print!(6);
    six_or_print!();
}
```

这个就好办了，打印的是`You didn't give me 6.`。你也可以看到，这不是匹配分支，因为没有`_`行。我们只能给它`(6)`，或者`()`，其他的都会出错。而我们给它的`6`甚至不是`i32`，只是一个输入6。其实你可以设置任何东西作为宏的输入，因为它只是看输入，看得到什么。比如说:

```rust
macro_rules! might_print {
    (THis is strange input 하하はは哈哈 but it still works) => {
        println!("You guessed the secret message!")
    };
    () => {
        println!("You didn't guess it");
    };
}

fn main() {
    might_print!(THis is strange input 하하はは哈哈 but it still works);
    might_print!();
}
```

所以这个奇怪的宏只响应两件事。`()`和`(THis is strange input 하하はは哈哈 but it still works)`. 没有其他的东西。它打印的是:

```text
You guessed the secret message!
You didn't guess it
```

所以宏不完全是Rust语法。但是宏也可以理解你给它的不同类型的输入。拿这个例子来说。

```rust
macro_rules! might_print {
    ($input:expr) => {
        println!("You gave me: {}", $input);
    }
}

fn main() {
    might_print!(6);
}
```

这将打印`You gave me: 6`。`$input:expr`部分很重要。它的意思是 "对于一个表达式，给它起一个变量名$input"。在宏中，变量以`$`开头。在这个宏中，如果你给它一个表达式，它就会打印出来。我们再来试一试。

```rust
macro_rules! might_print {
    ($input:expr) => {
        println!("You gave me: {:?}", $input); // 用 {:?}，因为会传入不同类型的表达式
    }
}

fn main() {
    might_print!(()); // 传入 ()
    might_print!(6); // 传入 6
    might_print!(vec![8, 9, 7, 10]); // 传入一个 vec
}
```

这将打印:

```text
You gave me: ()
You gave me: 6
You gave me: [8, 9, 7, 10]
```

另外注意，我们写了`{:?}`，但它不会检查`&input`是否实现了`Debug`。它只会写代码，并尝试让它编译，如果没有，那么它就会给出一个错误。

那么除了`expr`，宏还能看到什么呢？它们是 `block | expr | ident | item | lifetime | literal  | meta | pat | path | stmt | tt | ty | vis`. 这就是复杂的部分。你可以在[这里](https://doc.rust-lang.org/beta/reference/macros-by-example.html)看到它们各自的意思，这里说:

```text
item: an Item
block: a BlockExpression
stmt: a Statement without the trailing semicolon (except for item statements that require semicolons)
pat: a Pattern
expr: an Expression
ty: a Type
ident: an IDENTIFIER_OR_KEYWORD
path: a TypePath style path
tt: a TokenTree (a single token or tokens in matching delimiters (), [], or {})
meta: an Attr, the contents of an attribute
lifetime: a LIFETIME_TOKEN
vis: a possibly empty Visibility qualifier
literal: matches -?LiteralExpression
```

另外有一个很好的网站叫cheats.rs，在[这里](https://cheats.rs/#macros-attributes)解释了它们，并且每个都给出了例子。

然而，对于大多数宏，你只会用到 `expr`、`ident` 和 `tt`。`ident` 表示标识符，用于变量或函数名称。`tt`表示token树，和任何类型的输入。让我们尝试用这两个词创建一个简单的宏。

```rust
macro_rules! check {
    ($input1:ident, $input2:expr) => {
        println!(
            "Is {:?} equal to {:?}? {:?}",
            $input1,
            $input2,
            $input1 == $input2
        );
    };
}

fn main() {
    let x = 6;
    let my_vec = vec![7, 8, 9];
    check!(x, 6);
    check!(my_vec, vec![7, 8, 9]);
    check!(x, 10);
}
```

所以这将取一个`ident`(像一个变量名)和一个表达式，看看它们是否相同。它的打印结果是

```text
Is 6 equal to 6? true
Is [7, 8, 9] equal to [7, 8, 9]? true
Is 6 equal to 10? false
```

而这里有一个宏，输入`tt`，然后把它打印出来。它先用一个叫`stringify!`的宏创建一个字符串。

```rust
macro_rules! print_anything {
    ($input:tt) => {
        let output = stringify!($input);
        println!("{}", output);
    };
}

fn main() {
    print_anything!(ththdoetd);
    print_anything!(87575oehq75onth);
}
```

这个将打印:

```text
ththdoetd
87575oehq75onth
```

但是如果我们给它一些带有空格、逗号等的东西，它就不会打印。它会认为我们给了它不止一个元素或额外的信息，所以它会感到困惑。

这就是宏开始变得困难的地方。

要一次给宏提供多个元素，我们必须使用不同的语法。不要用`$input`，而是`$($input1),*`。这意味着零或更多(这是 * 的意思)，用逗号分隔。如果你想要一个或多个，请使用 `+` 而不是 `*`。

现在我们的宏看起来是这样的。

```rust
macro_rules! print_anything {
    ($($input1:tt),*) => {
        let output = stringify!($($input1),*);
        println!("{}", output);
    };
}


fn main() {
    print_anything!(ththdoetd, rcofe);
    print_anything!();
    print_anything!(87575oehq75onth, ntohe, 987987o, 097);
}
```

所以它接受任何用逗号隔开的token树，并使用 `stringify!` 把它变成一个字符串。然后打印出来。它的打印结果是:

```text
ththdoetd, rcofe

87575oehq75onth, ntohe, 987987o, 097
```

如果我们使用`+`而不是`*`，它会给出一个错误，因为有一次我们没有给它输入。所以`*`是一个比较安全的选择。

所以现在我们可以开始看到宏的威力了。在接下来的这个例子中，我们实际上可以创建我们自己的函数:

```rust
macro_rules! make_a_function {
    ($name:ident, $($input:tt),*) => { // 先给函数起一个名字，再检查其余内容
        fn $name() {
            let output = stringify!($($input),*); // 把其余内容变成字符串
            println!("{}", output);
        }
    };
}


fn main() {
    make_a_function!(print_it, 5, 5, 6, I); // 想要一个叫 print_it() 的函数，打印我们给它的其余内容
    print_it();
    make_a_function!(say_its_nice, this, is, really, nice); // 一样，只是换了函数名
    say_its_nice();
}
```

这个打印:

```text
5, 5, 6, I
this, is, really, nice
```


所以现在我们可以开始了解其他的宏了。你可以看到，我们已经使用的一些宏非常简单。这里是我们用来写入文件的`write!`的那个:

```rust
macro_rules! write {
    ($dst:expr, $($arg:tt)*) => ($dst.write_fmt($crate::format_args!($($arg)*)))
}
```

要使用它，你就输入这个:

- 一个表达式(`expr`) 得到变量名`$dst`.
- 之后的一切。如果它写的是`$arg:tt`，那么它只会取1个，但是因为它写的是`$($arg:tt)*`，所以它取0，1，或者任意多个。

然后它取`$dst`，并对它使用了一个叫做`write_fmt`的方法。在这里面，它使用了另一个叫做`format_args!`的宏，它接受所有的`$($arg)*`，或者我们输入的所有参数。



现在我们来看一下`todo!`这个宏。当你想让程序编译但还没有写出你的代码时，就会用到这个宏。它看起来像这样:

```rust
macro_rules! todo {
    () => (panic!("not yet implemented"));
    ($($arg:tt)+) => (panic!("not yet implemented: {}", $crate::format_args!($($arg)+)));
}
```

这个有两个选项:你可以输入`()`，也可以输入一些token树(`tt`)。

- 如果你输入`()`，它只是`panic!`，并加上一个信息。所以其实你可以直接写`panic!("not yet implemented")`，而不是`todo!`，这也是一样的。
- 如果你输入一些参数，它会尝试打印它们。你可以看到里面有同样的`format_args!`宏，它的工作原理和`println!`一样。

所以，如果你写了这个，它也会工作:

```rust
fn not_done() {
    let time = 8;
    let reason = "lack of time";
    todo!("Not done yet because of {}. Check back in {} hours", reason, time);
}

fn main() {
    not_done();
}
```

这将打印:

```text
thread 'main' panicked at 'not yet implemented: Not done yet because of lack of time. Check back in 8 hours', src/main.rs:4:5
```


在一个宏里面，你甚至可以调用同一个宏。这里有一个。

```rust
macro_rules! my_macro {
    () => {
        println!("Let's print this.");
    };
    ($input:expr) => {
        my_macro!();
    };
    ($($input:expr),*) => {
        my_macro!();
    }
}

fn main() {
    my_macro!(vec![8, 9, 0]);
    my_macro!(toheteh);
    my_macro!(8, 7, 0, 10);
    my_macro!();
}
```

这个可以取`()`，也可以取一个表达式，也可以取很多表达式。但是不管你放什么表达式，它都会忽略所有的表达式，只是在`()`上调用`my_macro!`。所以输出的只是`Let's print this`，四次。

在`dbg!`宏中也可以看到同样的情况，也是调用自己。

```rust
macro_rules! dbg {
    () => {
        $crate::eprintln!("[{}:{}]", $crate::file!(), $crate::line!()); //$crate 表示宏所在的 crate。
    };
    ($val:expr) => {
        // 这里故意用 `match`，因为它会影响临时值的生命周期
        // —— https://stackoverflow.com/a/48732525/1063961
        match $val {
            tmp => {
                $crate::eprintln!("[{}:{}] {} = {:#?}",
                    $crate::file!(), $crate::line!(), $crate::stringify!($val), &tmp);
                tmp
            }
        }
    };
    // 单参数时末尾逗号会被忽略
    ($val:expr,) => { $crate::dbg!($val) };
    ($($val:expr),+ $(,)?) => {
        ($($crate::dbg!($val)),+,)
    };
}
```

(`eprintln!`与`println!`相同，只打印到`io::stderr`而不是`io::stdout`。还有`eprint!`不增加一行)。)

所以我们可以自己去试一试。

```rust
fn main() {
    dbg!();
}
```

这与第一分支相匹配，所以它会用`file!`和`line!`宏打印文件名和行名。它打印的是`[src/main.rs:2]`。

我们用这个来试试。

```rust
fn main() {
    dbg!(vec![8, 9, 10]);
}
```

这将匹配下一个分支，因为它是一个表达式。然后它将调用输入`tmp`并使用这个代码。` $crate::eprintln!("[{}:{}] {} = {:#?}", $crate::file!(), $crate::line!(), $crate::stringify!($val), &tmp);`. 所以它会用`file!`和`line!`来打印，然后把`$val`做成`String`，用`{:#?}`来漂亮的打印`tmp`。所以对于我们的输入，它会这样写。

```text
[src/main.rs:2] vec![8, 9, 10] = [
    8,
    9,
    10,
]
```

剩下的部分，即使你多加了一个逗号，它也只是自己调用`dbg!`。

正如你所看到的，宏是非常复杂的！通常你只想让一个宏自动完成一些简单函数不能很好完成的事情。学习宏的最好方法是看其他宏的例子。没有多少人能够快速写出宏而不出问题。所以不要认为你需要知道宏的一切，才能知道如何在Rust中写。但如果你读了其他宏，并稍加修改，你就可以很容易地借用它们的力量。然后你可能会开始适应写自己的宏。

## 第2部分 - 电脑上的 Rust

你看到了，我们几乎可以使用Playground学习Rust中的任何东西。但如果你到目前为止已经学了这么多，现在你可能会想要在你的电脑上使用Rust。总有一些事情是你不能用Playground做的，比如使用文件或代码在多个文件中。其他如输入和flags也需要在电脑上安装Rust。但最重要的是，在你的电脑上有了Rust，你可以使用Crate。我们已经了解了crate，但在playground中你只能使用最流行的crate。但在你的电脑上，你可以在程序中使用任何crate。
