+++
title = "61-标准库之旅"
date = 2026-08-21T12:46:00+08:00
weight = 62
type = "docs"
description = "标准库之旅 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_60.html](https://dhghomon.github.io/easy_rust/Chapter_60.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 标准库之旅

现在你已经知道了很多Rust的知识，你将能够理解标准库里面的大部分东西。它里面的代码已经不是那么可怕了。让我们来看看它里面一些我们还没有学过的部分。本篇游记将介绍标准库的大部分部分，你不需要安装Rust。我们将重温很多我们已经知道的内容，这样我们就可以更深入地学习它们。

## 数组

关于数组需要注意的一点是，它们没有实现`Iterator.`。这意味着，如果你有一个数组，你不能使用`for`。但是你可以对它们使用 `.iter()` 这样的方法。或者你可以使用`&`来得到一个切片。实际上，如果你尝试使用`for`，编译器会准确地告诉你。

```rust
fn main() {
    // ⚠️
    let my_cities = ["Beirut", "Tel Aviv", "Nicosia"];

    for city in my_cities {
        println!("{}", city);
    }
}
```

消息是:

```text
error[E0277]: `[&str; 3]` is not an iterator
 --> src\main.rs:5:17
  |
  |                 ^^^^^^^^^ borrow the array with `&` or call `.iter()` on it to iterate over it
```

所以让我们试试这两种方法。它们的结果是一样的。

```rust
fn main() {
    let my_cities = ["Beirut", "Tel Aviv", "Nicosia"];

    for city in &my_cities {
        println!("{}", city);
    }
    for city in my_cities.iter() {
        println!("{}", city);
    }
}
```

这个打印:

```text
Beirut
Tel Aviv
Nicosia
Beirut
Tel Aviv
Nicosia
```



如果你想从一个数组中获取变量，你可以把它们的名字放在 `[]` 中来解构它。这与在 `match` 语句中使用元组或从结构体中获取变量是一样的。

```rust
fn main() {
    let my_cities = ["Beirut", "Tel Aviv", "Nicosia"];
    let [city1, city2, city3] = my_cities;
    println!("{}", city1);
}
```

打印出`Beirut`.

## char

您可以使用`.escape_unicode()`的方法来获取`char`的Unicode号码。

```rust
fn main() {
    let korean_word = "청춘예찬";
    for character in korean_word.chars() {
        print!("{} ", character.escape_unicode());
    }
}
```


这将打印出 `u{ccad} u{cd98} u{c608} u{cc2c}`。


你可以使用 `From` trait从 `u8` 中得到一个字符，但对于 `u32`，你使用 `TryFrom`，因为它可能无法工作。`u32`中的数字比Unicode中的字符多很多。我们可以通过一个简单的演示来了解。

```rust
use std::convert::TryFrom; // 要用 TryFrom 得先引入
use rand::prelude::*;      // 也会用到随机数

fn main() {
    let some_character = char::from(99); // 这个很简单 — 不需要 TryFrom
    println!("{}", some_character);

    let mut random_generator = rand::thread_rng();
    // 会尝试 40,000 次，从 u32 做成 char。
    // 范围是 0（std::u32::MIN）到 u32 最大值（std::u32::MAX）。失败就用 '-'。
    for _ in 0..40_000 {
        let bigger_character = char::try_from(random_generator.gen_range(std::u32::MIN..std::u32::MAX)).unwrap_or('-');
        print!("{}", bigger_character)
    }
}
```

几乎每次都会生成一个`-`。这是你会看到的那种输出的一部分。

```text
------------------------------------------------------------------------𤒰---------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-------------------------------------------------------------춗--------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
------------򇍜----------------------------------------------------
```

所以，你要用`TryFrom`是件好事。

另外，从2020年8月底开始，你现在可以从`char`中得到一个`String`。(`String`实现了`From<char>`)只要写`String::from()`，然后在里面放一个`char`。


## 整数

这些类型的数学方法有很多，另外还有一些其他的方法。下面是一些最有用的。



`.checked_add()`, `.checked_sub()`, `.checked_mul()`, `.checked_div()`. 如果你认为你可能会得到一个不适合类型的数字，这些都是不错的方法。它们会返回一个 `Option`，这样你就可以安全地检查你的数学计算是否正常，而不会让程序崩溃。

```rust
fn main() {
    let some_number = 200_u8;
    let other_number = 200_u8;

    println!("{:?}", some_number.checked_add(other_number));
    println!("{:?}", some_number.checked_add(1));
}
```

这个打印:

```text
None
Some(201)
```


你会注意到，在整数的页面上，经常说`rhs`。这意味着 "右边"，也就是你做一些数学运算时的右操作数。比如在`5 + 6`中，`5`在左边，`6`在右边，所以`6`就是`rhs`。这个不是关键词，但是你会经常看到，所以知道就好。

说到这里，我们来学习一下如何实现`Add`。在你实现了`Add`之后，你可以在你创建的类型上使用`+`。你需要自己实现`Add`，因为add可以表达很多意思。这是标准库页面中的例子。

```rust
use std::ops::Add; // 先引入 Add

#[derive(Debug, Copy, Clone, PartialEq)] // 这里大概最重要的是 PartialEq。你需要能比较数字
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Self; // 记住，这叫「关联类型」：「配套在一起的类型」。
                        // 这里就是另一个 Point

    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}
```

