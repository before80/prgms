+++
title = "error"
date = 2026-09-19T09:05:00+08:00
weight = 4
type = "docs"
description = "18 种语言的错误处理对照：错误表示、抛出与传播、捕获与处理、自定义错误、资源清理与未捕获错误"
isCJKLanguage = true
draft = false
+++

# 错误处理机制：18 种语言对照

错误处理是语言设计分歧最大的地方之一：Rust 把错误当**值**返回，Go 用 `error` 接口加 `if err != nil`，Java 区分 checked/unchecked 异常，Python/JavaScript 抛任意对象，Zig 用错误集与 `try`，Lua 用 `pcall` 返回的字符串。本页按五个主题组织：**错误的表示方式 → 抛出与传播 → 捕获与处理 → 自定义错误与上下文 → 资源清理与未捕获错误**，每个主题一套 18 语言标签页。

## 错误处理

**一页速览**

| 语言 | 错误怎么表示 | 抛出/返回 | 捕获 |
| --- | --- | --- | --- |
| Rust | 值：`Result<T, E>` | `return Err(e)`、`?`、`panic!` | `match`、`if let`、`?`、`catch_unwind` |
| Swift | 值 + 异常：`Error` 协议 | `throw`；`Result` 也可 | `do/catch`、`try?`、`try!` |
| Go | 值：`error` 接口 | `return err`、`panic` | `if err != nil`、`recover` |
| Python | 异常：`Exception` 层级 | `raise` | `try/except/else/finally` |
| Kotlin | 异常：`Throwable` | `throw` | `try/catch/finally`、`runCatching` |
| Java | 异常：checked/unchecked | `throw` | `try/catch/finally`、try-with-resources |
| C++ | 异常 + 错误码 | `throw`、`return std::error_code` | `try/catch`、`std::expected`（C++23） |
| C | 返回码 + `errno` | `return -1`、`setjmp/longjmp` | 检查返回值、`errno` |
| Julia | 异常：`Exception` 层级 | `throw`、`error` | `try/catch/finally` |
| C# | 异常：`System.Exception` | `throw` | `try/catch/finally`、`using` |
| Dart | 异常：`Exception` / `Error` | `throw` | `try/catch/finally` |
| R | 条件系统（condition） | `stop()`、`warning()` | `tryCatch`、`withCallingHandlers` |
| Zig | 值：错误集 + `!T` | `return error.X`、`try` | `catch`、`try/catch` |
| Lua | 值：字符串或表 | `error()` | `pcall`/`xpcall` |
| TypeScript | 异常（类型不跟踪） | `throw` | `try/catch`（`catch` 变量是 `unknown`） |
| JavaScript | 异常 + Promise rejection | `throw`、`reject` | `try/catch`、`.catch()` |
| PHP | 异常 + 错误 | `throw`、`trigger_error` | `try/catch/finally` |
| Ruby | 异常：`Exception` 层级 | `raise` | `begin/rescue/ensure` |

### 错误的表示方式

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 把可恢复错误做成**普通值**：`Result<T, E>`；不可恢复的用 `panic!`（默认直接终止线程）。缺失值另有一套 `Option<T>`。

| 机制 | 写法 |
| --- | --- |
| 可恢复错误 | `Result<T, E>`，配 `?` 传播 |
| 不可恢复 | `panic!("...")`、`unwrap()`、`expect()` |
| 可能缺失 | `Option<T>` |

```rust
fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> {
    s.parse()
}

let port = parse_port("8080").unwrap_or(8080);   // 失败时给默认值
```

`Result` 是枚举，所以"有没有错误"由类型系统保证，编译器会强制你处理；`panic!` 不是异常，默认不能被普通 `catch` 逻辑接住（只能 `catch_unwind`，且要求 unwind 支持）。

