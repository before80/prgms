+++
title = "44-类型别名"
date = 2026-08-21T12:46:00+08:00
weight = 45
type = "docs"
description = "类型别名 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_43.html](https://dhghomon.github.io/easy_rust/Chapter_43.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 类型别名

类型别名的意思是 "给某个类型一个新的名字"。类型别名非常简单。通常，当您有一个很长的类型，而又不想每次都写它时，您就会使用它们。当您想给一个类型起一个更好的名字，便于记忆时，也可以使用它。下面是两个类型别名的例子。

这里是一个不难的类型，但是你想让你的代码更容易被其他人(或者你)理解。

```rust
type CharacterVec = Vec<char>;

fn main() {}
```


这是一种非常难读的类型:

```rust
// 这个返回类型非常长
fn returns<'a>(input: &'a Vec<char>) -> std::iter::Take<std::iter::Skip<std::slice::Iter<'a, char>>> {
    input.iter().skip(4).take(5)
}

fn main() {}
```

所以你可以改成这样。

```rust
type SkipFourTakeFive<'a> = std::iter::Take<std::iter::Skip<std::slice::Iter<'a, char>>>;

fn returns<'a>(input: &'a Vec<char>) -> SkipFourTakeFive {
    input.iter().skip(4).take(5)
}

fn main() {}
```

当然，你也可以导入元素，让类型更短:

```rust
use std::iter::{Take, Skip};
use std::slice::Iter;

fn returns<'a>(input: &'a Vec<char>) -> Take<Skip<Iter<'a, char>>> {
    input.iter().skip(4).take(5)
}

fn main() {}
```

所以你可以根据自己的喜好来决定在你的代码中什么是最好看的。

请注意，这并没有创建一个实际的新类型。它只是一个代替现有类型的名称。所以如果你写了 `type File = String;`，编译器只会看到 `String`。所以这将打印出 `true`。

```rust
type File = String;

fn main() {
    let my_file = File::from("I am file contents");
    let my_string = String::from("I am file contents");
    println!("{}", my_file == my_string);
}
```

那么如果你想要一个实际的新类型呢？

如果你想要一个新的文件类型，而编译器看到的是`File`，你可以把它放在一个结构中。

```rust
struct File(String); // File 是 String 的包装

fn main() {
    let my_file = File(String::from("I am file contents"));
    let my_string = String::from("I am file contents");
}
```

现在这样就不行了，因为它们是两种不同的类型。

```rust
struct File(String); // File 是 String 的包装

fn main() {
    let my_file = File(String::from("I am file contents"));
    let my_string = String::from("I am file contents");
    println!("{}", my_file == my_string);  // ⚠️ 不能比较 File 和 String
}
```

如果你想比较里面的String，可以用my_file.0:

```rust
struct File(String);

fn main() {
    let my_file = File(String::from("I am file contents"));
    let my_string = String::from("I am file contents");
    println!("{}", my_file.0 == my_string); // my_file.0 是 String，所以打印 true
}
```

## 在函数中导入和重命名

通常你会在程序的顶部写上`use`，像这样。

```rust
use std::cell::{Cell, RefCell};

fn main() {}
```

但我们看到，你可以在任何地方这样做，特别是在函数中使用名称较长的enum。下面是一个例子:

```rust
enum MapDirection {
    North,
    NorthEast,
    East,
    SouthEast,
    South,
    SouthWest,
    West,
    NorthWest,
}

fn main() {}

fn give_direction(direction: &MapDirection) {
    match direction {
        MapDirection::North => println!("You are heading north."),
        MapDirection::NorthEast => println!("You are heading northeast."),
        // 还有很多要打……
        // ⚠️ 因为我们没有写出所有可能的变体
    }
}
```

所以现在我们要在函数里面导入MapDirection。也就是说，在函数里面你可以直接写`North`等。

```rust
enum MapDirection {
    North,
    NorthEast,
    East,
    SouthEast,
    South,
    SouthWest,
    West,
    NorthWest,
}

fn main() {}

fn give_direction(direction: &MapDirection) {
    use MapDirection::*; // 导入 MapDirection 中的全部内容
    let m = "You are heading";

    match direction {
        North => println!("{} north.", m),
        NorthEast => println!("{} northeast.", m),
        // 这样好一点
        // ⚠️
    }
}
```

我们已经看到`::*`的意思是 "导入::之后的所有内容"。在我们的例子中，这意味着`North`，`NorthEast`......一直到`NorthWest`。当你导入别人的代码时，你也可以这样做，但如果代码非常大，你可能会有问题。如果它有一些元素和你的代码是一样的呢？所以一般情况下最好不要一直使用`::*`，除非你有把握。很多时候你在别人的代码里看到一个叫`prelude`的部分，里面有你可能需要的所有主要元素。那么你通常会这样使用:`name::prelude::*`。 我们将在 `modules` 和 `crates` 的章节中更多地讨论这个问题。

您也可以使用 `as` 来更改名称。例如，也许你正在使用别人的代码，而你不能改变枚举中的名称。

```rust
enum FileState {
    CannotAccessFile,
    FileOpenedAndReady,
    NoSuchFileExists,
    SimilarFileNameInNextDirectory,
}

fn main() {}
```

那么你就可以
1) 导入所有的东西
2) 更改名称

```rust
enum FileState {
    CannotAccessFile,
    FileOpenedAndReady,
    NoSuchFileExists,
    SimilarFileNameInNextDirectory,
}

fn give_filestate(input: &FileState) {
    use FileState::{
        CannotAccessFile as NoAccess,
        FileOpenedAndReady as Good,
        NoSuchFileExists as NoFile,
        SimilarFileNameInNextDirectory as OtherDirectory
    };
    match input {
        NoAccess => println!("Can't access file."),
        Good => println!("Here is your file"),
        NoFile => println!("Sorry, there is no file by that name."),
        OtherDirectory => println!("Please check the other directory."),
    }
}

fn main() {}
```

所以现在你可以写`OtherDirectory`而不是`FileState::SimilarFileNameInNextDirectory`。
