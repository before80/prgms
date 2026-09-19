+++
title = "编译选项"
date = 2026-09-19T12:00:00+08:00
weight = 16
type = "docs"
description = "18 种语言的编译选项对照：优化等级、体积与链接、运行时与目标控制、调试与分析开关"
isCJKLanguage = true
draft = false
+++

# 编译选项：18 种语言对照

编译选项是横向对照里最难对齐的一块，因为「优化」这件事在 18 门语言里发生在完全不同的时刻：C、C++、Rust、Swift、Zig 在构建期由编译器静态完成，Java、C#、JavaScript 在运行期由 JIT 在方法变热之后才做，Python、Ruby、PHP、Lua、R 则只有解释器与字节码缓存级别的开关，根本没有「优化等级」这个旋钮。选项的载体也各不相同：C 系是纯命令行 flag，Rust 写进 `Cargo.toml` 的 profile，Java 靠 `-XX:` 之类的 JVM 参数，TypeScript 与 C# 把大部分配置放进 `tsconfig.json` 与 `.csproj`，Go 甚至只留了 `-gcflags` 一个后门。本页把这块拆成四组：**优化等级 → 体积与链接 → 运行时与目标控制 → 调试与分析开关**，每组一套 18 语言标签页，代码块里给的是可直接粘贴的 shell 命令与实测输出。理解这条分组逻辑的关键是分清「编译器选项」与「运行时/解释器选项」：`-O2`、`-C opt-level`、`-gcflags` 属于前者，`--yjit`、`PYTHON_JIT`、`-XX:TieredStopAtLevel`、`node --max-old-space-size` 属于后者，把两者混为一谈是这类配置最常见的事故来源。

## 编译选项

**一页速览**

| 语言 | 优化开关写法 | 一句话说明 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | `-C opt-level=0/1/2/3/s/z`, `[profile.release]` | 六档等级，`dev` 默认 0、`release` 默认 3 | 命令行 `-C` 会被 `Cargo.toml` 的 profile 覆盖；`incremental` 在 release 默认关 |
| Swift | `-Onone`, `-O`, `-Osize`, `-Ounchecked` | 默认 `-Onone`，发布必须显式给 `-O` | `-Ounchecked` 取消溢出检查，是语义变化而不是单纯优化 |
| Go | 没有等级开关，`-gcflags` 是后门 | `go build` 默认全量优化，官方刻意不暴露等级 | `-N -l` 只作用于本包，跨包要写 `all=-N -l` |
| Python | `-O`, `-OO`, `PYTHON_JIT=1` | 只有 assert 与 docstring 两级，JIT 仍是实验特性 | 没有 `-X jit`；free-threading 构建不支持 JIT |
| Kotlin | 没有（优化交给 JVM 或 ART） | `jvmTarget`, `-Xjvm-default` 是语义开关 | 发布瘦身靠 R8/ProGuard，`kotlinc` 本身不管体积 |
| Java | 没有（`javac` 不提供优化选项） | 优化全在运行期分层编译 C1/C2 | `-XX:TieredStopAtLevel=1` 只适合短命进程 |
| C++ | `-O0`, `-O1`, `-O2`, `-O3`, `-Os`, `-Og`, `-Ofast`, `-Oz` | 等级之外还有 `-march`/`-mtune` 调指令集 | clang 21 起 `-Ofast` 已弃用，改成 `-O3 -ffast-math` |
| C | 同 C++，`-O0` 到 `-O3`, `-Os`, `-Og` | 标准不规定优化，全由编译器实现决定 | `-O2` 下 UB 常常「看起来能跑」，换个版本就崩 |
| Julia | `-O0` 到 `-O3`（默认 2） | 优化在 JIT 首次特化时按具体类型做 | `--check-bounds` 与 `-O` 互相独立，别指望 `-O3` 去掉边界检查 |
| C# | `Debug`/`Release` 配置 + `Optimize` | 优化主要在 JIT，`TieredCompilation` 默认开 | `PublishAot` 与 `PublishTrimmed` 不能随意叠加 |
| Dart | `-O0` 到 `-O4`（只对 js 与 wasm） | AOT 走 `dart compile exe`，它没有 `-O` | `-O3`/`-O4` 会省掉隐式类型检查，必须先用 `-O2` 回归 |
| R | `compiler::enableJIT(0/1/2/3)` | 字节码编译器按函数调用次数逐级升级 | 关 JIT 要 `R --vanilla` 配合 `enableJIT(0)` |
| Zig | `-O Debug/ReleaseSafe/ReleaseFast/ReleaseSmall` | 模式同时决定安全检查与优化力度，Debug 是默认 | `zig build-exe` 没有 `--strip`，要用 `-fstrip` |
| Lua | 没有优化等级 | 常量折叠在编译期做，`luac -s` 只能剥调试信息 | `luac` 没有 `-O`；声明 `<const>` 才让折叠与寄存器分配更有效 |
| TypeScript | `target`, `module`, `incremental` | TS 7 是 Go 重写的原生编译器，官方称快 10 倍 | 改 `target` 是改产物形态而不是改优化；`tsc` 不生成运行时代码优化 |
| JavaScript | 没有（引擎 JIT 自己决定） | V8 有 Sparkplug, Maglev, Turbofan 三层 | `--max-old-space-size` 是内存上限，不是优化等级 |
| PHP | `opcache.jit`（默认禁用） | OPcache 缓存 opcode，JIT 需显式打开 | `opcache.jit` 自 8.4 起默认 `disable`，8.5 只把 `jit_hot_loop` 默认值从 64 调到 61 |
| Ruby | `--yjit`, `--zjit`, `--jit` | YJIT 是生产推荐，ZJIT 是 4.0 新引入的方法级 JIT | Ruby 4.0 已移除 `--rjit`，只剩 YJIT 与 ZJIT |

### 优化等级

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的优化等级不是命令行开关，而是 Cargo profile 里的一个字段：`opt-level` 取 0、1、2、3、s、z 六档，`dev` profile 默认 0、`release` 默认 3。它属于构建期静态优化，由 `rustc` 交给 LLVM 执行；同一个 profile 里还并排放着 `codegen-units`、`lto`、`incremental`、`panic`、`debug`、`strip`。最该先知道的是权威来源：有 `Cargo.toml` 时 profile 说了算，命令行的 `-C` 只是临时覆盖。

```rust
# ---- Cargo.toml 里声明（release 默认 opt-level = 3）----
# [profile.release]
# opt-level = 3          # 0, 1, 2, 3, s, z
# codegen-units = 1      # 越小跨函数优化越充分，编译越慢
# lto = "fat"            # false, "thin", "fat", "off"
# panic = "abort"        # 去掉 unwind 表
# strip = "symbols"      # 剥符号
# incremental = false    # release 默认就是 false

cargo build --release                     # 读 [profile.release]
cargo build --profile=dev                 # 读 [profile.dev]，即 opt-level = 0
cargo rustc --release -- -C opt-level=z   # 临时覆盖单个 profile

# ---- 直接调 rustc（实测，同一个 fib(30) 程序）----
rustc -C opt-level=0 bench.rs -o r0   && stat -f%z r0      # 470336 字节
rustc -C opt-level=3 bench.rs -o r3   && stat -f%z r3      # 469200 字节
rustc -C opt-level=z bench.rs -o rz   && stat -f%z rz      # 469280 字节
rustc -C opt-level=3 -C debuginfo=2 bench.rs -o rdbg       # 469864 字节（调试信息反把体积推大）
rustc -C opt-level=3 -C panic=abort -C strip=symbols bench.rs -o rab   # 341776 字节
rustc -C opt-level=z -C lto=fat -C codegen-units=1 -C panic=abort -C strip=symbols bench.rs -o rmin   # 285952 字节
./r0                                        # 832040，六档输出完全一致
rustc --print cfg | grep target_feature     # 列出本机目标特性，配合 -C target-cpu=native 使用
rustc -C target-cpu=native -C opt-level=3 bench.rs -o rnat             # 469208 字节
```

`opt-level` 只影响生成的机器码，不影响语言语义（`-C opt-level=s` 与 `z` 都是纯体积取向，`z` 更激进）。真正能砍体积的是 `panic=abort` 加上 `strip=symbols`，上面实测把 469200 字节压到 341776 字节，再叠加 `lto=fat` 与 `codegen-units=1` 可以到 285952 字节，代价是编译时间明显变长、且 `panic=abort` 会让 `catch_unwind` 失效。⚠️ `debuginfo=2` 反而让二进制变大，这在发布构建里通常是不需要的。要确定性行为还要注意：debug 构建的整数溢出会 panic，release 会回绕，这是 `opt-level` 与 `debug-assertions` 联动的结果，不是单纯的速度差异。

