+++
title = "macro"
date = 2026-09-19T12:00:00+08:00
weight = 18
type = "docs"
description = "18 种语言的宏对照：C/C++ 预处理宏、声明式与语法宏、过程宏与编译期代码生成、没有宏的语言用什么替代"
isCJKLanguage = true
draft = false
+++

# 宏：18 种语言对照

宏是唯一一类"写起来像函数、实际却不是函数"的机制。本页按四个主题递进：**预处理宏**看 C/C++ 的文本替换到底提供了什么、**声明式与语法宏**看 Rust 与 Julia 如何把宏做成语法树层面的模式匹配、**过程宏与编译期代码生成**看编译器怎样被当成一个库来调用、**没有宏的语言用什么替代**看装饰器、元编程、代码生成与泛型各自能顶替到什么程度。最根本的分歧在于替换发生在哪一层：C 的预处理器在词法层做字符串替换，Rust 与 Julia 在语法树层做结构匹配，C# 的源生成器与 Java 的注解处理器干脆把工作交给一个在编译过程中运行的普通程序。第二个分岔是卫生性（hygiene），Rust 与 Julia 的宏默认让宏内新引入的名字不与调用点冲突，C 的宏什么也不保证。第三个分岔是时机，C# 与 Java 的生成器只能**新增**源码，不能修改已有的声明，这决定了它们能表达什么。

## 宏

**一页速览**

| 语言 | 宏机制 / 关键字 | 一句话说明 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | `macro_rules!`, `#[proc_macro_derive]`, `#[cfg]` | 声明式宏按 AST 片段匹配，过程宏在编译期运行 Rust 代码 | 卫生性是混合的：局部变量按定义点解析，其它符号按调用点解析 |
| Swift | 5.9 起 `macro` 与 `#externalMacro`，此前只有 `#if` | 宏声明与实现分离，实现依赖 swift-syntax 库 | 实现必须在独立 target，宏不能访问调用点的语义信息 |
| Go | 没有宏，用 `//go:generate`, `//go:build`, `//go:embed` | 用代码生成、编译约束、嵌入文件三件事代替 | `go generate` 只是执行命令，不参与依赖分析也不自动运行 |
| Python | 没有宏，用装饰器 + `ast` + `exec` | 全部发生在运行时，没有编译期阶段 | 装饰器改写的是对象而不是语法，`ast` 要自己接住源码 |
| Kotlin | 没有宏，用 KSP + 编译器插件 + 注解 | KSP 只看声明与类型，看不到函数体 | 生成的代码只能新增文件，不能修改已有源文件 |
| Java | 没有宏，用 JSR 269 注解处理器 | 处理器分轮运行，用 `Filer` 生成新源码 | 不能改动已有类，运行期还要靠注解与反射读回 |
| C++ | `#define` 全套预处理器 + 模板 / `consteval` | 文本替换与编译期求值两套体系长期并存 | 模板能替代函数宏，代价是报错信息极长 |
| C | `#define` 全套预处理器，`_Generic`, `_Static_assert`, C23 的 `constexpr` | 纯文本替换，没有类型、没有作用域、没有调试信息 | 缺括号、参数多次求值、运算符优先级三连坑 |
| Julia | `macro` 加 `esc` 与 `quote` | 解析期把 AST 变换成 AST，默认对局部变量卫生 | `esc` 用错会让宏内名字污染调用者的绑定 |
| C# | 没有文本宏，`#if` 条件编译 + 源生成器 + T4 | 生成器只能追加源码，不能改动已有声明 | `#define` 只影响 `#if`，没有宏体也没有参数 |
| Dart | 没有宏，用 `build_runner` 与 `source_gen` | 由独立进程在构建前生成 `.g.dart` 文件 | 多一个构建步骤，增量生成慢，注解只在生成期可见 |
| R | `substitute`, `bquote`, `quote` 的非卫生元编程 | 直接操作 `call` 与 `symbol` 对象，运行期改写表达式 | 它不是宏：没有卫生性，也没有独立的展开阶段 |
| Zig | 没有宏，用 `comptime`, `@typeInfo`, `inline for` | 用编译期求值代替语法扩展 | 编译期代码必须能被求值器执行，不能有副作用 |
| Lua | 没有宏，用 `load`, 元表, `debug` 库 | 运行期拼接字符串再加载成函数 | `load` 不做作用域检查，性能与安全都差 |
| TypeScript | 没有宏，用编译器 API / transformer + 5.0 标准装饰器 | 类型层面有条件类型，值层面靠 transformer 改 AST | 装饰器是运行时函数，要改 AST 得靠 `ts-patch` |
| JavaScript | 没有宏，用 Babel / SWC 插件 | 插件在构建期真正改写 AST | 多一层工具链，source map 与调试链路变复杂 |
| PHP | 没有宏，用 8.0 attributes + 8.4 属性钩子 + composer 脚本 | 注解靠反射在运行时读取，代码生成靠 composer 钩子 | 没有编译期，反射有性能代价，属性钩子不是宏 |
| Ruby | 没有宏，用 `define_method`, `method_missing`, `eval` | 一切都在运行时，连类都可以重新打开 | 全局 monkey patch 难以追踪，`eval` 有注入风险 |

### 预处理宏

C 的预处理器是唯一一个**在词法层面**工作的宏系统：它拿到的是一串预处理记号，不认识类型、不认识作用域、也不产生调试信息。下面 18 个标签页里只有 C 与 C++ 有这套东西，其余 16 种语言都要写明"没有 C 预处理器"以及各自的替代路径。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有 C 预处理器，也没有任何独立的文本替换阶段：`rustc` 直接把源码解析成 AST，编译期的一切都发生在类型系统内部。可用的替代品分三类：`macro_rules!` 做语法层替换、`#[cfg]` 与 `cfg!` 做条件编译、`include_bytes!` 与 `include_str!` 与 `env!` 与 `file!` 与 `line!` 与 `column!` 做编译期注入。最该先知道的是 `#[cfg]` 属于声明级属性，它只能整段保留或删除 item、语句、字段与参数，没法像 `#if` 那样切进表达式中间。

```rust
// 对象宏的对应物：零参数规则
macro_rules! pi { () => { 3.14159_f64 }; }
// 函数宏的对应物：带片段分类符的规则
macro_rules! square { ($x:expr) => { $x * $x }; }

#[cfg(not(test))]                                    // 替代 #ifndef
const DEBUG: bool = true;

fn main() {
    println!("{}", square!(3));                      // 9
    println!("{}", pi!());                           // 3.14159
    println!("{}", env!("PATH").is_empty());         // false  编译期读环境变量
    println!("{}", include_bytes!("data.txt").len()); // 5     替代 C23 的 #embed
    println!("{}", include_str!("data.txt"));        // hello
    println!("{}", line!() > 0);                     // true   替代 __LINE__
    println!("{}", file!().ends_with(".rs"));        // true   替代 __FILE__
    println!("{}", cfg!(not(test)));                 // true   两边都要能编译
    println!("{}", DEBUG);                           // true
}
```

`SQUARE(1 + 2)` 在 C 里展开成 `1 + 2 * 1 + 2` 是一个经典事故，而 `square!(1 + 2)` 匹配的是完整的 `expr` 片段，不可能出现这个问题——这是"匹配 AST 片段"与"替换文本"最直接的差别。`#[cfg]` 删除的代码不参与类型检查与借用检查，`cfg!(...)` 则相反：它两边都要能编译通过，只是运行期返回常量而被优化掉。Rust 没有 `#pragma once` 与头文件守卫的概念，因为模块系统按 crate 只编译一次；也没有 `__DATE__` 与 `__TIME__`，需要构建时间戳就用 `build.rs` 把它写进 `rustc-env`，再用 `env!` 读出来。真正需要"按条件生成不同代码"时，`#[cfg_attr]` 与 `cfg_if!` 这类 crate 比手写 `#[cfg]` 更清晰。