现在让我们为自己的类型实现`Add`。让我们想象一下，我们想把两个国家加在一起，这样我们就可以比较它们的经济。它看起来像这样:

```rust
use std::fmt;
use std::ops::Add;

#[derive(Clone)]
struct Country {
    name: String,
    population: u32,
    gdp: u32, // 这是经济规模
}

impl Country {
    fn new(name: &str, population: u32, gdp: u32) -> Self {
        Self {
            name: name.to_string(),
            population,
            gdp,
        }
    }
}

impl Add for Country {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self {
            name: format!("{} and {}", self.name, other.name), // 把名字拼在一起，
            population: self.population + other.population, // 人口相加，
            gdp: self.gdp + other.gdp,   // GDP 相加
        }
    }
}

impl fmt::Display for Country {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "In {} are {} people and a GDP of ${}", // 然后用 {} 就能全部打印
            self.name, self.population, self.gdp
        )
    }
}

fn main() {
    let nauru = Country::new("Nauru", 10_670, 160_000_000);
    let vanuatu = Country::new("Vanuatu", 307_815, 820_000_000);
    let micronesia = Country::new("Micronesia", 104_468, 367_000_000);

    // 名字本可以用 &str 而不是 String。但那样到处都要写生命周期
    // 对小例子太重了。调用 println! 时 clone 一下更合适。
    println!("{}", nauru.clone());
    println!("{}", nauru.clone() + vanuatu.clone());
    println!("{}", nauru + vanuatu + micronesia);
}
```

这个打印:

```text
In Nauru are 10670 people and a GDP of $160000000
In Nauru and Vanuatu are 318485 people and a GDP of $980000000
In Nauru and Vanuatu and Micronesia are 422953 people and a GDP of $1347000000
```

以后在这段代码中，我们可以把`.fmt()`改成更容易阅读的数字显示。

