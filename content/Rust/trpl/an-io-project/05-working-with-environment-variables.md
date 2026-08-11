+++
title = "12.5 使用环境变量"
date = 2026-08-05T08:44:00+08:00
weight = 54
type = "docs"
description = "通过环境变量控制大小写不敏感搜索"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 使用环境变量


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-05-working-with-environment-variables.html](https://doc.rust-lang.org/stable/book/ch12-05-working-with-environment-variables.html)


## 使用环境变量

　　我们再为 `minigrep` 二进制增加一项功能：用户可通过环境变量开启大小写不敏感搜索。也可以做成命令行选项，让用户每次想用时都输入；但改成环境变量后，用户只需设置一次，该终端会话中的所有搜索就会默认大小写不敏感。

### 为大小写不敏感搜索编写失败的测试

　　首先在 `minigrep` 库中新增 `search_case_insensitive` 函数，在环境变量有值时调用它。我们继续遵循 TDD，第一步仍是写一个会失败的测试。为新函数添加测试，并把旧测试从 `one_result` 重命名为 `case_sensitive`，以区分两者，如示例 12-20 所示。

**文件名：`src/lib.rs`**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Duct tape.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }

    #[test]
    fn case_insensitive() {
        let query = "rUsT";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Trust me.";

        assert_eq!(
            vec!["Rust:", "Trust me."],
            search_case_insensitive(query, contents)
        );
    }
}
```

**示例 12-20：为即将添加的大小写不敏感函数增加失败测试**

　　注意我们也改了旧测试的 `contents`：新增一行 `"Duct tape."`，其中 *D* 为大写；在大小写敏感搜索时不应匹配查询 `"duct"`。这样改旧测试有助于确保不会意外破坏已实现的大小写敏感搜索。该测试现在应通过，并在我们实现大小写不敏感搜索时继续通过。

　　大小写*不敏感*搜索的新测试以 `"rUsT"` 为查询。在即将添加的 `search_case_insensitive` 中，查询 `"rUsT"` 应匹配含大写 *R* 的 `"Rust:"` 一行，也应匹配 `"Trust me."`，即便大小写与查询不同。这是失败的测试：由于尚未定义 `search_case_insensitive`，它会编译失败。你可以像示例 12-16 对 `search` 那样加一个总是返回空向量的骨架实现，让测试先编译再失败。

### 实现 `search_case_insensitive` 函数

　　示例 12-21 中的 `search_case_insensitive` 几乎与 `search` 相同。唯一区别是我们会对 `query` 和每一行 `line` 转小写，这样无论输入参数的大小写如何，比较时都是同一大小写。

**文件名：`src/lib.rs`**
```rust
pub fn search_case_insensitive<'a>(
    query: &str,
    contents: &'a str,
) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }

    results
}
```

**示例 12-21：定义 `search_case_insensitive`：比较前将查询与行转为小写**

　　首先对 `query` 字符串调用 `to_lowercase`，存入同名新变量以遮蔽原来的 `query`。无论用户查询是 `"rust"`、`"RUST"`、`"Rust"` 还是 `"rUsT"`，我们都当作 `"rust"` 处理，从而忽略大小写。`to_lowercase` 能处理基本 Unicode，但并非百分之百准确。若写真实应用，这里还需要更多工作；本节主题是环境变量而非 Unicode，因此点到为止。

　　注意此时 `query` 是 `String` 而非字符串切片，因为 `to_lowercase` 会创建新数据而不是引用已有数据。例如查询为 `"rUsT"` 时，该切片里没有可供使用的小写 `u` 或 `t`，必须分配包含 `"rust"` 的新 `String`。现在把 `query` 传给 `contains` 时需要加引用，因为 `contains` 的签名要求字符串切片。

　　接着对每一行 `line` 调用 `to_lowercase`。把 `line` 和 `query` 都转成小写后，无论查询大小写如何都能找到匹配。

　　看看实现能否通过测试：

```console
$ cargo test
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.33s
     Running unittests src/lib.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 2 tests
