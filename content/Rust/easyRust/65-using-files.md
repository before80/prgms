+++
title = "65-使用文件"
date = 2026-08-21T12:46:00+08:00
weight = 66
type = "docs"
description = "使用文件 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_64.html](https://dhghomon.github.io/easy_rust/Chapter_64.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 使用文件

现在我们在电脑上使用Rust，我们可以开始处理文件了。你会注意到，现在我们会开始在代码中越来越多的看到`Result`。这是因为一旦你开始处理文件和类似的事情，很多事情都会出错。一个文件可能不在那里，或者计算机无法读取它。

你可能还记得，如果你想使用`?`运算符，调用它的函数必须返回一个`Result`。如果你记不住错误类型，你可以什么都不给它，让编译器告诉你。让我们用一个试图用`.parse()`创建一个数字的函数来试试。

```rust
// ⚠️
fn give_number(input: &str) -> Result<i32, ()> {
    input.parse::<i32>()
}

fn main() {
    println!("{:?}", give_number("88"));
    println!("{:?}", give_number("5"));
}
```

编译器告诉我们到底该怎么做。

```text
error[E0308]: mismatched types
 --> src\main.rs:4:5
  |
3 | fn give_number(input: &str) -> Result<i32, ()> {
  |                                --------------- expected `std::result::Result<i32, ()>` because of return type
4 |     input.parse::<i32>()
  |     ^^^^^^^^^^^^^^^^^^^^ expected `()`, found struct `std::num::ParseIntError`
  |
  = note: expected enum `std::result::Result<_, ()>`
             found enum `std::result::Result<_, std::num::ParseIntError>`
```

很好! 所以我们只要把返回值改成编译器说的就可以了:

```rust
use std::num::ParseIntError;

fn give_number(input: &str) -> Result<i32, ParseIntError> {
    input.parse::<i32>()
}

fn main() {
    println!("{:?}", give_number("88"));
    println!("{:?}", give_number("5"));
}
```

现在程序可以运行了!

```text
Ok(88)
Ok(5)
```

所以现在我们想用`?`，如果能用就直接给我们数值，如果不能用就给错误。但是如何在`fn main()`中做到这一点呢？如果我们尝试在main中使用`?`，那就不行了。

```rust
// ⚠️
use std::num::ParseIntError;

fn give_number(input: &str) -> Result<i32, ParseIntError> {
    input.parse::<i32>()
}

fn main() {
    println!("{:?}", give_number("88")?);
    println!("{:?}", give_number("5")?);
}
```

它说:

```text
error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option` (or another type that implements `std::ops::Try`)
  --> src\main.rs:8:22
   |
7  | / fn main() {
8  | |     println!("{:?}", give_number("88")?);
   | |                      ^^^^^^^^^^^^^^^^^^ cannot use the `?` operator in a function that returns `()`
9  | |     println!("{:?}", give_number("5")?);
10 | | }
   | |_- this function should return `Result` or `Option` to accept `?`
```

但实际上`main()`可以返回一个`Result`，就像其他函数一样。如果我们的函数能工作，我们不想返回任何东西(main()并没有给其他任何东西)。而如果它不工作，我们将错误返回。所以我们可以这样写:

```rust
use std::num::ParseIntError;

fn give_number(input: &str) -> Result<i32, ParseIntError> {
    input.parse::<i32>()
}

fn main() -> Result<(), ParseIntError> {
    println!("{:?}", give_number("88")?);
    println!("{:?}", give_number("5")?);
    Ok(())
}
```

不要忘了最后的`Ok(())`:这在Rust中是很常见的，它的意思是`Ok`，里面是`()`，也就是我们的返回值。现在它打印出来了:

```text
88
5
```


只用`.parse()`的时候不是很有用，但是用文件就很有用。这是因为`?`也为我们改变了错误类型。下面是用简单英语写的[?运算符页面](https://doc.rust-lang.org/std/macro.try.html):

```text
If you get an `Err`, it will get the inner error. Then `?` does a conversion using `From`. With that it can change specialized errors to more general ones. The error it gets is then returned.
```

另外，Rust在使用`File`s和类似的东西时，有一个方便的`Result`类型。它叫做`std::io::Result`，当你在使用`?`对文件进行打开和操作时，通常在`main()`中看到的就是这个。这其实是一个类型别名。它的样子是这样的:

```text
type Result<T> = Result<T, Error>;
```

所以这是一个`Result<T, Error>`，但我们只需要写出`Result<T>`部分。

现在让我们第一次尝试使用文件。`std::fs`是处理文件的方法所在，有了`std::io::Write`，你就可以写。有了它，我们就可以用`.write_all()`来写进文件。

```rust
use std::fs;
use std::io::Write;