📘 [Rust · 条件编译](https://doc.rust-lang.org/reference/conditional-compilation.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 没有预处理器，但保留了 `#if` 系列的条件编译指令，它们由编译器前端求值，不是由独立程序做文本替换。可用条件包括 `os()`、`arch()`、`swift()`、`compiler()`、`canImport()`、`targetEnvironment()` 与 `hasFeature()`，也能用 `-D` 传入自定义标志。`#warning` 与 `#error` 这两个诊断指令从 Swift 4.2 起就可用（SE-0196），并不是 5.9 才补上的，它们对标 C23 的 `#warning` 与 `#error`。

```swift
#if os(macOS)                       // 平台分支，替代 #ifdef __APPLE__
let platform = "macOS"
#elseif os(Linux)
let platform = "Linux"
#else
let platform = "other"
#endif

#if swift(>=5.9)                    // 按编译器语言版本分支
let modern = true
#else
let modern = false
#endif

#if canImport(Foundation)           // 按模块可导入性分支
import Foundation
let hasFoundation = true
#else
let hasFoundation = false
#endif

func report() {
    #warning("对标 #warning：编译期警告")     // 编译时打印一条警告
    print(platform, modern, hasFoundation)   // macOS true true
}
report()
```

`-D` 标志打开的条件形如 `#if DEBUG`，写惯 C 的人要注意这里没有 `defined()`、没有 `#define MYMACRO 1`、也没有宏体：`#if` 的条件里只能出现布尔字面量、已定义标志、以及上面那批平台函数。被条件排除的代码完全不参与类型检查，所以 `#else` 分支里可以引用当前平台不存在的 API，这一点和 `#ifdef` 一样。`#sourceLocation(file:line:)` 可以改写后续诊断里的文件名与行号，用在对代码生成工具做映射的场景。

📘 [Swift · 条件编译语句](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/statements/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 明确没有预处理器：语言规范里没有宏这一章，`cmd/go` 也不理解 `#define`。替代品是三件事——`//go:build` 编译约束决定一个文件是否参与本次构建，`//go:embed` 把外部文件内容嵌进变量，`//go:generate` 只是约定格式的注释，由 `go generate` 这个显式命令去执行。最该先记住的是前两者是语言/工具链的正式机制，而 `go generate` 纯粹是一个"注释里写命令、然后手动跑"的约定。

```go
// 编译约束必须单独占一行，必须在 package 之前，并与它空一行
//go:build linux || darwin

package main

import (
	_ "embed"
	"fmt"
)

// 把文件内容编进二进制：替代 C23 的 #embed
//go:embed data.txt
var data string

const buildTag = "linux || darwin"

func main() {
	fmt.Println(data)          // hello
	fmt.Println(buildTag)      // linux || darwin
	fmt.Println(len(data))     // 5
}
```

条件编译在 Go 里没有"切进表达式"的能力：`//go:build` 的粒度是整个文件，要按平台给同一个函数不同实现，就得写 `foo_linux.go` 与 `foo_darwin.go` 两个文件，靠文件名后缀和约束行来筛选。约束行本身也挑剔：`//go:build` 必须独占一行，同一行后面再跟任何文字（哪怕看起来像注释）都会得到一个语法错误而不是警告（Go 1.27 实测报文是 `parsing //go:build line: invalid syntax at /`）；`//go:embed` 同理，它后面整行都是文件模式列表，再补一句中文解释就会被当成模式名，报出 `pattern 这里是解释: no matching files found` 这种莫名其妙的错误——模式名就是那串多余文字。注入版本的常见做法是 `go build -ldflags "-X main.version=1.2.3"`，往字符串变量里写值，效果等价于 `#define VERSION "1.2.3"`。`go:embed` 支持 `string`、`[]byte` 与 `embed.FS` 三种目标类型，放入 `string` 的必须是 UTF-8 文本。`go generate` 不会自动执行，CI 与提交的代码里必须包含生成结果，否则本地能编、远端拉下来就报错。

📘 [Go · 构建约束](https://pkg.go.dev/cmd/go)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有预处理器，也没有编译期常量：所有"条件编译"最后都退化成普通的模块级 `if`，区别只在于判断的是 `sys.platform`、`sys.version_info`、`os.environ` 还是 `__debug__`。类型层面的条件分支靠 `typing.TYPE_CHECKING`，它对类型检查器为真、对解释器为假，于是可以在里面写只为检查器准备的 `import`。

```python
import sys
from functools import singledispatch
from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # 只有类型检查器看得见，运行时不执行
    from collections.abc import Sequence

assert sys.version_info >= (3, 10)      # 运行期断言，不是编译期检查
DEBUG = __debug__                       # python -O 运行时为 False

@singledispatch                         # 用单分派替代 C11 的 _Generic
def describe(x):
    return "unknown"
@describe.register
def _(x: int):
    return "int"
@describe.register
def _(x: str):
    return "str"

print(sys.platform)                     # darwin 或 linux
print(describe(1), describe("a"), describe(1.5))   # int str unknown
print(DEBUG)                            # True
```

`__debug__` 是 Python 里唯一真正"由编译开关决定"的东西：`python -O` 会把 `__debug__` 置为 `False`，同时把所有 `assert` 语句整段丢掉，这就是 Python 版的 `#ifndef NDEBUG`。`singledispatch` 在用类型选择实现这一点上最接近 `_Generic`，但它在运行期查表，而 `_Generic` 是编译期选表达式，遇到含副作用的实参时两者的求值次数不一样。`exec` 与 `compile` 能生成代码，但那是运行时代码生成，不是预处理；如果只是想让不同平台走不同实现，用模块级的 `if sys.platform == "darwin":` 加函数定义，比字符串拼接再 `exec` 安全得多。

📘 [Python · sys 模块](https://docs.python.org/3/library/sys.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 没有预处理器，也没有宏：`#define`、`#if`、`#include` 一概不存在。条件编译靠三样东西实现——多平台项目里的 `expect` 与 `actual` 声明、Gradle 源集（source set）把不同目录编进不同产物、以及构建脚本注入的 `BuildConfig` 常量。`const val` 是编译期常量，会被内联到使用处，这是 Kotlin 里最接近对象宏的写法。

```kotlin
// 多平台：声明与实现分离，替代 #ifdef 平台分支
expect fun platformName(): String

// 编译期常量：会被内联进调用点，等价于 #define MAX_RETRY 3
const val MAX_RETRY = 3

// JVM 上唯一类似 #if 的东西是构建工具注入的常量
// Gradle: buildConfigField("boolean", "DEBUG", "true")
object BuildConfigLike {
    const val DEBUG = false          // 由源集或代码生成决定真假
}

fun main() {
    println(MAX_RETRY)               // 3
    println(BuildConfigLike.DEBUG)   // false
    if (BuildConfigLike.DEBUG) {     // 编译期常量条件，编译器能整段消除
        println("only in debug")
    }
}
```

`const val` 必须是顶层或 `object` 成员，类型只能是基本类型或 `String`，而且初始化式必须是编译期常量表达式——这三条限制让它无法像 `#define` 那样展开任意代码。`expect` 与 `actual` 是语言级机制，比 `#ifdef` 更严格：编译器会强制要求每个目标平台都提供 `actual` 实现，漏一个就编译失败，而 `#ifdef` 忘记写 `#else` 只会静默地少一段代码。真正的编译期代码生成要交给 KSP 或编译器插件，放在第三个子主题里讲。

📘 [Kotlin · 注解](https://kotlinlang.org/docs/annotations.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 完全没有预处理器：JLS 目录里没有宏，`javac` 也不做文本替换或文件包含。条件编译只能靠 `static final` 常量加 `if`——JLS 的常量表达式规则配合 `if` 语句的可达性分析，让 `javac` 能把条件恒假的分支整段从字节码里删掉。运行时开关用 `assert` 加 `-ea`，构建期分支用 Maven profile 或 Gradle source set。

```java
public class Main {
    // 常量表达式 + if = Java 唯一的“编译期分支”
    private static final boolean DEBUG = false;
    private static final int MAX_RETRY = 3;

    public static void main(String[] args) {
        if (DEBUG) {                       // javac 会整段删除这个分支
            System.out.println("only in debug");
        }
        System.out.println(MAX_RETRY);     // 3
        assert args.length >= 0;           // 需要 -ea 才生效
        System.out.println(String.join(",", args));  // 传入参数拼接
    }
}
```

把 `DEBUG` 写成 `static final` 而不是普通字段是关键：只有编译期常量才能触发死代码消除，而 `public static final` 常量还会被内联到调用方的字节码里，此后修改常量值不会影响已编译的调用方，这是升级库时的一个经典陷阱。`assert` 与 C 的 `assert` 一样需要显式开启，但它抛的是 `AssertionError` 而不是 `abort`。字符串拼接式的"宏"在 Java 里没有市场，因为哪怕用 `String` 常量拼出合法代码也无法在编译期插入到当前类中——真正的代码生成只有注解处理器一条路，放在第三个子主题。

📘 [JLS · 常量表达式](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 同时拥有两套机制：预处理器负责词法层的文本替换，编译器负责模板与 `constexpr` 的编译期求值。现代 C++ 的共识是能用 `inline` 函数、模板或 `constexpr` 表达的意思就不要写成宏，因为宏没有类型检查、没有作用域、不进调试信息，还会和命名空间、重载、模板参数里的逗号互相干扰。C++20 补上了 `__VA_OPT__`，C++23 补上了 `#elifdef` 与 `#elifndef` 以及标准化的 `#warning`。

```cpp
#include <cstdio>
#include <source_location>
#include "guard.hpp"

#define VERSION 3
#define SQUARE(x) ((x) * (x))          // 每个参数都要加括号
#define STR(x) #x                      // # 把实参变成字符串
#define XSTR(x) STR(x)                 // 两级展开才能把宏参数也展开
#define CAT(a, b) a##b                 // ## 拼接记号
#define LOG(...) std::printf(__VA_ARGS__)
/* 多行宏用反斜杠续行，续行符后不能有任何字符 */
#define CHECK(cond) do {                          \
        if (!(cond)) std::printf("failed: %s\n", #cond); \
    } while (0)
#define LOGF(fmt, ...) std::printf(fmt __VA_OPT__(,) __VA_ARGS__)  // C++20

#if defined(VERSION) && VERSION >= 3
#  define LEVEL 3
#elifdef FALLBACK                      // C++23 新增的 #elifdef / #elifndef
#  define LEVEL 2
#else
#  define LEVEL 1
#endif

#ifndef FROM_HEADER
#  error "guard.hpp 没有被包含进来"
#endif

#if __has_include(<string_view>)       // C++17 起的 __has_include
#  define HAS_SV 1
#endif

#ifdef EMIT_WARNING
#  warning "显式打开的警告"
#endif

// 编译期计算的替代路线：模板 + constexpr + consteval + inline 函数
template <typename T> constexpr T square(T x) { return x * x; }
inline int square_i(int x) { return x * x; }     // inline 函数替代函数宏
consteval int twice(int n) { return n * 2; }     // C++20：只允许编译期求值
constinit static int counter = 0;                // C++20：必须静态初始化

int main() {
    std::printf("%d\n", SQUARE(1 + 2));                  // 9
    std::printf("%s %s\n", STR(VERSION), XSTR(VERSION)); // VERSION 3
    int CAT(my, var) = 7;
    std::printf("%d\n", myvar);                          // 7
    CHECK(myvar == 7);                                   // 条件成立，什么都不打印
    LOGF("no varargs\n");                                // no varargs
    LOG("with %d\n", 1);                                 // with 1
    std::printf("%d %d %d\n", LEVEL, HAS_SV, FROM_HEADER);  // 3 1 1
    std::printf("%d %d %d\n", square(3), square_i(3), twice(21));  // 9 9 42
    auto loc = std::source_location::current();          // 替代 __LINE__，且是类型安全的
    std::printf("%s:%d %s\n", __FILE__, __LINE__, loc.function_name());  // 文件、行号、函数名
    std::printf("%s %s\n", __DATE__, __TIME__);          // 编译日期与时间
    std::printf("%d\n", counter);                        // 0
#undef LEVEL
#ifndef LEVEL
    std::printf("undef ok\n");                           // undef ok
#endif
    return 0;
}
```

`guard.hpp` 里只有两条指令：

```cpp
#pragma once                      // 现代写法；传统写法是 #ifndef GUARD_HPP 守卫
#define FROM_HEADER 1
```

`STR` 与 `XSTR` 的两级写法是所有 C 系代码里最反直觉的一处：`STR(VERSION)` 得到字面量 `"VERSION"`，`XSTR(VERSION)` 才得到 `"3"`，因为 `#` 会阻止实参被展开。`__VA_OPT__(,)` 解决的是"零可变参数时留下多余逗号"的老问题：`LOGF("no varargs\n")` 展开后没有尾逗号，而 `LOGF("%d\n", 1)` 会带上逗号。多行宏只能靠反斜杠续行，续行符必须是该行最后一个字符，`do { ... } while (0)` 则保证宏在 `if (x) CHECK(y); else ...` 里不会散架。`std::source_location::current()` 是 `__LINE__` 的类型安全替代，它作为默认实参求值，得到的正是调用点位置。命名空间里的宏不受命名空间限制，`#define` 一旦生效就污染整个翻译单元的后续文本，这是宏与命名空间最恶劣的相互作用；另外 `MACRO(a, b)` 里如果实参是 `std::map<int, int>`，未加括号的逗号会被当成两个参数，必须写成 `MACRO((std::map<int, int>))` 或改用模板。

📘 [cppreference · 替换文本宏](https://en.cppreference.com/w/cpp/preprocessor/replace)

{{% /tab %}}

{{% tab header="C" %}}

C 的预处理器是这门语言里唯一的元编程设施，也是全页唯一在词法层工作的宏系统。它有七个指令族：`#define` 与 `#undef`、`#include`、`#if` 族、`#error` 与 `#warning`、`#pragma`、`#line`、以及 C23 新增的 `#embed`。它不认识类型、不认识作用域、不产生调试信息，所有能力与所有陷阱都来自这一点。

```c
#include <stdio.h>
#include "guard.h"                       /* #include：文本包含，guard.h 见下一个代码块 */

#define VERSION 3                        /* 对象宏 */
#define SQUARE(x) ((x) * (x))            /* 函数宏：每个参数都要加括号 */
#define STR(x) #x                        /* #：把实参变成字符串字面量 */
#define XSTR(x) STR(x)                   /* 两级展开，让实参也展开 */
#define CAT(a, b) a##b                   /* ##：拼接两个记号 */
#define LOG(...) fprintf(stderr, "[log] " __VA_ARGS__)             /* C99 */
/* do { } while (0)：多行宏的惯用法，用反斜杠续行，行尾不能有空格 */
#define CHECK(cond) do {                         \
        if (!(cond)) {                           \
            printf("check failed: %s\n", #cond); \
        }                                        \
    } while (0)
#define LOGF(fmt, ...) printf(fmt __VA_OPT__(,) __VA_ARGS__)       /* C23 */

/* C23 的 #embed：把文件字节展开成整数字面量列表 */
static const unsigned char payload[] = {
#embed "data.txt"
};
_Static_assert(sizeof payload == 5, "payload must be 5 bytes");    /* C11 */

/* C11 的 _Generic：编译期按类型选择表达式 */
#define TYPE_NAME(x) _Generic((x), int: "int", double: "double", char *: "char*", default: "other")

#if defined(VERSION) && VERSION >= 3     /* #if / #ifdef / #ifndef / #defined */
#  define LEVEL 3
#elifdef FALLBACK                        /* C23：#elifdef / #elifndef */
#  define LEVEL 2
#elif VERSION >= 2
#  define LEVEL 2
#else
#  define LEVEL 1
#endif

#ifdef __STDC_VERSION__                  /* 预定义宏：C 标准版本 */
#  if __STDC_VERSION__ >= 202311L
#    define IS_C23 1
#  endif
#endif

#if __has_include(<stdio.h>)             /* C23：头文件存在性检测 */
#  define HAS_STDIO 1
#endif

#if __has_embed("data.txt") == __STDC_EMBED_FOUND__
#  define EMBED_OK 1
#endif

#ifdef EMIT_WARNING
#  warning "显式打开的警告，C23 起是标准指令"
#endif
#if 0
#  error "条件为假，这行不会被编译"
#endif

int main(void) {
    printf("%d\n", VERSION);             /* 3 */
    printf("%d\n", SQUARE(1 + 2));       /* 9：括号保住了运算顺序 */
    printf("%s %s\n", STR(VERSION), XSTR(VERSION));   /* VERSION 3 */
    int CAT(my, var) = 7;
    printf("%d\n", myvar);               /* 7 */
    LOG("level=%d\n", LEVEL);            /* [log] level=3，写到 stderr */
    CHECK(myvar == 7);                   /* 条件成立，什么都不打印 */
    LOGF("no varargs\n");                /* no varargs */
    LOGF("with %d\n", 1);                /* with 1 */
    printf("%d %s %s\n", payload[0], TYPE_NAME(1), TYPE_NAME(1.5));  /* 104 int double */
    printf("%d %d %d\n", FROM_HEADER, HAS_STDIO, IS_C23);   /* 1 1 1 */
    printf("%d\n", EMBED_OK);            /* 1 */
    printf("%s %d %s\n", __FILE__, __LINE__, __func__);   /* 文件、行号、函数名 */
    printf("%s %s\n", __DATE__, __TIME__);                /* 编译日期与时间 */
#undef LEVEL                             /* #undef：取消定义 */
#ifndef LEVEL
    printf("undef ok\n");                /* undef ok */
#endif
    return 0;
}
```

`guard.h` 里就是两条最常见的指令：

```c
#pragma once                     /* 现代写法；传统写法是 #ifndef GUARD_H 守卫 */
#define FROM_HEADER 1
```

C23 把好几个老扩展收进了标准：`__has_include`、`__has_embed`、`__VA_OPT__`、`#elifdef`、`#elifndef`、`#warning` 都是 C23 新标准化的，`#embed` 更是全新指令，它把文件字节展开成一串整数常量，正好可以初始化数组，替代过去必须靠外部脚本生成的 `xxd -i` 头文件。C11 的 `_Generic` 提供了第一个（也是目前唯一一个）编译期按类型选择表达式的机制，C11 的 `_Static_assert` 提供了编译期断言，C23 又给了 `constexpr` 变量与 `static_assert` 关键字。

多行宏只能靠反斜杠续行，续行符必须是该行的最后一个字符，后面连一个空格都不能有，所以 `do { ... } while (0)` 才成为标准惯用法：它把多条语句包成一个语句，放在 `if (x) CHECK(y); else ...` 这种位置不会因为分号或大括号而散架。传统头文件守卫用 `#ifndef` 加 `#define` 包住整个头文件，`#pragma once` 更简洁但它不在语言标准里、只是被所有主流实现支持。三个最常见的翻车点：`SQUARE(i++)` 会自增两次，因为参数在宏体里出现两次；`SQUARE(i + 1)` 若宏体没加括号会得到 `i + 1 * i + 1`；`#define DEBUG 0` 之后 `#if DEBUG` 为假，但如果写成 `#ifdef DEBUG` 反而为真——判断"有没有定义"和判断"值是多少"绝不能混用。

📘 [cppreference · C 预处理](https://en.cppreference.com/w/c/preprocessor/replace)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 没有预处理器，也明确把自己和 C 的文本宏区分开：它的宏在**解析期**工作，输入输出都是 AST 对象（`Expr` 与 `Symbol`），因此不需要额外的构建步骤。条件编译由 `@static` 提供，它要求条件在解析期就能求值成布尔量；文件与位置信息由 `@__FILE__`、`@__LINE__`、`@__MODULE__` 这几个宏给出。

```julia
macro twice(ex)
    return quote
        local v = $(esc(ex))     # esc：放到调用者作用域里求值
        v + v
    end
end

@static if Sys.isapple()          # 解析期条件编译，等价于 #ifdef __APPLE__
    const PLATFORM = "macOS"
else
    const PLATFORM = "other"
end

const DATA = read(joinpath(@__DIR__, "data.txt"), String)   # 替代 #embed

println(@twice(21))              # 42
println(PLATFORM)                # macOS
println(length(DATA))            # 5
println(@__FILE__)               # 当前文件名，替代 __FILE__
```

`@static if` 与普通 `if` 的区别在于求值时机：`@static` 的条件必须在解析期是常量，因此两条分支里可以放类型不同、甚至当前平台根本不存在的代码；普通 `if` 则要求两边都能编译。`@__FILE__` 与 `@__LINE__` 是宏而不是魔法变量，所以能出现在任何表达式位置并被内联到 AST 里。`@__DIR__` 给出的是**当前文件所在目录**，这在 `include` 别的文件时比 `pwd()` 可靠得多。跨平台条件还可以写成 `@static if VERSION >= v"1.13"`，用来按 Julia 版本切换实现。

📘 [Julia · 元编程](https://docs.julialang.org/en/v1/manual/metaprogramming/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有预处理器**指令**，但没有预处理宏：`#define` 只能定义一个没有值的符号，供 `#if` 判断真假，不能带参数、不能带宏体、也不能做文本替换。可用指令包括 `#define`、`#undef`、`#if`、`#elif`、`#else`、`#endif`、`#error`、`#warning`、`#line`、`#nullable`、`#region` 与 `#endregion`，再加上 `#pragma warning` 与 `#pragma checksum`。最该先分清的是"条件编译"与"代码生成"：`#if` 只能整段取舍源码，真要生成代码得靠源生成器（第三个子主题）。

```csharp
#define FEATURE_X                        // 只能定义符号，不能定义值
#undef  FEATURE_Y

using System;
using System.Diagnostics;

public class Main1 {
    [Conditional("FEATURE_X")]           // 调用点按符号整段消失
    static void Trace(string msg) => Console.WriteLine(msg);

    public static void Main() {
#if FEATURE_X
        Console.WriteLine("FEATURE_X on");    // FEATURE_X on
#elif FEATURE_Y
        Console.WriteLine("FEATURE_Y on");
#else
        Console.WriteLine("neither");
#endif
        Trace("traced");                 // traced：符号已定义
        Console.WriteLine(DEBUG_SYMBOL);  // 由 -define 或 csproj 决定
#line 200 "generated.cs"                 // 改写后续诊断的行号与文件名
        Console.WriteLine("line remapped");
    }

#if DEBUG_SYMBOL
    const string DEBUG_SYMBOL = "debug";
#else
    const string DEBUG_SYMBOL = "release";
#endif
}
```

`#define` 必须出现在文件里任何"真实"记号之前，C# 编译器读完整行注释后才会处理它，所以不能像 C 那样在文件中间改宏。`#if` 的表达式支持 `&&`、`||`、`!`、`==`、`!=` 与括号，操作数只能是符号名或 `true`/`false`，没有算术也没有字符串比较。`[Conditional("SYM")]` 是比 `#if` 更好的选择：把开关写在一处，调用点自动按符号取舍，还能避免 `#if` 包住的代码忘记更新另一半。`#nullable enable` 这类指令影响的是编译器分析模式，而 `#region` 只影响 IDE 折叠——两者都不改变生成结果。

📘 [MS Learn · C# 预处理器指令](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/preprocessor-directives)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有预处理器。条件编译靠三件事：`assert` 语句（`--enable-asserts` 控制，生产构建里整段移除）、常量环境声明（`const bool.fromEnvironment` 与 `String.fromEnvironment`，值由 `--define` 或 `dart-define-from-file` 注入）、以及条件导入（`import` 的 `if (dart.library.io)` 语法按可用库选择实现）。文件嵌入没有直接对应物，通常把资源写成 Dart 常量或用 `build_runner` 生成。

```dart
import 'dart:io' if (dart.library.html) 'dart:html' as impl;  // 条件导入

// 构建期注入的常量：dart run --define=DEBUG=true
const bool debugMode = bool.fromEnvironment('DEBUG', defaultValue: false);
const String apiUrl = String.fromEnvironment('API_URL', defaultValue: '/api');

void main() {
  assert(() {                       // 只在 --enable-asserts 下执行
    print('assertions on');
    return true;
  }());
  print(debugMode);                 // false（未传 --define 时）
  print(apiUrl);                    // /api
  print(impl.Platform.numberOfProcessors > 0);   // true
}
```

`bool.fromEnvironment` 与 `String.fromEnvironment` 必须是 `const` 上下文才有意义：只有常量才能在编译期被消除，进而让整个 `if (debugMode)` 分支从产物里消失，这与 Java 的 `static final` 常量折叠是同一套思路。条件导入的粒度是库而不是表达式，写法固定为 `import 'A' if (condition) 'B'`，条件里只能写 `dart.library.X` 这种库可用性判断。`assert` 里的回调形式 `assert(() { ...; return true; }())` 是 Dart 里放"调试专用逻辑"的标准惯用法，因为整块在关闭断言时不会被编译进产物。

📘 [Dart · 库与条件导入](https://dart.dev/language/libraries)

{{% /tab %}}

{{% tab header="R" %}}

R 没有预处理器：`#` 是注释符，不是指令起始符，所以 `#define`、`#if` 在 R 里根本不成立。条件执行是普通的 `if`，判断依据是 `Sys.getenv`、`capabilities()`、`R.version` 这些运行时信息。R 包在**编译 C/C++ 源码**时确实有类似预处理的机制，那由 `src/Makevars` 里的 `PKG_CPPFLAGS` 与 R 自身的配置头文件提供，属于 C 侧而不是 R 侧。

```r
# 下面全是运行期判断，没有编译期这一层
if (.Platform$OS.type == "windows") {          # 平台分支
  path_sep <- "\\"
} else {
  path_sep <- "/"
}

has_png <- capabilities("png")                 # 能力探测，运行时查询
r_version <- paste(R.version$major, R.version$minor, sep = ".")

# 替代“文件嵌入”：运行时读入，或把数据做成 .rda 随包分发
data <- readBin("data.txt", "raw", n = 5L)

cat(path_sep, "\n")                            # /
cat(has_png, "\n")                             # TRUE 或 FALSE
cat(r_version, "\n")                           # 4.6.0
cat(length(data), "\n")                        # 5
```

R 的 `if` 是运行期语句，一旦写成 `if (cond) x <- 1 else x <- 2` 就必然在运行期求值；想控制"包被加载时执行什么"，用的是 `.onLoad` 与 `.onAttach` 钩子，而不是条件编译。需要按 OS 编译不同 C 代码时，做法是给 `src/Makevars` 与 `src/Makevars.win` 两份文件，或在 `configure` 脚本里探测后生成 `Makevars`，这实际上是把预处理推给了 make 与 shell。真正意义上的"编译期"在 R 里只有 byte compiler（`compiler::cmpfun`），它把函数编译成字节码来提速，但不改变语义、也不做条件求值。

📘 [R · 语言定义](https://cran.r-project.org/doc/manuals/r-release/R-lang.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有预处理器，也没有宏，这是刻意的设计：`comptime` 让"编译期"成为语言内的一等概念，凡是能静态求值的都能在编译期算出来。对应关系很清楚——`#if` 对应 `comptime` 块与 `if` 在编译期求值的分支，`#include` 对应 `@import`，`#embed` 对应 `@embedFile`，`#error` 对应 `@compileError`，`#warning` 对应 `@compileLog`。再加上 `build.zig` 把构建期选项注入成模块常量。

```zig
const std = @import("std");
const build_options = @import("build_options");   // 由 build.zig 注入

// 编译期常量：等价于 #define VERSION 3
const version: u32 = 3;

// 等价于 #embed：把文件内容读成编译期已知的字节数组
const data = @embedFile("data.txt");

pub fn main() !void {
    // 编译期分支：条件必须是 comptime 可求值的
    if (comptime version >= 3) {
        std.debug.print("modern\n", .{});          // modern
    }

    // 编译期断言，条件不成立直接编译失败：等价于 #error
    comptime {
        if (version < 3) @compileError("version too old");
        @compileLog(version);                      // 编译时打印：3
    }

    std.debug.print("{d}\n", .{data.len});         // 5
    std.debug.print("{s}\n", .{build_options.mode});  // debug 或 release
    std.debug.print("{s}\n", .{@typeName(@TypeOf(version))});  // u32
}
```

`if (comptime cond)` 与普通 `if` 的区别在于是否要求条件静态已知：写成 `comptime` 前缀后，未选中的分支仍然要能通过语义分析（不像 Zig 的运行期 `if` 那样完全跳过），但分支本身会在编译期被裁掉。`@compileError` 的实参必须是编译期字符串，`@compileLog` 则在编译时把值打印出来，这两者是 Zig 里唯一的"编译期诊断"手段，配合 `@typeInfo` 就能写出针对类型结构报错的检查。`build.zig` 侧的典型写法是 `const opts = b.addOptions(); opts.addOption([]const u8, "mode", "release"); exe.root_module.addOptions("build_options", opts);`，这样 `@import("build_options")` 就能拿到构建期决定的常量，等价于 `#define` 加 `-D`。

📘 [Zig · 语言参考](https://ziglang.org/documentation/master/)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有预处理器，也没有条件编译：`#` 在 Lua 里是长度运算符，`--` 才是注释。替代路径是运行期拼接字符串再 `load`，以及用元表改写行为；平台差异靠 `package.config`、`jit` 全局表、`os.getenv` 这类运行时探测。最简单也最常用的"文件嵌入"办法是让构建脚本把资源写成 Lua 源码（`return "..."`）再 `require`。

```lua
-- 运行期条件，不是编译期分支
local sep = package.config:sub(1, 1)          -- "/" 或 "\\"
local is_luajit = rawget(_G, "jit") ~= nil

-- 运行期“代码生成”：拼接字符串再加载
local src = "return function(a, b) return a * b end"
local mul = load(src)()                        -- load 返回函数或 nil 加错误
print(mul(6, 7))                               -- 42

-- 元表：改写字段访问，替代“编译期注入”
local cfg = setmetatable({}, { __index = function(_, k) return "missing:" .. k end })
print(sep)                                     -- /
print(is_luajit)                               -- true 或 false
print(cfg.timeout)                             -- missing:timeout
```

`load` 与 `loadstring`（5.1 里的旧名）能编译任意字符串，但它们不检查自由变量来自哪里：默认用调用方的 `_ENV`，也可以显式传环境表来限制可见全局，这是沙箱化的关键。`load` 失败返回 `nil` 加错误消息而不是抛异常，所以正确写法是 `local f, err = load(src); assert(f, err)`。运行时拼代码的代价很实在：多一次解析、难以调试、容易引入注入漏洞，所以除了配置表与简单 DSL，能写成普通函数就不要用 `load`。Lua 里也没有 `#pragma once` 的问题，`require` 自带缓存。

📘 [Lua 5.5 · load](https://www.lua.org/manual/5.5/manual.html#pdf-load)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有预处理器，也没有宏：`#` 在 TS 里只出现在私有字段名前面。类型层面的条件编译由条件类型（`T extends U ? X : Y`）承担，值层面的"编译期常量"要靠打包器定义替换（Vite 的 `define`、webpack 的 `DefinePlugin`）或 `ts-patch` 之类的 transformer。`as const` 与字面量类型能让编译器把值收紧到具体字面量，这是 TS 里最接近"编译期常量折叠"的能力。

```typescript
// 类型层面的条件编译：条件类型在编译期求值，运行时不产生任何代码
type IsString<T> = T extends string ? true : false;
type A = IsString<"x">;      // true（字面量收窄）
type B = IsString<1>;        // false

// 值层面的“编译期常量”由打包器 define 替换，例如 define: { __DEBUG__: false }
declare const __DEBUG__: boolean;
declare const __VERSION__: string;

type Config = { readonly version: string; readonly retries: 3 };
const cfg = { version: "1.0", retries: 3 } as const;   // 字面量类型，readonly

export function describe(v: A): string {
  return v ? "string" : "not string";
}

console.log(cfg.version);            // 1.0
console.log(cfg.retries);            // 3
console.log(describe(true));         // string
// console.log(describe(false));     // 编译错误：false 不是 true 类型
```

条件类型是纯粹的类型运算，它不改变生成的 JavaScript，也不会帮你删掉运行时代码；真正让 `if (__DEBUG__)` 整段消失的是打包器的常量替换加压缩器的死代码消除。`as const` 把对象变成只读且保留字面量类型，效果类似 `#define` 加 `const`，但它是 TypeScript 的类型层面约束，运行时对象依然可变。需要真正改写 AST（比如自动生成校验函数、自动加日志）就要用编译器 API 写 transformer，并且因为 `tsc` 本身不加载自定义 transformer，还得借助 `ts-patch` 或直接换成 Babel / SWC 插件。

📘 [TypeScript · 条件类型](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有预处理器，也没有宏。运行时能拿到的最接近"条件编译"的东西是打包器注入的变量：webpack 与 Vite 会把 `process.env.NODE_ENV` 或 `import.meta.env.MODE` 替换成字符串字面量，随后压缩器把恒假分支整段删掉。`/*#__PURE__*/` 这类注释是给压缩器的标注，不是语言语法。

```javascript
// 打包器会把 process.env.NODE_ENV 替换成 "production"，随后死代码消除
if (process.env.NODE_ENV !== "production") {
  console.log("dev only");            // 直接 node 跑会打印；打包后整段消失
}

// Vite 风格：import.meta.env 也是替换出来的字面量（此处手工模拟）
const env = { MODE: "production", DEV: false };
if (env.DEV) {
  console.log("dev only, vite");      // 条件为常量假，压缩后整段消失
}

// /*#__PURE__*/ 告诉压缩器这个调用没有副作用，可以整句删除
const value = /*#__PURE__*/ createThing();

function createThing() {
  console.log("called");              // 未压缩时会打印
  return 1;
}

console.log(env.MODE);       // production
console.log(value);          // 1
console.log(typeof window);  // undefined（Node）或 object（浏览器）
```

`process.env.NODE_ENV` 在 Node 里是真实存在的运行时对象，在浏览器打包产物里则是被文本替换掉的常量，这导致同一行代码在两种环境下语义不同：没被替换时恒为 `undefined`，于是 `!== "production"` 恒真，dev 分支永远不会被消除。`import.meta` 是 ES 模块的正式语法，`import.meta.env` 里的 `env` 是打包器自定义的字段，Node 原生并不提供。`globalThis` 是判断运行环境的可靠入口，比 `typeof window` 更通用。

📘 [MDN · import.meta](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import.meta)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有预处理器，也没有宏：`#` 是注释符，`#if` 不是指令。条件执行是普通的 `if`，判断依据是 `PHP_VERSION_ID`、`extension_loaded()`、`function_exists()`、`PHP_OS_FAMILY` 这些运行时信息；`defined()` 与 `define()` 操作的是运行时常量，不是编译期符号。`declare(strict_types=1)` 与 `declare(ticks=1)` 是唯一带点"指令"味道的语法。

```php
<?php
if (PHP_VERSION_ID >= 80400) {                 // 运行期版本分支
    echo "PHP 8.4+\n";                          // PHP 8.4+
} else {
    echo "older PHP\n";
}

define('APP_VERSION', '3');                     // 运行时常量，不是宏
const MAX_RETRY = 3;                            // 编译期常量（不能用于条件编译）

if (!extension_loaded('mbstring')) {            // 能力探测
    echo "mbstring missing\n";
}

#[\Attribute]                                   // 8.0 的属性，靠反射在运行时读取
class Route { public function __construct(public string $path) {} }

echo APP_VERSION, "\n";                         // 3
echo MAX_RETRY, "\n";                           // 3
echo PHP_OS_FAMILY, "\n";                       // Darwin 或 Linux
echo (new ReflectionClass(Route::class))->getAttributes()[0]->getName(), "\n";  // Route
```

`const` 在顶层与 `define()` 的差别值得记牢：`const` 是编译期定义的、不能放在 `if` 里，`define()` 是运行期执行的、可以条件性定义，但两者都只是值，不能像 `#define` 那样替换代码。属性（attributes）是 PHP 8.0 引入的注解语法，`#[Attribute]` 标记可被反射读取的类，读取发生在运行时，代价是一次反射调用，所以框架通常会把结果缓存起来。真要在构建期生成代码，做法是 composer 的 `post-autoload-dump` 脚本或 `--no-dev` 之外的独立生成步骤，而不是语言本身。

📘 [PHP · 常量](https://www.php.net/manual/en/language.constants.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有预处理器：`#` 是注释起始符，`#if` 不存在。条件执行靠 `if` 与 `defined?`，平台差异靠 `RUBY_PLATFORM`、`RbConfig::CONFIG`、`Gem.win_platform?` 这些运行时信息，位置信息由 `__FILE__`、`__LINE__`、`__dir__`、`__method__` 这些关键字直接给出。唯一形式上像"pragma"的是文件第一行的魔法注释，例如 `# frozen_string_literal: true`。

```ruby
# frozen_string_literal: true

puts __FILE__                       # s1.rb   替代 __FILE__
puts __LINE__                       # 4       替代 __LINE__
puts defined?(String).inspect       # "constant"
puts RUBY_PLATFORM                  # arm64-darwin25
puts RbConfig::CONFIG["host_os"]    # darwin25

if RUBY_VERSION >= "3.0"            # 运行期版本分支，没有预处理
  puts "modern"
end

# 字符串冻结：魔法注释生效后字面量不可变
s = "abc"
puts s.frozen?                      # true
```

魔法注释只在文件第一行（或 shebang 之后的第二行）生效，写错位置会被静默忽略；而且这一行除了注释本身不能再跟别的内容——写成 `# frozen_string_literal: true` 后面再补一句说明，Ruby 就不认它，`"abc".frozen?` 会回到 `false`，这是最隐蔽的一处陷阱。`defined?` 返回的是字符串或 `nil` 而不是布尔值，所以判断时最好写 `!defined?(X).nil?` 或直接用 `if defined?(X)`。Ruby 的常量（大写开头）与 C 的宏完全不是一回事：它只是一个绑定了对象的常量名，可以重新赋值（会有警告），也不会在编译期替换任何代码。

📘 [Ruby · Kernel](https://docs.ruby-lang.org/en/master/Kernel.html)

{{% /tab %}}

{{< /tabpane >}}

### 声明式与语法宏

这一节的核心问题是：宏到底在**语法层面**替换还是在**AST 层面**变换。Rust 的 `macro_rules!` 匹配的是记号树与语法片段，Julia 的 `macro` 接住的是 `Expr` 对象，两者都属于"用模式描述语法结构再产出新语法结构"；而 C 的 `#define` 只是文本，PHP 的 attributes、Ruby 的 `define_method`、Python 的装饰器都发生在运行时，它们不是宏。第三个概念是卫生性：宏展开后新引入的名字会不会和调用点的名字撞车。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

`macro_rules!` 是 Rust 的声明式宏（macro by example），它由"匹配器 + 转写器"成对组成，匹配的是记号树与语法片段而不是文本。它属于编译期机制：展开发生在类型检查之前，展开结果必须是合法的语法结构，宏名字本身在名字解析阶段处理。最该先知道的两件事是完整片段分类符列表，以及 Rust 的卫生性是**混合位置**的。

```rust
// 匹配器 => 转写器；多条规则从上到下尝试，取第一条成功匹配
macro_rules! my_vec {
    () => { Vec::<i32>::new() };
    ($($x:expr),+ $(,)?) => {{          // $()* 重复，$(,)? 允许尾逗号
        let mut v = Vec::new();
        $( v.push($x); )+               // 转写器用同样的重复结构展开
        v
    }};
}

// tt muncher：每次吃掉一个 ident，靠递归把列表走完
macro_rules! count_idents {
    () => { 0usize };
    ($head:ident $($tail:ident)*) => { 1usize + count_idents!($($tail)*) };
}

// 卫生性：宏内 let x 不会影响调用点的 x
macro_rules! hygienic {
    () => {{ let x = 100; x }};
}

// 导出与 $crate：跨 crate 使用时用 $crate 指回定义方
#[macro_export]
macro_rules! make_fn {
    ($name:ident) => { pub fn $name() -> u32 { 42 } };
}
make_fn!(answer);

fn main() {
    println!("{:?}", my_vec![1, 2, 3]);        // [1, 2, 3]
    println!("{:?}", my_vec![]);               // []
    println!("{:?}", my_vec![1, 2, 3,]);       // [1, 2, 3]
    println!("{}", count_idents!(a b c d));    // 4
    let x = 7;
    println!("{} {}", hygienic!(), x);         // 100 7
    println!("{}", answer());                  // 42
}
```

完整的片段分类符一共有 15 个：`block`、`expr`、`expr_2021`、`ident`、`item`、`lifetime`、`literal`、`meta`、`pat`、`pat_param`、`path`、`stmt`、`tt`、`ty`、`vis`；`expr_2021` 是为了在 2024 edition 保留 `expr` 的旧行为而存在的（2024 起 `expr` 也能匹配 `_` 与 `const {}`）。重复运算符只有三个：`*` 表示零次或多次，`+` 表示至少一次，`?` 表示零次或一次且不允许带分隔符，分隔符可以是除括号与重复运算符以外的任意记号，`;` 与 `,` 最常见。卫生性是混合位置的：局部变量与循环标签按**定义点**解析，其余符号（函数、类型、常量、宏）按**调用点**解析，所以 `hygienic!()` 里的 `x` 永远是自己的 100，而宏体内调用的函数则可能来自调用点。跨 crate 导出时用 `#[macro_export]` 把宏提到 crate 根，并在宏体内用 `$crate::helper!()` 指回定义方；2018 edition 之后推荐路径式导入（`use mycrate::mymacro;`），`#[macro_use] extern crate` 只在老代码里还见得到。调试手段是 `cargo expand` 看展开结果、`cargo rustc -- -Zunpretty=expanded` 与 nightly 的 `trace_macros!`；转发片段给另一个宏时要注意不透明性：`$x:expr` 传下去后对方只能用 `expr` 类片段接住，只有 `ident`、`lifetime`、`tt` 能被字面记号继续匹配。

📘 [Rust · 声明式宏](https://doc.rust-lang.org/reference/macros-by-example.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 没有语法宏入口，也不允许用户定义类似 `macro_rules!` 的声明式宏：宏只能由 `#externalMacro` 指向一个用 swift-syntax 编写的编译器插件，属于下一节的外部宏。语言内部提供的两个"声明式变换"机制是结果构建器（`@resultBuilder`）与属性包装器（`@propertyWrapper`），它们由编译器识别、形态固定，不是通用的宏。

```swift
// @resultBuilder：把语句序列声明式地拼装成一个值（SwiftUI 的 DSL 基础）
@resultBuilder
struct StringBuilder {
    static func buildBlock(_ parts: String...) -> String { parts.joined(separator: " ") }
    static func buildOptional(_ part: String?) -> String { part ?? "" }
}

struct Doc {
    @StringBuilder var body: String {
        "hello"
        if Bool.random() { "maybe" }
        "world"
    }
}

let d = Doc()
print(d.body.split(separator: " ").count >= 2)   // true

// 没有通用的宏定义；宏声明要写成下面这样并指向外部实现
// @freestanding(expression)
// macro stringify<T>(_ value: T) -> (T, String) = #externalMacro(module: "MyMacros", type: "StringifyMacro")
```

`@resultBuilder` 与宏的差别在于它是**语法受限**的：只能有一组固定的 `build*` 静态方法，只能作用于特定位置（属性、参数、函数体），编译器按固定规则把语句收集成调用，用户无法自定义转换的形状。`@attached` 与 `@freestanding` 宏才提供任意变换能力，但必须写实现、必须单独编译成插件，见第三个子主题。理解这个分层很重要：Swift 把"常见形态的语法糖"做成语言内建（结果构建器、属性包装器、`@Observable` 这类宏），把"任意变换"留给外部宏。

📘 [Swift · 特性与结果构建器](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/attributes/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 明确没有宏，而且是设计上的拒绝：语言规范里没有宏、没有泛型宏、也没有元编程语法。官方的替代路线是代码生成——`go generate` 跑生成器，`stringer`、`mockgen`、`protoc-gen-go` 这类工具把源码或接口描述翻译成 Go 文件。`go generate` 本身只执行注释里的命令，不做任何语法分析，因此生成器的输入是何物完全取决于工具。

```go
package main

import "fmt"

//go:generate sh -c "printf 'package main\n\nconst generated = \"from go generate\"\n' > gen.go"

func main() {
	fmt.Println(generated)       // from go generate
	fmt.Println(len(generated))  // 16
}
```

`//go:generate` 必须从行首开始、`//` 与 `go` 之间不能有空格，但它可以出现在文件里的**任何位置**（`go generate` 不解析源码，所以注释里、甚至多行字符串里长得像指令的行也会被当成指令）；命令在**包源码目录**执行，`$GOFILE`、`$GOLINE`、`$GOPACKAGE`、`$GOROOT`、`$GOOS`、`$GOARCH`、`$DOLLAR`、`$PATH` 等变量会被替换后传给命令。生成的文件通常加一行 `// Code generated by <tool> DO NOT EDIT.`，`go vet` 与代码审查工具都认这个约定。工具链缓存不跟踪 `go generate`，所以生成结果必须提交或由 CI 显式执行。反射（`reflect`）是运行期能力，只能读结构信息、不能生成代码，所以 Go 里想"少写样板"最终都要落到生成器上。

📘 [Go · go generate](https://go.dev/blog/generate)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有宏：解释器没有宏展开阶段，也不存在用户定义的语法扩展入口（除了已废弃的 `__future__` 编译器指令）。最接近"声明式宏"的三样东西是装饰器、`ast` 模块与元类，但它们全部在**运行时**工作：装饰器拿到的已经是函数对象与类型对象，`ast` 需要你自己先读到源码文本，元类在类对象创建时才介入。

```python
import ast
import inspect
from functools import wraps

# 装饰器：高阶函数，运行时包装对象（等价于 f = deco(f)）
def traced(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        return fn(*a, **kw)
    return wrapper

@traced
def add(a, b):
    return a + b

# ast：只能解析与改写“文本”，要自己接住源码
tree = ast.parse("x = 1 + 2", mode="exec")
tree.body[0].value = ast.BinOp(left=ast.Constant(6), op=ast.Mult(), right=ast.Constant(7))
ns = {}
ast.fix_missing_locations(tree)     # 手工构造的节点缺少 lineno，必须补上
exec(compile(tree, "<ast>", "exec"), ns)

print(add(1, 2))                    # 3
print(add.__name__)                 # add，靠 wraps 保住
print(ns["x"])                      # 42
print(isinstance(tree.body[0], ast.Assign))   # True
```

装饰器的语法糖等价于把函数名重新绑定成装饰器的返回值，所以它改变的是**名字指向什么**，不是函数体里的语法；这也是为什么 `functools.wraps` 很重要——不写它，`add.__name__` 会变成 `wrapper`，文档与调试信息全丢。`ast` 能做的才是真正的语法层变换，但它需要源码文本作为输入，而且 `exec`/`compile` 生成的代码无法被静态分析工具看到，这是 Python 生态里"代码生成"总要额外配一个 `.pyi` 或显式导出的原因。元类与 `__init_subclass__` 能在类创建时改写类字典，属于运行时的类级变换，与宏的编译期性质量正好相反。

📘 [Python · ast 模块](https://docs.python.org/3/library/ast.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 没有语法宏，也没有 `macro_rules!` 那类声明式宏：`inline` 函数加上 `reified` 类型参数只能做有限的内联展开，不能匹配任意语法结构。要扩展语法就得写编译器插件（IR 层变换），要做声明级代码生成就得用 KSP。最该先分清的是两者的能力边界：编译器插件能看到函数体并修改 IR，KSP 只看得到声明与类型、只能生成新文件。

```kotlin
// inline + reified：Kotlin 唯一“接近宏”的语言内手段
inline fun <reified T> typeNameOf(): String = T::class.simpleName ?: "?"

// 编译器插件负责 IR 变换（如 kotlinx.serialization、Compose 编译器插件）
// KSP 负责声明级代码生成，接口长这样：
// interface SymbolProcessor { fun process(resolver: Resolver): List<KSAnnotated> }

fun main() {
    println(typeNameOf<Int>())        // Int
    println(typeNameOf<String>())     // String
}
```

`inline` 函数在调用点展开函数体，`reified` 让类型参数在展开后仍可当具体类型使用（可以写 `T::class` 或 `is T`），这两点合起来能做一部分宏能做的事，比如带类型的日志、序列化入口、DSL 构建器。但 `inline` 不是宏：它不能匹配语法结构、不能在编译期生成任意声明、也不能读取调用点的语法树。KSP 的地位相当于 Kotlin 版的注解处理器，但它明确"不提供表达式与函数体访问，也不能修改源文件"，只能读出符号信息再写新文件；kapt 是让 Kotlin 复用 Java 注解处理器的旧方案，官方文档已经给出「从 kapt 迁移到 KSP」的专门指引，新项目应当直接选 KSP。

📘 [Kotlin · KSP 总览](https://kotlinlang.org/docs/ksp-overview.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 没有宏，也没有语法扩展机制：语言规范不支持用户定义语法，`javac` 也没有公开的"编译期变换"入口。唯一被官方支持的编译期扩展点是 JSR 269 注解处理器，它能读取被注解的声明并在编译过程中生成**新的源文件**，但不能修改已有的类。想在字节码层面改写（比如 Lombok 那样往类里塞方法）必须依赖非标准 API，代价是对编译器版本极其敏感。

```java
// 注解声明：运行时可用反射读，编译期可被处理器读
import java.lang.annotation.*;

@Retention(RetentionPolicy.CLASS)      // 只保留到 class 文件，处理器能看、反射看不到
@Target(ElementType.TYPE)
public @interface Builder {}

// JSR 269 处理器的骨架（需要 java.compiler 模块，编译期运行）
// @SupportedAnnotationTypes("Builder")
// public class BuilderProcessor extends AbstractProcessor {
//     @Override public boolean process(Set<? extends TypeElement> ann, RoundEnvironment env) {
//         for (Element e : env.getElementsAnnotatedWith(Builder.class)) {
//             String name = e.getSimpleName() + "Builder";
//             try (Writer w = processingEnv.getFiler().createSourceFile(name).openWriter()) {
//                 w.write("public class " + name + " {}");   // 只能生成新文件
//             } catch (java.io.IOException ex) { throw new RuntimeException(ex); }
//         }
//         return true;
//     }
// }

public class Main {
    public static void main(String[] args) {
        System.out.println(Builder.class.isAnnotationPresent(Builder.class));  // false
        System.out.println(Builder.class.getAnnotations().length);             // 0
    }
}
```

处理器的运行模型是**分轮（round）**的：第一轮处理源码里标注的声明并生成新文件，新文件进入下一轮继续被处理，直到没有新文件为止；`RoundEnvironment.processingOver()` 用于区分最后一轮，`Filer` 负责创建源文件或资源，且同一个文件只能创建一次。`RetentionPolicy.CLASS` 与 `RUNTIME` 的取舍决定了注解是"只给处理器看"还是"运行期也要读"：前者不占运行期开销，后者需要反射。Lombok 走的是修改 AST 的非标准路线，因此每次 JDK 升级都可能失效；MapStruct 与 AutoValue 走标准处理器路线，生成的是普通的实现类或子类，稳定得多。Java 25 的构造函数体更灵活（JEP 513）这类语言变化同样会影响处理器的假设，所以处理器项目要显式声明支持的最低 `--release`。

📘 [Java · 注解处理 API](https://docs.oracle.com/en/java/javase/25/docs/api/java.compiler/javax/annotation/processing/Processor.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 没有 AST 层面的声明式宏：预处理器只有文本替换，模板是唯一的"结构化代码生成"机制。模板属于编译期，它的能力来自实例化与 `constexpr` 求值，而不是语法模式匹配——你无法写一条规则去匹配"任意语句序列"，只能靠偏特化、可变参数模板与 `if constexpr` 模拟。C++23 的基线里没有任何形式的反射，C++26 才把静态反射纳入标准。

```cpp
#include <cstdio>
#include <string_view>
#include <type_traits>

// 可变参数模板 + 折叠表达式：做“接受任意个参数”的宏做不到的类型安全工作
template <typename... Ts>
constexpr auto sum(Ts... xs) { return (xs + ... + 0); }

// 偏特化模拟“按结构分派”
template <typename T> struct Kind { static constexpr std::string_view value = "other"; };
template <typename T> struct Kind<T*> { static constexpr std::string_view value = "pointer"; };
template <typename T> struct Kind<T&> { static constexpr std::string_view value = "reference"; };

// if constexpr：编译期分支，未选中的分支仍然要语法正确
template <typename T>
constexpr std::string_view describe() {
    if constexpr (std::is_integral_v<T>) return "integral";
    else if constexpr (std::is_floating_point_v<T>) return "floating";
    else return "other";
}

int main() {
    std::printf("%d\n", sum(1, 2, 3));                              // 6
    std::printf("%.*s\n", (int)Kind<int*>::value.size(), Kind<int*>::value.data());   // pointer
    std::printf("%.*s\n", (int)Kind<int>::value.size(), Kind<int>::value.data());     // other
    std::printf("%.*s\n", (int)describe<double>().size(), describe<double>().data()); // floating
    return 0;
}
```

模板与宏的关键差别是模板参与类型系统：`sum(1, 2, 3)` 会做真正的重载解析与类型检查，重载失败给出的是带类型信息的诊断，而宏出错时给出的通常是一串被替换后的文本。代价是实例化爆炸与极长的报错信息，以及几乎所有编译期程序都要靠 `static_assert` 把错误"提前引爆"。C++26 的静态反射（P2996 等，配 `<meta>` 头文件与 `^^` 反射运算符）会让"遍历类的成员并生成代码"第一次成为标准能力，但按 C++23 基线它不可用，各编译器支持也不完整，跨平台项目仍需等待或使用第三方反射库。C++26 同时引入的展开语句（`template for`）常与反射一起使用，同样不在 C++23 里。

📘 [cppreference · C++26 编译器支持](https://en.cppreference.com/w/cpp/compiler_support/26)

{{% /tab %}}

{{% tab header="C" %}}

C 在语法层没有任何宏机制：预处理器只做记号替换，不认识语法结构，语言本身也没有模板或编译期函数。C 里最接近"声明式宏"的就是 `#define` 加 `##` 与 `#` 的组合，它能拼出看起来像新语法的东西（例如 `DEFINE_VECTOR(int, IntVec)` 生成整套类型与函数），但代价是所有错误都退化成替换后的文本错误。C11 的 `_Generic` 提供了编译期按类型分派，C23 的 `constexpr` 提供了编译期常量对象。

```c
#include <stdio.h>

/* 用宏“声明”一套类型与函数：C 里最接近语法宏的写法 */
#define DEFINE_PAIR(T, Name)                       \
    typedef struct { T a; T b; } Name;             \
    static inline Name Name##_make(T a, T b) {     \
        Name p = { a, b };                         \
        return p;                                  \
    }

DEFINE_PAIR(int, IntPair)
DEFINE_PAIR(double, DoublePair)

#define PAIR_EQ(lhs, rhs) _Generic((lhs),                    \
    IntPair: ((lhs).a == (rhs).a && (lhs).b == (rhs).b),      \
    DoublePair: ((lhs).a == (rhs).a && (lhs).b == (rhs).b),   \
    default: 0)

int main(void) {
    IntPair p = IntPair_make(1, 2);
    DoublePair q = DoublePair_make(1.5, 2.5);
    printf("%d %d\n", p.a, p.b);            /* 1 2 */
    printf("%.1f %.1f\n", q.a, q.b);        /* 1.5 2.5 */
    printf("%d\n", PAIR_EQ(p, ((IntPair){1, 2})));   /* 1：复合字面量要再套一层括号 */
    return 0;
}
```

`DEFINE_PAIR` 里那个反斜杠续行是 C 宏唯一的"多行"手段：续行符必须是该行最后一个字符，后面连空格都不能有，否则会得到一个隐蔽的编译错误。`##` 把 `Name` 与 `_make` 拼成一个新标识符，这是生成一族函数名的唯一办法，但它绕过了所有名字检查，拼错要到使用处才暴露。`_Generic` 只能按表达式的类型选**表达式**，不能选类型或语句，所以它能替代一部分函数宏重载，替代不了模板。C 没有卫生性概念：宏体内出现的任何名字都会与调用点可见的名字发生捕获，所以惯用法是给宏内局部变量起 `_tmp` 这种不易撞车的名字，或者干脆写成 `static inline` 函数。

📘 [cppreference · _Generic](https://en.cppreference.com/w/c/language/generic)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的宏是**语法层面**的：它在解析期被展开，宏体拿到的是 `Expr` 对象，返回的也是 `Expr`，可以完全访问调用点写下的语法结构。宏默认是卫生的——Julia 会把宏返回表达式里的局部变量用 `gensym` 重命名，并把全局名字解析到宏**定义所在模块**，只有被 `esc` 包住的表达式才回到调用者作用域。最该先掌握的工具是 `@macroexpand`。

```julia
macro timeit(ex)
    return quote
        local t0 = time_ns()          # local：会被 gensym 重命名，不污染调用者
        local v = $(esc(ex))          # esc：在调用者作用域里求值
        println("elapsed ns: ", time_ns() - t0)
        v
    end
end

macro zerox()
    return esc(:(x = 0))              # 故意打破卫生：直接改调用者的 x
end

ex = @macroexpand @timeit(1 + 1)      # 看展开结果，不执行
println(ex.head)                      # block

x = 42
@zerox()
println(x)                            # 0

println(@timeit(6 * 7))               # 先打印 elapsed ns: <n>，再打印 42
println(Symbol("t0") in names(Main))  # false：宏内的 t0 没有泄漏到 Main
```

Julia 的卫生规则可以概括成三句：宏返回表达式里被赋值、被声明为 `local`、或作为参数名的变量算局部变量，会被 `gensym` 重命名成唯一符号；其余名字算全局名，在宏定义所在模块解析（所以宏里写 `println` 永远指向定义模块的 `println`）；`esc(x)` 让 `x` 保持字面形态并按调用者作用域解析，这是"故意破坏卫生"的正规出口。`@macroexpand` 打印宏展开结果，`@macroexpand1` 只展开一层，两者是调试宏时最先用的命令。宏还可以像函数一样多重分派，但分派依据是**传入 AST 的类型**而不是求值结果，这点常让人意外。宏内能做的事很广，但文档明确建议：能用高阶函数与闭包解决就不要写宏，`eval` 与定义新宏都应当作最后手段。

📘 [Julia · 宏](https://docs.julialang.org/en/v1/manual/metaprogramming/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 没有宏：`#define` 只能定义供 `#if` 判断的符号，不能带参数、不能带宏体，也没有用户可定义的语法扩展。声明式代码生成的正规路线是 Roslyn 的源生成器，它读的是语法树与语义模型，产出的是新的 C# 源码。最该先分清的是源生成器与 T4 模板的差别：前者随编译运行、能看到语义信息、是推荐做法；后者是独立的文本模板引擎，只能看到你交给它的输入。

```csharp
// C# 侧只能写“被生成”的用法，生成器本身是一个独立的 analyzer 项目
using System;

public partial class Person
{
    public string Name { get; set; } = "";
    // 源生成器会为这个 partial 类补上 ToString 或 Builder
}

public static class Program
{
    public static void Main()
    {
#if NET10_0_OR_GREATER
        Console.WriteLine("net10.0");      // net10.0
#else
        Console.WriteLine("older");
#endif
        var p = new Person { Name = "Ada" };
        Console.WriteLine(p.Name);          // Ada
        Console.WriteLine(p.GetType().IsSealed);   // False
    }
}
```

源生成器在编译过程中运行，通过 `ISourceGenerator`（v1）或 `IIncrementalGenerator`（自 .NET 6 与 Roslyn 4.0 起，是当前推荐写法）实现，只能在 `Initialize` 里注册语法/语义提供程序，再在回调中用 `SourceProductionContext.AddSource` 追加源码，**不能修改已有代码**。生成的文件可以带上 `[GeneratedCode]` 标记，并配合 `partial` 让生成部分与手写部分合并成一个类型；与 analyzer 的分工是：生成器补代码，analyzer 报诊断，两者常打包在同一个 analyzer 项目里。T4（`.tt` 文件）是文本模板，在构建前或设计时由 Visual Studio 的模板引擎生成文本文件，适合生成固定形状的样板而无法读取编译期语义，所以现代项目优先选源生成器；在 .NET 10 上 `IIncrementalGenerator` 仍是当前推荐写法，公开 API 形态没有变化。

📘 [MS Learn · 源生成器总览](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有宏：官方曾在语言层面推进过"macros"实验并已放弃，当前的方案是 `build_runner` 加 `source_gen` 的代码生成。生成器是一个普通的 Dart 程序，读你在源码里写的注解，产出 `.g.dart` 或 `.freezed.dart` 文件；生成结果进入编辑期，但整个流程发生在构建之前而不是编译之中。最该先知道的是它需要显式的生成步骤，而且生成器只能追加文件。

```dart
// 注解在源码里，生成器读它并写出新文件
import 'package:meta/meta_meta.dart';

@Target({TargetKind.classType})
class JsonModel {
  const JsonModel();
}

@JsonModel()
class User {
  const User({required this.id, required this.name});
  final int id;
  final String name;
}

void main() {
  // 生成出来的通常是 User.fromJson / toJson / copyWith
  // 由 `dart run build_runner build` 产出 user.g.dart
  const u = User(id: 1, name: "Ada");
  print(u.id);          // 1
  print(u.name);        // Ada
  print(u is Object);   // true
}
```

`build_runner` 的工作模型是"输入 → 生成器 → 输出"：它扫描 `lib/` 下的文件、按 `build.yaml` 配置运行生成器、把结果写到 `*.g.dart`，用 `dart run build_runner watch` 做增量。它的约束有三条值得记牢：生成器只能看到自己声明的输入与注解，看不到整个程序的类型信息；生成结果必须提交进仓库或由 CI 重新生成（团队通常约定隐藏 `.g.dart` 以保持源码干净）；生成是**全量扫描**式的，项目变大后构建时间会显著上升，所以 `source_gen` 生态才强调把工作拆小。注解本身用 `package:meta` 的 `@Target` 之类的元注解约束作用位置，这与 Java 注解处理器的建模方式一致。

📘 [Dart · build_runner](https://dart.dev/tools/build_runner)

{{% /tab %}}

{{% tab header="R" %}}

R 有元编程，但没有宏：`quote` 阻止求值并得到语言对象（`call`、`symbol`、`name`），`substitute` 在函数内把实参的表达式原样取出来，`bquote` 支持用 `.()` 做部分求值，`eval` 再把语言对象放回求值。这套机制能改写表达式，但它发生在**运行时**、没有独立的展开阶段、也完全没有卫生性——默认所有的名字都在调用环境里解析。

```r
f <- function(x) substitute(x)          # 取实参的表达式，不求值
g <- function(x) bquote(.(x) * 2)       # 部分求值：x 先算出值再嵌进表达式

expr <- f(a + b)
print(expr)                             # a + b
print(typeof(expr))                     # language

built <- g(3)
print(built)                            # 3 * 2
print(eval(built))                      # 6

# 非卫生：substitute 出来的表达式在调用环境求值
h <- function(e) eval(substitute(e))
a <- 10; b <- 20
print(h(a + b))                         # 30
```

`substitute(x)` 与 `quote(x)` 的区别在于作用域：`substitute` 会沿着调用链做替换，`quote` 只是原样包住写下的表达式。`bquote` 里 `.()` 里的内容会被立即求值并嵌入结果，其他部分保持不动，这是构造表达式的常用手法。所谓"R 的宏不卫生"具体表现是：`substitute` 拿到的表达式携带的是**调用者的环境**，如果你把它拿到别处 `eval` 就会找不到变量，必须显式传 `envir` 参数或用 `eval(expr, envir = parent.frame())`；反过来，因为名字都在调用环境解析，宏式的函数无法保证内部临时变量不与用户变量冲突。S3 泛型（`UseMethod`）本身就是靠 `substitute` 捕获实参表达式来实现的，这也解释了为什么 `UseMethod` 的分派基于第一个实参的**类型**而不是表达式的形式。要用这套机制做批量代码生成，惯用写法是 `eval(bquote(...))` 配合 `lapply`。

📘 [R · substitute](https://stat.ethz.ch/R-manual/R-devel/library/base/html/substitute.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有宏：没有文本替换，也没有语法扩展入口。它的答案是把"编译期"做成语言的一等公民——`comptime` 参数、`comptime` 块、`inline for` 与 `inline while` 让代码在编译期被求值与展开，`@typeInfo` 把类型变成可遍历的数据，`@Type` 再把它变回类型。因此 Zig 的"宏"写起来就是普通的 Zig 函数，只是参数带 `comptime`。

```zig
const std = @import("std");

// comptime 函数参数 + 返回类型 type：这就是 Zig 的“泛型”，也是“宏”
fn Vec(comptime T: type, comptime n: usize) type {
    return struct {
        items: [n]T,
        fn sum(self: @This()) T {
            var total: T = 0;
            inline for (self.items) |v| {    // inline for：编译期展开循环
                total += v;
            }
            return total;
        }
    };
}

pub fn main() void {
    const V3 = Vec(i32, 3);
    const v = V3{ .items = .{ 1, 2, 3 } };
    std.debug.print("{d}\n", .{v.sum()});          // 6

    // @typeInfo：类型信息是编译期数据，可以遍历
    const info = @typeInfo(V3);
    std.debug.print("{s}\n", .{@tagName(info)});   // struct（标签在源码里写作 .@"struct"）
    std.debug.print("{d}\n", .{info.@"struct".fields.len});   // 1

    inline for (.{ u8, u16, u32 }) |T| {           // 编译期对类型集合展开
        std.debug.print("{s} ", .{@typeName(T)});  // u8 u16 u32
    }
}
```

`comptime` 参数在每次实例化时被当成常量，函数返回类型写在 `type` 上，于是 `Vec(i32, 3)` 就是"用编译期参数生成一个新类型"，与泛型宏的用途一致但完全在类型系统内。`inline for` 与普通 `for` 的差别是它必须能在编译期确定迭代次数，展开后没有循环体开销，也能对元组与类型数组做遍历——`@typeInfo` 返回的 `std.builtin.Type` 是一个带标签的联合，用 `info.@"struct".fields` 之类的方式取字段表，配合 `inline for` 就能为每个字段生成代码。三条限制要记住：编译期代码不能有副作用（不能做 IO、不能读可变全局），不能调用尚未定义的函数，循环展开规模受 `@setEvalBranchQuota` 限制，默认配额是 1000 次向后分支，超了要显式提高（官方文档明确默认值为 `1000`）。`@compileLog` 打印编译期值，`@compileError` 直接终止编译，两者是这套机制唯一的调试与断言手段。

📘 [Zig · comptime](https://ziglang.org/documentation/master/)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有宏，也没有语法扩展：语言没有提供 `macro` 关键字，标准库也不含预处理器。替代手段是 `load` 与 `loadstring` 做字符串求值、`debug` 库做函数与变量的内省、元表做行为改写。最该先知道的是这些手段全都在**运行时**，因此既没有展开期检查，也没有卫生性可言。

```lua
-- 运行期拼装函数：把一段字符串变成闭包
local function make_adder(n)
  return load("local n = ... ; return function(x) return x + n end")(n)
end
print(make_adder(10)(5))            -- 15

-- debug 库：读取函数信息、改写上值（内省能力，慎用）
local function f() return 1 end
print(debug.getinfo(f, "S").what)   -- "Lua"
local i = 1
while true do
  local name, val = debug.getupvalue(f, i)
  if not name then break end
  print(name, val)                  -- 打印 f 的上值
  i = i + 1
end

-- 元表：拦截索引与调用，做“注解式”行为
local t = setmetatable({}, { __index = function(_, k) return "gen:" .. k end })
print(t.anything)                   -- gen:anything
```

`load` 的返回约定是"成功给函数、失败给 `nil` 加错误消息"，所以上面那个直接 `load(...)(n)` 的写法在生产代码里必须改成两步并检查错误。`debug.getupvalue` 能读到闭包捕获的变量，`debug.setupvalue` 能改写它，这是 Lua 里唯一能"改变已有函数行为"的手段，但它依赖调试信息、在去掉了调试信息的构建里不可用，性能也很差。元表适合做缺省值与委托，不适合做语法变换。真正的"编译期生成"只能落在构建脚本一侧（生成 `.lua` 文件），Lua 本身不参与。

📘 [Lua 5.5 · 调试接口](https://www.lua.org/manual/5.5/manual.html#6.11)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有宏：`#` 在 TS 里只是私有字段前缀。它的"声明式变换"分两层——类型层面的条件类型与映射类型在编译期求值但不产生运行时代码，值层面的变换要靠 Babel / SWC 插件或 TypeScript 编译器 API 写的 transformer。5.0 起装饰器成为标准提案实现，但装饰器是**运行时函数**，不是宏。

```typescript
// 映射类型：类型层面的“代码生成”，运行时不产生任何代码
type ReadonlyDeep<T> = { readonly [K in keyof T]: ReadonlyDeep<T[K]> };
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

interface User { id: number; name: string; }
type FrozenUser = ReadonlyDeep<User>;
type DraftUser = PartialBy<User, "name">;

const u: FrozenUser = { id: 1, name: "Ada" };
const d: DraftUser = { id: 2 };            // name 可省略
// u.id = 9;                               // 编译错误：readonly

// 编译器 API 的 transformer 才是真正改 AST 的入口（示意）
// factory.updateSourceFile(sourceFile, visitEachChild(sourceFile, visitor, context))

console.log(u.name, d.id);                 // Ada 2
console.log(JSON.stringify(u));            // {"id":1,"name":"Ada"}
```

条件类型与映射类型是类型运算，编译后就消失了，它们能做的是"把类型算出来"，不是"把代码变出来"；需要生成真实代码时，`tsc` 自身不加载自定义 transformer，要么用 compiler API 自己驱动编译，要么用 `ts-patch` 给 `tsc` 打补丁让它加载 transformer。装饰器这一侧要区分两代：legacy 装饰器（`experimentalDecorators`）参数是 `(target, key, descriptor)`，5.0 标准装饰器参数是 `(value, context)`，两者不能混用，运行时语义也因此不同。需要"像宏一样"做语法糖时，社区方案基本都走 Babel 插件的 AST 变换，而不是 TS 本身。

📘 [TypeScript · 装饰器](https://www.typescriptlang.org/docs/handbook/decorators.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有宏，也没有编译期：整门语言只有运行时，所谓"构建期变换"全部由外部工具完成。Babel 与 SWC 插件是事实标准——它们把源码解析成 AST、遍历并替换节点、再生成新的源码与 source map。最该先知道的是这条路线的代价：多一层工具链、多一份 AST 依赖、调试时看到的行号是映射回来的。

```javascript
// 一个最小的 Babel 插件形态（示意，需要 @babel/core 才能运行）
const plugin = ({ types: t }) => ({
  visitor: {
    CallExpression(path) {
      // 把 assert(cond, msg) 改写成 if (!cond) throw new Error(msg)
      if (path.node.callee.name !== "assert") return;
      const [cond, msg] = path.node.arguments;
      path.replaceWith(
        t.ifStatement(
          t.unaryExpression("!", cond),
          t.throwStatement(t.newExpression(t.identifier("Error"), [msg]))
        )
      );
    },
  },
});

// 不用工具链也能做的：运行期行为改写
const assert = (cond, msg) => { if (!cond) throw new Error(msg); };
assert(1 + 1 === 2, "math works");
console.log("assert passed");        // assert passed

try {
  assert(false, "boom");
} catch (e) {
  console.log(e.message);            // boom
}

// 高阶函数是绝大多数“宏需求”的正解
const times = (n, f) => Array.from({ length: n }, (_, i) => f(i));
console.log(times(3, (i) => i * i)); // [0, 1, 4]
```

Babel 插件的 `visitor` 按节点类型注册，`path` 对象提供 `replaceWith`、`insertBefore`、`skip` 等操作，`t`（`@babel/types`）提供节点构造器；SWC 插件用 Rust 或 WASM 写，API 更贴近性能敏感的构建流水线，两者思路一致但插件不能互换。选型上，Babel 生态最全、插件最好写；SWC 与 esbuild 快得多但插件能力有限。要提醒的坑是：任何 AST 变换都必须同时生成正确的 source map，否则线上报错的行号全部错位；此外改写了语法意味着类型检查器与运行时看到的代码不再一致，所以这类插件通常只用于已冻结的语法糖（如旧版装饰器、可选链降级）。

📘 [Babel · 插件手册](https://babeljs.io/docs/plugins)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有宏：`#` 是注释符，语言里没有 `macro` 关键字，也没有可扩展语法的入口。8.0 引入的 attributes 提供了注解语法，8.4 引入的属性钩子（property hooks）提供了属性级的语法糖，两者都是语言内建而非用户可扩展。代码生成交给 composer 脚本或独立的构建步骤。

```php
<?php
#[\Attribute(\Attribute::TARGET_METHOD)]
class Route {
    public function __construct(public string $path, public string $method = 'GET') {}
}

class Controller {
    #[Route('/users', 'GET')]           // 8.0 的属性：靠反射在运行时读
    public function users(): array { return ['a', 'b']; }

    // 8.4 的属性钩子：属性访问自带逻辑，是语言内建而不是宏
    public string $name = 'ada' {
        get => ucfirst($this->name);
    }
}

$rc = new ReflectionClass(Controller::class);
$rm = $rc->getMethod('users');
$route = $rm->getAttributes(Route::class)[0]->newInstance();
echo $route->path, ' ', $route->method, "\n";     // /users GET
echo (new ReflectionMethod(Controller::class, 'users'))->invoke(new Controller())[0], "\n";  // a

$c = new Controller();
echo $c->name, "\n";                              // Ada
```

attributes 本身不产生任何代码，它只是把结构化元数据挂在声明上，读取必须显式用 `ReflectionClass`、`ReflectionMethod`、`ReflectionProperty` 或 `ReflectionParameter` 去查，`newInstance()` 才会真正构造注解类实例——所以框架普遍会把结果缓存进 opcache 或自己的缓存文件。属性钩子在 8.4 起可用，写法是在属性声明后加大括号并给出 `get` 与 `set`，它替代了过去的 `__get`/`__set`，好处是类型信息完整、IDE 能识别，坏处是它和 `__get` 同时存在时的优先级规则要小心。真要"生成代码"，php 侧的常规做法是 composer 的 `post-autoload-dump` 脚本、`php artisan` 风格的自定义命令，或在 CI 里先跑一遍生成器。

📘 [PHP · 属性](https://www.php.net/manual/en/language.attributes.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有宏：语言不支持用户定义语法，也没有展开阶段。它的替代品是元编程——`define_method` 在类级别动态定义方法，`method_missing` 拦截未定义的方法调用，`class_eval` 与 `instance_variable_set` 直接打开对象改结构，`eval` 与 `instance_eval` 执行字符串或块。这些全都在运行时发生，因此没有卫生性，也没有编译期检查。

```ruby
# frozen_string_literal: true

class Model
  # 用循环批量定义读写方法：替代“批量宏”
  %i[id name email].each do |field|
    define_method(field) { instance_variable_get(:"@#{field}") }
    define_method(:"#{field}=") { |v| instance_variable_set(:"@#{field}", v) }
  end

  # method_missing：拦截不存在的查询方法
  def method_missing(name, *args)
    return !public_send(:"#{name.to_s.delete_suffix('?')}").nil? if name.to_s.end_with?("?")
    super
  end

  def respond_to_missing?(name, include_private = false)
    name.to_s.end_with?("?") || super
  end
end

m = Model.new
m.name = "Ada"
puts m.name            # Ada
puts m.name?           # true
puts m.id?             # false

# class_eval 打开类，eval 用字符串定义方法
Model.class_eval { def kind = "model" }
puts m.kind            # model
Model.class_eval("def self.answer = 42")   # 顶层 eval 只会定义到 main 上
puts Model.answer      # 42
```

`define_method` 接受块作为方法体，块是闭包，因此能捕获定义时的局部变量；而 `def` 关键字里的方法体不捕获外部作用域，这两个作用域规则的差别是 Ruby 元编程最容易踩的坑之一。用字符串 `eval` 时一定要想清楚"代码在谁的作用域里执行"：在顶层写 `eval("def self.answer = 42")` 只会把方法定义到 `main` 这个对象上，必须写成 `Model.class_eval("def self.answer = 42")` 才会落到目标类。`method_missing` 必须配一个 `respond_to_missing?`，否则 `respond_to?`、`method`、鸭子类型检查都会给出错误答案，进而引发很难查的行为差异。`module_function`、`extend`、`prepend` 分别用于把模块方法变成单例方法、扩展单例类、在祖先链前方插入模块，`prepend` 是包装已有方法（类似"环绕通知"）的推荐做法，比 `alias_method` 链更清晰。这些能力很强，但全局重开核心类（monkey patch）会让程序行为依赖加载顺序，是 Ruby 项目里最需要自律的地方。

📘 [Ruby · Module](https://docs.ruby-lang.org/en/master/Module.html)

{{% /tab %}}

{{< /tabpane >}}

### 过程宏与编译期代码生成

这一节的共同点是"编译过程本身可以被一段普通程序介入"。差别在于介入的深度：Rust 的过程宏拿到的是 `TokenStream`，可以任意重写语法；Swift 的外部宏接住的是 SwiftSyntax 节点；C# 的源生成器与 Java 的注解处理器只能**追加**源码；Zig 的 `comptime` 是在语言语义内做编译期求值；C++ 的模板要走实例化而不是运行任意宿主代码。运行时代码生成（`eval`、`load`、`define_method`）与它们的差距不只是时机，还有代价：编译期做的工作进不了产物，运行期做的工作每次都要付钱。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的过程宏是"在编译期运行的 Rust 函数"，输入输出都是 `proc_macro::TokenStream`。一共有三种：`#[proc_macro_derive]` 的 derive 宏、`#[proc_macro_attribute]` 的属性宏、`#[proc_macro]` 的函数式宏。它们必须定义在 `proc-macro = true` 的 crate 里，这个 crate 只能导出过程宏，不能同时导出普通函数或类型，所以调用方与定义方必然是**两个 crate**。

```rust
// ---- hello_macro/src/lib.rs（proc-macro crate）----
use proc_macro::TokenStream;

#[proc_macro_derive(Describe)]                       // derive 宏
pub fn describe_derive(input: TokenStream) -> TokenStream {
    let ast = input.to_string();
    let name = ast.split_whitespace().nth(1).unwrap().to_string();
    format!("impl {name} {{ pub fn describe() -> &'static str {{ \"{name}\" }} }}")
        .parse()
        .unwrap()
}

#[proc_macro]                                        // 函数式宏
pub fn make_answer(_item: TokenStream) -> TokenStream {
    "fn answer() -> u32 { 42 }".parse().unwrap()
}

// ---- app/src/main.rs（普通 crate，通过 path 依赖 hello_macro）----
use hello_macro::{make_answer, Describe};

#[derive(Describe)]
struct Point { x: i32 }

make_answer!();                                      // 编译期吐出一个完整函数

fn main() {
    println!("{}", Point::describe());               // Point
    println!("{}", answer());                        // 42
}
```

三个种类的差别只在于"挂在什么语法上"：derive 宏挂在 `#[derive(...)]` 上、收到被标注类型的记号流，属性宏挂在任意 item 上、同时收到属性自身的参数与被标注项，函数式宏则像函数调用一样直接出现在表达式或 item 位置。官方推荐的实现方式是用 `syn` 把 `TokenStream` 解析成语法树、用 `quote` 把结果拼回 `TokenStream`，纯字符串拼接只适合最小的例子——上面那个 derive 宏就是靠 `split_whitespace` 取名字，真实项目里应该写 `syn::parse_macro_input!(input as DeriveInput)`。硬性限制有几条：proc-macro crate 不能与使用它的代码在同一个 crate；过程宏是**无卫生性（unhygienic）**的，官方文档的原话是它的输出相当于直接写在调用点，因此宏内新引入的名字会与调用点可见的名字冲突（输出里调用的其它宏仍会在后续轮次继续展开）；错误要用 `compile_error!` 或 `syn::Error::to_compile_error` 报出，直接 panic 会给出很难看的信息。编译期执行意味着构建时间是代价：宏跑在编译机上也跑在 CI 上，纯计算型的宏要控制复杂度。

📘 [Rust · 过程宏](https://doc.rust-lang.org/reference/procedural-macros.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 从 5.9 起有外部宏，分两大类：**freestanding**（独立宏，调用时写 `#name(...)`，作用于表达式或声明）与 **attached**（附着宏，写在 `@name` 位置，附着到声明上，可产出 peer、member、memberAttribute、accessor、extension、conformance、body 等成员）。宏声明用 `macro` 关键字加角色标注，实现用 `#externalMacro(module:type:)` 指向另一个 target 里的类型；实现代码基于 swift-syntax，必须单独编译成编译器插件。

```swift
// ---- 声明侧（普通库 target）----
@freestanding(expression)
public macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "MyMacros", type: "StringifyMacro")

@attached(member, names: named(init))
public macro AddInit() = #externalMacro(module: "MyMacros", type: "AddInitMacro")

// ---- 使用侧 ----
public struct Point {
    public let x: Int
    public let y: Int
}

// 真实用法：let (result, text) = #stringify(x + y)
// 展开后等价于 (x + y, "x + y")
let (v, s) = (3, "3")
print(v, s)          // 3 3
```

Attached 宏的七个角色分别是 `peer`（给同类加新声明）、`member`（给类型加成员）、`memberAttribute`（给成员加属性）、`accessor`（生成 get/set）、`extension`（给别的类型加扩展）、`conformance`（加协议遵循）与 `body`（替换或补充函数体，由 SE-0415 引入，Swift 6.0 起可用，不是 5.9）；freestanding 宏只有 `expression` 与 `declaration` 两种角色。实现侧要走 SwiftPM：宏实现 target 依赖 `swift-syntax`，用 `SwiftSyntaxMacros` 与 `SwiftCompilerPlugin` 暴露类型，可执行 target 用 `@main struct MyPlugin: CompilerPlugin` 注册。宏在编译期运行，不能访问调用点的类型语义（只能看到语法节点），所以"想基于类型信息做决定"要额外写一个 `MacroExpansionContext` 查询或改成编译器插件。调试展开始用 `swiftc -Xfrontend -Rmacro-expansions`，加载插件用 `-load-plugin-executable`；宏不能与调用它的代码放在同一个 target 里，因为实现必须是编译器插件二进制。

📘 [Swift · 宏](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/macros/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有编译期执行，也没有宏：`go generate` 是唯一官方承认的代码生成入口，它只是按注释里的命令跑一个外部程序。因此 Go 的"编译期代码生成"实际上是**构建前**的独立步骤，生成器的输入可以是 Go 源码、接口描述文件、模板或数据库结构，输出是普通的 `.go` 文件，与手写代码没有区别。

```go
package main

import "fmt"

//go:generate sh -c "printf 'package main\n\nconst generated = \"from go generate\"\n' > gen.go"
//go:generate stringer -type=Color        // 需要 golang.org/x/tools/cmd/stringer

type Color int

const (
	Red Color = iota
	Green
	Blue
)

func main() {
	fmt.Println(generated)       // from go generate
	fmt.Println(len(generated))  // 16
	fmt.Println(Red, Green, Blue) // 0 1 2（有了 stringer 会打印 Red Green Blue）
}
```

`stringer` 是这套模式最经典的例子：给一个整数类型和它的常量，生成一个 `String()` 方法，把枚举值变成可读名字；同类工具还有生成 mock 的 `mockgen`、生成 protocol buffer 代码的 `protoc-gen-go`、生成 `MarshalJSON` 的各种工具。所有生成物都带 `// Code generated by <tool> DO NOT EDIT.` 头部，`go vet` 会据此跳过它们，人也不应该手改。要记住三条工程约束：`go generate` 不自动运行、不参与构建缓存，所以必须在文档或 `Makefile` 里写清先跑哪条命令；生成器版本要固定（`tools.go` 里用 `//go:build tools` 钉住版本是标准做法）；生成代码提交进仓库还是 CI 现场生成需要团队统一，否则会出现"只有某些机器能编过"的问题。反射只能读、不能写代码，所以 Go 里不存在运行期生成函数的正规途径。

📘 [Go · stringer](https://pkg.go.dev/golang.org/x/tools/cmd/stringer)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有编译期，也没有宏：CPython 的执行模型是"源码 → 字节码 → 解释执行"，没有任何用户代码在编译阶段运行的钩子（`.pth`、导入钩子、`sitecustomize` 都在导入期而非编译期）。因此 Python 的"代码生成"要么是运行时的 `exec`/`eval`/元类/装饰器，要么是构建前的独立生成器脚本。最该分清的是这两者的代价：运行时生成每次启动都付钱，构建前生成只在流水线上付一次。

```python
import textwrap
from dataclasses import dataclass, fields, make_dataclass

# 运行时按需构造类：make_dataclass 是标准库里的“代码生成”
Point = make_dataclass("Point", [("x", int), ("y", int, 0)])
print(Point(1))                     # Point(x=1, y=0)
print([f.name for f in fields(Point)])   # ['x', 'y']

# 运行时代码生成：compile + exec，框架常用它做模板或 DSL
src = textwrap.dedent("""
    def make_validator(field, limit):
        def validate(value):
            return len(value) <= limit
        return validate
""")
ns: dict = {}
exec(compile(src, "<generated>", "exec"), ns)
validate = ns["make_validator"]("name", 3)
print(validate("abc"), validate("abcd"))   # True False

# 元类：在类对象创建时改写它
class Tagged(type):
    def __new__(mcs, name, bases, ns):
        ns.setdefault("tag", name.lower())
        return super().__new__(mcs, name, bases, ns)

class Widget(metaclass=Tagged): pass
print(Widget.tag)                   # widget
```

`make_dataclass` 是标准库里少见的"运行期生成类型"工具，它会动态构造 `__init__`、`__repr__`、`__eq__` 并通过 `exec` 生成代码字符串——这也是为什么 dataclass 的性能在创建类时有一次性开销。`exec(compile(src, filename, mode))` 是标准写法，`filename` 参数会出现在 traceback 里，务必传一个有意义的名字（`"<generated>"`），否则线上排错会非常痛苦。元类在类创建时运行，`__init_subclass__` 在子类定义时运行，两者都能改写类的形状，但都不涉及语法解析。想做真正的"编译期"代码生成（如 `datamodel-code-generator` 从 JSON Schema 生成 `pydantic` 模型、`protoc` 生成 gRPC stub），唯一路线是在构建或开发期跑一个生成器脚本，并把结果纳入版本控制。`importlib` 是运行期侧的另一种"生成"：`importlib.import_module`、`importlib.util.spec_from_file_location` 与自定义 `MetaPathFinder` 让你在导入阶段决定一个模块名对应什么代码，很多插件系统与热重载框架都建立在这上面，但它依然发生在运行时而非编译期。

📘 [Python · dataclasses](https://docs.python.org/3/library/dataclasses.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的编译期代码生成有两条路：KSP（Kotlin Symbol Processing，读声明与类型并生成新文件）与编译器插件（在 IR 层做真正的变换）。kapt 是第三条老路——把 Kotlin 声明先转成 Java stub 再喂给 Java 注解处理器，官方文档现在直接给出「从 kapt 迁移到 KSP」的指引，新项目应当直接选 KSP。最该记住的边界是：KSP **看不到表达式与函数体，也不能修改源文件**。

```kotlin
// KSP 处理器的入口只有两个接口：
// interface SymbolProcessorProvider { fun create(environment: SymbolProcessorEnvironment): SymbolProcessor }
// interface SymbolProcessor { fun process(resolver: Resolver): List<KSAnnotated>; fun finish(); fun onError() }

// 使用侧：注解标在声明上，处理器读它并生成新文件
@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.SOURCE)
annotation class GenerateDto

@GenerateDto
data class User(val id: Int, val name: String)

// 生成出来的通常是 UserDto.kt（由 build/generated/ksp 目录进入编译）
fun main() {
    val u = User(1, "Ada")
    println(u)                     // User(id=1, name=Ada)
    println(User::class.simpleName) // User
}
```

KSP 的工作模型分三步：处理器扫描源码与资源得到符号信息，处理器写出新文件，Kotlin 编译器把原源码与生成代码一起编译；多轮处理由 `SymbolProcessor` 返回"待处理的延迟符号"驱动（例如某符号本轮还解析不了就返回给下一轮）。处理器能拿到类、函数、属性、类型与注解，但拿不到函数体与表达式，这个限制正是 KSP 比编译器插件稳定得多的原因——它依赖的编译器内部结构少。编译器插件则能改 IR，能注册自定义诊断，能力上限高得多，但必须随每个 Kotlin 版本重新适配；典型例子是 `kotlinx.serialization` 与 Compose 编译器插件。工程上应当优先选 KSP 生成样板（DTO、依赖注入绑定、Room DAO 实现），只有确实要改变语义时才写编译器插件（`@Composable` 那种级别的变换）。KSP 的版本号跟随 Kotlin 版本发布，升级 Kotlin 时要同步升级 KSP 与各处理器的版本。

📘 [Kotlin · KSP 总览](https://kotlinlang.org/docs/ksp-overview.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的编译期代码生成走 JSR 269 注解处理：处理器在编译过程中分轮运行，用 `RoundEnvironment` 拿到被注解的元素，用 `Filer` 创建新源文件。它属于**编译期**机制，但能力被严格限制在"新增源码"上；想修改已有类就必须依赖编译器内部 API（Lombok 的路子），代价是脆弱。

```java
// 一个最小的处理器（需要 java.compiler 模块；这里演示接口形态与使用结果）
import java.io.Writer;
import java.util.Set;
import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.*;

// @SupportedAnnotationTypes("com.example.Builder")
// @SupportedSourceVersion(SourceVersion.RELEASE_26)
// public class BuilderProcessor extends AbstractProcessor {
//     @Override
//     public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
//         if (roundEnv.processingOver()) return false;          // 最后一轮不再生成
//         for (Element e : roundEnv.getElementsAnnotatedWith(Builder.class)) {
//             String pkg = processingEnv.getElementUtils().getPackageOf(e).toString();
//             String name = e.getSimpleName() + "Builder";
//             try (Writer w = processingEnv.getFiler()
//                     .createSourceFile(pkg + "." + name).openWriter()) {
//                 w.write("package " + pkg + "; public class " + name + " {}");
//             } catch (java.io.IOException ex) { throw new RuntimeException(ex); }
//         }
//         return true;
//     }
// }

public class Main {
    public static void main(String[] args) {
        System.out.println("processing is a compile-time step");   // processing is a compile-time step
        System.out.println(SourceVersion.latestSupported());        // RELEASE_26
    }
}
```

`AbstractProcessor` 由 `ProcessingEnvironment` 提供 `Filer`（生成文件）、`Elements` 与 `Types`（查询元素与类型）、`Messager`（报诊断）四个工具，`process` 返回 `true` 表示这批注解已被消费、不再传给后续处理器。分轮机制要小心：如果某轮生成的代码又引入了新注解，就会再来一轮；判断最后用 `roundEnv.processingOver()`，否则可能无限生成。生态里的分工很清楚：Lombok 用非标准 API 直接改 AST，能往类里插方法但每次 JDK 升级都可能出问题；MapStruct 与 AutoValue 走标准处理器路线，生成的是独立的实现类或子类，稳定且可读；Dagger 也走标准路线但用 KSP/Kotlin 时的形态不同。选型原则是"能生成新类就不要改旧类"。

📘 [Java · AbstractProcessor](https://docs.oracle.com/en/java/javase/25/docs/api/java.compiler/javax/annotation/processing/AbstractProcessor.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的编译期代码生成不靠"运行宿主程序"，而靠模板实例化与 `constexpr` 求值：编译器本身就是那个解释器，模板是它的代码生成语言。C++20 的 `consteval` 强制函数只能在编译期求值，`constinit` 强制静态初始化发生在编译期，`if constexpr` 提供编译期分支。C++23 基线里没有反射，C++26 才把静态反射纳入标准。

```cpp
#include <array>
#include <cstdio>
#include <string_view>
#include <type_traits>

// 模板元编程：用递归特化在编译期算阶乘
template <int N> struct Fact { static constexpr int value = N * Fact<N - 1>::value; };
template <> struct Fact<0> { static constexpr int value = 1; };

// constexpr 函数：编译期与运行期都能用
constexpr int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
static_assert(fib(10) == 55);

// consteval：只允许编译期求值，运行期调用直接编译失败
consteval int twice(int n) { return n * 2; }

// constinit：保证静态初始化在编译期完成，杜绝静态初始化顺序问题
constinit static int counter = twice(21);

// 用 constexpr 生成编译期数组，替代“宏展开一堆常量”的写法
template <std::size_t N>
constexpr std::array<int, N> make_seq() {
    std::array<int, N> a{};
    for (std::size_t i = 0; i < N; ++i) a[i] = static_cast<int>(i * i);
    return a;
}
constexpr auto squares = make_seq<5>();

int main() {
    std::printf("%d\n", Fact<5>::value);            // 120
    std::printf("%d\n", fib(10));                   // 55
    std::printf("%d\n", counter);                   // 42
    std::printf("%d %d %d\n", squares[0], squares[2], squares[4]);   // 0 4 16
    std::printf("%.*s\n", 3, "ok!");                 // ok!
    return 0;
}
```

`static_assert` 与 `consteval` 是这套体系的两道保险：前者把编译期计算的结果钉住，后者保证某个函数绝不在运行期被调用。`constinit` 解决的是静态初始化顺序这个老问题，它不要求常量表达式，只要求初始化在编译期完成，因此可以配合 `constexpr` 构造函数使用。模板的代价是实例化开销与诊断长度，`if constexpr` 让分支裁剪可读了许多，但被丢弃的分支仍需语法正确。C++26 的静态反射（P2996 系列，配 `<meta>` 头文件与 `^^` 反射运算符）会提供 `std::meta::info` 与一批 `std::meta` 函数，届时"遍历成员并生成代码"才成为标准能力；同一版本还引入展开语句（`template for`），两者经常一起用。按 C++23 基线这些不可用，各编译器对 C++26 的支持也不完整，需要用则要查编译器支持表。

📘 [cppreference · consteval](https://en.cppreference.com/w/cpp/language/consteval)

{{% /tab %}}

{{% tab header="C" %}}

C 没有"在编译期运行任意代码"的机制，也没有模板：编译器只做预处理、语法分析与常量折叠。因此 C 的编译期代码生成只有三条路——宏展开（预处理期）、`_Generic`（编译期按类型选表达式）、以及构建前的独立生成器（`m4`、`protoc`、Qt 的 `moc`、脚本生成 `.h`/`.c`）。C23 的 `constexpr` 只作用于变量，不能修饰函数，这一点和 C++ 差别很大。

```c
#include <stdio.h>

/* 编译期常量对象：C23 的 constexpr 只能修饰变量，不能修饰函数 */
constexpr int F10 = 55;
static_assert(F10 == 55, "F10 must be 55");     /* C23 起 static_assert 是关键字 */

#define SQUARE(x) ((x) * (x))
#define TYPE_NAME(x) _Generic((x), int: "int", double: "double", default: "other")

constexpr int SQ = SQUARE(3) + 1;               /* 宏展开后再常量折叠 */
static_assert(SQ == 10, "SQ must be 10");

/* 构建前生成器（m4）示意：define(`SQUARE', `(($1) * ($1))') 之后
   m4 会把 SQUARE(3) 展开成 ((3) * (3)) 写进源文件，再交给编译器 */

int main(void) {
    printf("%d\n", F10);                                     /* 55 */
    printf("%d\n", SQ);                                      /* 10 */
    printf("%s %s\n", TYPE_NAME(1), TYPE_NAME(1.5));           /* int double */
    return 0;
}
```

C 里最古老的"编译期代码生成"工具是 `m4`：它是通用宏处理器，`define` 与 `dnl` 加上位置参数就能把 `SQUARE(3)` 展开成 `((3) * (3))`，`autoconf` 整条工具链都建立在它之上，`bison` 与 `flex` 的输入也是通过 m4 风格模板产出 C 代码。现代项目更多用专用生成器：`protoc` 从 `.proto` 生成消息结构、Qt 的 `moc` 从带 `Q_OBJECT` 的头文件生成元对象代码、各种 IDL 编译器生成序列化代码。它们的共同特征是"生成物是普通源码文件"，需要进版本库或写进构建规则；与宏相比，生成器能表达复杂逻辑、报错也更友好，代价是引入构建步骤与额外依赖。C11 的 `_Generic` 与 C23 的 `constexpr` 只能覆盖很小的编译期场景，剩下的一切仍要靠宏或外部工具。

📘 [cppreference · C 语言 constexpr](https://en.cppreference.com/w/c/language/constexpr)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的宏在**解析期**展开，这是它与过程宏最接近的地方：宏体是一段普通 Julia 代码，运行时给出表达式对象，因此"编译期执行"就是"在 lowering 之前执行"。想按参数类型在**特化时**生成代码，用的是 `@generated` 生成函数；想批量定义东西，用 `@eval` 或 `eval(quote` 到 `end)`。

```julia
# 宏：解析期展开，能拿到调用点写下的表达式
macro swap!(a, b)
    return quote
        local tmp = $(esc(a))       # 局部变量会被 gensym 重命名
        $(esc(a)) = $(esc(b))
        $(esc(b)) = tmp
    end
end

x, y = 1, 2
@swap!(x, y)
println((x, y))                      # (2, 1)

# @generated：按参数类型在特化时生成表达式（只能看类型，不能看值）
@generated function pow2(x)
    if x <: Integer
        return :(x * x)
    else
        return :(x)
    end
end
println(pow2(7))                     # 49
println(pow2("ab"))                  # ab

# @eval：批量生成方法（是 eval 加 quote 块的简写）
for op in (:double, :triple)
    @eval $(op)(v::Int) = v * $(op === :double ? 2 : 3)
end
println(double(21), " ", triple(14))  # 42 42
```

`@macroexpand` 与 `@macroexpand1` 是查看展开结果的标准工具，`macroexpand` 是它们的函数形式。`@generated` 的规则比宏严格得多：函数体只能访问参数的**类型**而不是值，只能调用在生成函数定义之前已定义的函数，不能读写任何可变全局状态，也不能有副作用——违反这些会让行为变成未定义，因为生成可能在任意时刻、任意次数发生。把 `@generated` 与函数体里的 `if @generated` / `else` 两条分支结合，可以同时提供生成版与普通版实现，编译器可以自行选择，官方推荐这种写法以保留静态编译的可能。`@eval` 是 `eval(quote` 到 `end)` 的简写，它把代码插入调用模块的全局作用域，适合批量定义方法或类型，但要记住它改变全局状态、让预编译失效，能用宏或函数参数化解决就不要用 `eval`。

📘 [Julia · 生成函数](https://docs.julialang.org/en/v1/manual/metaprogramming/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有两条编译期代码生成路线：源生成器（Source Generator，基于 Roslyn，随编译运行、能看到语义模型）与 T4 文本模板（独立模板引擎、只能看到你给它的输入）。源生成器分两代：`ISourceGenerator` 是第一代（v1，仍可用但不再推荐），第二代 `IIncrementalGenerator` 把生成过程拆成可缓存的管道，明显更快，是 .NET 6 与 Roslyn 4.0 之后的推荐形态。

```csharp
// ---- 生成器项目（netstandard2.0 + Microsoft.CodeAnalysis.CSharp）----
// [Generator(LanguageNames.CSharp)]
// public sealed class HelloGenerator : IIncrementalGenerator
// {
//     public void Initialize(IncrementalGeneratorInitializationContext context)
//     {
//         var names = context.CompilationProvider.Select(static (c, _) => c.AssemblyName ?? "unknown");
//         context.RegisterSourceOutput(names, static (spc, name) =>
//         {
//             spc.AddSource("Hello.g.cs", $$"""
//                 namespace Generated {
//                     [System.CodeDom.Compiler.GeneratedCode("HelloGenerator", "1.0")]
//                     public static partial class Hello {
//                         public static string Name => "{{name}}";
//                     }
//                 }
//                 """);
//         });
//     }
// }

// ---- 使用侧 ----
using System.CodeDom.Compiler;

namespace Generated
{
    [GeneratedCode("HelloGenerator", "1.0")]
    public static partial class Hello
    {
        public static string Name => "app";      // 实际由生成器写出
    }
}

public static class Program
{
    public static void Main()
    {
        Console.WriteLine(Generated.Hello.Name);  // app
#if NET10_0_OR_GREATER
        Console.WriteLine("net10.0");             // net10.0
#endif
    }
}
```

`IIncrementalGenerator` 的模型是"提供程序 + 管道 + 输出"：`SyntaxProvider` 与 `CompilationProvider` 这类提供程序产出可比较的值，管道按值是否变化决定是否重跑，最后用 `RegisterSourceOutput` 注册回调，用 `SourceProductionContext.AddSource` 写文件——缓存命中的部分不会重新执行，这是它比 v1 生成器快的原因。生成器**不能修改已有代码**，只能加新文件，所以配套写法是把目标类声明为 `partial`，让生成的部分补进来。`[GeneratedCode]` 属性会出现在生成文件里，分析器与工具据此识别来源。T4（`.tt`）是另一条路：设计时模板在 IDE 内生成、运行时模板在程序内生成，它完全看不到编译期语义，适合固定样板而不适合"按类型生成"。在 .NET 10 上 `IIncrementalGenerator` 的公开 API 形态未变，仍是推荐写法。

📘 [MS Learn · 增量生成器手册](https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有编译期执行的用户代码：`build_runner` 是构建前的独立进程，`source_gen` 是写生成器的框架。这套组合属于"构建期代码生成"，与 Rust 的过程宏、Zig 的 `comptime` 都不同——生成器看不到整个程序的类型信息，只能看自己声明的输入。最该先知道的是生成物命名约定（`part` 指令 + `.g.dart`）与增量机制。

```dart
// user.dart
import 'package:meta/meta.dart';

part 'user.g.dart';               // 生成文件必须是 part

@immutable
class User {
  const User({required this.id, required this.name});
  final int id;
  final String name;

  // 生成器会补上 fromJson / toJson（json_serializable 风格）
  // 手写版本在这里给出，方便对照生成结果
  factory User.fromJson(Map<String, dynamic> json) =>
      User(id: json['id'] as int, name: json['name'] as String);

  Map<String, dynamic> toJson() => {'id': id, 'name': name};
}

void main() {
  const u = User(id: 1, name: 'Ada');
  print(u.id);                                  // 1
  print(u.name);                                // Ada
  print(User.fromJson(u.toJson()).name);        // Ada
}
```

生成器框架 `source_gen` 用 `Generator` 与 `GeneratorForAnnotation` 抽象"输入哪些文件、产出哪些文件"，`build_runner` 负责调度、依赖分析与增量缓存；配置写在 `build.yaml`，构建方式是 `dart run build_runner build --delete-conflicting-outputs` 或 `watch`。`part`/`part of` 是硬性要求：生成文件必须被原文件用 `part` 引用，否则生成出来的方法挂不到类上。生态里的典型分工是 `json_serializable` 生成 JSON 编解码、`freezed` 生成不可变数据类与联合类型、`built_value` 生成值类型、`retrofit` 生成 HTTP 客户端；`.g.dart` 与 `.freezed.dart` 通常加进 `.gitignore` 或提交进仓库，两种做法都要在团队内统一，因为 CI 没有跑生成就会编译失败。性能上要注意 `build_runner` 的首次构建与全量重建都相当慢，拆分生成器与减少 `builders` 数量能明显改善。

📘 [Dart · metadata 与代码生成](https://dart.dev/tools/build_runner)

{{% /tab %}}

{{% tab header="R" %}}

R 没有编译期：语言是解释执行的，`byte-compile` 只把函数编译成字节码提速，不改变语义也不做条件求值。所谓"编译期代码生成"在 R 里对应的是**构建期**：`Rcpp` 把 C++ 源码编译成共享库，`roxygen2` 从注释生成 `.Rd` 文档与 `NAMESPACE`，`src/Makevars` 与 `configure` 在安装时决定编译选项。包一旦装好，运行期就只剩解释执行。

```r
# roxygen2：注释即文档，devtools::document() 时生成 .Rd 与 NAMESPACE
#' Add two numbers
#' @param a first number
#' @param b second number
#' @return the sum
#' @export
add <- function(a, b) a + b

# byte-compile：把函数编译成字节码，语义不变、速度提升
fast <- compiler::cmpfun(function(n) {
  s <- 0
  for (i in seq_len(n)) s <- s + i
  s
})

cat(add(1, 2), "\n")                       # 3
cat(fast(100), "\n")                       # 5050
cat(is.function(compiler::cmpfun(add)), "\n")   # TRUE

# Rcpp：C++ 代码在包安装时编译，运行期只调用编译好的函数
# Rcpp::sourceCpp("fib.cpp") 会在开发期编译并加载
cat(.Platform$OS.type, "\n")               # unix
```

`roxygen2` 的模式是"文档写在源码注释里，用 `devtools::document()` 生成 `.Rd` 与 `NAMESPACE`"，这是 R 包里最接近宏的体验：注释里的 `@export`、`@param`、`@return` 会被翻译成真实的包元数据，但它由构建脚本执行、与编译无关。`Rcpp` 与 `cpp11` 的流程是"用 `Rcpp::sourceCpp` 或包安装期的 `Makevars` 编译 C++，再用 `.Call` 调用"，其中 `// [[Rcpp::export]]` 这个属性由 `Rcpp::compileAttributes()` 解析并生成 `RcppExports.cpp` 与 `RcppExports.R`——这是 R 生态里最典型的代码生成步骤，必须在 `devtools::document()` 或安装前跑。`compiler::cmpfun` 与 `compiler::enableJIT` 提供的是运行期优化，与代码生成无关，不要和它们混为一谈。真正的"编译期预计算"惯用法是在包的 `data-raw/` 目录里放一个脚本（`usethis::use_data_raw()` 会建好这个约定），用 `usethis::use_data()` 把昂贵的计算结果固化成 `data/` 下的 `.rda` 随包分发，运行期只负责读取；`data-raw/` 进版本库但不参与安装，`R CMD INSTALL` 与运行期都不会重跑那段计算。

📘 [R · roxygen2](https://roxygen2.r-lib.org/)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的"过程宏"就是 `comptime`：编译器内置一个编译期求值器，任何不带运行期依赖的 Zig 代码都能在编译期跑，包括函数调用、分支、循环与类型构造。因此 Zig 不需要另写一个宏宿主程序——`build.zig` 是普通的 Zig 程序，`@typeInfo` 把类型变成数据，`inline for` 把循环展开成代码，`@compileError` 与 `@compileLog` 负责诊断。

```zig
const std = @import("std");

// comptime 函数返回 type：这就是 Zig 的“derive 宏”
fn Struct(comptime fields: []const std.builtin.Type.StructField) type {
    return @Type(.{ .@"struct" = .{
        .layout = .auto,
        .fields = fields,
        .decls = &.{},
        .is_tuple = false,
    } });
}

// 用 @typeInfo 遍历字段，为每个字段生成打印代码
fn dump(value: anytype) void {
    const T = @TypeOf(value);
    inline for (std.meta.fields(T)) |f| {
        std.debug.print("{s}={any} ", .{ f.name, @field(value, f.name) });
    }
}

pub fn main() void {
    const Vec2 = Struct(&.{
        .{ .name = "x", .type = f32, .default_value_ptr = null, .is_comptime = false, .alignment = @alignOf(f32) },
        .{ .name = "y", .type = f32, .default_value_ptr = null, .is_comptime = false, .alignment = @alignOf(f32) },
    });
    var p: Vec2 = .{ .x = 1.5, .y = 2.5 };

    dump(p);                                   // x=1.5 y=2.5
    std.debug.print("\n", .{});

    // build.zig 侧的等价物：把构建选项注入成模块
    // const opts = b.addOptions();
    // opts.addOption([]const u8, "mode", "release");
    // exe.root_module.addOptions("build_options", opts);

    const T = @TypeOf(p);
    std.debug.print("{d}\n", .{std.meta.fields(T).len});   // 2
}
```

`@Type` 与 `@typeInfo` 是一对互逆的内建函数：前者把 `std.builtin.Type` 数据变回类型，后者把类型变成数据，两者配合 `comptime` 参数就构成了完整的类型级代码生成。`inline for` 用于对元组、数组与 `@typeInfo` 取得的字段表做展开，它在编译期逐项生成代码，所以能在不写宏的情况下为每个字段生成不同的语句。约束也很硬：编译期代码必须无副作用（不能做 IO、不能改可变全局），不能调用尚未定义的函数，循环展开规模由 `@setEvalBranchQuota` 控制，默认配额是 1000 次向后分支（不是一万），超限要显式提高。`@compileLog` 是排查编译期逻辑的主要手段——它把值打印在编译输出里，而不是运行期。

📘 [Zig · 类型反射](https://ziglang.org/documentation/master/)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有编译期，也没有过程宏：`load` 与 `loadstring` 是运行期的字符串编译器，`debug` 库能做内省与改写，两者都不是编译期设施。Lua 生态里的"代码生成"基本落在宿主程序一侧——C 侧生成 Lua 脚本、构建脚本生成常量表，再由 Lua 在运行期加载。最该先知道的是 `load` 的错误约定与 `_ENV` 的作用。

```lua
-- load 的签名：load(chunk, chunkname, mode, env) -> function | nil, err
local f, err = load("return 1 + 1", "chunk1", "t", {})
assert(f, err)
print(f())                                   -- 2

local bad, msg = load("return 1 +", "badchunk", "t", {})
print(bad, type(msg))                        -- nil string

-- 显式给环境表：沙箱化的关键（默认环境是调用方的 _ENV）
local sandbox = { x = 10 }
local g = load("return x * 2", "sandboxed", "t", sandbox)
print(g())                                   -- 20

-- 用 debug 库做内省，替代“编译期检查”
print(debug.getinfo(f, "S").source)          -- chunk1
print(debug.getinfo(f, "S").linedefined)     -- 0

-- 元表：运行期行为注入
local proxy = setmetatable({}, { __index = function(_, k) return k end })
print(proxy.hello)                           -- hello
```

`load` 的第四个参数 `env` 在 Lua 5.2 之后取代了原先的 `setfenv`：传入一个表，被加载的代码就以它为 `_ENV`，于是所有全局访问都落在沙箱里，这是 Lua 做配置与插件沙箱的标准手法。`chunkname` 参数会出现在错误消息与 `debug.getinfo` 的 `source` 里，务必传有意义的名字。`mode` 参数（`"b"`、`"t"`、`"bt"`）限制能加载字节码还是文本，从不可信来源加载字节码有安全风险——字节码可以被构造成能突破沙箱的形式。运行期生成代码的代价是明显的：多一次解析、无法被静态分析、错误只在运行时暴露；因此能用表驱动或函数组合表达的逻辑就不要用字符串拼接加 `load`。

📘 [Lua 5.5 · load](https://www.lua.org/manual/5.5/manual.html#pdf-load)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有编译期执行的用户代码：`tsc` 不加载第三方插件，类型层面的一切（条件类型、映射类型、模板字面量类型）在编译后完全消失。要做真正的 AST 变换只有三条路——用编译器 API 自己驱动一次编译、用 `ts-patch` 给 `tsc` 打补丁加载 transformer、或者干脆把构建换成 Babel / SWC。装饰器是标准语法，但它是**运行时**函数调用。

```typescript
// 装饰器：运行时函数，5.0 标准形态的参数是 (value, context)
function logged<This, Args extends unknown[], Ret>(
  value: (this: This, ...args: Args) => Ret,
  context: ClassMethodDecoratorContext<This, (this: This, ...args: Args) => Ret>,
) {
  return function (this: This, ...args: Args): Ret {
    console.log(`calling ${String(context.name)}`);   // 运行时打印方法名
    return value.apply(this, args);
  };
}

class Calc {
  @logged
  add(a: number, b: number): number { return a + b; }
}

console.log(new Calc().add(1, 2));   // 先打印 calling add，再打印 3

// 类型层面的“编译期”：模板字面量类型 + 映射类型，编译后无产物
type Event = "click" | "focus";
type Handler = { [K in Event as `on${Capitalize<K>}`]: () => void };
const h: Handler = { onClick: () => {}, onFocus: () => {} };
console.log(Object.keys(h).sort().join(","));   // onClick,onFocus
```

5.0 的标准装饰器参数是 `(value, context)`，`context` 提供 `kind`、`name`、`static`、`private`、`access`、`addInitializer` 等字段；legacy 装饰器（`experimentalDecorators`）参数是 `(target, key, descriptor)`，两者语义不同且不能混用，升级时要一并检查运行时的反射库。`ts-patch` 的作用是让原版 `tsc` 能加载 `transformers` 配置里指定的 transformer，这样可以在不换构建工具的前提下改写 AST；它要求 TypeScript 版本与补丁版本严格匹配，升级 TS 时往往要等 `ts-patch` 跟进。按 TypeScript 7 的基线还要多考虑一步：7.0 是 Go 重写的原生编译器（官方称 10x faster native port），它**不随版本提供编译器 API**，官方计划到 7.1 才给出新的、与旧版不同的 API，并让需要程序化访问编译器的工具与 6.0 并排运行（官方为此提供 `@typescript/typescript6` 与 `tsc6`）；所以在当前基线上，依赖旧 API 的 transformer 与 `ts-patch` 方案必须先确认它对原生编译器的支持情况。用编译器 API 自己做则要处理 `Program`、`TypeChecker`、`Printer` 与 source map，成本高但完全可控。实践中"像宏一样"的需求多数能靠类型体操 + 少量运行时代码解决，真需要语法变换时选 Babel 生态最省事。

📘 [TypeScript · 编译器 API](https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有编译期，也没有"编译期执行"的概念：整门语言只有运行时。Babel 与 SWC 插件是在构建期真正改写 AST 的手段，`eval` 与 `new Function` 是运行期的字符串求值手段，Proxy 与 Reflect 是运行期的行为拦截手段。三者的能力与代价完全不同，最该先分清的是"改语法结构"（Babel/SWC）与"改行为"（Proxy/eval）。

```javascript
// 构建期：Babel/SWC 插件改 AST（形态示意，需 @babel/core 才能跑）
// 插件导出 visitor，按节点类型注册回调，用 @babel/types 构造新节点

// 运行期：new Function 与 eval 是字符串求值
const add = new Function("a", "b", "return a + b");
console.log(add(1, 2));                       // 3
console.log(eval("2 ** 10"));                 // 1024

// 运行期：Proxy 拦截读写，Reflect 提供默认行为
const target = { count: 0 };
const p = new Proxy(target, {
  get(t, k, r) { return Reflect.get(t, k, r); },
  set(t, k, v, r) {
    if (k === "count" && typeof v !== "number") throw new TypeError("count must be number");
    return Reflect.set(t, k, v, r);
  },
});
p.count = 5;
console.log(p.count);                          // 5
try { p.count = "x"; } catch (e) { console.log(e.constructor.name); }  // TypeError

// 运行时代码生成：编译模板为函数（Vue/模板引擎的常规做法）
const compile = (tpl) => new Function("data", `return \`${tpl}\``);
console.log(compile("Hello ${data.name}")({ name: "Ada" }));   // Hello Ada
```

`new Function` 与 `eval` 的区别值得记牢：`eval` 在当前作用域执行、能读写局部变量，`new Function` 永远在全局作用域执行、只看得见全局与自己的参数，因此后者更安全也更快（不会被局部作用域干扰，V8 能更好地优化）。Proxy 的 `set` 陷阱里返回 `false` 会让赋值在严格模式下抛 `TypeError`，抛异常则是更明确的写法；`Reflect` 配合使用能拿到默认语义，避免手写赋值逻辑时漏掉原型链或 getter/setter。模板编译成 `new Function` 是 Vue 运行时编译器的真实做法，代价是 CSP 环境（禁止 `unsafe-eval`）下不可用，所以现代框架都提供预编译（构建期把模板编译成 render 函数）来绕开这个限制——这正好说明了"构建期做"与"运行期做"的取舍。

📘 [MDN · eval](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/eval)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有编译期执行的用户代码：`eval` 是运行期的字符串编译执行，attributes 靠反射在运行时读取，属性钩子是语言内建的属性级语法糖。三者当中只有 `eval` 能"生成代码"，而它生成的是当前作用域里立即执行的代码，不会被缓存也不会进 opcache。最该先知道的是 `eval` 的安全边界与反射的代价。

```php
<?php
#[\Attribute(\Attribute::TARGET_CLASS)]
class Table { public function __construct(public string $name) {} }

#[Table('users')]
class User {
    public function __construct(public int $id = 0, public string $name = '') {}

    // 8.4 属性钩子：语言内建，不是宏
    public string $label = 'user' {
        get => strtoupper($this->label);
    }
}

// 反射读注解：运行期代价，框架会缓存结果
$rc = new ReflectionClass(User::class);
echo $rc->getAttributes(Table::class)[0]->newInstance()->name, "\n";   // users

// eval：运行期生成并执行代码
$method = 'greet';
eval('class Gen { public function ' . $method . '() { return "hi"; } }');
echo (new Gen())->greet(), "\n";                                       // hi

$u = new User(1, 'ada');
echo $u->label, "\n";                                                  // USER
echo $u->name, "\n";                                                   // ada
```

`eval` 的输入是 PHP 代码字符串，必须以分号结尾、不能带 `<?php`，并且它**继承当前作用域**：局部变量在 `eval` 里可见，`return` 会把值带回调用处。它无法被 opcache 缓存，每次执行都要重新编译，还有严重的注入风险，所以现代 PHP 代码基本只在极端场景（如运行用户提交的表达式、动态生成类）才用它，正规做法是把代码生成搬到构建期。attributes 读取要显式走反射 API，`newInstance()` 才会构造注解对象，因此热路径上必须缓存；`ReflectionClass` 还会阻塞某些 opcache 优化，这也是"注解好用但要注意性能"的原因。属性钩子在 8.4 起可用，`get`/`set` 的简写形式让属性访问自带逻辑，与 `__get`/`__set` 相比有完整类型信息且性能更好。

📘 [PHP · eval](https://www.php.net/manual/en/function.eval.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有编译期机制：MRI 会把源码编译成字节码（YARV 指令）后再解释执行，但这个编译阶段不运行用户代码。所有"代码生成"都在运行期，手段是 `eval`、`instance_eval`、`class_eval`、`define_method` 与 `Module#prepend`。最该先知道的是各种 `eval` 的作用域差异——它们决定代码在谁的绑定里执行。

```ruby
# frozen_string_literal: true

class Report
  # define_method：用块定义方法，块是闭包，能捕获外部变量
  %i[revenue cost].each do |metric|
    define_method(:"#{metric}_in_cents") { public_send(metric) * 100 }
  end

  def revenue = 10
  def cost = 4
end

r = Report.new
puts r.revenue_in_cents     # 1000
puts r.cost_in_cents        # 400

# class_eval 打开类（运行时改结构）；eval 编译字符串并执行
Report.class_eval do
  def profit = revenue - cost
end
puts r.profit                # 6

# instance_eval 在对象自身的作用域里执行块，可访问私有方法
puts r.instance_eval { profit * 2 }   # 12

# eval 用字符串：能访问当前作用域的局部变量
local = 5
puts eval("local * 2")       # 10
```

`define_method` 与 `def` 的关键差别是作用域：`define_method` 传块，块捕获定义处的局部变量与 `self`；`def` 里的方法体不捕获外部作用域，方法名也不能用变量拼。`class_eval` 打开类对象、`instance_eval` 打开接收者对象、`module_eval` 等价于 `class_eval`，三者的区别在于 `self` 与常量查找路径。`eval` 与 `instance_eval` 接受字符串时会把字符串当源码编译，性能差且难以审计，安全场景要配合 `$SAFE`（已废弃）或用 `RubyVM::InstructionSequence` 做受限编译。要做构建期代码生成，Ruby 生态的常规选择是 ERB 模板（Rails 脚手架、配置文件）、`Rake` 任务与 `rails generate` 生成器，它们都不在语言层。

📘 [Ruby · Kernel#eval](https://docs.ruby-lang.org/en/master/Kernel.html)

{{% /tab %}}

{{< /tabpane >}}

### 没有宏的语言用什么替代

这一节按替代机制归类：**装饰器与注解**（Java、C#、Kotlin、Python、TypeScript、Swift、Dart、PHP）、**元编程与反射**（Ruby、Python、JavaScript、Lua、R、Julia、PHP、Go）、**代码生成工具**（Go、Dart、Java、C#、TypeScript、C/C++、Rust、Swift、Python、Ruby、PHP、R、Zig）、**泛型与高阶函数**（几乎所有语言）、以及能力最强也最危险的**字符串求值**。每一类都有明确的能力边界：装饰器不改变语法，反射看不见词法结构，代码生成需要额外构建步骤，泛型只能参数化而无法改变代码形状。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 有真正的宏，所以"替代"在这里指的是"哪些需求其实不该用宏解决"。首选是泛型与 trait：单态化会为每个具体类型生成专用代码，效果类似 C++ 模板，但没有文本替换的副作用；其次是高阶函数与迭代器，它们把"重复的控制流"变成库调用；构建期注入则用 `build.rs`，它能在编译前算出常量并通过 `cargo::rustc-cfg` 与 `cargo::rustc-env` 注入。

```rust
// 泛型 + trait：替代“为每种类型写一个宏”的最常见手段
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut max = list[0];
    for &x in &list[1..] { if x > max { max = x; } }
    max
}

// Cargo.toml 同目录下的 build.rs，只列关键两行
// fn main() {
//     println!("cargo::rustc-env=GENERATED_BY=build.rs");   // 编译前注入环境变量
//     println!("cargo::rerun-if-changed=build.rs");          // 精确控制重跑时机
// }

fn main() {
    // 高阶函数与迭代器：替代“展开循环”的宏
    let doubled: Vec<i32> = (1..4).map(|x| x * 2).collect();

    println!("{}", largest(&[1, 5, 3]));      // 5
    println!("{}", largest(&["a", "c", "b"])); // c
    println!("{:?}", doubled);                 // [2, 4, 6]
    println!("{}", env!("GENERATED_BY"));      // build.rs（由上面的 build.rs 注入）
}
```

`build.rs` 是 Cargo 的构建脚本，在编译 crate 之前运行，通过 `cargo::rustc-env=KEY=value` 注入编译期环境变量、通过 `cargo::rustc-cfg=flag` 注入 `cfg` 条件（并从 1.80 起建议同时写 `cargo::rustc-check-cfg=cfg(flag)` 以消除 lint 警告），还可以用 `cargo::rerun-if-changed` 精确控制重跑时机。它常被用来编译 C 代码（`cc` crate）、生成 protocol buffer 绑定（`prost`）、写入版本号与 git 提交哈希。判断标准很清楚：如果需求是"按类型生成不同的函数体"，用泛型加 trait；如果是"接受任意语法形式"，才需要宏；如果是"编译前算出常量或生成绑定"，用 `build.rs`。三种手段各有其位，不要把 `build.rs` 当成宏的替代品去做语法变换。

📘 [Rust · 构建脚本](https://doc.rust-lang.org/cargo/reference/build-scripts.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 在 5.9 之前完全没有宏，替代手段是属性包装器（`@propertyWrapper`）、结果构建器（`@resultBuilder`）、协议扩展与泛型；5.9 之后有了外部宏，"替代"更多指的是"优先用语言内建能力"。属性包装器在编译期被改写存取代码，运行期是一个普通类型；泛型在编译期做特化；两者都不需要额外的编译器插件，因此构建更简单、报错更友好。

```swift
// 属性包装器：在编译期改写属性的读写，运行时是普通类型
@propertyWrapper
struct Clamped {
    var wrappedValue: Int {
        didSet { wrappedValue = min(max(wrappedValue, 0), 100) }
    }
    init(wrappedValue: Int) { self.wrappedValue = min(max(wrappedValue, 0), 100) }
}

struct Score { @Clamped var value: Int = 0 }

// 泛型函数替代“为每种类型写一遍”
func swapValues<T>(_ a: inout T, _ b: inout T) { let t = a; a = b; b = t }

var s = Score()
s.value = 150
print(s.value)                          // 100

var x = 1, y = 2
swapValues(&x, &y)
print(x, y)                             // 2 1

// 高阶函数：map/filter/reduce 覆盖了大多数“想加语法糖”的场景
print([1, 2, 3].map { $0 * 2 })          // [2, 4, 6]
print([1, 2, 3].reduce(0, +))            // 6
```

属性包装器会把 `@Clamped var value` 改写成 `var value: Int { get { _value.wrappedValue } set { _value.wrappedValue = newValue } }` 加一个 `_value` 存储属性；`init(wrappedValue:)` 是固定名字的初始化器，所以自定义包装器必须提供它（或 `init()`）。`projectedValue` 可以额外暴露一个"投影"值，用于实现 `@Published` 那种 `$value` 语法。泛型在 Swift 里默认走"泛型特化 + witness table"混合策略，不需要手写模板特化。构建期代码生成在 Swift 生态里也有成熟的第三方工具：Sourcery 从源码与模板生成样板代码（Equatable、Hashable、mock、依赖注入容器），SwiftGen 从资源目录生成类型安全的字符串与图片常量；两者都在构建前跑、产出普通 Swift 文件，与 5.9 的宏解决的是同一类问题但不需要插件机制。判断标准是：能在属性读写层面表达的用属性包装器，能在类型层面表达的用泛型与协议，能做 DSL 的用结果构建器，能在构建期固化的用 Sourcery 或 SwiftGen；只有需要读取调用点语法、生成全新声明或验证字符串字面量这类需求，才值得写外部宏并承担插件构建的复杂度。

📘 [Swift · 属性包装器](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/properties/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 明确没有宏，替代路线是三条：泛型与高阶函数做抽象、`reflect` 做运行时内省、`go generate` 做代码生成。选择顺序也很清楚——能用泛型与接口表达的就不要反射，能反射解决的就不要生成，因为反射放弃类型安全与性能，生成则引入构建步骤。

```go
package main

import (
	"fmt"
	"reflect"
)

// Go 1.18+ 泛型：替代“为每种类型写一个函数”的宏
func Map[T, U any](xs []T, f func(T) U) []U {
	out := make([]U, 0, len(xs))
	for _, x := range xs {
		out = append(out, f(x))
	}
	return out
}

type Point struct {
	X int    `json:"x"`
	Y int    `json:"y"`
	Z string `json:"z,omitempty"`
}

func main() {
	fmt.Println(Map([]int{1, 2, 3}, func(x int) int { return x * 2 }))  // [2 4 6]
	fmt.Println(Map([]int{1, 2}, func(x int) string { return "n" }))    // [n n]

	// reflect 读结构体标签：替代注解处理器（但只在运行时）
	t := reflect.TypeOf(Point{})
	for i := 0; i < t.NumField(); i++ {
		f := t.Field(i)
		fmt.Printf("%s=%s ", f.Name, f.Tag.Get("json"))
	}
	fmt.Println()                                                       // X=x Y=y Z=z,omitempty
}
```

`Map` 这样的泛型函数在 Go 里是首选，因为它在编译期单态化（或按类型字典共享代码），没有反射开销也没有额外构建步骤。有一条边界必须记牢：含 union 元素（`|`）或近似元素（`~`）的接口只能当**类型约束**，不能当值类型——写成 `type Num interface{ ~int | ~string }` 之后再声明 `var x Num` 会被编译器拒绝，Go 1.27 的报文是 `cannot use type Num outside a type constraint: interface contains type constraints`，只有不含类型元素的普通接口才能声明变量与字段。`reflect` 能读结构体标签、字段名、方法集，但读不到源码结构，也不能生成代码，而且字段访问会失去编译期检查、性能比直接访问低一个数量级，热路径上必须避免。代码生成覆盖前两者的盲区：需要"从接口自动生成 mock"或"从 markdown 自动生成常量"时，写一个生成器并加 `//go:generate` 注释是唯一正规做法，生成结果进版本库。数据库与 JSON 这类场景的生态惯例也印证了这个分工：`encoding/json` 用反射，而要求高性能的项目改用生成器（`easyjson` 之类）把编解码代码静态化。

📘 [Go · reflect](https://pkg.go.dev/reflect)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有宏，替代手段按侵入性从低到高排列：装饰器改写函数与类的行为、`__init_subclass__` 与元类改写类创建、`getattr`/`setattr` 与 `functools` 做动态装配、`exec` 与 `ast` 做真正的代码生成。绝大多数"想用宏"的需求落在前两档，它们的可调试性与静态分析友好度都远好于字符串求值。

```python
import functools

# 1. 装饰器：不改语法，改对象
def logged(fn):
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        return fn(*a, **kw)
    return wrapper

@logged
def add(a, b):
    """add two numbers"""
    return a + b

# 2. __init_subclass__：类定义时自动登记，不需要元类
class Plugin:
    registry: dict[str, type] = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        Plugin.registry[cls.__name__] = cls

class Csv(Plugin): pass
class Json(Plugin): pass

# 3. 动态装配：setattr 批量挂方法
class Bag: pass
for name in ("open", "close"):
    setattr(Bag, name, lambda self, _n=name: f"{_n} done")

print(add(1, 2))                                  # 3
print(add.__name__, "/", add.__doc__)             # add / add two numbers
print(sorted(Plugin.registry))                    # ['Csv', 'Json']
print(Bag().open(), Bag().close())                # open done close done
```

装饰器与宏最本质的区别是它作用在**已经求值出来的对象**上：函数装饰器拿到的是函数对象，类装饰器拿到的是类对象，因此它无法改变函数体内的语法，只能包装调用、替换对象或注册信息。`__init_subclass__` 比元类更好用，因为它不需要理解 `metaclass` 的继承规则，只关心"子类被定义"这一事件。`setattr` 批量挂方法方便但会让静态分析工具与 IDE 完全失效，务必配 `__all__` 或类型存根（`.pyi`）。真正需要语法层变换时，`ast` 加 `compile` 是标准路线，但生成出来的代码无法被 mypy 检查，所以生成器项目通常同时产出 `.pyi`。

📘 [Python · functools.wraps](https://docs.python.org/3/library/functools.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 没有宏，替代手段是注解加 KSP、委托属性、`inline` 加 `reified` 泛型、以及扩展函数。选择逻辑是：能靠类型系统与委托表达的就不写处理器，需要生成样板时才上 KSP。委托属性（`by`）是 Kotlin 里最被低估的替代品，它把"重复的属性访问逻辑"抽成可复用对象，编译器在编译期插入存取代码。

```kotlin
import kotlin.properties.Delegates

// 委托属性：编译期插入存取逻辑，运行时是普通对象
class User {
    var name: String by Delegates.observable("") { _, old, new ->
        println("$old -> $new")            // 打印旧值到新值
    }
    val id: Int by lazy { 42 }             // 首次访问才计算
}

// inline + reified：把类型参数带到运行时（有限度地替代宏）
inline fun <reified T> typeName(): String = T::class.simpleName ?: "?"

// 扩展函数：给已有类型“加方法”，不需要修改原类
fun String.shout(): String = uppercase() + "!"

fun main() {
    val u = User()
    u.name = "ada"                          // -> ada
    println(u.id)                           // 42
    println(typeName<List<String>>())       // List（泛型实参被擦除，只剩下接口名）
    println("hi".shout())                   // HI!
}
```

`Delegates.observable` 与 `Delegates.vetoable` 在每次赋值时回调，`lazy` 只在首次读取时求值（默认线程安全），`by map` 能把属性映射到 `Map` 的键上——这些都不需要任何编译器插件，纯粹是标准库加语言语法。扩展函数是静态解析的：它不真正往类里加方法，只是编译成静态函数调用，因此不能被重写，也不能访问私有成员，跨模块使用时导入才能生效。`inline` 加 `reified` 能让类型参数在函数体里当具体类型用，这是"泛型无法表达"场景的常用出路，代价是代码膨胀与无法被非 inline 函数调用。需要批量生成 DTO、路由表、依赖注入绑定时，KSP 处理器是正规做法；需要改变语义时（如自动加序列化逻辑），才考虑编译器插件。

📘 [Kotlin · 委托属性](https://kotlinlang.org/docs/delegated-properties.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 没有宏，替代手段分三类：注解加反射（运行期读取元数据）、注解处理器（编译期生成新类）、以及泛型与函数式接口（把重复逻辑参数化）。运行期反射最灵活但最慢，注解处理器最快但需要额外模块与构建配置，泛型则是零运行期开销的常规选择。

```java
import java.lang.annotation.*;
import java.lang.reflect.Method;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

public class Main {
    @Retention(RetentionPolicy.RUNTIME)         // 运行期要读，必须是 RUNTIME
    @Target(ElementType.METHOD)
    @interface Labeled { String value(); }

    static class Api {
        @Labeled("list users")
        public List<String> users() { return List.of("a", "b"); }
    }

    // 泛型 + 函数式接口：替代“为每种类型写一遍”的宏
    static <T, R> List<R> map(List<T> in, Function<T, R> f) {
        return in.stream().map(f).collect(Collectors.toList());
    }

    public static void main(String[] args) throws Exception {
        System.out.println(map(List.of(1, 2, 3), x -> x * 2));      // [2, 4, 6]

        Method m = Api.class.getMethod("users");
        Labeled l = m.getAnnotation(Labeled.class);                  // 运行期反射读注解
        System.out.println(l.value());                               // list users
    }
}
```

`RetentionPolicy` 决定注解的可见性：`SOURCE` 只给注解处理器看、`CLASS` 进 class 文件但反射读不到、`RUNTIME` 才能被 `getAnnotation` 读出来；只有真正需要在运行期做决策时才用 `RUNTIME`，因为每次读取都要走反射、还会阻止某些优化。反射调用（`Method.invoke`）比直接调用慢一个数量级，热路径上应当把 `Method` 缓存起来或改用 `MethodHandle`（`java.lang.invoke`，JIT 能更好地内联）。泛型在 Java 里是类型擦除的，所以 `List<String>` 与 `List<Integer>` 在运行期是同一个类，靠泛型无法像 C++ 模板那样生成不同代码；要按类型生成专用代码只能靠注解处理器或手写。判断顺序建议是：能参数化的参数化，能编译期生成的用处理器，只有真正动态的需求才用反射。

📘 [JLS · 类型、值与变量](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有预处理器宏，所以"替代"指的是"哪些场合不该用宏"。答案是：模板与 concepts 替代类型泛化，`constexpr` 与 `consteval` 替代常量宏，`inline` 函数与 `enum class` 替代函数宏与常量宏，`std::source_location` 替代 `__LINE__`，`if constexpr` 替代条件编译中的类型分支。C++20 的 concepts 还让模板的约束与报错清晰了很多。

```cpp
#include <concepts>
#include <cstdio>
#include <string>
#include <type_traits>

// concepts：约束模板参数，替代“注释里写明只支持哪些类型”的宏
template <typename T>
concept Addable = requires(T a, T b) { { a + b } -> std::same_as<T>; };

template <Addable T> constexpr T add(T a, T b) { return a + b; }

// enum class：替代一组 #define 常量，有类型、有作用域
enum class Color { Red, Green, Blue };

// inline 函数替代函数宏，std::source_location 替代 __LINE__/__FILE__
constexpr const char *name(Color c) {
    switch (c) {
        case Color::Red: return "Red";
        case Color::Green: return "Green";
        case Color::Blue: return "Blue";
    }
    return "?";
}

int main() {
    std::printf("%d\n", add(1, 2));                      // 3
    std::printf("%s\n", name(Color::Green));              // Green
    std::printf("%d\n", static_cast<int>(Color::Blue));   // 2
    static_assert(std::is_integral_v<int>);
    return 0;
}
```

`enum class` 与 `#define RED 0` 的差别正是"类型系统"带来的：前者有独立类型、不会隐式转成整数、不会与别的常量撞名、在调试器里有名字；后者只是文本，作用域是整份文件。concepts 把"模板参数必须满足什么"从文档变成编译期约束，出错信息从几十行模板展开变成一句"约束不满足"，这是 C++20 之后写模板的最大改善。`std::source_location::current()` 作为默认实参使用时拿到的是调用点位置，比 `__LINE__` 多一层类型安全与作用域正确性。`constexpr` 与 `consteval` 的分工是：前者编译期运行期皆可、后者只允许编译期。总的原则是"宏只用于预处理器真正独占的场合"——条件编译、头文件包含、字符串化与记号拼接、以及 `assert` 这类需要拿到调用点文本的场景。

📘 [cppreference · constraints 与 concepts](https://en.cppreference.com/w/cpp/language/constraints)

{{% /tab %}}

{{% tab header="C" %}}

C 的替代手段最少：`_Generic` 提供编译期类型分派，`static inline` 函数替代函数宏，`enum` 与 `static const` 替代常量宏，函数指针与 `void *` 提供运行期"泛型"，而真正复杂的代码生成只能靠外部工具（`m4`、`protoc`、IDL 编译器）。最该记住的是每一条替代都只覆盖宏的一小部分能力。

```c
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

/* _Generic：编译期按类型选函数，替代“同一个名字的多个函数宏” */
#define ABS(x) _Generic((x), int: abs, long: labs, double: fabs)(x)

/* static inline 函数：有类型检查、有作用域，优于函数宏 */
static inline int square(int x) { return x * x; }

/* enum 替代一组 #define 常量 */
enum Color { COLOR_RED, COLOR_GREEN, COLOR_BLUE };
static const char *names[] = { "Red", "Green", "Blue" };

/* 函数指针 + void*：运行期泛型，代价是没有类型检查 */
static void apply(void *base, size_t n, size_t sz, void (*fn)(void *)) {
    for (size_t i = 0; i < n; i++) fn((char *)base + i * sz);
}
static void twice(void *p) { *(int *)p *= 2; }

int main(void) {
    printf("%d %ld %.1f\n", ABS(-3), ABS(-4L), ABS(-5.5));  /* 3 4 5.5 */
    printf("%d\n", square(1 + 2));                          /* 9 */
    printf("%s\n", names[COLOR_GREEN]);                     /* Green */

    int a[3] = { 1, 2, 3 };
    apply(a, 3, sizeof a[0], twice);
    printf("%d %d %d\n", a[0], a[1], a[2]);                 /* 2 4 6 */
    return 0;
}
```

`_Generic` 的选择依据是**表达式的类型**而不是值，而且所有分支的表达式都要能通过语法与语义分析（未选中的分支也会被检查类型兼容性），这让它比宏重载严格得多，也更安全。`static inline` 函数在 C99 起可用，它是替代函数宏的首选：参数只求值一次、有类型检查、能取地址、在调试器里可见；唯一的劣势是不能像宏那样"接受任意类型"，那部分只能交给 `_Generic`。用 `void *` 加函数指针做泛型是 C 的传统手法（`qsort`、`bsearch` 都这么写），但它丢掉了类型信息与长度信息，出错时通常是内存错误而不是编译错误。真正规模的代码生成（协议编解码、状态机、Qt 元对象）一律交给外部生成器，并把生成产物纳入构建流程。

📘 [cppreference · _Generic](https://en.cppreference.com/w/c/language/generic)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 有真正的宏，所以"替代"指的是官方反复强调的优先级：先用高阶函数与闭包，再用多重分派，最后才考虑宏与 `eval`。原因很实在——宏会改变作用域规则、难以调试、还可能让预编译失效。最实用的三条替代路径是函数作为参数、`do` 块语法、以及参数化类型加多重分派。

```julia
# 高阶函数 + do 块：绝大多数“想写宏”的场景其实是这个
function with_timing(f)
    t0 = time_ns()
    v = f()
    println("elapsed ns: ", time_ns() - t0)
    return v
end

result = with_timing() do
    6 * 7
end
println(result)                      # 42

# 多重分派：替代“按类型生成不同代码”的宏
area(w, h) = w * h
area(r::AbstractFloat) = π * r^2

println(area(2, 3))                  # 6
println(round(area(1.0), digits = 2))  # 3.14

# 参数化类型：替代“为每种元素类型写一遍”的宏
struct Box{T}
    value::T
end
println(Box(1).value, " ", Box("a").value)   # 1 a
println(typeof(Box(1)))                       # Box{Int64}
```

`do` 块语法是"把函数作为最后一个参数"的语法糖，`with_timing() do` 到 `end` 等价于 `with_timing(() -> ...)`，它让高阶函数用起来像控制流结构，覆盖了宏最常被误用的场景。多重分派是 Julia 的核心机制：同一个函数名按参数类型与个数选择方法，能力上等价于"按类型生成代码"，但它是语言内建的、可被编译期特化与内联的，不需要任何元编程。参数化类型让容器与算法对元素类型保持开放。真正需要语法变换时才写宏（比如 `@time`、`@assert` 这类需要拿到调用点表达式或文本的场合），需要按类型生成表达式时才用 `@generated`；`@eval` 与 `eval` 应当留到最后，因为它们会破坏预编译并让世界年龄（world age）问题浮现；真要为宏写"模式匹配"，社区库 MacroTools 提供了 `@capture`、`@q` 与 `walk` 这类工具，能在表达式层面做结构匹配，是手写 `Expr` 遍历的常用替代。

📘 [Julia · 函数与高阶函数](https://docs.julialang.org/en/v1/manual/functions/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 没有宏，替代手段按能力排序是：泛型与 LINQ（零额外成本）、属性加反射（运行期元数据）、源生成器（编译期生成新源码）、`Expression` 树（运行期构造可编译的代码）。属性与反射最灵活，源生成器性能最好，`Expression` 适合在运行期动态构造查询或委托。

```csharp
using System;
using System.Linq.Expressions;
using System.Reflection;

[AttributeUsage(AttributeTargets.Method)]
public sealed class LabelAttribute : Attribute
{
    public string Text { get; }
    public LabelAttribute(string text) => Text = text;
}

public class Api
{
    [Label("list users")]
    public string[] Users() => new[] { "a", "b" };
}

public static class Program
{
    public static void Main()
    {
        // 泛型 + LINQ：替代“为每种类型写一遍”的宏
        var doubled = System.Linq.Enumerable.Select(new[] { 1, 2, 3 }, x => x * 2);
        Console.WriteLine(string.Join(",", doubled));          // 2,4,6

        // 属性 + 反射：运行期读元数据
        var m = typeof(Api).GetMethod(nameof(Api.Users))!;
        var label = m.GetCustomAttribute<LabelAttribute>()!;
        Console.WriteLine(label.Text);                          // list users

        // Expression 树：运行期构造代码并编译成委托
        var p = Expression.Parameter(typeof(int), "x");
        var body = Expression.Multiply(p, Expression.Constant(2));
        var f = Expression.Lambda<Func<int, int>>(body, p).Compile();
        Console.WriteLine(f(21));                               // 42
    }
}
```

泛型在 .NET 里是**具化（reified）**的：`List<int>` 在运行期是真正不同的类型，值类型不会被装箱，这一点与 Java 的类型擦除不同，因此泛型能替代更多"为每种类型写一遍"的场合。属性加反射要付出反射代价，热路径上应缓存 `MethodInfo` 或编译成委托（`CreateDelegate`）；`Expression` 树与反射的区别在于它构造的是可被编译的表达式，`Compile()` 之后调用接近原生速度，ASP.NET Core 与 EF Core 的查询翻译都建立在这套机制上。源生成器则是"编译期就把样板写出来"的路线，适合 `System.Text.Json` 的序列化上下文、正则生成器、日志生成器这类场景；它的结果进产物、没有运行期反射成本，是 .NET 里最接近宏的机制。C# 14 起还多了 extension members：`extension<T>(IEnumerable<T> source) { ... }` 这样的块可以把扩展方法、扩展属性、静态扩展成员与用户定义运算符写在同一处，它属于语言内建的语法糖（不产生额外源码），能省掉一部分原本要靠源生成器补的样板，但能力仍限定在"给已有类型加成员"这一层。

📘 [MS Learn · 反射与属性](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 没有宏，替代手段是注解加 `build_runner` 代码生成、泛型、以及 `extension` 扩展方法。注解本身不产生代码，它只是给生成器看的标记；生成器把样板写成 `.g.dart` 文件后进入编译。最该先知道的是 `extension` 与 `extension type`：前者零成本地给已有类型加方法，后者提供零成本的包装类型。

```dart
// extension：给已有类型加方法，不需要修改原类型，也没有运行期开销
extension StringX on String {
  String shout() => toUpperCase() + '!';
}

// 泛型函数：替代“为每种类型写一遍”的宏
List<R> mapList<T, R>(List<T> xs, R Function(T) f) => xs.map(f).toList();

// 注解：只给 build_runner 的生成器看，本身不产生任何代码
class JsonModel {
  const JsonModel();
}

@JsonModel()
class User {
  const User({required this.id, required this.name});
  final int id;
  final String name;
}

void main() {
  print('hi'.shout());                                   // HI!
  print(mapList([1, 2, 3], (x) => x * 2));                // [2, 4, 6]
  const u = User(id: 1, name: 'Ada');
  print('${u.id} ${u.name}');                             // 1 Ada
  print(mapList(<String>[], (x) => x.length));            // []
}
```

`extension` 的方法在编译期被解析成静态调用，因此没有装箱、没有 vtable 查找，但也不能被重写、不能在运行期判断"某个类型有没有这个扩展"（Dart 3.3 起可以用 `extension type` 得到真正的新类型，它同样是零成本的包装，但参与类型检查）。`extension type` 的价值在于给 `String` 之类的基础类型套上一层有语义的类型（`UserId` 包 `int`），既保留零成本又能防止参数传错，这正是过去靠宏或代码生成才能达到的效果。注解加生成器的组合适合"必须有样板代码"的场景（JSON 编解码用 `json_serializable`、不可变数据类与联合类型用 `freezed`、路由表用 `go_router` 的生成器），而纯逻辑抽象优先用泛型与扩展方法，因为前者要付出构建时间与工具链复杂度。

📘 [Dart · extension 方法](https://dart.dev/language/extension-methods)

{{% /tab %}}

{{% tab header="R" %}}

R 的替代手段是 `substitute` 与 `bquote` 的非卫生元编程、S3/S4 泛型分派、以及 `eval` 族函数。`substitute` 能拿到实参表达式，这是 R 里实现"看起来像宏"的 API（`library`、`subset`、`with`、`plot` 的公式接口）的基础；S3 泛型则用 `UseMethod` 按第一个参数的类型分派，覆盖了大多数"按类型写不同实现"的需求。

```r
# substitute：拿实参的表达式，这是 R 里最像宏的能力
lazy_eval <- function(expr) {
  e <- substitute(expr)                 # 捕获表达式，不求值
  list(text = deparse(e), value = eval(e, parent.frame()))
}
a <- 6
res <- lazy_eval(a * 7)
cat(res$text, "=", res$value, "\n")     # a * 7 = 42

# S3 泛型：按第一个参数的类型分派，替代“按类型生成代码”
area <- function(x, ...) UseMethod("area")
area.default <- function(x, ...) NA_real_
area.numeric <- function(x, ...) x^2

cat(area(3), "\n")                      # 9
cat(area("a"), "\n")                    # NA

# bquote + eval：构造并执行表达式
expr <- bquote(.(a) + 1)
cat(eval(expr), "\n")                   # 7
```

R 没有泛型参数化：S3/S4 的"泛型"指的是按类型分派的函数族，而不是带类型参数的容器，向量本身是同质的（`c(1, "a")` 会把整条向量提升成字符型）。`substitute(expr)` 与 `eval(substitute(expr), parent.frame())` 的组合是 R 元编程的经典惯用法，`parent.frame()` 保证表达式在调用者的环境里求值，否则会找不到变量。`deparse` 把语言对象还原成字符串，用于日志与错误提示。S3 的 `UseMethod` 只按第一个参数分派，方法命名约定是 `泛型名.类名`，因此扩展一个新类只需要写一个新函数，不需要修改泛型本身——这是 R 里"开放扩展"的主要机制。`bquote` 的 `.()` 支持把已求值的值嵌进表达式，适合在循环里批量生成公式或调用。需要注意的是这套机制完全没有卫生性：`substitute` 捕获的表达式携带调用者环境，跨环境 `eval` 必须显式传 `envir`，否则会得到难以理解的"找不到对象"错误。

📘 [R · bquote](https://stat.ethz.ch/R-manual/R-devel/library/base/html/bquote.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有宏，替代手段是 `comptime`、`inline for`、`@typeInfo`、`anytype` 参数与 `comptime` 返回 `type` 的函数（见前两节）。在"没有宏用什么替代"这个视角下，最常用的是三样：用 `anytype` 写"接受任何类型"的函数、用 `@typeInfo` 做类型驱动的分支、用 `build.zig` 把构建配置注入成模块常量。最该先记住的是 Zig 里没有运行期反射，所有类型信息必须在编译期用完。

```zig
const std = @import("std");

// anytype：参数类型不写死，编译期为每个调用点生成专用版本
fn printAll(values: anytype) void {
    inline for (values) |v| {
        std.debug.print("{any} ", .{v});
    }
}

// @typeInfo 做类型驱动分支：编译期判断，未选中分支被裁掉
fn describe(comptime T: type) []const u8 {
    return switch (@typeInfo(T)) {
        .int => "integer",
        .float => "float",
        .pointer => "pointer",
        else => "other",
    };
}

pub fn main() void {
    printAll(.{ 1, 2.5, "x" });                       // 1 2.5 x
    std.debug.print("\n", .{});
    std.debug.print("{s} {s} {s}\n", .{ describe(i32), describe(f64), describe(bool) });
    // integer float other
    std.debug.print("{d}\n", .{@sizeOf(u32)});        // 4
}
```

`anytype` 是 Zig 泛型的基础写法：参数类型留给编译器推断，函数体会为每个具体类型单独实例化，因此 `printAll(.{1, 2.5, "x"})` 里的 `inline for` 能在编译期知道元组每项的类型与个数。`@typeInfo` 返回的 `std.builtin.Type` 是带标签的联合，用 `switch` 在上面分支就能写出"按类型生成不同代码"的逻辑，这在没有模板也没有宏的语言里是最接近编译期多态的手段。Zig 刻意不提供运行期反射：`@typeName`、`@typeInfo` 都只能在编译期使用，需要"按名字访问字段"时必须用 `inline for` 遍历 `@typeInfo` 得到的字段表，代码会为每种类型单独生成。构建配置走 `build.zig` 的 `b.addOptions()` 与 `addOption`，再 `addOptions("build_options", opts)` 注入成可 `@import` 的模块，这样配置值就是编译期常量，能被常量折叠与死代码消除充分利用。

📘 [Zig · build 系统](https://ziglang.org/learn/build-system/)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有任何编译期设施，替代手段是 `load`、元表、闭包与运行期内省。选择顺序是：能用表与闭包表达的就不要用 `load`，能用元表做委托的就不要改全局环境，只有在"必须接受外部字符串形式的代码"时才用 `load`。元表是 Lua 里最优雅的"行为注入"机制。

```lua
-- 闭包与表：替代“为每种情况写一段生成代码”
local ops = {
  add = function(a, b) return a + b end,
  sub = function(a, b) return a - b end,
}
local function calc(name, a, b) return ops[name](a, b) end
print(calc("add", 1, 2), calc("sub", 5, 3))    -- 3 2

-- 元表：__index 做委托与缺省值，__call 让对象可调用
local Vec = {}
Vec.__index = Vec
Vec.__call = function(self, x, y) return Vec.new(x, y) end
function Vec.new(x, y) return setmetatable({ x = x, y = y }, Vec) end
function Vec:len2() return self.x * self.x + self.y * self.y end

local v = Vec(3, 4)                             -- 通过 __call 构造
print(v:len2())                                 -- 25

-- load：只在必须接受字符串代码时使用，务必显式给环境表
local chunk = load("return ... + ...", "adder", "t", {})
print(chunk(20, 22))                            -- 42

-- debug 库做内省（慎用，依赖调试信息）
print(debug.getinfo(Vec.new, "S").what)         -- "Lua"
```

Lua 没有泛型，也没有类型声明：所有值都是动态类型，容器是统一的 table，需要"参数化"时只有靠约定与运行期断言。`__index` 既可以是表（委托给另一个表）也可以是函数（按需计算缺省值），这两条路覆盖了"动态方法解析"与"缺省值注入"两个最常见的元编程需求；`setmetatable` 返回的是同一个表，所以惯用写法是 `setmetatable({}, T)`。`__call` 让表可以被"调用"，于是构造函数可以写成 `Vec(3, 4)`，这是 Lua 里做面向对象风格 API 的常规手法。`load` 的 `env` 参数决定代码看见哪些全局量，给一个空表加 `_G` 白名单就能做基础沙箱，但要注意不能加载不可信字节码。`debug` 库能读函数的源代码位置、上值与局部变量，是 Lua 里唯一的真内省手段，但它依赖调试信息、性能差，生产代码应尽量避免。所有这些都是运行期机制：没有编译期检查，错误只能靠测试与断言暴露。Lua 5.5 的两处语言变化也值得一并记住：`global` 已经成为关键字（进而是保留字，不能再当普通标识符用），`global x` 与 `global<const> *` 用来收紧全局变量的可见性与可写性；数值 for 与泛型 for 的控制变量都是只读（`const`）的。这两条只作用于声明与赋值规则，Lua 依然没有任何编译期代码生成能力。

📘 [Lua 5.5 · 元表](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有宏，替代手段分三层：类型体操（条件类型、映射类型、模板字面量类型）在编译期算出类型但不产生代码；装饰器在运行期包装类与方法；编译器 API 与 Babel 插件真正改写 AST。多数"想要宏"的需求落在第一层与第二层，只有需要改语法结构时才动第三层。

```typescript
// 第一层：类型体操，编译后完全消失
type DeepReadonly<T> = { readonly [K in keyof T]: DeepReadonly<T[K]> };
type PropType<T, K extends keyof T> = T[K];
type Prefix<K extends string> = `prefix_${K}`;

interface User { id: number; name: string; tags: string[] }
type Frozen = DeepReadonly<User>;
type IdType = PropType<User, "id">;      // number
type Prefixed = Prefix<"a" | "b">;        // "prefix_a" | "prefix_b"

// 第二层：装饰器是运行期函数
function tag(value: unknown, context: ClassFieldDecoratorContext) {
  return (initial: unknown) => initial;
}

class Model {
  @tag
  id: number = 0;
}

// 第三层：编译器 API / Babel 插件（示意，需要搭建构建环境）
// factory.updateSourceFile(sf, visitEachChild(sf, visitor, context))

const u: Frozen = { id: 1, name: "Ada", tags: ["x"] };
console.log(u.id, u.name);                     // 1 Ada
console.log(new Model().id);                   // 0
console.log(`${"a" satisfies Prefix<"a">}`);   // prefix_a
```

类型体操的边界很清楚：它只能在**类型层**计算，产出的是类型而不是值，也不会改变运行时代码；但它能约束 API、把错误提前到编译期，这与宏的一部分价值重叠。标准装饰器（TS 5.0 起）在运行期执行，能在类、方法、字段、访问器、参数上包装行为，但它的参数是已求值的对象，不能插入语法。真正改 AST 需要 `tsc` 之外的驱动：`ts-patch` 给 `tsc` 加载 transformer、Babel 插件、SWC 插件三者选一，其中 `ts-patch` 的版本耦合最紧、Babel 生态最全、SWC 最快但插件能力受限（TypeScript 7.0 是 Go 重写的原生编译器，官方明确它暂时不带编译器 API，要在 7.1 才提供新 API，所以依赖旧 API 的工具链在这条基线上要先确认兼容性）。代码生成（如从 OpenAPI 生成客户端）属于构建期工具链，与语言机制无关，通常由 `openapi-typescript` 这类工具直接产出 `.ts` 文件。

📘 [TypeScript · 映射类型](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有宏，替代手段按侵入性排列是：高阶函数与 `this` 绑定（零成本）、`Proxy` 与 `Reflect`（运行期拦截）、`eval` 与 `new Function`（运行期编译代码）、Babel/SWC 插件（构建期改 AST）。前两项覆盖绝大多数需求，`eval` 应当尽量避免。

```javascript
// 高阶函数与闭包：替代“为每种情况写一段代码”
const pipe = (...fns) => (x) => fns.reduce((acc, f) => f(acc), x);
const inc = (n) => n + 1;
const dbl = (n) => n * 2;
console.log(pipe(inc, dbl)(3));                   // 8

// Proxy + Reflect：运行期拦截与默认行为
const readonly = (obj) => new Proxy(obj, {
  set(t, k, v, r) { throw new TypeError(`cannot set ${String(k)}`); },
  get(t, k, r) { return Reflect.get(t, k, r); },
});
const cfg = readonly({ a: 1 });
console.log(cfg.a);                               // 1
try { cfg.a = 2; } catch (e) { console.log(e.constructor.name); }  // TypeError

// eval / new Function：字符串求值，能力最强也最危险
console.log(new Function("a", "b", "return a * b")(6, 7));         // 42

// 构建期：Babel/SWC 插件（需要用 @babel/core 才能真正运行）
// 插件通过 visitor 遍历 AST，用 @babel/types 构造替换节点
```

`pipe` 这类组合函数是 JavaScript 里最常见的"语法缺失补偿"：语言没有管道运算符，就用高阶函数把数据流表达成函数组合。`Proxy` 的 `set` 陷阱抛异常比返回 `false` 更明确，返回 `false` 只在严格模式下才抛 `TypeError`，非严格模式会静默失败。`new Function` 相比 `eval` 更安全，因为它总在全局作用域执行、看不到局部变量，CSP 环境下两者都被 `unsafe-eval` 限制。构建期变换是唯一能改变语法结构的手段，Babel 插件的 `visitor` 按节点类型注册、用 `@babel/types` 构造新节点，SWC 插件用 Rust/WASM 写、性能更好但生态更小；选哪个取决于是否需要极端构建速度，以及团队是否愿意维护 AST 层代码。要提醒的最后一点是：AST 变换必须同时产出正确的 source map，否则错误堆栈会指向错误的行。

📘 [MDN · Proxy](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Proxy)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有宏，替代手段是 attributes 加反射（元数据）、魔术方法 `__call` 与 `__get`（动态行为）、闭包与 `Closure::bind`（改变绑定与作用域）、`eval`（运行期编译代码）、以及 composer 脚本（构建期代码生成）。最该先掌握的是 `Closure::bind`，它能做到普通函数做不到的"访问私有成员"级别的元编程。

```php
<?php
class Counter {
    private int $count = 0;
    private function step(): int { return ++$this->count; }
}

// Closure::bind：把闭包绑定到某个对象与作用域，从而访问私有成员
$read = Closure::bind(fn () => $this->step(), new Counter(), Counter::class);
echo $read(), "\n";                       // 1
echo $read(), "\n";                       // 1（每次绑定的是新对象）

$c = new Counter();
$readC = Closure::bind(fn () => $this->step(), $c, Counter::class);
echo $readC(), $readC(), "\n";            // 1 2

// __call：拦截不存在的方法调用（动态代理、门面模式的基础）
class Facade {
    public function __call(string $name, array $args) {
        return "called {$name}(" . implode(',', $args) . ")";
    }
}
echo (new Facade())->anything(1, 2), "\n";   // called anything(1,2)

// eval：运行期生成代码（谨慎使用）
eval('function gen(): string { return "gen"; }');
echo gen(), "\n";                            // gen
```

PHP 没有泛型，也没有模板：数组与 `iterable` 是唯一的容器抽象，想约束元素类型只能靠文档、静态分析工具（Psalm、PHPStan）或运行期检查，这是它相比 C#/Java/Kotlin 最明显的能力缺口。`Closure::bind($closure, $newThis, $scope)` 的第三个参数决定闭包能访问哪个类的私有与受保护成员，`Closure::bindTo` 是它的对象方法形式，`static fn` 闭包不能被绑定。这个能力常被用来写测试替身、序列化器与 ORM 的内部访问器——它比反射更快也更直观，但同样绕过了封装，属于"明确知道自己在做什么"时才用的工具。`__call` 与 `__callStatic` 让对象可以响应任意方法名，`__get`/`__set`/`__isset`/`__unset` 处理不可访问的属性；PHP 8.4 的属性钩子提供了类型安全的替代方案，优先用它而不是 `__get`/`__set`。构建期代码生成走 composer 的 `scripts`（`post-install-cmd`、`post-autoload-dump`）或独立命令，生成物应当提交进仓库，避免部署环境需要额外的工具链。

📘 [PHP · Closure::bind](https://www.php.net/manual/en/functions.anonymous.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有宏，替代手段是元编程全家桶：`define_method` 批量定义方法、`method_missing` 拦截未知调用、`Module#prepend` 包装已有方法、`class_eval` 打开类、`ERB` 做构建期模板。判断顺序是：能用 `define_method` 与模块组合表达的就不要用 `method_missing`，能用 `prepend` 包装的就不要复制原方法。

```ruby
require "erb"

module Timestamped
  # prepend 让模块的方法排在原方法之前，形成环绕包装
  def save
    @saved_at = Time.now
    super
  end
  attr_reader :saved_at
end

class Record
  def save = "saved"
end
class Logged < Record
  prepend Timestamped
end

r = Logged.new
puts r.save                       # saved
puts r.saved_at.class             # Time

# define_method：用循环批量定义（块是闭包）
class Flags
  %i[debug verbose].each do |name|
    define_method(:"#{name}?") { instance_variable_get(:"@#{name}") || false }
  end
end
puts Flags.new.debug?             # false

# ERB：构建期代码生成
puts ERB.new("<%= 6 * 7 %>").result    # 42
```

Ruby 没有泛型：数组与 Hash 接受任意对象，类型约束只能靠鸭子类型约定、`RBS`/`Sorbet` 这类签名工具在静态检查层面补，运行期不做约束。`prepend` 是 Ruby 里最干净的"包装已有方法"手段：`super` 会调用被包装的原方法，不需要 `alias_method` 那套手工改名，也不会污染原来的类。`define_method` 的块是闭包，能捕获循环变量与外部局部变量，所以批量定义时每个方法可以记住自己的参数——如果用 `def` 加字符串拼方法体就得不到这个能力。`method_missing` 与 `respond_to_missing?` 必须成对实现，否则 `respond_to?`、`method`、`duck typing` 检查都会给出错误答案。构建期代码生成在 Ruby 生态里主要是 ERB 模板（Rails 的脚手架、配置文件生成）、`Rake` 任务与各类 generator，它们与语言机制无关；`eval` 只在极少数场景（元编程 DSL、动态定义类）才用，因为它运行慢、无法静态分析、还有注入风险。

📘 [Ruby · Module#prepend](https://docs.ruby-lang.org/en/master/Module.html)

{{% /tab %}}

{{< /tabpane >}}
