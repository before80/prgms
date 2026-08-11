+++
title = "3.2 数据类型"
date = 2026-08-05T08:44:00+08:00
weight = 11
type = "docs"
description = "标量类型与复合类型：整数、浮点、布尔、字符、元组与数组"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 数据类型 {#data-types}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch03-02-data-types.html](https://doc.rust-lang.org/stable/book/ch03-02-data-types.html)


## 数据类型 {#data-types-heading}

　　Rust 中的每个值都属于某种*数据类型*（data type），它告诉 Rust 正在指定哪一类数据，从而知道如何处理这些数据。我们将看两个数据类型子集：标量（scalar）与复合（compound）。

　　请记住，Rust 是*静态类型*（statically typed）语言，这意味着它必须在编译期知道所有变量的类型。编译器通常能根据值以及我们如何使用它来推断我们想用的类型。在可能有多种类型时，例如在第 2 章[「比较猜测与秘密数字」][comparing-the-guess-to-the-secret-number]一节中我们用 `parse` 把 `String` 转换成数字类型时，就必须添加类型标注，像这样：

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

　　若我们不加前面代码中所示的 `: u32` 类型标注，Rust 会显示如下错误，意味着编译器需要我们提供更多信息才能知道我们想用哪种类型：

```console
$ cargo build
   Compiling no_type_annotations v0.1.0 (file:///projects/no_type_annotations)
error[E0284]: type annotations needed
 --> src/main.rs:2:9
  |
2 |     let guess = "42".parse().expect("Not a number!");
  |         ^^^^^        ----- type must be known at this point
  |
  = note: cannot satisfy `<_ as FromStr>::Err == _`
help: consider giving `guess` an explicit type
  |
2 |     let guess: /* Type */ = "42".parse().expect("Not a number!");
  |              ++++++++++++

For more information about this error, try `rustc --explain E0284`.
error: could not compile `no_type_annotations` (bin "no_type_annotations") due to 1 previous error
```

　　对于其他数据类型，你会看到不同的类型标注。

### 标量类型 {#scalar-types}

　　*标量*类型表示单个值。Rust 有四种主要的标量类型：整数、浮点数、布尔值和字符。你可能在其他编程语言中见过它们。让我们看看它们在 Rust 中如何工作。

#### 整数类型 {#integer-types}

　　*整数*是没有小数部分的数。我们在第 2 章用过一种整数类型：`u32`。这种类型声明表示与之关联的值应是占用 32 位空间的无符号整数（有符号整数类型以 `i` 而不是 `u` 开头）。表 3-1 展示了 Rust 中的内置整数类型。我们可以用这些变体中的任意一种来声明整数值的类型。

<span class="caption">表 3-1：Rust 中的整数类型</span>

| 长度 | 有符号 | 无符号 |
| ------- | ------- | -------- |
| 8 位 | `i8` | `u8` |
| 16 位 | `i16` | `u16` |
| 32 位 | `i32` | `u32` |
| 64 位 | `i64` | `u64` |
| 128 位 | `i128` | `u128` |
| 取决于架构 | `isize` | `usize` |

　　每个变体都可以是有符号或无符号的，并有明确的大小。*有符号*（Signed）和*无符号*（unsigned）指的是该数是否可能为负——换句话说，数字是否需要带符号（有符号），还是永远只会是正数因而可以不带符号表示（无符号）。这就像在纸上写数字：当符号重要时，数字会带正号或负号；而当可以假定数字为正时，则不写符号。有符号数使用[二进制补码][twos-complement]表示法存储。

　　每个有符号变体可以存储从 −(2<sup>n − 1</sup>) 到 2<sup>n − 1</sup> − 1（含）的数，其中 *n* 是该变体使用的位数。因此，`i8` 可以存储从 −(2<sup>7</sup>) 到 2<sup>7</sup> − 1 的数，即 −128 到 127。无符号变体可以存储从 0 到 2<sup>n</sup> − 1 的数，因此 `u8` 可以存储从 0 到 2<sup>8</sup> − 1 的数，即 0 到 255。

　　此外，`isize` 和 `usize` 类型取决于运行程序的计算机架构：若是 64 位架构则为 64 位，若是 32 位架构则为 32 位。

　　你可以用表 3-2 所示的任意形式书写整数字面量。注意，可以对应多种数字类型的数字字面量允许类型后缀，例如 `57u8`，以指定类型。数字字面量也可以使用 `_` 作为视觉分隔符，使数字更易读，例如 `1_000`，其值与指定 `1000` 相同。

<span class="caption">表 3-2：Rust 中的整数字面量</span>

| 数字字面量 | 示例 |
| ---------------- | ------------- |
| 十进制 | `98_222` |
| 十六进制 | `0xff` |
| 八进制 | `0o77` |
| 二进制 | `0b1111_0000` |
| 字节（仅 `u8`） | `b'A'` |

　　那么你怎么知道该用哪种整数类型呢？若不确定，Rust 的默认值通常是很好的起点：整数类型默认是 `i32`。你会使用 `isize` 或 `usize` 的主要场景是为某种集合建立索引。

> ##### 整数溢出
>
> 假设你有一个类型为 `u8` 的变量，可以保存 0 到 255 之间的值。若你试图把该变量改成该范围之外的值，例如 256，就会发生*整数溢出*（integer overflow），可能导致两种行为之一。在调试模式下编译时，Rust 会包含整数溢出检查，若发生这种情况，程序会在运行时 panic。Rust 中的 panic 指程序因错误而退出；我们会在第 9 章的[「用 `panic!` 处理不可恢复错误」][unrecoverable-errors-with-panic]一节更深入地讨论 panic。
>
> 当你用 `--release` 标志以发布模式编译时，Rust *不会*包含会导致 panic 的整数溢出检查。相反，若发生溢出，Rust 会执行*二进制补码回绕*（two’s complement wrapping）。简言之，超过该类型能保存的最大值的值会「回绕」到该类型能保存的最小值。对于 `u8`，值 256 变成 0，值 257 变成 1，依此类推。程序不会 panic，但变量会有一个你大概并不期望的值。依赖整数溢出的回绕行为被视为错误。
>
> 要显式处理溢出的可能性，可以使用标准库为原始数字类型提供的以下几组方法：
>
> - 在所有编译模式下用 `wrapping_*` 方法回绕，例如 `wrapping_add`。
> - 若发生溢出则用 `checked_*` 方法返回 `None` 值。
> - 用 `overflowing_*` 方法返回值以及一个指示是否发生溢出的布尔值。
> - 用 `saturating_*` 方法在值的最小或最大值处饱和。

#### 浮点类型 {#floating-point-types}

　　Rust 还有两种用于*浮点数*（floating-point numbers，带小数点的数）的原始类型。Rust 的浮点类型是 `f32` 和 `f64`，大小分别为 32 位和 64 位。默认类型是 `f64`，因为在现代 CPU 上，它的速度与 `f32` 大致相同，但精度更高。所有浮点类型都是有符号的。

　　下面的例子展示了浮点数的实际使用：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x = 2.0; // f64

    let y: f32 = 3.0; // f32
}
```

　　浮点数按照 IEEE-754 标准表示。

#### 数值运算 {#numeric-operations}

　　Rust 支持你对所有数字类型所期望的基本数学运算：加、减、乘、除和取余。整数除法会向零截断到最近的整数。下面的代码展示了如何在 `let` 语句中使用每种数值运算：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    // addition
    let sum = 5 + 10;

    // subtraction
    let difference = 95.5 - 4.3;

    // multiplication
    let product = 4 * 30;

    // division
    let quotient = 56.7 / 32.2;
    let truncated = -5 / 3; // Results in -1

    // remainder
    let remainder = 43 % 5;
}
```

