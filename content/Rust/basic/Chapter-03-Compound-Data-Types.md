+++
title = "第 3 章 复合数据类型"
weight = 30
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter-03 复合数据类型

## 3.1 字符串与字符串切片

字符串是编程中最常用的数据类型之一。Rust 的字符串系统有点独特——它区分了 `String` 和 `&str`，这两种类型各有各的用途。理解它们的区别，是掌握 Rust 字符串处理的关键！

### 3.1.1 String 与 &str 的本质区别

#### 3.1.1.1 String：拥有所有权的动态字符串

`String` 是一个**拥有所有权**的字符串类型，存储在堆上，可以动态增长。它就像一个任性的小朋友——我想变大就变大！

（至于为什么不能缩小...呃，Rust就是这么"记仇"）

```rust
fn main() {
    // 创建 String
    let s = String::from("hello");
    
    // 可以修改
    let mut s2 = String::from("hello");
    s2.push_str(", world");
    println!("{}", s2); // hello, world
    
    // String 的内存布局：
    // 栈上：ptr（指针）+ len（长度）+ capacity（容量）
    // 堆上：实际的字符串数据
}
```

#### 3.1.1.2 &str：借用的字符串切片

`&str` 是一个**借用**的字符串视图，由指向数据的指针和长度组成。它就像是 String 的"身份证复印件"——你可以随便看，但不能据为己有！

```rust
fn main() {
    let s = String::from("hello");
    
    // &str 引用 String
    let r: &str = &s;
    println!("{}", r); // hello
    
    // 字符串字面量本身就是 &str
    let literal: &str = "hello";
    println!("{}", literal); // hello
}
```

#### 3.1.1.3 内存布局对比

下面这张图对比 `String` 与 `&str` 的内存布局：`String` 自己在栈上持有堆缓冲区的指针、长度和容量，而 `&str` 只是一个指向别人数据的「胖指针」。

```mermaid
graph TB
    subgraph String[栈上 - String]
        S1[ptr: 0x1000]
        S2[len: 5]
        S3[capacity: 5]
    end
    
    subgraph 堆内存[堆上 - 共享数据]
        H1[字符数据<br/>h e l l o]
    end
    
    S1 --> H1
    
    subgraph "&str（栈上）"
        R1[ptr: 0x1000]
        R2[len: 5]
    end
    
    R1 --> H1
    S1 -.-> H1
    style H1 fill:#90EE90
```

```rust
use std::mem;

fn main() {
    // String 的组成
    println!("String 大小: {} 字节", mem::size_of::<String>()); // 24 字节（64位系统）
    // = 8 字节（ptr）+ 8 字节（len）+ 8 字节（capacity）
    
    // &str 的组成
    println!("&str 大小: {} 字节", mem::size_of::<&str>()); // 16 字节
    // = 8 字节（ptr）+ 8 字节（len）
}
```

### 3.1.2 字符串切片（&str）

#### 3.1.2.1 &str 的创建

`&str` 可以从字面量、`String` 借用或切片三种来源得到，它们的共同点是都不拥有数据。

```rust
fn main() {
    // 从字符串字面量创建
    let s1: &str = "hello";
    
    // 从 String 借用
    let s2 = String::from("hello");
    let s3: &str = &s2;
    
    // 字符串切片
    let s4 = &s2[0..3]; // "hel"
    let s5 = &s2[..3]; // "hel"
    let s6 = &s2[2..]; // "llo"
    let s7 = &s2[..]; // "hello"
    
    println!("s1: {}, s3: {}, s4: {}", s1, s3, s4);
}
```

#### 3.1.2.2 &str 作为函数参数

参数写成 `&str` 时，调用处传 `&String` 会自动解引用，字面量也能直接传，所以它是最通用的只读字符串参数类型。

```rust
// &str 是最灵活的字符串参数类型
fn print_str(s: &str) {
    println!("{}", s);
}

fn main() {
    let s1 = String::from("hello");
    let s2 = "world";
    
    // 可以接受 String 或字符串字面量
    print_str(&s1);
    print_str(s2);
}
```

#### 3.1.2.3 字符串切片的内存结构

切片不复制数据，它只记录起始指针和长度；下面的代码打印切片的长度以及它指向的字节。

```rust
fn main() {
    let s = String::from("hello");
    let slice = &s[1..4];
    
    // slice 的结构：
    // ptr 指向 'e' 的位置
    // len = 3（'e', 'l', 'l'）
    
    println!("slice: {}", slice); // ell
    
    // 切片必须落在字符边界！
    // 对于纯 ASCII 字符串，每个字符 1 字节，任意字节边界都落在字符边界上
    // let slice = &s[0..2]; // 对于 "hello" 这是有效的，返回 "he"（安全）
    // 但如果用于中文，落在字符中间就会 panic！
}
```

### 3.1.3 String 的创建与操作

#### 3.1.3.1 String::new() / String::from()

`String::new()` 创建空字符串（不分配堆内存），`String::from()` 则从字符串字面量拷贝出一份拥有所有权的数据。

```rust
fn main() {
    // 创建空字符串
    let s1 = String::new();
    let s2 = String::from("hello");
    
    // 两种方式等价
    println!("s1: '{}', s2: '{}'", s1, s2);
    
    // 从 &str 创建 String
    let s3: String = "world".to_string();
    println!("s3: {}", s3);
}
```

#### 3.1.3.2 to_string() / to_owned()

两者都能从 `&str` 得到 `String`：`to_string()` 走 `Display`/`ToString`，`to_owned()` 走 `ToOwned` trait，对字符串而言结果相同。

```rust
fn main() {
    let s1 = "hello";
    let s2 = s1.to_string(); // to_string() 方法
    let s3 = s1.to_owned(); // to_owned() 方法
    
    // to_owned() 和 to_string() 几乎等价
    // to_owned() 在某些情况下更符合习惯
    
    println!("s2: {}, s3: {}", s2, s3);
}
```

#### 3.1.3.3 String::with_capacity(capacity)

预分配容量可以避免反复扩容搬移数据；注意 `capacity()` 表示「至少能装下多少」，实际值可能比请求的更大。

```rust
fn main() {
    // 预先分配容量，避免多次重新分配
    let mut s = String::with_capacity(100);
    
    println!("初始容量: {}", s.capacity()); // 100
    
    // 快速追加
    s.push_str("hello");
    println!("追加后容量: {}", s.capacity()); // 仍然 100
    println!("内容: {}", s);
}
```

#### 3.1.3.4 String::from_utf8_lossy

非法 UTF-8 字节序列无法进入 `String`：`String::from_utf8` 会返回 `Result`，而 `from_utf8_lossy` 用替换字符兜底。

```rust
fn main() {
    // 字节到字符串的转换
    let bytes = vec![104, 101, 108, 108, 111]; // "hello" 的 UTF-8 字节
    let s = String::from_utf8(bytes).unwrap();
    println!("从 UTF-8 创建: {}", s); // 从 UTF-8 创建: hello
    
    // 无效 UTF-8 的处理
    let invalid_bytes = vec![255, 254, 236, 225]; // 不是有效的 UTF-8
    // 注意是 String::from_utf8_lossy，不是 str::from_utf8_lossy
    let lossy_string = String::from_utf8_lossy(&invalid_bytes);
    println!("lossy 转换: {}", lossy_string); // 每个非法字节都会被换成 U+FFFD（�）
    println!("是借用还是拥有？ {}", std::any::type_name_of_val(&lossy_string)); // Cow<str>
}
```

### 3.1.4 字符串常用方法

#### 3.1.4.1 拼接：push_str / push / format!

三种拼接方式各有取舍：`push_str`/`push` 在原地修改，`format!` 总是新建一个 `String`。

```rust
fn main() {
    // push_str: 追加 &str
    let mut s1 = String::from("hello");
    s1.push_str(", world");
    println!("push_str: {}", s1); // hello, world
    
    // push: 追加单个字符
    let mut s2 = String::from("hello");
    s2.push('!');
    println!("push: {}", s2); // hello!
    
    // format!: 格式化拼接
    let s3 = format!("{} + {} = {}", 1, 2, 3);
    println!("format: {}", s3); // 1 + 2 = 3
    
    // 字符串拼接
    let s4 = String::from("hello");
    let s5 = String::from(" world");
    let s6 = s4 + &s5; // s4 被移动！
    // println!("s4: {}", s4); // 错误！s4 已移动
    println!("s6: {}", s6); // hello world
}
```

#### 3.1.4.2 查询：len / is_empty / contains / starts_with / ends_with

这一组方法都不会改动字符串本身；特别注意 `len()` 返回的是字节数而不是字符数。

```rust
fn main() {
    let s = String::from("hello world");
    
    // len(): 字节长度
    println!("len: {}", s.len()); // 11
    
    // is_empty(): 是否为空
    println!("is_empty: {}", s.is_empty()); // false
    
    // contains(): 是否包含子串
    println!("contains 'world': {}", s.contains("world")); // true
    println!("contains 'rust': {}", s.contains("rust")); // false
    
    // starts_with / ends_with
    println!("starts_with 'hello': {}", s.starts_with("hello")); // true
    println!("ends_with 'world': {}", s.ends_with("world")); // true
}
```

#### 3.1.4.3 切片与 UTF-8 边界

按字节切片时越界、或切在多字节字符中间都会 panic，中文字符串尤其容易踩到。

```rust
fn main() {
    let s = String::from("hello");
    
    // 切片落在 ASCII 字符边界
    let slice = &s[0..3];
    println!("slice: {}", slice); // hel
    
    // 切片落在 UTF-8 字符边界（中文）
    let chinese = String::from("你好");
    let slice2 = &chinese[0..3]; // "你好" 中每个中文字符占 3 字节，0..3 正好切出第一个字符
    println!("chinese slice: {}", slice2); // 你
    
    // 错误示例：切片落在字符中间
    // let bad = &chinese[0..2]; // panic！因为 '你' 是 3 字节，字节 2 落在字符中间
}
```

