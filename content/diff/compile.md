+++
title = "compile"
date = 2026-09-19T09:00:00+08:00
weight = 3
type = "docs"
description = "18 种语言的编译与执行对照：执行模型、单文件编译运行命令、构建系统与依赖、编译产物、优化发布与调试"
isCJKLanguage = true
draft = false
+++

# 编译与执行：18 种语言对照

"怎么把代码跑起来"是每门语言的第一课，但 18 种语言给出的答案完全不同：Rust 先编译成机器码再运行，Python 交给解释器直接执行，Java 编译成字节码交给 JVM 的 JIT，TypeScript 先把类型擦掉再转译成 JavaScript，Ruby 边解释边可选 JIT。本页按五个主题组织：**执行模型与入口 → 单文件编译运行命令 → 构建系统与依赖管理 → 编译产物与中间表示 → 优化、发布与调试**，每个主题一套 18 语言标签页，命令都给可直接粘贴的完整写法。

## 编译与执行

**一页速览**

| 语言 | 执行模型 | 单文件运行命令 | 官方构建工具 | 典型产物 |
| --- | --- | --- | --- | --- |
| Rust | AOT（LLVM），无 VM/GC | `cargo run` / `rustc main.rs` | Cargo | 原生可执行文件 |
| Swift | AOT（LLVM）+ ARC | `swift main.swift` / `swift run` | SwiftPM / Xcode | 原生可执行文件 |
| Go | AOT（自带运行时与 GC） | `go run main.go` | go 命令（modules） | 单一静态二进制 |
| Python | 解释执行（字节码 VM）+ 实验 JIT | `python3 main.py` | pip / uv / poetry | `.pyc` 字节码缓存 |
| Kotlin | 编译到 JVM 字节码，JVM JIT；也可编译原生/Wasm/JS | `kotlin main.kts` / `java -jar` | Gradle / Maven | `.jar`、`.kexe`、`.wasm` |
| Java | 编译到字节码，JVM JIT（+ AOT 缓存） | `java Main.java` | Maven / Gradle | `.class`、`.jar` |
| C++ | AOT（LLVM/GCC）+ 链接 | `g++ -std=c++23 main.cpp && ./a.out` | CMake / Make / Meson | `.o`、`.a`、可执行文件 |
| C | AOT + 链接 | `gcc -std=c23 main.c && ./a.out` | Make / CMake / Meson | `.o`、`.a`、可执行文件 |
| Julia | JIT（LLVM，按需特化）+ `juliac` 可编译独立可执行文件 | `julia main.jl` | Pkg | 预编译缓存 `.ji`、sysimage、`juliac` 产物 |
| C# | 编译到 IL，.NET JIT；可 ReadyToRun / Native AOT | `dotnet run app.cs` | MSBuild / dotnet CLI | `.dll`、`.exe`、原生 AOT 文件 |
| Dart | Kernel IR → JIT（开发）或 AOT（发布） | `dart run main.dart` | pub | 原生可执行、`.js`、`.wasm` |
| R | 解释执行 + 字节码 JIT | `Rscript main.R` | R CMD / renv | 源码或 `.tar.gz` 包、`.rds` |
| Zig | AOT（LLVM/自研后端），无 GC | `zig run main.zig` | `zig build` | 可执行、`.a`、`.so`、`.o` |
| Lua | 解释执行（编译成字节码后由 VM 执行） | `lua main.lua` | LuaRocks | `.luac` 字节码、C 模块 |
| TypeScript | 类型检查 + 转译到 JS（TS 7 为原生编译器） | `npx tsc` 后 `node main.js`；Node 26 可直接 `node main.ts` | npm / pnpm / yarn + tsconfig | `.js`、`.d.ts`、source map |
| JavaScript | 引擎解释 + JIT（V8） | `node main.js` | npm / pnpm / yarn | `.js`、bundle、SEA 可执行文件 |
| PHP | Zend VM 解释执行 opcode（OPcache + JIT 可选） | `php main.php` | Composer | `.phar`、OPcache 缓存 |
| Ruby | YARV 字节码解释执行 + YJIT/ZJIT | `ruby main.rb` | Bundler / RubyGems | gem、`RubyVM::InstructionSequence` 字节码 |

### 执行模型与入口

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 是**提前编译（AOT）**语言：`rustc` 通过 LLVM 直接把源码编译成目标平台的机器码，产物是原生可执行文件；没有虚拟机、没有垃圾回收，运行时只有标准库与少量启动代码。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | AOT（LLVM 后端），无 VM、无 GC |
| 入口 | `fn main()`（二进制 crate）；库 crate 无入口 |
| 编译命令 | `rustc main.rs -o app`；项目里用 `cargo build` |
| 运行方式 | `./app`；项目里 `cargo run` |

```rust
fn main() {
    println!("hello from rust");
}
```

因为是 AOT，编译期就完成了类型检查、单态化与优化，运行时不带编译器；默认的 debug 构建会保留调试信息与溢出检查，release 构建才做完整优化。Rust 没有"启动虚拟机"这一步，所以启动时间与 C 程序在同一量级。

