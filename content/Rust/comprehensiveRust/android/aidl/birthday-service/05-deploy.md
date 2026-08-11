+++
title = "4.1.5 部署"
date = 2026-08-11T11:30:00+08:00
weight = 220
type = "docs"
description = "05-部署 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/example-service/deploy.html](https://google.github.io/comprehensive-rust/android/aidl/example-service/deploy.html)

# 4.1.5 部署

现在可以构建、推送并启动服务：

```shell
m birthday_server
adb push "$ANDROID_PRODUCT_OUT/system/bin/birthday_server" /data/local/tmp
adb root
adb shell /data/local/tmp/birthday_server
```

在另一个终端检查服务是否在运行：

```shell
adb shell service check birthdayservice
```

```text
Service birthdayservice: found
```

也可以用 `service call` 调用该服务：

```shell
adb shell service call birthdayservice 1 s16 Bob i32 24
```

```text
Result: Parcel(
  0x00000000: 00000000 00000036 00610048 00700070 '....6...H.a.p.p.'
  0x00000010: 00200079 00690042 00740072 00640068 'y. .B.i.r.t.h.d.'
  0x00000020: 00790061 00420020 0062006f 0020002c 'a.y. .B.o.b.,. .'
  0x00000030: 006f0063 0067006e 00610072 00750074 'c.o.n.g.r.a.t.u.'
  0x00000040: 0061006c 00690074 006e006f 00200073 'l.a.t.i.o.n.s. .'
  0x00000050: 00690077 00680074 00740020 00650068 'w.i.t.h. .t.h.e.'
  0x00000060: 00320020 00200034 00650079 00720061 ' .2.4. .y.e.a.r.'
  0x00000070: 00210073 00000000                   's.!.....        ')
```