#### 3.1.4.4 修剪：trim / trim_start / trim_end / trim_matches

`trim` 系列按 `char::is_whitespace` 判断，返回的是原字符串的子切片，不会重新分配内存。

```rust
fn main() {
    let s = "  hello  ";
    
    // trim(): 去除两端空白
    println!("trim: '{}'", s.trim()); // 'hello'
    
    // trim_start / trim_end: 只去除一端
    println!("trim_start: '{}'", s.trim_start()); // 'hello  '
    println!("trim_end: '{}'", s.trim_end()); // '  hello'
    
    // trim_matches: 去除指定的字符
    let s2 = "###hello###";
    println!("trim_matches: '{}'", s2.trim_matches('#')); // hello
}
```

#### 3.1.4.5 大小写：to_lowercase / to_uppercase

大小写转换会返回新的 `String`，因为个别字符转换后可能变成多个字符（例如 `ß` 变成 `SS`）。

```rust
fn main() {
    let s = "Hello World";
    
    // 转大写
    println!("uppercase: {}", s.to_uppercase()); // HELLO WORLD
    
    // 转小写
    println!("lowercase: {}", s.to_lowercase()); // hello world
    
    // 注意：Unicode 大小写不总是对称
    let german = "Straße";
    println!("uppercase: {}", german.to_uppercase()); // STRASSE（ß -> SS）
    
    let turkish = "i";
    println!("Turkish uppercase: {}", turkish.to_uppercase()); // İ（土耳其语特殊规则）
}
```

#### 3.1.4.6 替换：replace / replacen / replace_range

`replace` 替换全部匹配，`replacen` 限定次数，`replace_range` 按字节区间替换并要求区间落在字符边界上。

```rust
fn main() {
    let s = String::from("hello world");
    
    // replace: 替换所有出现
    let s2 = s.replace("world", "rust");
    println!("replace: {}", s2); // hello rust
    
    // replacen: 只替换前 n 次
    let s3 = "hello hello hello".replace("hello", "hi");
    println!("replacen (all): {}", s3); // hi hi hi
    
    // replace_range: 替换范围内的内容
    let mut s4 = String::from("hello world");
    s4.replace_range(6..11, "rust");
    println!("replace_range: {}", s4); // hello rust
}
```

#### 3.1.4.7 分割：split / split_once / split_whitespace / lines / split_at

分割返回的是惰性迭代器，不会立刻分配；`split_whitespace` 还会把连续的空白折叠成一个分隔符。

```rust
fn main() {
    let s = "apple,banana,cherry";
    
    // split: 按分隔符分割
    for part in s.split(',') {
        println!("split: {}", part);
    }
    
    // split_once: 只分割第一次
    if let Some((first, rest)) = s.split_once(',') {
        println!("first: {}, rest: {}", first, rest);
    }
    
    // split_whitespace: 按空白分割
    let s2 = "hello   world\nrust";
    for word in s2.split_whitespace() {
        println!("word: {}", word);
    }
    
    // lines: 按行分割
    let s3 = "line1\nline2\nline3";
    for line in s3.lines() {
        println!("line: {}", line);
    }
    
    // split_at: 按位置分割
    let (left, right) = s.split_at(5);
    println!("left: {}, right: {}", left, right); // apple, banana,cherry
}
```

#### 3.1.4.8 解析：parse<T>

`parse::<T>()` 借助 `FromStr` trait 把文本转成目标类型，返回 `Result`，所以失败必须处理。

```rust
fn main() {
    // 字符串解析为数字
    let num: i32 = "42".parse().unwrap();
    println!("解析 i32: {}", num);
    
    let num2: Result<i64, _> = "100".parse();
    println!("解析 Result: {:?}", num2);
    
    // 解析失败
    let bad = "not a number".parse::<i32>();
    println!("解析失败: {:?}", bad.is_err()); // true
}
```

#### 3.1.4.9 chars().count() vs len()

`len()` 数的是字节，`chars().count()` 数的是 Unicode 标量值，中文和 emoji 上两者差别明显。

```rust
fn main() {
    let s = "hello";
    
    // len(): 字节数
    println!("len (bytes): {}", s.len()); // 5
    
    // chars().count(): 字符数
    println!("chars().count(): {}", s.chars().count()); // 5
    
    // 中文字符
    let chinese = "你好";
    println!("len (bytes): {}", chinese.len()); // 6（每个中文字符 3 字节）
    println!("chars().count(): {}", chinese.chars().count()); // 2
    
    // emoji
    let emoji = "😀";
    println!("emoji len: {}", emoji.len()); // 4
    println!("emoji chars: {}", emoji.chars().count()); // 1
}
```

### 3.1.5 字符串的迭代

#### 3.1.5.1 字符迭代：chars()

`chars()` 按 Unicode 标量值迭代，是遍历字符串内容最常用的方式。

```rust
fn main() {
    let s = "hello";
    
    for c in s.chars() {
        println!("char: {}", c);
    }
    
    // 输出：
    // char: h
    // char: e
    // char: l
    // char: l
    // char: o
}
```

#### 3.1.5.2 字节迭代：bytes()

`bytes()` 按原始 UTF-8 字节迭代，适合处理二进制协议或需要精确控制字节的场合。

```rust
fn main() {
    let s = "hello";
    
    for b in s.bytes() {
        println!("byte: {}", b);
    }
    
    // 输出：
    // byte: 104
    // byte: 101
    // byte: 108
    // byte: 108
    // byte: 111
}
```

#### 3.1.5.3 Unicode 字符簇迭代

标准库的迭代只到「标量值」这一层；emoji 家庭、带变音符号的字母要按人眼看到的一个字符切分，得借助 `unicode-segmentation` 这类 crate。

```rust
// Rust 标准库不直接支持 grapheme clusters（字符簇）
// 需要使用第三方 crate如 unicode-segmentation

fn main() {
    let s = "a😀b😀c";
    
    // 使用 chars() 迭代（Unicode 标量值）
    println!("chars 迭代:");
    for c in s.chars() {
        print!("{} ", c);
    }
    println!();
    
    // 使用 bytes() 迭代
    println!("bytes 迭代:");
    for b in s.bytes() {
        print!("{} ", b);
    }
    println!();
}
```

#### 3.1.5.4 迭代与下标访问的区别

Rust 不允许用 `s[i]` 取字符，因为下标是字节索引，落在多字节字符中间会产生无效字符串；要遍历请用 `chars()`。

```rust
fn main() {
    let s = "hello";
    
    // 下标访问按字节索引
    // s[0] // 编译错误！不能直接下标访问
    
    // 但可以用 get()
    if let Some(c) = s.chars().nth(0) {
        println!("第一个字符: {}", c); // h
    }
    
    // 错误示例：下标落在多字节字符中间
    let chinese = "你好";
    // chinese[0..2] // panic！'你' 是 3 字节
    
    // 正确做法
    if let Some(c) = chinese.chars().nth(0) {
        println!("第一个中文字符: {}", c); // 你
    }
}
```

### 3.1.6 字符串格式化

#### 3.1.6.1 format! 宏

`format!` 返回一个全新的 `String`，是把多个值拼成文本时最常用的办法。

```rust
fn main() {
    // format! 返回 String
    let s = format!("{} + {} = {}", 1, 2, 3);
    println!("{}", s); // 1 + 2 = 3
    
    // 带格式
    let s2 = format!("{:#?}", vec![1, 2, 3]);
    println!("{}", s2);
}
```

#### 3.1.6.2 print! / println! / eprint! / eprintln!

这四个宏的区别只在输出流和是否换行：`print!`/`println!` 走标准输出，带 `eprint` 的版本走标准错误。

```rust
fn main() {
    // println! 打印到 stdout 并换行
    println!("hello");
    
    // print! 打印到 stdout 不换行
    print!("hello ");
    println!("world");
    
    // eprintln! 打印到 stderr
    eprintln!("这是错误信息");
    
    // 带格式化
    println!("PI ≈ {:.2}", 3.14159);
}
```

#### 3.1.6.3 write! / writeln!

`write!`/`writeln!` 把格式化结果写进任意 `io::Write` 实现，比 `format!` 少一次中间分配，代价是必须处理 `io::Result`。

```rust
use std::io::{self, Write};

fn main() -> io::Result<()> {
    // 写入文件：writeln! 需要 Write trait 在作用域里（上面的 use 就是干这个的）
    use std::fs::File;
    let mut file = File::create("output.txt")?;
    
    writeln!(file, "第一行")?;
    writeln!(file, "第二行: {}", 42)?;
    
    // String 也能接收格式化输出，但它实现的是 std::fmt::Write，而不是 io::Write
    {
        use std::fmt::Write as _;
        let mut s = String::new();
        writeln!(s, "格式化到 String: {}", 100).unwrap();
        println!("{}", s); // 格式化到 String: 100
    }
    
    Ok(())
}
```

#### 3.1.6.4 format_args!

`format_args!` 生成的是借用参数的 `Arguments` 结构，不能长期保存，它是所有格式化宏底层的公共机制。

```rust
fn main() {
    // format_args! 返回一个 Arguments 结构
    let args = format_args!("{} + {} = {}", 1, 2, 3);
    println!("{:?}", args);
    
    // 使用示例
    fn print_args(args: std::fmt::Arguments) {
        print!("{}", args);
    }
    
    print_args(format_args!("Hello, {}!", "world"));
}
```

### 3.1.7 转义字符

#### 3.1.7.1 \n / \r\n / \t

下面列出最常用的几个转义序列，注意 Rust 源码里的换行也可以直接写在字符串中。

```rust
fn main() {
    // 换行符
    println!("第一行\n第二行");
    
    // 回车 + 换行（Windows 风格）
    println!("Windows 换行\r\nCRLF");
    
    // 制表符
    println!("列1\t列2\t列3");
}
```

#### 3.1.7.2 \\ / \' / \"

要在字符串里写出反斜杠、单引号或双引号本身，需要额外加一个反斜杠转义。

