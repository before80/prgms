+++
title = "7.1.5 从 C 调用 Rust"
date = 2026-08-11T11:30:00+08:00
weight = 240
type = "docs"
description = "05-从 C 调用 Rust — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/with-c/rust.html](https://google.github.io/comprehensive-rust/android/interoperability/with-c/rust.html)

# 7.1.5 从 C 调用 Rust

现在可以从 C 二进制调用它了：

_interoperability/rust/libanalyze/analyze.h_

```c
#ifndef ANALYZE_H
#define ANALYZE_H

void analyze_numbers(int x, int y);

#endif
```

_interoperability/rust/analyze/main.c_

```c
#include "analyze.h"

int main() {
  analyze_numbers(10, 20);
  analyze_numbers(123, 123);
  return 0;
}
```

_interoperability/rust/analyze/Android.bp_

```javascript
cc_binary {
    name: "analyze_numbers",
    srcs: ["main.c"],
    static_libs: ["libanalyze_ffi"],
}
```

在设备上构建、推送并运行该二进制：

```shell
m analyze_numbers
adb push "$ANDROID_PRODUCT_OUT/system/bin/analyze_numbers" /data/local/tmp
adb shell /data/local/tmp/analyze_numbers
```
