+++
title = "3 Android 上的裸机"
date = 2026-08-11T11:30:00+08:00
weight = 338
type = "docs"
description = "Android 上的裸机 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/android.html](https://google.github.io/comprehensive-rust/bare-metal/android.html)

# 3 Android 上的裸机

要在 AOSP 中构建裸机 Rust 二进制文件，您需要使用 `rust_ffi_static`
Soong 规则构建 Rust 代码，然后使用带有链接器脚本的“cc_binary”
生成二进制文件本身，然后生成 `raw_binary` 将 ELF 转换为原始文件
二进制文件已准备好运行。

```soong
rust_ffi_static {
    name: "libvmbase_example",
    defaults: ["vmbase_ffi_defaults"],
    crate_name: "vmbase_example",
    srcs: ["src/main.rs"],
    rustlibs: [
        "libvmbase",
    ],
}

cc_binary {
    name: "vmbase_example",
    defaults: ["vmbase_elf_defaults"],
    srcs: [
        "idmap.S",
    ],
    static_libs: [
        "libvmbase_example",
    ],
    linker_scripts: [
        "image.ld",
        ":vmbase_sections",
    ],
}

raw_binary {
    name: "vmbase_example_bin",
    stem: "vmbase_example.bin",
    src: ":vmbase_example",
    enabled: false,
    target: {
        android_arm64: {
            enabled: true,
        },
    },
}
```
