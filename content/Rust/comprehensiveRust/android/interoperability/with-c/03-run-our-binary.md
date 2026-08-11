+++
title = "7.1.3 运行二进制"
date = 2026-08-11T11:30:00+08:00
weight = 238
type = "docs"
description = "03-运行二进制 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/with-c/run-our-binary.html](https://google.github.io/comprehensive-rust/android/interoperability/with-c/run-our-binary.html)

# 7.1.3 运行二进制

在设备上构建、推送并运行该二进制：

```shell
m print_birthday_card
adb push "$ANDROID_PRODUCT_OUT/system/bin/print_birthday_card" /data/local/tmp
adb shell /data/local/tmp/print_birthday_card
```

最后，可以运行自动生成的测试以确保绑定可用：

_interoperability/bindgen/Android.bp_：

```javascript
rust_test {
    name: "libbirthday_bindgen_test",
    srcs: [":libbirthday_bindgen"],
    crate_name: "libbirthday_bindgen_test",
    test_suites: ["general-tests"],
    auto_gen_config: true,
    clippy_lints: "none", // Generated file, skip linting
    lints: "none",
}
```

```shell
atest libbirthday_bindgen_test
```