fn main() -> std::io::Result<()> {
    let mut file = fs::File::create("myfilename.txt")?; // 用这个名字创建文件。
                                                        // 小心！如果已有同名文件，
                                                        // 里面的内容会被清空。
    file.write_all(b"Let's put this in the file")?;     // 别忘了 " 前面的 b。因为文件要的是字节。
    Ok(())
}
```

然后如果你打开新文件`myfilename.txt`，会看到内容`Let's put this in the file`。

不过我们不需要写两行，因为我们有`?`操作符。如果有效，它就会传递我们想要的结果，有点像在迭代器上很多方法一样。这时候`?`就变得非常方便了。

```rust
use std::fs;
use std::io::Write;

fn main() -> std::io::Result<()> {
    fs::File::create("myfilename.txt")?.write_all(b"Let's put this in the file")?;
    Ok(())
}
```

所以这是说 "请尝试创建一个文件，然后检查是否成功。如果成功了，那就使用`.write_all()`，然后检查是否成功。"

而事实上，也有一个函数可以同时做这两件事。它叫做`std::fs::write`。在它里面，你给它你想要的文件名，以及你想放在里面的内容。再次强调，要小心! 如果该文件已经存在，它将删除其中的所有内容。另外，它允许你写一个`&str`，前面不写`b`，因为这个:

```rust
pub fn write<P: AsRef<Path>, C: AsRef<[u8]>>(path: P, contents: C) -> Result<()>
```

`AsRef<[u8]>`就是为什么你可以给它任何一个。

很简单的:

```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("calvin_with_dad.txt", 
"Calvin: Dad, how come old photographs are always black and white? Didn't they have color film back then?
Dad: Sure they did. In fact, those photographs *are* in color. It's just the *world* was black and white then.
Calvin: Really?
Dad: Yep. The world didn't turn color until sometimes in the 1930s...")?;

    Ok(())
}
```

所以这就是我们要用的文件。这是一个名叫Calvin的漫画人物和他爸爸的对话，他爸爸对他的问题并不认真。有了这个，每次我们都可以创建一个文件来使用。



打开一个文件和创建一个文件一样简单。你只要用`open()`代替`create()`就可以了。之后(如果它找到了你的文件)，你就可以做`read_to_string()`这样的事情。要做到这一点，你可以创建一个可变的 `String`，然后把文件读到那里。它看起来像这样:

```rust
use std::fs;
use std::fs::File;
use std::io::Read; // 为了使用 .read_to_string()

fn main() -> std::io::Result<()> {
     fs::write("calvin_with_dad.txt", 
"Calvin: Dad, how come old photographs are always black and white? Didn't they have color film back then?
Dad: Sure they did. In fact, those photographs *are* in color. It's just the *world* was black and white then.
Calvin: Really?
Dad: Yep. The world didn't turn color until sometimes in the 1930s...")?;


    let mut calvin_file = File::open("calvin_with_dad.txt")?; // 打开刚创建的文件
    let mut calvin_string = String::new(); // 用这个 String 来装内容
    calvin_file.read_to_string(&mut calvin_string)?; // 把文件读进去

    calvin_string.split_whitespace().for_each(|word| print!("{} ", word.to_uppercase())); // 现在可以对 String 做操作了

    Ok(())
}
```

会打印:

```rust
CALVIN: DAD, HOW COME OLD PHOTOGRAPHS ARE ALWAYS BLACK AND WHITE? DIDN'T THEY HAVE COLOR FILM BACK THEN? DAD: SURE THEY DID. IN 
FACT, THOSE PHOTOGRAPHS *ARE* IN COLOR. IT'S JUST THE *WORLD* WAS BLACK AND WHITE THEN. CALVIN: REALLY? DAD: YEP. THE WORLD DIDN'T TURN COLOR UNTIL SOMETIMES IN THE 1930S...
```

