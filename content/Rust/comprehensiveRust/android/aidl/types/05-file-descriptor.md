+++
title = "4.2.5 发送文件"
date = 2026-08-11T11:30:00+08:00
weight = 229
type = "docs"
description = "05-发送文件 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/types/file-descriptor.html](https://google.github.io/comprehensive-rust/android/aidl/types/file-descriptor.html)

# 4.2.5 发送文件

可以使用 `ParcelFileDescriptor` 类型在 Binder 客户端/服务端之间发送文件：

_birthday_service/aidl/com/example/birthdayservice/IBirthdayService.aidl_：

```java
interface IBirthdayService {
    /** 同样的事，但从文件加载信息。 */
    String wishFromFile(in ParcelFileDescriptor infoFile);
}
```

_birthday_service/src/client.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    binder::ProcessState::start_thread_pool();
    let service = connect().expect("Failed to connect to BirthdayService");

    // 打开文件并把生日信息写入其中。
    let mut file = File::create("/data/local/tmp/birthday.info").unwrap();
    writeln!(file, "{name}")?;
    writeln!(file, "{years}")?;

    // 从该文件创建 `ParcelFileDescriptor` 并发送。
    let file = ParcelFileDescriptor::new(file);
    service.wishFromFile(&file)?;
}
```

_birthday_service/src/lib.rs_：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl IBirthdayService for BirthdayService {
    fn wishFromFile(
        &self,
        info_file: &ParcelFileDescriptor,
    ) -> binder::Result<String> {
        // 将文件描述符转换为 `File`。`ParcelFileDescriptor` 包装了
        // 一个 `OwnedFd`，可以克隆后再用来创建 `File` 对象。
        let mut info_file = info_file
            .as_ref()
            .try_clone()
            .map(File::from)
            .expect("Invalid file handle");

        let mut contents = String::new();
        info_file.read_to_string(&mut contents).unwrap();

        let mut lines = contents.lines();
        let name = lines.next().unwrap();
        let years: i32 = lines.next().unwrap().parse().unwrap();

        Ok(format!("Happy Birthday {name}, congratulations with the {years} years!"))
    }
}
```

> - `ParcelFileDescriptor` 包装了 `OwnedFd`，因此可以从 `File`（或任何其他包装 `OwnedFd` 的类型）创建，并在另一端用来创建新的 `File` 句柄。
> - 也可以包装并发送其他类型的文件描述符，例如 TCP、UDP 与 UNIX 套接字。

