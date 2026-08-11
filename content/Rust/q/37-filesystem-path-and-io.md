+++
title = "37-文件系统、Path 与 IO"
date = 2026-07-28T14:49:00+08:00
weight = 370
type = "docs"
description = "面向 Go 用户讲清 Path/PathBuf、读写文件、缓冲 IO、OpenOptions 与 ErrorKind 对照"
isCJKLanguage = true
draft = false

+++

# 文件系统、Path 与 IO (Filesystem, Path and IO)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否分不清 `Path`、`PathBuf`、`OsString`，以及该传 `&str` 还是路径类型？
- 你是否想知道 `join` / `push` / `parent` 和工作目录怎么用，才不会拼出错路径？
- 你是否只会 `read_to_string`，却不知道大文件该用 `BufReader`、写文件该用 `OpenOptions`？
- 你是否遇到 `ErrorKind::NotFound` / `AlreadyExists` 却不知道和 Go 的 `os.IsNotExist` 怎么对？
- 你是否要写「先写临时文件再改名」的原子保存，或设计接受路径的函数参数？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| `Path` | — | 路径切片/视图 | 不拥有数据的路径借用类型 | 类似只读路径字符串视图 |
| `PathBuf` | path buffer | 路径缓冲区 | 拥有所有权的可增长路径 | 可变的路径 `string` |
| `OsString` / `OsStr` | OS string | 操作系统字符串 | 平台原生字符串，不一定 UTF-8 | Windows 下更接近原生；Unix 近似字节串 |
| `CWD` | current working directory | 当前工作目录 | 相对路径解析所相对的目录 | `os.Getwd` |
| `BufReader` / `BufWriter` | buffered reader/writer | 缓冲读写器 | 减少系统调用次数的包装 | `bufio.Reader` / `Writer` |
| `OpenOptions` | — | 打开选项构建器 | 组合 create/append/truncate 等打开模式 | `os.OpenFile` 的 flag |
| `ErrorKind` | — | 错误种类 | `io::Error` 的粗分类枚举 | `os.IsNotExist` 等判断函数 |
| `AsRef<Path>` | — | 可转为路径引用 | 泛型参数可接受 `Path`/`PathBuf`/`str` 等 | 接口上常直接收 `string` |
| atomic replace | — | 原子替换 | 写临时文件再 rename，降低半截文件可见性 | 同思路的手写模式 |
| UTF-8 | — | Unicode 变换格式-8 | Rust `String`/`str` 的编码；路径未必是它 | Go `string` 也是字节，惯例当 UTF-8 |
| `canonicalize` | — | 规范化绝对路径 | 解析 `.`/`..` 并跟随符号链接，得到绝对路径 | `filepath.Abs` + `EvalSymlinks` |
| symlink | symbolic link | 符号链接 | 指向另一路径的目录项；`canonicalize` 会跟随 | 同概念 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q6](#q6), [Q9](#q9), [Q10](#q10) |
| `common` | [Q5](#q5), [Q7](#q7), [Q8](#q8), [Q11](#q11), [Q13](#q13), [Q15](#q15) |
| `occasional` | [Q12](#q12), [Q14](#q14) |
| `advanced` | — |

---

## Q1. `Path`、`PathBuf`、`OsString` 分别是什么？和 `String` 什么关系？ {#q1}
**Tags:** `hot` `beginner` `Path` `PathBuf` `OsString`
**适用版本:** Rust 1.0+

**一句话答案：**
`PathBuf` 拥有一条路径；`Path` 是其借用视图（像 `String`/`str`）。底层分量常是 **`OsString`/`OsStr`**（操作系统字符串）：在 Windows 等平台上路径**不一定**是合法 UTF-8，所以不要默认当成 `String`。

**解答：**
对应关系：

| 拥有 | 借用 | 用途 |
|------|------|------|
| `String` | `str` | 保证 UTF-8 的文本 |
| `OsString` | `OsStr` | 平台原生字符串 |
| `PathBuf` | `Path` | 专门表示文件系统路径 |

```rust
use std::path::{Path, PathBuf};

fn main() {
    let owned: PathBuf = PathBuf::from("data");
    let view: &Path = owned.as_path();
    assert!(view.ends_with("data"));

    let via_str: PathBuf = Path::new("logs").join("app.log");
    println!("{}", via_str.display());
}
```

需要给人看时用 `display()`（有损但安全）；需要 UTF-8 时用 `to_str()` → `Option`，失败就不要假装是 `String`。

```rust
use std::path::Path;

fn main() {
    let p = Path::new("readme.txt");
    match p.to_str() {
        Some(s) => println!("utf-8 path: {s}"),
        None => println!("path is not valid UTF-8"),
    }
}
```

**Go 对比：**
```go
p := filepath.Join("data", "a.txt")
fmt.Println(p) // string
```
- **Go 怎么做**：路径几乎就是 `string`，用 `path`/`filepath` 包处理。
- **Rust 为什么不同**：用类型区分「文本」和「可能非 UTF-8 的 OS 路径」。
- **Go 程序员易踩的坑**：到处 `path.to_str().unwrap()`，在非 UTF-8 文件名上直接崩。

**记忆点：**
- `PathBuf` : `Path` ≈ `String` : `str`。
- 展示用 `display()`；当文本用先 `to_str()`。

---

## Q2. `join`、`push`、`parent`、`file_name` 怎么用？ {#q2}
**Tags:** `hot` `join` `push` `parent`
**适用版本:** Rust 1.0+

**一句话答案：**
`join` 返回新的 `PathBuf`；`push` 就地追加；`parent` / `file_name` / `extension` 取部件。注意：若 `join`/`push` 的参数是绝对路径，会替换而不是拼接（和 Go `filepath.Join` 对绝对段的处理思路相近）。

**解答：**

```rust
use std::path::{Path, PathBuf};

fn main() {
    let base = Path::new("project");
    let full: PathBuf = base.join("src").join("main.rs");
    assert_eq!(full.file_name().unwrap().to_string_lossy(), "main.rs");
    assert_eq!(full.extension().unwrap().to_string_lossy(), "rs");
    assert!(full.parent().unwrap().ends_with("src"));
}
```

就地修改：

```rust
use std::path::PathBuf;

fn main() {
    let mut p = PathBuf::from("project");
    p.push("src");
    p.push("lib.rs");
    println!("{}", p.display());
}
```

绝对段替换示例（Unix 风格示意；Windows 上绝对路径以盘符等为绝对）：

```rust
use std::path::PathBuf;

fn main() {
    let mut p = PathBuf::from("project");
    p.push("/etc/hosts"); // 若参数为绝对路径，结果通常变成该绝对路径
    println!("{}", p.display());
}
```

**Go 对比：**
```go
filepath.Join("a", "b", "c")
filepath.Dir(p)
filepath.Base(p)
filepath.Ext(p)
```
- **Go 怎么做**：`filepath` 包函数式 API。
- **Rust 为什么不同**：方法挂在 `Path`/`PathBuf` 上，拥有/借用分型。
- **Go 程序员易踩的坑**：用字符串 `+ "/"` 拼路径——请改用 `join`，避免分隔符和绝对段问题。

**记忆点：**
- 不可变拼 → `join`；可变拼 → `push`。
- 绝对路径参数会「改道」。

---

## Q3. 当前工作目录是什么？相对路径相对谁解析？ {#q3}
**Tags:** `hot` `cwd` `current_dir` `env`
**适用版本:** Rust 1.0+

**一句话答案：**
相对路径相对进程的 **CWD**（current working directory，当前工作目录）；用 `std::env::current_dir` 读取、`set_current_dir` 修改。和「可执行文件所在目录」不是一回事。

**解答：**

```rust
use std::env;
use std::path::PathBuf;

fn main() -> std::io::Result<()> {
    let cwd: PathBuf = env::current_dir()?;
    println!("cwd = {}", cwd.display());

    let relative = cwd.join("Cargo.toml");
    println!("guess = {}", relative.display());
    Ok(())
}
```

从可执行文件定位资源更稳的做法是：安装时定好数据目录，或在 **Cargo 构建** 的代码里用 `env!("CARGO_MANIFEST_DIR")`（由 Cargo 注入，裸 `rustc` 没有）锚定到包根，而不是假设 CWD。

```rust
use std::env;
use std::path::PathBuf;

fn main() {
    // 相对路径是否找得到，完全取决于进程启动时的 CWD
    let guess: PathBuf = PathBuf::from("src").join("main.rs");
    println!("relative guess = {}", guess.display());
    if let Ok(cwd) = env::current_dir() {
        println!("resolved against cwd = {}", cwd.join(&guess).display());
    }
}
```

**Go 对比：**
```go
wd, err := os.Getwd()
err = os.Chdir("/tmp")
```
- **Go 怎么做**：`Getwd` / `Chdir`。
- **Rust 为什么不同**：同概念，API 在 `std::env`。
- **Go 程序员易踩的坑**：在 IDE/服务里 CWD 不是项目根，相对路径读文件失败。

**记忆点：**
- 相对路径 → 看 CWD，不看 exe 目录。
- 配置里尽量存绝对路径或明确根。

---

## Q4. `read_to_string` 和 `write` 怎么一次性读写文本？ {#q4}
**Tags:** `hot` `fs` `read_to_string` `write`
**适用版本:** Rust 1.0+（`write` 等为长期稳定 API）

**一句话答案：**
小文件用 `std::fs::read_to_string` / `fs::write`（或 `read`/`write` 字节版）最省事；返回 `io::Result`，失败要处理。大文件或流式处理见 [Q5](#q5)。

**解答：**

```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("demo-note.txt", "hello\n")?;
    let s = fs::read_to_string("demo-note.txt")?;
    assert!(s.contains("hello"));
    let bytes = fs::read("demo-note.txt")?;
    assert_eq!(bytes, s.as_bytes());
    let _ = fs::remove_file("demo-note.txt");
    Ok(())
}
```

`write` 会创建或**截断**已有文件并写入全部内容。只要追加，用 `OpenOptions`（见 [Q6](#q6)）。

「❌ 忽略错误」——`let _ = fs::read_to_string(...);` 丢掉 `Result`，文件不存在时静默失败。

「✅ 正确写法」——`?`、`match` 或至少 `expect` 带上下文。

**Go 对比：**
```go
os.WriteFile("demo-note.txt", []byte("hello\n"), 0644)
b, err := os.ReadFile("demo-note.txt")
```
- **Go 怎么做**：`ReadFile` / `WriteFile`。
- **Rust 为什么不同**：同层便利 API；文本专用 `read_to_string` 要求内容是 UTF-8。
- **Go 程序员易踩的坑**：对非 UTF-8 文件用 `read_to_string`——应改用 `fs::read`。

**记忆点：**
- 文本小文件 → `read_to_string` / `write`。
- 任意字节 → `read` / `write`。

---

## Q5. `BufReader` / `BufWriter` 什么时候用？ {#q5}
**Tags:** `common` `BufReader` `BufWriter` `bufio`
**适用版本:** Rust 1.0+

**一句话答案：**
按行读、多次小读小写时，用 **`BufReader`/`BufWriter`**（缓冲读写器）减少系统调用；记得出缓冲要用 `flush`（`BufWriter` 在 drop 时也会尝试 flush，但显式更清晰）。

**解答：**

```rust
use std::fs::File;
use std::io::{BufRead, BufReader, BufWriter, Write};

fn main() -> std::io::Result<()> {
    {
        let f = File::create("demo-lines.txt")?;
        let mut w = BufWriter::new(f);
        writeln!(w, "one")?;
        writeln!(w, "two")?;
        w.flush()?;
    }

    let f = File::open("demo-lines.txt")?;
    let reader = BufReader::new(f);
    for line in reader.lines() {
        println!("{}", line?);
    }
    let _ = std::fs::remove_file("demo-lines.txt");
    Ok(())
}
```

`lines()` 得到 `io::Result<String>` 迭代；每行可能失败（编码/IO）。

```rust
use std::io::{self, Write};

fn main() -> io::Result<()> {
    let mut out = io::BufWriter::new(io::stdout().lock());
    writeln!(out, "buffered stdout")?;
    out.flush()
}
```

**Go 对比：**
```go
r := bufio.NewReader(f)
w := bufio.NewWriter(f)
w.Flush()
```
- **Go 怎么做**：`bufio` 包。
- **Rust 为什么不同**：同样的缓冲思想，类型在 `std::io`。
- **Go 程序员易踩的坑**：写完不 `flush` 就读回同一文件——缓冲里可能还有数据。

**记忆点：**
- 多次小 IO → 加缓冲。
- `BufWriter` 记得 `flush`。

---

## Q6. `OpenOptions` 怎么表达创建、追加、截断？ {#q6}
**Tags:** `hot` `OpenOptions` `append` `create`
**适用版本:** Rust 1.0+

**一句话答案：**
用 **`OpenOptions`** 链式组合 `read`/`write`/`create`/`append`/`truncate` 等，对应 Go `os.OpenFile` 的 flag 位；`File::open` 只读，`File::create` 创建并截断。

**解答：**

```rust
use std::fs::OpenOptions;
use std::io::Write;

fn main() -> std::io::Result<()> {
    let mut f = OpenOptions::new()
        .create(true)
        .append(true)
        .open("demo-append.txt")?;
    writeln!(f, "line")?;
    let _ = std::fs::remove_file("demo-append.txt");
    Ok(())
}
```

只写新建（已存在则截断）常用：

```rust
use std::fs::OpenOptions;
use std::io::Write;

fn main() -> std::io::Result<()> {
    let mut f = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true)
        .open("demo-trunc.txt")?;
    write!(f, "fresh")?;
    let _ = std::fs::remove_file("demo-trunc.txt");
    Ok(())
}
```

| 需求 | 典型组合 |
|------|----------|
| 只读 | `File::open` 或 `.read(true)` |
| 创建并清空写 | `File::create` 或 write+create+truncate |
| 追加日志 | create+append |
| 必须是新文件 | `.create_new(true)`（已存在则错） |

**Go 对比：**
```go
os.OpenFile("f", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
```
- **Go 怎么做**：位标志 OR。
- **Rust 为什么不同**：构建器 API，同样表达打开语义。
- **Go 程序员易踩的坑**：`File::create` 当追加用——它会截断。

**记忆点：**
- 追加 → `append(true)`，不要用裸 `create`。
- `create_new` 防覆盖。

---

## Q7. `create_dir_all` 和 `read_dir` 怎么建目录、列目录？ {#q7}
**Tags:** `common` `create_dir_all` `read_dir`
**适用版本:** Rust 1.0+

**一句话答案：**
递归建目录用 `fs::create_dir_all`；列目录用 `fs::read_dir`，遍历时每个条目是 `Result<DirEntry>`，记得处理错误与文件类型。

**解答：**

```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::create_dir_all("demo-tree/a/b")?;
    fs::write("demo-tree/a/b/c.txt", "x")?;

    for entry in fs::read_dir("demo-tree/a")? {
        let entry = entry?;
        println!("{}", entry.path().display());
    }

    fs::remove_dir_all("demo-tree")?;
    Ok(())
}
```

`DirEntry` 可 `.path()`、`.file_type()`、`.metadata()`。删除树用 `remove_dir_all`（危险，确认路径）。

```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::create_dir_all("demo-empty/sub")?;
    assert!(fs::metadata("demo-empty/sub")?.is_dir());
    fs::remove_dir_all("demo-empty")?;
    Ok(())
}
```

**Go 对比：**
```go
os.MkdirAll("a/b", 0755)
entries, err := os.ReadDir("a")
```
- **Go 怎么做**：`MkdirAll` / `ReadDir`。
- **Rust 为什么不同**：同能力；`read_dir` 迭代器每次 `Result`。
- **Go 程序员易踩的坑**：忽略 `entry?`，一次坏条目就 panic 或漏处理。

**记忆点：**
- 建多层 → `create_dir_all`。
- 列目录 → `read_dir` + 处理每个 `Result`。

---

## Q8. `io::Error` 和 `ErrorKind` 怎么判断「不存在」等？ {#q8}
**Tags:** `common` `ErrorKind` `NotFound`
**适用版本:** Rust 1.0+（部分 kind 随版本增补，基础 kind 长期稳定）

**一句话答案：**
`io::Error` 用 `.kind()` 得到 **`ErrorKind`**（错误种类）；判断不存在用 `ErrorKind::NotFound`，对应 Go 的 `os.IsNotExist`。不要只靠字符串匹配错误文案。

**解答：**

```rust
use std::fs;
use std::io::ErrorKind;

fn main() {
    match fs::read_to_string("definitely-missing-xyz.txt") {
        Ok(s) => println!("{s}"),
        Err(e) if e.kind() == ErrorKind::NotFound => {
            println!("missing file");
        }
        Err(e) => println!("other error: {e}"),
    }
}
```

常见 kind：`NotFound`、`PermissionDenied`、`AlreadyExists`、`WouldBlock`、`UnexpectedEof` 等。平台相关细节可能落在 `Other` 或带额外 OS 错误码——需要时再向下取。

```rust
use std::fs::OpenOptions;
use std::io::ErrorKind;

fn main() {
    let _ = std::fs::write("demo-exists.txt", "x");
    let res = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open("demo-exists.txt");
    match res {
        Err(e) if e.kind() == ErrorKind::AlreadyExists => {
            println!("already there");
        }
        other => {
            println!("unexpected: {other:?}");
        }
    }
    let _ = std::fs::remove_file("demo-exists.txt");
}
```

**Go 对比：**
```go
if os.IsNotExist(err) { ... }
if errors.Is(err, fs.ErrNotExist) { ... }
```
- **Go 怎么做**：`IsNotExist` / `errors.Is`。
- **Rust 为什么不同**：`ErrorKind` 枚举 + 匹配。
- **Go 程序员易踩的坑**：用 `e.to_string().contains("not found")`——脆弱且不稳定。

**记忆点：**
- 分支看 `e.kind()`。
- `NotFound` ≈ `IsNotExist`。

---

## Q9. 函数参数该写 `&Path` 还是 `AsRef<Path>`？ {#q9}
**Tags:** `hot` `AsRef` `Path` `API`
**适用版本:** Rust 1.0+

**一句话答案：**
库函数若想同时接受 `&Path`、`PathBuf`、`&str`、`String`，参数用 `impl AsRef<Path>`（或泛型 `P: AsRef<Path>`）；内部立刻 `.as_ref()` 得到 `&Path`。只在模块内部、调用面很窄时，直接 `&Path` 也行。

**解答：**

```rust
use std::path::Path;

fn file_len(path: impl AsRef<Path>) -> std::io::Result<u64> {
    let path = path.as_ref();
    Ok(std::fs::metadata(path)?.len())
}

fn main() -> std::io::Result<()> {
    std::fs::write("demo-len.txt", "abc")?;
    assert_eq!(file_len("demo-len.txt")?, 3);
    assert_eq!(file_len(Path::new("demo-len.txt"))?, 3);
    let _ = std::fs::remove_file("demo-len.txt");
    Ok(())
}
```

返回路径给调用方时优先 `PathBuf`（拥有）；临时查看用 `&Path`。

```rust
use std::path::{Path, PathBuf};

fn child(base: &Path, name: &str) -> PathBuf {
    base.join(name)
}

fn main() {
    let p = child(Path::new("data"), "a.bin");
    println!("{}", p.display());
}
```

**Go 对比：**
```go
func FileLen(path string) (int64, error) { ... }
```
- **Go 怎么做**：参数基本是 `string`。
- **Rust 为什么不同**：用 `AsRef<Path>` 消除 `&str` vs `PathBuf` 的调用摩擦。
- **Go 程序员易踩的坑**：API 全收 `String` 强迫调用方分配；或全收 `&Path` 强迫先 `Path::new`。

**记忆点：**
- 输入路径 → `impl AsRef<Path>`。
- 输出拥有路径 → `PathBuf`。

---

## Q10. 和 Go 的 `os` / `path` / `filepath` 怎么整表对照？ {#q10}
**Tags:** `hot` `go` `filepath` `os`
**适用版本:** Rust 1.0+

**一句话答案：**
路径运算看 `std::path`，文件操作看 `std::fs`，工作目录看 `std::env`，缓冲看 `std::io`——大致对应 Go 的 `path`/`filepath` + `os` + `bufio`。

**解答：**

| Go | Rust |
|----|------|
| `filepath.Join` | `Path::join` / `PathBuf::push` |
| `filepath.Dir` / `Base` / `Ext` | `parent` / `file_name` / `extension` |
| `os.Getwd` / `Chdir` | `env::current_dir` / `set_current_dir` |
| `os.ReadFile` / `WriteFile` | `fs::read` / `read_to_string` / `write` |
| `os.Open` / `Create` / `OpenFile` | `File::open` / `create` / `OpenOptions` |
| `os.MkdirAll` / `ReadDir` | `create_dir_all` / `read_dir` |
| `os.IsNotExist` | `ErrorKind::NotFound` |
| `bufio.Reader` | `io::BufReader` |

```rust
use std::path::Path;

fn main() {
    let p = Path::new("a").join("b").join("c.txt");
    println!("dir-ish = {:?}", p.parent());
    println!("base = {:?}", p.file_name());
}
```

```go
p := filepath.Join("a", "b", "c.txt")
fmt.Println(filepath.Dir(p), filepath.Base(p))
```

**Go 对比：**
- **Go 怎么做**：标准库包名按职责拆开。
- **Rust 为什么不同**：同样拆；路径类型化是最大差别。
- **Go 程序员易踩的坑**：在 Rust 里继续用字符串拼接当 `filepath.Join`。

**记忆点：**
- 路径类型 → `path`；读写 → `fs`；缓冲 → `io`。

---

## Q11. 原子写 / 临时文件的常见做法是什么？ {#q11}
**Tags:** `common` `atomic` `tempfile` `rename`
**适用版本:** Rust 1.0+（`rename` 长期稳定；专用临时文件库为生态 crate）

**一句话答案：**
先写到同目录临时文件，`flush`/`sync` 后再 **`fs::rename`** 覆盖目标，降低读者看到半截内容的概率；跨卷 rename 可能失败，需回退拷贝。完整「临时文件」生命周期也可用 `tempfile` crate。

**解答：**
标准库做法（同目录临时名 + rename）：

```rust
use std::fs;
use std::io::Write;
use std::path::Path;

fn atomic_write(path: &Path, data: &[u8]) -> std::io::Result<()> {
    let dir = path.parent().unwrap_or_else(|| Path::new("."));
    let tmp = dir.join("demo-atomic.tmp");
    {
        let mut f = fs::File::create(&tmp)?;
        f.write_all(data)?;
        f.sync_all()?;
    }
    fs::rename(&tmp, path)?;
    Ok(())
}

fn main() -> std::io::Result<()> {
    atomic_write(Path::new("demo-atomic-out.txt"), b"ok")?;
    assert_eq!(fs::read("demo-atomic-out.txt")?, b"ok");
    let _ = fs::remove_file("demo-atomic-out.txt");
    Ok(())
}
```

注意：唯一临时名、崩溃清理、权限，生产代码往往用成熟 crate；这里只讲模式。

**Go 对比：**
```go
// 同目录写 tmp 再 os.Rename
```
- **Go 怎么做**：同样「写临时 + rename」模式。
- **Rust 为什么不同**：同 OS 语义；Rust 用 `Result` 显式传播失败。
- **Go 程序员易踩的坑**：临时文件写在 `/tmp`、目标在别的盘，Windows/Unix 上 rename 跨设备失败。

**记忆点：**
- 同目录临时文件 + `rename`。
- 需要时再 `sync_all`。

---

## Q12. Windows 路径要注意什么？（不含工具链安装） {#q12}
**Tags:** `occasional` `windows` `prefix` `separator`
**适用版本:** Rust 1.0+

**一句话答案：**
用 `Path`/`PathBuf` API，不要手写 `/` 或 `\`；Windows 有盘符、UNC、前缀等；比较/展示用 `Path` 方法与 `display()`。本篇不讨论 MSVC/GNU 工具链差异。

**解答：**

```rust
use std::path::{Path, PathBuf};

fn main() {
    let mut p = PathBuf::from("C:\\");
    p.push("Users");
    p.push("demo");
    println!("{}", p.display());

    // 即使源码里写正斜杠，Path 也会按平台理解许多情况
    let q = Path::new("C:/Users/demo");
    println!("file_name = {:?}", q.file_name());
}
```

`components()` 可遍历根、前缀、普通分量。不要假设所有路径 `to_str()` 成功。

```rust
use std::path::Path;

fn main() {
    let p = Path::new("C:\\Windows\\System32");
    for c in p.components() {
        println!("{c:?}");
    }
}
```

**Go 对比：**
```go
filepath.Join("C:\\", "Users", "demo")
filepath.FromSlash(...)
```
- **Go 怎么做**：`filepath` 处理分隔符与卷。
- **Rust 为什么不同**：`std::path` 同样平台相关；类型保留 OS 语义。
- **Go 程序员易踩的坑**：把 Unix 绝对路径逻辑原样搬到盘符路径上。

**记忆点：**
- 拼接走 `join`/`push`。
- Windows 前缀/UNC 交给 `Path`，别手拼。

---

## Q13. `metadata`、存在性检查、复制删除怎么做？ {#q13}
**Tags:** `common` `metadata` `copy` `remove_file`
**适用版本:** Rust 1.0+

**一句话答案：**
`fs::metadata` / `symlink_metadata` 看大小与类型；「是否存在」更稳的是尝试操作并匹配 `NotFound`，或用 `path.exists()`（注意 TOCTOU）；复制用 `fs::copy`，删文件 `remove_file`，删目录树 `remove_dir_all`。

**解答：**

```rust
use std::fs;
use std::path::Path;

fn main() -> std::io::Result<()> {
    fs::write("demo-meta.txt", "hello")?;
    let meta = fs::metadata("demo-meta.txt")?;
    assert!(meta.is_file());
    assert_eq!(meta.len(), 5);

    fs::copy("demo-meta.txt", "demo-meta-copy.txt")?;
    assert!(Path::new("demo-meta-copy.txt").exists());

    fs::remove_file("demo-meta.txt")?;
    fs::remove_file("demo-meta-copy.txt")?;
    Ok(())
}
```

`exists()` 与随后打开之间可能被别的进程改掉（**TOCTOU**，time-of-check to time-of-use，检查到使用之间的竞态）；权限敏感逻辑应以打开结果为准。

```rust
use std::fs;
use std::io::ErrorKind;

fn main() {
    if let Err(e) = fs::remove_file("nope-xyz.txt") {
        if e.kind() != ErrorKind::NotFound {
            panic!("{e}");
        }
    }
}
```

**Go 对比：**
```go
info, err := os.Stat(path)
os.Remove(path)
os.RemoveAll(dir)
```
- **Go 怎么做**：`Stat` / `Remove` / `RemoveAll`。
- **Rust 为什么不同**：同职责；仍用 `Result` + `ErrorKind`。
- **Go 程序员易踩的坑**：`exists()` 为真就假设一定能打开。

**记忆点：**
- 元数据 → `metadata`。
- 删/拷 → `remove_*` / `copy`；存在性别过度依赖。

---

## Q14. `Read`/`Write` trait 和 `stdin`/`stdout` 怎么接到文件同一套 API？ {#q14}
**Tags:** `occasional` `Read` `Write` `stdin`
**适用版本:** Rust 1.0+

**一句话答案：**
文件、套接字、标准流都实现 **`Read`/`Write`**（可读/可写 trait）；用泛型或 `impl Read` 就能把「读文件」和「读 stdin」写成同一套逻辑，再按需包 `BufReader`。

**解答：**

```rust
use std::fs::File;
use std::io::{self, Read};

fn count_bytes(mut r: impl Read) -> io::Result<usize> {
    let mut buf = Vec::new();
    r.read_to_end(&mut buf)?;
    Ok(buf.len())
}

fn main() -> io::Result<()> {
    std::fs::write("demo-rw.txt", "xyz")?;
    let n = count_bytes(File::open("demo-rw.txt")?)?;
    assert_eq!(n, 3);
    let _ = std::fs::remove_file("demo-rw.txt");
    Ok(())
}
```

标准输出：

```rust
use std::io::{self, Write};

fn main() -> io::Result<()> {
    let mut out = io::stdout().lock();
    writeln!(out, "hello from stdout")?;
    out.flush()
}
```

**Go 对比：**
```go
io.Copy(dst, src)
// Reader / Writer 接口
```
- **Go 怎么做**：`io.Reader` / `Writer` 统一流。
- **Rust 为什么不同**：同样用 trait 统一；再叠 `BufRead`/`BufWriter`。
- **Go 程序员易踩的坑**：为文件和 stdin 各写一套解析，而不是 `impl Read`。

**记忆点：**
- 流式能力看 `Read`/`Write`。
- 文件与标准流可共用函数。

---

## Q15. `canonicalize`、符号链接、相对路径规范化要注意什么？ {#q15}
**Tags:** `common` `canonicalize` `symlink` `normalize`
**适用版本:** Rust 1.0+（`canonicalize` 行为依平台文件系统）

**一句话答案：**
**`Path::canonicalize`** 会解析 `.` / `..`、跟随 **symlink**（符号链接），并变成绝对路径——但路径必须**已存在**，否则 `Err`。只要「字面上清掉 `..`」而不碰磁盘，用 `components` 自己拼，或明确接受「未解析链接」的语义；别把 `canonicalize` 当成纯字符串 API。

**解答：**
存在路径上的规范化：

```rust
use std::env;
use std::fs;
use std::path::PathBuf;

fn main() -> std::io::Result<()> {
    let dir = env::temp_dir().join("canon-demo");
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(dir.join("sub"))?;
    fs::write(dir.join("sub").join("a.txt"), b"hi")?;

    let messy: PathBuf = dir.join("sub").join(".").join("..").join("sub").join("a.txt");
    let abs = messy.canonicalize()?;
    assert!(abs.is_absolute());
    assert_eq!(fs::read(&abs)?, b"hi");

    let _ = fs::remove_dir_all(&dir);
    Ok(())
}
```

「文件还不存在」时 `canonicalize` 会失败——先写再规范化，或改用别的策略：

```rust
use std::path::{Component, Path, PathBuf};

/// 仅做词法清理：去掉 `.`、回退 `..`，不访问磁盘、不解析 symlink。
fn lexically_normalize(path: &Path) -> PathBuf {
    let mut out = PathBuf::new();
    for c in path.components() {
        match c {
            Component::CurDir => {}
            Component::ParentDir => {
                out.pop();
            }
            other => out.push(other.as_os_str()),
        }
    }
    out
}

fn main() {
    let p = Path::new("a/b/../c/./d.txt");
    assert_eq!(lexically_normalize(p), PathBuf::from("a/c/d.txt"));
}
```

符号链接注意点：

| 需求 | 做法 |
|------|------|
| 解析到最终目标 | `canonicalize` / 打开文件（跟随链接） |
| 看链接本身元数据 | `symlink_metadata`（见 [Q13](#q13)） |
| 相对路径拼配置 | 先相对 **CWD**（[Q3](#q3)）想清楚，再决定要不要 `canonicalize` |
| Windows 长路径前缀 | `canonicalize` 结果可能带 `\\?\`——展示或传给某些工具前要心里有数 |

安全场景（「用户给的相对路径不能逃出根目录」）：词法 `..` 清理不够时，还要在 `canonicalize` 之后检查是否仍落在允许根之下；链接可指到根外。

**Go 对比：**
```go
filepath.Abs(path)
filepath.EvalSymlinks(path)
filepath.Clean(path) // 词法，不解析 symlink
```
- **Go 怎么做**：`Clean` / `Abs` / `EvalSymlinks` 职责分开。
- **Rust 为什么不同**：`canonicalize` ≈ Abs + EvalSymlinks，且要求存在；词法清理需自写或第三方。
- **Go 程序员易踩的坑**：对尚未创建的输出路径直接 `canonicalize`，或以为它像 `Clean` 一样纯字符串。

**记忆点：**
- `canonicalize` = 绝对 + 跟 symlink + 必须存在。
- 只要词法清理 → `components`，别误用 `canonicalize`。
