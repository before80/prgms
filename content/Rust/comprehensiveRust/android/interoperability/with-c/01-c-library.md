+++
title = "7.1.1 简单的 C 库"
date = 2026-08-11T11:30:00+08:00
weight = 236
type = "docs"
description = "01-简单的 C 库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/with-c/c-library.html](https://google.github.io/comprehensive-rust/android/interoperability/with-c/c-library.html)

# 7.1.1 简单的 C 库

先创建一个小的 C 库：

_interoperability/bindgen/libbirthday.h_：

```c
typedef struct card {
  const char* name;
  int years;
} card;

void print_card(const card* card);
```

_interoperability/bindgen/libbirthday.c_：

```c
#include <stdio.h>
#include "libbirthday.h"

void print_card(const card* card) {
  printf("+--------------\n");
  printf("| Happy Birthday %s!\n", card->name);
  printf("| Congratulations with the %i years!\n", card->years);
  printf("+--------------\n");
}
```

把它加到你的 `Android.bp` 文件中：

_interoperability/bindgen/Android.bp_：

```javascript
cc_library {
    name: "libbirthday",
    srcs: ["libbirthday.c"],
}
rust_bindgen {
    name: "libbirthday_bindgen",
    crate_name: "birthday_bindgen",
    wrapper_src: "libbirthday_wrapper.h",
    source_stem: "bindings",
    static_libs: ["libbirthday"],
}
rust_test {
    name: "libbirthday_bindgen_test",
    srcs: [":libbirthday_bindgen"],
    crate_name: "libbirthday_bindgen_test",
    test_suites: ["general-tests"],
    auto_gen_config: true,
    clippy_lints: "none", // 生成的文件，跳过 lint
    lints: "none",
}
```