```rust
fn main() {
    // 转义字符
    println!("反斜杠: \\");
    println!("单引号: \\'");
    println!("双引号: \\\"");
    
    // 原始字符串
    let raw = r#"双引号 " 和 ' 都包含在原始字符串中"#;
    println!("原始字符串: {}", raw);
}
```

#### 3.1.7.3 \xNN / \u{NNNNNN}

`\xNN` 只能表示不超过 `\x7F` 的字节，非 ASCII 字符必须用 `\u{...}` 写码点。

```rust
fn main() {
    // \xNN：按字节写（合法的十六进制字节，范围到 \x7F）
    println!("\x48\x49"); // HI（\x48 = 72 = 'H'，\x49 = 73 = 'I'）
    
    // \u{NNNNNN}：按 Unicode 码点写
    println!("\u{2764}"); // ❤
    println!("\u{1F600}"); // 😀
    println!("\u{4E2D}"); // 中
    
    // 顺便一提：反斜杠本身要写两次才能打印出来
    println!("\\u{{4E2D}} 会原样打印转义写法");
}
```

### 3.1.8 C 风格字符串

#### 3.1.8.1 CStr：来自 C 的字符串

和 C 打交道时，字符串以 `\0` 结尾且不保证是合法 UTF-8，因此有了 `CStr`。

```rust
use std::ffi::CStr;

fn main() {
    // CStr 表示来自 C 的字符串（以 null 结尾）
    let c_string = CStr::from_bytes_with_nul(b"hello\0").unwrap();
    
    println!("CStr: {:?}", c_string);
    println!("转 &str: {}", c_string.to_str().unwrap());
}
```

#### 3.1.8.2 CString：传递给 C 的字符串

`CString` 是拥有所有权的 C 字符串，传给 C 函数时用 `as_ptr()` 取裸指针。

```rust
use std::ffi::CString;

fn main() {
    // CString 用于传递给 C 函数
    let c_str = CString::new("hello").unwrap();
    
    // 获取原始指针
    let ptr = c_str.as_ptr();
    println!("CString 指针: {:?}", ptr);
}
```

#### 3.1.8.3 CString::new 与 null 字节处理

`CString::new` 会拒绝内部含 `\0` 的输入，因为那会截断 C 侧看到的字符串。

```rust
use std::ffi::CString;

fn main() {
    // 正常创建
    let s1 = CString::new("hello").unwrap();
    
    // 包含 null 的处理
    let with_null = b"hello\x00world";
    let s2 = CString::new(&with_null[..]).unwrap();
    println!("包含 null 的 CString: {:?}", s2);
    
    // 空字符串
    let empty = CString::new("").unwrap();
    println!("空 CString: {:?}", empty);
}
```

#### 3.1.8.4 CStr::as_cstr / CStr::to_str / to_bytes

`to_str()` 只在内容恰好是合法 UTF-8 时才成功，`to_bytes()` 则总是可用。

```rust
use std::ffi::CStr;

fn main() {
    let c_str = CStr::from_bytes_with_nul(b"hello\0").unwrap();
    
    // CStr 本身就是"字符串引用"，没有 as_cstr() 这种转换；
    // 想拿到 &CStr 直接用它自己就行
    let _: &CStr = c_str;
    
    // to_str: 转成 &str（可能失败，因为 C 字符串不保证是 UTF-8）
    let s: &str = c_str.to_str().unwrap();
    println!("to_str: {}", s); // to_str: hello
    
    // to_bytes: 转成 &[u8]（不包含结尾的 \0）
    let bytes: &[u8] = c_str.to_bytes();
    println!("to_bytes: {:?}", bytes); // to_bytes: [104, 101, 108, 108, 111]
}
```

### 3.1.9 OsStr / OsString（操作系统原生字符串）

#### 3.1.9.1 OsStr：操作系统字符串切片

`OsStr` 表示「操作系统眼里的字符串」：在 Unix 上它可以是任意字节，不保证是合法 UTF-8。

```rust
use std::ffi::OsStr;

fn main() {
    // OsStr 表示操作系统层面的字符串切片
    // 在 Unix 上可能是 UTF-8 或非 UTF-8 字节
    // 在 Windows 上可能是 UTF-16
    
    let os_str: &OsStr = OsStr::new("hello");
    println!("OsStr: {:?}", os_str);
}
```

#### 3.1.9.2 OsString：拥有所有权的操作系统字符串

`OsString` 是 `OsStr` 的拥有所有权版本，两者关系类似 `String` 与 `&str`。

```rust
use std::ffi::OsString;

fn main() {
    // OsString 是 OsStr 的拥有版本
    let os_string = OsString::from("hello");
    
    // 可以从 String 或 &str 转换
    let from_string: OsString = String::from("world").into();
    
    println!("OsString: {:?}", os_string);
}
```

#### 3.1.9.3 OsStr 与 str / String 的转换

与 `str`/`String` 之间的转换在 Unix 上可能失败，因此要用 `to_str()`、`into_string()` 这类返回 `Result`/`Option` 的方法。

```rust
use std::ffi::{OsStr, OsString};

fn main() {
    let os_str: &OsStr = OsStr::new("hello");
    
    // OsStr -> &str（可能失败，因为 OsStr 不一定是 UTF-8）
    if let Some(s) = os_str.to_str() {
        println!("OsStr -> str: {}", s); // OsStr -> str: hello
    }
    
    // OsString -> String：返回的是 Result，不是 Option！
    let os_string = OsString::from("hello");
    match os_string.into_string() {
        Ok(s) => println!("OsString -> String: {}", s),
        Err(os) => println!("无法转换成 UTF-8: {:?}", os),
    }
}
```

#### 3.1.9.4 std::env::var() 返回 OsString

环境变量未必是合法 UTF-8，所以 `std::env::var` 返回 `Result<String, VarError>`，需要拿到原始字节时用 `var_os`。

```rust
use std::env;

fn main() {
    // 环境变量返回 OsString
    if let Ok(home) = env::var("HOME") {
        println!("HOME: {}", home); // String（Linux/Mac）
    }
    
    // Windows 上的环境变量
    // env::var("PATH") 返回 Result<String, ...>
    
    // 使用 OsString 处理更通用的环境变量
    // env::var_os("HOME") 返回 Option<OsString>
    if let Some(home) = env::var_os("HOME") {
        println!("HOME (OsString): {:?}", home);
    }
}
```

---

## 3.2 元组（Tuple）

元组是 Rust 中一种轻量级的复合类型，可以存储不同类型的多个值。它就像一个"固定大小的、轻量级的、不可变的容器"。

### 3.2.1 元组的创建与访问

#### 3.2.1.1 元组的创建语法

元组把不同类型的值打包在一起，元素的顺序和类型共同构成它的类型。

```rust
fn main() {
    // 创建元组
    let t: (i32, f64, u8) = (500, 6.4, 1);
    
    // 类型可以省略，让编译器推导
    let t2 = (500, 6.4, 1);
    
    // 混合类型
    let mixed = ("hello", 42, true, 3.14);
    
    // 空元组（单元类型）
    let empty: () = ();
    
    println!("t: {:?}", t);
    println!("t2: {:?}", t2);
    println!("mixed: {:?}", mixed);
}
```

#### 3.2.1.2 通过索引访问

元组用 `.0`、`.1` 这样的数字下标访问元素，不能用方括号。

```rust
fn main() {
    let t = (500, 6.4, 1);
    
    // 通过 .0, .1, .2 ... 访问
    println!("第一个: {}", t.0); // 500
    println!("第二个: {}", t.1); // 6.4
    println!("第三个: {}", t.2); // 1
    
    // 修改元组（如果是 mut 的）
    let mut t2 = (1, 2, 3);
    t2.0 = 10;
    println!("修改后: {:?}", t2); // (10, 2, 3)
}
```

#### 3.2.1.3 元组类型注解

元组类型的写法就是把各元素类型按顺序放进括号，元素类型不同也没关系。

```rust
fn main() {
    // 类型注解放在元组前面
    let pair: (i32, &str) = (42, "hello");
    
    let point: (f64, f64) = (1.0, 2.0);
    
    let complex: (bool, char, i64) = (true, 'x', -100);
    
    println!("pair: {:?}", pair);
    println!("point: {:?}", point);
    println!("complex: {:?}", complex);
}
```

### 3.2.2 元组作为函数返回值

#### 3.2.2.1 多返回值场景

元组最典型的用途是从函数返回多个值，调用处再用解构把结果拆开。

```rust
fn main() {
    // 元组经常用于返回多个值
    let result = divide(10.0, 3.0);
    println!("商: {}, 余数: {}", result.0, result.1);
    
    // 标准库示例：split_at
    let s = "hello";
    let (left, right) = s.split_at(2);
    println!("left: {}, right: {}", left, right);
}

fn divide(dividend: f64, divisor: f64) -> (f64, f64) {
    let quotient = dividend / divisor;
    let remainder = dividend % divisor;
    (quotient, remainder)
}
```

#### 3.2.2.2 标准库示例

标准库里也有不少返回元组的函数，例如 `Option::ok_or` 把 `Option` 转成 `Result`。

```rust
fn main() {
    // Option::ok_or
    let opt: Option<i32> = Some(42);
    let result: Result<i32, &str> = opt.ok_or("没有值");
    println!("ok_or: {:?}", result);
    
    // split_at
    let arr = [1, 2, 3, 4, 5];
    let (first, rest) = arr.split_at(2);
    println!("first: {:?}", first); // [1, 2]
    println!("rest: {:?}", rest); // [3, 4, 5]
}
```

### 3.2.3 元组解构

#### 3.2.3.1 let 解构赋值

`let` 模式可以直接把元组拆成多个变量，一次绑定多个名字。

```rust
fn main() {
    let t = (1, "hello", 3.14);
    
    // 解构赋值
    let (a, b, c) = t;
    println!("a = {}, b = {}, c = {}", a, b, c);
    
    // 可以只解构需要的部分
    let (x, _, z) = t; // 使用 _ 忽略不需要的值
    println!("x = {}, z = {}", x, z);
}
```