📘 [std::result](https://doc.rust-lang.org/std/result/)、[`?` 运算符](https://doc.rust-lang.org/reference/expressions/operator-expr.html#the-question-mark-operator)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 用**协议 + 抛出**：错误类型实现 `Error`，函数标 `throws` 后用 `throw` 抛出；也可以用 `Result<T, Error>` 把错误当值传递。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw MyError.failed` |
| 传播 | `func f() throws -> T` |
| 当值用 | `Result<T, Error>` |

```swift
enum MyError: Error { case failed(String) }

func load(_ path: String) throws -> String {
    throw MyError.failed("missing: \(path)")
}

let r: Result<String, Error> = Result { try load("a.txt") }
```

`throws` 是函数类型的一部分（错误能被编译器感知），但没有"checked exception"那套声明式约束；`Error` 可以带关联值，错误信息天然结构化。

📘 [Swift · Error Handling](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 里错误就是值：`error` 是一个只有 `Error() string` 方法的接口，函数把 `error` 作为**最后一个返回值**。`panic` 只用于"程序无法继续"的情况。

| 机制 | 写法 |
| --- | --- |
| 普通错误 | `error` 接口，`err != nil` 判断 |
| 带格式 | `fmt.Errorf("...: %w", err)`（`%w` 可包装） |
| 致命错误 | `panic(...)` + `recover()` |

```go
func load(path string) (string, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return "", fmt.Errorf("load %s: %w", path, err)
    }
    return string(data), nil
}
```

因为错误是普通返回值，Go 的代码里到处是 `if err != nil`；代价是啰嗦，好处是控制流完全显式。`panic` 的恢复只能在自己的 defer 里做，跨 goroutine 不会传播。

📘 [Go blog · Error handling](https://go.dev/blog/error-handling-and-go)、[`errors` 包](https://pkg.go.dev/errors)

{{% /tab %}}

{{% tab header="Python" %}}

Python 用异常：所有错误都是 `BaseException` 的子类，日常处理的是 `Exception` 子类；函数不声明抛什么，`raise` 随时可以抛。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `raise ValueError("bad")` |
| 层级 | `BaseException` → `Exception` → 具体错误 |
| 又当值用 | 把异常对象 `raise ... from e` 串起因果链 |

```python
class ConfigError(Exception):
    def __init__(self, key: str):
        super().__init__(f"missing key: {key}")
        self.key = key

def load(cfg: dict) -> str:
    if "path" not in cfg:
        raise ConfigError("path")
    return cfg["path"]
```

异常可以携带任意属性（如上面的 `key`），`raise ... from e` 会保留原始原因（`__cause__`）；`KeyboardInterrupt`/`SystemExit` 继承自 `BaseException`，所以 `except Exception` 不会误吞 Ctrl-C。

📘 [Python · Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 沿用 JVM 的异常体系：一切可抛出的东西都继承 `Throwable`；Kotlin **没有 checked exception**，编译器不强制你声明或捕获。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw IllegalStateException("...")` |
| 函数式 | `Result<T>` + `runCatching { }` |
| 可空 | 用 `T?` 表示缺失（比异常更常用） |

```kotlin
fun load(path: String): Result<String> = runCatching {
    require(path.isNotEmpty()) { "empty path" }
    File(path).readText()
}

val text = load("a.txt").getOrElse { "default" }
```

因为没有 checked exception，Java 的受检异常在 Kotlin 里变成"可以抛、也可以不处理"；`Result` 是标准库提供的值语义封装，适合链式处理（`map`/`getOrElse`/`fold`）。

📘 [Kotlin · Exceptions](https://kotlinlang.org/docs/exceptions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 把异常分成两类：**checked**（`Exception` 的子类，除 `RuntimeException`）必须在签名里声明或用 `try` 处理；**unchecked**（`RuntimeException`/`Error`）编译器不管。

| 机制 | 写法 |
| --- | --- |
| checked | `throws IOException`，调用方必须处理 |
| unchecked | `RuntimeException`（如 `IllegalArgumentException`） |
| 资源 | `try (var in = ...) { }` 自动关闭 |

```java
public String load(Path p) throws IOException {   // checked：必须声明
    if (!Files.exists(p)) throw new IllegalArgumentException("missing");  // unchecked
    return Files.readString(p);
}
```

设计的本意是"可恢复的问题强制处理"，实践中的抱怨是"签名被 `throws` 污染"；现代 Java 代码常用 `UncheckedIOException`、`Optional` 或 `Result` 风格库来减少受检异常的传播。

📘 [Java 教程 · Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有异常（`std::exception` 层级），也允许完全不开异常（`-fno-exceptions`）；C++23 又补了值语义的 `std::expected<T, E>`，与 `std::error_code` 一起构成"错误码路线"。

| 机制 | 写法 |
| --- | --- |
| 异常 | `throw std::runtime_error("...")` |
| 错误码 | `std::error_code`、`std::expected`（C++23） |
| 保证 | `noexcept` 表示不抛 |

```cpp
#include <expected>

std::expected<int, std::string> parse(std::string_view s) {
    if (s.empty()) return std::unexpected("empty");
    return 42;
}

if (auto v = parse("42")) { /* 用 *v */ }
```

异常适合"罕见、需要跨层传播"的错误，`expected`/错误码适合"常见、就地处理"的错误；游戏与嵌入式常直接关闭异常以减小体积。

📘 [cppreference · Exceptions](https://en.cppreference.com/w/cpp/language/exceptions)、[`std::expected`](https://en.cppreference.com/w/cpp/utility/expected)

{{% /tab %}}

{{% tab header="C" %}}

C 没有异常：错误通过**返回值 + `errno`** 表达，函数约定"返回 -1/NULL 表示失败"，具体原因写到 `errno`；`setjmp/longjmp` 能做非局部跳转，但绕过清理逻辑，风险很高。

| 机制 | 写法 |
| --- | --- |
| 返回值 | `return -1`、`return NULL` |
| 全局错误码 | `errno`、`perror()`、`strerror()` |
| 断言 | `assert()`（发布时用 `-DNDEBUG` 关掉） |

```c
#include <errno.h>
#include <stdio.h>

FILE *f = fopen("a.txt", "r");
if (!f) {
    fprintf(stderr, "open failed: %s\n", strerror(errno));
    return -1;
}
```

错误码是"上下文无关的全局状态"，容易被后续调用覆盖；现代 C 代码要么在函数返回时立刻读取 `errno`，要么自己定义 `enum` 返回值并把细节写进输出参数。

📘 [`errno.h`](https://en.cppreference.com/w/c/error/errno)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用异常：所有错误都是 `Exception` 的子类型（如 `ErrorException`、`BoundsError`、`InexactError`），用 `throw`/`error` 抛出。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw(ArgumentError("bad"))`、`error("...")` |
| 常见类型 | `ErrorException`、`ArgumentError`、`BoundsError`、`InexactError` |
| 缺失 | `nothing` / `missing`（不是错误） |

```julia
function parse_port(s::AbstractString)
    v = tryparse(Int, s)
    v === nothing && throw(ArgumentError("bad port: $s"))
    return v
end
```

`tryparse` 这类"不抛异常"的函数返回 `Union{T, Nothing}`，把"失败"变成普通值；与之相对，`parse` 失败会抛 `ArgumentError`，两种风格 Julia 都常见。

📘 [Julia · 错误处理](https://docs.julialang.org/en/v1/manual/error-handling/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 用异常：一切可抛出的类型继承 `System.Exception`；`Error` 在 .NET 里不是单独一族（`OutOfMemoryException` 等仍属异常）。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw new InvalidOperationException("...")` |
| 捕获 | `try/catch/finally`、`catch (Exception e) when (...)` |
| 值语义替代 | 库里的 `Result` 模式、`TryParse` 模式 |

```csharp
public bool TryLoad(string path, out string content) {
    content = "";
    if (!File.Exists(path)) return false;   // Try 模式：失败不抛异常
    content = File.ReadAllText(path);
    return true;
}
```

.NET 的惯例是"可预期的失败用 `TryXxx`（返回 `bool` + `out`），异常用于意外情况"；`catch` 可以用 `when` 过滤条件，`finally` 负责清理。

📘 [MS Learn · 异常](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 区分 `Exception`（可预期的失败）与 `Error`（编程错误，如断言失败）；两者都能 `throw`，也都能被 `catch`。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw FormatException("bad")`、`throw StateError("...")` |
| 捕获 | `try/catch/finally`，`on FormatException catch (e)` |
| 值语义 | `Result` 风格靠第三方包（如 fpdart） |

```dart
int parsePort(String s) {
  final v = int.tryParse(s);
  if (v == null) throw FormatException('bad port: $s');
  return v;
}

void main() {
  try {
    print(parsePort('x'));
  } on FormatException catch (e) {
    print('caught: $e');
  } finally {
    print('done');
  }
}
```

`Error`（如 `StateError`、`AssertionError`）表示"代码写错了"，通常不该被业务 `catch` 掉；`Exception` 才是常规可恢复错误。

📘 [Dart · Error handling](https://dart.dev/language/error-handling)

{{% /tab %}}

{{% tab header="R" %}}

R 用的是**条件系统**（condition system）：错误、警告、消息都是"条件"，可以抛出、捕获，也可以自定义处理器——比单纯的异常更灵活。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `stop("...")`、`warning("...")`、`message("...")` |
| 捕获 | `try()`、`tryCatch()`、`withCallingHandlers()` |
| 自定义 | `structure(class = c("myError", "error"), ...)` 后 `stop(cond)` |

```r
safe_log <- function(x) {
  if (x <= 0) stop("x must be positive", call. = FALSE)
  log(x)
}

r <- tryCatch(safe_log(-1), error = function(e) NA_real_)
print(r)   # NA
```

`tryCatch` 会**中断**当前计算进入处理器，`withCallingHandlers` 只"通知"然后继续执行；`warning()` 默认不中断，可用 `options(warn = 2)` 把警告升级成错误。

📘 [R · 条件系统](https://adv-r.hadley.nz/conditions.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 把错误做成**值**：错误集（`error{OutOfMemory, ...}`）与错误联合 `!T`，用 `try` 传播、用 `catch` 就地处理；没有异常，也没有隐藏的控制流。

| 机制 | 写法 |
| --- | --- |
| 错误联合 | `fn f() !void` |
| 传播 | `try` |
| 处理 | `catch`、`catch |err| switch (err)` |
| 不可能 | `unreachable`（进入即 UB） |

```zig
const ParseError = error{ Empty, TooLong };

fn parsePort(s: []const u8) ParseError!u16 {
    if (s.len == 0) return error.Empty;
    if (s.len > 5) return error.TooLong;
    return 8080;
}

pub fn main() void {
    const port = parsePort("") catch 8080;   // 失败就给默认值
    _ = port;
}
```

错误集是类型的一部分，编译器能检查 `switch` 是否覆盖全部错误；`try` 只能用在返回错误联合的函数里，调用栈上的每一层都必须显式处理或继续 `try`。

📘 [Zig 语言参考 · Errors](https://ziglang.org/documentation/master/#Errors)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的错误可以是任意值：字符串（`error("msg")` 的默认形式）或表（结构化错误）；用 `pcall`/`xpcall` 捕获，失败时返回 `false` 加错误对象。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `error("bad")`、`error({ code = 1 })` |
| 捕获 | `local ok, err = pcall(f)` |
| 带堆栈 | `xpcall(f, debug.traceback)` |

```lua
local function parse_port(s)
  local n = tonumber(s)
  if not n then error("bad port: " .. tostring(s)) end
  return n
end

local ok, err = pcall(parse_port, "x")
if not ok then print("caught: " .. tostring(err)) end
```

`error` 的第二个参数控制"错误位置信息"的层级，第三个参数（表）可以携带自定义字段；`assert(cond, "msg")` 是"条件不成立就抛错"的简写。

📘 [Lua 5.5 · 错误处理](https://www.lua.org/manual/5.5/manual.html#2.3)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 沿用 JavaScript 的异常，但**类型系统不跟踪函数会抛什么**——没有任何 `throws` 声明；`catch` 到的变量在 `useUnknownInCatchVariables` 下是 `unknown`。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw new Error("...")` |
| 捕获 | `try/catch/finally`；`catch (e: unknown)` 后要收窄 |
| 值语义 | `Result` 风格库（neverthrow 等）在 TS 里很流行 |

```ts
function parsePort(s: string): number {
  const n = Number(s);
  if (!Number.isInteger(n)) throw new Error(`bad port: ${s}`);
  return n;
}

try {
  parsePort("x");
} catch (e: unknown) {
  if (e instanceof Error) console.error(e.message);
}
```

因为类型不跟踪抛异常，"这个函数会不会抛"只能靠文档与约定；很多 TS 项目用 `Result` 库把错误重新变成类型可见的值（例如 `Result<number, ParseError>`）。

📘 [TS · 异常处理](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)、[neverthrow](https://github.com/supermacro/neverthrow)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 用异常（`Error` 及其子类），但 `throw` 可以抛**任何值**（字符串、对象、数字）；异步代码还有另一套：Promise 的 rejection。

| 机制 | 写法 |
| --- | --- |
| 同步抛出 | `throw new Error("...")` |
| 同步捕获 | `try/catch/finally` |
| 异步失败 | `reject(new Error(...))`、`.catch()`、`try/await/catch` |

```js
async function load(path) {
  if (!path) throw new Error("empty path");
  return await fs.readFile(path, "utf8");
}

try {
  await load("");
} catch (e) {
  console.error(e instanceof Error ? e.message : e);
}
```

未处理的 Promise rejection 在 Node 默认会终止进程（`--unhandled-rejections=throw`）；抛非 `Error` 值会丢掉堆栈，所以最佳实践是**永远抛 `Error` 实例**。

📘 [MDN · try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 有两条并行通道：**异常**（`Throwable`：`Exception` 与 `Error`）与**老式错误**（warning/notice/deprecated），后者可以通过错误处理器转成异常。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `throw new RuntimeException("...")` |
| 捕获 | `try/catch/finally`，可多 `catch` |
| 老式错误 | `trigger_error()`、`set_error_handler()` |

```php
function load(string $path): string {
    if (!is_file($path)) {
        throw new RuntimeException("missing: $path");
    }
    return file_get_contents($path);
}

try {
    echo load("a.txt");
} catch (RuntimeException $e) {
    error_log($e->getMessage());
} finally {
    echo "done\n";
}
```

PHP 7 起 `Error`（如 `TypeError`、`DivisionByZeroError`）也实现了 `Throwable`，所以 `catch (Throwable $e)` 能兜住所有异常与引擎错误；而 `@` 抑制符掩盖的是老式错误，不推荐使用。

📘 [PHP · 异常](https://www.php.net/manual/en/language.exceptions.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用异常：所有错误继承 `Exception`，日常捕获的是它的子类 `StandardError`（`rescue` 默认只接这个）。

| 机制 | 写法 |
| --- | --- |
| 抛出 | `raise ArgumentError, "bad"` |
| 捕获 | `begin/rescue/else/ensure` |
| 方法级 | `def f; ...; rescue => e; ...; end` |

```ruby
def load(path)
  raise ArgumentError, "empty path" if path.to_s.empty?
  File.read(path)
rescue Errno::ENOENT => e
  warn "missing: #{e.message}"
  nil
ensure
  puts "done"
end
```

`raise` 不带参数时会重新抛出当前异常（`$!`）；`retry` 可以重试 `begin` 块。注意 `rescue` 默认不捕获 `Exception` 的其他子类（如 `SignalException`、`NoMemoryError`），这是有意设计。

📘 [Ruby · 异常处理](https://docs.ruby-lang.org/en/master/syntax/exceptions_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 抛出与传播

"怎么抛"和"怎么让它传上去"是两件事。这一节按语言给出抛出的写法、传播的机制，以及跨层传递时会不会丢失上下文。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

**抛出**：`return Err(e)`；`panic!` 表示不可恢复。
**传播**：`?` 把错误返回给调用者，必要时自动 `From` 转换。

```rust
use std::io;

fn read_port(path: &str) -> Result<u16, io::Error> {
    let text = std::fs::read_to_string(path)?;   // ? 传播
    text.trim().parse().map_err(io::Error::other) // 错误类型转换
}
```

`?` 只做"向上返回"，不做日志或兜底；每一层都可以决定是继续 `?`、包装成自己的错误类型，还是就地处理。

📘 [`?` 运算符](https://doc.rust-lang.org/reference/expressions/operator-expr.html#the-question-mark-operator)

{{% /tab %}}

{{% tab header="Swift" %}}

**抛出**：`throw`（函数要标 `throws`）。
**传播**：调用点必须写 `try`，可加 `?`/`!` 变成可选值或崩溃。

```swift
enum LoadError: Error { case missing(String) }

func load(_ path: String) throws -> String {
    if path.isEmpty { throw LoadError.missing(path) }
    return try String(contentsOfFile: path)      // try 继续传播
}

let text = try? load("")        // 失败变 nil
```

`try?` 会丢掉错误细节，`try!` 失败直接崩溃；`rethrows` 用于"只有闭包参数会抛"的函数。

📘 [Swift · 传播错误](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/#Propagating-Errors-Using-Throwing-Functions)

{{% /tab %}}

{{% tab header="Go" %}}

**返回**：`return zero, err`（约定 `error` 放最后）。
**传播**：手动 `return err`，或用 `%w` 包装后继续返回。

```go
func load(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("load %s: %w", path, err)   // 包装并保留原因
    }
    return data, nil
}
```

没有隐式传播，所以每层都要显式 `if err != nil`；`%w` 让上层能用 `errors.Is`/`errors.As` 检查原始错误，这是 Go 1.13 之后的标准做法。

📘 [Go blog · Working with Errors](https://go.dev/blog/go1.13-errors)

{{% /tab %}}

{{% tab header="Python" %}}

**抛出**：`raise Exc(...)`。
**传播**：自动沿调用栈向上，直到被 `except` 接住；`raise ... from e` 记录因果链。

```python
def load(path: str) -> str:
    try:
        return open(path).read()
    except OSError as e:
        raise RuntimeError(f"cannot load {path}") from e   # 保留原因
```

`__cause__` 是显式的 `from`，`__context__` 是"处理某个异常时又抛出"产生的隐式上下文；打印回溯时会两者都显示。

📘 [Python · 异常链](https://docs.python.org/3/tutorial/errors.html#exception-chaining)

{{% /tab %}}

{{% tab header="Kotlin" %}}

**抛出**：`throw`；函数签名不需要声明。
**传播**：沿调用栈向上，直到被 `catch` 接住；或用 `Result` 当返回值传播。

```kotlin
fun load(path: String): String {
    require(path.isNotEmpty()) { "empty path" }   // 抛 IllegalArgumentException
    return File(path).readText()                   // kotlin.io 会抛异常
}

fun loadSafe(path: String): Result<String> = runCatching { load(path) }
```

JVM 上没有 checked exception，所以"这个函数可能抛什么"全靠文档；`Result`/`runCatching` 把异常转成值，适合在边界处统一处理。

📘 [Kotlin · Exceptions](https://kotlinlang.org/docs/exceptions.html)

{{% /tab %}}

{{% tab header="Java" %}}

**抛出**：`throw`。
**传播**：checked 异常必须在 `throws` 里声明；unchecked 直接向上传播。

```java
public String load(Path p) throws IOException {   // checked：显式声明
    if (Files.notExists(p)) throw new NoSuchFileException(p.toString());
    return Files.readString(p);
}

// 想把 checked 变 unchecked（跨层简化）：
throw new UncheckedIOException(e);
```

checked 异常强制调用方表态（处理或继续声明），unchecked 表示"代码缺陷"，两者的边界是 Java 里长期争论的话题；`throw new UncheckedIOException(e)` 是绕过 `throws` 污染的常用技巧。

📘 [JLS · 异常](https://docs.oracle.com/javase/specs/jls/se25/html/jls-11.html)

{{% /tab %}}

{{% tab header="C++" %}}

**抛出**：`throw`。
**传播**：栈展开（stack unwinding）——沿调用栈逐层销毁局部对象，直到匹配的 `catch`；`noexcept` 函数里抛出会直接 `std::terminate`。

```cpp
struct LoadError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

std::string load(const std::string& path) {
    if (path.empty()) throw LoadError("empty path");
    return read_file(path);     // 内部异常自动向外展开
}
```

栈展开是 C++ 的强项（RAII 保证资源释放），但要求析构函数不抛异常；用 `-fno-exceptions` 编译时 `throw` 直接不可用。

📘 [cppreference · throw](https://en.cppreference.com/w/cpp/language/throw)

{{% /tab %}}

{{% tab header="C" %}}

**返回**：`return -1`/`NULL` + `errno`。
**传播**：没有自动机制——每一层都要检查返回值并决定是否继续向上返回；`goto cleanup` 是常见的集中清理写法。

```c
int load(const char *path, char **out) {
    FILE *f = fopen(path, "r");
    if (!f) return -1;                 /* 上层继续检查 -1 */
    /* ... */
    fclose(f);
    return 0;
}
```

`setjmp/longjmp` 可以模拟非局部跳转，但不会执行中间层的清理代码，容易造成泄漏，只在极少数场景（软错误恢复）使用。

📘 [`setjmp.h`](https://en.cppreference.com/w/c/program/setjmp)

{{% /tab %}}

{{% tab header="Julia" %}}

**抛出**：`throw(e)`、`error("...")`（等价于 `throw(ErrorException(...))`）。
**传播**：自动沿栈向上；`rethrow()` 保留原始异常与堆栈。

```julia
function load(path::AbstractString)
    isfile(path) || throw(ArgumentError("missing: $path"))
    read(path, String)
end

try
    load("a.txt")
catch err
    @warn "load failed" exception = (err, catch_backtrace())
    rethrow()        # 记录之后继续向上抛
end
```

`@assert cond "msg"` 用于内部不变量检查；在 `catch` 里"处理一半再 `rethrow()`"是保留原堆栈的标准写法。

📘 [Julia · 错误处理](https://docs.julialang.org/en/v1/manual/error-handling/)

{{% /tab %}}

{{% tab header="C#" %}}

**抛出**：`throw new ...`。
**传播**：沿调用栈自动传播并保留堆栈；`throw;`（不带表达式）重新抛出以保留原始堆栈。

```csharp
public string Load(string path) {
    if (!File.Exists(path)) throw new FileNotFoundException(path);
    return File.ReadAllText(path);
}

try { Load("a.txt"); }
catch (IOException e) when (e is not FileNotFoundException) {
    throw;                 // 保留原始堆栈
}
```

`throw e;` 会重置堆栈（原始位置丢失），`throw;` 才是正确的重抛写法；`when` 过滤器让"捕获—判断—重抛"变得更干净。

📘 [MS Learn · throw](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/exception-handling-statements)

{{% /tab %}}

{{% tab header="Dart" %}}

**抛出**：`throw`（可以抛任意对象，惯例抛 `Exception`/`Error` 子类）。
**传播**：同步代码沿栈传播；异步函数里的异常变成返回 `Future` 的"错误状态"，`await` 时重新抛出。

```dart
Future<String> load(String path) async {
  if (path.isEmpty) throw ArgumentError('empty path');
  return await File(path).readAsString();   // 异常进入 Future
}

try {
  await load('');
} catch (e) {
  rethrow;        // 保留原始堆栈重新抛出
}
```

在 `catch` 里用 `rethrow`（不是 `throw e`）才能保留原始堆栈；未处理的异步异常会进 `Zone` 的错误处理，Flutter 里通常由框架统一上报。

📘 [Dart · 错误处理](https://dart.dev/language/error-handling)

{{% /tab %}}

{{% tab header="R" %}}

**抛出**：`stop("...")`；结构化错误用 `stop(structure(class = c("myError", "error"), list(...)))`。
**传播**：条件沿调用栈向上寻找处理器；`tryCatch` 会中断，`withCallingHandlers` 只观察并继续。

```r
load_cfg <- function(path) {
  if (!file.exists(path)) {
    cond <- structure(
      class = c("configError", "error", "condition"),
      list(message = paste("missing:", path), call = NULL)
    )
    stop(cond)
  }
  readRDS(path)
}
```

自定义条件类让你能在处理器里用 `inherits(e, "configError")` 区分错误来源；`warning()`/`message()` 走的是同一套条件机制。

📘 [R · 条件](https://adv-r.hadley.nz/conditions.html)

{{% /tab %}}

{{% tab header="Zig" %}}

**返回**：`return error.Name`。
**传播**：`try` 把错误继续向上返回；错误集可以用 `||` 合并，`catch` 就地兜底。

```zig
const LoadError = error{ Missing, Empty };

fn load(path: []const u8) (LoadError || std.fs.File.OpenError)![]u8 {
    if (path.len == 0) return error.Empty;
    const f = try std.fs.cwd().openFile(path, .{});   // try 继续传播
    defer f.close();
    return try f.readToEndAlloc(std.heap.page_allocator, 1 << 20);
}
```

错误集在类型里显式列出，所以"这个函数可能失败成什么样"一目了然；`errdefer` 在"函数因错误返回"时执行清理。

📘 [Zig · Errors](https://ziglang.org/documentation/master/#Errors)

{{% /tab %}}

{{% tab header="Lua" %}}

**抛出**：`error("msg")`、`assert(cond, "msg")`。
**传播**：沿调用栈向上，直到被 `pcall`/`xpcall` 捕获；库函数的惯例是"返回 `nil, err`"而不是抛错。

```lua
local function load(path)
  local f, err = io.open(path, "r")
  if not f then return nil, err end        -- 惯例：返回 nil + 错误
  local data = f:read("a")
  f:close()
  return data
end

local ok, err = pcall(function() error("boom") end)
if not ok then print("caught:", err) end
```

两种风格并存：`io.open` 返回 `nil, err`（调用方必须检查），`error()` 用于"不可恢复"或参数错误；`xpcall` 的第二个参数可以加 `debug.traceback` 拿到堆栈。

📘 [Lua 5.5 · 错误处理](https://www.lua.org/manual/5.5/manual.html#2.3)

{{% /tab %}}

{{% tab header="TypeScript" %}}

**抛出**：`throw`（任意值，惯例用 `Error`）。
**传播**：沿调用栈传播；async 函数里的异常变成 rejected Promise。类型系统不记录"会抛什么"。

```ts
async function load(path: string): Promise<string> {
  if (!path) throw new Error("empty path");
  return await fs.readFile(path, "utf8");
}

// 传播 = 调用方 await 时被抛出
await load("");
```

因为 `throws` 不进类型，跨层传播只能靠约定；把错误编码进返回类型（`Result<T, E>` 库）可以让编译期就检查"是否处理了错误"。

📘 [TS · 异常](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)、[neverthrow](https://github.com/supermacro/neverthrow)

{{% /tab %}}

{{% tab header="JavaScript" %}}

**抛出**：`throw new Error(...)`；异步函数里 `throw` 等价于 `reject`。
**传播**：同步沿栈传播，异步沿 Promise 链传播，`await` 时重新变成同步异常。

```js
async function load(path) {
  if (!path) throw new Error("empty path");
  return await fs.readFile(path, "utf8");
}

load("").catch((e) => console.error("async:", e.message));   // Promise 传播
```

未处理的 rejection 在 Node 默认终止进程；在浏览器里会触发 `unhandledrejection` 事件。抛非 `Error` 值会丢堆栈，所以始终抛 `Error` 实例。

📘 [MDN · Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

{{% /tab %}}

{{% tab header="PHP" %}}

**抛出**：`throw`；`Throwable` 是统一接口。
**传播**：自动沿调用栈向上；未捕获就变成致命错误（fatal error）。

```php
function load(string $path): string {
    if (!is_file($path)) {
        throw new RuntimeException("missing: $path");
    }
    return file_get_contents($path);
}

set_exception_handler(function (Throwable $e): void {
    error_log("uncaught: " . $e->getMessage());
});
```

`set_exception_handler` 是最后一道网，用于记录日志并返回友好错误页；框架（Laravel/Symfony）都在它之上做了统一异常处理与 HTTP 状态码映射。

📘 [PHP · 异常](https://www.php.net/manual/en/language.exceptions.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

**抛出**：`raise Exc, "msg"`。
**传播**：沿栈向上；`raise` 不带参数会重新抛出当前异常（`$!`），保留原始堆栈。

```ruby
def load(path)
  raise ArgumentError, "empty path" if path.to_s.empty?
  File.read(path)
rescue ArgumentError
  raise                    # 重新抛出当前异常
end

begin
  load("")
rescue => e
  puts "#{e.class}: #{e.message}"
end
```

`raise` 与 `fail` 是同义词；`$!` 保存当前异常，`retry` 可以重新执行 `begin` 块（配合重试计数使用）。

📘 [Ruby · raise](https://docs.ruby-lang.org/en/master/Kernel.html#method-i-raise)

{{% /tab %}}

{{< /tabpane >}}

### 捕获与处理

捕获的核心问题是"在哪一层处理、处理完还继不继续抛"。这一节给出每门语言的捕获语法与常见处理模式。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有 try/catch，用 `match`/`if let`/组合子处理 `Result`；`panic` 只能用 `catch_unwind` 兜。

```rust
match std::fs::read_to_string("a.txt") {
    Ok(text) => println!("{text}"),
    Err(e) if e.kind() == std::io::ErrorKind::NotFound => println!("missing"),
    Err(e) => eprintln!("error: {e}"),
}

let text = std::fs::read_to_string("a.txt").unwrap_or_default();
let n: i32 = "42".parse().map_err(|e| format!("bad: {e}")).unwrap();
```

`if let Ok(x) = ...` 处理"只关心成功"，`unwrap_or`/`unwrap_or_else`/`map_err` 是链式处理的常用组合子；`catch_unwind` 只在 FFI 边界或线程池里用。

📘 [std::result](https://doc.rust-lang.org/std/result/)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
do {
    let text = try load("a.txt")
    print(text)
} catch LoadError.missing(let p) {
    print("missing: \(p)")
} catch {
    print("other: \(error)")
} 

defer { print("cleanup") }      // 退出作用域时执行
```

`do/catch` 可以按错误模式分别处理；`defer` 是 Swift 版的 finally，作用域退出（含提前 return/throw）时执行；`try?` 把错误折叠成可选值。

📘 [Swift · 捕获错误](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/#Handling-Errors)

{{% /tab %}}

{{% tab header="Go" %}}

```go
data, err := os.ReadFile("a.txt")
if err != nil {
    if errors.Is(err, os.ErrNotExist) {          // 判断具体原因
        log.Println("missing")
    }
    var pathErr *os.PathError
    if errors.As(err, &pathErr) {                 // 取回具体错误类型
        log.Println("path:", pathErr.Path)
    }
    return
}
```

```go
defer func() {
    if r := recover(); r != nil {                 // 兜住 panic
        log.Println("recovered:", r)
    }
}()
```

`errors.Is` 判等（包含 `%w` 链）、`errors.As` 取类型，是 Go 1.13+ 处理包装错误的标准姿势；`recover` 只能在自己的 `defer` 里生效。

📘 [`errors` 包](https://pkg.go.dev/errors)

{{% /tab %}}

{{% tab header="Python" %}}

```python
try:
    text = open("a.txt").read()
except FileNotFoundError as e:
    print("missing:", e.filename)
except (OSError, ValueError) as e:      # 多类型捕获
    print("failed:", e)
else:
    print("ok, length:", len(text))      # 没有异常时执行
finally:
    print("done")                         # 一定执行
```

```python
try:
    async with asyncio.TaskGroup() as tg:   # 异常组（3.11+）
        tg.create_task(work())
except* ValueError as eg:                    # 只接住组里的 ValueError
    print(eg.exceptions)
```

`else` 用于"成功才走"的逻辑，`finally` 保证清理；`except*` 是 3.11 引入的异常组语法，配合 `TaskGroup` 处理并发任务的多重失败。

📘 [Python · 异常组](https://docs.python.org/3/library/exceptions.html#exception-groups)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
val text = try {
    File("a.txt").readText()
} catch (e: java.io.FileNotFoundException) {
    "default"
} finally {
    println("done")
}

val len = runCatching { File("a.txt").readText() }
    .map { it.length }
    .getOrElse { 0 }
```

`try/catch/finally` 在 Kotlin 里是**表达式**（有返回值）；`runCatching` 把异常折叠成 `Result`，随后用 `map`/`recover`/`getOrElse` 链式处理。

📘 [Kotlin · Result](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-result/)

{{% /tab %}}

{{% tab header="Java" %}}

```java
try (var in = Files.newInputStream(Path.of("a.txt"))) {   // 自动关闭
    in.readAllBytes();
} catch (FileNotFoundException | NoSuchFileException e) {  // multi-catch
    log.warn("missing", e);
} catch (IOException e) {
    throw new UncheckedIOException(e);
} finally {
    log.info("done");
}
```

try-with-resources 要求资源实现 `AutoCloseable`，它在关闭时抛出的异常会进入 `getSuppressed()`；multi-catch 让多个异常走同一段处理逻辑。

📘 [Java · try-with-resources](https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
try {
    auto text = load("a.txt");
} catch (const LoadError& e) {       // 按 const 引用捕获
    std::cerr << e.what() << '\n';
} catch (const std::exception& e) {
    std::cerr << "std: " << e.what() << '\n';
} catch (...) {                       // 兜底（不要吞掉后继续假装没事）
    std::cerr << "unknown\n";
}
```

C++ 没有 finally：清理靠 RAII（析构函数在栈展开时自动执行）。捕获时按 `const` 引用避免对象切片；`catch (...)` 只用于最后的边界。

📘 [cppreference · try-block](https://en.cppreference.com/w/cpp/language/try_catch)

{{% /tab %}}

{{% tab header="C" %}}

```c
int rc = 0;
FILE *f = fopen("a.txt", "r");
if (!f) { rc = -1; goto cleanup; }

char *buf = malloc(1024);
if (!buf) { rc = -2; goto cleanup; }

/* ... 使用 buf ... */

cleanup:
    free(buf);            /* free(NULL) 合法，所以可以无条件调用 */
    if (f) fclose(f);
    return rc;
```

C 的"捕获"就是检查返回值；`goto cleanup` 把所有清理集中在一处，是内核风格代码里最常见的模式。要注意 `errno` 会被后续调用覆盖，需要时应先存进局部变量。

📘 [`errno`](https://en.cppreference.com/w/c/error/errno)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
try
    v = parse(Int, "x")
catch err
    if err isa ArgumentError
        @warn "bad input" exception = err
    else
        rethrow()
    end
else
    @info "ok" value = v          # 没有异常时执行（1.8+）
finally
    @info "done"
end
```

`catch err` 拿到异常对象后可以用 `isa` 分类；`else` 分支在 Julia 1.8 起可用；`rethrow()` 保留堆栈，`throw(err)` 会重置堆栈。

📘 [Julia · try/catch](https://docs.julialang.org/en/v1/manual/error-handling/)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
try {
    var text = File.ReadAllText("a.txt");
}
catch (IOException e) when (e is FileNotFoundException) {
    Console.Error.WriteLine($"missing: {e.Message}");
}
catch (Exception e) {
    throw;                       // 保留堆栈
}
finally {
    Console.WriteLine("done");
}
```

```csharp
using var stream = File.OpenRead("a.txt");   // 作用域结束自动 Dispose
```

`when` 过滤器是 C# 的特色：它先判断条件、不匹配就继续向上传播（不会"进过 catch"）；`using` 声明（不是块）在作用域结束时释放资源。

📘 [MS Learn · using](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/using)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
try {
  final text = await load('a.txt');
} on FormatException catch (e, st) {     // 类型 + 对象 + 堆栈
  print('bad: ${e.message}');
  print(st);
} catch (e) {
  rethrow;                                // 保留原始堆栈
} finally {
  print('done');
}
```

`on T` 按类型过滤、`catch (e, st)` 连堆栈一起拿；`finally` 在同步与异步路径上都会执行。未捕获的异步异常可以通过 `Zone.runGuarded` 或自定义 `ZoneSpecification` 统一上报。

📘 [Dart · 错误处理](https://dart.dev/language/error-handling)

{{% /tab %}}

{{% tab header="R" %}}

```r
res <- tryCatch(
  {
    readRDS("model.rds")
  },
  configError = function(e) { message("config problem"); NULL },
  error = function(e) { message("other: ", conditionMessage(e)); NULL },
  finally = message("done")
)

withCallingHandlers(
  log(-1),
  warning = function(w) message("warning: ", conditionMessage(w))
)
```

`tryCatch` 按条件类名匹配处理器（可以自定义 `configError` 这样的类）；`withCallingHandlers` 观察警告后继续计算，是"记录但不中断"的标准做法。

📘 [R · tryCatch](https://stat.ethz.ch/R-manual/R-devel/library/base/html/conditions.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const value = parsePort("x") catch 8080;            // 默认值
const v2 = parsePort("x") catch |err| switch (err) { // 按错误分类
    error.Empty => 1,
    error.TooLong => 2,
};
const v3 = parsePort("x") catch |err| {
    std.log.err("failed: {}", .{err});
    return err;                                       // 记录后继续传播
};
```

`catch` 既能给默认值，也能拿到具体错误值做 `switch`；`try` 是"直接继续传播"的简写。Zig 没有 `finally`，清理用 `defer`（正常路径）与 `errdefer`（错误路径）。

📘 [Zig · catch](https://ziglang.org/documentation/master/#catch)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
local ok, err = pcall(load, "a.txt")
if not ok then
  print("caught:", err)
end

local ok2, err2 = xpcall(load, function(e)
  return debug.traceback(e, 2)     -- 附加堆栈
end, "a.txt")
```

Lua 没有 `try/finally`：清理要靠"在 pcall 之后显式执行"或把资源放进 `__gc`/`<close>` 变量（5.4+ 的 to-be-closed 变量）。`select(2, pcall(f))` 可以只取错误值。

📘 [`pcall`](https://www.lua.org/manual/5.5/manual.html#pdf-pcall)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
try {
  const text = await load("a.txt");
} catch (e: unknown) {
  if (e instanceof Error) console.error(e.message);        // 收窄
  else console.error("unknown error", e);
} finally {
  console.log("done");
}

const r = await load("a.txt").then(
  (v) => ({ ok: true, v }) as const,
  (e) => ({ ok: false, e }) as const,                       // 把失败当值
);
```

`catch` 的变量推荐用 `unknown`（`useUnknownInCatchVariables`），用前必须收窄；`Promise.then` 的双回调写法能把失败变成值，配合 `Result` 库更类型安全。

📘 [TS · catch 与 unknown](https://www.typescriptlang.org/tsconfig#useUnknownInCatchVariables)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
try {
  const text = await load("a.txt");
} catch (e) {
  console.error(e instanceof Error ? e.message : e);
} finally {
  console.log("done");
}

const results = await Promise.allSettled([load("a"), load("b")]);
for (const r of results) {
  if (r.status === "rejected") console.error(r.reason);
}
```

并发场景常用 `Promise.allSettled`（不短路、逐个看结果）与 `AggregateError`（`Promise.any` 全失败时抛）；进程级兜底是 `uncaughtException` 与 `unhandledRejection` 事件。

📘 [MDN · Promise.allSettled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
try {
    $text = load("a.txt");
} catch (RuntimeException | Error $e) {      // 多 catch（含引擎 Error）
    error_log($e->getMessage());
} finally {
    echo "done\n";
}

set_error_handler(function (int $no, string $msg, string $file, int $line): bool {
    throw new ErrorException($msg, 0, $no, $file, $line);   // warning → 异常
});
```

把老式 warning 统一转成异常，能让"错误只有一种处理路径"；`finally` 无论是否抛出都会执行。

📘 [PHP · set_error_handler](https://www.php.net/manual/en/function.set-error-handler.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
begin
  text = load("a.txt")
rescue Errno::ENOENT => e
  warn "missing: #{e.message}"
  text = nil
rescue StandardError => e
  warn "other: #{e.class}"
else
  puts "ok"
ensure
  puts "done"            # 相当于 finally，一定执行
end
```

```ruby
def load(path)
  File.read(path)
rescue Errno::ENOENT
  nil                    # 方法级 rescue（不用 begin/end）
end
```

`else` 只在没有异常时执行，`ensure` 一定执行；`retry` 可以重新执行 `begin` 块，配合计数实现重试。

📘 [Ruby · 异常](https://docs.ruby-lang.org/en/master/syntax/exceptions_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 自定义错误、资源清理与未捕获错误

最后一节看三件事：**怎么定义自己的错误类型**、**出错时怎么保证资源被释放**、**没人接住会发生什么**。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

```rust
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("missing file: {0}")] Missing(String),
    #[error("io: {0}")] Io(#[from] std::io::Error),   // 自动 From
}
```

- 自定义错误：手写 `impl std::error::Error + Display`，或用 `thiserror`（库）/`anyhow`（应用）简化。
- 清理：RAII + `Drop`（没有 finally）；`defer` 要用 `scopeguard` 这类库。
- 未捕获：`panic` 触发 unwind（默认），线程退出；`panic = "abort"` 时整个进程 abort。

📘 [std::error::Error](https://doc.rust-lang.org/std/error/trait.Error.html)、[thiserror](https://docs.rs/thiserror/)

{{% /tab %}}

{{% tab header="Swift" %}}

```swift
struct AppError: Error, LocalizedError {
    let path: String
    var errorDescription: String? { "missing: \(path)" }
}
```

- 自定义错误：任何实现 `Error` 的类型（enum/struct 都行）；`LocalizedError` 提供面向用户的消息。
- 清理：`defer`（作用域退出时执行，等价于 finally）。
- 未捕获：顶层未处理的 `Error` 会终止程序（crash），`fatalError()` 同样。

📘 [Swift · Error](https://developer.apple.com/documentation/swift/error)

{{% /tab %}}

{{% tab header="Go" %}}

```go
type ConfigError struct{ Key string }
func (e *ConfigError) Error() string { return "missing key: " + e.Key }

var ErrNotFound = errors.New("not found")            // 哨兵错误
err := errors.Join(ErrNotFound, io.ErrUnexpectedEOF)  // 合并错误（1.20+）
```

- 自定义错误：实现 `Error() string` 的结构体；哨兵错误（`io.EOF`）用于判等。
- 清理：`defer`（即使 panic 也会执行）。
- 未捕获：未 recover 的 panic 会打印堆栈并让进程退出（defer 仍会执行）。

📘 [Go · errors](https://pkg.go.dev/errors)

{{% /tab %}}

{{% tab header="Python" %}}

```python
class AppError(Exception):
    def __init__(self, path: str, cause: Exception | None = None):
        super().__init__(f"load failed: {path}")
        self.path = path
        if cause: self.__cause__ = cause
```

```python
with open("a.txt") as f:      # 上下文管理器：退出时自动关闭
    data = f.read()
```

- 自定义错误：继承 `Exception`；用 `from e` 保留原因。
- 清理：`finally` 与 `with`（`__enter__`/`__exit__`）。
- 未捕获：打印 traceback 并以退出码 1 结束；可用 `sys.excepthook` 自定义。

📘 [Python · 异常](https://docs.python.org/3/tutorial/errors.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

```kotlin
class ConfigException(val key: String) : Exception("missing key: $key")

File("a.txt").bufferedReader().use { reader ->   // use：自动 close
    println(reader.readText())
}
```

- 自定义错误：继承 `Exception`（或 `RuntimeException` 表示编程错误）。
- 清理：`use {}` 扩展函数（对 `Closeable`）与 `finally`。
- 未捕获：线程/进程终止并打印堆栈；Android 上由崩溃上报框架接管。

📘 [Kotlin · use](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.io/use.html)

{{% /tab %}}

{{% tab header="Java" %}}

```java
class ConfigException extends RuntimeException {
    private final String key;
    ConfigException(String key) { super("missing key: " + key); this.key = key; }
    public String key() { return key; }
}

throw new ConfigException("path");                 // unchecked：不用声明
```

- 自定义错误：checked 继承 `Exception`、unchecked 继承 `RuntimeException`；`initCause`/构造参数维护因果链。
- 清理：try-with-resources（`AutoCloseable`）与 `finally`。
- 未捕获：该线程终止并打印堆栈；`Thread.setDefaultUncaughtExceptionHandler` 可统一兜底。

📘 [Java · 自定义异常](https://docs.oracle.com/javase/tutorial/essential/exceptions/creating.html)

{{% /tab %}}

{{% tab header="C++" %}}

```cpp
class ConfigError : public std::runtime_error {
public:
    explicit ConfigError(const std::string& key)
        : std::runtime_error("missing key: " + key), key_(key) {}
    const std::string& key() const { return key_; }
private:
    std::string key_;
};
```

- 自定义错误：继承 `std::exception`（或 `std::runtime_error`），覆写 `what()`。
- 清理：RAII——析构函数在栈展开时执行；没有 finally。
- 未捕获：`std::terminate` → `abort`（可用 `std::set_terminate` 记录日志）。

📘 [cppreference · 异常类](https://en.cppreference.com/w/cpp/error/exception)

{{% /tab %}}

{{% tab header="C" %}}

```c
typedef enum { OK = 0, ERR_NOT_FOUND, ERR_IO, ERR_NOMEM } err_t;

static const char *err_str(err_t e) {
    switch (e) {
        case OK: return "ok";
        case ERR_NOT_FOUND: return "not found";
        case ERR_IO: return "io";
        case ERR_NOMEM: return "out of memory";
    }
    return "unknown";
}
```

- 自定义错误：枚举错误码 + 字符串表，或结构体携带 `code`/`message`。
- 清理：`goto cleanup` / `atexit()`；没有语言级 finally。
- 未捕获：没有"未捕获"概念——忘记检查返回值就继续跑，最坏情况是 UB 或静默错误。

📘 [`errno` 与错误码约定](https://en.cppreference.com/w/c/error)

{{% /tab %}}

{{% tab header="Julia" %}}

```julia
struct ConfigError <: Exception
    key::String
end
Base.showerror(io::IO, e::ConfigError) = print(io, "missing key: ", e.key)

throw(ConfigError("path"))
```

- 自定义错误：定义 `<: Exception` 的类型并实现 `Base.showerror`（控制显示）。
- 清理：`finally` 与 `do` 块（配合 `open` 自动关闭）。
- 未捕获：打印错误与堆栈、非零退出码；`atexit` 可注册收尾逻辑。

📘 [Julia · 自定义异常](https://docs.julialang.org/en/v1/manual/error-handling/)

{{% /tab %}}

{{% tab header="C#" %}}

```csharp
public sealed class ConfigException : Exception {
    public string Key { get; }
    public ConfigException(string key, Exception? inner = null)
        : base($"missing key: {key}", inner) => Key = key;
}
```

- 自定义错误：继承 `Exception`（推荐 `sealed`），用 `InnerException` 表达因果链。
- 清理：`using`/`try/finally`（`IDisposable`/`IAsyncDisposable`）。
- 未捕获：默认终止进程并打印堆栈；`AppDomain.CurrentDomain.UnhandledException` 可以最后记录一次。

📘 [MS Learn · 自定义异常](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/how-to-create-user-defined-exceptions)

{{% /tab %}}

{{% tab header="Dart" %}}

```dart
class ConfigException implements Exception {
  final String key;
  ConfigException(this.key);
  @override
  String toString() => 'ConfigException: missing key $key';
}
```

- 自定义错误：实现 `Exception`（或继承 `Error` 表示编程错误）。
- 清理：`try/finally`；`File.openRead` 这类 API 返回 `Stream`，用 `await for` + `finally` 关闭。
- 未捕获：同步异常打印后终止当前 isolate；异步异常进入所在 `Zone` 的错误处理。

📘 [Dart · Exception](https://api.dart.dev/stable/dart-core/Exception-class.html)

{{% /tab %}}

{{% tab header="R" %}}

```r
new_config_error <- function(key) {
  structure(
    class = c("configError", "error", "condition"),
    list(message = paste("missing key:", key), call = NULL, key = key)
  )
}
stop(new_config_error("path"))
```

- 自定义错误：构造带自定义类名的 condition（处理器里可用 `inherits()` 判断）。
- 清理：`on.exit()`——函数退出（含出错）时执行，等价于 finally。
- 未捕获：停止当前表达式并打印错误；`options(error = ...)` 可改成进入调试器或记录日志。

📘 [R · on.exit](https://stat.ethz.ch/R-manual/R-devel/library/base/html/on.exit.html)

{{% /tab %}}

{{% tab header="Zig" %}}

```zig
const ConfigError = error{ MissingKey, Empty };

fn load(path: []const u8) ConfigError!void {
    errdefer std.log.err("load failed: {s}", .{path});   // 只在错误路径执行
    if (path.len == 0) return error.Empty;
    return error.MissingKey;
}
```

- 自定义错误：错误集（`error{...}`）就是类型，可以直接作为返回类型。
- 清理：`defer`（正常退出）与 `errdefer`（错误退出），没有 finally。
- 未捕获：`main` 返回错误联合时，未处理的错误会打印并让进程以非零码退出；`unreachable` 则是 UB。

📘 [Zig · errdefer](https://ziglang.org/documentation/master/#errdefer)

{{% /tab %}}

{{% tab header="Lua" %}}

```lua
local ConfigError = {}
ConfigError.__index = ConfigError

function ConfigError.new(key)
  return setmetatable({ message = "missing key: " .. key, key = key }, ConfigError)
end

error(ConfigError.new("path"))     -- 抛一个表
```

- 自定义错误：任意值都行，实践中用带 `message`/`code` 字段的表并用 `__tostring` 美化。
- 清理：没有 finally——用 `pcall` 包住代码，在返回后手动清理；5.4+ 也可用 `<close>` 变量。
- 未捕获：默认打印错误消息并终止脚本（`lua` 解释器退出码非 0）。

📘 [Lua 5.5 · error](https://www.lua.org/manual/5.5/manual.html#pdf-error)

{{% /tab %}}

{{% tab header="TypeScript" %}}

```ts
class ConfigError extends Error {
  constructor(public readonly key: string, options?: ErrorOptions) {
    super(`missing key: ${key}`, options);   // ES2022 的 cause
    this.name = "ConfigError";
  }
}
```

- 自定义错误：继承 `Error`；`cause` 字段携带原始错误；注意给 `name` 赋值。
- 清理：`try/finally`；资源用 `using` 声明（TS 5.2 的显式资源管理）。
- 未捕获：浏览器触发 `window.onerror`，Node 进程退出；异步走 `unhandledrejection`。

📘 [TS · 显式资源管理](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

```js
class ConfigError extends Error {
  constructor(key, options) {
    super(`missing key: ${key}`, options);
    this.name = "ConfigError";
    this.key = key;
  }
}

throw new ConfigError("path", { cause: new Error("io") });
```

- 自定义错误：继承 `Error`，用 `cause`（ES2022）串因果链；`AggregateError` 表示多个错误。
- 清理：`finally`；`Symbol.dispose` + `using`（ES2024 提案已落地于现代运行时）。
- 未捕获：Node 打印堆栈并退出；浏览器进 `window.onerror`；Promise 走 `unhandledrejection`。

📘 [MDN · Error.cause](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause)

{{% /tab %}}

{{% tab header="PHP" %}}

```php
class ConfigException extends RuntimeException {
    public function __construct(public readonly string $key, ?Throwable $previous = null) {
        parent::__construct("missing key: $key", 0, $previous);   // previous = cause
    }
}
```

- 自定义错误：继承 `Exception`/`RuntimeException`，用 `$previous` 串因果链。
- 清理：`finally`；文件句柄等在函数结束时自动关闭，数据库/锁需要显式释放。
- 未捕获：Fatal error + 堆栈（生产环境应关掉 `display_errors` 并记录日志）；`set_exception_handler` + shutdown 函数是最后一道网。

📘 [PHP · 扩展异常](https://www.php.net/manual/en/language.exceptions.extending.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

```ruby
class ConfigError < StandardError
  attr_reader :key
  def initialize(key)
    @key = key
    super("missing key: #{key}")
  end
end

raise ConfigError.new("path")
```

- 自定义错误：继承 `StandardError`（继承 `Exception` 会绕过默认 `rescue`）。
- 清理：`ensure`（等价于 finally）与块方法（`File.open { |f| ... }` 自动关闭）。
- 未捕获：打印堆栈并退出（退出码 1）；`at_exit` 可注册收尾逻辑。

📘 [Ruby · StandardError](https://docs.ruby-lang.org/en/master/StandardError.html)

{{% /tab %}}

{{< /tabpane >}}