　　这些语句中的每个表达式都使用一个数学运算符并求值为单个值，然后绑定到变量。[附录 B][appendix_b] 包含 Rust 提供的所有运算符列表。

#### 布尔类型 {#the-boolean-type}

　　与大多数其他编程语言一样，Rust 中的布尔类型有两个可能的值：`true` 和 `false`。布尔值大小为一字节。Rust 中的布尔类型用 `bool` 指定。例如：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let t = true;

    let f: bool = false; // with explicit type annotation
}
```

　　使用布尔值的主要方式是通过条件，例如 `if` 表达式。我们会在[「控制流」][control-flow]一节介绍 `if` 表达式在 Rust 中如何工作。

#### 字符类型 {#the-character-type}

　　Rust 的 `char` 类型是语言中最原始的字母类型。下面是一些声明 `char` 值的例子：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let c = 'z';
    let z: char = 'ℤ'; // with explicit type annotation
    let heart_eyed_cat = '😻';
}
```

　　注意我们用单引号指定 `char` 字面量，而字符串字面量使用双引号。Rust 的 `char` 类型大小为 4 字节，表示一个 Unicode 标量值，这意味着它能表示的远不止 ASCII。带重音的字母；中文、日文和韩文字符；emoji；以及零宽空格，在 Rust 中都是合法的 `char` 值。Unicode 标量值的范围是 `U+0000` 到 `U+D7FF` 以及 `U+E000` 到 `U+10FFFF`（含）。不过，「字符」在 Unicode 中并不是一个真正的概念，因此你对「字符」的直觉未必与 Rust 中的 `char` 一致。我们会在第 8 章的[「用字符串存储 UTF-8 编码的文本」][strings]中详细讨论这个话题。

### 复合类型 {#compound-types}

　　*复合类型*可以把多个值组合成一个类型。Rust 有两种原始复合类型：元组（tuple）和数组（array）。

#### 元组类型 {#the-tuple-type}

　　*元组*是把若干具有各种类型的值组合进一个复合类型的通用方式。元组有固定长度：一旦声明，就不能增大或缩小。

　　我们通过在圆括号内写逗号分隔的值列表来创建元组。元组中的每个位置都有一个类型，不同值的类型不必相同。本例中我们添加了可选的类型标注：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);
}
```

　　变量 `tup` 绑定到整个元组，因为元组被视为单个复合元素。要从元组中取出各个值，我们可以用模式匹配来解构元组值，像这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is: {y}");
}
```