#### 3.2.3.2 match 中的元组解构

`match` 的每个分支都可以解构元组，配合字面量模式还能做精确匹配。

```rust
fn main() {
    let t = (1, 2, 3);
    
    match t {
        (a, b, c) => println!("({}, {}, {})", a, b, c),
    }
    
    // 带条件的解构
    let t2 = (5, 10);
    match t2 {
        (x, y) if x == y => println!("相等"),
        (x, y) if x + y == 15 => println!("和为15"),
        (x, y) => println!("({}, {})", x, y),
    }
}
```

#### 3.2.3.3 函数参数解构

函数参数位置同样支持模式，可以在调用时就把元组拆开。

```rust
fn main() {
    // 函数参数也可以解构
    let result = process((1, 2));
    println!("result: {}", result);
}

fn process((x, y): (i32, i32)) -> i32 {
    x + y
}
```

#### 3.2.3.4 部分解构 + rest

解构时也可以只取需要的几个位置，其余用 `..` 忽略。

```rust
fn main() {
    let t = (1, 2, 3, 4, 5);
    
    // 解构到第一个和最后一个，中间用 ..
    let (first, .., last) = t;
    println!("first: {}, last: {}", first, last); // first: 1, last: 5
    
    // 解构中间部分
    let (a, .., b) = (10, 20, 30, 40, 50);
    println!("a: {}, b: {}", a, b); // a: 10, b: 50
}
```

---

## 3.3 数组（Array）与切片（Slice）

数组和切片是 Rust 中存储固定和可变数量元素的方式。数组的长度在编译时就确定，切片则是对数组或向量部分数据的引用。

### 3.3.1 数组的创建与访问

#### 3.3.1.1 数组类型注解

数组类型写成 `[T; N]`，长度是类型的一部分，必须在编译期确定。

```rust
fn main() {
    // 类型注解：[T; N] - T 是元素类型，N 是长度
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    
    // 可以省略类型，让编译器推导
    let arr2 = [1, 2, 3, 4, 5];
    
    println!("arr: {:?}", arr);
    println!("arr2: {:?}", arr2);
}
```

#### 3.3.1.2 数组字面量

`[value; N]` 语法把同一个值复制 N 份，因此元素类型必须实现 `Copy`。

```rust
fn main() {
    // [value; N] - 创建 N 个相同值的数组
    let arr = [0; 5]; // [0, 0, 0, 0, 0]
    println!("零初始化: {:?}", arr);
    
    // 字符串数组
    let days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"];
    println!("星期: {:?}", days);
    
    // 字符数组
    let vowels: [char; 5] = ['a', 'e', 'i', 'o', 'u'];
    println!("元音: {:?}", vowels);
}
```

#### 3.3.1.3 数组下标访问

数组下标从 0 开始，运行时会做边界检查，越界会 panic 而不是读到垃圾数据。

```rust
fn main() {
    let arr = [10, 20, 30, 40, 50];
    
    // 通过下标访问
    println!("第一个: {}", arr[0]); // 10
    println!("第三个: {}", arr[2]); // 30
    println!("最后一个: {}", arr[4]); // 50
    
    // 修改元素
    let mut arr2 = [1, 2, 3];
    arr2[0] = 100;
    println!("修改后: {:?}", arr2); // [100, 2, 3]
    
    // 越界访问：Debug 模式 panic，Release 模式未定义
    // arr[10] // 越界！
}
```

#### 3.3.1.4 数组越界访问

下面演示越界访问的后果，以及如何用 `get()` 拿到 `Option` 做安全检查。

```rust
fn main() {
    let arr = [1, 2, 3];
    
    // 合法下标范围：0 ~ len-1
    // arr[0] OK
    // arr[2] OK
    // arr[3] 越界！
    
    // 边界检查在 Debug 模式下启用
    // let element = arr[10]; // panic!
    
    // 使用 get() 方法安全访问
    match arr.get(10) {
        Some(value) => println!("值: {}", value),
        None => println!("越界！"),
    }
}
```

### 3.3.2 数组的内存布局

#### 3.3.2.1 栈上连续内存

数组元素在栈上连续排列，因此大小固定、访问快，但不能像 `Vec` 那样增长。

```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];
    
    // 数组存储在栈上，连续内存
    // 内存布局：
    // [1][2][3][4][5]
    //  ↑           ↑
    // ptr         ptr + 4 * size_of::<i32>()
    
    // 每个 i32 占 4 字节
    println!("i32 大小: {}", std::mem::size_of::<i32>()); // 4
    println!("数组大小: {} 字节", std::mem::size_of::<[i32; 5]>()); // 20
}
```

#### 3.3.2.2 数组大小在编译期确定

数组长度必须是编译期常量，运行期才知道的长度只能交给切片或 `Vec`。

```rust
fn main() {
    // 数组大小必须是编译期常量！
    const SIZE: usize = 5;
    let arr = [0; SIZE];
    
    // 不能用变量作为数组大小
    // let n = 5;
    // let arr = [0; n]; // 编译错误！
    
    println!("固定大小数组: {:?}", arr);
}
```

#### 3.3.2.3 数组无法动态增长

数组的长度不可变，增删元素要改用 `Vec`。

```rust
fn main() {
    let arr = [1, 2, 3];
    
    // 数组长度固定，不能添加或删除元素
    // arr.push(4); // 编译错误！数组可不是橡皮筋！
    
    // 如果需要动态数组，用 Vec<T>
    let mut v = vec![1, 2, 3];
    v.push(4);
    println!("Vec: {:?}", v); // [1, 2, 3, 4]
}
```

### 3.3.3 切片（Slice）作为视图

#### 3.3.3.1 &[T] 切片类型

切片是「指向一段连续元素」的视图，本质上由指针和长度两个字段组成。

```rust
fn main() {
    // 切片是对数组部分数据的引用
    let arr = [1, 2, 3, 4, 5];
    
    // 创建切片
    let slice: &[i32] = &arr[1..4]; // [2, 3, 4]
    println!("slice: {:?}", slice);
    
    // 切片不拥有数据，只是视图
    println!("arr 仍然有效: {:?}", arr);
}
```

#### 3.3.3.2 从数组创建切片

用区间语法可以从数组或 `Vec` 借出部分元素，`&arr[..]` 得到覆盖整个数组的切片。

```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];
    
    // 完整切片
    let s1 = &arr[..]; // [1, 2, 3, 4, 5]
    
    // 头部切片
    let s2 = &arr[..3]; // [1, 2, 3]
    
    // 尾部切片
    let s3 = &arr[2..]; // [3, 4, 5]
    
    // 中间切片
    let s4 = &arr[1..4]; // [2, 3, 4]
    
    println!("s1: {:?}, s2: {:?}, s3: {:?}, s4: {:?}", s1, s2, s3, s4);
}
```

#### 3.3.3.3 切片的内存布局

下面这张图说明切片与底层数组的关系：切片自己只是一对（指针，长度）。

```mermaid
graph TB
    subgraph "数组 arr"
        A1[1]
        A2[2]
        A3[3]
        A4[4]
        A5[5]
    end
    
    subgraph "切片 slice = &arr[1..4]"
        S1["ptr → arr[1]"]
        S2["len: 3"]
    end
    
    S1 -.-> A2
```

```rust
use std::mem;

fn main() {
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[1..4];
    
    // 切片大小 = 指针 + 长度
    println!("&[i32] 大小: {} 字节", mem::size_of::<&[i32]>()); // 16 (64位)
    // = 8 字节（ptr）+ 8 字节（len）
    
    // 切片指向原数组
    println!("切片长度: {}", slice.len()); // 3
    println!("切片首元素: {}", slice[0]); // 2
}
```

#### 3.3.3.4 字符串切片 &str 对应字节切片 &[u8]

`&str` 可以看成带 UTF-8 保证的 `&[u8]`，必要时也能转成字节切片来处理。

```rust
fn main() {
    let s = "hello";
    let slice = &s[1..4];
    
    println!("&str 切片: {}", slice); // ell
    
    // &str 底层是 &[u8]
    let bytes: &[u8] = s.as_bytes();
    let byte_slice = &bytes[1..4];
    println!("&[u8] 切片: {:?}", byte_slice); // [101, 108, 108]
    
    // 字符集合切片（注意：这是 Vec<char> 的切片，不是 &str）
    let chars: Vec<char> = s.chars().collect();
    println!("字符切片: {:?}", &chars[1..4]); // ['e', 'l', 'l']
}
```

### 3.3.4 多维数组

#### 3.3.4.1 [[T; N]; M] 二维数组

把数组嵌套起来就得到二维结构，`[[i32; 3]; 2]` 表示 2 行、每行 3 个元素。

```rust
fn main() {
    // [[T; N]; M] - M 行，每行 N 个元素
    let matrix: [[i32; 3]; 2] = [
        [1, 2, 3],
        [4, 5, 6],
    ];
    
    println!("矩阵: {:?}", matrix);
    println!("matrix[0]: {:?}", matrix[0]); // [1, 2, 3]
    println!("matrix[1][2]: {}", matrix[1][2]); // 6
}
```

#### 3.3.4.2 访问方式

二维数组用 `arr[i][j]` 逐层索引，行列顺序在类型里已经写死。

```rust
fn main() {
    let arr = [[1, 2, 3], [4, 5, 6]];
    
    // 双下标访问
    for i in 0..2 {
        for j in 0..3 {
            print!("{} ", arr[i][j]);
        }
        println!();
    }
    
    // 输出：
    // 1 2 3
    // 4 5 6
}
```

#### 3.3.4.3 多维数组作为函数参数

多维数组作参数时维度也固定在类型中，工程里更常见的做法是传切片。

```rust
fn main() {
    let matrix = [[1.0, 2.0], [3.0, 4.0]];
    print_matrix(&matrix);
}

fn print_matrix(m: &[[f64; 2]; 2]) {
    for row in m {
        println!("{:?}", row);
    }
}
```

---