另外三个叫`Sub`、`Mul`和`Div`，实现起来基本一样。`+=`、`-=`、`*=`和`/=`，只要加上`Assign`:`AddAssign`、`SubAssign`、`MulAssign`和`DivAssign`即可。你可以看到完整的列表[这里](https://doc.rust-lang.org/std/ops/index.html#structs)，因为还有很多。例如 `%` 被称为 `Rem`, `-` 被称为 `Neg`, 等等。


## 浮点数

`f32`和`f64`有非常多的方法，你在做数学计算的时候会用到。我们不看这些，但这里有一些你可能会用到的方法。它们分别是 `.floor()`, `.ceil()`, `.round()`, 和 `.trunc()`. 所有这些方法都返回一个 `f32` 或 `f64`，它像一个整数，小数点后面是 `0`。它们是这样做的。

- `.floor()`: 给你下一个最低的整数.
- `.ceil()`: 给你下一个最高的整数。
- `.round()`: 如果小数部分大于等于0.5，返回数值加1;如果小数部分小于0.5，返回相同数值。这就是所谓的四舍五入，因为它给你一个 "舍入"的数字(一个数字的简短形式)。
- `.trunc()`:只是把小数点号后的部分截掉。Truncate是 "截断"的意思。

这里有一个简单的函数来打印它们。

```rust
fn four_operations(input: f64) {
    println!(
"For the number {}:
floor: {}
ceiling: {}
rounded: {}
truncated: {}\n",
        input,
        input.floor(),
        input.ceil(),
        input.round(),
        input.trunc()
    );
}

fn main() {
    four_operations(9.1);
    four_operations(100.7);
    four_operations(-1.1);
    four_operations(-19.9);
}
```

这个打印:

```text
For the number 9.1:
floor: 9
ceiling: 10
rounded: 9 // 因为小于 9.5
truncated: 9

For the number 100.7:
floor: 100
ceiling: 101
rounded: 101 // 因为大于 100.5
truncated: 100

For the number -1.1:
floor: -2
ceiling: -1
rounded: -1
truncated: -1

For the number -19.9:
floor: -20
ceiling: -19
rounded: -20
truncated: -19
```

`f32` 和 `f64` 有一个叫做 `.max()` 和 `.min()` 的方法，可以得到两个数字中较大或较小的数字。(对于其他类型，你可以直接使用`std::cmp::max`和`std::cmp::min`。)下面是用`.fold()`来得到最高或最低数的方法。你又可以看到，`.fold()`不仅仅是用来加数字的。

```rust
fn main() {
    let my_vec = vec![8.0_f64, 7.6, 9.4, 10.0, 22.0, 77.345, 10.22, 3.2, -7.77, -10.0];
    let maximum = my_vec.iter().fold(f64::MIN, |current_number, next_number| current_number.max(*next_number)); // 注意：从 f64 能表示的最小数开始。
    let minimum = my_vec.iter().fold(f64::MAX, |current_number, next_number| current_number.min(*next_number)); // 这里从最大可能数开始
    println!("{}, {}", maximum, minimum);
}
```

## bool

在 Rust 中，如果你愿意，你可以把 `bool` 变成一个整数，因为这样做是安全的。但你不能反过来做。如你所见，`true`变成了1，`false`变成了0。

```rust
fn main() {
    let true_false = (true, false);
    println!("{} {}", true_false.0 as u8, true_false.1 as i32);
}
```

这将打印出`1 0`。如果你告诉编译器类型，也可以使用 `.into()`。

```rust
fn main() {
    let true_false: (i128, u16) = (true.into(), false.into());
    println!("{} {}", true_false.0, true_false.1);
}
```

这打印的是一样的东西。

从Rust 1.50(2021年2月发布)开始，有一个叫做 `then()`的方法，它将一个 `bool`变成一个 `Option`。使用`then()`时需要一个闭包，如果item是`true`，闭包就会被调用。同时，无论从闭包中返回什么，都会进入`Option`中。下面是一个小例子:

```rust
fn main() {

    let (tru, fals) = (true.then(|| 8), false.then(|| 8));
    println!("{:?}, {:?}", tru, fals);
}
```

这个打印 `Some(8), None`。

下面是一个较长的例子:

```rust
fn main() {
    let bool_vec = vec![true, false, true, false, false];

    let option_vec = bool_vec
        .iter()
        .map(|item| {
            item.then(|| { // 放进 map 里以便继续传下去
                println!("Got a {}!", item);
                "It's true, you know" // 为 true 时放进 Some
                                      // 否则原样传出 None
            })
        })
        .collect::<Vec<_>>();

    println!("Now we have: {:?}", option_vec);

    // 那样会把 None 也打印出来。用 filter_map 滤掉，放进新 Vec。
    let filtered_vec = option_vec.into_iter().filter_map(|c| c).collect::<Vec<_>>();

    println!("And without the Nones: {:?}", filtered_vec);
}
```

将打印:

```text
Got a true!
Got a true!
Now we have: [Some("It\'s true, you know"), None, Some("It\'s true, you know"), None, None]
And without the Nones: ["It\'s true, you know", "It\'s true, you know"]
```

## Vec

Vec有很多方法我们还没有看。先说说`.sort()`。`.sort()`一点都不奇怪。它使用`&mut self`来对一个向量进行排序。

```rust
fn main() {
    let mut my_vec = vec![100, 90, 80, 0, 0, 0, 0, 0];
    my_vec.sort();
    println!("{:?}", my_vec);
}
```

这样打印出来的是`[0, 0, 0, 0, 0, 80, 90, 100]`。但还有一种更有趣的排序方式叫`.sort_unstable()`，它通常更快。它之所以更快，是因为它不在乎排序前后相同数字的先后顺序。在常规的`.sort()`中，你知道最后的`0, 0, 0, 0, 0`会在`.sort()`之后的顺序相同。但是`.sort_unstable()`可能会把最后一个0移到索引0，然后把第三个最后的0移到索引2，等等。


`.dedup()`的意思是 "去重复"。它将删除一个向量中相同的元素，但只有当它们彼此相邻时才会删除。接下来这段代码不会只打印`"sun", "moon"`。

```rust
fn main() {
    let mut my_vec = vec!["sun", "sun", "moon", "moon", "sun", "moon", "moon"];
    my_vec.dedup();
    println!("{:?}", my_vec);
}
```


它只是把另一个 "sun"旁边的 "sun"去掉，然后把一个 "moon"旁边的 "moon"去掉，再把另一个 "moon"旁边的 "moon"去掉。结果是 `["sun", "moon", "sun", "moon"]`.

如果你想把每个重复的东西都去掉，就先`.sort()`:

```rust
fn main() {
    let mut my_vec = vec!["sun", "sun", "moon", "moon", "sun", "moon", "moon"];
    my_vec.sort();
    my_vec.dedup();
    println!("{:?}", my_vec);
}
```

结果:`["moon", "sun"]`.


## String

你会记得，`String`有点像`Vec`。它很像`Vec`，你可以调用很多相同的方法。比如说，你可以用`String::with_capacity()`创建一个，如果你需要多次用`.push()`推一个`char`，或者用`.push_str()`推一个`&str`。下面是一个有多次内存分配的`String`的例子。

```rust
fn main() {
    let mut push_string = String::new();
    let mut capacity_counter = 0; // capacity 从 0 开始
    for _ in 0..100_000 { // 做 100,000 次
        if push_string.capacity() != capacity_counter { // 先检查 capacity 是否变了
            println!("{}", push_string.capacity()); // 变了就打印
            capacity_counter = push_string.capacity(); // 再更新计数器
        }
        push_string.push_str("I'm getting pushed into the string!"); // 每次都推进这段文字
    }
}
```

这个打印:

```text
35
70
140
280
560
1120
2240
4480
8960
17920
35840
71680
143360
286720
573440
1146880
2293760
4587520
```

我们不得不重新分配(把所有东西复制过来)18次。但既然我们知道了最终的容量，我们可以马上设置容量，不需要重新分配:只设置一次`String`容量就够了。

```rust
fn main() {
    let mut push_string = String::with_capacity(4587520); // 我们知道确切数字。别的大数字也可能行
    let mut capacity_counter = 0;
    for _ in 0..100_000 {
        if push_string.capacity() != capacity_counter {
            println!("{}", push_string.capacity());
            capacity_counter = push_string.capacity();
        }
        push_string.push_str("I'm getting pushed into the string!");
    }
}
```

而这个打印`4587520`。完美的! 我们再也不用分配了。

当然，实际长度肯定比这个小。如果你试了100001次，101000次等等，还是会说`4587520`。这是因为每次的容量都是之前的2倍。不过我们可以用`.shrink_to_fit()`来缩小它(和`Vec`一样)。我们的`String`已经非常大了，我们不想再给它增加任何东西，所以我们可以把它缩小一点。但是只有在你有把握的情况下才可以这样做:下面是原因。

```rust
fn main() {
    let mut push_string = String::with_capacity(4587520);
    let mut capacity_counter = 0;
    for _ in 0..100_000 {
        if push_string.capacity() != capacity_counter {
            println!("{}", push_string.capacity());
            capacity_counter = push_string.capacity();
        }
        push_string.push_str("I'm getting pushed into the string!");
    }
    push_string.shrink_to_fit();
    println!("{}", push_string.capacity());
    push_string.push('a');
    println!("{}", push_string.capacity());
    push_string.shrink_to_fit();
    println!("{}", push_string.capacity());
}
```

这个打印:

```text
4587520
3500000
7000000
3500001
```

所以首先我们的大小是`4587520`，但我们没有全部使用。我们用了`.shrink_to_fit()`，然后把大小降到了`3500000`。但是我们忘记了我们需要推上一个 `a`。当我们这样做的时候，Rust 看到我们需要更多的空间，给了我们双倍的空间:现在是 `7000000`。Whoops! 所以我们又调用了`.shrink_to_fit()`，现在又回到了`3500001`。

`.pop()`对`String`有用，就像对`Vec`一样。

```rust
fn main() {
    let mut my_string = String::from(".daer ot drah tib elttil a si gnirts sihT");
    loop {
        let pop_result = my_string.pop();
        match pop_result {
            Some(character) => print!("{}", character),
            None => break,
        }
    }
}
```

这打印的是`This string is a little bit hard to read.`，因为它是从最后一个字符开始的。

`.retain()`是一个使用闭包的方法，这对`String`来说是罕见的。就像在迭代器上的`.filter()`一样。

```rust
fn main() {
    let mut my_string = String::from("Age: 20 Height: 194 Weight: 80");
    my_string.retain(|character| character.is_alphabetic() || character == ' '); // 保留字母或空格
    dbg!(my_string); // 这次用 dbg!() 玩一下，不用 println!
}
```

这个打印:

```text
[src\main.rs:4] my_string = "Age  Height  Weight "
```


## OsString和CString

`std::ffi`是`std`的一部分，它帮助你将Rust与其他语言或操作系统一起使用。它有`OsString`和`CString`这样的类型，它们就像操作系统的`String`或语言C的`String`一样，它们各自也有自己的`&str`类型:`OsStr`和`CStr`。`ffi`的意思是 "foreign function interface"(外部函数接口)。

当你必须与一个没有Unicode的操作系统一起工作时，你可以使用`OsString`。所有的Rust字符串都是unicode，但不是每个操作系统支持。下面是标准库中关于为什么我们有`OsString`的简单英文解释。

- Unix系统(Linux等)上的字符串可能是很多没有0的字节组合在一起。而且有时你会把它们读成Unicode UTF-8。
- Windows上的字符串可能是由随机的16位值组成的，没有0。有时你会把它们读成Unicode UTF-16。
- 在Rust中，字符串总是有效的UTF-8，其中可能包含0。

所以，`OsString`被设计为支持它们读取。

你可以用一个`OsString`做所有常规的事情，比如`OsString::from("Write something here")`。它还有一个有趣的方法，叫做 `.into_string()`，试图把自己变成一个常规的 `String`。它返回一个 `Result`，但 `Err` 部分只是原来的 `OsString`。

```rust
// 🚧
pub fn into_string(self) -> Result<String, OsString>
```

所以如果不行的话，那你就把它找回来。你不能调用`.unwrap()`，因为它会崩溃，但是你可以使用`match`来找回`OsString`。我们通过调用不存在的方法来测试一下。

```rust
use std::ffi::OsString;

fn main() {
    // ⚠️
    let os_string = OsString::from("This string works for your OS too.");
    match os_string.into_string() {
        Ok(valid) => valid.thth(),           // 编译器：".thth() 是什么？？"
        Err(not_valid) => not_valid.occg(),  // 编译器：".occg() 是什么？？"
    }
}
```

然后编译器准确地告诉我们我们想知道的东西。

```text
error[E0599]: no method named `thth` found for struct `std::string::String` in the current scope
 --> src/main.rs:6:28
  |
6 |         Ok(valid) => valid.thth(),
  |                            ^^^^ method not found in `std::string::String`

error[E0599]: no method named `occg` found for struct `std::ffi::OsString` in the current scope
 --> src/main.rs:7:37
  |
7 |         Err(not_valid) => not_valid.occg(),
  |                                     ^^^^ method not found in `std::ffi::OsString`
```

我们可以看到，`valid`的类型是`String`，`not_valid`的类型是`OsString`。

## Mem

`std::mem`有一些非常有趣的方法。我们已经看到了一些，比如`.size_of()`、`.size_of_val()`和`.drop()`。


```rust
use std::mem;

fn main() {
    println!("{}", mem::size_of::<i32>());
    let my_array = [8; 50];
    println!("{}", mem::size_of_val(&my_array));
    let mut some_string = String::from("You can drop a String because it's on the heap");
    mem::drop(some_string);
    // some_string.clear();   如果这样做会 panic
}
```

这个打印:

```text
4
200
```

下面是`mem`中的一些其他方法。

`swap()`: 用这个方法你可以交换两个变量之间的值。你可以通过为每个变量创建一个可变引用来做。当你有两个东西想交换，而Rust因为借用规则不让你交换时，这很有帮助。或者只是当你想快速切换两个东西的时候。

这里有一个例子。

```rust
use std::{mem, fmt};

struct Ring { // 创建一个《指环王》里的戒指
    owner: String,
    former_owner: String,
    seeker: String, // seeker 意思是「寻找它的人」
}

impl Ring {
    fn new(owner: &str, former_owner: &str, seeker: &str) -> Self {
        Self {
            owner: owner.to_string(),
            former_owner: former_owner.to_string(),
            seeker: seeker.to_string(),
        }
    }
}

impl fmt::Display for Ring { // 用 Display 显示谁持有、谁在找
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "{} has the ring, {} used to have it, and {} wants it", self.owner, self.former_owner, self.seeker)
        }
}

fn main() {
    let mut one_ring = Ring::new("Frodo", "Gollum", "Sauron");
    println!("{}", one_ring);
    mem::swap(&mut one_ring.owner, &mut one_ring.former_owner); // 咕噜暂时又拿到了戒指
    println!("{}", one_ring);
}
```

这将打印:

```text
Frodo has the ring, Gollum used to have it, and Sauron wants it
Gollum has the ring, Frodo used to have it, and Sauron wants it
```

`replace()`:这个就像swap一样，其实里面也用了swap，你可以看到。

```rust
pub fn replace<T>(dest: &mut T, mut src: T) -> T {
    swap(dest, &mut src);
    src
}
```

所以它只是做了一个交换，然后返回另一个元素。有了这个，你就用你放进去的其他东西来替换这个值。因为它返回的是旧的值，所以你应该用`let`来使用它。下面是一个简单的例子。

```rust
use std::mem;

struct City {
    name: String,
}

impl City {
    fn change_name(&mut self, name: &str) {
        let old_name = mem::replace(&mut self.name, name.to_string());
        println!(
            "The city once called {} is now called {}.",
            old_name, self.name
        );
    }
}

fn main() {
    let mut capital_city = City {
        name: "Constantinople".to_string(),
    };
    capital_city.change_name("Istanbul");
}
```

这样就会打印出`The city once called Constantinople is now called Istanbul.`。

有一个函数叫`.take()`，和`.replace()`一样，但它在元素中留下了默认值。
 你会记得，默认值通常是0、""之类的东西。这里是签名。

```rust
// 🚧
pub fn take<T>(dest: &mut T) -> T
where
    T: Default,
```

所以你可以做这样的事情。

```rust
use std::mem;

fn main() {
    let mut number_vec = vec![8, 7, 0, 2, 49, 9999];
    let mut new_vec = vec![];

    number_vec.iter_mut().for_each(|number| {
        let taker = mem::take(number);
        new_vec.push(taker);
    });

    println!("{:?}\n{:?}", number_vec, new_vec);
}
```

你可以看到，它将所有数字都替换为0:没有删除任何索引。

```text
[0, 0, 0, 0, 0, 0]
[8, 7, 0, 2, 49, 9999]
```


当然，对于你自己的类型，你可以把`Default`实现成任何你想要的类型。我们来看一个例子，我们有一个`Bank`和一个`Robber`。每次他抢了`Bank`，他就会在桌子上拿到钱。但是办公桌可以随时从后面拿钱，所以它永远有50。我们将为此自制一个类型，所以它将永远有50。下面是它的工作原理。

```rust
use std::mem;
use std::ops::{Deref, DerefMut}; // 用它获得 u32 的能力

struct Bank {
    money_inside: u32,
    money_at_desk: DeskMoney, // 这是我们的「智能指针」类型。有自己的 Default，但会用到 u32
}

struct DeskMoney(u32);

impl Default for DeskMoney {
    fn default() -> Self {
        Self(50) // 默认总是 50，不是 0
    }
}

impl Deref for DeskMoney { // 有了它就能用 * 访问 u32
    type Target = u32;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for DeskMoney { // 有了它就能加减等
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl Bank {
    fn check_money(&self) {
        println!(
            "There is ${} in the back and ${} at the desk.\n",
            self.money_inside, *self.money_at_desk // 用 *，这样只打印 u32
        );
    }
}

struct Robber {
    money_in_pocket: u32,
}

impl Robber {
    fn check_money(&self) {
        println!("The robber has ${} right now.\n", self.money_in_pocket);
    }

    fn rob_bank(&mut self, bank: &mut Bank) {
        let new_money = mem::take(&mut bank.money_at_desk); // 这里取走钱，留下 50，因为那是默认值
        self.money_in_pocket += *new_money; // 用 *，因为只能加 u32。DeskMoney 不能直接加
        bank.money_inside -= *new_money;    // 这里一样
        println!("She robbed the bank. She now has ${}!\n", self.money_in_pocket);
    }
}

fn main() {
    let mut bank_of_klezkavania = Bank { // 设立银行
        money_inside: 5000,
        money_at_desk: DeskMoney(50),
    };
    bank_of_klezkavania.check_money();

    let mut robber = Robber { // 设立强盗
        money_in_pocket: 50,
    };
    robber.check_money();

    robber.rob_bank(&mut bank_of_klezkavania); // 抢劫，再检查钱
    robber.check_money();
    bank_of_klezkavania.check_money();

    robber.rob_bank(&mut bank_of_klezkavania); // 再来一次
    robber.check_money();
    bank_of_klezkavania.check_money();

}
```

这将打印:

```text
There is $5000 in the back and $50 at the desk.

The robber has $50 right now.

She robbed the bank. She now has $100!

The robber has $100 right now.

There is $4950 in the back and $50 at the desk.

She robbed the bank. She now has $150!

The robber has $150 right now.

There is $4900 in the back and $50 at the desk.
```

你可以看到桌子上总是有50美元。


## Prelude

标准库也有一个prelude，这就是为什么你不用写`use std::vec::Vec`这样的东西来创建一个`Vec`。你可以[在这里](https://doc.rust-lang.org/std/prelude/index.html#prelude-contents)看到所有这些元素，并且大致了解:

- `std::marker::{Copy, Send, Sized, Sync, Unpin}`. 你以前没有见过`Unpin`，因为几乎每一种类型都会用到它(比如`Sized`，也很常见)。"Pin"的意思是不让东西动。在这种情况下，`Pin`意味着它在内存中不能移动，但大多数元素都有`Unpin`，所以你可以移动。这就是为什么像`std::mem::replace`这样的函数能用，因为它们没有被钉住。
- `std::ops::{Drop, Fn, FnMut, FnOnce}`.
- `std::mem::drop`
- `std::boxed::Box`.
- `std::borrow::ToOwned`. 你之前用`Cow`看到过一点，它可以把借来的内容变成自己的。它使用`.to_owned()`来实现这个功能。你也可以在`&str`上使用`.to_owned()`，得到一个`String`，对于其他借来的值也是一样。
- `std::clone::Clone`
- `std::cmp::{PartialEq, PartialOrd, Eq, Ord}`.
- `std::convert::{AsRef, AsMut, Into, From}`.
- `std::default::Default`.
- `std::iter::{Iterator, Extend, IntoIterator, DoubleEndedIterator, ExactSizeIterator}`. 我们之前用`.rev()`来做迭代器:这实际上是做了一个`DoubleEndedIterator`。`ExactSizeIterator`只是类似于`0..10`的东西:它已经知道自己的`.len()`是10。其他迭代器不知道它们的长度是肯定的。
- `std::option::Option::{self, Some, None}`.
- `std::result::Result::{self, Ok, Err}`.
- `std::string::{String, ToString}`.
- `std::vec::Vec`.

如果你因为某些原因不想要这个prelude怎么办？就加属性`#![no_implicit_prelude]`。我们来试一试，看编译器的抱怨。

```rust
// ⚠️
#![no_implicit_prelude]
fn main() {
    let my_vec = vec![8, 9, 10];
    let my_string = String::from("This won't work");
    println!("{:?}, {}", my_vec, my_string);
}
```

现在Rust根本不知道你想做什么。

```text
error: cannot find macro `println` in this scope
 --> src/main.rs:5:5
  |
5 |     println!("{:?}, {}", my_vec, my_string);
  |     ^^^^^^^

error: cannot find macro `vec` in this scope
 --> src/main.rs:3:18
  |
3 |     let my_vec = vec![8, 9, 10];
  |                  ^^^

error[E0433]: failed to resolve: use of undeclared type or module `String`
 --> src/main.rs:4:21
  |
4 |     let my_string = String::from("This won't work");
  |                     ^^^^^^ use of undeclared type or module `String`

error: aborting due to 3 previous errors
```

因此，对于这个简单的代码，你需要告诉Rust使用`extern`(外部)crate，叫做`std`，然后是你想要的元素。这里是我们要做的一切，只是为了创建一个Vec和一个String，并打印它。

```rust
#![no_implicit_prelude]

extern crate std; // 现在必须告诉 Rust 你要用名为 std 的 crate
use std::vec; // 需要 vec 宏
use std::string::String; // 以及 String
use std::convert::From; // 以及把 &str 转成 String
use std::println; // 以及用来打印

fn main() {
    let my_vec = vec![8, 9, 10];
    let my_string = String::from("This won't work");
    println!("{:?}, {}", my_vec, my_string);
}
```

现在终于成功了，打印出`[8, 9, 10], This won't work`。所以你可以明白为什么Rust要用prelude了。但如果你愿意，你不需要使用它。而且你甚至可以使用`#![no_std]`(我们曾经看到过)，用于你连堆栈内存这种东西都用不上的时候。但大多数时候，你根本不用考虑不用prelude或`std`。

那么为什么之前我们没有看到`extern`这个关键字呢？是因为你已经不需要它了。以前，当带入外部crate时，你必须使用它。所以以前要使用`rand`，你必须要写成:

```rust
extern crate rand;
```

然后用 `use` 语句来表示你想使用的修改、trait等。但现在Rust编译器已经不需要这些帮助了--你只需要使用`use`，rust就知道在哪里可以找到它。所以你几乎再也不需要`extern crate`了，但在其他人的Rust代码中，你可能仍然会在顶部看到它。



## Time

`std::time`是你可以找到时间函数的地方。(如果你想要更多的功能，`chrono`这样的crate也可以。)最简单的功能就是用`Instant::now()`获取系统时间即可。

```rust
use std::time::Instant;

fn main() {
    let time = Instant::now();
    println!("{:?}", time);
}
```

如果你打印出来，你会得到这样的东西。`Instant { tv_sec: 2738771, tv_nsec: 685628140 }`. 这说的是秒和纳秒，但用处不大。比如你看2738771秒(写于8月)，就是31.70天。这和月份、日子没有任何关系。但是`Instant`的页面告诉我们，它本身不应该有用。它说它是 "不透明的，只有和Duration一起才有用"。Opaque的意思是 "你搞不清楚"，而Duration的意思是 "过了多少时间"。所以它只有在做比较时间这样的事情时才有用。

如果你看左边的trait，其中一个是`Sub<Instant>`。也就是说我们可以用`-`来减去一个。而当我们点击[src]看它的作用时，页面显示：

```rust
impl Sub<Instant> for Instant {
    type Output = Duration;

    fn sub(self, other: Instant) -> Duration {
        self.duration_since(other)
    }
}
```

因此，它需要一个`Instant`，并使用`.duration_since()`给出一个`Duration`。让我们试着打印一下。我们将创建两个相邻的 `Instant::now()`，然后让程序忙活一会儿，再创建一个 `Instant::now()`。然后我们再创建一个`Instant::now()`. 最后，我们来看看用了多长时间。

```rust
use std::time::Instant;

fn main() {
    let time1 = Instant::now();
    let time2 = Instant::now(); // 这两个紧挨着

    let mut new_string = String::new();
    loop {
        new_string.push('წ'); // 让 Rust 把这个格鲁吉亚字母推进 String
        if new_string.len() > 100_000 { //  直到长度达到 100,000 字节
            break;
        }
    }
    let time3 = Instant::now();
    println!("{:?}", time2 - time1);
    println!("{:?}", time3 - time1);
}
```

这将打印出这样的东西。

```text
1.025µs
683.378µs
```

所以，这只是1微秒多与683毫秒。我们可以看到，Rust确实花了一些时间来做。

不过我们可以用一个`Instant`做一件有趣的事情。
 我们可以把它变成`String`与`format!("{:?}", Instant::now());`。它的样子是这样的:

```rust
use std::time::Instant;

fn main() {
    let time1 = format!("{:?}", Instant::now());
    println!("{}", time1);
}
```

这样就会打印出类似`Instant { tv_sec: 2740773, tv_nsec: 632821036 }`的东西。这是没有用的，但是如果我们使用 `.iter()` 和 `.rev()` 以及 `.skip(2)`，我们可以跳过最后的 `}` 和 ` `。我们可以用它来创建一个随机数发生器。

```rust
use std::time::Instant;

fn bad_random_number(digits: usize) {
    if digits > 9 {
        panic!("Random number can only be up to 9 digits");
    }
    let now = Instant::now();
    let output = format!("{:?}", now);

    output
        .chars()
        .rev()
        .skip(2)
        .take(digits)
        .for_each(|character| print!("{}", character));
    println!();
}

fn main() {
    bad_random_number(1);
    bad_random_number(1);
    bad_random_number(3);
    bad_random_number(3);
}
```

这样就会打印出类似这样的内容:

```text
6
4
967
180
```

这个函数被称为`bad_random_number`，因为它不是一个很好的随机数生成器。Rust有更好的crate，可以用比`rand`更少的代码创建随机数，比如`fastrand`。但这是一个很好的例子，你可以利用你的想象力用`Instant`来做一些事情。

当你有一个线程时，你可以使用`std::thread::sleep`使它停止一段时间。当你这样做时，你必须给它一个duration。你不必创建多个线程来做这件事，因为每个程序至少在一个线程上。`sleep`虽然需要一个`Duration`，所以它可以知道要睡多久。你可以这样选单位:`Duration::from_millis()`, `Duration::from_secs`, 等等。这里举一个例子:

```rust
use std::time::Duration;
use std::thread::sleep;

fn main() {
    let three_seconds = Duration::from_secs(3);
    println!("I must sleep now.");
    sleep(three_seconds);
    println!("Did I miss anything?");
}
```

这将只打印

```text
I must sleep now.
Did I miss anything?
```

但线程在三秒钟内什么也不做。当你有很多线程需要经常尝试一些事情时，比如连接，你通常会使用`.sleep()`。你不希望线程在一秒钟内使用你的处理器尝试10万次，而你只是想让它有时检查一下。所以，你就可以设置一个`Duration`，它就会在每次醒来的时候尝试做它的任务。


## 其他宏


我们再来看看其他一些宏。

`unreachable!()`

这个宏有点像`todo!()`，除了它是针对你永远不会用的代码。也许你在一个枚举中有一个`match`，你知道它永远不会选择其中的一个分支，所以代码永远无法达到那个分支。如果是这样，你可以写`unreachable!()`，这样编译器就知道可以忽略这部分。

例如，假设你有一个程序，当你选择一个地方居住时，它会写一些东西。在乌克兰，除了切尔诺贝利，其他地方都不错。你的程序不让任何人选择切尔诺贝利，因为它现在不是一个好地方。但是这个枚举是很早以前在别人的代码里做的，你无法更改。所以在`match`的分支中，你可以用这个宏。它是这样的:

```rust
enum UkrainePlaces {
    Kiev,
    Kharkiv,
    Chernobyl, // 假装不能改这个枚举 — Chernobyl 会一直在
    Odesa,
    Dnipro,
}

fn choose_city(place: &UkrainePlaces) {
    use UkrainePlaces::*;
    match place {
        Kiev => println!("You will live in Kiev"),
        Kharkiv => println!("You will live in Kharkiv"),
        Chernobyl => unreachable!(),
        Odesa => println!("You will live in Odesa"),
        Dnipro => println!("You will live in Dnipro"),
    }
}

fn main() {
    let user_input = UkrainePlaces::Kiev; // 假装用户输入来自别的函数。无论如何用户选不了 Chernobyl
    choose_city(&user_input);
}
```

这将打印出 `You will live in Kiev`。

`unreachable!()`对你来说也很好读，因为它提醒你代码的某些部分是不可访问的。不过你必须确定代码确实是不可访问的。如果编译器调用`unreachable!()`，程序就会崩溃。

此外，如果你曾经有不可达的代码，而编译器知道，它会告诉你。下面是一个简单的例子:

```rust
fn main() {
    let true_or_false = true;

    match true_or_false {
        true => println!("It's true"),
        false => println!("It's false"),
        true => println!("It's true"), // 糟糕，又写成 true 了
    }
}
```

它会说

```text
warning: unreachable pattern
 --> src/main.rs:7:9
  |
7 |         true => println!("It's true"),
  |         ^^^^
  |
```

但是`unreachable!()`是用于编译器无法知道的时候，就像我们另一个例子。



`column!`, `line!`, `file!`, `module_path!`

这四个宏有点像`dbg!()`，因为你只是把它们放进代码去给你调试信息。但是它们不需要任何变量--你只需要用它们和括号一起使用，而没有其他的东西。它们放到一起很容易学:

- `column!()`给你写的那一列
- `file!()`给你写的文件的名称
- `line!()`给你写的那行字，然后是
- `module_path!()`给你模块的位置。

接下来的代码在一个简单的例子中展示了这三者。我们将假装有更多的代码(mod里面的mod)，因为这就是我们要使用这些宏的原因。你可以想象一个大的Rust程序,它有许多mod和文件。

```rust
pub mod something {
    pub mod third_mod {
        pub fn print_a_country(input: &mut Vec<&str>) {
            println!(
                "The last country is {} inside the module {}",
                input.pop().unwrap(),
                module_path!()
            );
        }
    }
}

fn main() {
    use something::third_mod::*;
    let mut country_vec = vec!["Portugal", "Czechia", "Finland"];

    // 做点事情
    println!("Hello from file {}", file!());

    // 做点事情
    println!(
        "On line {} we got the country {}",
        line!(),
        country_vec.pop().unwrap()
    );

    // 再做点事情

    println!(
        "The next country is {} on line {} and column {}.",
        country_vec.pop().unwrap(),
        line!(),
        column!(),
    );

    // 还有很多代码

    print_a_country(&mut country_vec);
}
```

它打印的是这样的。

```text
Hello from file src/main.rs
On line 23 we got the country Finland
The next country is Czechia on line 32 and column 9.
The last country is Portugal inside the module rust_book::something::third_mod
```



`cfg!`

我们知道，你可以使用 `#[cfg(test)]` 和 `#[cfg(windows)]` 这样的属性来告诉编译器在某些情况下该怎么做。当你有`test`时，当你在测试模式下运行Rust时，它会运行代码(如果是在电脑上，你输入`cargo test`)。而当你使用`windows`时，如果用户使用的是Windows，它就会运行代码。但也许你只是想根据不同操作系统对依赖系统的代码做很小的修改。这时候这个宏就很有用了。它返回一个`bool`。

```rust
fn main() {
    let helpful_message = if cfg!(target_os = "windows") { "backslash" } else { "slash" };

    println!(
        "...then in your hard drive, type the directory name followed by a {}. Then you...",
        helpful_message
    );
}
```

这将以不同的方式打印，取决于你的系统。Rust Playground在Linux上运行，所以会打印:

```text
...then in your hard drive, type the directory name followed by a slash. Then you...
```

`cfg!()`适用于任何一种配置。下面是一个例子，当你在测试中使用一个函数时，它的运行方式会有所不同。

```rust
#[cfg(test)] // cfg! 会去找 test 这个词
mod testing {
    use super::*;
    #[test]
    fn check_if_five() {
        assert_eq!(bring_number(true), 5); // 这个 bring_number() 应返回 5
    }
}

fn bring_number(should_run: bool) -> u32 { // 这个函数用 bool 决定是否运行
    if cfg!(test) && should_run { // 若应运行且配置为 test，返回 5
        5
    } else if should_run { // 若不是测试但应运行，就打印点东西。跑测试时会忽略 println!
        println!("Returning 5. This is not a test");
        5
    } else {
        println!("This shouldn't run, returning 0."); // 否则返回 0
        0
    }
}

fn main() {
    bring_number(true);
    bring_number(false);
}
```

现在根据配置的不同，它的运行方式也会不同。如果你只是运行程序，它会给你这样的结果:

```text
Returning 5. This is not a test
This shouldn't run, returning 0.
```

但如果你在测试模式下运行它(`cargo test`，用于电脑上的Rust)，它实际上会运行测试。因为在这种情况下，测试总是返回5，所以它会通过。

```text
running 1 test
test testing::check_if_five ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```
