+++
title = "02-用泛型模拟类型类"
date = 2026-08-18T22:10:00+08:00
weight = 48
type = "docs"
description = "用泛型模拟类型类 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/functional/generics-type-classes.html](https://rust-unofficial.github.io/patterns/functional/generics-type-classes.html)

# 用泛型模拟类型类

## 描述 {#description}

Rust 的类型系统设计得更像函数式语言（如 Haskell），而不是命令式语言（如 Java 和 C++）。因此，Rust 能把许多编程问题变成「静态类型」问题。这是选择函数式语言的最大收益之一，也对 Rust 的许多编译期保证至关重要。

这一思想的关键部分是泛型类型的工作方式。例如在 C++ 和 Java 中，泛型类型是面向编译器的元编程构造。C++ 中的 `vector<int>` 和 `vector<char>` 只是同一份 `vector` 类型样板代码（称为 `template`）填入两种不同类型后的两份拷贝。

在 Rust 中，泛型类型参数会创建函数式语言中所谓的「类型类约束」，而最终用户填入的每一个不同参数*实际上都会改变类型*。换言之，`Vec<isize>` 和 `Vec<char>` *是两种不同的类型*，类型系统的所有部分都会将其识别为彼此不同。

这称为**单态化（monomorphization）**：从**多态**代码创建出不同的类型。这种特殊行为要求 `impl` 块指定泛型参数。泛型类型的不同取值会产生不同的类型，而不同的类型可以有不同的 `impl` 块。

在面向对象语言中，类可以从父类继承行为。然而，这允许不仅为类型类的特定成员附加额外行为，还能附加更多行为。

最接近的等价物是 Javascript 和 Python 中的运行时多态：任何构造函数都可以随意给对象添加新成员。然而，与那些语言不同，Rust 的所有额外方法在使用时都能做类型检查，因为它们的泛型是静态定义的。这使得它们在保持安全的同时更易用。

## 示例 {#example}

假设你在为一组实验室机器设计存储服务器。由于所涉软件，你需要支持两种不同的协议：BOOTP（用于 PXE 网络启动）和 NFS（用于远程挂载存储）。

你的目标是用 Rust 写一个能同时处理两者的程序。它会有协议处理器并监听这两种请求。主应用逻辑随后允许实验室管理员为实际文件配置存储与安全控制。

无论来自何种协议，实验室机器对文件的请求都包含相同的基本信息：一种认证方式，以及要检索的文件名。一种直截了当的实现看起来会像这样：

```rust,ignore
enum AuthInfo {
    Nfs(crate::nfs::AuthInfo),
    Bootp(crate::bootp::AuthInfo),
}

struct FileDownloadRequest {
    file_name: PathBuf,
    authentication: AuthInfo,
}
```

这种设计或许够用。但现在假设你需要支持添加*协议特有*的元数据。例如，对于 NFS，你想知道它们的挂载点，以便强制执行额外的安全规则。

当前结构体的设计把协议决策留到了运行时。这意味着任何只适用于一种协议而不适用于另一种的方法，都要求程序员做运行时检查。

获取 NFS 挂载点会像这样：

```rust,ignore
struct FileDownloadRequest {
    file_name: PathBuf,
    authentication: AuthInfo,
    mount_point: Option<PathBuf>,
}

impl FileDownloadRequest {
    // ... 其他方法 ...

    /// 若这是 NFS 请求则获取 NFS 挂载点。否则，
    /// 返回 None。
    pub fn mount_point(&self) -> Option<&Path> {
        self.mount_point.as_ref()
    }
}
```

每个 `mount_point()` 的调用者都必须检查 `None` 并编写处理代码。即便他们知道在给定代码路径中只会使用 NFS 请求，也是如此！

若不同类型的请求被混淆时能产生编译期错误，会好得多。毕竟，用户代码的整条路径——包括他们使用库中的哪些函数——都会知道请求是 NFS 请求还是 BOOTP 请求。

在 Rust 中，这实际上是可能的！解决方案是*添加一个泛型类型*以拆分 API。

看起来像这样：

```rust
use std::path::{Path, PathBuf};

mod nfs {
    #[derive(Clone)]
    pub(crate) struct AuthInfo(String); // NFS 会话管理从略
}

mod bootp {
    pub(crate) struct AuthInfo(); // bootp 中无认证
}

// 保持模块私有，防止外部用户发明自己的协议。
mod proto_trait {
    use super::{bootp, nfs};
    use std::path::{Path, PathBuf};

    pub(crate) trait ProtoKind {
        type AuthInfo;
        fn auth_info(&self) -> Self::AuthInfo;
    }

    pub struct Nfs {
        auth: nfs::AuthInfo,
        mount_point: PathBuf,
    }

    impl Nfs {
        pub(crate) fn mount_point(&self) -> &Path {
            &self.mount_point
        }
    }

    impl ProtoKind for Nfs {
        type AuthInfo = nfs::AuthInfo;
        fn auth_info(&self) -> Self::AuthInfo {
            self.auth.clone()
        }
    }

    pub struct Bootp(); // 无额外元数据

    impl ProtoKind for Bootp {
        type AuthInfo = bootp::AuthInfo;
        fn auth_info(&self) -> Self::AuthInfo {
            bootp::AuthInfo()
        }
    }
}

use proto_trait::ProtoKind; // 保持内部可见以防止外部 impl
pub use proto_trait::{Bootp, Nfs}; // 重新导出，以便调用方可见

struct FileDownloadRequest<P: ProtoKind> {
    file_name: PathBuf,
    protocol: P,
}

// 所有公共 API 部分放入泛型 impl 块
impl<P: ProtoKind> FileDownloadRequest<P> {
    fn file_path(&self) -> &Path {
        &self.file_name
    }

    fn auth_info(&self) -> P::AuthInfo {
        self.protocol.auth_info()
    }
}

// 所有协议特有的 impl 放入各自的块
impl FileDownloadRequest<Nfs> {
    fn mount_point(&self) -> &Path {
        self.protocol.mount_point()
    }
}

fn main() {
    // 你的代码写在这里
}
```