## 3.4 结构体（Struct）

结构体是 Rust 中最重要的自定义类型之一。它允许你将多个不同类型的数据组合在一起，形成一个有意义的整体。

### 3.4.1 命名字段结构体

#### 3.4.1.1 struct 定义语法

结构体把若干个有名字的字段组合成一个新类型，每个字段都要写清类型。

```rust
// 定义结构体
struct User {
    name: String,
    email: String,
    age: u32,
    active: bool,
}

fn main() {
    // 创建结构体实例
    let user = User {
        name: String::from("Alice"),
        email: String::from("alice@example.com"),
        age: 30,
        active: true,
    };
    
    println!("用户: {} <{}>", user.name, user.email);
}
```

#### 3.4.1.2 字段访问

用点号访问结构体字段，能否修改由绑定本身的可变性决定。

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect = Rectangle { width: 30, height: 50 };
    
    // 通过点号访问字段
    println!("宽: {}, 高: {}", rect.width, rect.height);
    
    // 修改字段（需要 mut）
    let mut rect2 = Rectangle { width: 10, height: 20 };
    rect2.width = 15;
    println!("修改后宽: {}", rect2.width);
}
```

#### 3.4.1.3 字段初始化简写语法

当局部变量名与字段名相同时，可以省略字段名只写一次。

```rust
struct User {
    name: String,
    email: String,
    age: u32,
}

fn main() {
    let name = String::from("Bob");
    let email = String::from("bob@example.com");
    let age = 25;
    
    // 字段初始化简写：变量名和字段名相同时可以省略
    let user = User {
        name, // 等价于 name: name
        email, // 等价于 email: email
        age,
    };
    
    println!("用户: {} <{}>", user.name, user.email);
}
```

#### 3.4.1.4 所有权字段

字段里放 `String` 这类拥有所有权的类型时，结构体整体也就拥有这些数据，移动语义随之而来。

```rust
struct Person {
    name: String, // 所有权字段
    age: u32,
}

fn main() {
    let p = Person {
        name: String::from("Alice"),
        age: 30,
    };
    
    // name 是 String，拥有所有权
    // 如果把 Person 赋值给另一个变量，name 会被移动
    let p2 = p;
    // println!("{}", p.name); // 编译错误！p.name 已移动到 p2
    
    println!("{}", p2.name);
}
```

### 3.4.2 元组结构体

#### 3.4.2.1 元组结构体定义

元组结构体只有类型、没有字段名，适合做轻量包装。

```rust
// 元组结构体：没有字段名，只有类型
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let black = Color(0, 0, 0);
    let origin = Point(0, 0, 0);
    
    // 通过索引访问
    println!("黑色: R={}, G={}, B={}", black.0, black.1, black.2);
    println!("原点: x={}, y={}, z={}", origin.0, origin.1, origin.2);
}
```

#### 3.4.2.2 通过索引访问字段

元组结构体的字段用 `.0`、`.1` 访问，常见做法是配合 `impl` 提供构造函数。

```rust
struct RGB(u8, u8, u8);

impl RGB {
    fn new(r: u8, g: u8, b: u8) -> Self {
        RGB(r, g, b)
    }
    
    fn brightness(&self) -> u8 {
        (self.0 as f64 * 0.3 + self.1 as f64 * 0.59 + self.2 as f64 * 0.11) as u8
    }
}

fn main() {
    let red = RGB::new(255, 0, 0);
    let green = RGB(0, 255, 0);
    let blue = RGB(0, 0, 255);
    
    println!("红色亮度: {}", red.brightness());
    println!("绿色亮度: {}", green.brightness());
    println!("蓝色亮度: {}", blue.brightness());
}
```

#### 3.4.2.3 何时使用元组结构体

需要区分语义但又不必给每个字段命名时，元组结构体比完整结构体更简洁。

```rust
// 场景1：轻量级聚合
struct Pair(i32, i32);

// 场景2：区分类型
struct Kilometers(i32);
struct Miles(i32);

fn main() {
    let distance_km = Kilometers(100);
    let distance_mi = Miles(62);
    
    // 防止混淆：Kilometers 和 Miles 是不同类型
    // println!("{}", distance_km + distance_mi); // 编译错误！
}
```

### 3.4.3 单元结构体

#### 3.4.3.1 struct Foo;

单元结构体没有任何字段，主要用途是承载 trait 实现或充当类型标记。

```rust
// 单元结构体：没有任何字段
struct Marker;

// 用途1：实现 trait
trait Printable {
    fn print(&self);
}

struct Empty;

impl Printable for Empty {
    fn print(&self) {
        println!("Empty");
    }
}

fn main() {
    let marker = Marker;
    let empty = Empty;
    empty.print();
}
```

#### 3.4.3.2 单元结构体的作用

借助 `PhantomData`，单元结构体还能在类型层面携带信息而不占用运行时空间。

```rust
// PhantomData：用于标记类型
use std::marker::PhantomData;

struct PhantomTuple<T>(PhantomData<T>);

struct PhantomStruct<T> {
    data: PhantomData<T>,
}

fn main() {
    // PhantomData 不占用实际空间
    let _t: PhantomTuple<i32> = PhantomTuple(PhantomData);
    let _s: PhantomStruct<String> = PhantomStruct { data: PhantomData };
    
    println!("PhantomData 大小: {}", std::mem::size_of::<PhantomData<i32>>());
}
```

### 3.4.4 结构体更新语法

#### 3.4.4.1 ..default

先用 `Default::default()` 造出默认值，再用 `..` 覆盖要改的字段。

```rust
#[derive(Default)]
struct Config {
    host: String,
    port: u16,
    debug: bool,
}

fn main() {
    let default_config = Config::default();
    
    // ..default 填充剩余字段
    let config = Config {
        host: String::from("localhost"),
        port: 8080,
        ..Default::default()
    };
    
    println!("配置: {}:{}", config.host, config.port);
}
```

#### 3.4.4.2 ..other_instance

也可以从另一个同类型实例「继承」剩余字段，注意这会把未列出的字段移动过来。

```rust
struct User {
    name: String,
    email: String,
    age: u32,
    active: bool,
}

fn main() {
    let user1 = User {
        name: String::from("Alice"),
        email: String::from("alice@example.com"),
        age: 30,
        active: true,
    };
    
    // 从 user1 获取其余字段，但修改 name
    // 注意：email 是 String（所有权类型），会被移动而不是复制！
    let user2 = User {
        name: String::from("Bob"),
        ..user1 // 其余字段从 user1 获取（email 被移动，age 和 active 被复制）
    };
    
    println!("user1 name: {}", user1.name); // user1.email 已被移动到 user2
    println!("user2: {} <{}>", user2.name, user2.email);
    println!("user2 age: {}", user2.age); // 30（age 是 Copy 类型，从 user1 复制）
}
```

### 3.4.5 结构体方法

#### 3.4.5.1 impl 块定义方法

`impl` 块为结构体添加方法，方法与字段访问共用同一套点号语法。

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

// 方法放在 impl 块中
impl Rectangle {
    // self 参数
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect = Rectangle { width: 30, height: 50 };
    println!("面积: {}", rect.area()); // 1500
}
```

#### 3.4.5.2 &self 参数

`&self` 是不可变借用，方法只能读取字段。

```rust
struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Self {
        Counter { count: 0 }
    }
    
    // &self：不可变借用
    fn value(&self) -> u32 {
        self.count
    }
}

fn main() {
    let counter = Counter::new();
    println!("计数器: {}", counter.value()); // 0
}
```

#### 3.4.5.3 &mut self 参数

`&mut self` 允许方法修改字段，同一时刻只能存在一个可变借用。

```rust
struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Self {
        Counter { count: 0 }
    }
    
    // &mut self：可变借用
    fn increment(&mut self) {
        self.count += 1;
    }
    
    fn value(&self) -> u32 {
        self.count
    }
}

fn main() {
    let mut counter = Counter::new();
    counter.increment();
    counter.increment();
    counter.increment();
    println!("计数器: {}", counter.value()); // 3
}
```

#### 3.4.5.4 self 参数

`self` 按值接收，方法会把实例消费掉，适合做「转换」类的操作。

```rust
struct Person {
    name: String,
}

impl Person {
    fn new(name: &str) -> Self {
        Person { name: String::from(name) }
    }
    
    // self：获取所有权，消耗结构体
    fn into_string(self) -> String {
        self.name
    }
}

fn main() {
    let person = Person::new("Alice");
    let name = person.into_string(); // person 被消耗
    // println!("{}", person.name); // 编译错误！
    println!("名字: {}", name);
}
```

### 3.4.6 关联函数

#### 3.4.6.1 不带 self 的函数

关联函数不接收 `self`，通过 `类型名::函数名` 调用，通常用作构造函数。

```rust
struct Point {
    x: f64,
    y: f64,
}

impl Point {
    // 关联函数：不带 self 参数
    fn origin() -> Self {
        Point { x: 0.0, y: 0.0 }
    }
    
    fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }
    
    fn distance_from_origin(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let p1 = Point::origin();
    let p2 = Point::new(3.0, 4.0);
    
    println!("p1: ({}, {})", p1.x, p1.y);
    println!("p2 到原点距离: {:.2}", p2.distance_from_origin());
}
```

#### 3.4.6.2 构造函数模式

Rust 没有专门的构造语法，惯例是提供 `new` 这样的关联函数返回 `Self`。

```rust
struct User {
    name: String,
    email: String,
    age: u32,
}

impl User {
    // 构造函数
    fn new(name: &str, email: &str, age: u32) -> Self {
        User {
            name: String::from(name),
            email: String::from(email),
            age,
        }
    }
    
    // 静态工厂方法
    fn with_age_0(name: &str, email: &str) -> Self {
        User {
            name: String::from(name),
            email: String::from(email),
            age: 0,
        }
    }
}

fn main() {
    let user1 = User::new("Alice", "alice@example.com", 30);
    let user2 = User::with_age_0("Bob", "bob@example.com");
    
    println!("user1: {} ({}岁)", user1.name, user1.age);
    println!("user2: {} ({}岁)", user2.name, user2.age);
}
```

