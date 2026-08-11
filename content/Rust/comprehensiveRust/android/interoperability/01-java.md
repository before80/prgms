+++
title = "7.3 与 Java 互操作"
date = 2026-08-11T11:30:00+08:00
weight = 254
type = "docs"
description = "01-与 Java 互操作 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/java.html](https://google.github.io/comprehensive-rust/android/interoperability/java.html)

# 7.3 与 Java 互操作

Java 可以通过
[Java Native Interface (JNI)](https://en.wikipedia.org/wiki/Java_Native_Interface)
加载共享对象。[`jni` crate](https://docs.rs/jni/) 允许你创建兼容的库。

首先，创建一个要导出给 Java 的 Rust 函数：

_interoperability/java/src/lib.rs_：

```rust,compile_fail
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Rust <-> Java FFI demo.

use jni::JNIEnv;
use jni::objects::{JClass, JString};
use jni::sys::jstring;

/// HelloWorld::hello method implementation.
// SAFETY: There is no other global function of this name.
#[unsafe(no_mangle)]
pub extern "system" fn Java_HelloWorld_hello(
    mut env: JNIEnv,
    _class: JClass,
    name: JString,
) -> jstring {
    let input: String = env.get_string(&name).unwrap().into();
    let greeting = format!("Hello, {input}!");
    let output = env.new_string(greeting).unwrap();
    output.into_raw()
}
```

_interoperability/java/Android.bp_：

```javascript
rust_ffi_shared {
    name: "libhello_jni",
    crate_name: "hello_jni",
    srcs: ["src/lib.rs"],
    rustlibs: ["libjni"],
}
```

然后从 Java 调用该函数：

_interoperability/java/HelloWorld.java_：

```java
class HelloWorld {
    private static native String hello(String name);

    static {
        System.loadLibrary("hello_jni");
    }

    public static void main(String[] args) {
        String output = HelloWorld.hello("Alice");
        System.out.println(output);
    }
}
```

_interoperability/java/Android.bp_：

```javascript
java_binary {
    name: "helloworld_jni",
    srcs: ["HelloWorld.java"],
    main_class: "HelloWorld",
    jni_libs: ["libhello_jni"],
}
```

最后，可以构建、同步并运行该二进制：

```shell
m helloworld_jni
adb sync  # requires adb root && adb remount
adb shell /system/bin/helloworld_jni
```

> - `unsafe(no_mangle)` 属性指示 Rust 按原样发出 `Java_HelloWorld_hello` 符号。这一点很重要，以便 Java 能把该符号识别为 `HelloWorld` 类上的 `hello` 方法。
>
>   - 默认情况下，Rust 会 mangling（重命名）符号，以便一个二进制可以链接同一 Rust crate 的两个版本。