　　这个程序首先创建一个元组并把它绑定到变量 `tup`。然后用带 `let` 的模式把 `tup` 拆成三个独立变量 `x`、`y` 和 `z`。这称为*解构*（destructuring），因为它把单个元组拆成三部分。最后，程序打印 `y` 的值，即 `6.4`。

　　我们也可以用句点（`.`）后跟想访问的值的索引，直接访问元组元素。例如：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let x: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;

    let six_point_four = x.1;

    let one = x.2;
}
```

　　这个程序创建元组 `x`，然后用各自的索引访问元组的每个元素。与大多数编程语言一样，元组中的第一个索引是 0。

　　没有任何值的元组有一个特殊名称：*单元*（unit）。这个值及其对应类型都写成 `()`，表示无值或空返回类型。若表达式没有返回任何其他值，它们会隐式返回单元值。

#### 数组类型 {#the-array-type}

　　拥有多个值的集合的另一种方式是*数组*。与元组不同，数组的每个元素必须具有相同类型。与某些其他语言中的数组不同，Rust 中的数组有固定长度。

　　我们把数组中的值写成方括号内的逗号分隔列表：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];
}
```

　　当你希望数据像我们目前见过的其他类型一样分配在栈上，而不是堆上时（我们会在[第 4 章][stack-and-heap]更多地讨论栈与堆），或者当你希望始终拥有固定数量的元素时，数组很有用。不过，数组不如向量（vector）类型灵活。向量是标准库提供的类似集合类型，*允许*增大或缩小，因为它的内容位于堆上。若你不确定该用数组还是向量，多半应该用向量。[第 8 章][vectors]会更详细地讨论向量。

　　不过，当你知道元素数量不需要改变时，数组更有用。例如，若你在程序中使用月份名称，你大概会用数组而不是向量，因为你知道它始终包含 12 个元素：

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

　　你可以用方括号写出数组的类型：先写每个元素的类型，再写分号，然后是数组中的元素个数，像这样：

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

　　这里，`i32` 是每个元素的类型。分号之后的数字 `5` 表示数组包含五个元素。

　　你也可以通过指定初始值、后跟分号、再写方括号中的数组长度，来把数组初始化为每个元素都相同的值，如下所示：

```rust
let a = [3; 5];
```

　　名为 `a` 的数组将包含 `5` 个元素，初始时全部设为值 `3`。这与写 `let a = [3, 3, 3, 3, 3];` 相同，但更简洁。

#### 访问数组元素 {#array-element-access}

　　数组是一块大小已知且固定、可以分配在栈上的连续内存。你可以用索引访问数组的元素，像这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];

    let first = a[0];
    let second = a[1];
}
```

　　在这个例子中，名为 `first` 的变量会得到值 `1`，因为那是数组中索引 `[0]` 处的值。名为 `second` 的变量会从索引 `[1]` 得到值 `2`。

#### 无效的数组元素访问 {#invalid-array-element-access}

　　让我们看看若试图访问超出数组末尾的元素会发生什么。假设你运行这段与第 2 章猜数字游戏类似的代码，从用户那里获取数组索引：

<span class="filename">文件名：src/main.rs</span>

```rust
use std::io;

fn main() {
    let a = [1, 2, 3, 4, 5];

    println!("Please enter an array index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failed to read line");

    let index: usize = index
        .trim()
        .parse()
        .expect("Index entered was not a number");

    let element = a[index];

    println!("The value of the element at index {index} is: {element}");
}
```

　　这段代码能成功编译。若你用 `cargo run` 运行它并输入 `0`、`1`、`2`、`3` 或 `4`，程序会打印数组中该索引对应的值。若你输入一个超出数组末尾的数，例如 `10`，你会看到类似这样的输出：


```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　程序在使用无效值做索引运算时发生了运行时错误。程序带着错误信息退出，没有执行最后的 `println!` 语句。当你试图用索引访问元素时，Rust 会检查你指定的索引是否小于数组长度。若索引大于或等于长度，Rust 会 panic。这种检查必须在运行时发生，尤其是在本例中，因为编译器不可能知道用户稍后运行代码时会输入什么值。

　　这是 Rust 内存安全原则的实际例子。在许多底层语言中不会做这种检查，当你提供错误索引时，可能访问到无效内存。Rust 通过立即退出而不是允许该内存访问并继续执行，来保护你免受这类错误。第 9 章会更多地讨论 Rust 的错误处理，以及如何编写既不 panic 也不允许无效内存访问的可读、安全代码。

[comparing-the-guess-to-the-secret-number]: ../../guessing-game/#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ../05-control-flow/#control-flow
[strings]: ../../common-collections/02-strings/#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ../../understanding-ownership/01-what-is-ownership/#the-stack-and-the-heap
[vectors]: ../../common-collections/01-vectors/
[unrecoverable-errors-with-panic]: ../../error-handling/01-unrecoverable-errors-with-panic/
[appendix_b]: ../../appendix/02-b-operators/