#### 3.4.6.3 多 impl 块

同一个类型可以写多个 `impl` 块，常按功能分组或配合泛型约束拆分。

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

// 第一块：构造函数
impl Rectangle {
    fn new(width: u32, height: u32) -> Self {
        Rectangle { width, height }
    }
}

// 第二块：只读方法
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
    
    fn perimeter(&self) -> u32 {
        2 * (self.width + self.height)
    }
}

// 第三块：可变方法
impl Rectangle {
    fn scale(&mut self, factor: u32) {
        self.width *= factor;
        self.height *= factor;
    }
}

fn main() {
    let rect = Rectangle::new(10, 20);
    println!("面积: {}, 周长: {}", rect.area(), rect.perimeter());
}
```

### 3.4.7 结构体与所有权

#### 3.4.7.1 字段的可变性规则

`let mut` 控制的是整个结构体绑定的可变性，不能单独把某个字段设为可变。

```rust
struct Counter {
    count: u32,
}

fn main() {
    // 结构体整体是可变的，不是个别字段
    let mut counter = Counter { count: 0 };
    counter.count = 5; // OK
    
    let counter2 = Counter { count: 0 };
    // counter2.count = 5; // 编译错误！counter2 是不可变的
}
```

#### 3.4.7.2 结构体的移动行为

只要字段里有非 `Copy` 类型，结构体赋值的默认行为就是移动。

```rust
struct Person {
    name: String,
    age: u32,
}

fn main() {
    let p1 = Person {
        name: String::from("Alice"),
        age: 30,
    };
    
    let p2 = p1; // 整个结构体移动，包括 name
    
    // println!("{}", p1.name); // 编译错误！
    println!("{}", p2.name); // OK
}
```

#### 3.4.7.3 Copy 类型字段的结构体

所有字段都实现 `Copy` 且派生了 `Copy` 时，结构体赋值才会复制而不是移动。

```rust
#[derive(Copy, Clone)]
struct Point {
    x: f64,
    y: f64,
}

fn main() {
    let p1 = Point { x: 1.0, y: 2.0 };
    let p2 = p1; // Copy！p1 仍然有效
    
    println!("p1: ({}, {})", p1.x, p1.y);
    println!("p2: ({}, {})", p2.x, p2.y);
}
```

---

## 3.5 枚举（Enum）

枚举是 Rust 中表示"一个值可以是几种类型之一"的类型。它比结构体更灵活，因为不同的变体可以携带不同的数据。

### 3.5.1 枚举的定义与基本使用

#### 3.5.1.1 枚举的定义

枚举列出所有可能的取值，每个取值叫一个变体。

```rust
// 定义枚举
enum Direction {
    North,
    South,
    East,
    West,
}

fn main() {
    // 使用枚举值
    let direction = Direction::North;
    
    match direction {
        Direction::North => println!("向北"),
        Direction::South => println!("向南"),
        Direction::East => println!("向东"),
        Direction::West => println!("向西"),
    }
}
```

#### 3.5.1.2 带数据的枚举变体

变体可以携带数据，而且不同变体携带的数据形态可以完全不同。

```rust
enum Message {
    Quit,                      // 无数据
    Move { x: i32, y: i32 }, // 命名字段
    Write(String),             // 单个值
    ChangeColor(i32, i32, i32), // 多个值
}

fn main() {
    let quit = Message::Quit;
    let move_msg = Message::Move { x: 10, y: 20 };
    let write_msg = Message::Write(String::from("hello"));
    let color_msg = Message::ChangeColor(255, 0, 0);
}
```

#### 3.5.1.3 枚举的内存布局

带数据的枚举在内存里通常是「标签 + 最大变体的载荷」，具体布局由编译器决定。

```mermaid
graph TB
    subgraph 枚举 Message
        V1[Quit]
        V2[Move]
        V3[Write]
        V4[ChangeColor]
    end
    
    subgraph 内存
        T1[判别式 + 数据]
    end
```

```rust
use std::mem;

fn main() {
    enum Message {
        Quit,
        Move { x: i32, y: i32 },
        Write(String),
        ChangeColor(i32, i32, i32),
    }
    
    // Message 的大小是最大变体的大小 + 判别式
    println!("Message 大小: {} 字节", std::mem::size_of::<Message>());
    
    // 注意：不能直接对枚举变体调用 size_of
    // 但我们可以通过推断知道 Quit 变体本身不占空间
    println!("单元变体大小为 0");
}
```

### 3.5.2 Option<T> 枚举详解

#### 3.5.2.1 Option::Some / Option::None

标准库的 `Option<T>` 只有两个变体，它把「可能没有值」写进了类型系统。

```rust
fn main() {
    // Option<T> 定义在标准库中：
    // enum Option<T> {
    //     None,
    //     Some(T),
    // }
    
    let some_value: Option<i32> = Some(42);
    let no_value: Option<i32> = None;
    
    println!("some_value: {:?}", some_value); // Some(42)
    println!("no_value: {:?}", no_value); // None
}
```

#### 3.5.2.2 Option 的设计哲学

`Option` 取代了可空指针的角色：`None` 必须被显式处理，编译器会盯着你。

```rust
fn main() {
    // Option 替代了其他语言的 null
    // 好处：编译器强制你处理 None 的情况！
    let names = vec!["Alice", "Bob", "Charlie"];
    
    // 其他语言可能返回 null，Rust 返回 Option
    let first = names.get(0);
    println!("第一个名字: {:?}", first); // Some("Alice")
    
    let tenth = names.get(9);
    println!("第十个名字: {:?}", tenth); // None（安全！编译器会提醒你处理）
}
```

#### 3.5.2.3 unwrap / expect / unwrap_unchecked

这三个方法在 `None` 时都会 panic，区别只在报错信息是否自定义。

```rust
fn main() {
    let some = Some(42);
    
    // unwrap：如果是 Some 返回值，否则 panic
    println!("unwrap: {}", some.unwrap()); // 42
    
    // expect：类似 unwrap，但可以自定义错误信息
    println!("expect: {}", some.expect("应该是 Some")); // 42
    
    // unwrap_unchecked：如果是 Some 返回值，否则未定义行为
    unsafe {
        println!("unwrap_unchecked: {}", some.unwrap_unchecked()); // 42
    }
}
```

#### 3.5.2.4 unwrap_or / unwrap_or_else / unwrap_or_default

不想 panic 时，用这组方法提供兜底值或兜底计算。

```rust
fn main() {
    let some = Some(42);
    let none: Option<i32> = None;
    
    // unwrap_or：有默认值
    println!("some.unwrap_or(0): {}", some.unwrap_or(0)); // 42
    println!("none.unwrap_or(0): {}", none.unwrap_or(0)); // 0
    
    // unwrap_or_else：延迟计算默认值
    println!("none.unwrap_or_else(|| 100): {}", none.unwrap_or_else(|| 100)); // 100
    
    // unwrap_or_default：使用类型的默认值
    println!("none.unwrap_or_default(): {}", none.unwrap_or_default()); // 0
}
```

#### 3.5.2.5 map / and_then / or / or_else / filter / flatten

这组组合子让 `Option` 的链式处理不必层层写 `match`。

```rust
fn main() {
    let some = Some(5);
    let none: Option<i32> = None;
    
    // map：转换内部值
    let doubled = some.map(|x| x * 2);
    println!("doubled: {:?}", doubled); // Some(10)
    
    let doubled_none = none.map(|x| x * 2);
    println!("doubled_none: {:?}", doubled_none); // None
    
    // and_then：链式处理
    let result = some.and_then(|x| Some(x * 3));
    println!("and_then: {:?}", result); // Some(15)
    
    // or / or_else：提供默认值或备用计算
    let result = none.or(Some(100));
    println!("or: {:?}", result); // Some(100)
    
    // filter：注意闭包收到的是 &T（内部值的引用），所以要解引用
    let result = some.filter(|x| *x > 10);
    println!("filter (5 > 10): {:?}", result); // None
    
    let result = some.filter(|x| *x < 10);
    println!("filter (5 < 10): {:?}", result); // Some(5)
}
```

#### 3.5.2.6 is_some / is_none / as_ref / as_mut

检查与借用类方法不会消耗 `Option`，`as_ref` 用来把 `Option<T>` 转成 `Option<&T>`。

```rust
fn main() {
    let some = Some(42);
    let none: Option<i32> = None;
    
    // is_some / is_none
    println!("some.is_some(): {}", some.is_some()); // true
    println!("none.is_none(): {}", none.is_none()); // true
    
    // as_ref：转换为 &Option<T>
    let some_ref: Option<&i32> = some.as_ref();
    println!("as_ref: {:?}", some_ref); // Some(42)
    
    // as_mut：转换为 &mut Option<T>
    let mut some_mut = Some(42);
    if let Some(value) = some_mut.as_mut() {
        *value = 100;
    }
    println!("as_mut: {:?}", some_mut); // Some(100)
}
```

### 3.5.3 Result<T, E> 枚举详解

#### 3.5.3.1 Result::Ok / Result::Err

`Result<T, E>` 用两个变体区分成功与失败，并各自携带类型信息。

```rust
fn main() {
    // Result<T, E> 定义在标准库中：
    // enum Result<T, E> {
    //     Ok(T),
    //     Err(E),
    // }
    
    let ok: Result<i32, &str> = Ok(42);
    let err: Result<i32, &str> = Err("出错了");
    
    println!("ok: {:?}", ok);
    println!("err: {:?}", err);
}
```

#### 3.5.3.2 unwrap / expect / unwrap_err

`unwrap_err` 在成功时 panic，是 `unwrap` 的反面，常用于测试。

```rust
fn main() {
    let ok: Result<i32, &str> = Ok(42);
    let err: Result<i32, &str> = Err("出错了");
    
    // unwrap：Ok 返回值，Err panic
    println!("ok.unwrap(): {}", ok.unwrap()); // 42
    // err.unwrap(); // panic!
    
    // expect：自定义错误信息
    println!("ok.expect(): {}", ok.expect("应该是 Ok")); // 42
    
    // unwrap_err：Ok panic，Err 返回值
    println!("err.unwrap_err(): {}", err.unwrap_err()); // 出错了
}
```

#### 3.5.3.3 unwrap_or / unwrap_or_else / unwrap_or_default

与 `Option` 的同类方法一样，这组方法给出失败时的兜底值。

```rust
fn main() {
    let ok: Result<i32, &str> = Ok(42);
    let err: Result<i32, &str> = Err("error");
    
    // unwrap_or
    println!("ok.unwrap_or(0): {}", ok.unwrap_or(0)); // ok.unwrap_or(0): 42
    println!("err.unwrap_or(0): {}", err.unwrap_or(0)); // err.unwrap_or(0): 0
    
    // unwrap_or_else：闭包接收的是那个错误值，所以参数不能省
    println!("err.unwrap_or_else(|_| -1): {}", err.unwrap_or_else(|_| -1)); // -1
    
    // unwrap_or_default：用 T 的 Default 实现兜底
    println!("err.unwrap_or_default(): {}", err.unwrap_or_default()); // 0
}
```

#### 3.5.3.4 map / map_err / and_then / or / or_else

`map` 只改成功值，`map_err` 只改错误值，`and_then` 用于串联可能失败的下一步。

```rust
fn main() {
    let ok: Result<i32, &str> = Ok(5);
    let err: Result<i32, &str> = Err("error");
    
    // map：转换 Ok 值
    let doubled = ok.map(|x| x * 2);
    println!("map: {:?}", doubled); // Ok(10)
    
    // map_err：转换 Err 值
    let mapped_err = err.map_err(|e| format!("错误: {}", e));
    println!("map_err: {:?}", mapped_err); // Err("错误: error")
    
    // and_then：链式处理
    let result = ok.and_then(|x| Ok(x * 3));
    println!("and_then: {:?}", result); // Ok(15)
}
```

#### 3.5.3.5 ? 操作符（错误传播）

`?` 在出错时提前返回，并自动做一次 `From` 转换，是错误传播最简洁的写法。

```rust
use std::num::ParseIntError;

