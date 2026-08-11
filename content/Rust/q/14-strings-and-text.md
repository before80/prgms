+++
title = "14-字符串与文本"
date = 2026-07-28T14:49:00+08:00
weight = 140
type = "docs"
description = "从 Go 视角讲清 String、&str、UTF-8、字符遍历与路径字符串"
isCJKLanguage = true
draft = false

+++

# 字符串与文本 (Strings and Text)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会把 `String`、`str`、`&str` 当成三种“差不多的字符串类型”，结果到处撞类型错误？
- 你是否想知道：Go 里 `s[0]`、`len(s)`、`[]byte` / `[]rune` 很自然，为什么 Rust 要拆开讲字节、字符、切片边界？
- 你是否遇到过 `error[E0277]`、`error[E0308]`、`error[E0382]`，却不知道它们分别在拦字符串索引、类型不匹配、还是拼接后的 move？
- 你会不会把路径/`OsStr` 直接当 `&str` 用，结果在 Windows 上踩非 UTF-8 文件名？
- 你是否希望有一份“参数写 `&str`、拥有用 `String`、遍历选 `chars`/`bytes`/`char_indices`”的日常心智模型？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| UTF-8 | UTF-8 | UTF-8 编码 | 把 Unicode 文本编成 1～4 字节可变长序列 | Go 的 `string` / `[]byte` 也是 UTF-8 |
| Unicode scalar | Unicode scalar value | Unicode 标量值 | 一个合法的 Unicode 码点；Rust 的 `char` 就是它 | Go 的 `rune` |
| `String` | — | 拥有型字符串 | 拥有堆上 UTF-8 缓冲区，可增长 | 可变 `[]byte` + 当文本用，近似 |
| `str` | — | 字符串切片类型本身 | 一段有效 UTF-8；是 DST，通常不单独当局部变量 | 无直接对应 |
| `&str` | — | 字符串切片借用 | 对 UTF-8 文本的只读胖指针视图 | `string` 头（指针+长度），近似 |
| fat pointer | — | 胖指针 | 除数据地址外还带长度等信息的指针 | slice 头 |
| **DST** | Dynamically Sized Type | 动态大小类型 | 编译期大小未知，必须通过指针使用 | 无直接对应 |
| `char` | — | 字符类型 | 一个 Unicode 标量值，固定 4 字节 | `rune` |
| grapheme cluster | — | 字形簇 | 用户眼里“一个字”，可能由多个标量值组成 | 需额外库；Go 也非 `rune` 直接等同 |
| `OsString` / `OsStr` | OS string | 操作系统字符串 | 平台原生字符串，不一定是有效 UTF-8 | `os` 包路径字符串，近似 |
| `Path` / `PathBuf` | — | 路径视图 / 拥有路径 | 专门表示文件系统路径的类型 | `path` / `filepath` |
| WTF-8 | Wobbly Transformation Format-8 | WTF-8 | Windows 上 Rust 用来无损表示任意 UTF-16 的内部编码 | Go 在 Windows 也有类似路径编码问题 |
| `Display` | — | 面向用户的格式化 | `{}` 用的“好看输出” | `fmt.Stringer`，近似 |
| `Debug` | — | 面向调试的格式化 | `{:?}` 用的“看结构输出” | `%#v` / `%+v`，近似 |
| move | — | 移动 / 转移 | 所有权从一边转给另一边，旧绑定失效 | Go 赋值后两边仍可用，不等价 |
| borrow | — | 借用 | 临时看或改，不接管所有权 | 传指针 / slice 头 |
| `Deref` | Dereference | 解引用强制转换 | 让 `&String` 在需要 `&str` 处自动适配 | 无直接对应 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q21](#q21) |
| `common` | [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q19](#q19), [Q20](#q20) |
| `occasional` | [Q15](#q15), [Q16](#q16), [Q17](#q17) |
| `advanced` | [Q18](#q18) |

---

## Q1. `String`、`str`、`&str` 到底是什么关系？ {#q1}
**Tags:** `hot` `beginner` `string` `str`
**适用版本:** Rust 1.0+

**一句话答案：**

`String` 拥有堆上 UTF-8 文本；`str` 是“一段有效 UTF-8”这个类型本身（**DST**，Dynamically Sized Type，动态大小类型）；日常几乎总通过 `&str`（胖指针借用）去用它。

**解答：**

先把三层拆开：

| 类型 | 角色 | 日常怎么出现 |
|------|------|--------------|
| `String` | 所有者，可增长 | `String::from("hi")`、`format!(...)` |
| `str` | 文本内容类型（DST） | 很少直接当局部变量类型写 |
| `&str` | 对 `str` 的借用视图 | `"hello"`、`&s[..]`、`s.as_str()` |

字符串字面量 `"hello"` 的类型是 `&'static str`：它指向程序里某处只读的 UTF-8 数据，生命周期覆盖整个程序。

```rust
fn main() {
    let owned: String = String::from("hello");
    let borrowed: &str = owned.as_str(); // 借用，不接管所有权
    let literal: &str = "world";         // &'static str
    println!("{owned} / {borrowed} / {literal}");
}
```

`&str` 是**胖指针**（fat pointer）：通常是「数据地址 + 字节长度」。它不拥有缓冲区，只是一段视图——和 [13-slices](../13-slices/#q1) 里的 `&[T]` 是同一类想法。

```rust
use std::mem::size_of;

fn main() {
    assert_eq!(size_of::<&str>(), size_of::<usize>() * 2);
    let s = String::from("rust");
    let view: &str = &s; // &String 可经 Deref 变成 &str
    println!("{view}");
}
```

需要记住：参数位置优先 `&str`（字面量和 `String` 借用都能传）；需要拥有、拼接、长期保存时再用 `String`。细节见 [Q17](#q17)。

```rust
fn greet(name: &str) {
    println!("hi, {name}");
}

fn main() {
    greet("Ada"); // 字面量
    let s = String::from("Bob");
    greet(&s); // &String -> &str
}
```

**Go 对比：**

```go
package main

import "fmt"

func greet(name string) {
	fmt.Println("hi,", name)
}

func main() {
	greet("Ada")
	s := "Bob"
	greet(s) // Go 的 string 赋值复制的是头，不是“所有权转移”
}
```

- **Go 怎么做**：几乎处处用 `string`；需要可变字节再用 `[]byte`。
- **Rust 为什么不同**：Rust 把“谁拥有缓冲区”和“谁只是在看”拆开，才能在编译期决定何时释放堆内存（见 [11-ownership](../11-ownership/#q1)）。
- **Go 程序员易踩的坑**：把 `String` 当成默认字符串类型；其实读文本参数多半该写 `&str`。

**记忆点：**

- `String` = 拥有；`&str` = 借用视图；`str` = 内容类型（DST）。
- `"hello"` 是 `&'static str`，不是 `String`。
- 参数优先 `&str`，拥有/修改用 `String`。

---

## Q2. 为什么 `String` 可增长而 `&str` 不能？ {#q2}
**Tags:** `hot` `beginner` `string` `mutability`
**适用版本:** Rust 1.0+

**一句话答案：**

`String` 拥有堆缓冲区，还能带着容量（capacity）扩容；`&str` 只是别人缓冲区上的只读切片视图，既不能 realloc，也不能保证背后数据可变。

**解答：**

`String` 内部大致是「指针 + 长度 + 容量」，和 `Vec<u8>` 很像，只是额外保证内容永远是有效 UTF-8。因此你可以 `push` / `push_str` / `reserve`：

```rust
fn main() {
    let mut s = String::from("he");
    s.push('l');
    s.push_str("lo");
    println!("{s}"); // hello
    println!("len={} cap={}", s.len(), s.capacity());
}
```

`&str` 没有 capacity，也不负责分配。它指向的可能是字面量、只读映射，或某个 `String` 的中间一段——视图本身不能“变长”：

```rust
fn main() {
    let s = "hello";
    // s.push_str("!"); // 方法不存在：&str 不能增长
    let mut owned = s.to_string(); // 先变成 String 才能改
    owned.push('!');
    println!("{owned}");
}
```

即便你拿到 `&mut str`，也只能做“同长度范围内的原地改写”这类受限操作，不能像 `String` 那样追加字节导致重分配。日常要增长文本，几乎总是 `mut String`。

```rust
fn append_bang(buf: &mut String) {
    buf.push('!');
}

fn main() {
    let mut s = String::from("hi");
    append_bang(&mut s);
    println!("{s}"); // hi!
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hi"
	// s += "!"  会分配新 string；原 string 值本身仍不可变
	b := []byte(s)
	b = append(b, '!')
	fmt.Println(string(b))
}
```

- **Go 怎么做**：`string` 不可变；要增长通常转 `[]byte` / `strings.Builder` 再拼回去。
- **Rust 为什么不同**：Rust 把“可增长所有者”直接做成 `String`，把“只读视图”做成 `&str`，类型上就分清职责。
- **Go 程序员易踩的坑**：对 `&str` 调用 `push_str`；应先 `to_string()` / `String::from`。

**记忆点：**

- 增长文本 → `mut String`。
- `&str` = 视图，不拥有、不扩容。
- 需要改别人的缓冲区 → 传 `&mut String`，不要指望 `&str`。

---

## Q3. 为什么 Rust 禁止 `s[0]` 这种字符串索引？ {#q3}
**Tags:** `hot` `beginner` `string` `indexing` `utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 `s[0]` 语义模糊：是第 0 个字节、第 0 个 Unicode 标量值，还是用户眼里的第 0 个字形？Rust 拒绝提供这种有歧义且易切坏 UTF-8 的索引。

**解答：**

`String` / `str` 在内存里是 UTF-8 字节序列。多字节字符（如中文）不能从中间切开，否则会破坏“永远是有效 UTF-8”的不变量。若允许 `s[0]` 返回 `char`，又和“按字节下标”的直觉打架；若返回 `u8`，又和 Go/`[]byte` 的习惯混在一起。于是标准库干脆不实现 `str[usize]`：

```rust
fn main() {
    let s = String::from("hello");
    // let c = s[0];
    // error[E0277]: the type `str` cannot be indexed by `{integer}`
    println!("{}", s.len());
}
```

想拿“第一个字符”，请明确说按 Unicode 标量值遍历：

```rust
fn main() {
    let s = "你好";
    let first = s.chars().next().unwrap();
    println!("{first}"); // 你
}
```

想按字节看，也要显式走字节 API：

```rust
fn main() {
    let s = "你好";
    let first_byte = s.as_bytes()[0];
    println!("0x{first_byte:02x}"); // 0xe4，是 '你' 的首字节，不是完整字符
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "你好"
	fmt.Println(s[0])          // 字节，不是 rune
	fmt.Println([]rune(s)[0])  // 第一个 rune：你
	fmt.Printf("%c\n", []rune(s)[0])
}
```

- **Go 怎么做**：`s[i]` 明确是字节；要字符得 `range` 或转 `[]rune`。
- **Rust 为什么不同**：Rust 不提供“看起来像字符索引、实际却危险或歧义”的语法糖，逼你选 `chars()` / `bytes()` / 切片边界。
- **Go 程序员易踩的坑**：写出 `s[0]` 期望得到 `'h'` 或 `'你'`；在 Rust 里会直接 `E0277`。

**记忆点：**

- `s[0]` 对 `String`/`str` 不合法 → `error[E0277]`。
- 要字符用 `chars()`；要字节用 `as_bytes()` / `bytes()`。
- 禁止索引是为了保护 UTF-8 不变量，不是“Rust 刁难人”。

---

## Q4. `len()` 为什么返回字节数，不是字符数？ {#q4}
**Tags:** `hot` `beginner` `string` `len` `utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

`len()` 是 O(1) 的字节长度；字符（Unicode 标量值）个数要扫描解码，必须用 `chars().count()`，不能假装“下标即字符”。

**解答：**

UTF-8 是可变长编码：ASCII 占 1 字节，常见汉字常占 3 字节，有些符号/emoji 占 4 字节。因此“有几个字符”不是看一眼长度字段就能知道的：

```rust
fn main() {
    let s = "你好a";
    println!("bytes={}", s.len());            // 7：你(3)+好(3)+a(1)
    println!("chars={}", s.chars().count());  // 3
}
```

`String` / `&str` 的 `len()` 和底层缓冲区长度一致，和 `Vec<u8>` 的 `len` 同量级概念。切片下标也按字节算，所以必须落在字符边界上（详见 [13-slices](../13-slices/#q6) 与 [Q6](#q6)）：

```rust
fn main() {
    let s = "你好";
    assert_eq!(s.len(), 6);
    let first = &s[0..3]; // 3 字节边界 OK
    println!("{first}");  // 你
    // let bad = &s[0..1]; // 运行期 panic：不是字符边界
}
```

若你真正要的是“用户看到的显示宽度 / 字形簇个数”，连 `chars().count()` 都不够，需要专门的 Unicode 分段库。初学先分清：**字节数 ≠ 标量值个数 ≠ 字形簇个数**。

```rust
fn main() {
    let s = "e\u{0301}"; // e + 组合音调
    println!("bytes={} chars={}", s.len(), s.chars().count()); // 3 字节，2 个 char
    // 用户眼里可能仍是“一个带尖音的 e”
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "你好a"
	fmt.Println(len(s))             // 7，字节
	fmt.Println(len([]rune(s)))     // 3，rune 数
	for i, r := range s {
		fmt.Println(i, string(r)) // i 仍是字节偏移
	}
}
```

- **Go 怎么做**：`len(s)` 也是字节；`range` 给出的 index 同样是字节偏移。
- **Rust 为什么不同**：两边都按字节存 UTF-8；Rust 只是把“字符计数”明确推到迭代器上，避免假 O(1)。
- **Go 程序员易踩的坑**：用 `s.len()` 当“几个字”，对中文立刻错。

**记忆点：**

- `len()` = 字节数，O(1)。
- 字符数 ≈ `chars().count()`，要扫描。
- 切片下标按字节，且必须在字符边界。

---

## Q5. `chars()`、`bytes()`、`char_indices()` 该怎么选？ {#q5}
**Tags:** `hot` `beginner` `string` `iterator` `utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

要 Unicode 标量值用 `chars()`；要原始字节用 `bytes()`；既要字符又要字节偏移用 `char_indices()`。

**解答：**

`chars()` 产出 `char`（Unicode 标量值，Unicode scalar value：合法的单个 Unicode 码点）。适合“逐个字符处理 / 过滤 / 收集”：

```rust
fn main() {
    let s = "Hi你好";
    let upper_ascii: String = s
        .chars()
        .map(|c| c.to_ascii_uppercase())
        .collect();
    println!("{upper_ascii}");
    println!("count={}", s.chars().count());
}
```

`bytes()` 产出 `u8`，适合校验和、协议、ASCII 子集、与二进制缓冲区打交道：

```rust
fn main() {
    let s = "Ab";
    for b in s.bytes() {
        println!("{b}"); // 65, 98
    }
    assert_eq!(s.as_bytes(), &[65, 98]);
}
```

`char_indices()` 给出 `(字节偏移, char)`，做安全切片或“跳过前 N 个字符对应的字节前缀”时最省事：

```rust
fn main() {
    let s = "你好a";
    for (i, ch) in s.char_indices() {
        println!("{i}: {ch}"); // 0:你, 3:好, 6:a
    }
    // 取从第二个字符开始的后缀：
    let rest = &s[s.char_indices().nth(1).unwrap().0..];
    println!("{rest}"); // 好a
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "你好a"
	for i, r := range s { // 类似 char_indices：字节偏移 + rune
		fmt.Println(i, string(r))
	}
	for i := 0; i < len(s); i++ { // 类似 bytes
		fmt.Println(s[i])
	}
}
```

- **Go 怎么做**：`range string` ≈ `char_indices`；按字节就 `for i := 0; i < len(s); i++`。
- **Rust 为什么不同**：三种迭代器名字把意图写死，避免一个 `range` 里混两种语义。
- **Go 程序员易踩的坑**：以为 `chars()` 的下标是 0,1,2…；要偏移请用 `char_indices()`。

**记忆点：**

- `chars()` → `char`
- `bytes()` → `u8`
- `char_indices()` → `(byte_index, char)`，做切片时优先

---

## Q6. UTF-8 为什么会让“第几个字符”变复杂？ {#q6}
**Tags:** `hot` `beginner` `utf8` `string`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 UTF-8 可变长，而“第 N 个字符”还可能指标量值、字形簇或显示列宽——Rust 只保证字节层与标量值层清晰，不会假装随机访问字符是 O(1)。

**解答：**

同一段文本，按不同尺子量出的“第几个”不一样：

```rust
fn main() {
    let s = "👨‍👩‍👧‍👦"; // 家庭 emoji：多个标量值 + 零宽连接符
    println!("bytes={}", s.len());
    println!("scalars={}", s.chars().count()); // 通常 > 1
    // “用户眼里一个 emoji”需要字形簇分段，标准库不做
}
```

即便只谈标量值，随机访问第 N 个也要线性扫描，因为前面每个字符占几字节不固定：

```rust
fn main() {
    let s = "a你b";
    // 第 2 个标量值（0-based 的 index 1）：
    let second = s.chars().nth(1).unwrap();
    println!("{second}"); // 你
}
```

按字节硬切更危险：切到多字节字符中间会 panic（破坏 UTF-8 不变量）。安全做法是 `get` / `is_char_boundary` / `char_indices`：

```rust
fn main() {
    let s = "你好";
    assert_eq!(s.get(0..1), None);      // 非边界 → None，不 panic
    assert_eq!(s.get(0..3), Some("你"));
    assert!(s.is_char_boundary(3));
    assert!(!s.is_char_boundary(1));
}
```

更完整的切片边界说明见 [13-slices](../13-slices/#q6)。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "a你b"
	rs := []rune(s)
	fmt.Println(string(rs[1])) // 你；但会分配一份 rune 切片
	fmt.Println(s[1:2])        // 危险：可能切坏多字节字符
}
```

- **Go 怎么做**：`[]rune` 换随机访问，但要付转换成本；字节切片仍可能切坏。
- **Rust 为什么不同**：默认不提供“字符下标”，逼你承认扫描成本或不变量。
- **Go 程序员易踩的坑**：把“第 N 个字符”当成数组下标；对中文/emoji 立刻错位。

**记忆点：**

- UTF-8 可变长 → 字符随机访问不是 O(1)。
- 标量值用 `chars()`；用户字形可能要额外库。
- 字节切片必须落在字符边界，优先 `get` / `char_indices`。

---

## Q7. 怎么把 `&str` 变成 `String`？ {#q7}
**Tags:** `common` `beginner` `string` `conversion`
**适用版本:** Rust 1.0+

**一句话答案：**

用 `String::from`、`.to_string()` 或 `.to_owned()`——都会分配并复制一份堆上 UTF-8；字面量不能直接赋给 `String` 变量。

**解答：**

三种常见写法等价于“拥有一份拷贝”：

```rust
fn main() {
    let a = String::from("hi");
    let b = "hi".to_string();
    let c = "hi".to_owned();
    assert_eq!(a, b);
    assert_eq!(b, c);
}
```

直接把 `&str` 赋给 `String` 会类型不匹配：

```rust
fn main() {
    // let s: String = "hello";
    // error[E0308]: mismatched types
    //  expected `String`, found `&str`
    let s: String = "hello".to_string();
    println!("{s}");
}
```

已经有 `String`、只是想再要一份时用 `.clone()`；从格式化结果得到新字符串用 `format!`（见 [Q9](#q9)）。

```rust
fn main() {
    let s = String::from("rust");
    let t = s.clone();
    println!("{s} {t}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hi"
	t := s // 复制 string 头；底层字节通常共享，直到有人修改 []byte 视图
	fmt.Println(s, t)
}
```

- **Go 怎么做**：`string` 赋值很轻；需要独立可变缓冲再转 `[]byte`。
- **Rust 为什么不同**：`&str → String` 明确表示“我要拥有并可能修改的缓冲区”，所以要分配。
- **Go 程序员易踩的坑**：写 `let s: String = "hi";` 期望自动转换 → `E0308`。

**记忆点：**

- `&str → String`：`from` / `to_string` / `to_owned`。
- 字面量不是 `String`。
- 需要拥有才转换；只读继续用 `&str`。

---

## Q8. 怎么把 `String` 借成 `&str`？ {#q8}
**Tags:** `common` `beginner` `string` `borrow` `deref`
**适用版本:** Rust 1.0+

**一句话答案：**

`&s`、`s.as_str()`、`&s[..]` 都能得到 `&str`；`&String` 还可通过 **`Deref`**（Dereference，解引用强制转换）在需要 `&str` 的地方自动适配。

**解答：**

最常见写法是直接借用：

```rust
fn print_len(s: &str) {
    println!("{}", s.len());
}

fn main() {
    let owned = String::from("hello");
    print_len(&owned);        // Deref: &String -> &str
    print_len(owned.as_str());
    print_len(&owned[..]);
}
```

这是零成本视图：不复制字节，只产生胖指针。所有权仍在 `owned` 手里，函数返回后 `owned` 还能用：

```rust
fn main() {
    let owned = String::from("rust");
    let view: &str = owned.as_str();
    println!("{view}");
    println!("{owned}"); // 仍可用
}
```

注意：返回指向局部 `String` 的 `&str` 会挂生命周期问题——那是借用规则，不是字符串特有魔法。需要把文本传出作用域时，返回 `String`（或带生命周期的借用，见后续 lifetimes 篇）。

```rust
fn make_greeting(name: &str) -> String {
    format!("hi, {name}")
}

fn main() {
    let g = make_greeting("Ada");
    println!("{g}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func printLen(s string) {
	fmt.Println(len(s))
}

func main() {
	s := "hello"
	printLen(s) // 复制 string 头
}
```

- **Go 怎么做**：`string` 传参复制头，语义上像“便宜的值”。
- **Rust 为什么不同**：`String` 是所有者；借成 `&str` 才能在不交出所有权的情况下只读共享（见 [11-ownership](../11-ownership/#q1)）。
- **Go 程序员易踩的坑**：函数要吃 `String` 导致调用处不断 `to_string()`；参数写成 `&str` 更省心。

**记忆点：**

- `String → &str` 是借用，不分配。
- 参数写 `&str`，调用处传 `&owned` 即可。
- 需要拥有结果时再 `format!` / `to_string`。

---

## Q9. 什么时候该用 `push_str`，什么时候该用 `format!`？ {#q9}
**Tags:** `common` `string` `format` `builder`
**适用版本:** Rust 1.0+

**一句话答案：**

已有 `mut String`、只是往末尾追加片段 → `push` / `push_str`；要从多个值拼出**新**字符串、夹杂格式化 → `format!`。

**解答：**

追加到现有缓冲区（可复用 capacity，少分配）：

```rust
fn main() {
    let mut s = String::from("hello");
    s.push(' ');
    s.push_str("rust");
    println!("{s}");
}
```

一次性拼出新文本，尤其混有数字/多段插值时，用 `format!` 更清晰：

```rust
fn main() {
    let name = "Ada";
    let n = 3;
    let s = format!("{name} has {n} apples");
    println!("{s}");
}
```

循环里大量拼接时，优先 `mut String` + `push_str`（或 `std::fmt::Write`），避免每轮 `format!` 都新建再丢掉：

```rust
fn main() {
    let parts = ["a", "b", "c"];
    let mut out = String::new();
    for (i, p) in parts.iter().enumerate() {
        if i > 0 {
            out.push(',');
        }
        out.push_str(p);
    }
    println!("{out}"); // a,b,c
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	var b strings.Builder
	b.WriteString("hello")
	b.WriteString(" rust")
	fmt.Println(b.String())

	s := fmt.Sprintf("%s has %d apples", "Ada", 3)
	fmt.Println(s)
}
```

- **Go 怎么做**：循环拼接用 `strings.Builder`；插值用 `fmt.Sprintf`。
- **Rust 为什么不同**：`push_str` ≈ Builder；`format!` ≈ `Sprintf` 并直接得到 `String`。
- **Go 程序员易踩的坑**：在热循环里反复 `format!("{s}{x}")` 造成多余分配。

**记忆点：**

- 追加已有缓冲 → `push_str`。
- 新建带插值 → `format!`。
- 热路径少用“每轮新建整串”。

---

## Q10. 拼接字符串时为什么 `String + &str` 会 move 左边？ {#q10}
**Tags:** `common` `string` `move` `add`
**适用版本:** Rust 1.0+

**一句话答案：**

`+` 吃掉左边的 `String`（复用其缓冲区再追加右边），所以左边被 **move**；再用左边会 `error[E0382]`。`&str + &str` 根本不能加。

**解答：**

`String + &str` 的设计是：消费左边所有者，把右边字节追加进去，返回新的（其实常是同一个缓冲区扩容后的）`String`：

```rust
fn main() {
    let s = String::from("hello");
    let t = s + " world";
    // println!("{s}");
    // error[E0382]: borrow of moved value: `s`
    println!("{t}");
}
```

两边都是 `&str` 时没有“可复用的所有者”，标准库不提供 `+`：

```rust
fn main() {
    let a = "hello";
    let b = " world";
    // let c = a + b;
    // error[E0369]: cannot add `&str` to `&str`
    let c = format!("{a}{b}");
    println!("{c}");
}
```

不想失去原 `String` 时：用 `push_str`，或先 `clone` 再加，或直接 `format!`：

```rust
fn main() {
    let s = String::from("hello");
    let t = format!("{s} world"); // 借用 s，不 move
    println!("{s}");
    println!("{t}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "hello"
	t := s + " world"
	fmt.Println(s, t) // 两边都能用；+ 产生新 string
}
```

- **Go 怎么做**：`+` 总是得到新 `string`，原变量仍可用。
- **Rust 为什么不同**：复用左边堆缓冲能少一次拷贝，但代价是交出所有权（所有权规则见 [11-ownership](../11-ownership/#q2)）。
- **Go 程序员易踩的坑**：`let t = s + "x";` 后再用 `s` → `E0382`。

**记忆点：**

- `String + &str` → move 左边。
- `&str + &str` → 不行，用 `format!`。
- 还要原串 → `push_str` / `format!` / `clone`。

---

## Q11. 解析文本为什么常写 `parse::<T>()`？ {#q11}
**Tags:** `common` `string` `parse` `fromstr`
**适用版本:** Rust 1.0+

**一句话答案：**

`parse` 依赖 `FromStr`：你用涡轮鱼 `parse::<T>()`（或类型注解）告诉编译器目标类型，成功得 `Ok(T)`，失败得 `Err`。

**解答：**

从文本得到数字等类型时，Rust 不靠“隐式转换”，而是显式解析：

```rust
fn main() {
    let n: i32 = "42".parse().unwrap();
    let m = "42".parse::<i32>().unwrap(); // 涡轮鱼写法
    assert_eq!(n, m);
    println!("{n}");
}
```

解析可能失败，工程代码应处理 `Result`：

```rust
fn double(s: &str) -> Result<i32, std::num::ParseIntError> {
    let n: i32 = s.parse()?;
    Ok(n * 2)
}

fn main() {
    println!("{:?}", double("21"));  // Ok(42)
    println!("{:?}", double("xx"));  // Err(...)
}
```

类型必须能从字符串解析（实现了 `FromStr`）。自定义类型也可以实现它，从而复用同一套 `parse` API。

```rust
fn main() {
    let ok: Result<u8, _> = "255".parse();
    let bad: Result<u8, _> = "256".parse();
    println!("{ok:?}");
    println!("{bad:?}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	n, err := strconv.Atoi("42")
	fmt.Println(n, err)
	f, err := strconv.ParseFloat("3.14", 64)
	fmt.Println(f, err)
}
```

- **Go 怎么做**：`strconv.Atoi` / `ParseFloat` 等按类型分函数。
- **Rust 为什么不同**：统一走 `parse` + 目标类型，错误用 `Result` 显式表达。
- **Go 程序员易踩的坑**：写成 `"42" as i32` 这种不存在的转换；要用 `parse`。

**记忆点：**

- `"42".parse::<i32>()` 或 `let n: i32 = "42".parse()...`。
- 失败是 `Err`，别一味 `unwrap`。
- 自定义类型可实现 `FromStr`。

---

## Q12. 格式化输出里 `Display` 和 `Debug` 差什么？ {#q12}
**Tags:** `common` `formatting` `display` `debug`
**适用版本:** Rust 1.0+

**一句话答案：**

`Display`（`{}`）给人看；`Debug`（`{:?}`）给开发者看结构。字符串两者都能打，但自定义类型常先有 `Debug`（`#[derive(Debug)]`），`Display` 要手写。

**解答：**

对 `&str` / `String`，`{}` 和 `{:?}` 都能用，但 `Debug` 会加引号并转义，更适合日志里看“原始样子”：

```rust
fn main() {
    let s = "hi\n";
    println!("Display: [{s}]");
    println!("Debug:   [{s:?}]");
}
```

结构体默认不能 `{}`，但可以 `derive(Debug)` 后用 `{:?}`：

```rust
#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 2 };
    println!("{p:?}");
    // println!("{p}"); // 没有 Display 会编译失败
}
```

需要面向用户的好看文本时，再实现 `Display`：

```rust
use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

fn main() {
    println!("{}", Point { x: 1, y: 2 }); // (1, 2)
}
```

**Go 对比：**

```go
package main

import "fmt"

type Point struct{ X, Y int }

func (p Point) String() string {
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

func main() {
	p := Point{1, 2}
	fmt.Println(p)      // 走 Stringer，类似 Display
	fmt.Printf("%#v\n", p) // 偏调试
}
```

- **Go 怎么做**：`String()` ≈ `Display`；`%#v` / `%+v` ≈ 调试输出。
- **Rust 为什么不同**：两套 trait 分开，避免“用户输出”和“调试转储”绑死。
- **Go 程序员易踩的坑**：对只实现了 `Debug` 的类型写 `{}`，编译不过。

**记忆点：**

- `{}` → `Display`；`{:?}` → `Debug`。
- 调试优先 `#[derive(Debug)]`。
- 对外文案再实现 `Display`。

---

## Q13. 什么时候该按字节处理，什么时候该按字符处理？ {#q13}
**Tags:** `common` `utf8` `bytes` `chars`
**适用版本:** Rust 1.0+

**一句话答案：**

协议、校验、ASCII/二进制边界 → 按字节；面向人类语言的计数、大小写、截断展示 → 按字符（标量值），必要时再考虑字形簇。

**解答：**

按字节合适的例子：HTTP 头分隔、固定宽度二进制字段、只含 ASCII 的标识符扫描：

```rust
fn is_ascii_ident(s: &str) -> bool {
    !s.is_empty()
        && s.bytes()
            .all(|b| b.is_ascii_alphanumeric() || b == b'_')
}

fn main() {
    assert!(is_ascii_ident("foo_1"));
    assert!(!is_ascii_ident("你好"));
}
```

按字符合适的例子：统计“几个字”、过滤标点、截取前 N 个标量值（见 [Q15](#q15)）：

```rust
fn main() {
    let s = "Hi，世界";
    let letters: String = s.chars().filter(|c| c.is_alphabetic()).collect();
    println!("{letters}"); // Hi世界
    println!("scalars={}", s.chars().count());
}
```

经验法则：只要文本可能含非 ASCII，就不要用字节下标当“第几个字”。确认是 ASCII 子集后，字节路径往往更快、更简单。

```rust
fn main() {
    let s = "abc";
    assert_eq!(s.len(), s.chars().count()); // ASCII 时碰巧相等
    let t = "你好";
    assert_ne!(t.len(), t.chars().count());
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"unicode"
)

func main() {
	s := "Hi，世界"
	for _, r := range s {
		if unicode.IsLetter(r) {
			fmt.Print(string(r))
		}
	}
	fmt.Println()
	fmt.Println([]byte(s)) // 按字节
}
```

- **Go 怎么做**：字节用 `[]byte` / `s[i]`；字符用 `range` / `[]rune` / `unicode`。
- **Rust 为什么不同**：同一套拆分，只是 API 名字是 `bytes` / `chars`。
- **Go 程序员易踩的坑**：用字节 API 做中文 UI 截断，结果切开半个汉字。

**记忆点：**

- 机器协议 / ASCII → 字节。
- 人类文本语义 → `chars()`（或字形簇库）。
- 非 ASCII 时切勿把 `len()` 当字数。

---

## Q14. 为什么说 Go 的 `[]byte` / `[]rune` 直觉在 Rust 里要拆开理解？ {#q14}
**Tags:** `common` `string` `go-compare` `utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

Go 用 `string` / `[]byte` / `[]rune` 三套“近似同一文本”的视图；Rust 对应的是 `String`/`&str`（UTF-8 文本）、`[u8]`/`Vec<u8>`（字节）、`char` 迭代（标量值）——类型边界更硬，不能靠一次转换糊弄所有需求。

**解答：**

对照表：

| Go | Rust 近亲 | 注意 |
|----|-----------|------|
| `string` | `&str` / `String` | Rust 还分拥有与借用 |
| `[]byte` | `&[u8]` / `Vec<u8>` | 不保证是 UTF-8 |
| `[]rune` | `chars()` / `Vec<char>` | 很少整表物化 |

```rust
fn main() {
    let s = "你好";
    let bytes: &[u8] = s.as_bytes();
    let chars: Vec<char> = s.chars().collect();
    println!("bytes={bytes:?}");
    println!("chars={chars:?}");
}
```

字节转回文本必须验证 UTF-8；Go 的 `string([]byte)` 遇到非法序列会换替换符，Rust 默认用 `from_utf8` 返回错误：

```rust
fn main() {
    let ok = std::str::from_utf8(&[0xe4, 0xbd, 0xa0]).unwrap(); // 你
    println!("{ok}");
    let bad = std::str::from_utf8(&[0xff]);
    assert!(bad.is_err());
}
```

不要一上来就 `s.chars().collect::<Vec<_>>()` 再当数组用——那会分配，并丢掉“按字节切片”的能力。多数时候迭代器就够。

```rust
fn main() {
    let s = "a你b";
    // 需要第 n 个标量值时再 nth，而不是先 collect 全表
    assert_eq!(s.chars().nth(1), Some('你'));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "你好"
	b := []byte(s)
	r := []rune(s)
	fmt.Println(b)
	fmt.Println(r)
	fmt.Println(string(b), string(r))
}
```

- **Go 怎么做**：三者互转很常见，语言鼓励“同一文本多种切片”。
- **Rust 为什么不同**：UTF-8 不变量、所有权、是否合法编码被类型系统钉死，转换更显式。
- **Go 程序员易踩的坑**：把 `Vec<u8>` 当成一定能当字符串；忘记 `from_utf8` 可能失败。

**记忆点：**

- Go 三视图 → Rust 三套类型/API，勿混。
- `&[u8]` ≠ `&str`，中间要过 UTF-8 校验。
- 优先迭代，避免无谓 `Vec<char>`。

---

## Q15. 如何安全截取前 N 个字符？ {#q15}
**Tags:** `occasional` `string` `utf8` `slice`
**适用版本:** Rust 1.0+

**一句话答案：**

用 `chars().take(n).collect()` 得到前 N 个 Unicode 标量值；若要保留 `&str` 后缀/前缀，用 `char_indices()` 找字节边界，切勿 `&s[..n]` 把 `n` 当字符数。

**解答：**

最直接、也最不容易切坏 UTF-8 的写法：

```rust
fn prefix_chars(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

fn main() {
    assert_eq!(prefix_chars("你好世界", 2), "你好");
    assert_eq!(prefix_chars("hi", 10), "hi"); // take 不会越界 panic
}
```

若你想继续借用原字符串的前缀（不分配新 `String`），先找到第 N 个字符的结束字节偏移：

```rust
fn prefix_str(s: &str, n: usize) -> &str {
    match s.char_indices().nth(n) {
        Some((idx, _)) => &s[..idx],
        None => s, // 不足 n 个字符，整段返回
    }
}

fn main() {
    let s = "你好a";
    assert_eq!(prefix_str(s, 2), "你好");
    assert_eq!(prefix_str(s, 9), "你好a");
}
```

错误示范是把字符数当字节下标：

```rust
fn main() {
    let s = "你好";
    // let bad = &s[..2]; // 运行期 panic：byte index 2 is not a char boundary
    let ok = s.get(..3).unwrap(); // 按字节边界，且用 get 更安全
    println!("{ok}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func prefixRunes(s string, n int) string {
	rs := []rune(s)
	if n > len(rs) {
		n = len(rs)
	}
	return string(rs[:n])
}

func main() {
	fmt.Println(prefixRunes("你好世界", 2))
}
```

- **Go 怎么做**：转 `[]rune` 再切，或用手写解码。
- **Rust 为什么不同**：`chars().take` 避免整表分配；`char_indices` 保留 `&str` 借用。
- **Go 程序员易踩的坑**：`s[:n]` 把 `n` 当字符数——在 Go/Rust 里按字节切都危险。

**记忆点：**

- 前 N 个标量值 → `chars().take(n).collect()`。
- 要 `&str` 前缀 → `char_indices().nth(n)`。
- 永远别把字符数直接塞进字节切片下标。

---

## Q16. 路径和操作系统字符串为什么不是普通 `&str`？ {#q16}
**Tags:** `occasional` `path` `osstr` `ffi`
**适用版本:** Rust 1.0+（`std::path` / `std::ffi` 为 stable）

**一句话答案：**

操作系统文件名不一定是有效 UTF-8；Rust 用 `OsString`/`OsStr` 和 `Path`/`PathBuf` 保留平台原生表示，需要时再 `to_str` / `to_string_lossy` 转成 Rust 文本。

**解答：**

先分清两对类型：

| 拥有 | 借用视图 | 含义 |
|------|----------|------|
| `std::ffi::OsString` | `std::ffi::OsStr` | 操作系统字符串（不一定 UTF-8） |
| `std::path::PathBuf` | `std::path::Path` | 专门表示文件系统路径 |

在 Unix 上，路径本质是任意字节序列（除 `\0` 与 `/` 语义外）；在 Windows 上，路径基于 UTF-16。Rust 在 Windows 内部常用 **WTF-8**（Wobbly Transformation Format-8）：一种能无损往返任意 UTF-16（含 unpaired surrogate）的 UTF-8 超集。因此“磁盘上的名字”**不保证**能变成合法 `&str`。

```rust
use std::ffi::OsStr;
use std::path::{Path, PathBuf};

fn main() {
    let path: &Path = Path::new("foo/bar.txt");
    let os: &OsStr = path.as_os_str();
    let owned: PathBuf = path.to_path_buf();

    match path.to_str() {
        Some(s) => println!("utf8 path={s}"),
        None => println!("path is not valid Unicode"),
    }
    // 非法序列会被替换成 U+FFFD，总能得到可读文本：
    let lossy = path.to_string_lossy();
    println!("lossy={lossy}");
    println!("os={os:?} owned={owned:?}");
}
```

需要和文本 API 交接时，优先保留 `Path`/`OsStr` 直到边界；只有确要 UTF-8 时才转换，并处理 `None`：

```rust
use std::path::Path;

fn print_file_name(path: &Path) {
    match path.file_name().and_then(|n| n.to_str()) {
        Some(name) => println!("file={name}"),
        None => println!("file name missing or not UTF-8"),
    }
}

fn main() {
    print_file_name(Path::new("docs/readme.md"));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"path/filepath"
)

func main() {
	p := filepath.Join("foo", "bar.txt")
	fmt.Println(p) // Go 的 string 路径在 Windows 上同样可能丢信息/需特殊处理
}
```

- **Go 怎么做**：路径常常直接是 `string`；非 UTF-8 文件名在跨平台时同样麻烦。
- **Rust 为什么不同**：类型上把“可能非 Unicode 的 OS 字符串”和“保证 UTF-8 的 `&str`”分开，避免静默损坏。
- **Go 程序员易踩的坑**：到处 `path.to_str().unwrap()`；遇非 UTF-8 文件名直接崩。应用 `to_string_lossy` 或显式处理 `None`。

**记忆点：**

- 路径用 `Path`/`PathBuf`，OS 字符串用 `OsStr`/`OsString`。
- Windows 可能是 WTF-8 / 非严格 UTF-8。
- `to_str()` 可能 `None`；`to_string_lossy()` 可降级可读。

---

## Q17. 文本 API 参数为什么优先写 `&str`？ {#q17}
**Tags:** `occasional` `api` `string` `deref`
**适用版本:** Rust 1.0+

**一句话答案：**

`&str` 最通用：字面量、`String` 借用、子切片都能传；参数写 `String` 会逼调用者无谓分配或交出所有权。

**解答：**

对比两种签名：

```rust
fn greet_str(name: &str) {
    println!("hi, {name}");
}

fn greet_owned(name: String) {
    println!("hi, {name}");
}

fn main() {
    greet_str("Ada");
    let s = String::from("Bob");
    greet_str(&s);

    // greet_owned("Ada"); // 需要先 to_string()
    greet_owned(s); // s 被 move
}
```

只有函数需要**拥有**并保存/修改文本时，才在签名里要 `String`（或 `impl Into<String>`）。只读加工、比较、解析，一律 `&str` 更友好：

```rust
fn starts_with_hi(s: &str) -> bool {
    s.starts_with("hi")
}

fn main() {
    assert!(starts_with_hi("hi rust"));
    assert!(starts_with_hi(&String::from("hi!")));
}
```

这和切片篇同一原则：能借就不夺（见 [13-slices](../13-slices/#q1)）。

```rust
fn total_bytes(parts: &[&str]) -> usize {
    parts.iter().map(|s| s.len()).sum()
}

fn main() {
    let owned = String::from("ab");
    println!("{}", total_bytes(&["x", owned.as_str(), "yz"]));
}
```

**Go 对比：**

```go
package main

import "fmt"

func greet(name string) {
	fmt.Println("hi,", name)
}

func main() {
	greet("Ada")
	s := "Bob"
	greet(s)
}
```

- **Go 怎么做**：参数几乎总是 `string`，复制头很便宜。
- **Rust 为什么不同**：`String` 传值是所有权转移；用 `&str` 把“只读查看”表达清楚。
- **Go 程序员易踩的坑**：库函数参数写成 `String`，调用方被迫 `.to_string()` 刷屏。

**记忆点：**

- 只读文本参数 → `&str`。
- 需要拥有/存储/修改 → `String`。
- `&String` 能自动变成 `&str`，反之要分配。

---

## Q18. 本章最实用的字符串心智模型是什么？ {#q18}
**Tags:** `advanced` `summary` `string` `utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

把文本拆成四层：拥有（`String`）、借用（`&str`）、字节（`[u8]`）、标量值（`char`/`chars`）；路径再单独一层（`Path`/`OsStr`）。先问“谁拥有、按哪把尺子量”，再选 API。

**解答：**

日常决策树：

1. 需要增长/长期保存 → `String`
2. 只是读一段文本 → `&str`
3. 协议/二进制/ASCII → 字节 API
4. 人类字符计数/截断 → `chars` / `char_indices`
5. 文件系统名 → `Path` / `OsStr`，别假扮成必定 UTF-8

```rust
fn summarize(s: &str) -> String {
    format!(
        "bytes={} chars={} prefix={}",
        s.len(),
        s.chars().count(),
        s.chars().take(2).collect::<String>()
    )
}

fn main() {
    let owned = String::from("你好rust");
    println!("{}", summarize(&owned));
}
```

把常见报错也嵌进模型里：索引歧义是 `E0277`，字面量当 `String` 是 `E0308`，`+` 吃掉左边是 `E0382`：

```rust
fn main() {
    let mut s = String::from("hi");
    s.push_str("!");
    let t = format!("{s} there"); // 不 move s
    println!("{s} | {t}");
}
```

最后记住：Rust 不是“没有 `[]byte`/`[]rune` 的 Go”，而是把那些视角拆成了不会互相伤害的类型与方法（回顾 [Q14](#q14)）。

```rust
use std::path::Path;

fn main() {
    let text: &str = "ok";
    let path = Path::new(text);
    println!("{:?} / {}", path, text);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := "你好"
	fmt.Println(len(s), len([]rune(s)))
	fmt.Println(string([]rune(s)[:2]))
}
```

- **Go 怎么做**：同一 `string` 上切换 `len` / `range` / `[]byte` / `[]rune`。
- **Rust 为什么不同**：用类型把所有权与编码不变量钉死，换视角必须显式。
- **Go 程序员易踩的坑**：带着“字符串就是一种东西”的直觉入门；在 Rust 里先问视图与所有权。

**记忆点：**

- 拥有 / 借用 / 字节 / 字符 / 路径，五层分开想。
- 参数 `&str`，修改 `String`，路径用 `Path`。
- 报错对照：`E0277` 索引，`E0308` 类型，`E0382` move。

---

## Q19. `to_string` / `to_owned` / `into` / `String::from` 该怎么选？ {#q19}
**Tags:** `common` `string` `conversion` `From` `Into` `ToOwned`
**适用版本:** Rust 1.0+

**一句话答案：**

对 `&str → String`，四者都能得到拥有副本；按**意图与 API 边界**选：字面量/明确构造用 `String::from`，泛型 `T: Into<String>` 用 `.into()`，强调“从借用变拥有”用 `.to_owned()`，已有 `Display` 值用 `.to_string()`（基础写法见 [Q7](#q7)）。

**解答：**

`&str` 上几条路最终都是分配拷贝：

```rust
fn main() {
    let a = String::from("hi");
    let b: String = "hi".into();
    let c = "hi".to_owned();
    let d = "hi".to_string();
    assert_eq!(a, b);
    assert_eq!(b, c);
    assert_eq!(c, d);
}
```

选型口诀：

| 写法 | 更合适的场景 |
|------|----------------|
| `String::from(s)` | 最直白的构造；文档/示例里常见 |
| `s.into()` | 函数参数是 `impl Into<String>`，让调用方传 `&str` 或 `String` |
| `s.to_owned()` | 强调 `ToOwned`：从借用型得到拥有型（`&str → String`，`&[T] → Vec<T>`） |
| `x.to_string()` | `x` 实现了 `Display`（数字、自定义类型），不只是 `&str` |

```rust
fn save(name: impl Into<String>) {
    let name = name.into();
    println!("saved {name}");
}

fn main() {
    save("demo"); // &str
    save(String::from("demo2"));
    save(42.to_string()); // Display → String 后再 Into
}
```

`to_string` 对任意 `Display` 都可用，因此在只接受 `&str` 的上下文里，有人更偏好 `to_owned`/`String::from`，避免“格式化转换”的语义联想；性能上对 `&str` 通常同等。

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	s := "hi"
	t := s                 // 拷贝 string 头
	n := strconv.Itoa(42) // 数值 → 字符串
	fmt.Println(t, n)
}
```

- **Go 怎么做**：字符串赋值很轻；数值转字符串用 `strconv` / `fmt`。
- **Rust 为什么不同**：`&str` 与 `String` 分离，任何“拥有缓冲”都要显式 API。
- **Go 程序员易踩的坑**：四处 `.to_string()` 灭火，不区分 Display 转换与单纯拥有。

**记忆点：**

- 字面量 → `String::from` / `to_owned`。
- API 要灵活 → `Into<String>`。
- 任意可打印值 → `to_string`。

---

## Q20. `String::from_utf8` 和 `from_utf8_lossy` 怎么选？ {#q20}
**Tags:** `common` `string` `utf8` `from_utf8`
**适用版本:** Rust 1.0+

**一句话答案：**

要**严格合法 UTF-8**（协议、校验、存储不变量）用 `String::from_utf8` / `str::from_utf8`，失败返回 `Err`；只想尽量显示、坏字节可替换成 `�` 时用 `String::from_utf8_lossy`。

**解答：**

严格路径：非法就报错，且 `from_utf8` 失败时能拿回原始字节：

```rust
fn main() {
    let ok = String::from_utf8(vec![104, 105]).unwrap(); // "hi"
    let bad = String::from_utf8(vec![0xff, 0xfe]);
    assert!(bad.is_err());
    let bytes = bad.unwrap_err().into_bytes(); // 字节不丢
    println!("{ok} {bytes:?}");
}
```

lossy 路径：返回 **`Cow<'_, str>`**（Clone-on-Write，写时克隆：可能是借用的 `&str`，也可能是拥有的 `String`），无效序列变成 U+FFFD（`�`）：

```rust
use std::borrow::Cow;

fn main() {
    let cow: Cow<str> = String::from_utf8_lossy(&[0xff, b'a', 0xfe]);
    assert!(cow.contains('�'));
    println!("{cow}");
}
```

只借用、不分配拥有 `String` 时，用 `str::from_utf8`：

```rust
fn main() {
    let raw = b"hello";
    let s = std::str::from_utf8(raw).unwrap();
    assert_eq!(s, "hello");
    assert!(std::str::from_utf8(&[0xff]).is_err());
}
```

日志、调试转储、尽力展示用户输入 → lossy；网络协议字段、文件格式、哈希/签名原语 → 严格 `from_utf8`。

**Go 对比：**

```go
package main

import (
	"fmt"
	"unicode/utf8"
)

func main() {
	b := []byte{0xff, 'a'}
	fmt.Println(utf8.Valid(b), string(b)) // string(b) 可含非法 UTF-8
}
```

- **Go 怎么做**：`string([]byte)` 允许非法 UTF-8；用 `utf8.Valid` 另检。
- **Rust 为什么不同**：`String`/`&str` **保证**有效 UTF-8，转换时必须选择严格或替换。
- **Go 程序员易踩的坑**：以为任意字节都能安静变成 `String`；在 Rust 里要么 `Err`，要么 lossy。

**记忆点：**

- 要保证 UTF-8 → `from_utf8`。
- 要尽量显示 → `from_utf8_lossy`（`�`）。
- 只读查看字节 → `str::from_utf8`。

---

## Q21. `split` / `trim` / `contains` / `replace` / `to_lowercase` 日常怎么用？（对标 Go `strings`） {#q21}
**Tags:** `hot` `beginner` `split` `trim` `contains` `replace`
**适用版本:** Rust 1.0+（`split_once` 等为后续稳定 API，1.97 均可用）

**一句话答案：**
这些就是 Go `strings` 包的日常活：查子串用 `contains`，去空白用 `trim*`，切开用 `split`/`split_once`，字面量替换用 `replace`，大小写用 `to_lowercase`/`to_uppercase`。真正的模式匹配再上 [42-regex](42-regex.md)。

**解答：**

```rust
fn main() {
    let raw = "  Hello, Rust  ";
    assert!(raw.contains("Rust"));
    assert!(!raw.contains("Go"));
    assert_eq!(raw.trim(), "Hello, Rust");
    assert_eq!(raw.trim_start(), "Hello, Rust  ");
}
```

```rust
fn main() {
    let line = "a,b,c";
    let parts: Vec<&str> = line.split(',').collect();
    assert_eq!(parts, ["a", "b", "c"]);

    let (k, v) = "key=value".split_once('=').unwrap();
    assert_eq!((k, v), ("key", "value"));

    assert_eq!("foo-bar-foo".replace("foo", "x"), "x-bar-x");
    assert_eq!("foo-bar-foo".replacen("foo", "x", 1), "x-bar-foo");
}
```

```rust
fn main() {
    assert_eq!("AbC".to_lowercase(), "abc");
    assert_eq!("AbC".to_uppercase(), "ABC");
    // 注意：Unicode 大小写不是简单 ASCII 映射；比较时常用 to_lowercase 两边都转
    let a = "Straße";
    let b = "STRASSE";
    assert_ne!(a.to_lowercase(), b.to_lowercase()); // 德语 ß 等要当心
}
```

和正则的分工：固定针/固定分隔符 → 本题 API；`\d+`、可选空白模式、捕获 → [42-regex](42-regex.md)。

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	s := "  Hello, Rust  "
	fmt.Println(strings.Contains(s, "Rust"))
	fmt.Println(strings.TrimSpace(s))
	fmt.Println(strings.Split("a,b", ","))
	fmt.Println(strings.ReplaceAll("foo-foo", "foo", "x"))
	fmt.Println(strings.ToLower("AbC"))
}
```

- **Go 怎么做**：`strings.Contains` / `TrimSpace` / `Split` / `ReplaceAll` / `ToLower`。
- **Rust 为什么不同**：方法挂在 `str`/`String` 上，不是独立包；语义几乎一一对应。
- **Go 程序员易踩的坑**：找 `strings.TrimSpace` 同名函数；在 Rust 里是 `trim()`（默认空白），不是包级函数。

**记忆点：**

- Go `strings` → Rust `str` 方法。
- 字面量日常处理先别上正则。

---
