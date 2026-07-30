+++
title = "47-webassembly"
date = 2026-07-28T14:49:00+08:00
weight = 470
type = "docs"
description = "面向 Go 用户讲清 Rust WASM 目标、bindgen、体积优化、WASI 与浏览器/wasmtime 边界"
isCJKLanguage = true
draft = false

+++

# WebAssembly (WebAssembly)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否想知道：为什么大家爱用 Rust 写 WASM，而不是只在浏览器里写 JS？
- 你是否分不清 `wasm32-unknown-unknown` 和 WASI、浏览器跑和 wasmtime 跑？
- 你是否想走通：`rustup target add` → `cargo build --target` →（可选）wasm-bindgen / wasm-pack？
- 你是否纠结体积优化、`panic=abort`、`no_std`、异步与线程在 WASM 里的限制？
- 你是否想对照 Go 的 `GOOS=js GOARCH=wasm`，并判断什么时候别用 WASM？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| **WASM** | WebAssembly | 可移植字节码 | 浏览器/嵌入运行时都能跑的低级二进制格式 | `GOARCH=wasm` |
| target | — | 编译目标三元组 | 告诉 rustc 为谁生成机器码/字节码 | `GOOS`/`GOARCH` |
| `wasm32-unknown-unknown` | — | 浏览器向 WASM 目标 | 无 OS 假设，常配合 JS glue | `js/wasm` |
| **WASI** | WebAssembly System Interface | WASM 系统接口 | 给 WASM 提供类 POSIX 能力的标准接口 | 更接近“带 syscall 的 WASM” |
| **wasm-bindgen** | — | JS 绑定生成器 | 生成 Rust↔JS 的胶水与类型桥 | `syscall/js` |
| **wasm-pack** | — | WASM 打包工具 | 封装 build + bindgen + npm 包布局 | 手写 wasm + JS 胶水 |
| glue | — | 胶水代码 | JS 侧加载/调用 WASM 的辅助代码 | `wasm_exec.js` |
| **wasmtime** | — | WASM 运行时 | 在本地/服务端嵌入执行 WASM | 非浏览器宿主 |
| LTO | Link-Time Optimization | 链接时优化 | 链接阶段再优化，常减小体积 | `-ldflags`/编译器优化类比 |
| `wasm-opt` | — | Binaryen 优化器 | 对 `.wasm` 再压一刀 | 体积优化工具 |
| `panic=abort` | — | panic 即中止 | 不展开 unwinding，减小体积 | 类似少用 panic 栈展开 |
| `no_std` | — | 不用标准库 | 只靠 `core`/`alloc`，适合极致裁剪 | 极简/嵌入式思路 |
| host | — | 宿主 | 加载并调用 WASM 的环境（浏览器/引擎） | 同概念 |
| ABI | Application Binary Interface | 应用二进制接口 | 跨语言调用约定；WASM 导入导出形状 | `syscall/js` 约定 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6) |
| `common` | [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `occasional` | [Q11](#q11) |
| `advanced` | — |

---

## Q1. 为什么 Rust 常被拿来写 WASM？ {#q1}
**Tags:** `hot` `beginner` `WASM` `why-rust`
**适用版本:** 生态层面；Rust 1.x stable 均可编译 wasm 目标

**一句话答案：**
Rust 无 GC 停顿、能精细控内存与体积、工具链（rustc → WASM）成熟，又有 **wasm-bindgen** / **wasm-pack** 连 JS——适合把计算热点、编解码、校验逻辑塞进浏览器或嵌入运行时，同时尽量保持小而快。

**解答：**
常被点名的理由：

| 诉求 | Rust 为什么合拍 |
|------|-----------------|
| 体积 | 可 `opt-level=z`、LTO、`wasm-opt`（见 [Q6](#q6)） |
| 性能 | 贴近原生的控制流与数据布局 |
| 安全默认 | 所有权/借用减少一类内存错误带进 WASM |
| 与 JS 协作 | bindgen 生成类型化胶水 |
| 可移植 | 同一套逻辑可瞄准浏览器或 WASI 宿主 |

典型分工（不是替代前端框架）：

```text
UI / DOM / 产品逻辑  → JS/TS（或框架）
重计算 / 解析 / 加密热点 → Rust → .wasm
```

「❌ 错误预期」——用 Rust WASM 重写整个 SPA 只为“更潮”：胶水与调试成本常高于收益（见 [Q12](#q12)）。

**Go 对比：**
- **Go 怎么做**：也能 `GOOS=js GOARCH=wasm`，但运行时/GC 体积通常更大，和 JS 互操作靠 `syscall/js`。
- **Rust 为什么不同**：默认更易往“小二进制、细控内存”方向拧。
- **Go 程序员易踩的坑**：把 Go wasm 的“能跑”直接当成和 Rust 一样的体积画像——量级常不同。

**记忆点：**
- Rust WASM = 热点与可移植计算，不是默认前端全家桶。
- 优势在体积/控制/bindgen 生态。

---

## Q2. `wasm32-unknown-unknown` 和 WASI 差在哪？ {#q2}
**Tags:** `hot` `target` `WASI` `wasm32`
**适用版本:** rustup 目标；WASI preview 演进中，以当前 rustup 名为准

**一句话答案：**
**`wasm32-unknown-unknown`**：面向“无 OS”的 WASM，浏览器里通常靠 JS 提供能力（DOM、fetch）。**WASI**（WebAssembly System Interface）：给 WASM 一套系统接口（文件、时钟、参数等），适合在 **wasmtime** 等宿主里跑非浏览器程序。二者目标三元组与能力模型都不同。

**解答：**
对照：

```text
wasm32-unknown-unknown
  ├─ 常见宿主：浏览器（+ JS glue）
  ├─ 系统调用：基本没有；I/O 经导入的 JS 函数
  └─ 典型工具：wasm-bindgen / wasm-pack

WASI（如 wasm32-wasip1 等，以 rustup 列表为准）
  ├─ 常见宿主：wasmtime、WasmEdge…
  ├─ 系统调用：经 WASI 能力（可裁剪权限）
  └─ 更像“可移植的命令行/服务端插件”
```

怎么记：
- 要进 **网页** 调 DOM/JS → `unknown-unknown` + bindgen。
- 要在 **本地/服务器** 当沙箱插件、读受限文件 → WASI + wasmtime 一类。

列出本机目标（命令）：

```bash
rustup target list | findstr wasm
# Unix 可用: rustup target list | grep wasm
```

**Go 对比：**
- **Go 怎么做**：主推 `js/wasm` 浏览器路径；WASI 支持另线演进，和 Rust 目标矩阵不完全一一对应。
- **Rust 为什么不同**：rustup 上浏览器目标与 WASI 目标分得很清。
- **Go 程序员易踩的坑**：以为任意 `.wasm` 都能 `node`/`浏览器`/`wasmtime` 直接通吃——宿主与导入集必须匹配。

**记忆点：**
- unknown-unknown ≈ 浏览器 + JS。
- WASI ≈ 系统接口 + 非浏览器宿主。

---

## Q3. 最小流程：rustup target 和 cargo build --target？ {#q3}
**Tags:** `hot` `rustup` `cargo` `build`
**适用版本:** rustup + cargo；Rust 1.97.1

**一句话答案：**
先 `rustup target add wasm32-unknown-unknown`，再在项目里 `cargo build --target wasm32-unknown-unknown --release`，产物在 `target/wasm32-unknown-unknown/release/*.wasm`。这只得到裸 WASM；要跟 JS 友好互调通常还要 bindgen（见 [Q4](#q4)）。

**解答：**
安装目标并编译：

```bash
rustup target add wasm32-unknown-unknown
cargo new --lib hello_wasm
cd hello_wasm
cargo build --target wasm32-unknown-unknown --release
```

`src/lib.rs` 最小导出直觉（无 bindgen 时可用 `#[no_mangle]` 等；浏览器侧仍要自己写加载；bindgen 更常见）：

```text
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

`Cargo.toml` 可先保持默认 lib；若做 cdylib：

```toml
[lib]
crate-type = ["cdylib", "rlib"]
```

产物路径：

```text
target/wasm32-unknown-unknown/release/hello_wasm.wasm
```

「❌ 错误写法」——忘加 target 直接 `--target`：

```bash
# 未 rustup target add 时会失败：找不到该目标的标准库
cargo build --target wasm32-unknown-unknown
```

**Go 对比：**
```bash
GOOS=js GOARCH=wasm go build -o main.wasm
# 还需 wasm_exec.js 等运行支撑
```
- **Go 怎么做**：改环境变量交叉编译。
- **Rust 为什么不同**：用 rustup **target** + cargo `--target`。
- **Go 程序员易踩的坑**：只 build 出 `.wasm` 就以为页面能直接 `WebAssembly.instantiate` 跑复杂库——常缺 glue。

**记忆点：**
- `target add` → `cargo build --target`。
- 裸 `.wasm` ≠ 完整前后端桥。

---

## Q4. wasm-bindgen / wasm-pack 分别干什么？ {#q4}
**Tags:** `hot` `wasm-bindgen` `wasm-pack`
**适用版本:** wasm-bindgen / wasm-pack 以 crates.io / 安装文档为准

**一句话答案：**
**wasm-bindgen**：编译期/工具链生成 Rust↔JS 的类型化胶水（导出函数、字符串、结构等）。**wasm-pack**：把“编译 + bindgen + 打成 npm 能用的包”流程包起来，省手写步骤。多数浏览器项目：`wasm-pack build` 就够入门。

**解答：**
分工：

```text
你的 Rust 源码
    ↓  rustc（wasm 目标）
.wasm + 元数据
    ↓  wasm-bindgen
.wasm + JS/TS glue
    ↓  wasm-pack（编排上述步骤 + package.json 布局）
可 npm 依赖的包
```

依赖与属性示意（text）：

```toml
[dependencies]
wasm-bindgen = "0.2"

[lib]
crate-type = ["cdylib", "rlib"]
```

```text
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("hello, {name}")
}
```

常用命令：

```bash
cargo install wasm-pack
wasm-pack build --target web
# 或 --target bundler / nodejs，按宿主选
```

**Go 对比：**
- **Go 怎么做**：`syscall/js` 手写绑定 + 官方 `wasm_exec.js`。
- **Rust 为什么不同**：bindgen 从注解生成大量样板；wasm-pack 再打包。
- **Go 程序员易踩的坑**：只装了 rustc 目标、没跑 bindgen，却期望字符串像 JS 一样自动来回——类型桥要工具生成。

**记忆点：**
- bindgen = 桥；wasm-pack = 一键构建桥+包。
- `#[wasm_bindgen]` 标导出。

---

## Q5. 和 JS 互调函数怎么直觉理解？ {#q5}
**Tags:** `hot` `JS` `FFI` `bindgen` `ABI`
**适用版本:** wasm-bindgen 模型

**一句话答案：**
把 WASM 想成**只能通过导入/导出表说话**的沙箱：Rust 导出函数给 JS `import`；Rust 要调 `alert`/DOM/fetch，必须经 bindgen 声明的 **JS 导入**。字符串与复杂对象不是“直接指针共享”，而是胶水编码/解码（有时涉及 WASM 线性内存）。

**解答：**
双向：

```text
JS  → 调用导出 →  Rust #[wasm_bindgen] fn
Rust → 调用导入 →  #[wasm_bindgen(module = "...")] 或 js_sys / web_sys
```

导出给 JS（text）：

```text
#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

JS 侧直觉：

```text
import init, { add } from "./pkg/hello_wasm.js";
await init();
console.log(add(2, 3));
```

从 Rust 调 JS（示意）：

```text
#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn shout() {
    alert("hi from rust");
}
```

边界规则：
- 数字、`bool` 最好传；`String`/`Vec` 交给 bindgen。
- 不要假设能随便传 `&T` 裸指针给 JS 长期持有。
- 异步见 [Q11](#q11)。

**Go 对比：**
```go
import "syscall/js"
js.Global().Get("console").Call("log", "hi")
```
- **Go 怎么做**：`syscall/js` 运行时反射式调 JS。
- **Rust 为什么不同**：多在编译期用 bindgen/`web-sys` 生成。
- **Go 程序员易踩的坑**：把 Go 的 `js.Value` 动态风格硬套到 Rust——Rust 侧更偏生成好的类型化 API。

**记忆点：**
- 只有 import/export，没有“偷偷碰 DOM”。
- 字符串走胶水，不走裸指针幻想。

---

## Q6. 大小怎么优化：opt-level、LTO、wasm-opt？ {#q6}
**Tags:** `hot` `size` `LTO` `wasm-opt` `release`
**适用版本:** Cargo profile；Binaryen `wasm-opt` 为可选外部工具

**一句话答案：**
Release 开小体积优化：`opt-level = "z"`（或 `"s"`）、**LTO**、必要时 `codegen-units = 1`，再跑 **wasm-opt -Oz**；并考虑 `panic = "abort"`（见 [Q7](#q7)）。体积是配置+剥离+后处理叠出来的，不是单靠 `--release`。

**解答：**
`Cargo.toml` profile 示意：

```toml
[profile.release]
opt-level = "z"     # 优化体积
lto = true          # 链接时优化
codegen-units = 1   # 更好优化，编译更慢
panic = "abort"
strip = true        # 较新 Cargo：剥符号
```

构建：

```bash
cargo build --target wasm32-unknown-unknown --release
# 若用 wasm-pack，它可串联优化；也可手动：
wasm-opt -Oz -o out.wasm target/wasm32-unknown-unknown/release/your.wasm
```

还有哪些“隐性体积”：
- 拉了 `web-sys` 全特征 → feature 裁剪。
- 格式化/panic 信息字符串 → `abort` + 少用 `format!` 热路径。
- 未开启 LTO 的依赖边界 → 开 LTO。

**Go 对比：**
- **Go 怎么做**：`-ldflags="-s -w"` 减符号；WASM 仍常带运行时。
- **Rust 为什么不同**：无 GC 运行时，但标准库/panic/格式化仍能胀；工具链更强调 LTO/`wasm-opt`。
- **Go 程序员易踩的坑**：两边都只打 release 就以为已经最小——都还要再剥一层。

**记忆点：**
- `z` + LTO + strip + `wasm-opt`。
- 裁 feature 和 panic 策略同样重要。

---

## Q7. `panic=abort` 和 `no_std` 何时考虑？ {#q7}
**Tags:** `common` `panic` `no_std` `size`
**适用版本:** Cargo profile；`no_std` 需自行设计

**一句话答案：**
要缩体积、且能接受 panic 直接中止模块时，用 **`panic = "abort"`**（不做栈展开）。**`no_std`** 在极致嵌入/无分配或自定义分配、不要标准库的场景再考虑；浏览器业务库多数仍用 `std` + abort 就够。

**解答：**
`panic=abort`：

```toml
[profile.release]
panic = "abort"
```

效果直觉：

```text
unwind（默认）: panic 可展开、体积与复杂度更高
abort         : panic ≈ 直接停，二进制通常更小
```

`no_std` 何时：
- 目标极小、无 OS、自己管分配或完全不分配。
- 写可被多种嵌入宿主复用的核心算法 crate。

何时**先别**上 `no_std`：
- 还在用 wasm-bindgen + 常规 `String`/`Vec` 的网页模块——`std` 更省事。
- 团队还不熟 `core`/`alloc` 边界。

可编译的“仍用 std”空 lib 心智（主机上验证逻辑，真正 wasm 用 `--target`）：

```rust
pub fn clamp(n: i32, lo: i32, hi: i32) -> i32 {
    n.max(lo).min(hi)
}

fn main() {
    // 普通 bin 可测；wasm 库项目则放在 lib + 测试里
    assert_eq!(clamp(100, 0, 10), 10);
}
```

**Go 对比：**
- **Go 怎么做**：很难真正 `no_std`；运行时几乎总在。
- **Rust 为什么不同**：可以选择不要 std，换体积与能力。
- **Go 程序员易踩的坑**：一上来就 `#![no_std]` 却还在用 `String`/`HashMap` 的 std 心智——要改 `alloc` 或收束 API。

**记忆点：**
- 先 `panic=abort`；真要抠到骨子再 `no_std`。
- 网页业务优先 std。

---

## Q8. WASI 能做文件/网络吗？边界在哪？ {#q8}
**Tags:** `common` `WASI` `filesystem` `capability`
**适用版本:** WASI preview；能力随宿主实现变化

**一句话答案：**
**能，但只在宿主授予的能力里**：WASI 把文件/环境/时钟等做成可裁剪权限；默认不是“全盘 root”。网络在早期 WASI 与预览版里支持度因实现而异——不要假设和本地 Linux 进程一样 `bind :80`。浏览器里的 `unknown-unknown` 更不是靠 WASI 读盘。

**解答：**
能力模型：

```text
宿主（wasmtime 等）
  └─ 启动 WASM 时传入：可访问的目录、环境变量、stdio…
        └─ 模块内 open/read 只能落在授权范围
```

文件：常见“预打开目录”模式——宿主映射 `./data` → 模块内路径。  
网络：查清你的 WASI 版本与运行时（wasmtime 等）当前支持；很多生产场景仍把网络留在**宿主**，WASM 只做纯计算。

边界口诀：

| 环境 | 文件 | 网络 |
|------|------|------|
| 浏览器 + unknown-unknown | 经 JS（上传/IndexedDB 等） | 经 JS `fetch` |
| WASI + wasmtime | 经授权目录 | 看 WASI/宿主；常受限 |
| 原生 OS 进程 | 常规权限模型 | 常规 socket |

**Go 对比：**
- **Go 怎么做**：`js/wasm` 下文件系统/网络同样受运行时限制，不是桌面 Go。
- **Rust 为什么不同**：WASI 把“能力安全”写进接口叙事更强。
- **Go 程序员易踩的坑**：以为编译成 WASM 仍能 `os.Open("/etc/passwd")`——宿主说了算。

**记忆点：**
- WASI = 带权限的系统接口，不是满血 Linux。
- 浏览器 I/O 走 JS，不走幻想中的 POSIX。

---

## Q9. 和 Go 的 `GOOS=js GOARCH=wasm` 怎么对照？ {#q9}
**Tags:** `common` `Go` `GOARCH=wasm` `cheat-sheet`
**适用版本:** Go 1.x js/wasm；Rust wasm 目标

**一句话答案：**
Go：`GOOS=js GOARCH=wasm go build` + `wasm_exec.js` + `syscall/js`。Rust：`rustup target add` + `cargo build --target wasm32-unknown-unknown` +（通常）wasm-bindgen/wasm-pack。都是“编译成 WASM 进浏览器”，但运行时体积、互操作风格、工具链名词不同。

**解答：**

| 维度 | Go | Rust |
|------|----|------|
| 交叉编译 | `GOOS=js GOARCH=wasm` | `--target wasm32-unknown-unknown` |
| JS 互操作 | `syscall/js` | wasm-bindgen / `web-sys` |
| 启动胶水 | `wasm_exec.js` | bindgen 生成的 JS |
| GC | 有 | 无（除非用 GC 语言特性/外部） |
| 体积倾向 | 往往更大 | 更易抠到很小 |
| WASI | 另线 | rustup WASI 目标清晰 |

命令对照：

```bash
# Go
GOOS=js GOARCH=wasm go build -o main.wasm

# Rust
rustup target add wasm32-unknown-unknown
cargo build --target wasm32-unknown-unknown --release
```

**Go 对比：**
- **Go 怎么做**：环境变量选目标，官方 JS 运行支撑。
- **Rust 为什么不同**：target 三元组 + 可选 bindgen 生态。
- **Go 程序员易踩的坑**：把 Go 的 `wasm_exec.js` 步骤原样找 Rust——Rust 侧换成 bindgen 输出。

**记忆点：**
- 概念镜像：交叉编译 + JS 胶水。
- 名词不共用：别找 `GOOS` 在 cargo 里。

---

## Q10. 在浏览器跑 vs 在 wasmtime 跑差在哪？ {#q10}
**Tags:** `common` `browser` `wasmtime` `host`
**适用版本:** 宿主差异；与 Rust 版本弱相关

**一句话答案：**
**浏览器**：沙箱强、I/O 经 Web API/JS、常用 bindgen、受页面与同源策略约束。**wasmtime**（及同类）：嵌入本地/服务端，可挂 WASI 能力、当插件引擎；没有 DOM。同一份源码未必同一 target、更未必同一套导入。

**解答：**

```text
浏览器宿主
  ├─ 加载：fetch .wasm + JS glue
  ├─ 能力：DOM、fetch、WebWorker…
  └─ 目标：常 wasm32-unknown-unknown

wasmtime 宿主
  ├─ 加载：嵌入式 API 读 .wasm
  ├─ 能力：你配置的 WASI/host functions
  └─ 目标：常 WASI 或自定义导入
```

选型：
- 给网页加速编解码 → 浏览器路径。
- 给边缘节点/插件跑不可信模块 → wasmtime + 严格能力。
- “一份 wasm 通吃两处” → 先对齐 target 与导入，再谈复用核心 `no_std` 算法 crate。

**Go 对比：**
- **Go 怎么做**：浏览器 `js/wasm` 一条主路径；服务端嵌入另选运行时。
- **Rust 为什么不同**：浏览器与 WASI 工具链都常用，文档里分叉更明显。
- **Go 程序员易踩的坑**：拿浏览器 bindgen 产物丢进 wasmtime 期望直接跑——导入表对不上。

**记忆点：**
- 宿主决定能力；target 跟着宿主走。
- 复用逻辑，谨慎复用同一 `.wasm` 文件。

---

## Q11. 异步和线程在 WASM 里有什么限制？ {#q11}
**Tags:** `occasional` `async` `threads` `SharedArrayBuffer`
**适用版本:** 浏览器线程/原子能力依赖 COOP/COEP 等；持续演进

**一句话答案：**
浏览器主路径上，异步通常是 **JS Promise ↔ WASM 导出/导入** 的协作，不是随意 `tokio` 多线程跑满 OS。真正的线程依赖 **原子 + SharedArrayBuffer** 等，且受浏览器安全头限制；许多项目用单线程 + 把阻塞交给 JS/`web-sys` 异步 API。

**解答：**
实用图景：

```text
常见：WASM 同步算完 → 返回 JS；或导出 async（bindgen）等 Promise
少见/有门槛：WASM 内多线程（atomics + 合适的打包/头配置）
WASI/wasmtime：线程与异步模型跟宿主/标准版本相关，勿照搬浏览器假设
```

注意点：
- 在 WASM 里阻塞主线程 = 卡页面；重活放 Worker 或切细任务。
- 不要假设桌面 Tokio 多线程 runtime 原样搬进浏览器。
- 需要并行时，先查当前 `wasm32` 线程目标与打包方案是否满足部署环境。

**Go 对比：**
- **Go 怎么做**：goroutine 在 `js/wasm` 上有运行时支持，但同样受浏览器单线程事件模型约束。
- **Rust 为什么不同**：线程/异步更“显式可选”，默认别当原生服务器。
- **Go 程序员易踩的坑**：以为 `async fn` + Tokio 在浏览器里自动等于 Go 的 goroutine 调度——宿主模型不同。

**记忆点：**
- 先单线程 + JS 异步；真要线程先查浏览器门槛。
- 别把桌面并发模型原样塞进页面。

---

## Q12. 什么时候别用 WASM？ {#q12}
**Tags:** `common` `when-not` `architecture`
**适用版本:** 架构判断

**一句话答案：**
DOM 密集 UI、需要频繁廉价跨边界传大数据、团队只会 JS 且热点不值、或纯CRUD后台——别硬上 WASM。它适合**可隔离的计算内核**，不适合“把整个应用搬进沙箱图个新鲜”。

**解答：**
更该继续用 JS/TS 或普通服务端的信号：
- 主要工作是改 DOM、绑表单、调一堆 Web API。
- 每帧在 JS↔WASM 间拷贝巨大 TypedArray，胶水成本吃掉增益。
- 构建链（bindgen、打包、调试 sourcemap）拖垮迭代，而性能没测出瓶颈。
- 只要调 REST 的业务服务——直接 Go/Rust 原生进程更简单。

更该用 WASM 的信号：
- 已有 Rust 核心库，想在浏览器复用。
- 编解码、校验、几何、图像、密码学热点经 profiling 证实。
- 需要统一沙箱插件格式（WASI）跑到边缘/桌面宿主。

决策口诀：

```text
先测瓶颈 → 再抽内核到 WASM
先写整站 Rust WASM UI → 通常后悔
```

**Go 对比：**
- **Go 怎么做**：同样不该为“能编译成 wasm”而把所有服务端搬进浏览器。
- **Rust 为什么不同**：生态更推 WASM，**误用诱惑也更大**。
- **Go 程序员易踩的坑**：用 Rust WASM 重写已足够快的 JS 逻辑——机会成本高。

**记忆点：**
- WASM 是手术刀，不是瑞士军刀替代品。
- 有测量、有边界，再引入。

---

## Q13. JS string / 内存边界要注意什么？ {#q13}
**Tags:** `common` `wasm-bindgen` `string` `memory`
**适用版本:** wasm-bindgen 模型；细节以当前文档为准

**一句话答案：**
JS `string` 与 Rust `String`/`&str` **不共享同一块内存视图**：跨边界通常要 **编码拷贝**（UTF-8 ↔ JS 字符串）。大块二进制优先 `Uint8Array` / 共享缓冲策略；别在热循环里来回传巨型字符串。胶水由 **wasm-bindgen** 生成，但拷贝成本仍在。

**解答：**
边界心智：

```text
JS string  ──(bindgen 编码/拷贝)──►  Rust String / &str
Rust 字节  ──(拷贝或视图约定)──►  JS Uint8Array
WASM 线性内存是一块 ArrayBuffer；指针只在 WASM 侧有意义
```

导出字符串时（示意，需 wasm-bindgen）：

```toml
[dependencies]
wasm-bindgen = "0.2"
```

```text
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    // name 已从 JS 拷入 WASM；返回值再拷回 JS
    format!("hello, {name}")
}
```

标准库侧提醒「字符串本身可分配」：

```rust
fn main() {
    let s = String::from("跨边界会复制");
    assert!(!s.is_empty());
}
```

注意点清单：
- 每次 `String` 往返 ≈ 分配 + 拷贝；profiling 后再优化。
- 改 WASM 内存后，若把裸指针丢给 JS 且内存增长导致 ArrayBuffer 分离，旧视图会失效——跟 bindgen 文档的 typed array 规则走。
- DOM/频繁 UI 字符串拼接仍更适合留在 JS（见 [Q12](#q12)）。

**Go 对比：**
- **Go 怎么做**：`syscall/js` 同样有 JS Value 与 Go string 的转换成本。
- **Rust 为什么不同**：bindgen 更类型化，但**拷贝经济学**两边一样。
- **Go 程序员易踩的坑**：以为「都在浏览器里就零拷贝」——默认不是。

**记忆点：**
- 字符串跨边界 ≈ 拷贝；热路径少传大串。
- 指针只在 WASM 线性内存里有意义。
- 大块数据想清楚 TypedArray 策略。

---

## Q14. wasm 体积太大第一步查什么？ {#q14}
**Tags:** `common` `size` `wasm-opt` `diagnostics`
**适用版本:** 发布构建；工具以当前生态为准

**一句话答案：**
先确认你在看 **`--release`（或 wasm-pack 的 release）产物**，再按 [Q6](#q6) 打开 **`opt-level = "z"` / LTO / `panic = "abort"` / strip / `wasm-opt`**。仍大：用 **twiggy** 等工具看谁占空间（格式化、正则、panic 信息、未裁掉的依赖），而不是先盲目 `no_std`。

**解答：**
第一步检查表：

```text
[ ] 1. 量的是 release .wasm，不是 debug
[ ] 2. Cargo.toml：[profile.release] opt-level="z", lto=true, codegen-units=1
[ ] 3. panic = "abort"（见 [Q7](#q7)）
[ ] 4. strip / 去掉调试信息
[ ] 5. 再跑 wasm-opt -Oz
[ ] 6. 仍大 → 分析哪些 crate/函数贡献体积
```

配置回顾（与 [Q6](#q6) 一致）：

```toml
[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
```

```rust
fn main() {
    // 体积优化发生在构建配置与后处理，不在这行业务代码
    println!("measure the .wasm, not the source line count");
}
```

常见「隐形胖子」：`format!`/大量字符串、`regex`、完整 `std` 的某些路径、依赖树里用了半个框架。先减依赖与开 LTO，再考虑 `no_std`。

**Go 对比：**
- **Go 怎么做**：同样先看是否含运行时/调试信息；Go wasm 体积基线往往更高。
- **Rust 为什么不同**：更常靠 LTO + `wasm-opt` 抠到很小，但配置漏了会「看起来不该这么大」。
- **Go 程序员易踩的坑**：拿 debug 或未 wasm-opt 的文件和文章里的 KB 数比大小。

**记忆点：**
- 先 release + z/LTO/abort/strip/wasm-opt。
- 再分析依赖与符号，别先上 `no_std` 玄学。