fn parse_and_double(s: &str) -> Result<i32, ParseIntError> {
    let num: i32 = s.parse()?; // ? 操作符
    Ok(num * 2)
}

fn main() {
    let result = parse_and_double("21");
    println!("result: {:?}", result); // Ok(42)
    
    let result = parse_and_double("not a number");
    println!("result: {:?}", result); // Err(ParseIntError)
}
```

#### 3.5.3.6 is_ok / is_err / as_ref / as_mut / as_deref

与 `Option` 对应的一组检查与借用方法；其中 `as_deref` 会在 `T: Deref` 时把 `Result<T, E>` 借成 `Result<&T::Target, &E>`。

```rust
fn main() {
    let ok: Result<i32, &str> = Ok(42);
    let err: Result<i32, &str> = Err("error");
    
    // is_ok / is_err
    println!("ok.is_ok(): {}", ok.is_ok()); // true
    println!("err.is_err(): {}", err.is_err()); // true
    
    // as_ref：把 Result<T, E> 变成 Result<&T, &E>
    // 因为这里的 E 本身就是 &str，所以拿到的是 Result<&i32, &&str>
    let ok_ref: Result<&i32, &&str> = ok.as_ref();
    println!("as_ref: {:?}", ok_ref); // Ok(42)
    
    // as_mut：变成 Result<&mut T, &mut E>
    let mut ok_mut: Result<i32, &str> = Ok(42);
    if let Ok(v) = ok_mut.as_mut() {
        *v = 100;
    }
    println!("as_mut: {:?}", ok_mut); // Ok(100)
}
```

### 3.5.4 match 与枚举的完整匹配

#### 3.5.4.1 match 穷尽匹配要求

`match` 必须覆盖枚举的所有变体，漏掉分支编译不过，这正是它比 `if` 更安全的地方。

```rust
enum Direction {
    North,
    South,
    East,
    West,
}

fn main() {
    let direction = Direction::North;
    
    // 必须穷尽所有情况！
    match direction {
        Direction::North => println!("向北"),
        Direction::South => println!("向南"),
        Direction::East => println!("向东"),
        Direction::West => println!("向西"),
    }
}
```

#### 3.5.4.2 解构枚举变体

分支模式可以顺着变体把内部数据取出来，结构体风格与元组风格的变体各有对应写法。

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::Move { x: 10, y: 20 };
    
    match msg {
        Message::Quit => println!("退出"),
        Message::Move { x, y } => println!("移动到 ({}, {})", x, y),
        Message::Write(text) => println!("写入: {}", text),
        Message::ChangeColor(r, g, b) => println!("颜色: RGB({}, {}, {})", r, g, b),
    }
}
```

#### 3.5.4.3 if let 简化单分支匹配

只关心某一个变体时，`if let` 比写完整 `match` 更省事。

```rust
enum Message {
    Move { x: i32, y: i32 },
    Quit,
}

fn main() {
    let msg = Message::Move { x: 10, y: 20 };
    
    // 完整 match
    match msg {
        Message::Move { x, y } => println!("移动到 ({}, {})", x, y),
        Message::Quit => println!("退出"),
    }
    
    // if let 简化：只关心其中一种情况
    if let Message::Move { x, y } = msg {
        println!("移动到 ({}, {})", x, y); // 移动到 (10, 20)
    }
}
```

### 3.5.5 枚举的方法实现

#### 3.5.5.1 impl enum 块

枚举和结构体一样可以用 `impl` 添加方法，`match self` 是方法体内最常见的入口。

```rust
#[derive(Debug)]
enum Direction {
    North,
    South,
    East,
    West,
}

impl Direction {
    fn opposite(&self) -> Direction {
        match self {
            Direction::North => Direction::South,
            Direction::South => Direction::North,
            Direction::East => Direction::West,
            Direction::West => Direction::East,
        }
    }
    
    fn is_vertical(&self) -> bool {
        matches!(self, Direction::North | Direction::South)
    }
}

fn main() {
    println!("North 反向: {:?}", Direction::North.opposite()); // North 反向: South
    println!("East 是垂直? {}", Direction::East.is_vertical()); // false
}
```

#### 3.5.5.2 #[derive(...)] 在枚举上的行为差异

派生宏能否用在枚举上取决于变体是否满足条件，例如含 `String` 的变体就不能 `Copy`。

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
enum Color {
    Red,
    Green,
    Blue,
}

fn main() {
    let c1 = Color::Red;
    let c2 = Color::Red;
    
    // Debug
    println!("{:?}", c1); // Red
    
    // Clone
    let c3 = c1.clone();
    
    // Copy
    let c4 = c1;
    
    // PartialEq
    println!("c1 == c2: {}", c1 == c2); // true
}
```

---

## 3.6 模式匹配（Pattern Matching）

模式匹配是 Rust 最强大的特性之一。它允许你检查一个值是否符合某种"模式"，并解构出其中的数据。

### 3.6.1 match 完整语法

#### 3.6.1.1 基本 match 表达式

`match` 逐个比较分支模式，第一个匹配上的分支获胜。

```rust
fn main() {
    let x = 3;
    
    let result = match x {
        1 => "one",
        2 => "two",
        3 => "three",
        _ => "other",
    };
    
    println!("x 是 {}", result); // x 是 three
}
```

#### 3.6.1.2 match 作为表达式

`match` 是表达式，各分支的返回值类型必须一致，结果可以直接赋给变量。

```rust
fn main() {
    // match 是表达式，可以返回值
    let number = 7;
    let description = match number {
        1 => "一",
        2 => "二",
        3 => "三",
        _ => "其他",
    };
    
    println!("数字 {} 是{}", number, description);
}
```

#### 3.6.1.3 match 的求值顺序

下图强调 `match` 自上而下顺序匹配，`_` 一旦出现，后面的分支就再也轮不到。

```mermaid
graph LR
    A[match 表达式] --> B[按顺序检查分支]
    B --> C{匹配?}
    C -->|是| D[执行分支体]
    C -->|否| E[检查下一个分支]
    E --> B
```

```rust
fn main() {
    // Rust 不保证 match 分支的求值顺序
    // 不应该依赖特定的执行顺序
    
    let x = 5;
    match x {
        _ => println!("默认分支"),
    }
}
```

### 3.6.2 解构模式

#### 3.6.2.1 解构元组

模式可以一次拆开元组里的所有元素。

```rust
fn main() {
    let tuple = (1, "hello", 3.14);
    
    let (a, b, c) = tuple;
    println!("a={}, b={}, c={}", a, b, c);
    
    // 部分解构
    let (first, .., last) = tuple;
    println!("first={}, last={}", first, last);
}
```

#### 3.6.2.2 解构结构体

结构体模式按字段名解构，用 `..` 可以忽略剩余字段。

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 10, y: 20 };
    
    // 解构结构体
    let Point { x, y } = p;
    println!("x={}, y={}", x, y);
    
    // 解构时重命名
    let Point { x: px, y: py } = p;
    println!("px={}, py={}", px, py);
    
    // 解构时忽略字段
    let Point { x, .. } = p;
    println!("x={}", x);
}
```

#### 3.6.2.3 解构枚举