📘 [Cargo 手册 · Profiles](https://doc.rust-lang.org/cargo/reference/profiles.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的优化等级由 `swiftc` 的 `-O` 家族控制，共有 `-Onone`、`-O`、`-Osize`、`-Ounchecked` 四档，默认是 `-Onone`。它同样是构建期静态优化，跑在 LLVM 上，但默认不做跨文件内联；跨模块优化要靠 `-whole-module-optimization` 或 `-cross-module-optimization`。最该先知道的是：SwiftPM 的 Debug 配置不会自动加上 `-O`，发布时得在 `swift build -c release` 之外自己确认参数。

```swift
# 实测：同一个求和程序，四种等级的产物大小
swiftc -Onone      opt.swift -o sw_Onone      # 52584 字节（默认，便于调试）
swiftc -O          opt.swift -o sw_O          # 50760 字节
swiftc -Osize      opt.swift -o sw_Osize      # 50776 字节（体积优先）
swiftc -Ounchecked opt.swift -o sw_Ounchecked # 50720 字节（关掉溢出与前置条件检查）
./sw_Onone; ./sw_O; ./sw_Osize; ./sw_Ounchecked
# 四者都输出 333332833333500000

swiftc -O -whole-module-optimization opt.swift -o sw_wmo   # 50696 字节，整模块一起优化
swiftc -O -Xlinker -dead_strip opt.swift -o sw_ds          # 50776 字节，链接期删死代码
swiftc -O -static-stdlib opt.swift -o sw_static
# error: -static-stdlib is no longer supported for Apple platforms
# Apple 平台已移除该开关，静态链接标准库只在 Linux 等平台可用
swiftc -print-target-info | head -12
# "triple": "arm64-apple-macosx26.0"   ← 交叉编译时的 -target 就写这个形状
```

`-Onone` 保留全部调试信息与断言、编译最快，适合日常开发；`-O` 是发布默认选择；`-Osize` 牺牲少量速度换体积，嵌入式与 App 体积敏感时用。⚠️ `-Ounchecked` 不只是「优化更狠」，它会去掉整数溢出检查与 `precondition`，越界与溢出会变成未定义行为，等价于换了一门语言，绝不能在生产里随手打开。`-whole-module-optimization` 把整个模块当成一个编译单元，能显著增加内联机会，但会让增量编译失效，本项目在 Xcode 里对应 `SWIFT_WHOLE_MODULE_OPTIMIZATION`。

📘 [Swift 官方文档 · Swift 编译器](https://www.swift.org/documentation/swift-compiler/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有优化等级这个概念：`go build` 默认就把代码全线优化，官方刻意不提供 `-O0`/`-O2` 之类的开关。想关优化的唯一入口是 `-gcflags`，把参数透传给内部编译器 `cmd/compile`；想诊断优化行为则用 `-gcflags="-m"` 看内联与逃逸分析。最该先知道的是作用域规则：`-gcflags` 只作用于本次构建涉及的包，要影响全部依赖必须写 `all=`。

```go
go build -o go_def opt.go && stat -f%z go_def       # 2413186 字节，默认即优化
go build -gcflags="all=-N -l" -o go_noopt opt.go    # 2309218 字节，关内联与优化
go build -trimpath -ldflags="-s -w" -o go_strip opt.go   # 1571186 字节，去符号与调试信息
./go_def   # 333332833333500000，三种构建输出一致

go build -gcflags="-m=1" opt.go
# ./opt.go:10:13: inlining call to fmt.Println
# ./opt.go:10:13: ... argument does not escape
# ./opt.go:10:14: s escapes to heap        ← 逃逸分析诊断，不是优化开关

go build -gcflags="-d=ssa/check_bce/debug=1" opt.go   # 打印边界检查消除的 SSA 结果
go build -gcflags="-S" opt.go 2>&1 | head -20          # 打印汇编
go test -gcflags="all=-N -l" ./...                     # 关闭优化跑测试（调试用）
```

`-N` 关掉优化、`-l` 关掉内联，两个都要写才有意义，单独一个几乎不改变行为；它们主要用于 `delve` 调试时让变量不被优化掉。`-m` 是纯诊断输出，不会改变生成的代码，⚠️ 不要把它当成性能开关——它只在编译期打印决策结果。体积上真正有效的是 `-ldflags="-s -w"`（去掉符号表与 DWARF），上面实测从 2413186 字节降到 1571186 字节，但会同时让 `pprof` 的符号解析和 `delve` 的能力下降，所以发布版和调试版应当分开构建。

📘 [`cmd/compile` 文档](https://pkg.go.dev/cmd/compile)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有「优化等级」，只有 `-O` 与 `-OO` 两级语义削减，它们属于**解释器选项**而不是编译器选项：CPython 仍然照常生成字节码，只是跳过 `assert` 与 docstring 的装载。再往上一层是字节码缓存：`.pyc` 文件放在 `__pycache__` 里按源文件时间戳失效，这一层直接决定启动速度。真正意义上的编译优化从 3.13 才开始，即 PEP 744 的实验性 JIT，到 3.14 仍然是实验特性。

```python
python3 -c "import sys; print(sys.flags.optimize)"       # 0   默认
python3 -O -c "import sys; print(sys.flags.optimize)"    # 1   去掉 assert 与 __debug__ 分支
python3 -OO -c "import sys; print(sys.flags.optimize)"   # 2   再去掉 docstring

python3    doc.py    # 'docstring'   函数仍能读到 __doc__
python3 -O doc.py    # 'docstring'   -O 不删 docstring
python3 -OO doc.py   # None          -OO 才删

python3 -c "assert False, 'boom'"; echo "exit=$?"
# AssertionError: boom   exit=1
python3 -O -c "assert False, 'boom'; print('asserts removed')"   # asserts removed

python3 -m py_compile doc.py && ls __pycache__/
# doc.cpython-314.pyc          ← 默认缓存
python3 -O -m py_compile doc.py && ls __pycache__/
# doc.cpython-314.opt-1.pyc    ← PEP 488：优化级别写进文件名后缀
python3 -OO -m py_compile doc.py && ls __pycache__/
# doc.cpython-314.opt-2.pyc
python3 -m compileall -q -o 2 .                 # 递归预编译，-o 指定级别
PYTHONDONTWRITEBYTECODE=1 python3 doc.py        # 完全不写缓存

# ---- JIT 与 free-threading ----
python3 -c "import sys; print(sys._jit.is_available(), sys._jit.is_enabled(), sys._jit.is_active())"
# False False False   ← 本机 3.14.7 官方二进制未编入 JIT
PYTHON_JIT=1 python3 -c "import sys; print(sys._jit.is_enabled())"
# False               ← 唯一官方启用方式是环境变量 PYTHON_JIT=1
python3 -c "import sysconfig; print(sysconfig.get_config_var('Py_GIL_DISABLED'))"   # 0
python3 -c "import sys; print(sys._is_gil_enabled())"       # True
python3 -VV
# Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)]    ← free-threading 构建这里会多出 "free-threading build"
```

`-O` 与 `-OO` 的行为差别只在 docstring：`-O` 移除 `assert` 与依赖 `__debug__` 的代码，`-OO` 在此基础上丢弃 docstring，于是 `f.__doc__` 变成 `None`、`help()` 失去文档、依赖 docstring 的框架（例如某些 `argparse` 与 ORM 的自动文档）会失效。⚠️ 它们都**不会**让代码变快多少，唯一稳定的收益是 `.pyc` 更小、启动略快；把 `-OO` 当性能开关是常见误会。缓存文件名带 `.opt-1`/`.opt-2` 后缀是 PEP 488 的设计，所以不同优化级别可以共存、不会互相覆盖。JIT 方面必须记牢三条：3.14 的 JIT 仍是实验性的、**没有 `-X jit` 这个开关**、只能用 `PYTHON_JIT=1` 启用，而 free-threaded 构建**不支持** JIT；官方 macOS 与 Windows 二进制以 `yes-off` 方式编译，所以即使 `sys._jit.is_available()` 为真也必须显式设环境变量。free-threading 自 3.14 起由 PEP 779 定为正式支持，检测方式是 `sysconfig.get_config_var("Py_GIL_DISABLED") == 1`（构建能力）配合 `sys._is_gil_enabled()`（运行状态）。

📘 [Python 3.14 · 命令行与环境变量](https://docs.python.org/3.14/using/cmdline.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 没有优化等级，`kotlinc` 也不提供任何「优化力度」参数：前端把源码变成 JVM 字节码（或 JS、Native、Wasm），真正的优化交给目标平台的 JIT 或 Native 后端。`kotlinc` 上与性能相关的选项基本都是**语义开关**，例如 `-jvm-target` 决定字节码版本、`-Xjvm-default` 决定接口默认方法的生成方式、`-progressive` 打开渐进式语言语义。发布瘦身则完全在 JVM 生态里做，由 R8 或 ProGuard 负责。

```kotlin
# 编译到 JVM 字节码；没有 -O，只有目标与语义开关
kotlinc Main.kt -include-runtime -d app.jar
kotlinc Main.kt -jvm-target 21 -d app.jar          # 字节码版本，不是优化等级
kotlinc Main.kt -Xjvm-default=all -d app.jar       # 接口默认方法生成真实 default 方法
kotlinc Main.kt -progressive -d app.jar            # 渐进式语义（可能改变行为，慎用）
kotlinc -X | grep -i -E "jvm-default|inline|lambda" | head -10   # 高级 -X 选项清单

java -jar app.jar
# hello from kotlin

# Gradle 侧（build.gradle.kts）：优化与瘦身都写在这里
# kotlin { compilerOptions { jvmTarget = JvmTarget.JVM_21 } }
# android { buildTypes { release { isMinifyEnabled = true } } }   ← R8 做 shrink/obfuscate
./gradlew assembleRelease        # Android 发布构建，R8 介入
./gradlew build --configuration-cache   # 构建缓存，缩短编译时间
# Kotlin/Native：优化在 Gradle 的 binaries 配置里
# kotlin { linuxX64 { binaries { executable { entryPoint = "main"; optimize() } } } }
```

`-jvm-target` 只是让字节码版本对齐 JVM，写成 21 并不会让代码更快，写错反而会 `UnsupportedClassVersionError`。`-Xjvm-default=all` 影响的是接口默认方法的调用方式与二进制兼容性，属于语义级开关：老版本用 `DefaultImpls` 桥接，新方式生成真正的 `default` 方法，混用不同设置编译的模块会 `NoSuchMethodError`。⚠️ 想让产物变小，唯一有效的路径是 R8/ProGuard 的 `shrinkResources` 与 `minifyEnabled`，它们做的是静态可达性分析加名称混淆，`kotlinc` 本身不参与。Kotlin/Native 是例外：它的 `optimize()` 与 Gradle 的 `mode = "release"` 才是真正意义上的编译优化等级，等价于 LLVM 的 `-O2`。

📘 [Kotlin · 编译器选项参考](https://kotlinlang.org/docs/compiler-reference.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 把优化彻底推迟到了运行期：`javac` 的 man page 里**没有任何优化等级选项**，它只做解析、类型检查、少量常量折叠与 `invokedynamic` 生成，产出的 `.class` 几乎逐条对应源码。真正决定性能的是 HotSpot 的分层编译——方法先解释执行，变热后由 C1 编译，更热再由 C2 编译。最该先知道的是：想调「优化」必须调 JVM 参数（`-XX:` 系列），而不是 `javac` 参数。

```java
# ---- javac：没有优化等级，只有调试信息与目标版本 ----
javac Main.java                    # 无 -O 之类的选项
javac -g Main.java                 # 生成全部调试信息（行号、源文件、局部变量）
javac -g:none Main.java            # 不带调试信息，class 文件最小
javac -g:lines,vars Main.java      # 只带行号与局部变量
javac --release 25 Main.java       # 指定 API 与 class 版本，不是优化
javac -Xlint:all Main.java         # 静态诊断，不改变产物
javap -c -p Main.class | head -20  # 反汇编字节码，看 javac 有多「老实」

# ---- 分层编译：真正的优化旋钮 ----
java -XX:+PrintCompilation Main    # 打印每个方法的编译层级（1/2/3 = C1，4 = C2）
java -XX:TieredStopAtLevel=1 Main  # 只用 C1：启动快、峰值低，适合 CLI 与短命进程
java -XX:TieredStopAtLevel=4 Main  # 允许 C2，默认就是分层到底
java -Xint Main                    # 纯解释执行，等价于关掉所有 JIT
java -Xmixed Main                  # 默认模式：解释 + 分层编译
java -XX:CompileThresholdScaling=0.5 Main  # 缩放热度阈值：小于 1.0 更早编译，大于 1.0 更晚
java -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints Main   # 诊断级开关，栈信息更准

# ---- AOT 与启动加速 ----
java -XX:ArchiveClassesAtExit=app.jsa -cp app.jar com.example.App   # AppCDS 生成归档
java -XX:SharedArchiveFile=app.jsa -cp app.jar com.example.App      # 复用归档启动
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -cp app.jar com.example.App
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf -XX:AOTCache=app.aot
java -XX:AOTCacheOutput=app.aot -cp app.jar com.example.App   # JDK 25 一步完成（JEP 514）
java -XX:AOTCache=app.aot -cp app.jar com.example.App         # 生产运行只给缓存

# ---- 裁剪运行时 ----
jlink --add-modules java.base --strip-debug --no-header-files --no-man-pages \
      --compress=zip-6 --output myjre
jpackage --type app-image --input target --main-class com.example.App --name myapp
native-image -O2 -cp app.jar com.example.App app-native   # GraalVM，默认 -O2，另有 -O0/-O1/-O3/-Ob/-Os
```

`javac` 唯一的「优化」是常量折叠和字符串拼接的 `invokedynamic` 化，字节码层面看不到循环变换或内联，这正是 JDK 的设计：把优化留给能看到真实运行剖面的 JIT。分层编译的层级含义要记牢：第 1 层是 C1 不带 profiling、第 2 层是 C1 带有限 profiling、第 3 层是 C1 带完整 profiling、第 4 层是 C2；`-XX:TieredStopAtLevel=1` 因此适合「跑完就退出」的命令行工具，对长时间运行的服务反而是灾难，因为它永远拿不到 C2 的峰值性能。启动加速有两条独立路线：AppCDS／AOT cache 只把**类的加载与链接**提前，不改优化（JEP 483 在 JDK 24 引入 AOT 缓存，JEP 514 在 JDK 25 加了 `-XX:AOTCacheOutput` 一步式工作流），而 GraalVM `native-image` 才是真正的提前编译，它自己也有 `-O0`、`-O1`、`-O2`（默认）、`-O3`、`-Ob`、`-Os` 一组等级，代价是失去动态类加载与反射的便利，反射与资源要在配置里显式声明。

📘 [`javac` 手册（JDK 25）](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javac.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 把优化完全交给编译器实现，标准只说「as-if 规则」：只要可观察行为不变，编译器可以做任何变换。因此 C++ 的优化等级是纯命令行概念，`-O0` 到 `-O3` 外加体积取向的 `-Os`、`-Oz`，调试取向的 `-Og`，以及放松浮点语义的 `-Ofast`。除等级之外还有一层独立的开关是目标指令集：`-march`、`-mtune`、`-mcpu` 决定能不能用上向量指令。最该先知道的是：优化等级与 `-march=native` 是两件正交的事，前者是「做多少变换」，后者是「允许用哪些指令」。

```cpp
# 实测（clang 21 / Apple Silicon，fib(38)）
clang++ -std=c++23 -O0 bench.cpp -o cpp_0 && ./cpp_0        # 39088169，real 0.13s
clang++ -std=c++23 -O2 bench.cpp -o cpp_2 && ./cpp_2        # 39088169，real 0.07s
clang++ -std=c++23 -O3 bench.cpp -o cpp_3 && ./cpp_3        # 39088169，real 0.06s
clang++ -std=c++23 -Os bench.cpp -o cpp_s                   # 体积优先
clang++ -std=c++23 -Oz bench.cpp -o cpp_z                   # 体积优先（clang 更激进）
clang++ -std=c++23 -Og bench.cpp -o cpp_g                   # 面向调试的轻度优化
clang++ -std=c++23 -Ofast bench.cpp -o cpp_fast
# clang++: warning: argument '-Ofast' is deprecated; use '-O3 -ffast-math'
#   for the same behavior, or '-O3' to enable only conforming optimizations
#   [-Wdeprecated-ofast]        ← clang 21 起 -Ofast 已弃用

clang++ -std=c++23 -O2 -march=native -mtune=native bench.cpp -o cpp_native && ./cpp_native
clang++ -std=c++23 -O2 -march=armv8.4-a bench.cpp -o cpp_mar  # 显式指定微架构
clang++ -std=c++23 -O2 -flto bench.cpp -o cpp_lto            # 链接时优化
clang++ -std=c++23 -O2 -flto -fuse-ld=lld bench.cpp -o cpp_lld
# clang++: error: invalid linker name in argument '-fuse-ld=lld'   ← 未安装 lld 时如此
clang++ -std=c++23 -O2 -fvisibility=hidden -c bench.cpp -o b.o    # 隐藏符号，利于 DCE
g++ -std=c++23 -O3 -march=native -flto -fuse-linker-plugin bench.cpp -o cpp_gcc
```

`-O0` 保留一切、编译最快、`gdb`/`lldb` 的单步最准，是唯一的调试等级；`-O1` 做廉价变换；`-O2` 是绝大多数场景的默认建议值，它在不显著增大体积的前提下开启向量化与内联；`-O3` 额外做更激进的内联与循环展开，对大程序可能反而更慢（指令缓存压力）；`-Os`/`-Oz` 反过来以体积为目标；`-Og` 为调试体验做了取舍，比 `-O0` 快又比 `-O2` 好调试。⚠️ `-Ofast` 会打开 `-ffast-math`，破坏 IEEE 754 的严格性（`NaN` 传播、结合律、`errno` 都不再保证），clang 21 已明确建议改用 `-O3 -ffast-math` 或干脆只用 `-O3`。另一类陷阱是把 `-march=native` 用于发布：产物只能在构建机上跑，换一台没有 AVX-512 的机器就是 `SIGILL`，跨机分发必须显式写死基线架构。

📘 [Clang 命令行参考](https://clang.llvm.org/docs/CommandGuide/clang.html)

{{% /tab %}}

{{% tab header="C" %}}

C 和 C++ 共用同一套 `-O` 家族，但 C 的处境更极端：语言标准完全不管优化，`-O2` 下那些「看起来能跑」的未定义行为随时可能变成另一个结果。C 的选项集合与 C++ 一致——`-O0`、`-O1`、`-O2`、`-O3`、`-Os`、`-Oz`、`-Og`、`-Ofast`，再加 `-march`/`-mtune` 调目标指令集。最该先知道的是：优化等级是**编译器实现**的概念，不是语言规范的概念，换编译器或换版本，同一段代码的「优化后行为」就可能不同。

```c
# 实测（clang 21，fib(38)）
clang -O0 fib.c -o f0 && ./f0        # 39088169，real 0.13s
clang -O2 fib.c -o f2 && ./f2        # 39088169，real 0.06s
clang -O3 fib.c -o f3                # 更激进的向量化与内联
clang -Os fib.c -o fs                # 体积优先
clang -Oz fib.c -o fz && ./fz        # 39088169
clang -Og fib.c -o fg                # 调试友好的轻度优化，仍可用 gdb
clang -O2 -march=native -mtune=native fib.c -o fn
clang -O2 -flto -ffunction-sections -fdata-sections fib.c -Wl,-dead_strip -o flto_s
clang -O1 -fsanitize=undefined -fno-sanitize-recover=all fib.c -o fub   # 见「调试与分析开关」

# 优化等级导致的 UB 差异（经典例子）
clang -O0 -xc - <<'EOF' -o ub0 && ./ub0; echo "O0 exit=$?"
#include <stdio.h>
int main(void){ int x = 2147483647; x += 1; printf("%d\n", x); return 0; }
EOF
clang -O2 -xc - <<'EOF' -o ub2 && ./ub2; echo "O2 exit=$?"
#include <stdio.h>
int main(void){ int x = 2147483647; x += 1; printf("%d\n", x); return 0; }
EOF
# clang -fsanitize=undefined 下会明确报：
# runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'

gcc -O2 -march=x86-64-v3 -mtune=generic fib.c -o fx    # 交叉分发的做法：写死基线
gcc -O2 -flto=auto -fuse-linker-plugin fib.c -o fglto
size ./f0 ./f2 2>/dev/null || stat -f%z f0 f2
```

`-O0` 是唯一能保证「源码逐行对应汇编」的等级，也是 `valgrind` 与 `-fsanitize` 默认搭配的等级。`-O2` 是发布默认，`-O3` 只在剖面证明有收益时才用；`-Og` 是 GCC 引入、clang 也支持的调试等级。⚠️ 两个最常见的坑：一是把 `-O2` 下的 UB 当作「代码没问题」的证据，二是用 `-march=native` 编译要分发的二进制。GCC 与 clang 都提供 `-fno-strict-aliasing`、`-fwrapv` 之类的「关掉某类优化」的开关，当代码里有依赖溢出的逻辑时，改语义正确的写法永远优于关优化。

📘 [GCC 手册 · 优化选项](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的优化等级属于**运行期 JIT** 的范畴：`-O0` 到 `-O3`（默认 2）控制 LLVM 优化管线，但每个函数是在第一次用具体类型调用时才被特化编译的，因此同一份源码可以针对 `Int64` 和 `Float64` 生成两份完全不同的机器码。与 `-O` 正交的还有几组开关：`--check-bounds` 控制数组边界检查、`--math-mode` 控制浮点严格性、`--compile` 控制预编译激进程度。最该先知道的是：Julia 的性能主要来自类型稳定（type stability）而不是抬高 `-O` 等级。

```julia
# ---- 命令行（julia 1.13）----
julia -O0 script.jl      # 关掉大部分 LLVM 优化，最快出结果，最慢运行
julia -O2 script.jl      # 默认
julia -O3 script.jl      # 更激进
julia -O script.jl       # 单独给 -O 等价于 -O3
julia --min-optlevel=2 script.jl     # 设定全局最低优化等级（影响依赖包）
julia --check-bounds=yes script.jl   # 强制保留边界检查
julia --check-bounds=no  script.jl   # 关掉边界检查，最快也最危险
julia --compile=min script.jl        # 最少编译：只解释，启动最快
julia --compile=all script.jl        # 预编译所有方法
julia --math-mode=ieee script.jl     # 严格 IEEE 浮点（@fastmath 也无效）
julia --math-mode=user script.jl     # 默认：@fastmath 区块放宽
julia --strip-metadata --strip-ir    # 打包时去掉文档与 IR

# ---- 代码内观察 ----
julia -e '@time sum(i*i for i in 1:10^7)'
#   0.012345 seconds (1 allocation: ...)   ← 编译时间会算进第一次调用
julia -e '@allocated sum(i*i for i in 1:10^7)'   # 看分配字节数，0 才是好代码
julia -e 'using InteractiveUtils; @code_warntype (x -> x + 1)(1)'
julia -e 'using Pkg; Pkg.precompile()'           # 预编译所有依赖，缩短首次加载
ls ~/.julia/compiled/v1.13/                      # 编译缓存落在 .ji 文件里
```

`-O0` 的意义在于「跳过编译等结果」，做数值实验与调试时能省掉大量编译时间；生产代码几乎总是用默认的 `-O2`。`--check-bounds=no` 是 Julia 里最容易被滥用的开关：官方的 `@inbounds` 已经能在局部关掉检查，全局 `--check-bounds=no` 会让每个越界访问变成静默内存错误，只能配合 `--check-bounds=yes` 的测试跑一遍再上。⚠️ `--math-mode` **只有 `ieee` 与 `user` 两个取值**，没有 `fast`；要放宽浮点必须写 `@fastmath`（`user` 模式下才生效）或 `@simd`。启动时间靠 `--compile=min` 与预编译缓存 `.ji` 优化，包作者应当把重活放进 `PrecompileTools` 的 `@compile_workload`，而不是简单抬高 `-O`。

📘 [Julia · 命令行开关](https://docs.julialang.org/en/v1/manual/command-line-interface/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有两套优化机制叠在一起：编译期由 `csc` 根据 `Optimize` 属性决定是否做基本的 IL 优化，运行期由 .NET 的分层编译决定真正的机器码质量。`Debug` 与 `Release` 两个配置的差别就落在 `Optimize`、`DebugType` 这几个 MSBuild 属性上；再往上还有 `PublishReadyToRun` 与 `PublishAot` 两条提前编译路线。最该先知道的是：**分层编译自 .NET Core 3.0 起默认开启**，所以「Release 就一定跑得快」这个直觉并不成立，冷启动阶段跑的是 quick JIT 生成的代码。

```csharp
# ---- 编译期：Debug/Release 只是属性组合 ----
dotnet build -c Debug          # <Optimize>false</Optimize>
dotnet build -c Release        # <Optimize>true</Optimize>
csc /optimize+ Program.cs      # 等价的 csc 命令行写法
csc /debug:portable Program.cs # DebugType 的 csc 写法，portable 是默认值

# .csproj 里显式控制
# <PropertyGroup Condition="'$(Configuration)' == 'Release'">
#   <Optimize>true</Optimize>
#   <DebugType>none</DebugType>   <!-- full, pdbonly, portable, embedded, none -->
# </PropertyGroup>
# <DebugType>portable</DebugType> 是 Debug 与 Release 的共同默认值，都会生成 PDB

# ---- 运行期：分层编译与动态 PGO ----
DOTNET_TieredCompilation=1 dotnet bin/Release/net10.0/app.dll   # 默认即开启
DOTNET_TieredCompilation=0 dotnet bin/Release/net10.0/app.dll   # 关掉分层，直接上优化 JIT
DOTNET_TieredPGO=1 dotnet bin/Release/net10.0/app.dll           # 动态 PGO（.NET 6+）
DOTNET_TC_QuickJit=0 dotnet bin/Release/net10.0/app.dll         # 跳过 quick JIT
dotnet bin/Release/net10.0/app.dll                              # 也可以在 runtimeconfig.json 里覆盖

# ---- 提前编译 ----
dotnet publish -c Release -r linux-x64 -p:PublishReadyToRun=true
dotnet publish -c Release -r linux-x64 -p:PublishReadyToRun=true -p:PublishReadyToRunComposite=true
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
dotnet publish -c Release -r linux-x64 -p:PublishAot=true -p:OptimizationPreference=Size
# OptimizationPreference 取 Size 或 Speed；不写就由 Native AOT 自行权衡
```

`Optimize` 只影响 IL 层面很小的一部分变换（例如未使用局部变量、简单内联提示），因为它把重活留给了 JIT。`DebugType` 的默认值 `portable` 意味着 Debug 与 Release 都会产出 PDB，要彻底去掉调试信息必须显式写 `<DebugType>none</DebugType>`，⚠️ 只设 `<DebugSymbols>false</DebugSymbols>` 在 .NET 8 之后并不可靠。`PublishReadyToRun` 把 IL 提前编译成机器码，但**仍然保留 JIT**（用于分层优化与不支持 R2R 的方法），所以它优化的是启动而不是峰值，而且必须指定 `-r <RID>`，因为 R2R 镜像是平台与架构相关的；复合 R2R（`PublishReadyToRunComposite`）能把跨程序集内联也做进去，代价是发布变慢。`PublishAot` 才是完全去掉 JIT 的真 AOT，其代价是硬性限制：没有动态加载、没有 `System.Reflection.Emit`、没有 C++/CLI、Windows 上没有内置 COM，并且强制要求裁剪、强制单文件，`System.Linq.Expressions` 永远走解释形式。

📘 [.NET 运行时配置 · 编译](https://learn.microsoft.com/en-us/dotnet/core/runtime-config/compilation)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的「优化等级」分裂成两条互不相通的路径：开发时用 `dart run`，代码由 VM 的 JIT 编译；发布时用 `dart compile exe` 走 AOT，把整个程序编译成原生机器码并且**没有 `-O` 等级可调**。带 `-O0` 到 `-O4` 的只有 Web 方向的 `dart compile js` 与 `dart compile wasm`。最该先知道的是：AOT 产物的优化是「全程序编译 + tree shaking」自动完成的，不需要也不提供等级旋钮。

```dart
# ---- 开发期：JIT ----
dart run bin/myapp.dart
dart run --enable-asserts bin/myapp.dart      # 打开断言
dart run --observe bin/myapp.dart             # 启动 VM service，供 DevTools 连接

# ---- 发布期：AOT，没有 -O 等级 ----
dart compile exe bin/myapp.dart -o /tmp/myapp
# Generated: /tmp/myapp
dart compile exe bin/myapp.dart -o /tmp/myapp --target-os=linux --target-arch=arm64
dart compile aot-snapshot bin/myapp.dart      # 只出 .aot 模块，不打包运行时
dartaotruntime bin/myapp.aot                  # 用 dartaotruntime 运行
dart compile jit-snapshot bin/myapp.dart      # 带训练数据的 JIT 快照
dart compile kernel bin/myapp.dart            # 平台无关的 Kernel IR（.dill）

# ---- Web：-O0 到 -O4 只在这里 ----
dart compile js -O0 -o out/main.js web/main.dart   # 关掉大量优化，便于阅读产物
dart compile js -O1 -o out/main.js web/main.dart   # 默认优化
dart compile js -O2 -o out/main.js web/main.dart   # 增加压缩等对语义安全的优化
dart compile js -O3 -o out/main.js web/main.dart   # 再省掉隐式类型检查
dart compile js -O4 -o out/main.js web/main.dart   # 比 -O3 更激进，对输入分布敏感
dart compile js --no-source-maps -o out/main.js web/main.dart
dart compile wasm -O2 --minify --strip-wasm -o out/main.wasm web/main.dart

# 混淆与调试符号分离是 flutter build 的选项（dart compile exe 的文档里没有）
# flutter build apk --obfuscate --split-debug-info=build/app/outputs/symbols
```

`dart compile js` 的四个等级语义很清楚：`-O0` 关掉大量优化以便调试、`-O1` 是默认、`-O2` 在 `-O1` 基础上做压缩等对所有程序都安全的优化（但类型的字符串表示会与 VM 下不同）、`-O3` 开始省略隐式类型检查、`-O4` 比 `-O3` 更激进。⚠️ `-O3` 与 `-O4` 会让类型错误从「抛 `TypeError`」变成「静默算错或崩溃」，官方明确要求先用 `-O2` 回归、确认程序从不抛 `Error` 的子类，`-O4` 还要额外覆盖边界输入。AOT 侧没有等级，因为 `dart compile exe` 做的是整程序编译，tree shaking 会自动剔除不可达的类、函数与方法；真正影响体积的选项是 `--target-os`/`--target-arch` 这类目标选择，以及先 `dart compile kernel` 再喂给 `aot-snapshot`。⚠️ `--obfuscate` 与 `--split-debug-info` 常被当成 Dart CLI 选项，其实它们是 Flutter 构建的选项；纯 Dart 侧只有 `--save-debugging-info` 这类未在 `dart compile` 文档页列出的隐藏开关，不要照抄。

📘 [`dart compile`](https://dart.dev/tools/dart-compile)

{{% /tab %}}

{{% tab header="R" %}}

R 没有编译期优化等级，只有**字节码编译器 + JIT** 的一套级别：`compiler::enableJIT(level)` 接受 0 到 3 四个档，默认就是 3；级别越高，越多闭包与顶层循环会在执行前被编译成字节码。它属于运行期机制，与 C 系语言的 `-O` 完全不是一回事；R 也没有把脚本编译成独立可执行文件的官方通道。最该先知道的是：包在安装时默认已经做过字节码编译（`ByteCompile` 默认开启），所以「R 慢是因为没编译」通常是误会。

```r
# ---- JIT 级别 ----
R --vanilla -q -e 'compiler::enableJIT(-1)'      # 3   负值表示查询当前级别
R --vanilla -q -e 'compiler::enableJIT(0)'       # 全部解释执行
R_ENABLE_JIT=0 Rscript opt.R                     # 用环境变量在同一进程启动前关掉
R_ENABLE_JIT=3 Rscript opt.R                     # 环境变量也能指定级别

# 级别含义：0 关闭；1 较大的闭包在首次使用前编译；
# 2 一些小的闭包也在第二次使用前编译；3 额外把所有顶层循环在执行前编译
# 级别 3 要求编译器选项 optimize 为 2 或 3

# ---- 手工编译与观察 ----
Rscript -e 'f <- function(n) sum((1:n)^2); g <- compiler::cmpfun(f); print(g(1000))'
# [1] 333833500
Rscript -e 'print(compiler::disassemble(compiler::cmpfun(function(x) x + 1)))'
# 打印字节码：list(...) 形式的指令序列
Rscript -e 'print(compiler::getCompilerOption("optimize"))'   # 2 或 3
Rscript -e 'print(compiler::enableJIT(-1))'                   # 3

# ---- 包安装时的编译 ----
# DESCRIPTION 里：ByteCompile: yes      ← 默认就是字节编译
R CMD INSTALL --no-byte-compile mypkg   # 显式关掉
R CMD INSTALL --preclean mypkg          # 先清理再编译
_R_CHECK_CONSTANTS_=1 R_JIT_STRATEGY=3 R CMD check mypkg   # 更严格的常量检查
Rscript -e 'print(.Platform$OS.type)'   # "unix"
```

`enableJIT` 的非零三个级别是**编译时机**的差别，不是优化力度：级别 1 只处理较大的闭包（避免为小函数浪费编译时间），级别 2 把一些小闭包提前编译，级别 3 连顶层 `for` 循环也编译。因为默认已经是 3，绝大多数脚本不需要调它；⚠️ 只有在调试字节码相关问题时才把级别降到 0，否则会明显变慢。`cmpfun`/`compile`/`cmpfile` 用来手动编译单个闭包或整个文件（产出 `.Rc`，用 `loadcmp` 装载），是作者控制编译粒度的工具。发布层面 R 没有 `--strip-ir` 之类的选项，官方路径是把源码或已安装的包打包成 `.tar.gz` 并通过 lazy-load 数据库加速装载，所谓「二进制包」也只是安装结果的压缩拷贝，不是可执行文件。

📘 [R · compiler 包参考手册](https://cran.r-project.org/doc/manuals/r-release/packages/compiler/refman/compiler.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 用四个**构建模式**代替了优化等级，每个模式同时决定「优化力度」与「安全检查是否开启」这两件事：`Debug`、`ReleaseSafe`、`ReleaseFast`、`ReleaseSmall`，默认是 `Debug`。它属于构建期静态优化，模式之间不只是速度差异，而是语义差异——`ReleaseFast` 与 `ReleaseSmall` 会关掉整数溢出、越界等安全检查。最该先知道的是：想要「既快又不失控的 UB」，正确答案是 `ReleaseSafe`，它是 Zig 与 C 最大的区别所在。

```zig
# 实测可用的四种模式（zig 0.15）
zig build-exe main.zig -O Debug          # 默认：优化关、安全检查开、编译最快
zig build-exe main.zig -O ReleaseSafe    # 安全检查开 + 完整优化
zig build-exe main.zig -O ReleaseFast    # 安全检查关 + 最快运行
zig build-exe main.zig -O ReleaseSmall   # 安全检查关 + 体积最小
zig build-exe main.zig -OReleaseFast     # 紧贴写法同样被接受
zig build -Doptimize=ReleaseFast         # zig build 用 -Doptimize
zig build --release=fast                 # zig build 专用简写：fast, safe, small

zig build-exe main.zig -O ReleaseFast -fstrip      # 去调试符号（没有 --strip）
zig build-exe main.zig -O ReleaseSmall -target x86_64-linux
zig build-exe main.zig -O ReleaseSafe -fsanitize-c # C 代码的 UBSan 检查
zig build-exe main.zig -O ReleaseSafe -fsanitize-c=trap   # 0.15 新增：越界即 trap
zig test main.zig -O Debug --verbose-air           # 打印 AIR，观察优化前后差异
zig cc -target aarch64-linux-gnu -O2 hello.c -o hello   # 拿 zig 当交叉编译器
zig targets | head -20                             # 列出支持的目标三元组
```

`Debug` 下所有安全检查都在，是唯一适合排查 UB 的模式；`ReleaseSafe` 保留安全检查但做完整优化，是服务端与需要确定性的场景的推荐选择；`ReleaseFast` 追求峰值性能、`ReleaseSmall` 追求体积，两者都会关掉安全检查，越界访问与整数溢出将变成真正的 UB。⚠️ 两个常见误记：`zig build-exe --strip` 并不存在，去符号要用 `-fstrip`；`--release=fast` 只是 `zig build` 的简写，`zig build-exe` 并不接受它，直接编译要用 `-O ReleaseFast`。`zig cc` 与 `zig c++` 是另一条独立能力：它内置了 libc 与目标平台的 sysroot，因此不装交叉工具链也能用 `-target` 直接产出其他平台的可执行文件，这也是 Zig 在构建系统里最常见的用法。

📘 [Zig 语言参考 · 构建模式](https://ziglang.org/documentation/0.15.1/#Build-Mode)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有优化等级这个概念：`luac` 与 `lua` 都不接受 `-O`，语言规范里也没有「优化级别」这一项。存在的只有**编译成字节码**（`luac`，或 `lua` 载入时的隐式编译）与**剥离调试信息**（`luac -s`）两件事，优化本身由编译器在生成字节码时无条件完成，最典型的是常量折叠。最该先知道的是：Lua 的 `<const>` 属性不是给程序员看的修饰，它会让编译器把对这些变量的访问也折叠成常量。

```lua
lua main.lua                       # 解释执行，没有优化等级
luac -v                            # Lua 5.5.x
luac -p main.lua                   # 只做语法检查，不产出文件
luac -o main.luac main.lua         # 预编译成字节码
luac -l main.luac                  # 列出字节码
luac -l -l main.luac               # 完整列出（含常量表）
luac -s -o main.luac main.lua      # 剥离调试信息，这是 luac 唯一的体积开关
lua main.luac                      # 直接运行字节码
lua -e 'local x <const> = 2 ^ 10; print(x)'
# 1024          ← 常量折叠在编译期完成
lua -e 'local t <const> = {1,2,3}; print(#t)'
# 3             ← <const> 让编译期可以做更强的常量传播
lua -e 'local i = 0; for k = 1, 3 do i = i + k end; print(i)'
# 6
luac -l -l -e 2>/dev/null; echo "(luac 没有 -O 选项，见 Lua 5.5 手册与 luac 手册页)"
```

`luac` 的选项集合是固定的：`-l` 列表、`-o` 输出、`-p` 只解析、`-s` 剥调试信息、`-v` 版本、`--` 结束选项、`-` 从标准输入读，**没有 `-O`**。同一份源码无论用 `lua` 直接跑还是用 `luac` 预编译，生成的字节码是一样的，`luac` 带来的唯一收益是省掉启动时的解析与编译，对启动敏感的 CLI 有意义。⚠️ 必须澄清一个常见说法：Lua 5.5 **没有**文档化的「常量折叠变更」，官方手册里连「folding」这个词都没出现，5.5 相对 5.4 的正式不兼容点集中在语言层——`global` 成了保留字（不要再用作普通变量名）、`for` 循环的控制变量变成只读、`__call` 元方法链最多 15 个对象、`nil` 错误对象被替换成字符串消息；GC 参数改用统一的 `param` 选项。要真正影响运行速度，应当关注 `<const>` 与 `<close>` 这类能改变编译器决策的属性，而不是寻找并不存在的优化等级。

📘 [Lua 5.5 参考手册 · 不兼容变更](https://www.lua.org/manual/5.5/manual.html#8)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有「优化等级」，因为 `tsc` 不是优化编译器：它的工作是类型检查加语法降级（downlevel），把 TS 转成目标版本的 JavaScript，运行期优化完全由宿主引擎负责。TypeScript 7 值得单独记一笔——它是用 Go 重写的原生编译器，官方称完整构建有 10 倍量级的加速，此前预览版的 `tsgo` 名字已并入正式 `tsc`。与「优化」最接近的旋钮其实是 `target`、`module` 与 `incremental` 三个编译选项。

```typescript
npm install -D typescript
npx tsc --version                 # Version 7.x（Go 原生实现）
npx tsc                           # 按 tsconfig.json 编译整个项目
npx tsc --noEmit                  # 只做类型检查，不产出文件
npx tsc --target es2023 --module nodenext --moduleResolution nodenext
npx tsc --lib es2023,dom                        # 选定可用的标准库接口
npx tsc --incremental --tsBuildInfoFile .tsbuildinfo   # 增量编译
npx tsc --build                   # 项目引用模式的增量构建
npx tsc --checkers 4              # TS 7 新增：并行类型检查器数量
npx tsc --builders 4              # TS 7 新增：并行项目构建器数量
npx tsc --singleThreaded          # TS 7 新增：单线程，便于复现与排查
npx tsc --isolatedModules --verbatimModuleSyntax   # 保证逐文件转译语义一致
npx tsc --removeComments --declaration false
cat tsconfig.json
# { "compilerOptions": { "target": "es2023", "module": "nodenext",
#     "moduleResolution": "nodenext", "incremental": true, "strict": true } }
```

`target` 决定输出里能保留哪些新语法：调高它产出的代码更接近源码、更少 helper、体积更小、可读性更好，但要求运行环境支持；调低它就要为 `async`、类字段、可选链等生成降级代码，产物更大。这不是「优化等级」，而是「目标环境声明」。⚠️ TS 7 改了默认值并收紧了旧配置：`target: es5`、`downlevelIteration`、`moduleResolution: node/node10/classic`、`module: amd/umd/systemjs/none`、`baseUrl` 等都变成硬错误，`strict` 默认打开，升级时最容易踩的就是这一组。真正的体积与运行期优化发生在 `tsc` 之后：由 esbuild、Rollup、terser 这类打包器做 tree shaking 与压缩，`tsc` 只负责把类型擦掉并生成 `.js`、`.d.ts` 与 source map。想加速构建有三条正交手段：`incremental`/`--build` 复用上次结果、TS 7 的并行 `--checkers`/`--builders`、以及把类型检查与转译分离（`--isolatedModules` + 第三方转译器）。

📘 [TypeScript 7.0 发布公告](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有编译期优化选项：源码由引擎在运行时解释执行，热点函数被 JIT 编译成机器码，V8 的三层分别是基线编译器 Sparkplug、中层 Maglev 与顶层 Turbofan。Node 暴露出来的 `--max-old-space-size`、`--jitless` 之类的开关属于**运行时选项**，控制的是内存上限与 JIT 是否启用，而不是优化力度。最该先知道的是：想「调优」Node 程序，真正有效的通常是减少分配与反优化（deopt），而不是找 `-O`。

```javascript
node -v                                   # 本机 v24.20.0（文档按 Node 26 书写）
node main.js
node --max-old-space-size=512 main.js     # 限制老生代；实测默认上限约 4288 MB
node -e 'console.log((require("v8").getHeapStatistics().heap_size_limit/1048576).toFixed(1))'
# 4288.0
node --max-old-space-size=64 -e 'console.log(require("v8").getHeapStatistics().heap_size_limit/1048576)'
# 256                     ← 下限被钳到 256 MB
node --jitless main.js                    # 关掉 JIT，只解释执行
node --v8-options | grep -E "maglev|turbofan" | head -5
# --maglev (enable the maglev optimizing compiler)
# --maglev-inlining (enable inlining in the maglev optimizing compiler)
node --trace-deopt main.js                # 打印反优化事件，找出「优化又退回」的函数
node --allow-natives-syntax -e 'function f(x){return x+1}; %OptimizeFunctionOnNextCall(f); f(1)'
node --cpu-prof --cpu-prof-dir=./prof main.js && ls prof/
# CPU.20260919.181846.29993.0.001.cpuprofile
node --prof main.js && ls isolate-*.log
# isolate-0x8a540c000-30010-v8.log        ← 用 node --prof-process 解析
node --build-snapshot --snapshot-blob snapshot.blob main.js   # 生成启动快照
node --snapshot-blob snapshot.blob main.js                    # 用快照启动
node --experimental-sea-config sea-config.json                # 单文件可执行（SEA）
```

V8 的编译管线是分层的：先解释执行，调用够热后由 Sparkplug 生成基线代码，再热则交给 Maglev，最热才上 Turbofan；每一层都会根据运行时的类型反馈做投机优化，一旦类型假设被打破就触发 deopt 回到解释器。因此 `--trace-deopt` 往往比任何「优化等级」都有用——一个反复 deopt 的热函数会把性能吃掉一大半。⚠️ `--max-old-space-size` 是堆上限而不是优化开关，设得太小会让 GC 频繁触发甚至 OOM，实测把它设成 64 会被钳到 256 MB 下限。启动优化走的是另一条路：`--build-snapshot` 与 `--snapshot-blob` 把模块初始化结果固化成快照，`--experimental-sea-config` 则生成单文件可执行程序。本机装的是 Node 24，而版本基线按 Node 26 书写，`--jitless`、`--cpu-prof`、`--prof`、快照与 SEA 这几组行为在两者之间一致。

📘 [Node.js · 命令行选项](https://nodejs.org/api/cli.html)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的「优化」完全发生在运行期的 OPcache 里：Zend VM 先把源码编译成 opcode，OPcache 把这层 opcode 缓存在共享内存中，避免每次请求都重新编译；在此之上还有可选的 JIT，把热点 opcode 直接编译成机器码。⚠️ 最该先知道的一点是：**JIT 默认是关闭的**，`opcache.jit` 的默认值自 8.4.0 起是 `disable`，所以「升级到 PHP 8 就有 JIT 加速」是不成立的，必须显式打开。PHP 也**没有** `-O` 之类的编译期优化等级：`opcache.optimization_level` 只是一个按位控制优化 pass 的位掩码（默认 `0x7FFEBFFF`），不是分档的等级。

```php
php -v
php -l main.php                          # 只做语法检查
php --ini                                # 显示实际加载的 ini 文件
php --ini=diff                           # 8.5 新增：只打印与内置默认值不同的项

php -d opcache.enable_cli=1 main.php     # 命令行下也要显式开启 OPcache
php -d zend_extension=opcache \
    -d opcache.enable_cli=1 \
    -d opcache.jit=tracing \
    -d opcache.jit_buffer_size=64M \
    main.php
php -i | grep -i -E "opcache.jit|opcache.enable" | head
# opcache.enable => On
# opcache.jit => disable          ← 默认值，必须手动改成 tracing 或 function
# opcache.jit_buffer_size => 64M

php -d opcache.preload=preload.php main.php     # 预加载，把框架代码提前编译进共享内存
php -r 'var_dump(opcache_compile_file("lib.php"));'   # 手工预热单个文件
php -d opcache.jit=1254 main.php                # 整数 CRTO 形式：tracing 等价于 1254
php -d opcache.jit=function main.php            # 函数级 JIT，等价于 1205
php -d opcache.jit=off main.php                 # 只缓存 opcode，不做 JIT
```

`opcache.jit` 有两套写法：字符串取 `disable`、`off`、`tracing`（别名 `on`）、`function`，整数则是四位 CRTO 编码，分别代表 CPU 特定优化、寄存器分配、触发时机与优化级别；`tracing` 等价于 `1254`、`function` 等价于 `1205`。选 `tracing` 还是 `function` 要看负载：`tracing` 峰值更高但编译开销大，适合长驻的 Web 进程；`function` 编译单个函数、启动开销小，适合短命脚本。⚠️ `opcache.jit_buffer_size` 为 0 会彻底禁用 JIT，而 `opcache.enable_cli` 默认关闭意味着你在命令行测出的结果不代表 Web 表现。PHP 8.5 在 JIT 上没有新功能，唯一的 OPcache 变更只是把 `opcache.jit_hot_loop` 的默认值从 64 调到 61；真正的体积与启动优化仍然是 OPcache 的 opcode 缓存加 `opcache.preload`，打包侧则是 `.phar` 与 Composer 的 `dump-autoload --classmap-authoritative`。

📘 [PHP · OPcache 配置](https://www.php.net/manual/en/opcache.configuration.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的优化等级体现在**运行时 JIT 开关**上：默认每条指令都走 YARV 字节码解释器，`--yjit` 打开 YJIT（基于基本块复制的方法级 JIT），`--zjit` 打开 Ruby 4.0 新引入的 ZJIT（更传统的 SSA IR 方法编译器），而 `--jit` 只是 `--yjit` 的别名。⚠️ 最该先知道的两件事：Ruby 4.0 已经**移除** `--rjit`，且 ZJIT 官方明确说目前比 YJIT 慢、不建议上生产。

```ruby
ruby opt.rb                       # 默认：纯解释执行
ruby --yjit opt.rb                # 启用 YJIT
ruby --jit opt.rb                 # 等价于 --yjit
ruby --zjit opt.rb                # ZJIT（4.0 起，实验性）
ruby --yjit --yjit-stats opt.rb   # 打印 YJIT 统计
ruby --yjit --yjit-mem-size=256 --yjit-call-threshold=10 opt.rb
ruby --zjit --zjit-mem-size=128 --zjit-call-threshold=30 opt.rb
ruby --rjit opt.rb
# ruby: invalid option --rjit  (-h will show valid options) (RuntimeError)   ← 4.0 已移除
ruby -e 'puts RubyVM::YJIT.enabled?'            # false   未开 JIT
ruby --yjit -e 'puts RubyVM::YJIT.enabled?'     # true
ruby --zjit -e 'puts defined?(RubyVM::ZJIT) ? "ZJIT 常量存在" : "无"'
# ZJIT 常量存在
ruby --yjit --yjit-stats -e 's=0; 1_000_000.times{|i| s+=i*i}; puts s' 2>&1 | tail -6
# yjit_insns_count:         11,999,652
# side_exit_count:                   0
# total_exit_count:            999,971
# code_region_size:             16,384
ruby --disable-gems -e 'puts "gems off"'        # 不加载 RubyGems，启动更快
ruby -e 'puts RUBY_DESCRIPTION'
```

YJIT 与 ZJIT 都是**运行期**优化，与编译期无关：Ruby 源码永远先编译成 YARV 指令序列，JIT 只是在方法变热后把这段字节码再编译一次。`--yjit-stats` 的读数很有信息量——`yjit_insns_count` 是 JIT 生成的指令数、`total_exit_count` 是从 JIT 代码退回解释器的次数、`ratio_in_yjit` 表示真正跑在 JIT 里的比例；⚠️ Ruby 4.0 起 `ratio_in_yjit` 在默认构建里不再可用，必须在 `configure` 时加 `--enable-yjit=stats` 才能看到。ZJIT 的定位要写清楚：它用更大的编译单元与 SSA IR 换取更高的性能天花板，但 4.0 时「比解释器快、比 YJIT 慢」，官方建议只做实验；更早的 MJIT 走的是「字节码转 C 再交给系统 C 编译器」的路线，因编译开销与稳定性问题被淘汰，位置由 YJIT 与 ZJIT 取代。启动敏感的场景还可以用 `--disable-gems` 省掉 RubyGems 的加载，代价是 `require` 找不到 gem。

📘 [Ruby 4.0 · 发布说明（JIT 一节）](https://docs.ruby-lang.org/en/4.0/NEWS_md.html)

{{% /tab %}}

{{< /tabpane >}}

### 体积与链接

发布产物的体积由三段互相独立的机制叠加决定：**链接时优化（LTO）**决定跨编译单元能看到多少信息，**死代码消除（DCE）与裁剪**决定有多少代码根本不会被链进去，**静态链接还是动态链接**决定运行时要不要额外文件。三段的取舍方向并不一致：LTO 花编译时间换运行性能，DCE 同时省体积与启动时间但会破坏反射，静态链接省部署麻烦但放弃安全补丁的共享更新。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的体积与链接控制集中在 Cargo profile 的四个字段：`lto` 决定链接时优化强度（`false`、`"thin"`、`"fat"`、`"off"`），`codegen-units` 决定并行编译单元数量，`panic` 决定是否生成 unwind 表，`strip` 决定符号保留程度。此外 `-C linker-plugin-lto` 支持与 C/C++ 混编时的跨语言 LTO，`--target` 加 musl 三元组则提供真正静态的二进制。最该先知道的是：`lto = "fat"` 加上 `codegen-units = 1` 才是最激进的组合，只写其中一个收益有限。

```rust
# 实测（同一 fib(30) 程序，rustc 1.98）
rustc -C opt-level=3 bench.rs -o r3                                            # 469200 字节
rustc -C opt-level=3 -C panic=abort -C strip=symbols bench.rs -o rab           # 341776 字节
rustc -C opt-level=z -C lto=fat -C codegen-units=1 -C panic=abort -C strip=symbols bench.rs -o rmin
                                                                               # 285952 字节
rustc -C opt-level=3 -C lto=fat -C codegen-units=1 bench.rs -o rlto            # 407448 字节
./rmin                                            # 832040，行为不变

# Cargo.toml 里的等价写法
# [profile.release]
# lto = "fat"          # false, "thin", "fat", "off"
# codegen-units = 1
# panic = "abort"
# strip = "symbols"    # "none", "debuginfo", "symbols"
# opt-level = "z"
cargo build --release
cargo bloat --release --crates        # 哪个依赖最占体积
cargo tree --duplicates               # 找出被重复链接的版本
strip target/release/app              # 事后剥离也可以

# 跨语言 LTO：Rust 与 C 一起做链接时优化（需要同一 LLVM 版本）
RUSTFLAGS="-C linker-plugin-lto" cargo build --release --target x86_64-unknown-linux-gnu
clang -flto=thin -c helper.c -o helper.o

# 真正静态：musl 目标
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
file target/x86_64-unknown-linux-musl/release/app
# 静态链接，无 glibc 依赖
# Windows 上的静态 CRT：-C target-feature=+crt-static
# macOS 上没有可用的静态链接方案，只能靠 strip 与 DCE
```

`strip = "symbols"` 与 `panic = "abort"` 是体积收益最直接的两个开关，上面实测把 469200 字节压到 341776 字节，去掉的是符号表与 unwind 表。⚠️ `panic = "abort"` 会让 `catch_unwind` 失效、让 `std::panic::catch_unwind` 相关的错误恢复策略报废，同时也让某些依赖 `panic` 语义的库行为异常，因此它只适合最终的可执行文件 crate，不适合库。`lto = "thin"` 是绝大多数项目的正确默认：它在增量编译与优化强度之间取得平衡，`"fat"` 只在发布构建时值得开启，因为它会让编译时间与内存占用明显上升。`linker-plugin-lto` 是 Rust 与 C/C++ 混编项目的关键选项，⚠️ 它要求 Rust 与 clang 使用同一版本的 LLVM，否则链接时会报位码版本不匹配；跨语言 LTO 通常还能顺手消掉 Rust 与 C 之间重复的 panic 与格式化代码。

📘 [rustc · 代码生成选项](https://doc.rust-lang.org/rustc/codegen-options/index.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的体积控制分三层：编译期的 `-Osize` 与跨模块优化、链接期的 `-dead_strip`、以及运行库的链接方式（动态还是静态）。`-static-stdlib` 曾是把 Swift 运行时链进产物的常用手段，如今在 Apple 平台已被移除，只在 Linux 等平台可用，这也是 Swift 在 Linux 上发布单文件程序的主要手段。最该先知道的是：Swift 的链接器是平台链接器，GNU 的 `--gc-sections` 在这里并不通用。

```swift
# 实测（Swift 6.4 / Apple Silicon）
swiftc -O opt.swift -o sw_O                        # 50760 字节
swiftc -Osize opt.swift -o sw_Osize                # 50776 字节
swiftc -O -Xlinker -dead_strip opt.swift -o sw_ds  # 50776 字节（链接期删死代码）
swiftc -O -whole-module-optimization opt.swift -o sw_wmo        # 50696 字节
cp sw_O sw_strip && strip sw_strip                 # 事后剥离符号
swiftc -O -static-stdlib opt.swift -o sw_static
# error: -static-stdlib is no longer supported for Apple platforms
# Linux 上等价写法：swift build -c release --static-swift-stdlib

swift build -c release -Xswiftc -cross-module-optimization      # SwiftPM 跨模块优化
swift build -c release -Xswiftc -Osize -Xlinker -dead_strip
swiftc -O -emit-library -o libx.dylib lib.swift    # 动态库
install_name_tool -id @rpath/libx.dylib libx.dylib # macOS 上设置安装名
otool -L sw_O                                      # 查看动态依赖
nm -u sw_O | head                                  # 查看未定义符号
```

`-Osize` 让 LLVM 以体积为目标做内联与特化决策，通常能比 `-O` 再小几个百分点，代价是少量性能；`-whole-module-optimization` 与 `-cross-module-optimization` 让编译器能看到整个模块甚至跨模块的定义，从而删掉未使用的泛型特化与 internal 函数，这是 Swift 体积优化里收益最大的单项。⚠️ `-dead_strip` 走的是 Apple 链接器（ld64/ld-prime）的参数，在 Linux 上要用 `-Xlinker --gc-sections` 配合 `-ffunction-sections` 才有类似效果，直接照搬会报未知选项。`-static-stdlib` 的移除是平台策略变化而非全局移除：Apple 平台的 Swift 运行时由系统提供，静态链接标准库会带来巨大的体积与兼容性问题，所以官方直接禁用了；Linux 上则相反，`--static-swift-stdlib` 是发布可移植二进制的推荐做法。最终产物里还可看到 Swift 运行时与 Foundation 的动态依赖，用 `otool -L` 就能确认。

📘 [Swift 官方文档 · Swift 编译器](https://www.swift.org/documentation/swift-compiler/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 默认就把所有依赖静态链接进单一二进制，因此「体积与链接」在 Go 里主要是**怎么把已经很大的产物变小**：`-ldflags="-s -w"` 去掉符号表与 DWARF、`-trimpath` 去掉本机绝对路径、`CGO_ENABLED=0` 保证纯静态、`-buildmode` 控制产物形态。Go 没有 LTO 概念，因为整个程序本来就是一个编译单元。最该先知道的是：`-s -w` 的收益非常可观，但它同时会让 `pprof` 的符号解析退化成地址。

```go
go build -o app .
stat -f%z app                                  # 2413186 字节
go build -trimpath -ldflags="-s -w" -o app-strip .
stat -f%z app-strip                            # 1571186 字节
go build -ldflags="-s -w -X main.version=1.2.3" -o app-ver .
go tool nm app | wc -l                         # 符号条数
go version -m app                              # 查看嵌入的模块与构建信息

# 交叉编译纯静态二进制（不含 cgo）
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o app-linux-arm64 .
file app-linux-arm64
# ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), statically linked

# 其他产物形态
go build -buildmode=pie -o app-pie .
go build -buildmode=c-shared -o libapp.so .
go build -buildmode=c-archive -o libapp.a .
go build -buildmode=plugin -o plug.so .        # 平台支持有限
go build -gcflags="all=-l" -ldflags="-s -w" -o app-nol .
# -l 关闭内联往往能让体积再降一点，但会牺牲性能
go list -deps . | wc -l                        # 依赖包数量，体积的主要来源
```

Go 的二进制之所以动辄几兆，是因为运行时（GC、调度器、反射、`fmt`、`net`）全部被链进去了，`-s -w` 能砍掉的只是符号与调试信息，真正的减重手段是减少依赖与避免引入 `net/http`、`database/sql` 这类「拖家带口」的包。⚠️ `-s -w` 之后 `go tool pprof` 依然可用（Go 自带符号信息仍在 `.gopclntab` 里），但 `delve` 的调试体验会大幅下降，`runtime/debug.PrintStack` 的符号也可能不完整，所以正确的做法是保留一份未剥离的构建用于排查问题。`CGO_ENABLED=0` 是跨平台发布的关键：打开 cgo 会引入 libc 依赖，交叉编译时还需要目标平台的 C 工具链，关掉之后 `net` 包会退回到纯 Go 的解析实现，得到一个除了内核之外什么都不依赖的二进制。

📘 [`cmd/link` 文档](https://pkg.go.dev/cmd/link)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有链接期，也没有编译期优化能砍体积，所谓「体积与链接」实际是**打包与分发**：标准库自带 `zipapp` 可以把整个包塞进一个 `.pyz`，第三方工具 `PyInstaller` 能做成免安装可执行文件，`Nuitka` 与 `mypyc` 则把 Python 编译成 C 或 C 扩展。`-OO` 去掉 docstring 属于唯一「语言级」的瘦身手段，收益通常只有几个百分点。最该先知道的是：Python 的体积问题本质是解释器运行时，`zipapp` 减小的是你自己代码的体积，不是运行时的体积。

```python
python3 -m zipapp myapp -o myapp.pyz -p "/usr/bin/env python3"   # 标准库打包
python3 myapp.pyz                                                 # 直接运行
python3 -m zipapp myapp -o myapp.pyz -c                           # 顺带压缩
unzip -l myapp.pyz | head                                         # 就是个 zip

python3 -OO -m compileall -q myapp     # 去掉 docstring 的 .pyc
python3 -c "import sys; print(sys.flags.optimize)"      # 0
python3 -OO -c "import sys; print(sys.flags.optimize)"  # 2
du -sh myapp/__pycache__/

# 第三方：做成免安装可执行文件
pip install pyinstaller
pyinstaller --onefile --strip main.py       # 产物在 dist/main
pip install nuitka
python -m nuitka --standalone --onefile --follow-imports main.py
pip install mypyc
mypyc main.py                               # 编译成 C 扩展，需自己打包
pip install shiv && shiv -o myapp.pyz -e myapp:main .   # 带依赖的 zipapp
python3 -m venv --without-pip .venv         # 体积最小的隔离环境
python3 -c "import sys; print(sys.base_prefix)"   # 运行时本体所在，无法用 -OO 缩小
```

`zipapp` 只做一件事：把目录打成一个带 `__main__.py` 的 zip，运行时由解释器直接执行，因此**必须**在目标机器上有兼容的 CPython，适用于部署内部脚本而不是交付给最终用户。`PyInstaller` 与 `Nuitka` 走的是另一条路——把解释器、字节码和依赖一起塞进一个自解压文件或原生可执行文件，代价是启动变慢、体积从几兆涨到几十兆，而且对动态 `import` 与 C 扩展的兼容性需要逐个验证。⚠️ `-OO` 会把 docstring 删掉，许多框架依赖 docstring 做事（文档生成、某些 ORM 与 CLI 的自动帮助），因此它是「有语义代价的瘦身」，不是安全优化。⚠️ `mypyc` 编译的是被注解过的模块，编译失败会静默退回纯 Python，看不出加速时要检查是不是有模块没被编译。

📘 [Python · zipapp](https://docs.python.org/3/library/zipapp.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 在 JVM 上没有自己的链接器，体积与裁剪全部复用 Java 生态的工具链：`jlink` 裁运行时、`jpackage` 打安装包、R8/ProGuard 裁代码与混淆名字；Kotlin 只是提供 `-include-runtime` 打 fat jar 的便利。Kotlin/Native 是例外，它有自己的二进制选项，包括 `optimize()` 与 `bundle` 静态链接开关。最该先知道的是：**Kotlin 标准库本身就占几百 KB 到数 MB**，这是 JVM 上 Kotlin 产物比 Java 大的主要原因，也是 R8 收益最大的地方。

```kotlin
kotlinc Main.kt -include-runtime -d app.jar    # 自带 kotlin-stdlib 的 fat jar
ls -lh app.jar
java -jar app.jar
# hello from kotlin

# Gradle 侧：R8 做裁剪与混淆（Android 官方，JVM 服务端用 ProGuard）
# android { buildTypes { release { isMinifyEnabled = true; isShrinkResources = true } } }
# R8 规则写进 proguard-rules.pro，反射用到的类要 -keep
./gradlew assembleRelease
./gradlew shadowJar                             # 第三方插件打 fat jar（等价 -include-runtime）

# 运行时裁剪：与 Java 共用 jlink / jpackage
jlink --add-modules java.base --strip-debug --no-header-files --no-man-pages \
      --compress=zip-6 --output myjre
jpackage --type app-image --input build/libs --main-jar app.jar --name myapp
du -sh myjre

# Kotlin/Native：真正的静态链接与体积选项
# kotlin { linuxX64 { binaries { executable {
#     entryPoint = "main"
#     optimize()                                  // 开启优化（release 模式）
#     binaryOption("bundle", "STATIC")            // 静态链接
#     freeCompilerArgs += "-Xbinary=stripDebugInfo=true"
# } } } }
./gradlew linkReleaseExecutableLinuxX64
file build/bin/linuxX64/releaseExecutable/app.kexe
# Kotlin/JS 的体积交给 webpack/terser，见 JavaScript 标签页
```

在 JVM 上，`-include-runtime` 只是把 `kotlin-stdlib` 解压进同一个 jar，并不减少任何字节；真正的减重必须靠 R8/ProGuard 做可达性分析，把未使用的类、方法、字段删掉并顺带改名。⚠️ R8 与反射天然冲突：任何通过字符串或 `Class.forName` 用到的类型都必须显式 `-keep`，否则会在运行时才 `ClassNotFoundException`，这类问题在 debug 构建里不会出现，只有 release 才会暴露。`jlink` 的价值在于把 JDK 里用不到的模块整块删掉，一个只依赖 `java.base` 的服务可以把上百兆的 JRE 压到几十兆；`jpackage` 则在 `jlink` 之上再包一层平台安装器，默认已带 `--strip-debug --no-header-files --no-man-pages`。Kotlin/Native 侧是另一套语义：`STATIC` bundle 让产物不依赖 Kotlin 运行时动态库，`-Xbinary=stripDebugInfo=true` 去符号，两者叠加后可以得到接近 C 程序的单文件产物。

📘 [Kotlin · Native 二进制选项](https://kotlinlang.org/docs/native-binary-options.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的「体积与链接」在 JVM 世界里有三种含义：`jlink` 裁掉用不到的 JDK 模块、`jpackage` 把裁剪后的运行时与 jar 打成平台安装包、R8/ProGuard 裁掉 jar 里用不到的类；至于链接，Java 的产物是 jar 与 class 文件，不存在静态链接，只有在 `native-image` 下才有真正的链接期。最该先知道的是：**裁剪运行时（jlink）与裁剪应用（R8）是两件独立的事**，两者都要做才能得到最小的自包含产物。

```java
javac -d out src/Main.java
jar --create --file app.jar --main-class Main -C out .

# 1) 裁运行时：只保留 java.base
jlink --add-modules java.base --strip-debug --no-header-files --no-man-pages \
      --compress=zip-6 --output myjre
myjre/bin/java --list-modules          # 确认只剩需要的模块
du -sh myjre

# 2) 打平台安装包（默认已带 --strip-debug --no-header-files --no-man-pages）
jpackage --type app-image --input out --main-jar app.jar --main-class Main --name myapp
jpackage --type dmg --runtime-image myjre --input out --main-jar app.jar --main-class Main --name myapp

# 3) 裁应用：R8 或 ProGuard（都要写 keep 规则应对反射）
java -jar r8.jar --release --lib $JAVA_HOME/jars --output out-opt.jar app.jar
java -jar proguard.jar @proguard-rules.pro

# 4) 真提前编译：GraalVM Native Image
native-image -O2 -cp app.jar Main app-native
native-image -Os -cp app.jar Main app-native-small     # 体积优先
ldd myjre/lib/server/libjvm.so | head    # JVM 本身就是动态库，谈不上静态链接
```

`jlink` 只处理 JDK 自身的模块图，它读的是 `java.base` 之类的模块依赖，因此裁剪效果取决于你的应用真的用了哪些 JDK 模块——服务端程序常常只能用 `java.base` 加 `java.sql`，收益最大；用了几十个模块的应用收益就有限了。⚠️ `--compress` 的取值在 JDK 21 之后改成 `zip-0` 到 `zip-9`（默认 `zip-6`），旧的 `0`/`1`/`2` 写法已废弃。R8 与 ProGuard 的作用与 Kotlin 标签页相同：做可达性分析并改名，代价是反射、序列化、JNI 用到的元素必须在规则文件里 `-keep`，否则只在运行时炸。真正把「链接」概念带进 Java 的是 GraalVM `native-image`：它在构建期做全程序分析，把可达的类与方法编译进一个原生可执行文件，还能用 `-O2`（默认）、`-O3`、`-Ob`、`-Os`、`-O0`、`-O1` 调优化取向，代价是失去动态类加载与 `Reflection.Emit`，反射与资源必须在配置里显式声明。

📘 [`jlink` 手册（JDK 25）](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jlink.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的体积与链接由三段组成：编译期的 `-flto` 让链接器看到跨编译单元的 IR，`-ffunction-sections`/`-fdata-sections` 把每个函数与数据切成独立段，链接期的 `--gc-sections`（GNU）或 `-dead_strip`（Apple）把不可达的段丢掉，最后再用 `strip` 去符号。`-fvisibility=hidden` 则在库场景里让未被显式导出的符号无法被外部引用，从而为 DCE 创造条件。最该先知道的是：这套选项在不同平台上并不通用，GNU 与 Apple 的链接器参数互不认账。

```cpp
# 实测（clang 21 / Apple Silicon）
clang++ -std=c++23 -O2 -flto bench.cpp -o cpp_lto               # 33432 字节
clang++ -std=c++23 -O2 -flto -ffunction-sections -fdata-sections bench.cpp \
        -Wl,-dead_strip -o cpp_ds                               # 33432 字节（macOS 链接器）
clang++ -std=c++23 -O2 -flto -ffunction-sections -fdata-sections bench.cpp \
        -Wl,--gc-sections -o cpp_gc
# ld: unknown options: --gc-sections   ← macOS 的 ld64 不认 GNU 选项
cp cpp_ds cpp_strip && strip cpp_strip && stat -f%z cpp_strip   # 事后剥离

clang++ -std=c++23 -Oz -fvisibility=hidden -fvisibility-inlines-hidden -c bench.cpp -o b.o
clang++ -std=c++23 -O2 -flto -fuse-ld=lld bench.cpp -o cpp_lld
# clang++: error: invalid linker name in argument '-fuse-ld=lld'   ← 未安装 lld 时

# Linux 上的一条完整发布链
g++ -std=c++23 -O2 -flto -ffunction-sections -fdata-sections \
    -fvisibility=hidden -static-libgcc -static-libstdc++ \
    -Wl,--gc-sections -Wl,--as-needed app.cpp -o app
strip app
clang++ -static app.cpp -o app   # ld: library 'crt0.o' not found   ← macOS 不支持全静态
otool -L cpp_ds | head           # macOS：看动态依赖
nm -C --defined-only cpp_ds | head   # Linux：看导出符号
du -h cpp_ds
```

`-flto` 让内联与常量传播跨越编译单元，同时也会让未被引用的函数在优化后彻底消失；`-ffunction-sections` 与 `-fdata-sections` 是把这份信息变成可回收的段，缺了它们链接器只能整段保留。⚠️ `--gc-sections` 与 `-dead_strip` 不能混用：前者是 GNU ld 与 lld 的选项，后者是 Apple 链接器的选项，写错会直接链接失败。`-fvisibility=hidden` 对可执行文件用处不大，对共享库则是标配——它让默认导出的符号从「全部」变成「只有显式标注的」，既缩小编译产物的动态符号表，又给优化器更多自由度；Windows 上对应的机制是 `__declspec(dllexport)` 与模块定义文件。静态链接的取舍要分平台看：Linux 上 `-static` 或 `-static-libstdc++` 能做出可移植的单文件，macOS 上系统根本不提供静态 libSystem，只能用 `-static-libgcc`/`-static-libstdc++` 类似的局部静态；把 libstdc++ 静态链进去还能顺手避开目标机器 GCC 版本不一致导致的 ABI 问题。

📘 [gcc 手册 · 链接选项](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html)

{{% /tab %}}

{{% tab header="C" %}}

C 的体积控制与 C++ 完全同源，只是少了模板与异常表这些额外开销，收益通常更明显：`-flto` 做跨单元优化、`-ffunction-sections`/`-fdata-sections` 配合 `--gc-sections` 删死代码、`strip` 去符号，需要可移植二进制时再用 musl 做全静态。C 没有运行时概念，所以「链接什么」这件事比 C++ 简单得多，唯一需要注意的是 libc 的选择。最该先知道的是：真正让 C 产物小下来的往往是 `--gc-sections` 加 `-fdata-sections`，而不是任何优化等级。

```c
# 实测（clang 21 / Apple Silicon）
clang -O2 -flto -ffunction-sections -fdata-sections fib.c -Wl,-dead_strip -o f_ds
clang -O2 -fvisibility=hidden -fno-semantic-interposition -c fib.c -o fib.o
cp f_ds f_strip && strip f_strip && stat -f%z f_ds f_strip

clang -O2 -static fib.c -o f_static
# ld: library 'crt0.o' not found     ← macOS 不提供静态 libSystem
gcc -O2 -static -static-libgcc fib.c -o f_static_linux     # Linux 上可行
gcc -O2 -flto -ffunction-sections -fdata-sections -Wl,--gc-sections fib.c -o f_gc
musl-gcc -O2 -static fib.c -o f_musl       # 用 musl 做可移植的全静态二进制
file f_musl
# ELF 64-bit LSB executable, ... statically linked
du -h f_ds f_musl
ldd f_static_linux        # Linux 上应输出 "not a dynamic executable"
nm --defined-only f_ds | wc -l
```

`-flto` 与 section 拆分是两件互补的事：前者让编译器在链接期做跨单元优化，后者让链接器能把没被引用的段整体丢弃，只有两者同时开启才能得到最小产物——只写 `-flto` 通常会因为链接器仍按整段保留而收益有限。⚠️ `-Wl,--gc-sections` 只对 ELF 平台（GNU ld、gold、lld）有效，macOS 的 ld64 要用 `-Wl,-dead_strip`，这条差异在跨平台 CMake 工程里必须用生成器表达式区分。静态链接的取舍是经典权衡：`-static` 让程序不依赖目标机器的 glibc 版本，部署最简单，但也放弃了 glibc 的安全更新与 NSS（名字解析、用户查询）的动态加载能力，用 musl 编译还能得到更小的产物与更可预测的行为；`-static-libgcc` 只是把 GCC 自己的辅助库静态链入，是一个风险更低的折中选择。

📘 [gcc 手册 · 链接选项](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的体积问题不在可执行文件大小，而在**预编译缓存与 sysimage**：每次加载包都要从 `.ji` 缓存与系统镜像里取已编译的方法，缓存越大启动越慢、分发越笨重。官方由此提供了两条路：`--strip-ir` 与 `--strip-metadata` 在打包时删掉 IR 与文档/源码位置，`PackageCompiler.jl` 与 `juliac` 则把应用与依赖提前编译进一个 sysimage 或可执行文件。最该先知道的是：Julia 没有链接期 LTO，跨包优化只能靠 sysimage 内的预编译来实现。

```julia
# 裁剪系统镜像：去掉 IR 与元数据
julia --strip-metadata --strip-ir -e 'println("trimmed sysimage")'
julia --strip-ir -J custom.so -e 'using MyPkg; println("loaded")'

# 生成自定义 sysimage / 独立应用
julia -e 'using PackageCompiler
  create_sysimage([:MyPkg]; sysimage_path="MySys.so",
                  precompile_execution_file="warmup.jl")
  create_app("MyApp", "build/MyApp")'
./build/MyApp/bin/MyApp
ls -lh build/MyApp/lib/julia/sys.so

# juliac：官方 JuliaC.jl 提供的驱动（Julia 1.12+）
juliac --output-exe myapp --bundle build --trim=safe --experimental app.jl

du -sh ~/.julia/compiled/v1.13/       # 预编译缓存，分发与启动的主要负担
julia -e 'using Pkg; Pkg.precompile()'
julia --compiled-modules=no -e 'using MyPkg'    # 调试缓存问题时关掉
julia -e 'println(Base.isprecompiled(Base.PkgId(MyPkg)))'
```

`--strip-ir` 去掉已编译函数的中间表示，`--strip-metadata` 进一步去掉文档字符串与源码位置信息，两者一起用能显著缩小 sysimage，代价是失去栈回溯里的源码位置与内省能力，因此只适合最终交付的产物。`PackageCompiler.create_sysimage` 把包与一个「预热脚本」的编译结果固化进 `.so`，`create_app` 在此之上再打包运行时与启动脚本，得到近似原生的分发目录；`juliac` 是同一思路的官方 CLI 包装，用 `--trim=safe` 做可达性裁剪。⚠️ sysimage 里的代码是**在特定机器与 Julia 版本上**编译出来的，会带上那台机器的目标特性与绝对路径，因此不能直接跨平台分发；正确的做法是在目标平台上构建。缓存放大的另一个原因是类型特化：同一份泛型代码会为每个用到的具体类型生成一份机器码，这也是 Julia 编译产物天然比 C 大的根本原因，能做的只有减少类型组合、把热路径收敛到少数具体类型。

📘 [Julia · 系统镜像构建](https://docs.julialang.org/en/v1/devdocs/sysimg/)

{{% /tab %}}

{{% tab header="C#" %}}

.NET 的体积控制由三个 MSBuild 属性主导：`PublishTrimmed` 让 ILLink 做程序集级可达性分析并删掉未使用的类型与成员，`PublishSingleFile` 把托管程序集与原生库塞进一个文件，`PublishAot` 则把整程序编译成本地机器码同时强制裁剪。`InvariantGlobalization` 是一个常被忽视的体积开关，它去掉 ICU 数据，能再省几兆。最该先知道的是：裁剪会破坏反射，必须依赖裁剪分析器的警告而不是「跑起来没问题」。

```csharp
dotnet publish -c Release -r linux-x64 --self-contained true -p:PublishSingleFile=true
dotnet publish -c Release -r linux-x64 -p:PublishTrimmed=true
dotnet publish -c Release -r linux-x64 -p:PublishTrimmed=true -p:TrimMode=partial
dotnet publish -c Release -r linux-x64 -p:PublishTrimmed=true -p:TrimmerSingleWarn=false
dotnet publish -c Release -r linux-x64 -p:PublishTrimmed=true -p:EnableTrimAnalyzer=true
dotnet publish -c Release -r linux-x64 -p:PublishAot=true -p:InvariantGlobalization=true
dotnet publish -c Release -r linux-x64 -p:PublishAot=true -p:OptimizationPreference=Size
du -sh bin/Release/net10.0/linux-x64/publish/
ls -l  bin/Release/net10.0/linux-x64/publish/

# 项目文件里的等价写法
# <PropertyGroup>
#   <PublishTrimmed>true</PublishTrimmed>
#   <TrimMode>full</TrimMode>              <!-- full 或 partial，默认 full -->
#   <InvariantGlobalization>true</InvariantGlobalization>
#   <StackTraceSupport>false</StackTraceSupport>
#   <PublishSingleFile>true</PublishSingleFile>
#   <SelfContained>true</SelfContained>
#   <IncludeNativeLibrariesForSelfExtract>true</IncludeNativeLibrariesForSelfExtract>
# </PropertyGroup>
```

`TrimMode` 只有 `full` 与 `partial` 两个合法值，默认 `full`（对全部程序集做裁剪），`partial` 只裁掉那些显式声明支持裁剪的程序集，兼容性更好但收益更小——迁移期建议先用 `partial` 跑通再切 `full`。⚠️ 裁剪的三个经典炸点：反射（`Type.GetType` 用字符串找类型）、序列化（`System.Text.Json` 的源生成器可以规避）、以及依赖注入按约定注册的服务，它们都不会在编译期报错，而是发布后才 `MissingMethodException`，因此 `EnableTrimAnalyzer` 与 `TrimmerSingleWarn=false` 必须打开，把警告逐条看完。`InvariantGlobalization=true` 让应用进入「固定区域性」模式，不再访问 ICU 的特定区域性数据（日期格式、排序规则、大小写映射都会退化成不变文化的行为），在裁剪模式下还会顺带删掉整个全球化代码与数据，代价是无法正确处理多语言格式——只面向单一区域的服务可以放心用。`PublishAot` 与 `PublishTrimmed` 不要同时手写：Native AOT 已经隐含裁剪与单文件，重复设置反而会让属性互相覆盖，导致体积与预期不符。

📘 [.NET · 裁剪选项](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的体积优化主要落在 Web 编译上：`dart compile js` 的 `-O2` 及以上会做 tree shaking 与压缩，`--no-source-maps` 少产出一个映射文件，`dart compile wasm` 还有 `--strip-wasm`。AOT 侧（`dart compile exe`）的 tree shaking 是整程序编译自动完成的，可调的只有目标平台；混淆与符号分离在 Flutter 构建里做。最该先知道的是：Dart 没有链接期 LTO 开关，AOT 的减重靠「全程序编译 + 可达性分析」自动完成。

```dart
dart compile exe bin/myapp.dart -o build/myapp
du -h build/myapp                                   # 自包含可执行文件

# 分两步：先出可移植 Kernel IR，再按目标 AOT
dart compile kernel bin/myapp.dart -o build/myapp.dill
dart compile aot-snapshot build/myapp.dill -o build/myapp.aot
dartaotruntime build/myapp.aot
dart compile exe bin/myapp.dart -o build/myapp-arm64 --target-os=linux --target-arch=arm64

# Web：tree shaking 主要在 -O2 及以上
dart compile js -O2 -o out/main.js web/main.dart
dart compile js -O2 --no-source-maps -o out/main.js web/main.dart
dart compile js -O4 -o out/main.js web/main.dart    # 更激进的体积优化，风险更高
dart compile wasm -O2 --strip-wasm --minify -o out/main.wasm web/main.dart
du -h out/main.js out/main.wasm

# 混淆与调试符号分离是 Flutter 构建的选项
# flutter build apk --obfuscate --split-debug-info=build/app/outputs/symbols
# flutter build ipa --obfuscate --split-debug-info=build/ios/symbols
```

`dart compile exe` 的产物是「机器码 + 一个小型 Dart 运行时」，运行时负责类型检查与垃圾回收，这是它比 C 产物大一圈的原因；`dart compile aot-snapshot` 把运行时单独拿出来，多个 CLI 工具可以共享一份 `dartaotruntime`，适合一次分发多个命令的场景。tree shaking 之所以在 Dart 里效果显著，是因为 AOT 与 dart2js 都是整程序编译：编译器知道哪些类、方法、`extension` 最终没有被引用，可以直接不生成。⚠️ 反射式的用法（`dart:mirrors`、按名字构造）会直接挡住 tree shaking，`dart compile exe` 干脆不支持 `dart:mirrors` 与 `dart:developer`，这类代码必须在编译期改成显式调用；`--strip-wasm` 与 `--obfuscate` 都会让栈回溯失去可读信息，所以官方要求把符号文件单独保管，否则线上崩溃无法定位。`dart compile js` 的 `-O4` 虽然能再压一点体积，但它对输入数据分布敏感，⚠️ 必须先用 `-O2` 与 `-O3` 各自回归一遍才能上。

📘 [`dart compile`](https://dart.dev/tools/dart-compile)

{{% /tab %}}

{{% tab header="R" %}}

R 没有链接期，也没有能删代码的打包器：交付形态只有源码包与二进制包两种，`.tar.gz` 里装的是源码，安装到库目录后由 `lazy-load` 数据库加速装载，所谓「二进制包」只是已安装结果的压缩拷贝。体积与启动的优化手段因此只有三条：安装时做字节码编译、用 `LazyData` 把数据延迟加载、减少依赖包的 `Depends`。最该先知道的是：R 的官方文档里不存在任何「编译成独立可执行文件」或「剥离 IR」的选项。

```r
R CMD build mypkg                       # 生成 mypkg_1.0.tar.gz（源码包）
R CMD INSTALL mypkg_1.0.tar.gz          # 安装到库目录，默认会字节编译
R CMD INSTALL --no-byte-compile mypkg   # 关掉字节编译，包更大、装载更慢
R CMD INSTALL --preclean mypkg          # 先清理再编译（有 C 代码时常用）
R CMD INSTALL --libs-only mypkg         # 只构建共享库，用于合并子架构
R CMD check mypkg_1.0.tar.gz

du -sh mypkg/                           # 包目录里的 R/ 与 data/ 与 lazyload 数据库
Rscript -e 'cat(system.file(package = "mypkg"), "\n")'
Rscript -e 'print(.Platform$pkgType)'   # "source"、"mac.binary" 等，决定分发形态
Rscript -e 'print(tools:::.OStype())'
Rscript -e 'tools::checkFF("mypkg", verbose = TRUE)'   # 检查 .Call/.C 是否正确注册
Rscript -e 'print(length(getDLLRegisteredRoutines("mypkg")$.Call))'

# DESCRIPTION 里与体积/装载相关的字段
# LazyData: true          数据惰性加载
# ByteCompile: yes        安装时字节编译（默认即如此）
# Depends: R (>= 4.6)     依赖越少，安装与装载越快
```

R 的分发单位是**包**而不是程序：用户拿到 `.tar.gz` 后在目标机器上 `R CMD INSTALL`，或者在仓库里下载对应的二进制包，因此「链接」这一步发生在安装时而不是构建时。`ByteCompile` 字段默认为真，安装阶段会把 `R/` 下的代码全部编译成字节码存入 `lazyload` 数据库，这也是为什么 `R CMD INSTALL --no-byte-compile` 只应在排查编译器 bug 时使用——它会让包更大且首次调用更慢。⚠️ `.Call`/`.C` 等原生调用必须用 `useDynLib` 声明并依赖 `R_registerRoutines` 注册，`tools::checkFF` 就是官方用来查这类问题的工具，漏注册会让 CRAN 检查失败并在某些平台崩溃。想要类似「独立可执行文件」的效果，社区路径是 `Rscript` 加 shebang（`#!/usr/bin/env Rscript`），或者用第三方工具打包整个 R 运行时，但这都不是官方支持的交付方式；R 自身的 `--enable-lto` 只影响 R 解释器本体的构建，跟用户包无关。

📘 [R · 编写 R 扩展](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的体积与链接控制非常直接：`ReleaseSmall` 从编译期就以体积为目标，`-fstrip` 去掉调试符号，`zig build-lib` 的 `-static`/`-dynamic` 决定产物是静态库还是动态库，而 `-target` 能直接指定 musl 三元组做出全静态二进制。Zig 自带 libc，因此它是少数不需要额外工具链就能做交叉静态链接的语言之一。最该先知道的是：Zig 没有单独的 LTO 开关，因为它默认走「整个编译单元 + 自研链接器」的路径。

```zig
zig build-exe main.zig -O ReleaseSmall -fstrip -femit-bin=app-small
zig build-exe main.zig -O ReleaseFast -fstrip -femit-bin=app-fast
zig build -Doptimize=ReleaseSmall
ls -l zig-out/bin/ app-small app-fast

# 静态与动态库
zig build-lib mylib.zig -static -O ReleaseFast -femit-bin=libmy.a
zig build-lib mylib.zig -dynamic -O ReleaseFast -femit-bin=libmy.so
zig build-exe main.zig -O ReleaseSafe -lmy -L. -femit-bin=app-linked

# 全静态、可移植：指定 musl 目标
zig build-exe main.zig -O ReleaseSmall -target x86_64-linux-musl -fstrip
zig build-exe main.zig -O ReleaseSmall -target aarch64-linux-musl -fstrip
file zig-out/bin/main
# ELF 64-bit LSB executable, ... statically linked

zig cc -O2 -static hello.c -o hello-static         # 用 zig cc 编 C，顺手做静态链接
zig cc -target aarch64-linux-musl -static hello.c -o hello-arm64
zig build-exe main.zig -O ReleaseSmall -fstrip --verbose-link   # 看链接器实际做了什么
```

`ReleaseSmall` 与 `-fstrip` 是唯一直接作用于体积的组合：前者让优化目标从速度切换到体积（不做激进内联与循环展开），后者删掉 DWARF 与符号表；`ReleaseFast` 加 `-fstrip` 的产物会明显更大。⚠️ 去符号的开关是 `-fstrip` 而不是 `--strip`，后者在 `zig build-exe` 上不存在，这是最常见的记错。`-target <arch>-<os>-<abi>` 三元组里 ABI 段写 `musl` 就能得到不依赖 glibc 的静态二进制，配合 Zig 自带的 libc 源码与交叉链接器，无需在机器上安装任何目标平台工具链——这正是很多项目把 Zig 只当作「交叉编译器」来用的原因。`zig build-lib -dynamic` 生成的共享库默认导出的符号策略与 C 一致，需要在源码里用 `export fn` 显式导出，否则符号不会出现在动态符号表中，这一点与 `-fvisibility=hidden` 的效果类似。

📘 [Zig 语言参考](https://ziglang.org/documentation/0.15.1/)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 里唯一能减少分发体积的机制是 `luac -s`：把调试信息（行号、局部变量名、源码路径）从字节码里剥掉，通常能省掉可观的一部分。除此之外 Lua 没有链接期优化，也没有 tree shaking，`luac` 甚至没有优化等级选项。最该先知道的是：`luac -s` 剥掉的调试信息正是 `debug` 库与错误回溯需要的，剥之前要想清楚线上是否需要精确定位。

```lua
luac -o main.luac main.lua            # 普通字节码
luac -s -o main.strip.luac main.lua   # 剥掉调试信息
ls -l main.lua main.luac main.strip.luac
luac -l main.luac | head              # 还能看到行号信息
luac -l main.strip.luac | head        # 行号变成 ?
strip main.luac 2>/dev/null || echo "不是 ELF，strip 不适用"

# 运行期报错信息的差别
lua main.luac
lua main.strip.luac
# 剥离后的版本回溯里没有行号与变量名

# C 模块照常编译成共享库
gcc -O2 -shared -fPIC -I/usr/include/lua5.5 mymod.c -o mymod.so
lua -e 'local m = require("mymod"); print(m.hello())'

# 解释器本体的体积可以靠编译期选项控制，但那是发行版的事
# make linux MYCFLAGS="-O2 -Os" MYLDFLAGS="-s"
luac -v
```

Lua 的字节码文件本身就是一个可移植的 chunk，`lua main.luac` 与 `lua main.lua` 的运行行为一致，区别只在启动时省掉了词法与语法分析；对于嵌入了 Lua 的宿主程序，预编译还能顺带做语法检查（`luac -p`），把错误挡在部署之前。⚠️ `luac -s` 的代价很具体：出错时的回溯只剩函数名，`debug.getinfo` 拿不到 `currentline`，`debug.traceback` 也失去行号，如果线上依赖日志定位问题就不要剥。Lua 没有 tree shaking 的另一个原因是它的模块边界是运行时的：`require` 接受的是字符串，编译器根本无法静态判断哪些模块会被加载，所以裁剪只能靠人工拆分脚本或让宿主按需 `require`。真正想让 Lua 程序变小变快，应当考虑 LuaJIT（它有自己的字节码与 JIT）或把热点逻辑下沉到 C 模块，而不是寻找并不存在的编译期裁剪选项。

📘 [Lua 5.5 参考手册](https://www.lua.org/manual/5.5/manual.html)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的体积控制全部发生在 `tsc` 之后的打包阶段：`tsc` 只做类型擦除与语法降级，tree shaking 由 esbuild、Rollup、webpack 这类打包器完成，而它们能否安全删代码取决于两个前提——源码用 ESM 静态导入，且 `package.json` 里正确声明了 `sideEffects`。`--declaration` 与 source map 属于产物体积的另一半。最该先知道的是：`tsc --outFile` 之类的做法不会做 tree shaking，`.d.ts` 也要单独控制。

```typescript
npx tsc --noEmit                        # 只做类型检查，零产物
npx tsc --outDir dist                   # 逐文件转译，不做打包
npx tsc --declaration --emitDeclarationOnly --outDir types
npx tsc --sourceMap false --inlineSources false --removeComments
du -sh dist types

# 打包：tree shaking 在这里发生
npx esbuild src/index.ts --bundle --minify --format=esm --outfile=dist/bundle.js
npx rollup -c                             # 读 package.json 的 sideEffects
npx terser dist/bundle.js -c -m -o dist/bundle.min.js
npx webpack --mode production
du -h dist/bundle.js

cat package.json
# { "name": "app", "type": "module", "sideEffects": false,
#   "exports": { ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" } } }
npx esbuild src/index.ts --bundle --analyze --outfile=dist/bundle.js   # 看谁占体积
```

tree shaking 能生效的硬条件是**静态可分析**：`import { a } from "./mod"` 可以被删，`require(dynamicName)` 与 `import(variable)` 不行；打包器还需要知道模块有没有副作用，`sideEffects: false` 是在告诉它「这个包里的模块只要导出没被用到，整个模块都能删」，写错会导致应该执行的初始化被删掉，这是最危险的一种优化。⚠️ `tsc` 的 `--module commonjs` 与 ESM 混用会直接让 tree shaking 失效，`verbatimModuleSyntax` 与 `isolatedModules` 就是用来强制每个文件都能被独立转译、避免打包器误解语义的开关。体积的另一半是类型声明与 source map：`.d.ts` 只在给别的包做依赖时需要，`--emitDeclarationOnly` 可以把它与运行时代码分开输出；source map 对最终用户没有价值，生产构建通常用 `--no-source-maps` 或把它上传到错误监控平台后删除。真正的减重顺序应当是「先换 ESM + 声明 sideEffects，再开 minify，最后才考虑拆包」，顺序反了收益会小很多。

📘 [TypeScript · tsconfig 参考](https://www.typescriptlang.org/tsconfig/)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的体积优化是全前端与 Node 生态最成熟的一块：bundler 做 tree shaking 与 scope hoisting，minifier 做压缩与改写，Node 侧则多了单文件可执行（SEA）与启动快照两种交付形态。与 TypeScript 一样，tree shaking 的前提是 ESM 静态导入加 `sideEffects` 声明。最该先知道的是：压缩与 tree shaking 是两件不同的事——前者删空格与改名字，后者才真的删代码。

```javascript
npx esbuild src/index.js --bundle --minify --format=esm --outfile=dist/bundle.js
npx esbuild src/index.js --bundle --analyze --outfile=dist/bundle.js   # 体积归因
npx rollup -c                                  # 依赖 package.json 的 sideEffects
npx terser dist/bundle.js -c -m -o dist/bundle.min.js
npx webpack --mode production
node dist/bundle.js

cat package.json
# { "type": "module", "sideEffects": false }
node --input-type=module -e 'import("./dist/bundle.js").then(m => console.log(typeof m))'

# Node 侧的两种交付形态
node --build-snapshot --snapshot-blob app.blob main.js   # 生成启动快照
node --snapshot-blob app.blob main.js                    # 用快照启动，跳过模块初始化
cat sea-config.json
# { "main": "main.js", "output": "sea-prep.blob" }
node --experimental-sea-config sea-config.json
cp $(command -v node) myapp && npx postject myapp NODE_SEA_BLOB sea-prep.blob \
  --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2
./myapp
du -h myapp dist/bundle.js
```

Rollup 与 esbuild 的 tree shaking 都建立在 ESM 的静态结构上：导入导出在解析阶段就能确定，未使用的导出可以整块删除，甚至能把多个模块合并进同一作用域（scope hoisting）从而进一步内联与删除。⚠️ `sideEffects: false` 是一句强承诺：如果某个模块只靠导入产生副作用（注册全局、注入 polyfill、修改原型），声明为 false 后它会被删除，程序在运行时才莫名其妙地坏掉，所以只有纯函数式模块才该这么写。CommonJS 的动态 `require` 与 `module.exports` 计算属性会让静态分析失效，体积随之膨胀，这也是「换到 ESM」几乎是所有打包体积优化的第一步的原因。Node 的 SEA 与启动快照解决的是另一个问题：SEA 把脚本与 blob 附加到 Node 二进制上，得到一个可分发的单文件（体积接近整个 Node 运行时，通常几十兆，实测本机 Node 24 支持 `--experimental-sea-config` 与 `--build-snapshot`）；快照则把模块初始化结果序列化下来，主要收益是启动时间而不是体积。

📘 [Node.js · 单文件可执行应用](https://nodejs.org/api/single-executable-applications.html)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的产物体积主要由 `vendor/` 决定，优化手段也就集中在自动加载与打包两处：Composer 的 `--optimize-autoloader` 生成 classmap 减少文件系统扫描，`--classmap-authoritative` 进一步声明「类只可能来自 classmap」，`.phar` 则把所有代码打进一个归档并支持整包缓存。运行时的 OPcache 与 preload 属于启动优化，不改变分发体积。最该先知道的是：`--classmap-authoritative` 会让动态生成的类无法被自动加载，是体积与灵活性的直接取舍。

```php
composer install --no-dev --optimize-autoloader           # 生成 classmap
composer dump-autoload --optimize-autoloader              # -o
composer dump-autoload --classmap-authoritative           # -a，隐含 -o
composer dump-autoload --apcu                             # 用 APCu 缓存 classmap 查找
composer install --no-dev --classmap-authoritative --apcu
du -sh vendor/

# 打成 .phar（注意 phar.readonly 默认开启，必须显式关掉）
php -d phar.readonly=0 build-phar.php
php myapp.phar
php -r '$p = new Phar("myapp.phar"); echo count($p), " files\n";'

# 运行时：OPcache 与预加载
php -d opcache.enable=1 -d opcache.memory_consumption=256 \
    -d opcache.max_accelerated_files=20000 \
    -d opcache.preload=preload.php -d opcache.preload_user=www-data -S 0.0.0.0:8000
php -i | grep -E "opcache.(enable|memory_consumption|max_accelerated_files)"
# opcache.enable => On
# opcache.max_accelerated_files => 20000
php -d opcache.validate_timestamps=0 -S 0.0.0.0:8000   # 生产：不再检查文件改动
```

Composer 的自动加载默认走 PSR-4 规则映射，每次 `new Foo()` 都要按命名空间拼路径再去文件系统确认存在；`--optimize-autoloader` 会把所有类扫描成一个静态数组，省掉路径拼接，`--classmap-authoritative` 更进一步——它告诉加载器「classmap 里没有的类就是不存在的」，于是完全跳过文件系统探测，代价是从此不能靠约定自动发现未列入的类。⚠️ 这条限制在大量使用动态类名（工厂、插件、`eval` 生成）的项目里会直接致命，发布前必须跑一遍全量功能测试。`.phar` 的价值是把成百上千个小文件收成一个，减少 inode 压力并让 OPcache 更容易整包命中，但 ⚠️ `phar.readonly` 默认为 `On`，构建脚本必须用 `php -d phar.readonly=0` 运行，且 `phar` 扩展在生产环境要允许读取。`opcache.preload` 把框架与热路径文件在进程启动时就编译进共享内存，是 PHP 8 之后启动优化的主要手段，但它只在 `php-fpm` 这类长驻进程下有意义，并且 `preload_user` 必须正确设置，否则会因权限问题静默失效。

📘 [Composer · dump-autoload](https://getcomposer.org/doc/03-cli.md#dump-autoload-dumpautoload)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 是这 18 门语言里唯一**明确没有任何裁剪机制**的：官方只提供解释器与标准库，没有打包器、没有 tree shaking、也没有把脚本编译成独立可执行文件的工具。实践中的体积控制因此退化成「少装 gem、少 `require`、用 Bundler 分组」三件事，启动优化则靠 `--disable-gems`。最该先知道的是：Ruby 的 `require` 在运行时解析字符串，静态分析无从下手，这是没有 tree shaking 的根本原因。

```ruby
ruby --disable-gems -e 'puts "gems off"'       # 不加载 RubyGems，启动更快
ruby --disable-gems -e 'require "json"'
# LoadError: cannot load such file -- json（RubyGems 未加载，gem 不可见）
ruby -e 'puts $LOAD_PATH' | head               # 默认加载路径
ruby -e 'puts Gem.default_dir'
du -sh "$(gem env gemdir)"                     # gem 目录总体积

bundle install --without development test      # 生产不装开发/测试组
bundle list                                    # 看实际装了什么
bundle exec ruby app.rb
gem contents mygem | head                       # 单个 gem 装了哪些文件
gem list --local | wc -l
gem install --no-document mygem                 # 不装文档，省体积
ruby -e 'puts Gem::Specification.map { |s| s.name }.uniq.size'   # 已装 gem 数

# Ruby 没有 --strip-ir 之类的选项；只有运行期 JIT 与解释器开关
ruby --yjit -e 'puts "yjit on"'
ruby -e 'puts RUBY_DESCRIPTION'
```

Ruby 的分发单位是 gem：一个 gem 是「一堆 Ruby 文件 + 元数据 + 可选的 C 扩展共享库」，安装时 C 扩展会被就地编译，因此体积取决于装了哪些 gem 以及它们的文档。`--disable-gems` 跳过 RubyGems 自身的加载（`rubygems.rb` 及其依赖），能省下可观的启动时间，⚠️ 代价是所有通过 `gem install` 安装的库都不再可见，只适合「只用标准库的脚本」或自带 `$LOAD_PATH` 配置的场景。Bundler 的 `--without` 分组是控制生产依赖体积的主要手段，`--no-document` 则在安装时跳过 ri/rdoc 生成，能省掉大量文件。⚠️ 想找「Ruby 版的 -s -w 或 tree shaking」是没有的：解释器是系统安装的一部分（macOS 上由 Homebrew 或系统提供），应用代码只是文本，官方文档里不存在打包成单文件的选项；社区方案（如 Travelling Ruby、`ruby-packer`）都是第三方且多年未更新，选用前要评估维护状态。真正能改善 Ruby 启动与运行的是 YJIT 与 `--disable-gems` 这类运行期手段，而不是编译期裁剪。

📘 [Ruby · Gem 模块](https://docs.ruby-lang.org/en/master/Gem.html)

{{% /tab %}}

{{< /tabpane >}}

### 运行时与目标控制

这一组把两个常常被混在一起的问题分开：**代码什么时候被翻译成机器码**（AOT、JIT、解释执行，以及各种混合形态），以及**翻译成哪个平台的机器码**（交叉编译与目标三元组）。前者决定启动时间与峰值性能的取舍，后者决定一份源码能产出多少种产物；两者都会反过来限制上两节的优化选项——例如开启 JIT 的语言无法彻底关闭运行时，而交叉编译到 `wasm32` 的语言会失去线程与系统调用。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 是纯 AOT 语言，没有 JIT、没有解释器，也没有运行时可切换的执行模式：`rustc` 把源码编成目标平台的机器码，进程启动即执行。目标控制在 Rust 里由 `--target` 三元组加一组按目标配置的加载项完成，标准库需要先用 `rustup target add` 装到本地。最该先知道的是：Rust 的交叉编译**只差一个链接器和一个标准库**，`.cargo/config.toml` 的 `[target.*]` 段就是补齐这两样的地方。

```rust
rustc --version --verbose          # 看 host 三元组，例如 aarch64-apple-darwin
rustc --print target-list | wc -l  # 内置目标列表规模
rustc --print target-list | grep -E "musl|wasm"

# 交叉编译三步：加标准库、指定 --target、必要时配链接器
rustup target add aarch64-unknown-linux-gnu
rustup target add x86_64-unknown-linux-musl
rustup target add wasm32-unknown-unknown
rustup target add wasm32-wasip1
cargo build --release --target aarch64-unknown-linux-gnu
cargo build --release --target x86_64-unknown-linux-musl
cargo build --release --target wasm32-unknown-unknown
cargo build --release --target wasm32-wasip1
file target/aarch64-unknown-linux-gnu/release/app
# ELF 64-bit LSB executable, ARM aarch64, ...
rustc --print cfg --target wasm32-unknown-unknown | head -6
# target_arch="wasm32"
# target_family="wasm"

# .cargo/config.toml：为目标指定链接器与运行器
# [target.aarch64-unknown-linux-gnu]
# linker = "aarch64-linux-gnu-gcc"
# [target.wasm32-wasip1]
# runner = "wasmtime"
cargo run --target wasm32-wasip1        # 通过 runner 在本地跑 wasm
cargo build --release --target wasm32-unknown-unknown -Z build-std   # nightly 可为自定义目标重编 std
```

Rust 的运行时控制几乎没有旋钮，因为「运行时」本身就只有标准库与一小段启动代码：`panic` 策略、`std` 还是 `no_std`、以及是否链接 libc 就是全部。目标控制则非常细：`--target` 选定三元组，`.cargo/config.toml` 按目标覆盖 `linker`、`runner`、`rustflags`，这样切换平台不需要改命令行。⚠️ `rustup target add` 装的只是预编译标准库，交叉编译到 `aarch64-unknown-linux-gnu` 仍然需要目标平台的 C 链接器（例如 `aarch64-linux-gnu-gcc`）来链接 libc，否则会在链接阶段报缺少 `cc`；换成 `musl` 三元组则连 libc 都静态打包好了，只需要 `rust-lld`，因此 `x86_64-unknown-linux-musl` 是最省事的分发目标。⚠️ `wasm32-unknown-unknown` 没有操作系统接口，`std` 的多数功能会编译失败，要跑带文件与网络的服务应当用 `wasm32-wasip1` 配 WASI 运行时。

📘 [rustc · 平台支持](https://doc.rust-lang.org/rustc/platform-support.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 是 AOT 加 ARC 的语言，没有 JIT；它的「运行时」是随产物链接的 Swift 运行时库（Apple 平台上由系统提供，其他平台可以静态链接）。目标控制由 `-target` 三元组与 `-sdk` 两件事组成：三元组决定架构与操作系统，SDK 决定能链接哪套系统框架，两者必须匹配。最该先知道的是：Apple 平台的多平台构建真正靠的是 SDK 切换，而不是三元组本身。

```swift
swiftc -print-target-info | head -14          # 看默认三元组与运行时库路径
swiftc -target arm64-apple-macosx26.0 opt.swift -o app
xcrun --sdk macosx --show-sdk-path            # macOS SDK 路径
xcrun --sdk iphoneos --show-sdk-path          # iOS SDK 路径
swiftc -target arm64-apple-ios17.0 -sdk "$(xcrun --sdk iphoneos --show-sdk-path)" \
       -emit-library opt.swift -o libopt.dylib

# Linux 目标：交叉编译需要对应平台的 SDK 与静态运行时
swift build -c release --triple x86_64-unknown-linux-gnu --static-swift-stdlib
swiftc -O -static-stdlib opt.swift -o app
# error: -static-stdlib is no longer supported for Apple platforms   ← 仅 Apple 平台被禁

# 通用二进制（macOS 上的「多架构单文件」）
swift build -c release --arch arm64 --arch x86_64
lipo -info .build/release/app
# Architectures in the fat file: ... are: x86_64 arm64
file sw_O
```

Swift 在 Apple 平台上的运行模型是「AOT 代码 + 系统 Swift 运行时」：`libswiftCore` 等动态库由操作系统提供，因此产物体积很小，但要求目标系统版本足够新（这也是 `-target` 里那个 `26.0` 的意义——它声明最低部署版本）。换到 Linux 或 Windows 时系统不带 Swift 运行时，`--static-swift-stdlib` 就成了必选项，否则用户必须先装一整套 Swift 运行时。⚠️ `-static-stdlib` 在 Apple 平台上被显式移除，写上去会直接报错，不要把它当作通用的瘦身手段。跨平台构建还要求目标平台上有对应的 SDK 与工具链，SwiftPM 的 `--triple` 只能选架构与系统，真正的 SDK 路径要靠 `--sdk` 或工具链安装位置给出，这与 C 系「一个 clang 到处编」的体验差别很大。想让一个 macOS 程序同时支持 Intel 与 Apple Silicon，用 `--arch` 叠加即可，SwiftPM 会自动用 `lipo` 合成通用二进制。

📘 [Swift 官方文档 · Swift 编译器](https://www.swift.org/documentation/swift-compiler/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 是 AOT 加自带运行时（GC、调度器）的语言，没有 JIT，也没有可切换的执行模式；它的目标控制在 18 门语言里最简单——**四个环境变量**：`GOOS`、`GOARCH`、`GOARM`（仅 32 位 ARM）、`CGO_ENABLED`。因为工具链内置了所有平台的标准库，不需要额外安装任何东西就能一次编译出十几个平台。最该先知道的是：只要 `CGO_ENABLED=0`，交叉编译就是零依赖的，一旦打开 cgo 就必须准备目标平台的 C 工具链。

```go
go env GOOS GOARCH GOARM CGO_ENABLED
# darwin
# arm64
#
# 1

GOOS=linux   GOARCH=amd64 go build -o app-linux-amd64 .
GOOS=linux   GOARCH=arm64 go build -o app-linux-arm64 .
GOOS=linux   GOARCH=arm   GOARM=7 go build -o app-linux-armv7 .
GOOS=windows GOARCH=amd64 go build -o app.exe .
GOOS=darwin  GOARCH=arm64 go build -o app-mac .
GOOS=js      GOARCH=wasm  go build -o app.wasm .        # 给浏览器/Node 用
GOOS=wasip1  GOARCH=wasm  go build -o app.wasi.wasm .   # WASI 运行时用
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o app-static .
file app-linux-arm64
# ELF 64-bit LSB executable, ARM aarch64, ..., statically linked
go tool dist list | wc -l        # 支持的 GOOS/GOARCH 组合总数
go env -w GOFLAGS=-trimpath      # 把选项固化进 go env 配置
GOOS=js GOARCH=wasm go build -o app.wasm . && \
  cp "$(go env GOROOT)/lib/wasm/wasm_exec.js" .    # 浏览器侧需要的胶水脚本
```

Go 的「运行时」不是可选项：GC、goroutine 调度器、`reflect`、`runtime` 一定会被链进产物，唯一能做的是通过减少依赖间接减小它；`-gcflags`/`-ldflags` 只能影响优化与符号，不能关掉运行时。目标控制上，`GOOS`/`GOARCH` 的组合由 `go tool dist list` 完整列出（覆盖主流操作系统与 amd64、arm64、arm、386、riscv64、ppc64le、s390x、loong64 等架构），且 `wasm` 有两种截然不同的目标——`js/wasm` 需要 JavaScript 胶水代码，`wasip1/wasm` 则面向 WASI 运行时。⚠️ cgo 是交叉编译的分界线：`CGO_ENABLED=1` 时 `net` 包会走系统解析器、`os/user` 会链接 libc，产物不再是静态的，交叉编译还必须提供目标平台的 `CC`，很多「交叉编译失败」都是因为忘了把它设成 0。⚠️ 用 `GOOS=wasip1` 时 `os/exec`、网络等能力取决于运行时实现，不要假设 WUNIX 语义完整。

📘 [`go` 命令文档](https://pkg.go.dev/cmd/go)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的默认运行模型是解释执行：源码编译成字节码后由 CPython 的求值循环执行，没有提前编译，也没有真正意义上的 AOT 产物。从 3.13 起有了实验性的 JIT（PEP 744），到 3.14 仍标为实验特性、且与 free-threading 构建互斥；要拿到原生机器码只能走 Cython、Nuitka、mypyc 这类第三方编译器。最该先知道的是：**官方二进制里的 JIT 默认关闭，唯一开关是环境变量 `PYTHON_JIT=1`**，并且它至今不推荐上生产。

```python
python3 -VV                              # 解释器实现、版本、构建编译器
python3 -c "import platform; print(platform.platform(), platform.machine())"
python3 -c "import sys; print(sys.implementation)"
python3 -c "import sys; print(sys._jit.is_available(), sys._jit.is_enabled(), sys._jit.is_active())"
# False False False        ← 本机 3.14.7 官方二进制未编入 JIT
PYTHON_JIT=1 python3 -c "import sys; print(sys._jit.is_enabled())"
# False                    ← 启用了也需构建期支持
python3 -c "import sysconfig; print(sysconfig.get_config_var('Py_GIL_DISABLED'))"   # 0
python3 -c "import sys; print(sys._is_gil_enabled())"                               # True
python3 -c "import sysconfig; print(sysconfig.get_platform())"
# macosx-15.0-arm64

# 变成原生代码的三条第三方路径
pip install cython && cythonize -i mymod.pyx      # 把 .pyx 编译成 C 扩展
python -m nuitka --standalone --onefile main.py   # 整程序编译成可执行文件
pip install mypyc && mypyc main.py                # 用 mypy 的编译器后端
python3 -m zipapp myapp -o myapp.pyz              # 打包但仍需解释器
python3 -c "import sys; print(sys.base_prefix)"   # 运行时本体位置
```

CPython 的求值循环在 3.14 有两条改进路线：一是新的 tail-call 解释器（`--with-tail-call-interp`，需要 Clang 19 以上），二是实验 JIT，两者都只影响执行速度而不改变语义。JIT 在 3.14 的状态务必记清三点：它是「实现细节」而非语言特性，官方 macOS 与 Windows 二进制以 `yes-off` 构建（所以必须设 `PYTHON_JIT=1`），并且 **free-threaded 构建不支持 JIT**；文档给出的收益区间是「慢 10% 到快 20%」，因此不能当作性能保证。⚠️ 网上流传的 `-X jit` 并不是 3.14 的开关，官方只有 `PYTHON_JIT` 环境变量与构建期的 `--enable-experimental-jit`。真要 AOT，Cython 适合「把热点模块编译成 C 扩展」，Nuitka 适合「把整个应用编译成可执行文件」，mypyc 适合「已有完整类型注解的模块」；三者都不改变 Python 的语义，也不解决 GIL 问题。

📘 [Python 3.14 · sys._jit](https://docs.python.org/3.14/library/sys.html#sys._jit)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 是「一次编写、多目标编译」的语言：同一份源码可以编译到 JVM 字节码（交 JIT）、JavaScript（交引擎）、Kotlin/Native（AOT 到机器码）与 WebAssembly，目标由 Gradle 里的 source set 决定。这四种目标的运行时模型完全不同，产物形态也完全不同。最该先知道的是：多目标不是在编译选项里切换，而是在构建脚本里声明，每个目标有各自的产物目录与运行命令。

```kotlin
# 单文件用 kotlinc 系列命令快速试各目标
kotlinc-jvm Main.kt -d app.jar                        # JVM 目标
kotlinc-js Main.kt -output app.js                     # JavaScript 目标
kotlinc-native Main.kt -o app                         # Native 目标（AOT）

# Gradle 多目标（build.gradle.kts）
# kotlin {
#     jvm()
#     js(IR) { browser(); nodejs() }
#     linuxX64 { binaries { executable { entryPoint = "main" } } }
#     macosArm64 { binaries { executable { entryPoint = "main" } } }
#     wasmJs { browser() }
#     wasmWasi { nodejs() }
# }
./gradlew build
./gradlew jsNodeProductionRun                 # JS 目标：Node 上跑
./gradlew linkReleaseExecutableLinuxX64       # Native 目标：AOT 可执行文件
./gradlew wasmJsBrowserProductionWebpack      # Wasm 目标：打包成 web 资源
ls build/bin/linuxX64/releaseExecutable/      # app.kexe
ls build/dist/js/productionExecutable/        # JS 产物
file build/bin/linuxX64/releaseExecutable/app.kexe
# Mach-O 或 ELF 可执行文件，无 JVM 依赖
```

JVM 目标产出 `.class`/`.jar`，运行时需要 JVM 并享受 HotSpot 的分层编译；JS 目标产出 `.js`，运行时由 V8 之类的引擎决定优化；Native 目标通过 LLVM 做 AOT，产出可直接运行的 `.kexe`，没有虚拟机也没有 JIT，垃圾回收换成了 Kotlin/Native 自带的内存管理器；Wasm 目标分 `wasmJs`（浏览器/Node）与 `wasmWasi`（WASI 运行时）两支，前者依赖 JS 宿主提供胶水层。多目标的代价是**不能随意共享代码**：只有 `commonMain` 里的代码才能被所有目标使用，任何目标特有的 API 都必须放进对应的 source set 并在 `expect`/`actual` 里桥接，写错了会在编译期报「找不到 actual 声明」。⚠️ 各目标的线程与并发语义并不一致：Kotlin/Native 在旧内存模型下限制了跨线程共享可变状态（新内存模型已默认启用），Wasm 目标则根本没有线程概念，把 JVM 上的并发代码直接搬过去通常编译不过。产物命名与目录由目标类型决定，排查问题时先确认 `build/bin/<target>/` 与 `build/dist/` 下的真实输出。

📘 [Kotlin 多平台](https://kotlinlang.org/docs/multiplatform.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的运行时模型是「编译成字节码 + 运行期 JIT」，`javac` 只负责前半段；由于字节码是平台无关的，Java 的「目标控制」主要不是指架构，而是指**语言与 API 版本**：`--release` 声明要兼容的最低 JDK，`--enable-preview` 打开预览特性，而真正的平台绑定发生在运行时的 JVM 实现上。想要 AOT 产物则要换用 GraalVM 的 `native-image`。最该先知道的是：`--release` 同时约束语法、字节码版本与 API 集合，比分别写 `-source`/`-target` 可靠得多。

```java
java --version
javac --release 25 Main.java        # 用 JDK 25 的 API 与 class 版本，class 文件版本 69
javac --release 21 Main.java        # 在 JDK 26 上生成可跑在 JDK 21 的产物
javac --enable-preview --release 26 Main.java
java --enable-preview Main          # 运行预览特性必须显式再开一次
javap -v Main.class | grep -E "major|minor"        # major version 即 class 版本
jar --describe-module --file app.jar                # 模块信息
java --list-modules | head                          # 当前 JDK 提供的模块
java -XX:+PrintFlagsFinal -version | grep -i tiered | head -3

# 真正的 AOT：GraalVM
native-image -O2 -cp app.jar Main app-native        # 无 JVM、无 JIT 的原生可执行文件
./app-native
file app-native
# Mach-O 或 ELF 可执行文件
java -XX:AOTCache=app.aot -cp app.jar Main          # JDK 24+：只提前类加载与链接，仍用 JIT
```

`--release N` 是一个组合约束：它把编译器的 `-source`、`-target` 与 `--system`（平台 API 签名）一起锁定到 JDK N，从而避免「用了新版 API 却在旧 JDK 上运行」这类只能在运行期暴露的错误，新代码一律应该用它而不是裸写 `-source`/`-target`。预览特性要开两次：编译时 `--enable-preview`，运行时还要再给 JVM 一次，因为预览特性的字节码带有特殊标记。平台绑定方面，Java 的 `.jar` 本身跨平台，真正的目标是 JVM 实现——同一份 jar 在 HotSpot 上走分层编译，在 GraalVM JIT 上走另一套优化，在 `native-image` 上则完全没有 JVM。⚠️ `native-image` 与 JIT 的取舍是根本性的：它换来毫秒级启动与更低内存，但失去动态类加载与 `Reflection.Emit`，反射、资源、JNI、序列化都必须写进配置，而且**用 `-O2` 之外的等级前要先测量**，`-Os` 与 `-Ob` 主要面向体积。⚠️ JDK 24 引入的 AOT cache（`-XX:AOTCache`）与 `native-image` 完全不是一回事：前者只把类的加载与链接结果提前算好，运行时依旧由 JIT 编译代码，所以启动变快但峰值性能不变。

📘 [`javac` 手册（JDK 25）](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javac.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 是 AOT 语言，运行模型由编译器后端（LLVM 或 GCC）决定，没有 JIT 也没有运行时切换；目标控制靠 `--target=<triple>` 选定架构与操作系统，用 `--sysroot` 指向目标平台的头文件与库，用 `-march`/`-mtune`/`-mcpu` 选定指令集与调度模型。同一个 clang 可以同时充当本机编译器与交叉编译器。最该先知道的是：`--target` 换的是**整套 ABI 与默认开关**，因此必须在编译与链接时给同一份参数，否则会出现难以理解的链接错误。

```cpp
clang++ --print-target-triple                 # arm64-apple-darwin25.6.0
clang++ --target=aarch64-linux-gnu -O2 -c bench.cpp -o b_arm64.o
clang++ --target=x86_64-w64-windows-gnu -O2 -c bench.cpp -o b_win.obj
clang++ --target=riscv64-linux-gnu -O2 -c bench.cpp -o b_rv.o
clang++ -O2 -march=native -mtune=native bench.cpp -o b_native
clang++ -O2 -march=armv8.4-a -mtune=apple-m1 bench.cpp -o b_mar
clang++ -O2 -mcpu=apple-m1 bench.cpp -o b_cpu        # -mcpu 相当于两者合一
clang++ --target=aarch64-linux-gnu --sysroot=/opt/sysroot -O2 bench.cpp -o app_arm64
clang++ --print-search-dirs | head -6                # 查看默认库搜索路径

# WebAssembly 目标（需要 wasi-sdk 或 Emscripten 提供 sysroot）
clang++ -std=c++23 -O2 --target=wasm32 -nostdlib -Wl,--no-entry -Wl,--export-all -o app.wasm bench.cpp
wasmtime app.wasm
emcc -O2 -s WASM=1 main.cpp -o main.html             # Emscripten 路线
clang++ -std=c++23 -O2 main.cpp -o main.js -s WASM=1 # 同上，em++ 才能编 C++
```

C++ 的运行时控制体现在三个层次：语言运行时（`libstdc++` 还是 `libc++`、静态还是动态）、异常与 RTTI 是否开启（`-fno-exceptions`、`-fno-rtti`，嵌入式与游戏引擎常用）、以及线程模型。目标控制的核心是三元组与 sysroot 的配对：`--target=aarch64-linux-gnu` 只是告诉 clang 用哪套 ABI 与内置定义，真正让 `#include <stdio.h>` 找到目标平台头文件的是 `--sysroot`（或跨平台工具链自动提供的 sysroot）。⚠️ 常见错误是编译时给了 `--target` 而链接时忘了，结果把目标平台的目标文件交给宿主链接器，报一堆「架构不匹配」或「未知重定位」；用 CMake 时应当把三元组设为 `CMAKE_CXX_COMPILER_TARGET`，让编译与链接用同一份配置。`-march=native` 只适合在本机跑的程序，分发给别人必须写死基线（例如 `-march=x86-64-v3` 或具体的 `armv8-a`），否则在老机器上会因非法指令崩溃。WebAssembly 目标没有系统调用，要跑带文件或网络的服务必须使用 WASI sysroot，同时用 `-nostdlib` 加链接器参数控制导出与入口。

📘 [Clang · 交叉编译](https://clang.llvm.org/docs/CrossCompilation.html)

{{% /tab %}}

{{% tab header="C" %}}

C 的运行模型同样纯粹是 AOT，而且比 C++ 更少变数：没有异常表、没有 RTTI、没有模板实例化，运行时的全部内容就是可选的 libc。目标控制与 C++ 共用一套 `--target` 加 `--sysroot` 机制，只是 C 更常直接用 `musl` 或 `zig cc` 来绕开交叉工具链的配置麻烦。最该先知道的是：C 的交叉编译难点从来不是编译器，而是 libc 与启动文件（`crt0.o` 之类）。

```c
clang --print-target-triple          # arm64-apple-darwin25.6.0
clang --target=aarch64-linux-gnu -O2 -c fib.c -o fib_arm64.o
clang --target=riscv64-linux-gnu -O2 -c fib.c -o fib_rv.o
clang --target=wasm32-wasi -O2 fib.c -o fib.wasm
wasmtime fib.wasm                    # WASI 运行时装上后可直接运行
clang -O2 -march=armv8.4-a -mcpu=apple-m1 fib.c -o fib_m
clang --target=aarch64-linux-gnu --sysroot=/opt/sysroot -O2 -static fib.c -o app_arm64
gcc -dumpmachine                     # 例如 x86_64-linux-gnu
gcc -print-sysroot                   # 空输出表示用系统默认
musl-gcc -O2 -static fib.c -o fib_musl
zig cc -target aarch64-linux-musl -O2 fib.c -o fib_zig    # 用 zig 当交叉编译器
file fib_musl fib_zig
```

C 的运行时控制其实只有三个问题：用哪个 libc（glibc、musl、uclibc 还是完全 `-nostdlib`）、是否静态链接、是否保留 `crt` 启动文件（`-nostartfiles` 时得自己写 `_start`）。目标控制则几乎完全交给「三元组 + sysroot + libc 实现」这三件东西，一旦其中任何一个与目标平台不匹配，就会在链接阶段以找不到 `crt0.o`、`crt1.o` 或符号版本错误的形式暴露。⚠️ macOS 是最典型的反例：它不提供静态 libSystem，因此 `clang -static` 会直接报 `ld: library 'crt0.o' not found`，想给 macOS 做「可移植单文件」只能退回动态链接或改用 musl 目标的 Linux 产物。⚠️ `-march=native` 与 `-mcpu`/`-mtune` 的区别要分清：`-march` 决定可用的指令集（能否用某条指令），`-mtune` 只影响调度与代价模型（不改变可用指令），`-mcpu` 在 AArch64 上近似二者合一；只调 `-mtune` 的产物能在更多机器上跑，只调 `-march=native` 的产物则可能直接崩溃。WebAssembly 在 C 侧同样需要 WASI 或 Emscripten 提供 sysroot，`--target=wasm32-wasi` 只是前半句。

📘 [Clang · 交叉编译](https://clang.llvm.org/docs/CrossCompilation.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 是 JIT 语言：解释器把源码降成 IR，由 LLVM 在**首次以具体类型调用时**编译成机器码，因此同一函数的每次类型特化都会触发一次编译。运行时可切换的开关因此特别多——`--compile=min|yes|all|no` 控制编译激进程度，`--sysimage` 换一个预编译好的系统镜像。目标控制是 Julia 的弱项：sysimage 与预编译缓存都绑定宿主平台与 Julia 版本。最该先知道的是：Julia 的「目标控制」主要是**换 sysimage 而不是换架构**，真正的交叉编译要靠 juliac 与目标平台的工具链。

```julia
julia --version
julia -e 'println(Sys.MACHINE); println(Sys.ARCH); println(Sys.KERNEL); println(Sys.WORD_SIZE)'
# aarch64-apple-darwin25.6.0
# aarch64
# Darwin
# 64

julia --compile=min -e 'println(sum(1:10))'     # 最少编译，启动最快、循环最慢
julia --compile=yes -e 'println(sum(1:10))'     # 默认
julia --compile=all -e 'println(sum(1:10))'     # 预编译所有方法（含被调用的）
julia --compile=no  -e 'println(sum(1:10))'     # 完全解释执行
julia --sysimage MySys.so -e 'using MyPkg; println("ok")'
julia --sysimage-native-code=no -e 'println("不带原生代码的镜像")'
julia -e 'println(Sys.BINDIR); println(Base.julia_cmd())'
julia -e 'using Pkg; Pkg.precompile()'          # 预编译依赖，缩短首次加载
julia -e 'using PackageCompiler; create_app("MyApp", "build/MyApp")'
juliac --output-exe myapp --bundle build --trim=safe --experimental app.jl
ls ~/.julia/compiled/v1.13/                     # 平台相关的预编译缓存
```

Julia 的性能模型是「编译期开销换运行期速度」：默认的 `--compile=yes` 会在第一次调用时按具体类型生成专用机器码，这让数值代码跑得极快，也让短脚本启动很慢；`--compile=min` 让解释器直接执行、跳过大部分特化，适合「跑一次就退出」的 CI 脚本，代价是循环慢一个数量级。`--compile=all` 在包预编译时把所有方法都编出来，能显著缩短用户首次调用某条路径的等待，但会让缓存变大、预编译时间变长，适合作为库作者的默认策略。⚠️ `--sysimage` 指定的镜像必须与当前 Julia 版本、架构、以及构建它的机器严格匹配，用别人的 sysimage 通常会 `Segmentation fault` 或 `InitError`；`PackageCompiler` 的 `create_app` 与 `juliac` 之所以要求「在目标平台上构建」，正是这个原因。⚠️ `--compile=min` 与 `--check-bounds=yes` 这类组合会让代码慢得离谱，它们是调试与诊断工具，不要写进生产启动脚本；反过来，想把 CPU 特性（AVX2、AVX-512）用到极致，也必须在构建 sysimage 的那台机器上开启对应目标，JIT 时无法凭空获得。

📘 [Julia · 命令行开关](https://docs.julialang.org/en/v1/manual/command-line-interface/)

{{% /tab %}}

{{% tab header="C#" %}}

.NET 的运行模型是「编译成 IL + 运行期 JIT」，另外提供两条提前编译路线：`PublishReadyToRun` 把 IL 预编译成机器码但保留 JIT，`PublishAot` 则彻底去掉 JIT 产出原生可执行文件。目标控制在 .NET 里由两个属性分工：`TargetFramework` 决定语言与 API 面（例如 `net10.0`），`RuntimeIdentifier` 决定操作系统与架构（例如 `linux-musl-x64`）。最该先知道的是：**`RuntimeIdentifier` 与 `TargetFramework` 是正交的**，换平台只改前者，换 API 面只改后者。

```csharp
dotnet --info | head -20                       # SDK、运行时与平台信息
dotnet --list-runtimes | head -3
dotnet build -c Release -f net10.0
dotnet publish -c Release -r linux-x64 --self-contained true
dotnet publish -c Release -r linux-musl-x64 --self-contained true -p:PublishAot=true
dotnet publish -c Release -r linux-arm64 --self-contained true -p:PublishTrimmed=true
dotnet publish -c Release -r osx-arm64 -p:PublishReadyToRun=true
dotnet publish -c Release -r win-x64 --self-contained false
dotnet publish -c Release -r linux-x64 -p:PublishSingleFile=true --self-contained true
file bin/Release/net10.0/linux-x64/publish/app
# ELF 64-bit LSB pie executable, x86-64, ..., dynamically linked
file bin/Release/net10.0/linux-musl-x64/publish/app    # AOT 产物：原生可执行文件

# .csproj 里的等价声明
# <PropertyGroup>
#   <TargetFramework>net10.0</TargetFramework>
#   <RuntimeIdentifiers>linux-x64;linux-arm64;win-x64;osx-arm64</RuntimeIdentifiers>
#   <PublishAot>true</PublishAot>
# </PropertyGroup>
```

`TargetFramework` 是可移植面的边界：设为 `net10.0` 就能用 C# 14 与 .NET 10 的全部 API，设为 `net8.0` 则编译器会拒绝更新的 API，这是多目标库控制兼容性的标准手段（`<TargetFrameworks>` 可以一次产出多份）。`RuntimeIdentifier` 才是平台绑定：`-r linux-x64` 会去拿对应运行时的原生资源，`linux-musl-x64` 用 musl 而不是 glibc，得到真正静态链接的 AOT 产物；`-r` 与 `--self-contained false` 组合则是「带平台资源的框架依赖发布」。⚠️ Native AOT 支持的操作系统与架构是有限的，Windows 上还需要 VS2022 的 C++ 工作负载、Linux 上需要 clang 与构建工具，且它**只支持特定的 RID**，对不支持的组合会在还原阶段直接报错而不是给出可用的降级方案。⚠️ ReadyToRun 与 Native AOT 都必须显式给 `-r`，因为两者的产物都含机器码，天然是平台相关的——这是 .NET 里最容易被忽视的「目标控制」约束。

📘 [.NET · 运行时标识符（RID）目录](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 有两个运行时：开发期的 Dart VM 用 JIT 执行，发布期的 AOT 编译器产出原生机器码，两者共享同一套语义。目标控制体现在 `dart compile` 的子命令选择上——`exe` 与 `aot-snapshot` 是原生目标，`js` 与 `wasm` 是 Web 目标，`kernel` 是平台无关的中间表示。最该先知道的是：**`dart compile kernel` 没有 `--platform` 选项**，交叉编译只有 `exe`/`aot-snapshot` 通过 `--target-os`/`--target-arch` 支持，而且目标操作系统目前只支持 Linux。

```dart
dart --version
dart run bin/myapp.dart                    # JIT：开发期默认
dart compile exe bin/myapp.dart -o build/myapp          # AOT：发布期
dart compile js   -O2 -o out/main.js web/main.dart      # Web：JavaScript
dart compile wasm -O2 -o out/main.wasm web/main.dart    # Web：WebAssembly
dart compile kernel bin/myapp.dart -o build/app.dill    # 平台无关 IR

# 交叉编译（Dart 3.8 起支持 Linux ARM64/x64，3.9 起加入 ARM/RISCV64）
dart compile exe bin/myapp.dart -o build/app-linux-x64 --target-os=linux --target-arch=x64
dart compile exe bin/myapp.dart -o build/app-linux-arm64 --target-os=linux --target-arch=arm64
dart compile exe bin/myapp.dart -o build/app-linux-riscv64 --target-os=linux --target-arch=riscv64
file build/myapp
# Mach-O 64-bit executable arm64      ← 未指定 target 时编的是宿主平台
dart run --observe bin/myapp.dart          # 打开 VM service，DevTools 可连接
dartaotruntime build/app.aot               # 用 dartaotruntime 跑 AOT 模块
```

Dart 的执行模型切换是**整个程序级别**的，而不是逐函数：`dart run` 全程 JIT，`dart compile exe` 全程 AOT，没有「部分方法回退到 JIT」的机制（这一点与 .NET 的 ReadyToRun + JIT 混合模式不同），因此 AOT 产物冷启动快且行为可预测，JIT 则在长期运行的热点代码上峰值更高。`dart compile kernel` 产出的是 Kernel AST 二进制，平台无关、可跨操作系统运行，常被用作「先编 IR 再 AOT」的两阶段构建中间产物。⚠️ 交叉编译的边界要写清楚：官方文档只声明 `--target-os=linux` 配 `--target-arch=arm|arm64|riscv64|x64`，并没有提供「编出 macOS 或 Windows 可执行文件」的能力；网上常见的 `--platform` 参数属于 dart2wasm 的内部实现，不是 `dart compile kernel` 的公开选项，照抄会报未知选项。⚠️ 跨编译时会临时下载目标平台的 SDK 二进制并缓存到 `~/.dart`，离线环境必须先预热缓存。

📘 [`dart compile`](https://dart.dev/tools/dart-compile)

{{% /tab %}}

{{% tab header="R" %}}

R 的运行模型是「解释器 + 可选的字节码 JIT」，**没有 AOT，也没有交叉编译目标开关**：`R` 进程本身就是平台的绑定物，`.Platform` 只报告宿主平台的信息，`R CMD config` 报告的是编译这个 R 时用到的工具链。R 的「目标控制」因此退化成「用哪一份 R 安装」：源码安装的包必须与 R 的版本、架构、编译选项一致。最该先知道的是：R 的跨平台分发单位是**包**，而包的二进制兼容性由 R 自身的构建配置决定，用户无法在安装时切换目标。

```r
R --version | head -2
Rscript -e 'print(R.version.string)'
Rscript -e 'print(R.version$platform)'        # 例如 aarch64-apple-darwin20
Rscript -e 'print(.Platform)'
# $OS.type   "unix"
# $file.sep  "/"
# $dynlib.ext ".so"
# $GUI       "AQUA"
# $endian    "little"
# $pkgType   "mac.binary"
# $path.sep  ":"
# $r_arch    ""
Rscript -e 'print(R.home("bin"))'
Rscript -e 'cat(R.home("include"), "\n")'

# 编译期配置：查看这份 R 是用什么工具链构建的
R CMD config CC
R CMD config CFLAGS
R CMD config --all | grep -E "^(CC|CXX|CPPFLAGS|LTO)" | head
R CMD SHLIB mymod.c                            # 用这份 R 的配置编译共享库
Rscript -e 'print(capabilities())'             # 编译期决定的能力位（含 long.double、profmem 等）
Rscript -e 'compiler::enableJIT(-1)'           # 3，运行期 JIT 级别
```

R 本身在构建时可以用 `--enable-lto`（链接时优化）与 `--enable-memory-profiling`（开启 `Rprofmem` 与 `Rprof(memory.profiling=TRUE)`）之类的 `configure` 开关，但这些开关是**发行版与系统管理员的决定**，用户装完包之后无法再改变；`.Platform` 与 `capabilities()` 就是用来探测这些构建期选择的接口。⚠️ 因此「同一份 R 代码在不同机器上表现不同」往往不是代码问题，而是两份 R 的构建配置不同（例如一个开了 LTO 与参考 BLAS、另一个没有）。R 也**没有** `--target` 之类的交叉编译选项：官方文档里不存在「为别的架构编译一个 R 包」的流程，跨平台分发的正解是在目标平台上构建二进制包，或者干脆只发布源码包让用户本地编译。⚠️ 需要按平台条件编译时，标准做法是写进 `src/Makevars` 与 `src/Makevars.win`，并用 `R CMD config` 拿到当前工具链，而不是在 R 代码里猜平台。

📘 [R · 安装与管理（R-admin）](https://cran.r-project.org/doc/manuals/r-release/R-admin.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 同时是语言、编译器和交叉编译工具链：`zig build-exe` 是纯 AOT，`zig cc`/`zig c++` 则能在不装任何交叉工具链的情况下编译 C 与 C++。目标由 `-target <arch>-<os>-<abi>` 三元组指定，Zig 自带 libc 源码与各平台的启动文件，所以从 x86_64-linux-musl 到 thumb-freestanding-gnueabihf 都能一次编出。最该先知道的是：Zig 没有 JIT，也没有需要运行时安装的「目标 SDK」——`-target` 一写就能编。

```zig
zig version
zig targets | head -30                       # 支持的全部 arch / os / abi 组合

zig build-exe main.zig -target x86_64-linux-musl -O ReleaseSmall -fstrip
zig build-exe main.zig -target aarch64-macos -O ReleaseFast
zig build-exe main.zig -target aarch64-linux-gnu -O ReleaseSafe
zig build-exe main.zig -target wasm32-freestanding -O ReleaseSmall
zig build-exe main.zig -target wasm32-wasi -O ReleaseSmall
zig build-exe main.zig -target thumb-freestanding-gnueabihf -O ReleaseSmall
zig build-exe main.zig -target x86_64-windows-gnu -O ReleaseFast

# 微架构：要不要用上目标机器的全部指令
zig build-exe main.zig -O ReleaseFast -mcpu=baseline      # 保守，兼容性最好
zig build-exe main.zig -O ReleaseFast -mcpu=native        # 只在本机跑
zig build-exe main.zig -O ReleaseFast -mcpu=znver4        # 显式指定

# 用 zig 当 C/C++ 交叉编译器
zig cc -target x86_64-windows-gnu -O2 hello.c -o hello.exe
zig cc -target aarch64-linux-musl -static hello.c -o hello-arm64
zig c++ -target aarch64-linux-gnu -std=c++23 -O2 main.cpp -o main-arm64
wasmtime main.wasm                           # 跑 wasm32-wasi 产物
```

Zig 的运行模型是「编译期完成一切」：没有虚拟机、没有 JIT、没有反射，运行时只有你显式选择的标准库部分（甚至可以完全不用 `std`）；0.15 起连 `async`/`await` 关键字都已从语言中移除，异步 I/O 改由标准库的 `std.Io` 接口提供。目标控制的两层含义要分清：`-target` 的三元组由「架构 + CPU 特性 + 操作系统 + OS 版本范围 + ABI + ABI 版本」组成，`-mcpu` 则只调架构内的指令集与调度，`baseline` 表示「该架构的最低公共子集」，`native` 表示宿主 CPU 的全部特性。⚠️ 这两个层次混用会出两种典型错误：把 `-mcpu=native` 的产物分发出去会在老 CPU 上非法指令崩溃；把 `thumb-freestanding-gnueabihf` 之类的裸机目标当 Linux 目标用，会因为没有 syscall 接口而链接失败。`zig cc` 的价值在于它**内置**了各平台的 libc（musl、glibc 头文件、mingw-w64、macOS SDK 的替身），因此只需一条命令就能产出面向 Windows 或 ARM Linux 的静态二进制，这是把 Zig 引入现有 C/C++ 项目最常见的理由，也是替代手工配置 sysroot 的最省事方案。

📘 [Zig 语言参考 · 目标](https://ziglang.org/documentation/0.15.1/#Targets)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 是纯解释执行的语言（字节码由 VM 执行），**没有交叉编译这个概念**：官方实现里不存在 `--target` 之类的选项，因为 Lua 的编译单位是「宿主程序 + 脚本」，脚本本身是文本，字节码也只是平台无关（在配置一致的前提下）的中间格式。最该先知道的是：字节码的可移植性有硬前提——整数/浮点类型位数、字节序、以及编译期配置必须一致，否则加载时会直接报格式错误。

```lua
lua -v
lua -e 'print(_VERSION)'
luac -o main.luac main.lua                # 编译成字节码
lua main.luac                             # 字节码可以在同配置的平台间复制
luac -s -o main.strip.luac main.lua       # 剥掉调试信息

# 字节码头里带校验：整数宽度、浮点类型、字节序、LUAC_DATA 都对不上就拒绝加载
lua -e 'local f = assert(loadfile("main.luac")); f()'
# 若字节码来自不兼容的配置，会看到：
# bad binary format (truncated precompiled chunk)  或  格式校验失败

# 「交叉编译」的实际上是解释器本体，属于构建问题
# make linux CC=arm-linux-gnueabihf-gcc        ← 用交叉工具链编 Lua 解释器
# make linux MYCFLAGS="-O2 -DLUA_32BITS"       ← 32 位整数配置
gcc -O2 -shared -fPIC -I/usr/include/lua5.5 mymod.c -o mymod.so   # C 模块随平台走

# 想让 Lua 跑得更快或更小：换实现而不是换目标
luajit -v
luajit -jv -e 'local s=0 for i=1,1000000 do s=s+i end print(s)'
# LuaJIT 是独立的第三方实现，跟踪 Lua 5.1 语义并自带 JIT
```

Lua 的可移植性分两层：脚本源码完全可移植，`luac` 产出的字节码只在「同一份 Lua 配置」内可移植——官方在字节码头部写入 `LUAC_DATA` 标记、`sizeof(int)`、`sizeof(size_t)`、指令宽度、整数与浮点类型标记、以及字节序，任何一项不匹配都会让 `load` 失败并报二进制格式错误。⚠️ 因此「在 64 位机器上编译、拿到 32 位嵌入式设备上跑」这种做法不可靠，稳妥做法是把 `.lua` 源码带过去在目标平台编译，或者用 `string.dump` 之前在两端确认配置一致。⚠️ `LUA_32BITS`、`LUA_USE_C89`、`LUA_USE_APICHECK` 这类编译期宏会改变语言运行时的行为（整数宽度、API 检查），它们必须在解释器与 C 模块之间保持一致，否则会在传参时出现难以定位的内存错误。LuaJIT 与 eLua 是社区为「更快」与「更小/嵌入式」做的分支实现，⚠️ LuaJIT 面向 Lua 5.1 语义，不能直接拿来跑 5.4/5.5 的脚本（`<const>`、`<close>`、整除运算符都不支持），选型时必须先确认语言版本。

📘 [Lua 5.5 参考手册](https://www.lua.org/manual/5.5/manual.html)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的运行模型是「先编译成 JavaScript，再交给引擎决定执行方式」：`tsc` 不做任何优化，也不产出机器码，所谓「目标控制」在这里是**编译目标与模块系统的选择**——`target` 决定语法降级程度，`module`/`moduleResolution` 决定产物是 ESM 还是 CJS 以及如何解析依赖，`lib` 决定可用哪些标准库类型。TypeScript 7 是 Go 重写的原生编译器，官方称完整构建有约 10 倍加速。最该先知道的是：`target` 不是「优化等级」，把它调高不会自动让程序变快，只会让产物更接近源码。

```typescript
npx tsc --showConfig | head -30              # 展开继承与默认值后的最终配置
npx tsc --target es2023 --module nodenext --moduleResolution nodenext --lib es2023
npx tsc --target esnext --module preserve --moduleResolution bundler
npx tsc --noEmit                              # 只检查类型，不产出
node --version

# 现代 Node 目标的两种产物
npx tsc --module esnext --outDir dist-esm
npx tsc --module commonjs --outDir dist-cjs
cat package.json
# { "type": "module",
#   "exports": { ".": { "import": "./dist-esm/index.js", "require": "./dist-cjs/index.js" } } }

# Node 侧的类型擦除（属运行时选项，不是 tsc 选项）
node main.ts                                   # Node 26 默认剥离类型，不做类型检查
node --no-strip-types main.js                  # 关掉类型剥离
# 模块语法探测自 Node 22.7 起默认开启；Node 26 已移除 --experimental-transform-types
```

`target` 与 `lib` 是两件事：`target` 决定降级后的语法形态，`lib` 决定类型检查时能看到哪些标准库接口（例如设 `lib: ["es2023"]` 之后 `document` 就不再存在），两者配错会得到「语法能过但类型报错」或反之的奇怪现象。`module` 与 `moduleResolution` 必须成对选择：`nodenext` 会按 Node 的真实规则解析（含 `exports` 字段与扩展名要求），`bundler` 则放宽扩展名要求以适配打包器，⚠️ 把 `moduleResolution: node`（旧 Node 解析）用在现代包上会因为 `exports` 字段不被识别而报「找不到模块」。⚠️ TypeScript 7 把一批旧配置变成了硬错误（`target: es5`、`downlevelIteration`、`moduleResolution: node/node10/classic`、`module: amd/umd/systemjs/none`、`baseUrl` 等），并改了默认值（`strict` 打开、`module` 为 `esnext`、`rootDir` 为 `./`、`types` 为空数组），升级到 7 时这一组是必查项。Node 侧的类型擦除是另一条独立路线：它只删类型不做类型检查，因此能直接 `node main.ts`，但要求代码不使用需要代码生成的语法（枚举、参数属性、含运行期代码的命名空间），这些语法会直接报 `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`——Node 26 已移除把它们转换掉的 `--experimental-transform-types`，需要那些语法就必须改用 `tsc`、`tsx` 这类工具。类型擦除自 Node 24.12／25.2 起是稳定特性并默认开启，`--no-strip-types` 可以关掉它。

📘 [TypeScript · tsconfig 参考](https://www.typescriptlang.org/tsconfig/)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有编译期目标控制，源文件就是交付物，执行方式完全由宿主引擎决定：浏览器与 Node 都在运行时做解释加 JIT。它的「运行时与目标控制」因此体现在**模块系统的选择**与**Node 的实验特性开关**上——ESM 与 CJS 的互操作规则、`package.json` 的 `type` 字段、以及一堆 `--experimental-*` 标志。最该先知道的是：Node 的目标不是「平台」而是「模块语义」，`"type": "module"` 与文件扩展名共同决定一个 `.js` 会被当成 ESM 还是 CJS。

```javascript
node -v
node main.js
node --input-type=module -e 'import("node:fs").then(m => console.log(typeof m.readFile))'
# function
node --experimental-detect-module main.js     # 无 package.json 时按语法自动判断 ESM/CJS
node --experimental-vm-modules -e 'console.log(typeof require("node:vm").SourceTextModule)'
node --experimental-sea-config sea-config.json
node --build-snapshot --snapshot-blob app.blob main.js
node --no-experimental-fetch main.js          # 显式关掉已默认开启的实验特性
node --v8-options | grep -E "harmony" | head -5
cat package.json
# { "name": "app", "type": "module", "main": "./index.js" }
node -e 'console.log(require("./package.json").type)'   # module
node --force-node-api-uncaught-exceptions-policy -e '1' # 另一类实验开关
```

模块系统是 Node 里最容易出错的一环：`.mjs` 永远是 ESM、`.cjs` 永远是 CJS、`.js` 则看最近的 `package.json` 里 `type` 是 `module` 还是省略（省略即 CJS）；ESM 里没有 `require`、`__dirname`、`__filename`（要用 `import.meta.url` 推导），CJS 里不能 `import`（只能动态 `import()`）。⚠️ 混用两套语义时最常见的症状是 `ERR_REQUIRE_ESM`（CJS 想 require 一个 ESM 包）与 `Cannot use import statement outside a module`（ESM 语法被按 CJS 解析），两者的根因都是 `type` 字段与文件扩展名的组合与预期不符，改 `type` 之前要先确认全部依赖是否都支持 ESM。Node 的 `--experimental-*` 标志属于**运行时选项**，与编译选项完全无关：它们开启的是 Node 自身的新能力（类型擦除、模块探测、VM 模块、SEA），每次大版本升级都要重新确认哪些已经默认开启、哪些已被移除。⚠️ 与本机环境对照：本机装的是 Node 24，而基线按 Node 26 书写，`--experimental-sea-config`、`--build-snapshot`、`--snapshot-blob`、`--experimental-detect-module` 这几项在两者上均可用，但新版本里部分实验标志会转正，写进脚本前应先用 `node --help` 核对。

📘 [Node.js · 命令行选项](https://nodejs.org/api/cli.html)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的运行模型是「编译成 opcode + Zend VM 解释执行」，可选由 OPcache 缓存 opcode、再由 JIT 把热点编译成机器码；没有 AOT，也没有多平台目标三元组。它的「目标控制」实际发生在**编译 PHP 自身**的阶段：`./configure` 决定启用哪些扩展、是否开启 ZTS（线程安全）、以及优化与调试选项，产物因此是平台与配置绑定的。最该先知道的是：PHP 扩展与 PHP 主程序的 ABI 必须严格匹配（ZTS/NTS、VC 版本、API 版本号），这是 PHP 生态里最常见的兼容性问题。

```php
php -v
php -m | head -20                                # 已加载扩展
php -i | grep -E "Thread Safety|Debug Build|Zend Extension Build|PHP API"
# Thread Safety => disabled
# Debug Build => no
# Zend Extension Build => API420240925,NTS
php -r 'echo PHP_INT_SIZE, " ", PHP_OS_FAMILY, " ", php_uname("m"), "\n";'
# 8 Linux x86_64
php -r 'echo PHP_BINARY, "\n";'
php --ini                                         # 实际加载的 ini 文件
php -i | grep "Configure Command"                 # 这份 PHP 是怎么编出来的
php -r 'var_dump(function_exists("opcache_get_status"));'

# 从源码构建时的 configure 选项（决定能力，不是运行期开关）
./configure --disable-all --enable-cli --enable-opcache --enable-opcache-jit \
            --with-zlib --enable-mbstring --enable-json
make -j"$(nproc)"
sudo make install
php -i | grep -E "opcache|jit" | head -6
# Windows 上必须挑选与 PHP 版本、架构、VC 运行时一致的 DLL，且要区分 TS/NTS
```

PHP 的目标控制里没有「交叉编译」这一项，因为官方只提供少数平台的预编译二进制，其他平台一律自行编译：`./configure` 的 `--enable-*` 与 `--with-*` 决定把哪些扩展静态编进 `php` 可执行文件、哪些作为共享库（`.so`）动态加载，这直接影响启动速度与分发体积（静态编入的扩展无需 `extension=` 指令）。⚠️ ABI 兼容是硬约束：ZTS 与非 ZTS 的扩展互不通用，Windows 上还要匹配 VC 运行时与 PHP 的 API 版本号（`Zend Extension Build` 那一行），版本不匹配的表现通常是启动时打印「Unable to load dynamic library」或直接崩溃，而不是给出明确的版本错误。⚠️ `--disable-all` 加按需 `--enable-*` 能做出体积极小的 PHP，但要注意 CLI、`opcache`、`json` 这类基础能力默认行为会变，做容器镜像时先用 `php -m` 对比官方镜像的扩展清单再决定删哪些。运行时的 OPcache/JIT 则属于上两节的范畴，它们只影响执行方式，不改变平台与 ABI。

📘 [PHP · Unix 系统安装](https://www.php.net/manual/en/install.unix.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的运行模型是「编译成 YARV 字节码 + 栈式虚拟机解释执行」，可选叠加 YJIT 或 ZJIT 做运行期即时编译；没有 AOT，也没有 `--target` 之类的交叉编译开关。Ruby 的目标控制体现在**构建 Ruby 本体时的 `configure` 选项**与 `RbConfig` 暴露的配置上：`--enable-shared` 决定 libruby 是静态还是动态，`--with-jemalloc` 换分配器，平台三元组由构建时的 `host`/`target` 记录。最该先知道的是：C 扩展必须与 Ruby 的 ABI、平台三元组、以及是否共享库完全匹配，否则 `require` 会直接失败。

```ruby
ruby -v
ruby -e 'puts RUBY_PLATFORM'                     # arm64-darwin25
ruby -e 'puts RUBY_DESCRIPTION'
ruby -e 'puts RUBY_ENGINE, RUBY_ENGINE_VERSION'  # ruby / 4.0.6
ruby -e 'puts RbConfig::CONFIG["host"]'
ruby -e 'puts RbConfig::CONFIG["target"]'
ruby -e 'puts RbConfig::CONFIG["ENABLE_SHARED"]' # yes 或 no
ruby -e 'puts RbConfig::CONFIG["CC"]'
ruby -e 'puts RbConfig::CONFIG["archdir"]'       # 头文件目录，编译 C 扩展要用
ruby -e 'require "rbconfig"; puts RbConfig.ruby' # 当前解释器路径

# 构建 Ruby 本体（决定运行模型与 ABI）
./configure --enable-shared --disable-install-doc --with-jemalloc --enable-yjit
make -j"$(nproc)"
sudo make install
ruby -e 'puts RbConfig::CONFIG["configure_args"]'

# C 扩展按当前平台编译
ruby extconf.rb && make && make install
ruby --disable-gems -e 'puts "no gems"'          # 运行期选项，与目标无关
ruby --yjit -e 'puts "yjit on"'
```

Ruby 的运行时最特别的一点是**解释器与 gem 的 ABI 强绑定**：C 扩展用 `mkmf` 读取 `RbConfig` 里这套 Ruby 的头文件路径与编译选项来编译，因此换 Ruby 版本（甚至同版本换构建配置）后必须重新编译所有原生 gem，否则 `require` 会报「incompatible library version」或符号缺失。⚠️ `--enable-shared` 让 libruby 成为动态库，扩展可以动态链接到它，代价是部署时多一个库文件且启动略慢；默认的静态构建把 libruby 编进可执行文件，扩展则各自静态链接一份，分发更简单但体积更大。⚠️ `--with-jemalloc` 换的是内存分配器，会改变内存占用与碎片表现，对长驻服务通常有收益，但对短脚本会略增启动开销。Ruby 也没有「编译成独立可执行文件」的官方路径：`ruby app.rb` 永远需要解释器，社区方案（Travelling Ruby 等）本质是把整个 Ruby 运行时打包，属于第三方工程而非语言能力。

📘 [Ruby · 编写 C 扩展](https://docs.ruby-lang.org/en/master/extension_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 调试与分析开关

这一组按用途分成三层：**调试信息**决定崩溃与断点能不能对上源码，**sanitizer** 在运行时主动抓出内存、并发与未定义行为，**性能分析**回答「时间花在哪里」。三层的开销依次递增，也依次更不适合生产：调试信息只在磁盘上占体积，sanitizer 会让程序慢上数倍并需要整套依赖都重新编译，profiler 的采样开销通常可以接受但会改变缓存行为。判断该用哪个的标准很简单——找出「为什么错了」用调试信息与 sanitizer，找出「为什么慢」用 profiler。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的调试信息由 `-C debuginfo` 控制（`-g` 是它的别名，取值为 0、1、2），`-C debug-assertions` 决定 `debug_assert!` 与整数溢出检查是否生效，`-C split-debuginfo` 决定调试信息是内联还是拆到 `.dSYM`/`.dwp`；Cargo 侧用 profile 里的 `debug` 与 `split-debuginfo` 字段配置，也可以用环境变量临时覆盖。sanitizer 与 Miri 都**只在 nightly 上可用**，这是 Rust 生态里最需要提前知道的一条硬约束。

```rust
// 实测（rustc 1.98 / Apple Silicon）
rustc -C debuginfo=2 opt.rs -o rs_dbg && stat -f%z rs_dbg       # 471992 字节
rustc -C debuginfo=0 opt.rs -o rs_nodbg && stat -f%z rs_nodbg   # 470664 字节（同为 opt-level 0）
rustc -g opt.rs -o rs_g                                          # -g 等价于 debuginfo=2
rustc -C debuginfo=2 -C split-debuginfo=unpacked -g opt.rs -o rs_split
# macOS 上调试信息会拆到 rs_split.dSYM 目录
rustc -C debug-assertions=on -O opt.rs -o rs_da   # release 下也保留 debug_assert 与溢出检查
RUST_BACKTRACE=1 ./rs_panic
# thread 'main' panicked at src/main.rs:2:5:
# attempt to add with overflow
# stack backtrace:
#    0: rust_begin_unwind

# Cargo：临时给 release 加调试信息
CARGO_PROFILE_RELEASE_DEBUG=true cargo build --release
CARGO_PROFILE_RELEASE_DEBUG=2 CARGO_PROFILE_RELEASE_SPLIT_DEBUGINFO=unpacked cargo build --release

# sanitizer：必须 nightly
rustc -Zsanitizer=address opt.rs -o /dev/null
# error: the option `Z` is only accepted on the nightly compiler
# help: consider switching to a nightly toolchain: `rustup default nightly`
rustup toolchain install nightly
RUSTFLAGS="-Zsanitizer=address" cargo +nightly build -Zbuild-std --target aarch64-apple-darwin
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly build -Zbuild-std
RUSTFLAGS="-Zsanitizer=leak"   cargo +nightly build -Zbuild-std
# -Zsanitizer=memory 支持 x86_64/aarch64 Linux 与 x86_64 FreeBSD，需要 nightly，且要求全部依赖都用 msan 编译

# Miri：解释执行 MIR 以检测 UB
cargo +nightly miri test
cargo miri --version
# error: the 'miri' component which provides the command 'cargo-miri' is not available
#   for the 'stable-...' toolchain        ← stable 上不可用，需 rustup +nightly component add miri

# 性能分析
rustc -Zself-profile -O opt.rs -o /dev/null     # nightly：编译期自身耗时
cargo install flamegraph && cargo flamegraph --release   # Linux 上基于 perf
perf record -g ./target/release/app && perf report
cargo bench
```

`debuginfo` 的三个取值差别在「有多少」：`0` 完全不带，`1` 只带行号与文件，`2` 带类型与变量信息（`gdb`/`lldb` 完整可用的最低要求）。⚠️ `debug-assertions` 与 `opt-level` 是**互相独立**的：release 构建默认 `debug-assertions = off`，于是整数溢出静默回绕，想在不牺牲速度的前提下保留检查就单独打开 `-C debug-assertions=on`。⚠️ sanitizer 的门槛要说清楚：`-Zsanitizer=address|thread|leak|memory` 全都要 nightly 工具链，而且必须用 `-Zbuild-std` 连标准库一起重编，否则只有你的 crate 被插桩，报告会不完整甚至互相冲突；`memory` sanitizer 官方只支持 x86_64/aarch64 Linux 与 x86_64 FreeBSD。Miri 是另一条路：它不运行机器码，而是按 MIR 语义解释执行，因此能抓到悬垂指针、未初始化读取、越界、别名违规等 UB，⚠️ 但它的速度极慢且不支持 `std` 里的系统调用，适合跑单元测试而不是跑完整程序；stable 工具链上没有 `miri` 组件，会直接报组件不可用。性能分析方面 `cargo flamegraph` 只是 `perf` 的封装，macOS 上没有 `perf`，要用 `cargo instruments` 或 Xcode 的 Instruments。

📘 [rustc 不稳定的 sanitizer 支持](https://doc.rust-lang.org/nightly/unstable-book/compiler-flags/sanitizer.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的调试信息由 `-g`（含 `-gline-tables-only` 的轻量档）控制，调试体验最好的是 `-g` 配 `-Onone`；sanitizer 通过 `-sanitize=address|thread|undefined` 开启，`swift test --sanitize=` 与 `swift run --sanitize=` 是 SwiftPM 的入口；性能分析则主要落在 Instruments 与 `lldb` 上。最该先知道的是：发布构建（`-O`）与调试构建（`-Onone -g`）必须分开，把 `-O` 的产物拿去做断点调试会看到变量被优化掉。

```swift
# 实测（Swift 6.4 / Apple Silicon）
swiftc -g opt.swift -o sw_g && stat -f%z sw_g          # 53656 字节
swiftc -g -Onone opt.swift -o sw_gd                    # 调试首选组合
swiftc -Onone opt.swift -o sw_Onone                    # 52584 字节，无调试信息
swiftc -gline-tables-only opt.swift -o sw_lt           # 只带行号表，体积更小
swiftc -g -Xlinker -dead_strip opt.swift -o sw_gds     # 调试信息 + 链接期删死代码

# sanitizer
swiftc -sanitize=address -g opt.swift -o sw_asan && echo asan-ok
swiftc -sanitize=thread  -g opt.swift -o sw_tsan && echo tsan-ok
swiftc -sanitize=undefined -g opt.swift -o sw_ubsan && echo ubsan-ok
swift test --sanitize=address
swift run --sanitize=thread
# ASAN_OPTIONS=detect_leaks=1 ./sw_asan        # 运行时环境变量

# 调试与分析
lldb ./sw_gd
# (lldb) breakpoint set --name main
# (lldb) run
swift build -c debug && .build/debug/app
swift test --enable-code-coverage
xcrun xctrace list templates                    # Instruments 模板
xcrun xctrace record --template "Time Profiler" --launch ./sw_O
swiftc -O -Xllvm -debug-only=inline opt.swift -o /dev/null 2>&1 | head   # LLVM 内部调试输出
```

`-Onone -g` 是断点与单步的唯一可靠组合：`-O` 会把变量放进寄存器、内联函数、重排语句，`lldb` 里看到的行号与变量值都可能与源码不一致。`-gline-tables-only` 是折中档，只保留「哪条机器指令对应哪一行」，足够看崩溃栈但看不到变量，适合「发布构建也要能定位崩溃」的场景。⚠️ Swift 的 sanitizer 有一个容易踩的坑：`-sanitize=` 会链接相应的运行库，因此产物必须在同一平台上运行，且 ThreadSanitizer 与其他 sanitizer 不能同时开启；另外 `swift test --sanitize=address` 需要整包重新构建，第一次会明显变慢。⚠️ 与 C 系不同，Swift 没有官方记忆化的「性能分析编译选项」，真正的剖析工具是 Instruments：`xcrun xctrace` 的 Time Profiler 模板给出调用树与火焰图，Allocations 模板给出内存分配生命周期；`-Xllvm -debug-only=` 之类的参数属于 LLVM 内部调试开关，输出非结构化且随时可能变更，只适合排查编译器本身的 bug。

📘 [Swift 官方文档 · Swift 编译器](https://www.swift.org/documentation/swift-compiler/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 默认就在二进制里嵌入 DWARF 调试信息，因此 `gdb`/`delve` 开箱可用；`-gcflags="all=-N -l"` 关掉优化与内联是为了让调试器看到真实的变量与调用栈；sanitizer 方面 Go 提供 `-race`（竞态检测）、`-msan`（内存检测）与 `-asan`（地址检测）三个内建选项，⚠️ 后两者都要求启用 cgo、各自只支持少数平台，`-msan` 还要求 Clang/LLVM 作为宿主 C 编译器（`-asan` 在 amd64/arm64 上接受 GCC 7 以上或 Clang/LLVM 9 以上）。性能分析是 Go 的强项：`runtime/pprof`、`net/http/pprof`、`go tool trace` 与 `benchstat` 都是官方工具。

```go
// 实测（Go 1.27.1 / darwin-arm64）
go build -o app .                                  # 默认带 DWARF
go build -gcflags="all=-N -l" -o app-debug .       # 关优化与内联，便于调试
go tool objdump -s "main.main" app | head -20      # 反汇编单个函数
dlv debug .                                        # Delve 调试器
dlv test ./... -- -test.run TestFoo

# 竞态与内存检测
go test -race ./...                                # 竞态检测，实测可正常运行
go run -race main.go
go build -msan -o app main.go
# -msan is not supported on darwin/arm64            ← 实测本机不支持
# 官方支持的 -msan 目标是 linux/amd64、linux/arm64、linux/loong64、freebsd/amd64，且要求 Clang/LLVM
go build -asan -o app-asan main.go                 # 地址检测，支持 linux/amd64、linux/arm64、linux/loong64
go test -gcflags="all=-N -l" -run TestFoo -v ./...

# 性能分析
go test -bench=. -benchmem -cpuprofile=cpu.out -memprofile=mem.out ./...
go tool pprof -http=:8080 cpu.out
go tool pprof -top cpu.out
go test -trace=trace.out ./... && go tool trace trace.out
go test -coverprofile=cover.out ./... && go tool cover -html=cover.out
go build -gcflags="-m=1" .                          # 逃逸分析与内联决策
go vet ./...
go test -bench=. -count=10 ./... > old.txt && benchstat old.txt new.txt
```

Go 的调试信息与优化是解耦的：`-ldflags="-s -w"` 会同时去掉符号表与 DWARF，这才是 `delve` 失效的原因，而 `-gcflags="all=-N -l"` 只是让代码保持「源码形状」，两者可以独立选择。⚠️ `all=` 前缀很重要，不加它只影响本次构建的直接包，标准库与其他依赖仍是优化过的，断点会跳来跳去。⚠️ `-race` 不是免费的：它会让内存占用与运行时间成倍上升，通常只在 CI 与预发布环境开启；它也只能发现**实际发生过**的数据竞争，不能证明没有竞争。⚠️ `-msan` 与 `-asan` 的限制更硬：`-msan` 官方只支持 linux/amd64、linux/arm64、linux/loong64 与 freebsd/amd64，`-asan` 官方只支持 linux/amd64、linux/arm64 与 linux/loong64；`-msan` 要求 Clang/LLVM 作为宿主 C 编译器，`-asan` 则接受 GCC 7 以上或 Clang/LLVM 9 以上（loong64 上要 Clang/LLVM 16 以上），两者还都要求启用 cgo 并把整个程序（包括依赖）一起插桩，所以在 macOS/ARM 上会直接报 `-msan is not supported on darwin/arm64`（实测如此）。性能分析链路上，`pprof` 负责 CPU/内存/阻塞/互斥，`go tool trace` 负责 goroutine 调度与 GC 时序，`benchstat` 负责把多轮 benchmark 的差异做成统计结论——三者配合才是完整的「为什么慢」答案。⚠️ 用 `benchstat` 前必须 `-count=10` 以上并固定 `GOMAXPROCS`，单次 benchmark 的噪声足以得出相反结论。

📘 [Go · 诊断工具](https://go.dev/doc/diagnostics)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有编译期调试信息开关，调试能力来自解释器自身的选项与标准库：`-X dev` 打开开发模式（相当于一批严格检查的组合），`faulthandler` 负责在段错误时打印 Python 栈，`pdb` 提供断点，`cProfile`/`timeit` 提供性能数据。要采样式分析则需第三方工具 `py-spy`（可在不修改代码、不重启进程的情况下附着）与 `scalene`（同时看 CPU、内存与 GPU）。最该先知道的是：**`-X dev` 是 Python 里最接近「调试构建」的开关**，它不改字节码但会打开额外的检查。

```python
# 实测（Python 3.14.7）
python3 -X dev -c "import sys; print('dev:', sys.flags.dev_mode)"
# dev: True
PYTHONDEVMODE=1 python3 main.py          # 与环境变量等价
python3 -X faulthandler main.py           # 段错误时打印 Python 栈
PYTHONFAULTHANDLER=1 python3 main.py
python3 -X dev -X faulthandler main.py
python3 -m pdb main.py                    # 标准库调试器
python3 -m trace --trace main.py          # 逐行跟踪（非常慢）
python3 -X importtime -c "import json"    # 导入耗时
# import time:       821 |       5542 | json

# 性能分析
python3 -m cProfile -s cumtime prof.py
#          200006 function calls in 0.017 seconds
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
python3 -m cProfile -o out.prof prof.py
python3 -c "import pstats; pstats.Stats('out.prof').sort_stats('cumtime').print_stats(5)"
python3 -m timeit -s "s=0" "sum(i*i for i in range(1000))"
# 10000 loops, best of 5: 28 usec per loop
pip install py-spy && py-spy top -- python3 main.py
py-spy record -o profile.svg -- python3 main.py
pip install scalene && scalene main.py
python3 -c "import sys; print(sys.getsizeof([]))"     # 对象大小
traceback.print_stack()
```

`-X dev` 会把「开发模式」需要的检查一次性打开：更严格的资源警告（未关闭的文件、未 await 的协程）、`PYTHONMALLOC=debug` 级别的内存检查、默认的 `faulthandler` 与 `-W default` 警告级别；它的作用是让错误更早暴露，代价是执行变慢，所以只在开发与 CI 上开。⚠️ Python 没有 `-g`，`-O`/`-OO` 只影响 assert 与 docstring（见「优化等级」一节），因此「调试构建」在 Python 里指的是安装一个 debug 版解释器（`--with-pydebug`），它会打开 `sys.gettotalrefcount()` 之类的额外能力，与 `-X dev` 不是一回事。性能分析的选择顺序建议是：先用 `timeit` 验证微观热点，再用 `cProfile` 拿到函数级归属，最后用 `py-spy` 或 `scalene` 看采样级真实分布。⚠️ `cProfile` 会给每个函数调用插桩，因此对「大量小函数调用」的代码会严重失真（被插桩开销放大），也可能掩盖真正的 I/O 等待；采样式工具不修改程序、能看 C 扩展与线程，但受采样频率限制，短函数可能整个被跳过。⚠️ `py-spy` 与 `scalene` 都是第三方工具，需自行安装，官方标准库只提供 `cProfile`、`profile`、`timeit`、`tracemalloc`。⚠️ Python 本身**没有** `-fsanitize=` 这类编译器级开关，排查解释器或 C 扩展的内存错误要靠 `--with-pydebug` 构建的解释器，或者把 ASan、Valgrind 接到扩展模块上。

📘 [Python · profile 与 pstats](https://docs.python.org/3/library/profile.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 自身没有调试信息或 sanitizer 的编译选项，调试与分析完全复用 JVM 的工具链：`assert` 是否生效取决于 JVM 的 `-ea`，崩溃定位靠 `-g` 级别的调试信息（`kotlinc` 生成的字节码默认带行号），性能分析靠 JFR、`jcmd` 与第三方 async-profiler。最该先知道的是：**Kotlin 的 `assert` 是运行期函数而不是编译期开关**，不加 `-ea` 它就什么都不做，而 `check`/`require` 无论何时都会抛异常。

```kotlin
kotlinc Main.kt -d app.jar
java -jar app.jar             # 未加 -ea：assert 被跳过
java -ea -jar app.jar         # 打开 JVM 断言，assert 才生效
java -ea -esa -jar app.jar    # -esa 打开系统类断言
# check/require 是库函数，始终抛 IllegalStateException/IllegalArgumentException
kotlinc Main.kt -Werror -d app.jar          # 警告升级为错误
kotlinc Main.kt -X -d /dev/null 2>&1 | head -20   # 列出全部高级 -X 选项

# JVM 侧调试信息与断言
javap -l -p -c MainKt.class | head -20      # 看 LineNumberTable 是否在
java -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -jar app.jar

# JFR：JDK 内置的低开销剖析
java -XX:StartFlightRecording=filename=app.jfr,settings=profile,dumponexit=true -jar app.jar
jfr print --events jdk.ExecutionSample app.jfr | head
jcmd <pid> JFR.start name=prof settings=profile filename=app.jfr
jcmd <pid> Thread.print
jcmd <pid> GC.heap_dump heap.hprof

# 第三方剖析器（采样式，开销低）
java -agentpath:/opt/async-profiler/lib/libasyncProfiler.so=start,event=cpu,file=cpu.html -jar app.jar
# 基准测试用 JMH，不要用 System.currentTimeMillis 手写循环
./gradlew jmh
```

Kotlin 的断言体系值得单独记牢：`assert(value)` 只有在 JVM 以 `-ea` 启动时才检查，因此它在生产环境是「零开销」的；`check(value)` 抛 `IllegalStateException`，`require(value)` 抛 `IllegalArgumentException`，两者永远生效，适合做参数与状态的强校验。⚠️ 这意味着「用 assert 做参数校验」是一类真实事故：本地跑没问题，生产上什么都没检查。字节码层面 `kotlinc` 默认生成 `LineNumberTable`，但**局部变量表**是否完整取决于编译选项与后端，若要用 `javap -l` 看到变量名，需要在 Gradle 里打开 `-java-parameters` 与调试信息级别。⚠️ JFR 是 JDK 自带、开销极低（默认配置约 1%）的剖析方案，适合长时间在生产上开着做「事后取证」；async-profiler 是第三方但能以极低开销给出火焰图，并支持 `event=alloc`、`event=lock` 等维度，两者互补。⚠️ 微基准一定要用 JMH：JVM 的预热、分层编译与死代码消除会让手写的 `currentTimeMillis` 循环得出完全错误的数字，JMH 的 `@Fork`、`@Warmup`、`@BenchmarkMode` 正是为消除这些偏差设计的。⚠️ Kotlin 自身也**没有** sanitizer 开关，内存安全由 JVM 保证；只有 JNI 与 `sun.misc.Unsafe` 那部分代码需要 C/C++ 侧的 ASan/TSan。

📘 [Java · jfr 工具（JDK 25）](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jfr.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的调试信息由 `javac -g` 家族控制（默认只带行号与源文件名，`-g` 才带局部变量），sanitizer 在 JVM 上没有直接对应物（内存错误基本不会发生，代之以 JFR 事件与堆转储），性能分析的官方答案是 JFR 与 `jcmd`，第三方答案是 async-profiler 与 JMH。最该先知道的是：`javac -g` 与运行速度无关，它只影响 `class` 文件大小与调试体验，因此可以在发布构建里保留。

```java
# 调试信息
javac Main.java                       # 默认：行号 + 源文件名
javac -g Main.java                    # 行号 + 源文件名 + 局部变量
javac -g:none Main.java               # 完全不带，class 文件最小
javac -g:lines,vars Main.java         # 只带行号与变量
javap -l -p Main.class | head -20     # 查看 LineNumberTable 与 LocalVariableTable
java -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints Main
# DebugNonSafepoints 是诊断级开关，需先解锁，作用是让采样剖析的栈更准

# JFR：低开销、可长期开启
java -XX:StartFlightRecording=filename=app.jfr,settings=profile,duration=60s,dumponexit=true Main
jfr print --events jdk.ExecutionSample,jdk.ObjectAllocationSample app.jfr | head
jfr summary app.jfr
jcmd <pid> JFR.start name=prof settings=profile filename=app.jfr
jcmd <pid> JFR.dump name=prof filename=/tmp/now.jfr
jcmd <pid> Thread.print
jcmd <pid> GC.heap_dump heap.hprof
java -Xlog:gc*:file=gc.log:time,uptime,level,tags Main

# 第三方：async-profiler 与 JMH
java -agentpath:/opt/async-profiler/lib/libasyncProfiler.so=start,event=cpu,file=cpu.html Main
java -agentpath:/opt/async-profiler/lib/libasyncProfiler.so=start,event=alloc,file=alloc.html Main
java -jar benchmarks.jar -f 1 -wi 5 -i 10      # JMH：fork、预热、迭代
java -XX:+PrintCompilation Main | head -20      # 观察方法被编译到第几层
```

`-g` 的四个取值影响的是 class 文件里的三张表：`LineNumberTable`（指令到源码行）、`LocalVariableTable`（局部变量名与作用域）、`SourceFile`（源文件名）。默认只带行号与文件名，所以 `javac` 不加 `-g` 时 `jdb` 里看不到局部变量名；`-g:none` 会把这三张表全部去掉，class 更小但崩溃栈只剩行号、无法在 IDE 里正确单步。⚠️ JFR 与 `jcmd` 是 JDK 内置的官方诊断组合：`jcmd <pid> JFR.start` 可以在不重启、不修改启动参数的情况下给正在跑的进程开启记录，这是排查生产问题最实用的能力；`jcmd Thread.print` 能一眼看出线程死锁，`GC.heap_dump` 给出可用 MAT 分析的堆快照。⚠️ JVM 里没有 AddressSanitizer 这样的工具，因为 Java 层面不存在指针运算与手动内存管理；真正需要 sanitizer 的是 JNI 或 `sun.misc.Unsafe` 的代码，那部分要靠 C/C++ 侧的工具链，并且要给 JVM 加 `-XX:+UnlockDiagnosticVMOptions` 才能让剖析器拿到准确栈。⚠️ 微基准必须用 JMH：JIT 的预热与分层编译会让「跑一次计时」的结果毫无意义，JMH 的 `@Warmup`/`@Fork`/`@BenchmarkMode` 就是为消除这类偏差而存在。

📘 [Java · jfr 工具（JDK 25）](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jfr.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的调试信息由 `-g` 家族控制，`-g3` 额外包含宏定义信息；sanitizer 由 LLVM 与 GCC 共同提供，`-fsanitize=address,undefined,thread,memory,leak` 是最常用的五个，外加 `-fsanitize=fuzzer` 做模糊测试；性能分析有 `perf`、`gprof`、VTune 与 `lldb`。最该先知道的是：sanitizer 与 `-fno-omit-frame-pointer` 是配套的，缺了后者火焰图会断链。

```cpp
// 实测（clang 21 / Apple Silicon）
clang++ -g bench.cpp -o g && stat -f%z g               # 33768 字节
clang++ -g3 bench.cpp -o g3 && stat -f%z g3            # 33768 字节（本例中与 -g 同大）
clang++ -ggdb bench.cpp -o gg                          # gdb 扩展（DWARF + GNU 扩展）
clang++ -g -gdwarf-5 bench.cpp -o gd5                  # 显式 DWARF 5
clang++ -g -gcodeview -c bench.cpp -o b.obj            # Windows/COFF 目标用 CodeView

# sanitizer（实测）
clang++ -fsanitize=address -g asan.cpp -o asan_app && ./asan_app
# ==27640==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000104
# WRITE of size 4 at 0x602000000104 thread T0
#     #0 0x... in main asan.cpp:3
clang++ -fsanitize=undefined -g -x c++ - -o ubsan_app
# runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
# SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior
clang++ -fsanitize=thread -g -c bench.cpp -o /dev/null && echo tsan-ok
clang++ -fsanitize=memory -g bench.cpp -o msan_app     # 需全部依赖也用 msan 编译
clang++ -fsanitize=leak -g bench.cpp -o lsan_app
clang++ -fsanitize=fuzzer,address -g fuzz.cpp -o fuzzer && ./fuzzer corpus/
clang++ -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all app.cpp

# 性能分析
clang++ -O2 -g -fno-omit-frame-pointer bench.cpp -o prof && perf record -g ./prof && perf report
clang++ -pg bench.cpp -o gp && ./gp && gprof -b ./gp gmon.out | head -20      # gprof（老派）
vtune -collect hotspots ./app                                                  # Intel VTune
valgrind --tool=memcheck --leak-check=full ./app                               # Linux
lldb ./g
```

`-g` 与 `-g3` 的差别在宏：`-g3` 会把 `#define` 也写进调试信息，于是 `lldb`/`gdb` 里能用 `macro expand` 看宏展开，代价是调试信息显著变大；`-ggdb` 是 GCC 的扩展档，clang 也接受，产出 GNU 扩展的 DWARF。⚠️ sanitizer 的取舍完全不同：AddressSanitizer 抓越界与释放后使用，UndefinedBehaviorSanitizer 抓有符号溢出、错位指针、非法转换，ThreadSanitizer 抓数据竞争，MemorySanitizer 抓未初始化读取，LeakSanitizer 抓泄漏；它们**不能随意组合**——ASan 与 TSan 互斥、MSan 要求整个程序（含 libc++）都插桩，正确做法是按问题类型挑一个，用 `-fno-sanitize-recover=all` 让它第一次出错就中止。⚠️ 生产环境通常只保留 `-fsanitize=undefined` 的轻量组合或干脆不开，因为 ASan 会让内存占用翻倍、速度下降 2 倍以上；模糊测试用 `-fsanitize=fuzzer` 配合 libFuzzer 的语料目录，是抓解析器类 bug 最有效的手段。性能分析上，`perf` 需要 `-fno-omit-frame-pointer`（否则栈回溯断裂）、`gprof` 需要 `-pg` 且对共享库与内联函数支持很差，现代场景优先用 `perf` 加火焰图或采样式 profiler。

📘 [Clang · AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

{{% /tab %}}

{{% tab header="C" %}}

C 的调试与分析选项与 C++ 完全同源：`-g` 家族控制调试信息，`-fsanitize=` 系列提供运行时检查，`perf`/`gprof`/`valgrind` 提供性能与内存分析。C 的最大不同在于未定义行为更容易发生，因此 UndefinedBehaviorSanitizer 与 Valgrind 在 C 项目里几乎是标配。最该先知道的是：C 的 sanitizer 效果最好在 `-O1` 配上 `-fno-omit-frame-pointer` 时使用，`-O0` 会掩盖部分只有优化后才暴露的问题。

```c
// 实测（clang 21 / Apple Silicon）
clang -g fib.c -o g
clang -g3 fib.c -o g3                     # 含宏信息
clang -g -gdwarf-5 fib.c -o gd5
clang -O2 -g -fno-omit-frame-pointer fib.c -o prof
clang -fsanitize=address,undefined -g -fno-sanitize-recover=all fib.c -o san && ./san
clang -fsanitize=thread -g -c fib.c -o t.o && echo tsan-ok
clang -fsanitize=memory -g fib.c -o m
clang -fsanitize=leak -g fib.c -o l
clang -fsanitize=fuzzer,address -g fuzz.c -o fuzz && ./fuzz corpus/
clang -O1 -g -fsanitize=undefined -fno-sanitize-recover=all -xc - -o ub <<'EOF'
#include <stdio.h>
int main(void){ int x = 2147483647; x += 1; printf("%d\n", x); return 0; }
EOF
./ub
# runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
# SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior

# 性能与内存分析
perf record -g ./prof && perf report                 # Linux
gcc -pg fib.c -o gp && ./gp && gprof -b ./gp gmon.out | head -20
valgrind --tool=memcheck --leak-check=full --track-origins=yes ./g
valgrind --tool=callgrind ./g && callgrind_annotate callgrind.out.*
gdb ./g
gdb -ex run -ex bt --args ./app
```

C 的调试信息格式主要由平台决定：ELF 平台用 DWARF（`-gdwarf-5` 可显式指定版本），Windows 的 COFF 用 CodeView（`-gcodeview`），而 `-g3` 的宏信息只有 DWARF 支持。⚠️ `-g` 与优化等级是独立的：`-O2 -g` 完全合法，也是「发布构建仍要能定位崩溃」的推荐组合，代价是行号会跳跃、变量可能被优化掉；要单步调试还是应该用 `-O0 -g` 或 `-Og -g`。⚠️ sanitizer 的选择原则与 C++ 相同但更重要：C 没有异常与 RAII，一处越界往往直接破坏相邻数据，ASan 能在写入瞬间定位，比事后用 `gdb` 看内存靠谱得多；`-fno-sanitize-recover=all` 让 UBSan 的第一次触碰就终止程序，避免「报了一堆警告但继续跑出错的结果」。⚠️ Valgrind 与 sanitizer 的定位不同：Valgrind 不需要重新编译、能检测未初始化读取与泄漏（配 `--track-origins=yes` 还能指出来源），但速度慢 10 到 50 倍且与 sanitizer 冲突（同一程序不能同时用），适合在单元测试级别跑；`perf` 与 `gprof` 里，`gprof` 需要 `-pg` 且对内联与共享库支持差，现代项目优先用 `perf` 加火焰图。

📘 [Clang · UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的调试开关集中在边界检查与警告级别上：`--check-bounds=yes|no|auto` 决定数组访问是否插入边界检查（默认 `auto`，即由 `@inbounds` 与优化器决定），`--depwarn=error|yes|no` 决定弃用警告是否致命；性能分析主要用 `@time`、`@allocated`、`@code_warntype` 与标准库 `Profile`。Julia 没有 sanitizer，因为内存安全由语言本身保证（越界只会是显式的 `BoundsError` 或被 `@inbounds` 关掉）。最该先知道的是：Julia 里性能问题的第一诊断工具是 `@code_warntype`，而不是 profiler。

```julia
julia --check-bounds=yes script.jl        # 强制保留边界检查
julia --check-bounds=no  script.jl        # 全部去掉（最危险，也最快）
julia -e 'println(Base.JLOptions().check_bounds)'   # 0=no 1=yes 2=auto
julia --depwarn=error script.jl           # 弃用警告变成错误，适合 CI
julia --warn-overwrite=yes script.jl
julia --track-allocation=user -e 'include("script.jl")'
# 之后用 Coverage.jl 的 analyze_malloc 查看每个源码行的分配（using Coverage; analyze_malloc(".")）

# 基准与观察
julia -e '@time sum(i*i for i in 1:10^7)'
#   0.012345 seconds (1 allocation: 16 bytes)
julia -e '@allocated sum(i*i for i in 1:10^7)'      # 看分配字节数，0 才是好代码
julia -e 'using InteractiveUtils; @code_warntype (x -> x + 1)(1)'
julia -e 'using InteractiveUtils; @code_native (x -> x + 1)(1)'
julia -e 'using InteractiveUtils; @code_llvm (x -> x + 1)(1)'
julia -e 'using BenchmarkTools; @benchmark sum(i*i for i in 1:10^6)'

# Profile：采样式剖析
julia -e 'using Profile; Profile.init(); @profile (() -> sum(i*i for i in 1:10^7))(); Profile.print()'
julia -e 'using Profile; @profile f(); Profile.print(format=:flat, sortedby=:count)'
julia -e 'using Profile; Profile.clear(); @profile f(); Profile.print(mincount=20)'
julia -e 'using Pkg; Pkg.add("PProf"); using Profile, PProf; @profile f(); pprof()'
```

Julia 的性能诊断有一条非常明确的顺序：先用 `@code_warntype` 确认**类型稳定**，再用 `@allocated` 确认热路径没有多余分配，最后才用 `Profile` 找热点；顺序颠倒会让你在优化的代码上浪费时间。类型不稳定是 Julia 特有的性能杀手——同一个函数在不同分支返回不同类型，会让编译器生成动态派发代码，速度差几十倍，而 `@code_warntype` 会用红色标出 `Any` 与 `Union`。⚠️ `--check-bounds=no` 是全局关掉边界检查，会让越界访问变成静默内存错误或段错误，正确做法是用局部的 `@inbounds` 并单独跑一遍 `--check-bounds=yes` 的测试；同理 `@simd` 与 `@fastmath` 也必须先验证数值正确性。⚠️ `@time` 的第一次调用包含编译时间，直接看第一个数字会严重高估，正确做法是先调用一次预热或用 `BenchmarkTools.@benchmark`（它会自动做多次采样与统计分析）；`Profile` 是采样式剖析，`Profile.print()` 的树状输出里时间归属要靠 `mincount` 过滤，配合 `PProf` 可以导出火焰图。

📘 [Julia · Profile 标准库](https://docs.julialang.org/en/v1/stdlib/Profile/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的调试信息由 `DebugType` 控制，默认值 `portable` 表示生成跨平台的便携式 PDB；`.NET` 没有 AddressSanitizer 这类工具（内存安全由运行时保证），诊断依靠一整套 `dotnet-*` 全局工具与 EventCounters，性能基准则必须用 BenchmarkDotNet。最该先知道的是：`portable` PDB 是 Debug 与 Release 的**共同默认值**，想彻底去掉调试信息必须显式写 `<DebugType>none</DebugType>`。

```csharp
// .csproj：调试信息的三档
// <DebugType>full</DebugType>      老式 Windows PDB
// <DebugType>pdbonly</DebugType>   C# 6.0 起与 full 无差别
// <DebugType>portable</DebugType>  默认，跨平台
// <DebugType>embedded</DebugType>  把 PDB 嵌进程序集
// <DebugType>none</DebugType>      完全不生成
dotnet build -c Debug                                         # 带完整 PDB
dotnet build -c Release -p:DebugType=embedded                  # 单文件交付时常用
dotnet build -c Release -p:DebugType=none -p:DebugSymbols=false
dotnet publish -c Release -p:DebugType=embedded -p:StackTraceSupport=true

// 运行时诊断（官方全局工具，先 dotnet tool install -g <name>）
dotnet-trace collect --process-id <pid> --profile cpu-sampling -o trace.nettrace
dotnet-trace convert trace.nettrace --format Speedscope         # 用 speedscope 看火焰图
dotnet-counters monitor --process-id <pid> --counters System.Runtime
dotnet-counters ps                                              # 列出可监视的进程
dotnet-dump collect -p <pid> -o core.dmp && dotnet-dump analyze core.dmp
dotnet-gcdump collect -p <pid> -o heap.gcdump
dotnet-monitor collect --urls http://localhost:52323            # 常驻诊断端点

// 代码内的诊断与基准
// using System.Diagnostics; var sw = Stopwatch.StartNew();
// [Conditional("DEBUG")] static void Log(string m) { ... }     ← DEBUG 宏决定是否调用
dotnet run -c Release --project benchmarks                      # BenchmarkDotNet 入口
DOTNET_EnableWriteXorExecute=0 dotnet app.dll                   # 排查特定崩溃时可试
```

`DebugType` 的取值在现代 .NET 上实际只有三档有意义：`portable`（默认，跨平台且体积小）、`embedded`（PDB 直接嵌进 `.dll`/`.exe`，适合单文件发布，代价是程序集变大）、`none`（完全不生成）。⚠️ `full` 与 `pdbonly` 是历史遗留，从 C# 6.0 起两者行为一致，新项目不要再用。`.NET` **没有**与 `-fsanitize=address` 对等的工具，因为托管堆不允许指针运算；真正需要 sanitizer 的是 `unsafe` 代码、P/Invoke 与 Native AOT 产出的原生部分，那些要用对应平台的 C 工具链。⚠️ `--self-contained` 与 `PublishSingleFile` 组合时 PDB 不会被自动打包，要在发布目录里单独保留 `.pdb` 才能让线上栈可读，或者打开 `embedded`。诊断工具的分工是：`dotnet-trace` 采 CPU 与运行时事件（可导出 speedscope 火焰图）、`dotnet-counters` 实时看 GC 与线程池指标、`dotnet-dump` 抓完整托管堆快照、`dotnet-gcdump` 抓轻量堆图、`dotnet-monitor` 把这几件事做成常驻端点。⚠️ 基准测试务必用 BenchmarkDotNet：它会做预热、多轮迭代、统计显著性检验并隔离不同配置，手写 `Stopwatch` 的测量在 JIT 分层编译下毫无意义。

📘 [.NET · dotnet-trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的调试开关主要是 `--enable-asserts`：`dart run` 与 `dart compile js` 都要显式加这个标志才会检查 `assert`，AOT 产物（`dart compile exe`）同样默认把断言编译掉，所以想要带断言的发布版本必须用 `dart compile exe --enable-asserts` 重新编译。分析能力则由 DevTools 提供——`dart run --observe` 打开 VM service，DevTools 通过它做 CPU 剖析、内存快照与时间线分析。最该先知道的是：**AOT 产物默认不含断言**，靠 `assert` 做的参数校验在生产环境会全部消失。

```dart
dart run --enable-asserts bin/myapp.dart      # 打开断言（不加则 assert 全被忽略）
dart --enable-asserts run bin/myapp.dart      # 等价写法
dart run --observe bin/myapp.dart             # 启动 VM service，输出可连接的 URI
dart run --pause-isolates-on-start bin/myapp.dart   # 启动即暂停，等调试器接入
dart devtools                                 # 本地启动 DevTools 页面
dart compile exe bin/myapp.dart -o build/myapp
dart compile exe --enable-asserts bin/myapp.dart -o build/myapp-debug   # AOT 里保留断言
dart compile aot-snapshot --target-sanitizer=asan bin/myapp.dart -o build/myapp-asan.aot
dartaotruntime build/myapp-asan.aot          # sanitizer 只能配 aot-snapshot，exe 不支持
dart analyze                                  # 静态分析
dart test --coverage=coverage                 # 覆盖率
dart pub global activate coverage && format_coverage --lcov --in=coverage --out=coverage.lcov
dart run --verbose bin/myapp.dart             # 详细日志
// 代码内：assert(x > 0, 'x 必须为正');  Debug将仅在开启断言时生效
// 生产校验请用显式 if + throw，而不是 assert
```

Dart 的断言语义与 Kotlin 的 `assert` 类似但更隐蔽：`dart run` 不加 `--enable-asserts` 就完全不检查断言，`dart compile exe` 默认也关闭且**不报错**，于是同一份代码在本地与生产的行为可能不同。⚠️ 因此官方风格指南明确反对用 `assert` 做输入校验：它只应用于「不可能发生」的内部不变量，用户输入与外部数据必须用 `ArgumentError` 之类的显式异常。⚠️ 分析工具方面，DevTools 的 CPU profiler 支持采样与「记录全部」两种模式，后者能看到每一次函数调用但开销极大；Memory 视图能抓堆快照并对比两个时点找出泄漏对象；Timeline 视图则把 `dart:developer` 的 `Timeline` 事件与框架事件串起来。⚠️ AOT 产物里 `--observe` 依旧可用（VM service 在 AOT 运行时同样存在），但部分调试能力（热重载、表达式求值）只在 JIT 下可用，这也是「开发用 JIT、发布用 AOT」这条分界线的另一半原因。⚠️ Dart 的 sanitizer 只存在于 AOT 快照这一条路径：`dart compile aot-snapshot --target-sanitizer=asan|msan|tsan`，可选值目前只在 Linux 的 x64/arm64 主机上齐全（riscv64 上没有 msan）；`dart compile exe` 明确不提供该选项，因为单文件可执行里的快照无法自符号化，插桩产物必须交给 `dartaotruntime` 运行。

📘 [Dart DevTools](https://dart.dev/tools/dart-devtools)

{{% /tab %}}

{{% tab header="R" %}}

R 的调试信息不存在「编译进产物」这一说（源码就是交付物），调试能力来自解释器选项与函数：`R -d gdb` 用外部调试器调试 C 层，`options(error=recover)` 与 `browser()` 处理 R 层，`--vanilla` 保证启动环境干净；性能分析由 `Rprof`、`Rprofmem` 与第三方的 `profvis`、`bench` 提供。最该先知道的是：**`Rprof` 现在是 utils 包里的函数**，且采样是「按时间间隔」而不是按调用次数，因此短函数可能被漏掉。

```r
# 实测（R 4.6.x）
Rscript -e 'print(R.version.string)'
R --vanilla -q -e 'options(error = recover)'          # 出错进入交互式恢复
Rscript -e 'options(error = function() { traceback(3); q(status = 1) })'
Rscript -e 'f <- function(x) if (x > 0) stop("boom"); tryCatch(f(1), error = function(e) print(conditionMessage(e)))'
Rscript -e 'browser()'                                # 断点（交互式终端才有意义）
Rscript -e 'debug(f); f(1); undebug(f)'               # 单步调试函数
Rscript -e 'traceback()'                              # 要配合 options(error=...) 使用
R -d gdb                                               # 用 gdb 调试 R 本体与 C 代码
R --debugger=valgrind                                  # 用 valgrind 检查内存
Rscript -e 'print(capabilities("profmem"))'            # 编译期是否开启内存剖析

# 性能分析
Rscript -e 'Rprof("prof.out", interval = 0.01, memory.profiling = TRUE);
            f(); Rprof(NULL); print(summaryRprof("prof.out")$by.total[1:5, ])'
Rscript -e 'Rprofmem("mem.out"); f(); Rprofmem(NULL); print(readLines("mem.out", n = 10))'
R CMD Rprof prof.out                                   # 命令行汇总
Rscript -e 'print(system.time(f()))'                   # 最简单的计时
install.packages(c("profvis", "bench"))
Rscript -e 'library(profvis); profvis(f())'            # 交互式火焰图
Rscript -e 'library(bench); print(bench::mark(f(), g()))'
R CMD check --as-cran mypkg                            # 静态检查 + 示例运行
```

R 的调试分两层：R 层的 `browser()`/`debug()`/`recover` 是解释器级工具，C 层（包里的 `.Call` 代码与 R 本体）要靠 `R -d gdb` 或 `R --debugger=valgrind` 交给外部调试器，因为 R 进程本身就是被调试对象。⚠️ `options(error=recover)` 只在交互式会话里有用，脚本模式（`Rscript`）下不会进入恢复浏览器，脚本里正确的做法是 `options(error=function() { traceback(3); q(status=1) })` 加非零退出码，让 CI 能识别失败。⚠️ `Rprof` 的采样是按时间间隔（`interval` 默认 0.02 秒），因此它给出的是**统计近似**：执行时间极短的热点可能完全不被采到，长时间阻塞在 I/O 的函数也会被记成「未知」；`memory.profiling=TRUE` 能同时记录内存，但需要 R 编译时开启 `--enable-memory-profiling`，否则 `Rprofmem` 不可用（用 `capabilities("profmem")` 先确认）。⚠️ `profvis` 与 `bench` 都是第三方包，前者把 `Rprof` 的结果渲染成火焰图，后者用统计方法比较多段表达式的性能；R 本身没有 sanitizer，检查 C 代码只能靠 `valgrind` 与 `R CMD check` 的 `--use-valgrind`。

📘 [R · Rprof](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/Rprof.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 把调试信息与安全检查都放进了构建模式里：`Debug` 模式默认开启全部安全检查（整数溢出、越界、空指针、非法联合访问）并保留调试符号，`ReleaseSafe` 保留安全检查去掉符号，`ReleaseFast`/`ReleaseSmall` 两者都关。因此 Zig 没有独立的 `-fsanitize=` 家族，只有面向 C 代码的 `-fsanitize-c`。最该先知道的是：**Zig 的「sanitizer」是默认开启的**，Debug 构建下越界与溢出的报错就是安全检查在工作。

```zig
zig build-exe main.zig -O Debug              # 默认：安全检查全开 + 调试符号
zig build-exe main.zig -O Debug -fno-strip   # 显式保留符号
zig build-exe main.zig -O ReleaseSafe        # 保留安全检查，去掉调试符号
zig build-exe main.zig -O ReleaseFast -fsanitize-c       # 编译其中的 C 代码时做 UBSan
zig build-exe main.zig -O ReleaseFast -fsanitize-c=trap  # 0.15 新增：越界直接 trap
zig build-exe main.zig -O Debug --verbose-air            # 打印 AIR（编译前端 IR）
zig build-exe main.zig -O Debug -femit-asm=out.s         # 输出汇编
zig build-exe main.zig -O Debug -femit-llvm-ir=out.ll
zig build test --summary all                     # 跑测试并给摘要（build 侧的等级走 -Doptimize，默认 Debug）
zig test main.zig -O Debug
// 代码内调试输出
// try std.testing.expectEqual(@as(i32, 3), x);
// std.debug.print("x = {d}\n", .{x});
// @import("builtin").mode == .Debug   ← 按构建模式分支
```

Zig 的安全检查是语言语义的一部分：`Debug` 与 `ReleaseSafe` 下，整数溢出、数组越界、空指针解引用、非法类型转换都会 panic 并打印源码位置，这正是 Zig「不依赖外部 sanitizer」的原因。⚠️ 这意味着性能与安全在 Zig 里是一个**编译期就定死的二选一**：`ReleaseFast` 下同样的代码不再检查，出错就是 UB，因此发布前必须在 `ReleaseSafe` 下跑完整测试，官方也把 `ReleaseSafe` 列为服务端的推荐模式。⚠️ `-fsanitize-c` 只作用于链接进来的 C 代码（Zig 本身不需要它），0.15 起新增了 `=trap` 与 `=full` 两个取值，单独的 `-fsanitize-c` 等价于 `full`。调试内存问题的另一条路是分配器：`std.heap.DebugAllocator`（0.14 起由 `GeneralPurposeAllocator` 改名而来）在 Debug 与 ReleaseSafe 下会做泄漏检测、使用后释放检测与双重释放检测，`std.heap.page_allocator` 则没有任何检测；⚠️ 因此「换分配器」本身就是 Zig 里常用的排查手段。`--verbose-air` 打印的是编译器前端的 AIR，用它能看到安全检查被插在哪里、优化前后有多少指令被消掉，是排查「为什么这段代码没被优化」的第一手材料。

📘 [Zig 语言参考 · Debug 模式](https://ziglang.org/documentation/0.15.1/#Debug)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的调试能力来自标准库 `debug`：`debug.sethook` 安装钩子做单步或按指令计数跟踪，`debug.getinfo` 取当前函数与行号，`debug.traceback` 生成栈回溯；静态检查则用 `luac -l` 反汇编字节码，`luac -s` 反过来剥掉调试信息。Lua 没有 sanitizer，C 模块的问题要靠 C 侧工具链。最该先知道的是：调试信息是**可选**的，剥离之后所有回溯与 `debug.getinfo` 都会退化。

```lua
lua -e 'debug.sethook(function(ev, line) print(ev, line, debug.traceback("", 2)) end, "", 1000)'
# 每执行 1000 条指令打印一次当前位置（count 钩子）
lua -e 'local f = assert(loadfile("main.lua")); debug.sethook(function(ev) print(ev, debug.getinfo(2, "Sl").currentline) end, "l")'
# "l" 钩子：每进入新行都触发，用来做逐行跟踪
lua -e 'print(debug.traceback("trace:"))'
lua -e 'local i = debug.getinfo(1); print(i.currentline, i.short_src, i.what)'
lua -e 'print(pcall(function() error("boom") end))'
lua -e 'print(xpcall(function() error({code = 42}) end, function(e) return e.code end))'
luac -l main.luac              # 反汇编：看每条指令与行号
luac -l -l main.luac           # 附带常量表与局部变量表
luac -p main.lua               # 只做语法检查
luac -s -o main.strip.luac main.lua   # 剥掉调试信息（之后回溯只剩函数名）
luajit -jv script.lua          # LuaJIT：查看哪些轨迹被编译/中止
luajit -jdump script.lua       # LuaJIT：导出生成的机器码
```

`debug.sethook` 的钩子有三类事件：`"c"`（每次函数调用）、`"r"`（每次返回）、`"l"`（每执行到新的一行）；`mask` 里带 `"l"` 时逐行跟踪，不带时按 `count` 条指令触发，⚠️ 无论哪种都会让程序慢上几十倍，只适合小范围排查。`debug.getinfo` 的 `what` 字段区分 `"Lua"`、`"C"`、`"main"`，配合 `short_src` 与 `currentline` 就能自己实现一个错误报告器；这也是很多 Lua 框架实现「格式化堆栈」的方式。⚠️ 剥离调试信息（`luac -s`）与调试能力是直接对立的：剥了之后 `debug.getinfo` 拿不到行号、错误回溯只剩函数名，所以生产环境要么保留行号信息、要么把源码版本与二进制版本一一对应地归档。⚠️ Lua 没有内存 sanitizer，因为 Lua 层的错误（`nil` 索引、错误的参数类型）都会以明确的 `error` 抛出；真正需要 sanitizer 的是 C 模块里的指针与 `lua_State` 栈操作，排查方式与普通 C 程序相同（`valgrind`、ASan），另外启用 `LUA_USE_APICHECK` 重新编译可以让 Lua 检查 C API 的参数合法性。⚠️ LuaJIT 的 `-jv` 与 `-jdump` 是完全独立的一套诊断接口，只在 LuaJIT 上存在。

📘 [Lua 5.5 参考手册 · debug 库](https://www.lua.org/manual/5.5/manual.html#6.10)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的「调试开关」全部围绕 source map：`sourceMap` 让 `.js` 与 `.ts` 的对应关系以 `.js.map` 形式单独输出，`inlineSourceMap` 与 `inlineSources` 把它内联进产物，`declarationMap` 则让跳转到 `.d.ts` 时能回到 `.ts`。分析方面 TypeScript 7 提供 `--diagnostics`、`--extendedDiagnostics` 与 `--generateTrace` 观察编译各阶段耗时。最该先知道的是：**source map 只对「从源码到产物」的映射负责**，运行时还得让宿主显式支持它（Node 要用 `--enable-source-maps`）。

```typescript
npx tsc --sourceMap                        // 生成 .js.map
npx tsc --inlineSourceMap                  // 映射内联进 .js（部署时少一个文件）
npx tsc --inlineSources                    // 把 .ts 原文也塞进映射
npx tsc --declarationMap                   // .d.ts 也能跳回 .ts
npx tsc --noEmit                           // 只检查，不产出
npx tsc --pretty false                     // 让错误信息便于机器解析
npx tsc --diagnostics                      // 输出编译各阶段耗时统计
npx tsc --extendedDiagnostics              // 更细：绑定、检查、emit 分别多久
npx tsc --generateTrace trace              // 生成可被 Chrome tracing 打开的追踪
npx tsc --listFiles --listEmittedFiles     // 列出参与编译与产出的文件
node --enable-source-maps dist/main.js     // Node 侧按 source map 还原堆栈
node --inspect-brk dist/main.js            // 断点调试产物
// 第三方：调试器直接消费 source map，无需额外开关
// VS Code 的 launch.json 里 "sourceMaps": true 即可在 .ts 上断点
du -sh dist && ls dist | head
```

`sourceMap` 与 `inlineSourceMap` 是二选一：前者产出独立的 `.map` 文件，适合把映射上传到错误监控平台（不随产物公开），后者把 base64 映射塞进 `.js` 末尾，部署更简单但产物更大且映射对用户可见。`inlineSources` 会把 `.ts` 原文也写进映射，⚠️ 这意味着源码等于随产物一起发布，闭源项目不要打开。⚠️ 一个常见误解是「配了 sourceMap 就能在 Node 里看到 TS 行号」：Node 需要 `--enable-source-maps` 才在未捕获异常里还原原始位置，否则堆栈里仍是编译后 `.js` 的行号与列号。TypeScript 7 的原生编译器在诊断输出上也做了改进：`--diagnostics` 与 `--extendedDiagnostics` 给出的是真实阶段耗时，`--generateTrace` 产出的追踪文件可以在浏览器的 `chrome://tracing` 里打开，用来看「时间花在类型检查还是 emit 还是项目图构建」；配合新增的 `--checkers`/`--builders`/`--singleThreaded`，大仓库的构建调优有了可观测的抓手。⚠️ source map 只解决「错误定位」，不解决「性能分析」：要剖析 TypeScript 产物，仍应按 JavaScript 的方式用 `--cpu-prof` 或采样 profiler，并在报告里对照 source map 还原到 `.ts`。⚠️ TypeScript 与 JavaScript 一样**没有** sanitizer，运行时诊断只能靠宿主提供的开关（Node 的 `--cpu-prof`、`--heap-prof`、`--trace-deopt`、`--jitless`），原生插件的内存错误要用 C/C++ 工具链。

📘 [TypeScript · sourceMap 选项](https://www.typescriptlang.org/tsconfig/#sourceMap)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的调试与分析接口由 Node 提供：`--inspect` 与 `--inspect-brk` 打开 Inspector 协议供 Chrome DevTools 或 VS Code 连接，`--enable-source-maps` 让堆栈按映射还原，`--cpu-prof` 与 `--prof` 采 CPU，`--heap-prof` 采堆，`--trace-deopt` 与 `--trace-gc` 打印运行时的内部决策。JavaScript 没有 sanitizer，但有 `--jitless` 与 `--stack-trace-limit` 之类的运行时开关辅助定位。最该先知道的是：`--trace-deopt` 往往比任何采样式 profiler 都更能解释「为什么这个函数慢」。

```javascript
node main.js
node --inspect main.js                 # 打开 Inspector，DevTools 连接 9229 端口
node --inspect-brk main.js             # 第一行就停下，等调试器接入
node --inspect=0.0.0.0:9230 main.js    # 指定地址与端口
node --enable-source-maps dist/bundle.js   # 按 source map 还原堆栈
node --stack-trace-limit=50 -e 'throw new Error("x")' | head -20

# CPU / 内存剖析
node --cpu-prof --cpu-prof-dir=./prof --cpu-prof-interval=500 main.js && ls prof/
node --prof main.js && node --prof-process isolate-*.log | head -40
node --heap-prof --heap-prof-dir=./prof main.js
node --trace-deopt main.js | head -20       # 找出反复反优化的函数
node --trace-opt main.js | head -20
node --trace-gc main.js | head -20
node --report-on-fatalerror main.js         # 致命错误时自动生成诊断报告
node --diagnostic-dir=./diag --report-directory=./diag main.js
node --max-old-space-size=512 main.js
npx clinic doctor -- node main.js           # 第三方一站式诊断
node -e 'console.log(process.memoryUsage())'
```

Node 的调试协议是 Inspector 协议，`--inspect` 只打开端口不做任何输出，真正好用的是把 VS Code 的 `attach` 配置或 Chrome 的 `chrome://inspect` 连上去——这样能得到断点、单步、调用栈与实时表达式求值，而这套体验与浏览器里完全一致。⚠️ `--inspect-brk` 与 `--inspect` 的区别很适合用来调试「启动阶段就崩」的问题：前者在第一行暂停，让你有时间在模块加载前设断点。剖析方面有两条完全不同的路线：`--prof` 产生 V8 的底层日志，需要用 `node --prof-process` 解析成可读表格（包含 C++ 与 JS 两侧的归属），适合深挖；`--cpu-prof` 直接产生标准的 `.cpuprofile`，可以拖进 Chrome DevTools 的 Performance 面板看火焰图，适合日常。⚠️ `--trace-deopt` 是 V8 独有的诊断能力：JIT 的投机优化一旦被打破就会回退到解释器，一个反复 deopt 的热函数能吃掉一半性能，而采样 profiler 只会显示它「很慢」却不会告诉你原因。⚠️ JavaScript 层面没有 sanitizer，`--jitless` 关掉 JIT 后可以让某些与优化相关的诡异问题消失，从而缩小排查范围；真正的内存错误只会来自原生插件，那部分要用 C/C++ 的工具链。⚠️ 与本机的版本对照：本机是 Node 24，而基线按 Node 26 书写，上面用到的 `--cpu-prof`、`--prof`、`--heap-prof`、`--trace-deopt`、`--enable-source-maps`、`--report-on-fatalerror` 在两者上均存在。

📘 [Node.js · 命令行选项](https://nodejs.org/api/cli.html)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的调试信息不是编译选项，而是**扩展**：`xdebug` 提供断点、单步、性能剖析与覆盖率，`pcov` 提供轻量覆盖率，`tideways`/`blackfire` 提供生产级采样剖析；错误可见性由 `error_reporting` 与 `display_errors` 控制，`zend.assertions` 决定 `assert()` 是否被编译掉。最该先知道的是：**xdebug 会显著拖慢执行**，生产环境不应加载它，只在开发与 CI 上开。

```php
php -l main.php                                // 语法检查
php -d error_reporting=E_ALL -d display_errors=1 main.php
php -d zend.assertions=1 -d assert.exception=1 main.php   // 断言生效并抛异常
php -d zend.assertions=-1 -d error_reporting=0 main.php   // 生产：断言被编译掉
php -i | grep -E "zend.assertions|error_reporting|assert.exception"

// xdebug（先安装扩展并在 php.ini 中设置模式）
php -d xdebug.mode=develop,debug -d xdebug.start_with_request=yes main.php
php -d xdebug.mode=coverage -d pcov.enabled=1 -d pcov.directory=src vendor/bin/phpunit
php -d xdebug.mode=profile -d xdebug.output_dir=/tmp main.php   // 产出 cachegrind 文件
php -m | grep -i -E "xdebug|pcov"
php -r 'var_dump(function_exists("xdebug_info"), extension_loaded("pcov"));'
XDEBUG_MODE=coverage vendor/bin/phpunit --coverage-text     // 用环境变量切换模式

// 手工计时与内存
php -r '$t = hrtime(true); $s = 0; for ($i = 0; $i < 1e6; $i++) { $s += $i; }
        printf("耗时 %.3f ms\n", (hrtime(true) - $t) / 1e6);'
php -r 'echo memory_get_peak_usage(true), " bytes\n";'
php -r 'echo ini_get("opcache.jit"), "\n";'
php --ri xdebug | head -20                      // 查看扩展配置
```

`zend.assertions` 有三个取值：`1` 完全启用、`0` 生成但不执行、`-1` 在编译期就把 `assert()` 整段删掉，所以生产用 `-1` 是零开销的，⚠️ 但这也意味着断言里的**副作用代码会一并消失**（`assert($x = f())` 这类写法在生产上根本不会执行）。xdebug 的模式是分场景的：`develop` 增强 `var_dump` 与错误页、`debug` 打开远程调试协议（配合 IDE 的 DBGp 客户端）、`coverage` 生成覆盖率、`profile` 输出 cachegrind 文件（用 KCachegrind 或 QCachegrind 查看）、`trace` 记录每次函数调用的参数与耗时；⚠️ 这些模式的开销从几十个百分点到数十倍不等，且**同时只应开一个**，用 `XDEBUG_MODE` 环境变量切换比反复改 `php.ini` 更实际。⚠️ PHP 没有 sanitizer，因为请求结束即释放全部内存，悬垂指针类问题主要出在扩展与 FFI 层，要用 C 侧工具链；另外 `--enable-debug` 编译的 PHP 会打开额外的运行时检查与内存分配诊断，是排查扩展崩溃的常用手段。⚠️ 生产采样剖析应当选 tideways 或 blackfire 这类为常驻场景设计的工具，并把 `xdebug` 完全排除在镜像之外。

📘 [Xdebug 文档](https://xdebug.org/docs/)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的调试手段分三层：`-w` 与 `--debug` 打开解释器级警告与调试输出，`debug.gem`（Ruby 3.1 起随语言分发）提供断点与单步，`stackprof`/`ruby-prof`/`benchmark-ips` 提供性能剖析与基准；运行期还能用 `--yjit-stats` 看 JIT 效率、用 `GC.stat` 看内存。Ruby 没有 sanitizer，C 扩展的问题要用 C 侧工具链。最该先知道的是：**`--debug` 会输出大量内部日志**，它和 `-w` 不是一回事，后者只是打开警告。

```ruby
ruby -w script.rb                 # 打开警告（含未使用变量、方法重定义）
ruby -W2 script.rb                # 更严格：-W0 关、-W1 默认、-W2 详细
ruby --debug script.rb            # 打印解释器内部调试输出（实测会输出 LoadError 等事件）
ruby -e 'begin; 1/0; rescue => e; puts e.class; puts e.backtrace.first(3); end'
# ZeroDivisionError
# -e:1:in '<main>'
ruby -e 'puts caller.first(3)'
ruby -e 'puts Thread.current.backtrace'

// debug.gem（随 Ruby 分发，也可 gem install debug）
// ruby -rdebug/start script.rb     → 在脚本第一行停住
// (rdbg) break / step / next / continue / info locals
gem list debug
ruby -rdebug -e 'puts "breakpoint api: #{defined?(DEBUGGER__)}"'

// 性能分析
ruby --yjit --yjit-stats -e 's=0; 1_000_000.times{|i| s+=i*i}; puts s' 2>&1 | tail -6
# yjit_insns_count:         11,999,652
# total_exit_count:            999,971
# code_region_size:             16,384
ruby -e 'GC.stat.select { |k,_| k.to_s.start_with?("heap") }.each { |k,v| puts "#{k}=#{v}" }'
ruby -robjspace -e 'ObjectSpace.trace_object_allocations { }; puts ObjectSpace.count_objects[:TOTAL]'
ruby -rbenchmark -e 'puts Benchmark.measure { 100_000.times { |i| i*i } }'
#   0.002078   0.000010   0.002088 (  0.002086)
gem install stackprof && ruby -rstackprof -e 'StackProf.run(mode: :cpu, out: "tmp/stackprof.dump") { }'
gem install ruby-prof && ruby -rruby-prof -e 'RubyProf.profile { }; puts "done"'
gem install benchmark-ips && ruby -rbenchmark-ips -e 'Benchmark.ips { |x| x.report("add") { 1+1 } }'
```

`-w`/`-W` 控制的是警告级别，`--debug` 打开的是解释器自身的调试输出（会打印 `require` 失败、常量查找等内部事件），两者用途不同；⚠️ `--debug` 的输出量很大且格式不稳定，只适合排查「为什么某个 `require` 没生效」这类问题。`debug.gem` 是官方维护的调试器，支持断点、单步、`catch` 异常、以及 `debug` 方法直接进入会话，它与 `byebug` 这类老牌 gem 的关键区别是**随 Ruby 分发且与新版语言特性同步**；⚠️ 注意 `require "debug"` 与 `ruby -rdebug` 会与 Ruby 3.1 之前的标准库 `lib/debug.rb` 重名，3.1 起该标准库已被 `debug.gem` 取代。运行期分析上，YJIT 的 `--yjit-stats` 给出的是 JIT 层面的读数（生成指令数、退出次数、代码区大小），⚠️ `ratio_in_yjit` 在 Ruby 4.0 默认构建里不再可用，需要 `configure --enable-yjit=stats`；ZJIT 目前还没有同等成熟的统计接口。内存方面 `GC.stat` 给出各代堆的大小与晋升次数，`ObjectSpace` 能按类型统计对象数量并追踪分配来源，是找内存泄漏的主要手段。⚠️ `stackprof`、`ruby-prof`、`benchmark-ips` 都是第三方 gem，官方只提供 `benchmark` 标准库的 `Benchmark.measure`/`bm`；其中 `benchmark-ips` 会给出「每秒迭代次数」并做统计置信区间，比单次 `measure` 可靠得多。

📘 [Ruby · GC 模块](https://docs.ruby-lang.org/en/master/GC.html)

{{% /tab %}}

{{< /tabpane >}}
