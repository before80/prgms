+++
title = "2.18-WebAssembly/WASI"
date = 2026-08-22T20:00:00+08:00
weight = 20
type = "docs"
description = "在 WASM/WASI 上使用 Criterion"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# WebAssembly/WASI {#wasi}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/wasi.html](https://bheisler.github.io/criterion.rs/book/user_guide/wasi.html)


Criterion 基准测试可以编译为 WebAssembly/WASI。这使你可以使用 [wasmer](https://wasmer.io/) 和 [wasmtime](https://wasmtime.dev/) 等运行时，以及 [NodeJS](https://nodejs.org/en/) 或 Web 浏览器（[FireFox](https://www.mozilla.org/en-US/firefox/new/)、[Chrome](https://www.google.com/chrome/)、[Safari](https://www.apple.com/safari/)）等 JavaScript 环境对代码进行性能测试。

## 添加 `wasm32-wasi` 目标

我们交叉编译到 WebAssembly System Interface（即 WASI），因此必须添加正确的目标。若忘记此步骤，基准测试将无法编译，并会显示友好提示。我们使用 [rustup](https://rustup.rs/) 工具：

```properties
rustup target add wasm32-wasi
```

## 安装 cargo-wasi

接下来安装 `cargo-wasi` 命令。虽然 Criterion 不要求此工具，但它能大大简化 WASI 程序的构建。

```properties
cargo install cargo-wasi
```

## 构建

安装 `wasm32-wasi` 和 `cargo-wasi` 后，我们几乎可以编译基准测试了。还剩一件事：告诉 Criterion 不要使用 rayon 等在 WASI 中尚不可用的默认特性：

```diff
[dev-dependencies]
-criterion = "0.5.1"
+criterion = { version = "0.5.1", default-features = false }
```

使用 `cargo-wasi` 编译基准测试会自动选择正确目标并优化生成的文件。这里以 [hex](https://crates.io/crates/hex) crate 为例：

```properties
cargo wasi build --bench=hex --release
```

也可以不使用 `cargo-wasi` 编译：

```properties
cargo build --bench=hex --release --target wasm32-wasi
```

此时 `target/wasm32-wasi/release/deps/` 中应有一个 `.wasm` 文件。若使用了 `cargo-wasi`，会有优化版和未优化版。为方便起见，将最新的 WASM 文件复制到顶层目录：

```console
cp `ls -t target/wasm32-wasi/release/deps/*.wasm | head -n 1` hex.wasm
```

## 使用 wasmer/wasmtime 运行

```properties
wasmer run --dir=. hex.wasm -- --bench
```

```properties
wasmtime run --dir=. hex.wasm -- --bench
```

## 使用 nodejs 运行

可通过 wasmer-cli 在 NodeJS 中运行：

```properties
npm install -g @wasmer/cli
```

安装 `wasmer-js` 后，接口与纯 `wasmer` 相同：

```properties
wasmer-js run --dir=. hex.wasm -- --bench
```

## 在浏览器中使用 webassembly.sh 运行

浏览器不原生支持 WASI，但有变通方案。最简单的方案是 [webassembly.sh](https://webassembly.sh/)。该网站使用内存文件系统模拟 WASI。

使用该网站时，访问 https://webassembly.sh/，将 `hex.wasm` 文件拖放到浏览器窗口，然后输入：

```properties
hex --bench
```

开始基准测试后，浏览器窗口会冻结直到结果就绪。这是在浏览器中运行 WebAssembly 的不幸限制。

### 导出结果

在浏览器中将基准测试结果写入内存文件系统本身用处不大。幸运的是，结果可以轻松导出并下载为 JSON：

```properties
hex --bench --export=base | download
```

## 比较结果

让我们用原生、wasmer、wasmtime、nodejs、firefox 和 chromium 运行同一基准测试，看看它们如何对比。第一步是生成 json 文件：

```properties
wasmer run --dir=. hex.wasm -- --bench --save-baseline wasmer
wasmer run --dir=. hex.wasm -- --bench --export wasmer > wasmer.json
```

```properties
wasmtime run --dir=. hex.wasm -- --bench --save-baseline wasmtime
wasmtime run --dir=. hex.wasm -- --bench --export wasmtime > wasmtime.json
```

```properties
wasmer-js run --dir=. hex.wasm -- --bench --save-baseline nodejs
wasmer-js run --dir=. hex.wasm -- --bench --export nodejs > nodejs.json
```

```properties
hex --bench --save-baseline firefox
hex --bench --export firefox | download
```

```properties
hex --bench --save-baseline chromium
hex --bench --export chromium | download
```

第二步是将 json 文件制表：

```properties
cargo bench --bench=hex -- --compare --baselines=native.json,wasmer.json,wasmtime.json,nodejs.json,firefox.json,chromium.json --compare-list
```

控制台输出：

```bash
faster_hex_decode
-----------------
native       1.00       3.6±0.02µs       ? ?/sec
wasmer      14.72      52.6±0.49µs       ? ?/sec
wasmtime    16.83      60.1±0.53µs       ? ?/sec
chromium    17.66      63.1±0.70µs       ? ?/sec
firefox     19.82      70.8±6.53µs       ? ?/sec
nodejs      20.76      74.2±0.34µs       ? ?/sec

faster_hex_decode_fallback
--------------------------
native       1.00      10.9±0.12µs       ? ?/sec
wasmer       1.49      16.2±0.04µs       ? ?/sec
firefox      1.61      17.6±0.51µs       ? ?/sec
wasmtime     1.65      18.1±0.73µs       ? ?/sec
chromium     1.87      20.4±0.16µs       ? ?/sec
nodejs       2.30      25.1±0.56µs       ? ?/sec

faster_hex_decode_unchecked
---------------------------
native       1.00   1239.7±16.97ns       ? ?/sec
wasmer      14.27      17.7±0.35µs       ? ?/sec
wasmtime    14.36      17.8±0.23µs       ? ?/sec
firefox     14.38      17.8±1.83µs       ? ?/sec
chromium    16.53      20.5±0.28µs       ? ?/sec
nodejs      20.36      25.2±0.15µs       ? ?/sec

faster_hex_encode
-----------------
native       1.00     948.3±5.47ns       ? ?/sec
wasmer      19.17      18.2±0.36µs       ? ?/sec
chromium    21.25      20.2±0.17µs       ? ?/sec
nodejs      22.85      21.7±0.09µs       ? ?/sec
wasmtime    24.01      22.8±0.53µs       ? ?/sec
firefox     30.68      29.1±0.89µs       ? ?/sec

faster_hex_encode_fallback
--------------------------
native       1.00      11.1±0.20µs       ? ?/sec
firefox      1.98      21.9±0.57µs       ? ?/sec
chromium     2.04      22.7±0.20µs       ? ?/sec
wasmtime     2.05      22.8±0.13µs       ? ?/sec
wasmer       2.06      22.8±0.15µs       ? ?/sec
nodejs       2.38      26.4±0.09µs       ? ?/sec

hex_decode
----------
native       1.00     244.6±2.36µs       ? ?/sec
firefox      1.66    405.7±14.22µs       ? ?/sec
wasmer       1.72     421.4±9.65µs       ? ?/sec
wasmtime     1.73     423.0±3.00µs       ? ?/sec
nodejs       2.00     490.3±3.49µs       ? ?/sec
chromium     2.81    688.5±12.23µs       ? ?/sec

hex_encode
----------
native       1.00      69.2±0.40µs       ? ?/sec
wasmtime     1.18      81.7±0.38µs       ? ?/sec
wasmer       1.46     100.9±1.22µs       ? ?/sec
nodejs       2.20     152.5±1.93µs       ? ?/sec
firefox      3.25     224.8±7.53µs       ? ?/sec
chromium     4.08     282.7±4.19µs       ? ?/sec

rustc_hex_decode
----------------
native       1.00     103.1±2.78µs       ? ?/sec
wasmer       1.33     136.8±4.06µs       ? ?/sec
wasmtime     1.38     142.3±3.31µs       ? ?/sec
firefox      1.50     154.7±4.80µs       ? ?/sec
nodejs       1.78     183.3±2.02µs       ? ?/sec
chromium     2.04     210.0±3.37µs       ? ?/sec

rustc_hex_encode
----------------
native       1.00      30.9±0.42µs       ? ?/sec
wasmtime     2.24      69.1±0.36µs       ? ?/sec
wasmer       2.25      69.6±0.74µs       ? ?/sec
nodejs       2.40      74.2±1.94µs       ? ?/sec
chromium     2.67      82.6±2.61µs       ? ?/sec
firefox      3.31     102.2±2.66µs       ? ?/sec
```

# 注意事项与陷阱

## 预热与 JIT

大多数 WebAssembly 环境在代码运行一段时间后才能达到峰值性能。这意味着预热步骤至关重要，跳过它（设为 0 秒或使用 `--quick` 标志）会导致结果不准确。

## 在 [webassembly.sh](https://webassembly.sh/) 中重新运行基准测试

WebAssembly.sh 网站模拟 Criterion 所需的 WebAssembly System Interface（WASI）。但该模拟并不完美，多次运行会导致 criterion 严重失败。若遇到此问题，重新加载浏览器窗口通常可以绕过。

## Wasm 与 default-features

编译到 wasm 时必须禁用 Criterion 的默认特性。否则将触发编译错误。若看到某特性与 wasm 不兼容的错误，打开 `Cargo.toml` 并进行如下修改：

```diff
[dev-dependencies]
-criterion = "0.5.1"
+criterion = { version = "0.5.1", default-features = false }
```