枚举模式先写出变体名，再按该变体的数据形态继续拆解。

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn main() {
    let msg = Message::Move { x: 10, y: 20 };
    
    match msg {
        Message::Quit => println!("退出"),
        Message::Move { x, y } => println!("移动到 ({}, {})", x, y),
        Message::Write(text) => println!("写入: {}", text),
    }
}
```

#### 3.6.2.4 解构嵌套模式

模式可以任意嵌套，一层层剥开 `Option`、元组和结构体。

```rust
fn main() {
    let nested = Some(Some(42));
    
    match nested {
        Some(Some(value)) => println!("值: {}", value),
        Some(None) => println!("内层是 None"),
        None => println!("外层是 None"),
    }
}
```

### 3.6.3 匹配守卫（Match Guard）

#### 3.6.3.1 if 条件附加在分支后

分支后面可以加 `if` 守卫，只有守卫为真时该分支才成立。

```rust
fn main() {
    let num = Some(7);
    
    match num {
        Some(x) if x > 5 => println!("大于5: {}", x), // 匹配！
        Some(x) if x <= 5 => println!("小于等于5: {}", x),
        // ⚠️ 关键点：带 if 的匹配臂不算"穷尽"！
        // 编译器会认为 Some 还可能没被覆盖，所以必须补一个兜底分支
        Some(_) => println!("Some，但没匹配上任何带条件的分支"),
        None => println!("没有值"),
    }
}
```

#### 3.6.3.2 多条件组合

用 `|` 把多个模式并在一起，它们会共用同一个分支体。

```rust
fn main() {
    let x = 4;
    let y = true;
    
    match x {
        // x == 4 且 y == true
        4 if y => println!("x 是 4 且 y 为真"),
        // x == 4 且 y == false
        4 if !y => println!("x 是 4 且 y 为假"),
        // x 是其他值
        _ => println!("其他情况"),
    }
}
```

### 3.6.4 范围与多值匹配

#### 3.6.4.1 范围模式

`..=` 可以写出闭区间模式，两个端点本身也包含在内。

```rust
fn main() {
    let score = 85;
    
    match score {
        90..=100 => println!("等级: A"),
        80..=89 => println!("等级: B"),
        70..=79 => println!("等级: C"),
        60..=69 => println!("等级: D"),
        _ => println!("等级: F"),
    }
    
    // 字符范围
    let grade = 'C';
    match grade {
        'A'..='C' => println!("通过了！"),
        'D'..='F' => println!("需要补考"),
        _ => println!("无效等级"),
    }
}
```

#### 3.6.4.2 多值匹配

字符和数字都可以用 `|` 并列写出多个备选值。

```rust
fn main() {
    let c = 'e';
    
    match c {
        'a' | 'e' | 'i' | 'o' | 'u' => println!("{} 是元音", c),
        'a'..='z' => println!("{} 是辅音", c),
        _ => println!("{} 不是字母", c),
    }
}
```

#### 3.6.4.3 数值范围 vs 字符范围

范围模式既可用于数值也可用于 `char`，比较的是码点顺序。

```rust
fn main() {
    // 数值范围
    match 50 {
        1..=50 => println!("在 1-50 之间"),
        51..=100 => println!("在 51-100 之间"),
        _ => println!("其他"),
    }
    
    // 字符范围
    match 'k' {
        'a'..='j' => println!("a-j 范围"),
        'k'..='t' => println!("k-t 范围"), // 匹配！
        'u'..='z' => println!("u-z 范围"),
        _ => println!("其他"),
    }
}
```

### 3.6.5 @ 绑定

#### 3.6.5.1 x @ 1..=5

`@` 在判断范围的同时，把匹配到的值绑定到变量上。

```rust
fn main() {
    let score = 85;
    
    match score {
        // 匹配 80..=89 范围，同时绑定到 grade 变量
        grade @ 80..=89 => println!("等级 B (分数: {})", grade),
        grade @ 90..=100 => println!("等级 A (分数: {})", grade),
        grade => println!("其他分数: {}", grade),
    }
}
```

#### 3.6.5.2 @ 在解构中的使用

`@` 也可以出现在解构内部，把整个子结构或某个字段绑出来。

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 5, y: 10 };
    
    match p {
        // 匹配 x 在 0..20 之间，同时绑定整个点
        point @ Point { x: 0..=20, y: _ } => {
            println!("点在左侧区域: ({}, {})", point.x, point.y);
        }
        Point { x, y } => {
            println!("点在右侧区域: ({}, {})", x, y);
        }
    }
}
```

### 3.6.6 忽略剩余字段

#### 3.6.6.1 .. 忽略结构体剩余字段

结构体模式里的 `..` 表示「其余字段都不关心」。

```rust
struct Config {
    host: String,
    port: u16,
    debug: bool,
    timeout: u64,
}

fn main() {
    let config = Config {
        host: String::from("localhost"),
        port: 8080,
        debug: true,
        timeout: 30,
    };
    
    match config {
        // 只关心 host 和 port，忽略其他字段
        Config { host, port, .. } => {
            println!("{}:{}", host, port);
        }
    }
}
```

#### 3.6.6.2 .. 在元组和枚举中的使用

在元组和切片模式里，`..` 可以匹配任意多个元素，包括零个。

```rust
fn main() {
    // 元组中使用 ..
    let triple = (1, 2, 3, 4, 5);
    let (first, .., last) = triple;
    println!("first={}, last={}", first, last); // first=1, last=5
    
    // 枚举中使用 ..
    enum Message {
        Move { x: i32, y: i32, z: i32 },
    }
    
    let msg = Message::Move { x: 1, y: 2, z: 3 };
    
    match msg {
        Message::Move { x, y, .. } => {
            println!("移动到 ({}, {})", x, y);
        }
    }
}
```

### 3.6.7 if-let 与 while-let

#### 3.6.7.1 if let Some(x) = option

`if let` 只处理匹配成功的一种情况，其余情况走 `else`。

```rust
fn main() {
    let option = Some(42);
    
    // 完整 match
    match option {
        Some(x) => println!("有值: {}", x),
        None => println!("没有值"),
    }
    
    // if let 简化
    if let Some(x) = option {
        println!("有值（if let）: {}", x);
    }
}
```

#### 3.6.7.2 if let...else 变体

`if let ... else` 让「匹配」和「不匹配」两条路径都有落点。

```rust
fn main() {
    let option = Some(42);
    
    if let Some(x) = option {
        println!("有值: {}", x); // 有值: 42
    } else {
        println!("没有值");
    }
    
    // 带条件的 if let：Rust 2024 支持 let 链，用 && 把条件接在后面
    let option = Some(100);
    
    // 下面这种写法是错的（编译器会报 expected `{`, found keyword `if`）：
    // if let Some(x) = option if x > 50 { ... }
    if let Some(x) = option && x > 50 {
        println!("大于50的值: {}", x); // 大于50的值: 100
    } else {
        println!("小于等于50或没有值");
    }
}
```

#### 3.6.7.3 while let 循环模式

`while let` 在模式持续匹配时反复执行循环体，非常适合消费栈或迭代器。

```rust
fn main() {
    let mut stack = vec![1, 2, 3];
    
    // while let 循环
    while let Some(value) = stack.pop() {
        println!("弹出: {}", value);
    }
    
    // 等价的 loop match 写法
    let mut stack = vec![1, 2, 3];
    loop {
        match stack.pop() {
            Some(value) => println!("弹出: {}", value),
            None => break,
        }
    }
}
```

#### 3.6.7.4 matches! 宏

`matches!` 把「模式是否匹配」压缩成一个布尔表达式。

```rust
fn main() {
    // matches! 宏测试值是否匹配模式
    let value = 5;
    
    let is_small = matches!(value, 1..=5);
    println!("is_small: {}", is_small); // true
    
    // 枚举匹配
    enum Color {
        Red,
        Green,
        Blue,
    }
    
    let color = Color::Red;
    let is_primary = matches!(color, Color::Red | Color::Green | Color::Blue);
    println!("is_primary: {}", is_primary); // true
    
    // 带条件的匹配
    let num = 10;
    let is_positive_even = matches!(num, x if x > 0 && x % 2 == 0);
    println!("is_positive_even: {}", is_positive_even); // true
}
```

### 3.6.8 let 链中的模式匹配（Rust 2024）

#### 3.6.8.1 if let Some(x) = opt && x > 10

let 链把多个模式匹配和布尔条件合并到同一个条件表达式里。它从 rustc 1.88 起稳定，但**只在 Rust 2024 及之后的 edition 可用**——旧 edition 下编译器会直接报 `let chains are only allowed in Rust 2024 or later`。

```rust
fn main() {
    let option: Option<i32> = Some(42);

    // Rust 2024 之前：两层 if 嵌套
    if let Some(x) = option {
        if x > 10 {
            println!("大于10: {}", x); // 大于10: 42
        }
    }

    // Rust 2024 起：用 && 把条件接在模式后面
    if let Some(x) = option
        && x > 10
    {
        println!("大于10: {}", x);
    }

    // while 条件里同样可以使用 let 链
    let mut iter = vec![1, 2, 3].into_iter();
    while let Some(n) = iter.next()
        && n < 3
    {
        println!("n = {}", n); // 1、2
    }
}
```

---

## 本章小结

恭喜你完成了第三章"复合数据类型"的学习！🎉

在这一章中，我们深入探索了 Rust 的各种复合类型：

1. **字符串与字符串切片**：掌握了 `String` 和 `&str` 的区别、字符串的各种操作方法，以及 Unicode 处理。以后看到 emoji 再也不会"乱码"了！（大概吧...）

2. **元组**：学会了创建、访问、解构元组，以及元组作为函数返回值的使用。多个返回值？元组帮你打包带走！

3. **数组与切片**：了解了数组的固定大小特性、切片作为数据视图的工作原理，以及多维数组。数组虽"死"（不能动态增长），但切片让它重获新生！

4. **结构体**：掌握了命名字段结构体、元组结构体、单元结构体的定义和使用，以及方法实现。终于可以给数据类型"整容"了！

5. **枚举**：深入学习了枚举的定义、`Option<T>` 和 `Result<T, E>` 这两个标准库最重要的枚举，以及如何为枚举实现方法。告别空指针恐惧症，从 Rust 开始！

6. **模式匹配**：全面了解了 `match`、`if let`、`while let`、`matches!` 宏等模式匹配工具。这是 Rust 最"秀"的部分，好好练！

---

> 💡 **学习建议**：这一章的内容是 Rust 的核心基础，建议动手敲代码验证每一个例子。别光看不练，否则明天就会"战略性遗忘"！