📘 [The Cargo Book](https://doc.rust-lang.org/cargo/)、[rustc 手册](https://doc.rust-lang.org/rustc/)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的主线也是 **AOT**：`swiftc` 用 LLVM 编译成机器码，对象生命周期由 ARC 管理。但 `swift` 命令本身可以在"解释/JIT"模式下直接跑一个脚本文件，适合写小工具。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | AOT（LLVM）+ ARC 引用计数 |
| 入口 | `main.swift` 顶层代码，或 `@main` 标注的类型 |
| 编译命令 | `swiftc main.swift -o app` |
| 运行方式 | `swift main.swift`（脚本模式）；`./app` |

```swift
// main.swift
print("hello from swift")
```

`swift main.swift` 走的是前端解释执行（`swift-frontend -interpret`），启动快但性能不是编译产物的水平；正式发布用 `swiftc -O` 或 SwiftPM 的 `swift build -c release`。SwiftPM 会把 `main.swift` 识别为可执行目标入口，而 `@main` 写法适合多文件项目。

📘 [Swift.org · SwiftPM](https://www.swift.org/documentation/package-manager/)、[swiftc 文档](https://www.swift.org/documentation/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 是 **AOT** 语言，但和 C 不同：编译器会把**运行时**（调度器、GC、栈管理）一起链进二进制，所以产物是"自带运行时"的单个可执行文件，没有虚拟机、也不需要额外安装依赖。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | AOT，自带运行时与 GC |
| 入口 | `package main` 里的 `func main()` |
| 编译命令 | `go build -o app .` |
| 运行方式 | `./app`；开发期 `go run main.go` |

```go
package main

import "fmt"

func main() {
    fmt.Println("hello from go")
}
```

`go run` 在临时目录里编译再执行，适合开发；`go build` 生成可分发二进制。默认情况下（不依赖 cgo）产物是静态链接的，所以交叉编译只要改 `GOOS`/`GOARCH` 环境变量即可，这也是 Go 发布体验好的原因。

📘 [Go 官方文档 · go 命令](https://go.dev/cmd/go/)、[Go 交叉编译](https://go.dev/doc/install/source#environment)

{{% /tab %}}

{{% tab header="Python" %}}

Python 是**解释执行**：`python` 先把源码编译成字节码（`.pyc`），再由 CPython 虚拟机执行——所以严格说 Python"有编译步骤，只是自动且透明"。Python 3.14 起官方二进制还包含实验性的 JIT（`PYTHON_JIT=1` 开启），并把 free-threaded 模式（PEP 779）列为正式支持。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | 解释执行（字节码 VM），可选实验 JIT |
| 入口 | 模块顶层代码；`if __name__ == "__main__":` 是约定 |
| "编译"命令 | 无（自动生成 `__pycache__/*.pyc`） |
| 运行方式 | `python3 main.py`、`python3 -m package`、`python3 -c "..."` |

```python
def main() -> None:
    print("hello from python")

if __name__ == "__main__":
    main()
```

因为是解释执行，Python 的启动时间主要花在"导入模块 + 编译字节码"上，`python -X importtime` 可以看清导入开销；`-O`/`-OO` 会去掉断言与文档字符串，`PYTHON_JIT=1` 在 3.14 的官方构建里启用实验 JIT。

📘 [Python 3.14 What's New](https://docs.python.org/3.14/whatsnew/3.14.html)、[使用 Python](https://docs.python.org/3/using/index.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的主线是**编译到 JVM 字节码**（K2 编译器），由 JVM 的 JIT 执行；同一套语言还能编译到原生（Kotlin/Native，LLVM AOT）、WebAssembly 与 JavaScript。所以"Kotlin 怎么运行"取决于目标平台。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | JVM 字节码 + JIT；或 Kotlin/Native 的 AOT；或 JS/Wasm |
| 入口 | JVM 上是 `fun main()` |
| 编译命令 | `kotlinc main.kt -include-runtime -d app.jar` |
| 运行方式 | `java -jar app.jar`；脚本用 `kotlin main.kts` |

```kotlin
fun main() {
    println("hello from kotlin")
}
```

JVM 路线和 Java 一样要经过"编译 → 加载 → JIT 预热"；Kotlin/Native 则直接产出可执行文件（`linkReleaseExecutable*` 任务），启动快、适合 CLI 与移动端；Kotlin/Wasm 用于浏览器，产物是 `.wasm`。

📘 [Kotlin 文档 · Gradle](https://kotlinlang.org/docs/gradle.html)、[Kotlin/Native](https://kotlinlang.org/docs/native-overview.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 是"编译到字节码 + JVM 执行"的经典模型：`javac` 生成与平台无关的 `.class`，JVM 加载后用 HotSpot 的 C1/C2 JIT 把热点代码编译成机器码。JDK 24/25 又加了 AOT 类加载与方法画像（JEP 483/514/515），用来缩短启动时间。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | 字节码 + JVM JIT（HotSpot），可选 AOT 缓存 |
| 入口 | `public static void main(String[])`；JDK 25 起可用紧凑源文件省略类声明 |
| 编译命令 | `javac -d out src/Main.java` |
| 运行方式 | `java -cp out Main`；单文件 `java Main.java` |

```java
void main() {                       // JDK 25+ 的紧凑源文件写法
    System.out.println("hello from java");
}
```

`java Main.java` 是"源码模式"：JVM 在内存里编译并执行，适合单文件脚本；正式构建仍走 `javac` + `jar`。AOT 缓存（`-XX:AOTCache`）把类加载与链接结果存下来，能显著改善小工具、CLI 的启动时间。

📘 [Java SE 25 · java 命令](https://docs.oracle.com/en/java/javase/25/docs/specs/man/java.html)、[JEP 483](https://openjdk.org/jeps/483)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 是纯 **AOT**：编译每个翻译单元得到目标文件，再由链接器合并成可执行文件或库。没有虚拟机、没有 GC（RAII 负责资源），但需要处理头文件、模板实例化与 ABI。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | AOT（LLVM/GCC）→ 目标文件 → 链接 |
| 入口 | `int main(int argc, char** argv)` |
| 编译命令 | `g++ -std=c++23 -O2 main.cpp -o app` |
| 运行方式 | `./app` |

```cpp
#include <print>

int main() {
    std::println("hello from c++");
}
```

C++20 起也可以用模块（`import std;`）替代头文件，但主流工具链的模块支持仍在完善，跨编译器项目通常还是 `#include`。编译慢是模板与头文件模型的固有代价，预编译头（PCH）和 CMake 的 `target_precompile_headers` 能缓解。

📘 [cppreference · 编译器支持](https://en.cppreference.com/w/cpp/compiler_support)、[CMake 文档](https://cmake.org/documentation/)

{{% /tab %}}

{{% tab header="C" %}}

C 是 AOT 的鼻祖：预处理 → 编译 → 汇编 → 链接四步走，产物是目标文件与可执行文件。没有运行时（除 libc），也没有 GC。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | AOT → `.o` → 链接 libc |
| 入口 | `int main(int argc, char** argv)` |
| 编译命令 | `gcc -std=c23 -O2 main.c -o app` |
| 运行方式 | `./app` |

```c
#include <stdio.h>

int main(void) {
    puts("hello from c");
    return 0;
}
```

四个阶段可以单独执行：`gcc -E`（只预处理）、`-S`（输出汇编）、`-c`（输出目标文件）、默认动作是链接。链接顺序与库的 ABI 是 C 项目最常见的坑。

📘 [GCC 手册](https://gcc.gnu.org/onlinedocs/gcc/)、[Clang 文档](https://clang.llvm.org/docs/)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 是**按需 JIT**：函数在第一次用具体类型调用时，由 LLVM 编译出这个类型组合的专用机器码。没有传统的"编译整个程序"步骤，但 Julia 1.12/1.13 提供了 `juliac`（JuliaC.jl），可以把程序编译成独立可执行文件或库。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | JIT（LLVM，按调用特化）；`juliac` 可做 AOT |
| 入口 | 脚本顶层代码；约定 `function main()` 后调用 |
| 编译命令 | 一般不需要；发布用 `juliac` |
| 运行方式 | `julia main.jl`、`julia -e 'println("hi")'`、REPL |

```julia
function main()
    println("hello from julia")
end

main()
```

JIT 的代价是"首次调用编译"（TTFX）：包会做预编译（`.ji` 缓存 + pkgimage），但新类型组合仍要在运行时编译。`PackageCompiler.jl` 可以做成 sysimage 或独立 app，1.13 起 `juliac` 成为官方路径。

📘 [Julia 1.13 Highlights](https://julialang.org/blog/2026/09/julia-1.13-highlights/)、[PackageCompiler.jl](https://julialang.github.io/PackageCompiler.jl/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 编译成 IL（中间语言）程序集，由 .NET 运行时 JIT（RyuJIT）执行；.NET 10 还支持 ReadyToRun 预编译、Native AOT（`PublishAot`）和"文件级应用"（`dotnet run app.cs`），把脚本体验和 AOT 都补齐了。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | IL + JIT；可选 ReadyToRun / Native AOT |
| 入口 | `Main` 方法或顶级语句 |
| 编译命令 | `dotnet build -c Release` |
| 运行方式 | `dotnet run`；文件级应用 `dotnet run app.cs` |

```csharp
// app.cs（.NET 10 文件级应用，可加 #:package 指令）
Console.WriteLine("hello from c#");
```

文件级应用让单文件 C# 脚本不用建项目；正式发布用 `dotnet publish -c Release`（自包含、单文件、裁剪）或 `PublishAot=true` 直接产出原生可执行文件（启动更快、体积更小，但反射受限）。

📘 [.NET 10 新增功能](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview)、[Native AOT](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的执行分两条路：开发时用 `dart run`（编译到 Kernel IR 后 JIT，支持热重载），发布时用 `dart compile exe` 编译成**AOT 原生可执行文件**；Web 目标则编译成 JavaScript 或 WebAssembly。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | Kernel IR → JIT（开发）/ AOT（发布）/ JS / Wasm |
| 入口 | `void main()` |
| 编译命令 | `dart compile exe main.dart -o app` |
| 运行方式 | `dart run main.dart`；`./app` |

```dart
void main() {
    print('hello from dart');
}
```

`dart compile exe` 的产物自带 Dart 运行时，不需要目标机器装 Dart；`dart compile js` 用 dart2js 做 tree shaking 与优化（`-O2`/`-O4`），`dart compile wasm` 产出 `.wasm`。

📘 [dart compile](https://dart.dev/tools/dart-compile)、[Dart 概览](https://dart.dev/overview)

{{% /tab %}}

{{% tab header="R" %}}

R 是解释型语言：源码被解析成表达式树，再由解释器执行；函数在首次调用时会被**字节码编译器**（JIT）编译成字节码，从而加快后续调用。R 没有独立的编译步骤。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | 解释执行 + 字节码 JIT |
| 入口 | 脚本顶层代码；包可以没有"入口" |
| 编译命令 | 无（`R CMD INSTALL --byte-compile` 可预编译包） |
| 运行方式 | `Rscript main.R`、`R -e '...'`、REPL |

```r
main <- function() {
  cat("hello from R\n")
}

main()
```

脚本用 `Rscript` 跑（无交互、适合自动化），交互探索用 `R`；`Rscript -e` 适合一行命令。性能敏感的函数可以用 `compiler::cmpfun()` 强制字节码编译，或把热点下沉到 C/C++（Rcpp）。

📘 [R 官方文档](https://cran.r-project.org/manuals.html)、[R CMD check](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 是 AOT 编译语言，默认用自研后端 + LLVM；它把"编译期执行"做成了语言核心（`comptime`），而且交叉编译只需要一个 `-target` 参数——不需要目标平台的 SDK。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | AOT（自研后端/LLVM），无 GC |
| 入口 | `pub fn main() !void`（或 `void`） |
| 编译命令 | `zig build-exe main.zig` |
| 运行方式 | `./main`；开发期 `zig run main.zig` |

```zig
const std = @import("std");

pub fn main() !void {
    std.debug.print("hello from zig\n", .{});
}
```

`zig run` = 编译 + 运行；`zig build-exe` 只产出文件。Zig 还充当 C/C++ 交叉编译器（`zig cc`、`zig c++`），这是它最实用的能力之一。

📘 [Zig 语言参考](https://ziglang.org/documentation/master/)、[zig build 系统](https://ziglang.org/documentation/master/#Zig-Build-System)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 是解释型语言：加载源码时先编译成字节码，再由 Lua 虚拟机执行。没有 AOT 编译步骤，但可以把字节码预编译成 `.luac` 文件（加载更快，也用于保护源码）。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | 解释执行（源码 → 字节码 → VM） |
| 入口 | 脚本顶层代码；`return` 结束 |
| 编译命令 | `luac -o out.luac main.lua` |
| 运行方式 | `lua main.lua`、`lua -e 'print("hi")'`、REPL |

```lua
local function main()
  print("hello from lua")
end

main()
```

`lua` 命令每次启动都会重新编译源码；`luac` 预编译可以把这一步省掉（`lua out.luac` 直接跑字节码）。需要更高性能时可以换 LuaJIT，它会跟踪热点路径并 JIT 编译。

📘 [Lua 5.5 手册](https://www.lua.org/manual/5.5/)、[LuaJIT](https://luajit.org/)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 不是"编译成机器码"，而是**类型检查 + 转译**：类型在编译期被擦除，产物是 JavaScript（或声明文件）。TypeScript 7 的编译器是从零重写的原生实现，官方称全量构建快 8~12 倍，命令仍然是 `tsc`。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | 类型检查 + 转译到 JS（类型全部擦除） |
| 入口 | 生成的 JS 由引擎决定（Node 常看 `main` 字段） |
| 编译命令 | `npx tsc`（配合 `tsconfig.json`） |
| 运行方式 | `node main.js`；Node 26 可直接 `node main.ts` |

```ts
function main(): void {
  console.log("hello from typescript");
}
main();
```

两条常见路线：`tsc` 只做转译（类型检查用 `--noEmit`），打包交给 esbuild/Vite/webpack；或者干脆不预编译，交给 Node 26 的**类型剥离**直接运行 `.ts`（要求代码是"可擦除语法"，配 `erasableSyntaxOnly` 最稳）。

📘 [TypeScript 7 发布说明](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)、[Node.js · TypeScript 支持](https://nodejs.org/api/typescript.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有编译步骤：源码交给 JS 引擎（V8、JavaScriptCore 等），引擎先解析成字节码（V8 的 Ignition），热点函数再被 JIT 编译（TurboFan）。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | 解析 → 字节码 → JIT（V8） |
| 入口 | 脚本顶层代码；Node 的模块入口 |
| 编译命令 | 无；打包/压缩是可选步骤 |
| 运行方式 | `node main.js`、`node -e '...'`、REPL |

```js
function main() {
  console.log("hello from javascript");
}
main();
```

没有编译期类型检查，所以"编译错误"基本都要到运行时才暴露（可以先用 `node --check` 做语法检查）。生产环境通常会做打包与压缩（esbuild/webpack），Node 还支持 SEA（单文件可执行程序）把脚本变成可分发二进制。

📘 [Node.js 文档](https://nodejs.org/api/)、[V8 文档](https://v8.dev/docs)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 是解释型：每个请求把源码编译成 opcode，再由 Zend 虚拟机执行；开启 OPcache 后 opcode 会被缓存（避免重复编译），PHP 8 还提供 JIT（`opcache.jit`）加速热点代码。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | Zend VM 解释 opcode；OPcache + 可选 JIT |
| 入口 | 脚本顶层代码；Web 场景由 FPM/Apache 调用 |
| 编译命令 | 无；`php -l` 只做语法检查 |
| 运行方式 | `php main.php`；内置服务器 `php -S localhost:8000` |

```php
<?php
function main(): void {
    echo "hello from php\n";
}

main();
```

CLI 脚本用 `php main.php`，本地起服务用 `php -S`（不用装 Nginx/Apache）。生产环境的性能主要看 OPcache 配置：`opcache.enable=1`、`opcache.validate_timestamps=0`、按需开启 `opcache.jit=tracing`。

📘 [PHP 手册 · OPcache](https://www.php.net/manual/en/book.opcache.php)、[PHP 8.5 发布说明](https://www.php.net/releases/8.5/en.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 是解释型：源码先编译成 YARV 字节码再执行；Ruby 3.1 起有 YJIT（进程内 JIT），Ruby 4.0 还提供实验性的 ZJIT（方法级 JIT）。是否启用由命令行或环境变量决定。

| 项目 | 内容 |
| --- | --- |
| 执行模型 | YARV 字节码解释 + 可选 YJIT/ZJIT |
| 入口 | 脚本顶层代码；`if __FILE__ == $0` 是约定 |
| 编译命令 | 无；`ruby -c main.rb` 只做语法检查 |
| 运行方式 | `ruby main.rb`、`irb`、`ruby --yjit main.rb` |

```ruby
def main
  puts "hello from ruby"
end

main if __FILE__ == $0
```

启用 JIT：`ruby --yjit main.rb`（或环境变量 `RUBY_YJIT_ENABLE=1`）、`--zjit`；YJIT 对长时间运行的进程收益最大（Rails、Sidekiq），短脚本反而可能变慢。

📘 [Ruby 官方文档](https://docs.ruby-lang.org/en/master/)、[YJIT](https://docs.ruby-lang.org/en/master/RubyVM/YJIT.html)

{{% /tab %}}

{{< /tabpane >}}

### 编译与运行命令

这一节只讲"一个文件怎么跑起来"，命令都按可直接粘贴的形式给出；项目级的构建留给下一节。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

单文件用 `rustc` 直接编译；一旦有多文件或依赖，就应该用 `cargo`。

| 场景 | 命令 |
| --- | --- |
| 编译单文件 | `rustc main.rs -o app` |
| 编译并优化 | `rustc -O --edition 2024 main.rs -o app` |
| 只做类型检查 | `rustc --emit=metadata main.rs` |
| 运行 | `./app` |
| 新建项目 | `cargo new demo && cd demo && cargo run` |
| 发布构建 | `cargo build --release` → `target/release/demo` |

```bash
rustc --edition 2024 -O main.rs -o app
./app
# 项目方式
cargo new demo && cd demo
cargo run                 # 开发（debug）
cargo run --release       # 发布（优化）
cargo check               # 只检查，不产出二进制（最快）
```

`rustc` 适合单文件与学习；`cargo check` 是日常迭代里最常用的命令——它跳过代码生成，只做类型与借用检查，因此比 `cargo build` 快得多。编译产物在 `target/debug` 或 `target/release`。

📘 [Cargo 命令参考](https://doc.rust-lang.org/cargo/commands/index.html)

{{% /tab %}}

{{% tab header="Swift" %}}

| 场景 | 命令 |
| --- | --- |
| 直接运行脚本 | `swift main.swift` |
| 编译可执行文件 | `swiftc main.swift -o app` |
| 发布优化 | `swiftc -O -whole-module-optimization main.swift -o app` |
| 新建项目 | `swift package init --type executable` |
| 项目构建/运行 | `swift build -c release`、`swift run` |

```bash
swift main.swift                       # 解释执行，适合脚本
swiftc -O main.swift -o app && ./app    # 编译成原生可执行文件

swift package init --type executable    # 生成 Package.swift 与 Sources/
swift build -c release                  # 产物在 .build/release/
swift run                               # 编译并运行
```

`swift` 与 `swiftc` 的区别很关键：前者是"前端解释执行"（启动快、无独立产物），后者是真正的 AOT 编译。多文件项目一律用 SwiftPM，它负责依赖解析（`Package.resolved`）与跨平台构建。

📘 [SwiftPM 文档](https://www.swift.org/documentation/package-manager/)

{{% /tab %}}

{{% tab header="Go" %}}

| 场景 | 命令 |
| --- | --- |
| 直接运行 | `go run main.go` |
| 编译 | `go build -o app .` |
| 去符号（更小） | `go build -ldflags="-s -w" -o app .` |
| 交叉编译 | `GOOS=linux GOARCH=amd64 go build -o app .` |
| 测试 | `go test ./...` |

```bash
go mod init example.com/demo     # 初始化模块（生成 go.mod）
go run main.go                   # 临时编译并运行
go build -o app .                # 生成二进制
./app

GOOS=windows GOARCH=amd64 go build -o app.exe .   # 一条命令交叉编译
go test -race ./...                                # 竞态检测
```

`go run` 适合开发，`go build` 产出可分发文件；`-ldflags="-s -w"` 去掉符号表与调试信息，能显著减小体积。默认静态链接让交叉编译不需要额外工具链，`CGO_ENABLED=0` 可以强制纯静态。

📘 [go 命令文档](https://go.dev/cmd/go/)

{{% /tab %}}

{{% tab header="Python" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `python3 main.py` |
| 运行模块 | `python3 -m mypackage` |
| 一行代码 | `python3 -c "print('hi')"` |
| 优化模式 | `python3 -O main.py`（去断言）、`-OO`（再去文档字符串） |
| 预编译字节码 | `python3 -m compileall .` |

```bash
python3 main.py
python3 -m venv .venv && source .venv/bin/activate   # 虚拟环境
python3 -m pip install -r requirements.txt

python3 -O main.py            # __debug__ 变为 False，断言被移除
python3 -m compileall .        # 生成 __pycache__/*.pyc
python3 -X importtime main.py  # 看导入耗时
```

Python 没有"编译命令"，但 `compileall` 可以提前生成 `.pyc`（部署时常用），`-O`/`-OO` 会改变运行语义。3.13+ 的 free-threaded 构建（`python3.14t`）与 3.14 的实验 JIT（`PYTHON_JIT=1`）是性能相关的新选项。

📘 [Python 命令行与环境变量](https://docs.python.org/3/using/cmdline.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 场景 | 命令 |
| --- | --- |
| 编译成 JAR | `kotlinc main.kt -include-runtime -d app.jar` |
| 运行 JAR | `java -jar app.jar` |
| 跑脚本 | `kotlin main.kts` |
| 项目构建 | `./gradlew build`、`./gradlew run` |
| 测试 | `./gradlew test` |

```bash
kotlinc main.kt -include-runtime -d app.jar   # 单文件 → 可执行 JAR
java -jar app.jar

kotlin script.kts                              # .kts 脚本直接运行

gradle init --type kotlin-application          # 生成 Gradle 项目
./gradlew run                                  # 运行
./gradlew build                                # 构建（含测试）
```

`kotlinc -include-runtime` 会把 Kotlin 标准库打进 JAR，换来的是更大的体积；更正式的做法是用 Gradle 的 `application` 插件生成启动脚本与分发包。Kotlin/Native 项目用 `./gradlew linkReleaseExecutable<目标>` 产出原生可执行文件。

📘 [Kotlin 文档 · 命令行编译器](https://kotlinlang.org/docs/command-line.html)

{{% /tab %}}

{{% tab header="Java" %}}

| 场景 | 命令 |
| --- | --- |
| 编译 | `javac -d out src/Main.java` |
| 运行 | `java -cp out Main` |
| 单文件源码模式 | `java Main.java`（不用先 javac） |
| 打成 JAR | `jar --create --file app.jar --main-class Main -C out .` |
| 交互 | `jshell` |

```bash
javac -d out src/Main.java
java -cp out Main

java Main.java                 # 源码模式：JVM 内部编译并运行

jar --create --file app.jar --main-class Main -C out .
java -jar app.jar

javac --release 25 -d out src/Main.java   # 按指定 Java 版本编译
```

`javac --release N` 保证生成的字节码兼容目标版本，是发布时最该记住的选项；`-cp`/`-classpath` 指定类路径，`-Xmx` 等 JVM 参数要写在 `java` 之后、主类之前。

📘 [javac 手册](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javac.html)、[java 手册](https://docs.oracle.com/en/java/javase/25/docs/specs/man/java.html)

{{% /tab %}}

{{% tab header="C++" %}}

| 场景 | 命令 |
| --- | --- |
| 编译并优化 | `g++ -std=c++23 -O2 -Wall -Wextra main.cpp -o app` |
| Clang 版本 | `clang++ -std=c++23 -O2 main.cpp -o app` |
| 带消毒器 | `clang++ -g -fsanitize=address,undefined main.cpp -o app` |
| 只编译成目标文件 | `g++ -c main.cpp -o main.o` |
| 链接多个目标文件 | `g++ main.o util.o -o app` |

```bash
g++ -std=c++23 -O2 -Wall -Wextra main.cpp -o app
./app

clang++ -std=c++23 -O2 -flto main.cpp -o app     # LTO 链接期优化
clang++ -g -O1 -fsanitize=address,undefined main.cpp -o app   # 调试 + 消毒器
```

编译器与标准库版本要匹配（`g++`/`libstdc++`、`clang++`/`libc++`）；C++23 特性在 GCC 13+、Clang 17+ 上基本可用。日常开发建议常开 `-Wall -Wextra`，发布时再叠加 `-O2 -DNDEBUG -flto`。

📘 [GCC 选项](https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html)、[Clang 命令行](https://clang.llvm.org/docs/CommandGuide/clang.html)

{{% /tab %}}

{{% tab header="C" %}}

| 场景 | 命令 |
| --- | --- |
| 编译并优化 | `gcc -std=c23 -O2 -Wall -Wextra main.c -o app` |
| Clang 版本 | `clang -std=c23 -O2 main.c -o app` |
| 只要目标文件 | `gcc -c main.c -o main.o` |
| 只要汇编 | `gcc -S main.c` |
| 只要预处理结果 | `gcc -E main.c` |

```bash
gcc -std=c23 -O2 -Wall -Wextra main.c -o app
./app

gcc -std=c23 -c main.c util.c          # 分别编译成 .o
gcc main.o util.o -lm -o app           # 链接（注意 -l 的顺序）
```

C23 的关键字（`bool`、`true`、`nullptr`、`typeof`、`constexpr`）需要 `-std=c23`；老代码常加 `-std=gnu17` 之类保持兼容。链接时库的顺序很重要：被依赖的库要放在后面（`-lm` 放最后）。

📘 [GCC 手册](https://gcc.gnu.org/onlinedocs/gcc/)、[Clang 文档](https://clang.llvm.org/docs/)

{{% /tab %}}

{{% tab header="Julia" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `julia main.jl` |
| 一行代码 | `julia -e 'println("hi")'` |
| 指定项目环境 | `julia --project=. main.jl` |
| 安装依赖 | `julia --project=. -e 'using Pkg; Pkg.instantiate()'` |
| 编译独立可执行文件 | `juliac`（JuliaC.jl，1.12+） |

```bash
julia main.jl
julia -e 'println(sum(1:10))'

julia --project=. -e 'using Pkg; Pkg.instantiate()'   # 按 Manifest.toml 装依赖
julia --project=. main.jl

julia --threads=auto main.jl        # 多线程
julia -O3 main.jl                    # 提高优化等级（默认 -O2）
```

Julia 的命令行参数决定优化等级、线程数、是否加载 startup 文件（`--startup-file=no` 常用于 CI）。要发布"双击就能跑"的程序，用 `juliac` 或 `PackageCompiler.jl` 生成独立可执行文件/sysimage，否则用户机器上必须有 Julia。

📘 [Julia 命令行选项](https://docs.julialang.org/en/v1/manual/command-line-options/)、[JuliaC.jl](https://github.com/JuliaLang/JuliaC.jl)

{{% /tab %}}

{{% tab header="C#" %}}

| 场景 | 命令 |
| --- | --- |
| 文件级应用（.NET 10） | `dotnet run app.cs` |
| 新建项目 | `dotnet new console -o demo` |
| 运行项目 | `dotnet run --project demo` |
| 发布 | `dotnet publish -c Release -o out` |
| 单文件 / AOT | `dotnet publish -c Release -r osx-arm64 --self-contained`（加 `-p:PublishAot=true` 走 AOT） |

```bash
dotnet run app.cs                     # 单文件脚本（.NET 10 文件级应用）

dotnet new console -o demo && cd demo
dotnet run                            # 开发运行
dotnet publish -c Release -o out      # 发布（依赖目标机器有 .NET）

dotnet publish -c Release -r linux-x64 --self-contained -p:PublishSingleFile=true
dotnet publish -c Release -r linux-x64 -p:PublishAot=true     # Native AOT
```

文件级应用适合脚本与原型（可以用 `#:package` 指令直接引 NuGet 包）；正式项目仍走 `.csproj`。发布时四个开关最常用：`--self-contained`（自带运行时）、`PublishSingleFile`（单文件）、`PublishTrimmed`（裁剪）、`PublishAot`（原生 AOT）。

📘 [dotnet publish](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish)、[文件级应用](https://learn.microsoft.com/en-us/dotnet/csharp/tutorials/file-based-programs)

{{% /tab %}}

{{% tab header="Dart" %}}

| 场景 | 命令 |
| --- | --- |
| 运行（JIT） | `dart run main.dart` |
| 编译原生可执行 | `dart compile exe main.dart -o app` |
| 编译到 JS | `dart compile js main.dart -o out/main.js` |
| 编译到 Wasm | `dart compile wasm main.dart` |
| 依赖与检查 | `dart pub get`、`dart analyze`、`dart test` |

```bash
dart run main.dart                       # 开发：JIT，可配合热重载
dart compile exe main.dart -o app         # 发布：AOT 原生可执行
./app

dart compile js -O2 main.dart -o out/main.js   # Web（dart2js）
dart pub get && dart analyze               # 拉依赖 + 静态检查
```

`dart compile exe` 产物自带运行时，目标机器不需要装 Dart；`dart compile js` 会做 tree shaking 并按 `-O` 级别优化（`-O2` 平衡、`-O4` 最激进）。Flutter 项目则用 `flutter build apk|ipa|web`。

📘 [dart compile](https://dart.dev/tools/dart-compile)

{{% /tab %}}

{{% tab header="R" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `Rscript main.R` |
| 一行代码 | `Rscript -e 'cat("hi\n")'` |
| 交互会话 | `R` |
| 输出到文件 | `R CMD BATCH main.R out.txt` |
| 安装/检查包 | `R CMD INSTALL`、`R CMD check` |

```bash
Rscript main.R
Rscript -e 'print(sum(1:10))'

R CMD build mypkg && R CMD check mypkg_0.1.0.tar.gz   # 打包 + 检查
R CMD INSTALL mypkg                                   # 本地安装
Rscript -e 'renv::restore()'                           # 按 renv.lock 还原依赖
```

`Rscript` 是非交互执行、CI 与定时任务的标准入口；`R CMD BATCH` 会把输入和输出都写进文件，调试老脚本时会见到。包开发的三件套是 `build`/`check`/`INSTALL`，依赖锁定常用 `renv`。

📘 [R 手册 · R CMD](https://cran.r-project.org/manuals.html)

{{% /tab %}}

{{% tab header="Zig" %}}

| 场景 | 命令 |
| --- | --- |
| 编译并运行 | `zig run main.zig` |
| 编译可执行文件 | `zig build-exe main.zig` |
| 项目构建 | `zig build`（读 `build.zig`） |
| 测试 | `zig test main.zig` |
| 指定优化等级 | `zig build-exe -O ReleaseFast main.zig` |

```bash
zig run main.zig                       # 编译 + 立即运行
zig build-exe main.zig                 # 生成 ./main
./main

zig build-exe -O ReleaseFast -fstrip main.zig   # 优化 + 去符号
zig build -Doptimize=ReleaseSafe                 # 项目级构建
zig test main.zig                                 # 运行测试
```

Zig 的四个优化等级是 `Debug`（默认）、`ReleaseSafe`（保留安全检查）、`ReleaseFast`（关掉安全检查换性能）、`ReleaseSmall`（体积优先）。`ReleaseFast` 下整数溢出等行为会变成未定义，所以只用在自己确定安全的地方。

📘 [Zig 语言参考 · 构建模式](https://ziglang.org/documentation/master/#Build-Mode)

{{% /tab %}}

{{% tab header="Lua" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `lua main.lua` |
| 一行代码 | `lua -e 'print("hi")'` |
| 交互模式 | `lua -i` |
| 预编译字节码 | `luac -o main.luac main.lua` |
| 运行字节码 | `lua main.luac` |

```bash
lua main.lua
lua -e 'print(("hello"):upper())'

luac -o main.luac main.lua     # 预编译
lua main.luac                   # 直接跑字节码（跳过解析与编译）
luac -l main.luac               # 反汇编字节码（调试用）
```

`.luac` 有两个用途：加快启动（省去编译）与保护源码（不易直接读）。注意字节码与 Lua 版本绑定（5.5 的字节码在 5.4 上不能跑），跨版本分发仍应带源码。

📘 [Lua 5.5 手册](https://www.lua.org/manual/5.5/)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 场景 | 命令 |
| --- | --- |
| 编译 | `npx tsc main.ts` → `main.js` |
| 只做类型检查 | `npx tsc --noEmit` |
| 监听模式 | `npx tsc --watch` |
| 直接运行（第三方） | `npx tsx main.ts` |
| 直接运行（Node 26） | `node main.ts` |

```bash
npx tsc main.ts                 # 输出 main.js
node main.js

npx tsc --noEmit                # 只检查类型，常用于 CI
npx tsc --init                  # 生成 tsconfig.json

node main.ts                    # Node 26：类型剥离，直接跑 .ts
npx tsx main.ts                 # 或用 tsx/ts-node 做完整转换
```

Node 26 的 `.ts` 支持是"类型剥离"：只擦掉类型注解，不做类型检查，也不支持 `enum`/`namespace` 这类需要生成代码的语法（配 `erasableSyntaxOnly` 能提前发现）。要完整语义就用 `tsc` 或 `tsx`。

📘 [TypeScript 7 发布说明](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)、[Node.js · TypeScript](https://nodejs.org/api/typescript.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `node main.js` |
| 一行代码 | `node -e 'console.log(1)'` |
| 语法检查 | `node --check main.js` |
| 监听变化 | `node --watch main.js` |
| 通过 npm 脚本 | `npm run start` |

```bash
node main.js
node --check main.js          # 只做语法检查，不执行
node --watch main.js          # 文件变化自动重启（Node 18.11+）

npm init -y && npm run start   # package.json 里的 scripts.start
node --experimental-sea-config sea-config.json   # 生成单文件可执行程序
```

JavaScript 没有"编译"这一步，最常见的"编译问题"其实是模块格式：`.mjs`/`"type": "module"` 是 ESM，`.cjs` 是 CommonJS，`require` 与 `import` 不能随意混用（Node 26 支持在 ESM 里 `require` 部分场景）。

📘 [Node.js CLI 文档](https://nodejs.org/api/cli.html)、[Node.js 模块](https://nodejs.org/api/modules.html)

{{% /tab %}}

{{% tab header="PHP" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `php main.php` |
| 一行代码 | `php -r 'echo "hi";'` |
| 语法检查 | `php -l main.php` |
| 内置开发服务器 | `php -S localhost:8000` |
| 查看配置 | `php -i`、`php --ini` |

```bash
php main.php
php -l main.php                  # 只做语法检查（lint）
php -S localhost:8000 -t public   # 开发用内置服务器

php -d opcache.enable_cli=1 main.php   # CLI 下也启用 OPcache
composer install                        # 安装依赖（读 composer.lock）
```

`php -l` 是提交前必跑的检查；`php -S` 让本地开发不用装 Nginx/Apache；生产环境的性能主要取决于 OPcache 与 JIT 的配置，以及是否用 `-d opcache.validate_timestamps=0` 关掉时间戳检查。

📘 [PHP 命令行用法](https://www.php.net/manual/en/features.commandline.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 场景 | 命令 |
| --- | --- |
| 运行脚本 | `ruby main.rb` |
| 一行代码 | `ruby -e 'puts 1'` |
| 语法检查 | `ruby -c main.rb` |
| 交互 | `irb` |
| 启用 JIT | `ruby --yjit main.rb`、`ruby --zjit main.rb` |

```bash
ruby main.rb
ruby -c main.rb            # 语法检查
ruby --yjit main.rb         # 启用 YJIT

bundle install              # 读 Gemfile.lock 安装依赖
bundle exec ruby main.rb     # 在 bundle 环境下运行
gem build mygem.gemspec      # 打包成 .gem
```

有 `Gemfile` 的项目一律用 `bundle exec` 前缀，避免用错 gem 版本。YJIT 对长驻进程收益明显，短脚本可以不启用；`ruby -w` 打开警告，`ruby -d` 打开调试模式。

📘 [Ruby 命令行选项](https://docs.ruby-lang.org/en/master/ruby/options_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 构建系统与依赖管理

单文件跑通之后，下一步是"多文件 + 第三方依赖 + 可重复构建"。这一节给出每门语言的事实标准工具、依赖清单文件、锁文件与最常用的几条命令。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Cargo（随 rustc 一起发布） |
| 依赖清单 | `Cargo.toml` |
| 锁文件 | `Cargo.lock`（二进制项目应提交，库项目按需） |
| 依赖源 | crates.io |

```bash
cargo new demo                 # 新建二进制项目
cargo add serde --features derive   # 加依赖
cargo build --release           # 发布构建
cargo tree                      # 查看依赖树
cargo update -p serde            # 升级某个依赖
cargo vendor                     # 把依赖复制到本地（离线构建）
rustup toolchain install 1.98    # 管理工具链
```

Cargo 同时管构建、依赖与测试，一个 `Cargo.toml` 就能描述整个项目；`Cargo.lock` 锁定精确版本，保证"在我机器上能编，在 CI 上也能编"。多 crate 项目用 workspace 共享依赖与锁文件。

📘 [The Cargo Book](https://doc.rust-lang.org/cargo/)

{{% /tab %}}

{{% tab header="Swift" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | SwiftPM（命令行）/ Xcode（IDE） |
| 依赖清单 | `Package.swift` |
| 锁文件 | `Package.resolved` |
| 依赖源 | Swift Package Index / Git 仓库 |

```swift
// Package.swift 片段
let package = Package(
    name: "demo",
    dependencies: [.package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.5.0")],
    targets: [.executableTarget(name: "demo", dependencies: ["ArgumentParser"])]
)
```

```bash
swift package init --type executable
swift package resolve            # 解析并写 Package.resolved
swift build -c release
swift test
```

SwiftPM 用 Git 仓库作依赖源，`Package.resolved` 锁版本；Xcode 项目可以同时依赖 SwiftPM 包与 xcframework。跨平台（Linux/Windows）构建也走 SwiftPM。

📘 [SwiftPM](https://www.swift.org/documentation/package-manager/)

{{% /tab %}}

{{% tab header="Go" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | go 命令（内置模块系统） |
| 依赖清单 | `go.mod` |
| 锁文件 | `go.sum`（校验和）；精确版本记录在 `go.mod` |
| 依赖源 | 任意 Git 仓库 / 模块代理（GOPROXY） |

```bash
go mod init example.com/demo    # 初始化
go get github.com/gin-gonic/gin@latest   # 加依赖
go mod tidy                      # 清理未用依赖并补齐缺失
go mod download                  # 预下载到模块缓存
go mod vendor                    # 复制到 vendor/（离线构建）
go work init ./a ./b             # 多模块工作区（go.work）
```

Go 的模块系统把"依赖清单 + 锁文件"合并成 `go.mod` + `go.sum`：`go.mod` 记录最小版本（MVS 算法），`go.sum` 保证内容不被篡改。CI 上常跑 `go mod verify` 与 `go mod tidy -diff` 检查一致性。

📘 [Go Modules 参考](https://go.dev/ref/mod)

{{% /tab %}}

{{% tab header="Python" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | pip + `pyproject.toml`（PEP 621）；社区常用 uv / poetry / pipenv |
| 依赖清单 | `pyproject.toml` 的 `[project] dependencies` 或 `requirements.txt` |
| 锁文件 | 标准库没有；uv 用 `uv.lock`、poetry 用 `poetry.lock`、pip 用 `requirements.txt` + `pip-compile` |
| 依赖源 | PyPI |

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # 可编辑安装 + 开发依赖
pip freeze > requirements.txt     # 导出（粗暴但常见）

uv sync                          # 用 uv.lock 安装（快）
python -m build                  # 生成 wheel 与 sdist
```

`pyproject.toml` 是现在的标准清单文件；虚拟环境隔离依赖。需要"可重复构建"就用带锁文件的工具（uv/poetry/pdm），否则 `requirements.txt` 里通常只写宽松版本范围。

📘 [Python 打包用户指南](https://packaging.python.org/)、[uv 文档](https://docs.astral.sh/uv/)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Gradle（Kotlin DSL）/ Maven |
| 依赖清单 | `build.gradle.kts` + `settings.gradle.kts`（或 `pom.xml`） |
| 锁文件 | Gradle 默认无锁文件，可用 `dependencyLocking` 生成 |
| 依赖源 | Maven Central / Google Maven |

```kotlin
// build.gradle.kts 片段
plugins {
    kotlin("jvm") version "2.4.0"
    application
}
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2")
    testImplementation(kotlin("test"))
}
application { mainClass.set("MainKt") }
```

```bash
./gradlew run            # 运行
./gradlew build          # 构建 + 测试
./gradlew dependencies    # 查看依赖树
```

Gradle 的 `libs.versions.toml` 版本目录集中管理版本号；`gradle wrapper`（`gradlew`）保证所有人用同一个 Gradle 版本，这是团队协作的关键。

📘 [Gradle · Kotlin](https://docs.gradle.org/current/userguide/kotlin_dsl.html)

{{% /tab %}}

{{% tab header="Java" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Maven / Gradle |
| 依赖清单 | `pom.xml`（Maven）或 `build.gradle(.kts)` |
| 锁文件 | Maven 无（用 BOM 固定版本）；Gradle 可用 dependency locking |
| 依赖源 | Maven Central |

```xml
<!-- pom.xml 片段 -->
<dependencies>
  <dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>33.4.0-jre</version>
  </dependency>
</dependencies>
```

```bash
mvn -q package           # 打包
mvn test                  # 测试
mvn dependency:tree       # 依赖树
mvn versions:display-dependency-updates
```

Maven 的 `dependencyManagement` 与 BOM（如 `spring-boot-dependencies`）用来统一版本，避免"依赖冲突"；Gradle 侧对应 `platform()` 与版本目录。

📘 [Maven 入门](https://maven.apache.org/guides/getting-started/)

{{% /tab %}}

{{% tab header="C++" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | CMake（事实标准）/ Make / Meson / Bazel |
| 依赖清单 | `CMakeLists.txt`（构建）、`vcpkg.json` / `conanfile.txt`（包管理） |
| 锁文件 | vcpkg 有 `vcpkg-lock.json`（3.0+）；Conan 有 conan.lock |
| 依赖源 | 系统包管理器、vcpkg、Conan |

```cmake
# CMakeLists.txt 片段
cmake_minimum_required(VERSION 3.28)
project(demo CXX)
set(CMAKE_CXX_STANDARD 23)
add_executable(app main.cpp)
target_compile_options(app PRIVATE -Wall -Wextra)
```

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/app
```

C++ 没有官方包管理器，`find_package`/`pkg-config` 找系统库，vcpkg 或 Conan 管第三方依赖。`CMakePresets.json` 可以把常用配置固化成一条 `cmake --preset release`。

📘 [CMake 文档](https://cmake.org/documentation/)、[vcpkg](https://learn.microsoft.com/en-us/vcpkg/)

{{% /tab %}}

{{% tab header="C" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Make / CMake / Meson / Autotools |
| 依赖清单 | `Makefile`、`CMakeLists.txt`、`configure.ac` |
| 锁文件 | 无（依赖系统包管理器） |
| 依赖源 | 发行版包管理器、pkg-config |

```make
# Makefile 片段
CC = cc
CFLAGS = -std=c23 -O2 -Wall -Wextra
app: main.o util.o
	$(CC) $^ -o $@
```

```bash
make            # 增量构建
make clean
cc $(pkg-config --cflags --libs libcurl) main.c -o app

cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j
```

C 项目通常直接把依赖交给系统：`pkg-config` 给编译/链接参数，发行版打包工具负责版本。要自带依赖就把源码 vendor 进仓库，或用 CMake 的 `FetchContent`。

📘 [GNU Make 手册](https://www.gnu.org/software/make/manual/)、[pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/)

{{% /tab %}}

{{% tab header="Julia" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Pkg（标准库） |
| 依赖清单 | `Project.toml` |
| 锁文件 | `Manifest.toml` |
| 依赖源 | General Registry（GitHub） |

```julia
using Pkg
Pkg.activate(".")          # 激活当前目录为项目环境
Pkg.add("DataFrames")       # 加依赖（写 Project.toml 与 Manifest.toml）
Pkg.instantiate()           # 按 Manifest.toml 精确还原
Pkg.status()                # 查看当前依赖
Pkg.update()                # 升级
```

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. main.jl
```

Julia 的项目环境是"每个项目一份 `Project.toml` + `Manifest.toml`"；`Manifest.toml` 锁定精确版本与依赖树，是复现环境的关键文件。用 `Pkg.develop` 把本地包挂进环境做开发。

📘 [Pkg 文档](https://pkgdocs.julialang.org/v1/)

{{% /tab %}}

{{% tab header="C#" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | MSBuild / dotnet CLI |
| 依赖清单 | `.csproj`（项目）+ `.sln`（解决方案） |
| 锁文件 | 可选 `packages.lock.json`（`RestorePackagesWithLockFile`） |
| 依赖源 | NuGet |

```xml
<!-- demo.csproj 片段 -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Serilog" Version="4.2.0" />
  </ItemGroup>
</Project>
```

```bash
dotnet new console -o demo
dotnet add demo package Serilog     # 加依赖
dotnet restore                       # 还原 NuGet 包
dotnet build -c Release
dotnet test
dotnet list package --outdated       # 检查可升级的包
```

NuGet 默认不生成锁文件（`obj/project.assets.json` 是中间产物）；团队协作与 CI 建议打开 `RestorePackagesWithLockFile`，或用中央包管理（`Directory.Packages.props`）统一版本。

📘 [dotnet CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/)、[NuGet](https://learn.microsoft.com/en-us/nuget/)

{{% /tab %}}

{{% tab header="Dart" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | pub（`dart pub`） |
| 依赖清单 | `pubspec.yaml` |
| 锁文件 | `pubspec.lock` |
| 依赖源 | pub.dev |

```yaml
# pubspec.yaml 片段
name: demo
environment:
  sdk: ^3.13.0
dependencies:
  http: ^1.2.0
dev_dependencies:
  test: ^1.25.0
```

```bash
dart pub get          # 安装依赖（写 pubspec.lock）
dart pub upgrade       # 升级到允许范围内的最新版
dart pub outdated      # 查看可升级项
dart analyze           # 静态分析
dart test              # 跑测试
dart pub publish --dry-run   # 发布前检查
```

Dart 3.6 起支持 pub workspace（多个包共享一个 `pubspec.lock`），适合 monorepo；Flutter 项目用 `flutter pub get`，两者是同一套 pub 机制。

📘 [pub 文档](https://dart.dev/tools/pub)

{{% /tab %}}

{{% tab header="R" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | R CMD（`build`/`check`/`INSTALL`） |
| 依赖清单 | `DESCRIPTION`（`Imports`/`Suggests` 字段）+ `NAMESPACE` |
| 锁文件 | `renv.lock`（renv 包） |
| 依赖源 | CRAN / Bioconductor / GitHub |

```r
# 包开发常用（devtools）
devtools::load_all()      # 载入当前包（开发态）
devtools::check()          # 跑 R CMD check
devtools::document()       # 生成 man/ 文档
```

```bash
R CMD build mypkg           # 生成源码包 .tar.gz
R CMD check mypkg_0.1.0.tar.gz
R CMD INSTALL mypkg          # 本地安装
Rscript -e 'renv::init()'    # 为项目建立 renv.lock
Rscript -e 'renv::restore()' # 按锁文件还原
```

`DESCRIPTION` 是包的元数据与依赖清单，`renv` 负责项目级锁定。生产脚本建议把 renv 的 restore 放进部署流程，避免"某天 CRAN 上的版本变了导致结果不同"。

📘 [R 扩展手册](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)、[renv](https://rstudio.github.io/renv/)

{{% /tab %}}

{{% tab header="Zig" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | `zig build`（读 `build.zig`） |
| 依赖清单 | `build.zig.zon` |
| 锁文件 | `build.zig.zon` 里的哈希即锁定 |
| 依赖源 | URL + 内容哈希（无中心仓库） |

```zig
// build.zig.zon 片段
.{
    .name = .demo,
    .version = "0.1.0",
    .dependencies = .{
        .zap = .{ .url = "https://github.com/zigzap/zap/archive/refs/tags/v0.10.0.tar.gz", .hash = "..." },
    },
    .paths = .{""},
}
```

```bash
zig init                 # 生成 build.zig 与 build.zig.zon
zig build                # 构建（产物在 zig-out/）
zig build run            # 构建并运行
zig build test            # 跑测试
zig fetch --save <url>    # 加依赖并写入哈希
```

Zig 没有中心包仓库：依赖就是一个 URL + 内容哈希，哈希对不上就拒绝构建（供应链安全）。构建缓存放在 `zig-cache/` 与 `~/.cache/zig`，`zig build --summary all` 能看到每一步耗时。

📘 [Zig 构建系统](https://ziglang.org/documentation/master/#Zig-Build-System)

{{% /tab %}}

{{% tab header="Lua" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | 无官方；LuaRocks 是事实标准 |
| 依赖清单 | `.rockspec` |
| 锁文件 | 无（LuaRocks 按版本安装） |
| 依赖源 | luarocks.org |

```bash
luarocks install luafilesystem     # 安装一个 rock
luarocks install --local busted     # 装到用户目录
luarocks make                       # 用当前目录的 rockspec 构建安装
luarocks list                       # 已安装列表
```

```lua
-- 在代码里 require 已安装的模块
local lfs = require("lfs")
print(lfs.currentdir())
```

Lua 项目结构非常自由：`require` 按 `package.path` 找文件，配置靠环境变量 `LUA_PATH`/`LUA_CPATH`。要把 Lua 嵌进 C 程序，构建交给宿主项目的 CMake/Make。

📘 [LuaRocks](https://luarocks.org/)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | `tsc` + 打包器（esbuild / Vite / webpack / Rollup） |
| 依赖清单 | `package.json` |
| 锁文件 | `package-lock.json`（npm）/ `pnpm-lock.yaml` / `yarn.lock` |
| 依赖源 | npm Registry |

```jsonc
// tsconfig.json 片段
{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "strict": true,
    "noEmit": true,          // 由打包器产出 JS
    "declaration": true       // 需要发 .d.ts 时
  },
  "include": ["src"]
}
```

```bash
npm install -D typescript esbuild
npx tsc --noEmit             # 只做类型检查
npx esbuild src/main.ts --bundle --minify --outfile=dist/main.js
npx tsc --build              # 项目引用（monorepo）增量构建
```

常见分工是"`tsc` 管类型、打包器管产物"：CI 里先 `tsc --noEmit` 把类型错误挡住，再用 esbuild/Vite 生成运行代码。monorepo 用 project references 与 `--build` 做增量编译。

📘 [tsconfig 参考](https://www.typescriptlang.org/tsconfig)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | npm / pnpm / yarn + 打包器 |
| 依赖清单 | `package.json` |
| 锁文件 | `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` |
| 依赖源 | npm Registry |

```jsonc
// package.json 片段
{
  "name": "demo",
  "type": "module",
  "scripts": {
    "start": "node src/main.js",
    "build": "esbuild src/main.js --bundle --minify --outfile=dist/main.js",
    "test": "node --test"
  }
}
```

```bash
npm ci                 # 按 lockfile 精确安装（CI 推荐）
npm install <pkg>       # 加依赖
npm run build           # 跑脚本
npm audit fix            # 安全修复
```

锁定依赖是 Node 项目的基本要求：CI 用 `npm ci`（严格按锁文件）而不是 `npm install`。monorepo 用 workspaces（npm/pnpm/yarn 都支持）；包体积与攻击面用 `npm ls`、`npm audit` 观察。

📘 [npm 文档](https://docs.npmjs.com/)、[pnpm](https://pnpm.io/)

{{% /tab %}}

{{% tab header="PHP" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Composer |
| 依赖清单 | `composer.json` |
| 锁文件 | `composer.lock` |
| 依赖源 | Packagist |

```jsonc
// composer.json 片段
{
  "require": { "php": "^8.5", "monolog/monolog": "^3.0" },
  "require-dev": { "phpunit/phpunit": "^11.0" },
  "autoload": { "psr-4": { "App\\": "src/" } }
}
```

```bash
composer install          # 按 composer.lock 安装（CI 用这个）
composer update            # 升级依赖并更新锁文件
composer require guzzlehttp/guzzle
composer dump-autoload --optimize    # 生成并优化自动加载
composer validate          # 校验 composer.json
```

Composer 的 PSR-4 自动加载是 PHP 项目组织代码的基础；`composer.lock` 必须提交，CI 用 `composer install`（而不是 `update`）。打包成单文件 `.phar` 用 Box 等工具。

📘 [Composer 文档](https://getcomposer.org/doc/)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 项目 | 内容 |
| --- | --- |
| 构建工具 | Bundler + RubyGems |
| 依赖清单 | `Gemfile`（项目）/ `.gemspec`（库） |
| 锁文件 | `Gemfile.lock` |
| 依赖源 | rubygems.org |

```ruby
# Gemfile 片段
source "https://rubygems.org"
gem "rails", "~> 8.0"
group :development, :test do
  gem "rspec"
end
```

```bash
bundle install             # 安装并写 Gemfile.lock
bundle update rails         # 升级指定 gem
bundle exec rspec           # 在锁定环境下运行
gem build mygem.gemspec     # 打包 gem
gem install mygem-0.1.0.gem
rake build                  # 项目里的 Rake 任务
```

`Gemfile.lock` 必须进版本库；所有命令加 `bundle exec` 前缀才能保证用到锁定的版本。工具链版本（Ruby 自身）用 rbenv/asdf/rvm 管理，`.ruby-version` 记录版本。

📘 [Bundler](https://bundler.io/)、[RubyGems](https://guides.rubygems.org/)

{{% /tab %}}

{{< /tabpane >}}

### 编译产物与中间表示

"编译之后到底生成了什么"决定了调试方式、部署方式与性能上限。这一节列出每门语言的产物类型，以及查看中间表示（IR/字节码/汇编）的命令。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 产物 | 说明 |
| --- | --- |
| `target/debug/<name>`, `target/release/<name>` | 可执行文件 |
| `.rlib`, `.rmeta` | 库产物与元数据 |
| LLVM IR, 汇编, 目标文件 | 用 `--emit` 按需生成 |

```bash
cargo build --release
cargo rustc --release -- --emit=asm       # 生成 .s
cargo rustc --release -- --emit=llvm-ir    # 生成 .ll
rustc --emit=obj main.rs                    # 只要 .o
```

中间层是 MIR（借用检查在这一层完成）与 LLVM IR；要看具体函数的汇编可以用 cargo-show-asm。

📘 [rustc 代码生成选项](https://doc.rust-lang.org/rustc/codegen-options/index.html)

{{% /tab %}}

{{% tab header="Swift" %}}

| 产物 | 说明 |
| --- | --- |
| 可执行文件 + `.dSYM` | 发布产物与调试符号 |
| `.swiftmodule`, `.swiftdoc` | 模块接口与文档 |
| `.o` | 目标文件 |

```bash
swiftc -O main.swift -o app -g          # 带调试信息
swiftc -emit-sil main.swift              # Swift 中间语言 SIL
swiftc -emit-ir main.swift               # LLVM IR
```

SIL 是 Swift 特有的中间层：ARC 优化、所有权检查都在这里发生，再往下才是 LLVM IR。

📘 [Swift 编译器文档](https://www.swift.org/documentation/)

{{% /tab %}}

{{% tab header="Go" %}}

| 产物 | 说明 |
| --- | --- |
| 单个可执行文件 | 默认静态链接、自带运行时 |
| 汇编 | `-gcflags=-S` 或 `go tool objdump` |
| 临时中间目录 | `go build -work` 会打印路径 |

```bash
go build -o app .
go build -gcflags=-S main.go > main.s     # 查看汇编
go tool objdump -s main.main app           # 反汇编指定函数
```

Go 没有可移植的字节码；`go tool compile`/`go tool link` 是内部工具，正常构建请始终用 `go build`。

📘 [go 命令文档](https://go.dev/cmd/go/)

{{% /tab %}}

{{% tab header="Python" %}}

| 产物 | 说明 |
| --- | --- |
| `__pycache__/*.cpython-314.pyc` | 字节码缓存 |
| wheel, sdist | `.whl` 与 `.tar.gz` 分发包 |
| 独立可执行文件 | PyInstaller / Nuitka / zipapp 产出 |

```bash
python3 -m compileall -q .          # 生成 .pyc
python3 -m dis main.py               # 反汇编字节码
python3 -m zipapp mypkg -o app.pyz    # 打包成可执行 zip
```

`.pyc` 只是缓存，不是分发格式；跨机器部署用 wheel 或打包器生成的独立可执行文件。

📘 [dis 模块](https://docs.python.org/3/library/dis.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 产物 | 说明 |
| --- | --- |
| `.class`, `.jar` | JVM 字节码与包 |
| `.kexe`, `.framework`, `.a` | Kotlin/Native 产物 |
| `.wasm`, `.js` | Kotlin/Wasm 与 Kotlin/JS 产物 |

```bash
kotlinc main.kt -include-runtime -d app.jar
jar tf app.jar | head                  # 查看 JAR 内容
javap -c -p MainKt                      # 反汇编字节码
```

编译分两步：前端产出 Kotlin IR，后端再生成 JVM 字节码 / Native / Wasm；`javap` 是查看 JVM 实际指令的常用手段。

📘 [Kotlin 编译器选项](https://kotlinlang.org/docs/compiler-reference.html)

{{% /tab %}}

{{% tab header="Java" %}}

| 产物 | 说明 |
| --- | --- |
| `.class` | JVM 字节码 |
| `.jar`, `.jmod` | 打包与模块文件 |
| CDS/AOT 归档, jlink 运行时镜像 | 启动加速与裁剪后的 JRE |

```bash
javac -d out src/Main.java
javap -c -p out/Main.class             # 反汇编
jar --create --file app.jar --main-class Main -C out .
java -XX:ArchiveClassesAtExit=app.jsa -cp out Main   # 生成 CDS 归档
jlink --add-modules java.base --output runtime        # 定制运行时
```

CDS/AOT 归档把类加载结果缓存下来加速启动，jlink 用来裁出只含所需模块的运行时镜像。

📘 [javap](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javap.html)

{{% /tab %}}

{{% tab header="C++" %}}

| 产物 | 说明 |
| --- | --- |
| `.o` | 目标文件 |
| `.a`, `.so`, `.dylib`, `.dll` | 静态库与动态库 |
| `.pch`/`.gch`, `.pcm` | 预编译头与模块缓存 |

```bash
g++ -std=c++23 -c main.cpp -o main.o
g++ -std=c++23 -S main.cpp -o main.s       # 汇编
g++ -std=c++23 -shared -fPIC lib.cpp -o lib.so
nm -C app | head                            # 查看符号
```

静态库在链接期复制进产物，动态库在运行期加载；ABI 不兼容是 C++ 依赖问题的主要来源。

📘 [cppreference · 翻译阶段](https://en.cppreference.com/w/cpp/language/translation_phases)

{{% /tab %}}

{{% tab header="C" %}}

| 产物 | 说明 |
| --- | --- |
| `.i`, `.s`, `.o`, 可执行文件 | 预处理、汇编、目标文件、链接产物 |
| `.a`, `.so` | 静态库与共享库 |

```bash
gcc -E main.c -o main.i        # 预处理结果
gcc -S main.c -o main.s        # 汇编
gcc -c main.c -o main.o        # 目标文件
gcc main.o -o app              # 链接
```

排查宏展开看 `.i`，排查性能看 `.s`，排查链接看 `nm`/`ldd` 输出的符号与依赖。

📘 [GCC 总体选项](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)

{{% /tab %}}

{{% tab header="Julia" %}}

| 产物 | 说明 |
| --- | --- |
| `.ji` 预编译缓存 | 包预编译结果 |
| sysimage（`.so`/`.dylib`/`.dll`） | 固化常用包与代码的镜像 |
| `juliac` 产物 | 独立可执行文件或共享库 |

```julia
@code_lowered f(1)   # 降级后的 IR
@code_typed f(1)       # 类型推断结果
@code_llvm f(1)         # LLVM IR
@code_native f(1)       # 本机汇编
```

```bash
julia -e 'using Pkg; Pkg.precompile()'
julia -e 'using PackageCompiler; create_sysimage(["DataFrames"])'
```

预编译缓存加快加载，sysimage 把加载与部分编译固化，`juliac` 进一步产出可分发的原生程序。

📘 [Julia · 性能提示](https://docs.julialang.org/en/v1/manual/performance-tips/)

{{% /tab %}}

{{% tab header="C#" %}}

| 产物 | 说明 |
| --- | --- |
| `.dll` | IL 程序集（默认输出） |
| `.exe` (apphost), `.pdb` | 平台启动器与调试符号 |
| Native AOT / ReadyToRun | 原生可执行文件 / 预编译镜像 |

```bash
dotnet build -c Release                 # bin/Release/net10.0/
dotnet publish -c Release -o out
dotnet publish -c Release -r linux-x64 -p:PublishAot=true -p:StripSymbols=true
```

默认产物是跨平台 IL，运行需要 .NET 运行时；`--self-contained` 带上运行时，`PublishAot` 直接产出机器码（启动快、体积小，但反射受限）。

📘 [.NET 部署](https://learn.microsoft.com/en-us/dotnet/core/deploying/)

{{% /tab %}}

{{% tab header="Dart" %}}

| 产物 | 说明 |
| --- | --- |
| `.dill` | Kernel 中间表示 |
| `dart compile exe` 产物 | AOT 原生可执行（自带运行时快照） |
| `.js`, `.wasm` | Web 目标产物 |

```bash
dart compile kernel main.dart -o main.dill
dart compile exe main.dart -o app
dart compile js -O2 main.dart -o out/main.js
dart compile wasm main.dart -o out/main.wasm
```

JIT 与 AOT 都从 Kernel IR 出发；Web 目标走 dart2js（tree shaking + `-O` 优化）或 dart2wasm。

📘 [dart compile](https://dart.dev/tools/dart-compile)

{{% /tab %}}

{{% tab header="R" %}}

| 产物 | 说明 |
| --- | --- |
| 源码 `.R` | 直接执行，无编译产物 |
| `.rds`, `.rda`, `.RData` | 序列化的数据与对象 |
| `.tar.gz`, `.zip` | 源码包与二进制包（含字节码） |

```r
saveRDS(model, "model.rds")
readRDS("model.rds")
```

```bash
R CMD INSTALL --byte-compile mypkg     # 安装时预编译字节码
```

包的字节码在安装时生成（`ByteCompile: yes`），运行时不再重复编译；`.rds`/`.RData` 是数据产物，不是代码产物。

📘 [R 语言定义](https://cran.r-project.org/doc/manuals/r-release/R-lang.html)

{{% /tab %}}

{{% tab header="Zig" %}}

| 产物 | 说明 |
| --- | --- |
| 可执行文件, `.o`, `.a`, `.so` | `build-exe` / `build-obj` / `build-lib` |
| `zig-out/` | `zig build` 默认输出目录 |
| `zig-cache/`, `~/.cache/zig` | 构建缓存 |

```bash
zig build-exe main.zig
zig build-lib -dynamic lib.zig
zig build-exe -femit-asm=main.s main.zig
zig build-exe -femit-llvm-ir=main.ll main.zig
```

`comptime` 的计算结果会直接写进产物：单态化、未使用分支裁剪都在编译期完成，所以"产物长什么样"取决于编译期执行了什么。

📘 [Zig · 构建模式](https://ziglang.org/documentation/master/#Build-Mode)

{{% /tab %}}

{{% tab header="Lua" %}}

| 产物 | 说明 |
| --- | --- |
| `.luac` | 预编译字节码 |
| `string.dump` 结果 | 运行时导出的字节码 |
| `.so`, `.dll` | C 扩展模块 |

```bash
luac -o main.luac main.lua
luac -l main.luac              # 反汇编（带调试信息时）
luac -s -o main.luac main.lua   # 去掉调试信息
```

字节码与 Lua 版本强绑定，跨版本分发必须带源码；嵌入式场景常把脚本编成 C 数组链接进宿主程序。

📘 [Lua 5.5 · luac](https://www.lua.org/manual/5.5/luac.html)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 产物 | 说明 |
| --- | --- |
| `.js` | 转译结果 |
| `.d.ts`, `.d.ts.map` | 类型声明与声明映射 |
| `.js.map`, `.tsbuildinfo` | source map 与增量信息 |

```bash
npx tsc --declaration --sourceMap
npx tsc --incremental
npx tsc --noEmit
```

类型在产物里被完全擦除，`.d.ts` 是给下游项目用的类型描述；source map 是调试转译产物的唯一桥梁。

📘 [tsconfig 参考](https://www.typescriptlang.org/tsconfig)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 产物 | 说明 |
| --- | --- |
| `.js`, `.mjs`, `.cjs` | 源码即产物 |
| bundle + `.map` | 打包与 source map |
| SEA blob, 启动快照 | 单文件可执行与快照 |

```bash
npx esbuild src/main.js --bundle --minify --sourcemap --outfile=dist/main.js
node --build-snapshot -e 'require("./heavy.js")'
```

Node 的 SEA 把脚本与运行时打成单个可执行文件；`--build-snapshot` 生成的快照能显著降低冷启动时间。

📘 [Node.js · 单文件可执行程序](https://nodejs.org/api/single-executable-applications.html)

{{% /tab %}}

{{% tab header="PHP" %}}

| 产物 | 说明 |
| --- | --- |
| 无（源码执行） | 每次请求编译成 opcode |
| OPcache 缓存 | 进程内存或文件缓存 |
| `.phar` | 单文件打包格式 |

```bash
php -d opcache.enable_cli=1 -d opcache.file_cache=/tmp/opcache main.php
php -d opcache.jit=tracing -d opcache.jit_buffer_size=64M main.php
php -d phar.readonly=0 build.php     # 打包 .phar
```

PHP 的产物主要是缓存：OPcache 存 opcode，preload 把代码常驻内存，JIT 再把热点编译成机器码。

📘 [OPcache 配置](https://www.php.net/manual/en/opcache.configuration.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 产物 | 说明 |
| --- | --- |
| 无（源码执行） | 启动时编译成 YARV 字节码 |
| `RubyVM::InstructionSequence` | 可导出/导入字节码 |
| `.gem` | gem 包 |

```ruby
iseq = RubyVM::InstructionSequence.compile("1 + 2")
puts iseq.disasm                  # 反汇编字节码
binary = iseq.to_binary           # 导出字节码
RubyVM::InstructionSequence.load_from_binary(binary).eval
```

```bash
ruby --yjit -e 'p RubyVM::YJIT.enabled?'
```

ISeq 字节码可以导出并在同版本间加载，但跨版本不保证兼容；发布仍以源码或 gem 为主。

📘 [RubyVM::InstructionSequence](https://docs.ruby-lang.org/en/master/RubyVM/InstructionSequence.html)

{{% /tab %}}

{{< /tabpane >}}

### 优化、发布与调试

能跑之后要关心的三件事：**优化等级**（编译得有多快）、**发布形态**（怎么交给用户）、**调试手段**（出问题怎么看）。这一节把它们放在一起对照。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 项目 | 做法 |
| --- | --- |
| Release 构建 | `cargo build --release`（默认 opt-level=3） |
| 体积/性能调优 | `[profile.release] lto="thin"`, `codegen-units=1`, `panic="abort"`, `strip=true` |
| 分发 | `cargo install --path .`；或用 `--target x86_64-unknown-linux-musl` 做静态二进制 |
| 调试 | `RUST_BACKTRACE=1`、`rust-gdb`/`rust-lldb`、`cargo test`、`cargo clippy`、Miri、`cargo bloat` |

```toml
# Cargo.toml
[profile.release]
lto = "thin"
codegen-units = 1
panic = "abort"
strip = true
```

```bash
cargo build --release
cargo clippy --all-targets -- -D warnings   # 静态检查
cargo test
cargo install --path .
```

`lto` 与 `codegen-units=1` 会显著拉长编译时间换运行性能，`panic="abort"` 去掉 unwind 表能再瘦一圈（代价是无法捕获 panic）。

📘 [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html)

{{% /tab %}}

{{% tab header="Swift" %}}

| 项目 | 做法 |
| --- | --- |
| 优化等级 | `-Onone`（默认）、`-O`、`-Osize` |
| 跨模块优化 | `-whole-module-optimization`、`-cross-module-optimization` |
| 发布 | `swift build -c release`；`-static-stdlib` 静态链接标准库 |
| 调试 | lldb、`-g`、`-sanitize=address`、`swift test` |

```bash
swift build -c release
swiftc -O -whole-module-optimization main.swift -o app
swiftc -g -sanitize=address main.swift -o app-debug
lldb ./app
```

Debug 构建默认 `-Onone`（编译快、便于调试），发布务必显式 `-O`；`-Osize` 用于体积敏感的 App/嵌入式。

📘 [Swift 优化](https://www.swift.org/documentation/)

{{% /tab %}}

{{% tab header="Go" %}}

| 项目 | 做法 |
| --- | --- |
| 体积 | `-ldflags="-s -w"`、`-trimpath` |
| 交叉编译 | `GOOS`/`GOARCH`，`CGO_ENABLED=0` 纯静态 |
| 性能分析 | `pprof`、`go test -bench -benchmem`、`-gcflags="-m"` 看逃逸 |
| 调试 | `go test -race`、`dlv`（Delve）、`GODEBUG` |

```bash
go build -trimpath -ldflags="-s -w" -o app .
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o app .

go test -race -cover ./...
go test -bench=. -benchmem ./...
go build -gcflags="-m" . 2>&1 | grep escapes | head
```

Go 没有"优化等级"开关，编译器自己决定内联与逃逸；发布时能做的优化主要是去符号（`-s -w`）、去路径（`-trimpath`）与静态链接。

📘 [Go · 诊断](https://go.dev/doc/diagnostics)、[pprof](https://pkg.go.dev/net/http/pprof)

{{% /tab %}}

{{% tab header="Python" %}}

| 项目 | 做法 |
| --- | --- |
| 优化模式 | `-O`（去断言）、`-OO`（再去 docstring）、`PYTHONOPTIMIZE=2` |
| 加速 | 3.14 实验 JIT（`PYTHON_JIT=1`）、free-threaded 构建、C 扩展 |
| 发布 | PyInstaller / Nuitka / zipapp / wheel |
| 调试 | `pdb`、`breakpoint()`、`cProfile`、`tracemalloc`、`mypy`/`ruff` |

```bash
python3 -O main.py
PYTHON_JIT=1 python3 main.py          # 3.14 官方构建的实验 JIT

python3 -m cProfile -s cumtime main.py | head -20
python3 -m pdb main.py
mypy . && ruff check .
```

CPython 的解释器开销决定了纯 Python 代码的性能上限；真正的提速手段是算法、C 扩展（NumPy 等）或换实现（PyPy），`-O`/JIT 只是边际优化。

📘 [Python · 性能分析](https://docs.python.org/3/library/profile.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 项目 | 做法 |
| --- | --- |
| 发布构建 | `./gradlew assembleRelease`（Android 侧配合 R8/ProGuard） |
| 原生 | Kotlin/Native 的 `linkRelease*`，`-opt`、`-g` |
| 运行优化 | JVM 参数：`-Xmx`、`-XX:+UseZGC`、`-XX:TieredStopAtLevel=1`（短进程） |
| 调试 | IDE 断点、`jdb`、`kotlin.test`、JFR |

```bash
./gradlew build
./gradlew linkReleaseExecutableMacosArm64    # Kotlin/Native 原生可执行
java -XX:+UseZGC -jar app.jar
```

JVM 路线的优化本质是"JVM 调优 + 减少装箱/分配"；Kotlin/Native 与 Wasm 路线则要看各自后端的优化选项。

📘 [Kotlin/Native](https://kotlinlang.org/docs/native-overview.html)

{{% /tab %}}

{{% tab header="Java" %}}

| 项目 | 做法 |
| --- | --- |
| JVM 调优 | `-Xmx`、`-XX:+UseZGC`/`G1`、`-XX:TieredStopAtLevel=1` |
| 启动加速 | CDS/AOT 缓存（JDK 24/25 的 JEP 483/514/515） |
| 发布 | `jlink` 定制运行时、`jpackage` 打安装包、GraalVM `native-image` |
| 调试 | `jdb`、JDWP（`-agentlib:jdwp`）、JFR、`jcmd`/`jstack` |

```bash
java -XX:+UseZGC -Xmx2g -jar app.jar
java -XX:AOTCache=app.aot -XX:AOTMode=create -cp out Main   # JDK 24+ AOT 缓存
jlink --add-modules java.base,java.sql --output runtime
jpackage --input out --main-jar app.jar --type dmg
```

短命进程（CLI、函数计算）最在意启动时间：AOT/AppCDS 缓存比 JIT 调参有效得多；长驻服务则相反，让 JIT 预热、选择低延迟 GC 更关键。

📘 [JEP 483](https://openjdk.org/jeps/483)、[jpackage](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jpackage.html)

{{% /tab %}}

{{% tab header="C++" %}}

| 项目 | 做法 |
| --- | --- |
| 优化等级 | `-O2`（默认推荐）、`-O3`、`-Os`（体积）、`-Og`（调试友好） |
| 进阶优化 | `-flto`、`-march=native`、PGO（`-fprofile-generate`/`-fprofile-use`） |
| 发布 | `-DNDEBUG`、`-s`、`-static`、`strip` |
| 调试 | `-g`、gdb/lldb、`-fsanitize=address,undefined`、valgrind、perf |

```bash
g++ -std=c++23 -O2 -DNDEBUG -flto -s main.cpp -o app
clang++ -g -O1 -fsanitize=address,undefined main.cpp -o app-san
valgrind --leak-check=full ./app-debug
perf record ./app && perf report
```

发布用 `-O2 -DNDEBUG`（关掉 assert）；排查内存/未定义行为用 ASan+UBSan；`-march=native` 会绑定本机指令集，交叉分发时慎用。

📘 [GCC 优化选项](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)

{{% /tab %}}

{{% tab header="C" %}}

| 项目 | 做法 |
| --- | --- |
| 优化等级 | `-O0`/`-O1`/`-O2`/`-O3`/`-Os` |
| 进阶 | `-flto`、`-march=native`、PGO |
| 发布 | `-DNDEBUG`、`strip`、`-static` |
| 调试 | `-g`、gdb、ASan/UBSan、valgrind、`-fanalyzer`（GCC 静态分析） |

```bash
gcc -std=c23 -O2 -DNDEBUG main.c -o app
gcc -g -O1 -fsanitize=address,undefined main.c -o app-san
gcc -fanalyzer -Wall main.c        # 编译期静态分析
```

C 的优化开关与 C++ 基本一致，差别在于没有异常/RTTI 相关选项；静态分析器（`-fanalyzer`、clang `--analyze`）能在编译期抓出一批内存与空指针问题。

📘 [GCC 静态分析](https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html)

{{% /tab %}}

{{% tab header="Julia" %}}

| 项目 | 做法 |
| --- | --- |
| 优化等级 | `-O3`（默认 `-O2`）、`--check-bounds=no`（危险）、`--compile=min`（启动优先） |
| 并发 | `--threads=auto` |
| 发布 | `PackageCompiler.jl` 生成 sysimage/app、`juliac` 编译独立可执行 |
| 调试 | `@code_warntype`、`@time`/`@btime`、`Profile`、`JET.jl` |

```bash
julia -O3 --threads=auto main.jl
julia -e 'using Profile; @profile f(); Profile.print()'
```

```julia
@code_warntype slow_function(1)    # 找类型不稳定
```

Julia 的性能几乎完全取决于**类型稳定**：一旦出现 `Any` 或类型不稳定，JIT 生成的代码就会退回到动态派发。

📘 [Julia · 性能提示](https://docs.julialang.org/en/v1/manual/performance-tips/)

{{% /tab %}}

{{% tab header="C#" %}}

| 项目 | 做法 |
| --- | --- |
| 发布构建 | `dotnet publish -c Release` |
| 形态 | `PublishReadyToRun`、`PublishTrimmed`、`PublishSingleFile`、`PublishAot` |
| 运行优化 | TieredPGO、`ServerGarbageCollection`、`InvariantGlobalization` |
| 调试 | IDE 断点、`dotnet test`、`dotnet-counters`、`dotnet-trace` |

```bash
dotnet publish -c Release -r linux-x64 --self-contained \
  -p:PublishSingleFile=true -p:PublishTrimmed=true -p:PublishReadyToRun=true
dotnet-counters monitor -p <pid>
```

裁剪（Trim）与 AOT 会与反射、`dynamic`、序列化框架冲突，启用前要检查依赖是否支持（用 `IsTrimmable`/`IsAotCompatible` 标注）。

📘 [.NET 发布选项](https://learn.microsoft.com/en-us/dotnet/core/deploying/)

{{% /tab %}}

{{% tab header="Dart" %}}

| 项目 | 做法 |
| --- | --- |
| 发布编译 | `dart compile exe`（AOT）、`dart compile js -O2/-O4`（Web） |
| 体积/混淆 | `--obfuscate --split-debug-info=out/` |
| 断言 | 默认关闭；`dart run --enable-asserts` |
| 调试 | DevTools、`dart test`、`dart analyze` |

```bash
dart compile exe --obfuscate --split-debug-info=out main.dart -o app
dart compile js -O4 --minify main.dart -o out/main.js
dart run --enable-asserts main.dart
```

`dart run`（JIT）保留断言与调试信息，`dart compile exe`（AOT）才是发布形态；`--split-debug-info` 把符号单独保存，出线上崩溃时用它还原堆栈。

📘 [dart compile](https://dart.dev/tools/dart-compile)

{{% /tab %}}

{{% tab header="R" %}}

| 项目 | 做法 |
| --- | --- |
| 提速思路 | 向量化 → 字节码编译 → C/C++（Rcpp）→ 并行 |
| 性能分析 | `Rprof()`、`profvis`、`bench`/`microbenchmark` |
| 发布 | `R CMD build` + `check`；脚本用 renv.lock 固定依赖 |
| 调试 | `browser()`、`debug()`、`traceback()`、`options(error = recover)` |

```r
Rprof("prof.out"); f(); Rprof(NULL)
summaryRprof("prof.out")

options(error = recover)      # 出错时进入交互式调试
browser()                      # 在函数里打断点
```

```bash
Rscript --vanilla main.R        # 不加载用户配置，CI 友好
```

R 的性能问题十有八九是"用循环写成了向量化应该做的事"；`profvis` 能直观看出时间花在哪一行。

📘 [R · 调试](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Debugging)

{{% /tab %}}

{{% tab header="Zig" %}}

| 项目 | 做法 |
| --- | --- |
| 构建模式 | `Debug`、`ReleaseSafe`、`ReleaseFast`、`ReleaseSmall` |
| 发布 | `-O ReleaseFast -fstrip`；`zig build -Doptimize=ReleaseSafe` |
| 安全检查 | Debug/ReleaseSafe 保留；ReleaseFast/Small 关闭（溢出变 UB） |
| 调试 | `zig test`、`std.testing`、`-fvalgrind`、gdb/lldb |

```bash
zig build -Doptimize=ReleaseFast
zig build-exe -O ReleaseSmall -fstrip main.zig
zig test main.zig
zig build test -Doptimize=ReleaseSafe
```

Zig 的取舍很清楚：**ReleaseSafe** 保留溢出与越界检查（推荐默认发布模式），**ReleaseFast** 才关掉它们换性能。发布前建议先用 ReleaseSafe 跑一遍测试。

📘 [Zig · 构建模式](https://ziglang.org/documentation/master/#Build-Mode)

{{% /tab %}}

{{% tab header="Lua" %}}

| 项目 | 做法 |
| --- | --- |
| 加载加速 | `luac` 预编译字节码；`luac -s` 去调试信息 |
| JIT | LuaJIT（热点路径编译；注意 5.1 语义） |
| 发布 | 源码或 `.luac`；嵌入时编成 C 数组 |
| 调试 | `debug` 库、`print`、`pcall`/`xpcall`、第三方 profiler |

```bash
luac -s -o app.luac main.lua
lua app.luac
luajit -jv main.lua          # LuaJIT 的 JIT 日志（-jv）
```

```lua
local ok, err = xpcall(work, function(e)
  return debug.traceback(e, 2)      -- 带堆栈的错误信息
end)
```

标准 Lua 没有 JIT；需要性能就换 LuaJIT（但要接受它是 Lua 5.1 语义，`goto`、整数子类型等特性不同）。

📘 [Lua 5.5 手册](https://www.lua.org/manual/5.5/)、[LuaJIT](https://luajit.org/)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 项目 | 做法 |
| --- | --- |
| 类型检查 | `tsc --noEmit`（CI 必跑） |
| 产物优化 | esbuild `--minify --bundle`、`--target` |
| 增量构建 | `tsc --incremental`、`tsc --build`（project references） |
| 调试 | source map + `node --inspect`、`tsc --watch`、`tsc --noEmit --watch` |

```bash
npx tsc --noEmit
npx esbuild src/main.ts --bundle --minify --sourcemap --target=es2022 --outfile=dist/main.js
node --enable-source-maps dist/main.js
```

类型错误在编译期就能拦住，但"运行时错误"（空值、越界、`any` 漏网）仍需测试与校验；`--enable-source-maps` 让 Node 的堆栈指向 `.ts` 源码行。

📘 [tsconfig](https://www.typescriptlang.org/tsconfig)、[Node · source maps](https://nodejs.org/api/cli.html#--enable-source-maps)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 项目 | 做法 |
| --- | --- |
| 体积 | 打包 + `--minify`（esbuild/webpack/rollup） |
| 运行优化 | `--max-old-space-size`、`--trace-gc` |
| 性能分析 | `--cpu-prof`、`--heap-prof`、`--inspect` |
| 发布 | bundle、Node SEA（单文件可执行） |

```bash
node --inspect-brk main.js            # 断点调试
node --cpu-prof main.js                # 生成 .cpuprofile
node --max-old-space-size=4096 main.js  # 调大堆上限
npx esbuild main.js --bundle --minify --sourcemap --outfile=dist/main.js
```

JS 的性能问题通常分两类：算法/分配问题（看 CPU profile）与内存泄漏（看 heap profile）；V8 的 JIT 参数一般不需要手动调，崩溃或 OOM 时才是调 `--max-old-space-size` 的时机。

📘 [Node.js CLI](https://nodejs.org/api/cli.html)、[Node.js · 诊断](https://nodejs.org/api/inspector.html)

{{% /tab %}}

{{% tab header="PHP" %}}

| 项目 | 做法 |
| --- | --- |
| 上线优化 | OPcache（`opcache.enable=1`）+ JIT（`opcache.jit=tracing`）+ preload |
| 自动加载 | `composer dump-autoload -o --classmap-authoritative` |
| 发布 | 源码目录、`.phar`；FPM 部署（php-fpm） |
| 调试 | Xdebug、phpdbg、`php -l`、`error_reporting(E_ALL)` |

```bash
php -d opcache.enable=1 -d opcache.jit=tracing -d opcache.jit_buffer_size=64M -S localhost:8000
composer dump-autoload -o --classmap-authoritative
php -d zend_extension=xdebug -d xdebug.mode=debug main.php
```

PHP 的性能开关集中在 `php.ini`：OPcache 决定"要不要重复编译"，preload 决定"启动时加载哪些类"，JIT 只对计算密集代码有效（I/O 型 Web 应用收益有限）。

📘 [OPcache 配置](https://www.php.net/manual/en/opcache.configuration.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 项目 | 做法 |
| --- | --- |
| JIT | `--yjit`、`--zjit`、`RUBY_YJIT_ENABLE=1`；`RubyVM::YJIT.enable` |
| 内存调优 | `RUBY_GC_HEAP_INIT_SLOTS`、`RUBY_GC_HEAP_GROWTH_FACTOR` 等环境变量 |
| 发布 | gem、`Gemfile.lock` 固定依赖；Rails 侧配合 bootsnap |
| 调试 | `debug` gem（`binding.break`）、`ruby -w`、`stackprof` |

```bash
ruby --yjit main.rb
RUBY_YJIT_ENABLE=1 ruby main.rb
ruby -w main.rb                  # 打开警告
stackprof --text profile.dump     # 火焰图/文本报告
```

YJIT 对长驻进程（Web、任务队列）收益最大；短脚本启用 JIT 反而可能更慢。GC 调参只在确认 GC 是瓶颈后才有意义。

📘 [Ruby · YJIT](https://docs.ruby-lang.org/en/master/RubyVM/YJIT.html)、[debug gem](https://github.com/ruby/debug)

{{% /tab %}}

{{< /tabpane >}}