采用这种方法，如果用户出错并使用了错误的类型：

```rust,ignore
fn main() {
    let mut socket = crate::bootp::listen()?;
    while let Some(request) = socket.next_request()? {
        match request.mount_point().as_ref() {
            "/secure" => socket.send("Access denied"),
            _ => {} // 继续……
        }
        // 其余代码写在这里
    }
}
```

他们会得到语法错误。类型 `FileDownloadRequest<Bootp>` 没有实现 `mount_point()`，只有类型 `FileDownloadRequest<Nfs>` 实现了。而后者当然是由 NFS 模块创建的，不是 BOOTP 模块！

## 优点 {#advantages}

首先，它允许对多个状态共有的字段去重。通过使非共享字段成为泛型，它们只需实现一次。

其次，它让 `impl` 块更易读，因为它们按状态拆分。所有状态共有的方法在一个块中只写一次，而某一状态独有的方法则在单独的块中。

这两者都意味着代码行数更少，且组织得更好。

## 缺点 {#disadvantages}

由于编译器中单态化的实现方式，这目前会增大二进制体积。希望未来实现能够改进。

## 替代方案 {#alternatives}

- 若某个类型因构造或部分初始化而似乎需要「拆分 API」，请考虑改用
  [构建器模式](../design-patterns/02-creational/01-builder/)。

- 若类型之间的 API 不变——只有行为改变——则更适合使用
  [策略模式](../design-patterns/01-behavioural/05-strategy/)。

## 参见 {#see-also}

这种模式贯穿标准库：

- `Vec<u8>` 可以从 String 转换而来，与其他每一种 `Vec<T>` 不同。[^1]
- 迭代器可以转换成二叉堆，但仅当它们包含实现了 `Ord` trait 的类型时。[^2]
- `to_string` 方法仅为 `str` 类型的 `Cow` 做了特化。[^3]

若干流行 crate 也用它来获得 API 灵活性：

- 用于嵌入式设备的 `embedded-hal` 生态大量使用这种模式。例如，它允许静态验证用于控制嵌入式引脚的设备寄存器配置。当引脚进入某种模式时，它返回一个 `Pin<MODE>` 结构体，其泛型决定了该模式下可用、且不在 `Pin` 本身上的函数。[^4]

- `hyper` HTTP 客户端库用它为不同的可插拔请求暴露丰富的 API。带有不同连接器的客户端既有不同的方法，也有不同的 trait 实现，同时有一组核心方法适用于任何连接器。[^5]

- 「类型状态」模式——对象基于内部状态或不变量获得与失去 API——在 Rust 中用相同的基本概念、略有不同的技术实现。[^6]

[^1]: 参见：
    [impl From\<CString\> for Vec\<u8\>](https://doc.rust-lang.org/1.59.0/src/std/ffi/c_str.rs.html#803-811)

[^2]: 参见：
    [impl\<T: Ord\> FromIterator\<T\> for BinaryHeap\<T\>](https://web.archive.org/web/20201030132806/https://doc.rust-lang.org/stable/src/alloc/collections/binary_heap.rs.html#1330-1335)

[^3]: 参见：
    [impl\<'\_\> ToString for Cow\<'\_, str>](https://doc.rust-lang.org/stable/src/alloc/string.rs.html#2235-2240)

[^4]: 示例：
    [https://docs.rs/stm32f30x-hal/0.1.0/stm32f30x_hal/gpio/gpioa/struct.PA0.html](https://docs.rs/stm32f30x-hal/0.1.0/stm32f30x_hal/gpio/gpioa/struct.PA0.html)

[^5]: 参见：
    [https://docs.rs/hyper/0.14.5/hyper/client/struct.Client.html](https://docs.rs/hyper/0.14.5/hyper/client/struct.Client.html)

[^6]: 参见：
    [The Case for the Type State Pattern](https://web.archive.org/web/20210325065112/https://www.novatec-gmbh.de/en/blog/the-case-for-the-typestate-pattern-the-typestate-pattern-itself/)（类型状态模式的理由）
    以及
    [Rusty Typestate Series（详尽专题）](https://web.archive.org/web/20210328164854/https://rustype.github.io/notes/notes/rust-typestate-series/rust-typestate-index)