好吧，如果我们想创建一个文件，但如果已经有另一个同名的文件就不做了怎么办？也许你不想为了创建一个新的文件而删除已经存在的其他文件。要做到这一点，有一个结构叫`OpenOptions`。其实，我们一直在用`OpenOptions`，却不知道。看看`File::open`的源码吧。

```rust
pub fn open<P: AsRef<Path>>(path: P) -> io::Result<File> {
        OpenOptions::new().read(true).open(path.as_ref())
    }
```

有意思，这好像是我们学过的建造者模式。`File::create`也是如此。

```rust
pub fn create<P: AsRef<Path>>(path: P) -> io::Result<File> {
        OpenOptions::new().write(true).create(true).truncate(true).open(path.as_ref())
    }
```

如果你去[OpenOptions的页面](https://doc.rust-lang.org/std/fs/struct.OpenOptions.html)，你可以看到所有可以选择的方法。大多数采取`bool`。


- `append()`: 意思是 "添加到已经存在的内容中，而不是删除"。
- `create()`: 这让 `OpenOptions` 创建一个文件。
- `create_new()`: 意思是只有在文件不存在的情况下才会创建文件。
- `read()`: 如果你想让它读取文件，就把这个设置为 `true`。
- `truncate()`: 如果你想在打开文件时把文件内容剪为0(删除内容)，就把这个设置为true。
- `write()`: 这可以让它写入一个文件。

然后在最后你用`.open()`加上文件名，就会得到一个`Result`。我们来看一个例子。

```rust
// ⚠️
use std::fs;
use std::fs::OpenOptions;

fn main() -> std::io::Result<()> {
     fs::write("calvin_with_dad.txt", 
"Calvin: Dad, how come old photographs are always black and white? Didn't they have color film back then?
Dad: Sure they did. In fact, those photographs *are* in color. It's just the *world* was black and white then.
Calvin: Really?
Dad: Yep. The world didn't turn color until sometimes in the 1930s...")?;

    let calvin_file = OpenOptions::new().write(true).create_new(true).open("calvin_with_dad.txt")?;

    Ok(())
}
```

首先我们用`new`做了一个`OpenOptions`(总是以`new`开头)。然后我们给它的能力是`write`。之后我们把`create_new()`设置为`true`，然后试着打开我们做的文件。打不开，这是我们想要的。

```text
Error: Os { code: 80, kind: AlreadyExists, message: "The file exists." }
```

让我们尝试使用`.append()`，这样我们就可以向一个文件写入。为了写入文件，我们可以使用 `.write_all()`，这是一个尝试写入你给它的一切内容的方法。

另外，我们将使用 `write!` 宏来做同样的事情。你会记得这个宏，我们在为结构体做`impl Display`的时候用到过。这次我们是在文件上使用它，而不是在缓冲区上。

```rust
use std::fs;
use std::fs::OpenOptions;
use std::io::Write;

fn main() -> std::io::Result<()> {
    fs::write("calvin_with_dad.txt", 
"Calvin: Dad, how come old photographs are always black and white? Didn't they have color film back then?
Dad: Sure they did. In fact, those photographs *are* in color. It's just the *world* was black and white then.
Calvin: Really?
Dad: Yep. The world didn't turn color until sometimes in the 1930s...")?;

    let mut calvin_file = OpenOptions::new()
        .append(true) // 现在可以写入而不删除原有内容
        .read(true)
        .open("calvin_with_dad.txt")?;
    calvin_file.write_all(b"And it was a pretty grainy color for a while too.\n")?;
    write!(&mut calvin_file, "That's really weird.\n")?;
    write!(&mut calvin_file, "Well, truth is stranger than fiction.")?;

    println!("{}", fs::read_to_string("calvin_with_dad.txt")?);

    Ok(())
}
```

这个打印:

```text
Calvin: Dad, how come old photographs are always black and white? Didn't they have color film back then?
Dad: Sure they did. In fact, those photographs *are* in color. It's just the *world* was black and white then.
Calvin: Really?
Dad: Yep. The world didn't turn color until sometimes in the 1930s...And it was a pretty grainy color for a while too.
That's really weird.
Well, truth is stranger than fiction.
```