test tests::case_insensitive ... ok
test tests::case_sensitive ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests minigrep

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

　　很好，通过了。现在从 `run` 调用新的 `search_case_insensitive`。首先给 `Config` 结构体加一个配置选项，在大小写敏感与不敏感搜索之间切换。添加该字段会引发编译错误，因为尚未在任何地方初始化它：

<span class="filename">文件名：src/main.rs</span>

```rust
pub struct Config {
    pub query: String,
    pub file_path: String,
    pub ignore_case: bool,
}
```

　　我们添加了保存布尔值的 `ignore_case` 字段。接下来让 `run` 检查 `ignore_case` 的值，据此决定调用 `search` 还是 `search_case_insensitive`，如示例 12-22。此时仍无法编译。

**文件名：`src/main.rs`**
```rust
use minigrep::{search, search_case_insensitive};

// --snip--


fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    let results = if config.ignore_case {
        search_case_insensitive(&config.query, &contents)
    } else {
        search(&config.query, &contents)
    };

    for line in results {
        println!("{line}");
    }

    Ok(())
}
```

**示例 12-22：根据 `config.ignore_case` 调用 `search` 或 `search_case_insensitive`**

　　最后需要检查环境变量。处理环境变量的函数在标准库的 `env` 模块中，*src/main.rs* 顶部已将其引入作用域。我们用 `env::var` 检查名为 `IGNORE_CASE` 的环境变量是否设置了任意值，如示例 12-23。

**文件名：`src/main.rs`**
```rust
impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let file_path = args[2].clone();

        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}
```

**示例 12-23：检查名为 `IGNORE_CASE` 的环境变量是否有值**

　　这里创建新变量 `ignore_case`。要设置其值，调用 `env::var` 并传入环境变量名 `IGNORE_CASE`。若该变量被设为任意值，`env::var` 返回成功的 `Ok` 变体并包含其值；若未设置则返回 `Err` 变体。

　　我们用 `Result` 上的 `is_ok` 检查环境变量是否已设置——若已设置，程序应做大小写不敏感搜索。若 `IGNORE_CASE` 未设置，`is_ok` 返回 `false`，程序做大小写敏感搜索。我们不关心环境变量的*值*，只关心是否设置，因此检查 `is_ok` 而不是用 `unwrap`、`expect` 或其他 `Result` 方法。

　　把 `ignore_case` 的值传给 `Config` 实例，这样 `run` 就能读取它并决定调用 `search_case_insensitive` 还是 `search`，正如示例 12-22 所实现的。

　　试一下！先不设置环境变量，用查询 `to` 运行——应匹配所有包含全小写 *to* 的行：

```console
$ cargo run -- to poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep to poem.txt`
Are you nobody, too?
How dreary to be somebody!
```

　　看起来仍然正常！现在把 `IGNORE_CASE` 设为 `1`，仍用查询 `to`：

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

　　若使用 PowerShell，需要把设置环境变量与运行程序分成两条命令：

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

　　这会使 `IGNORE_CASE` 在当前 shell 会话剩余时间内一直有效。可用 `Remove-Item` cmdlet 取消设置：

```console
PS> Remove-Item Env:IGNORE_CASE
```

　　我们应得到可能含大写字母的、包含 *to* 的行：


```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

　　太好了，也匹配到了含 *To* 的行！`minigrep` 现在可以通过环境变量控制大小写不敏感搜索。你已知道如何用命令行参数或环境变量管理选项。

　　有些程序对同一配置同时允许参数*和*环境变量；此时由程序决定哪一方优先。作为练习，试着通过命令行参数或环境变量控制大小写敏感性，并决定：若一个设为敏感、另一个设为忽略大小写，应以谁为准。

　　`std::env` 模块还有许多处理环境变量的有用功能，可查阅其文档了解可用内容。
