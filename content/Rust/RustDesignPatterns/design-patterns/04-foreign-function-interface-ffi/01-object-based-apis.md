+++
title = "01-基于对象的 API"
date = 2026-08-18T22:10:00+08:00
weight = 40
type = "docs"
description = "基于对象的 API — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/ffi/export.html](https://rust-unofficial.github.io/patterns/patterns/ffi/export.html)

# 基于对象的 API

## 描述 {#description}

在设计向其他语言暴露的 Rust API 时，有一些重要设计原则与普通的 Rust API 设计相反：

1. 所有封装类型应由 Rust *拥有*，由用户 *管理*，并且是 *不透明的*。
2. 所有事务性数据类型应由用户 *拥有*，并且是 *透明的*。
3. 所有库行为都应是作用于封装类型的函数。
4. 所有库行为都应封装进不以结构、而以 *来源/生命周期* 为基础的类型中。

## 动机 {#motivation}

Rust 内置了对其他语言的 FFI 支持。它通过不同 ABI（尽管对本实践并不重要）为 crate 作者提供 C 兼容 API 的方式。

设计良好的 Rust FFI 遵循 C API 设计原则，同时尽可能少地折损 Rust 侧的设计。任何外部 API 都有三个目标：

1. 使目标语言易于使用。
2. 尽可能避免 API 在 Rust 侧强加内部不安全性。
3. 尽可能缩小内存不安全与 Rust `undefined behaviour` 的潜在空间。

超过某一点之后，Rust 代码必须信任外部语言的内存安全性。然而，Rust 侧每一处 `unsafe` 代码都是出现 bug 或加剧 `undefined behaviour` 的机会。

例如，若指针来源错误，可能因无效内存访问而导致段错误。但若它被不安全代码操纵，则可能变成全面的堆损坏。

基于对象的 API 设计允许编写具有良好内存安全特性、以及安全与 `unsafe` 之间清晰边界的垫片。

## 代码示例 {#code-example}

POSIX 标准定义了访问磁盘数据库的 API，称为
[DBM](https://web.archive.org/web/20210105035602/https://www.mankier.com/0p/ndbm.h)。
它是“基于对象”API 的优秀示例。

下面是 C 中的定义，对参与 FFI 的人来说应易于阅读。下方的评注应能帮助那些忽略细微之处的人理解它。

```C
struct DBM;
typedef struct { void *dptr, size_t dsize } datum;

int     dbm_clearerr(DBM *);
void    dbm_close(DBM *);
int     dbm_delete(DBM *, datum);
int     dbm_error(DBM *);
datum   dbm_fetch(DBM *, datum);
datum   dbm_firstkey(DBM *);
datum   dbm_nextkey(DBM *);
DBM    *dbm_open(const char *, int, mode_t);
int     dbm_store(DBM *, datum, datum, int);
```

此 API 定义了两种类型：`DBM` 和 `datum`。

上文称 `DBM` 类型为“封装”类型。它被设计为包含内部状态，并作为库行为的入口点。

它对用户完全不透明：用户无法自行创建 `DBM`，因为他们不知道其大小或布局。相反，他们必须调用 `dbm_open`，而这只给他们 *一个指向它的指针*。

这意味着在 Rust 意义上，所有 `DBM` 都由库“拥有”。未知大小的内部状态保存在由库而非用户控制的内存中。用户只能用 `open` 和 `close` 管理其生命周期，并用其他函数对其执行操作。

上文称 `datum` 类型为“事务性”类型。它被设计为便于库与用户之间交换信息。

该数据库被设计为存储“非结构化数据”，没有预定义的长度或含义。因此，`datum` 是 Rust 切片在 C 中的等价物：一堆字节，以及它们有多少的计数。主要区别是没有类型信息，而这正是 `void` 所表示的。

请记住，此头文件是从库的视角编写的。用户可能有某种他们正在使用、且大小已知的类型。但库并不关心，并且根据 C 强制转换规则，指针背后的任何类型都可以转换为 `void`。

如前所述，此类型对用户是 *透明的*。但同样，此类型由用户 *拥有*。这带来细微影响，因为它内部有那个指针。问题是：谁拥有该指针所指向的内存？

对最佳内存安全而言，答案是“用户”。但在诸如检索值的情况下，用户不知道如何正确分配它（因为他们不知道值有多长）。在这种情况下，库代码应使用用户可访问的堆——例如 C 库的 `malloc` 和 `free`——然后在 Rust 意义上 *转移所有权*。

这一切似乎都是推测，但这正是指针在 C 中的含义。它与 Rust 中的含义相同：“用户定义的生命周期。”库的用户需要阅读文档才能正确使用。即便如此，也有一些决策在用户做错时后果较轻或较重。尽量减少这些后果就是本最佳实践的目标，关键在于 *转移一切透明之物的所有权*。

## 优点 {#advantages}

这把用户必须维护的内存安全保证数量减到相对较少：

1. 不要用非 `dbm_open` 返回的指针调用任何函数（无效访问或损坏）。
2. 不要在 close 之后对指针调用任何函数（释放后使用）。
3. 任何 `datum` 上的 `dptr` 必须为 `NULL`，或指向所声明长度的有效内存切片。

此外，它避免了许多指针来源问题。为理解原因，让我们较深入地考虑一种替代方案：键迭代。

Rust 因其迭代器而闻名。实现迭代器时，程序员会创建一个生命周期受限于所有者的独立类型，并实现 `Iterator` trait。

以下是在 Rust 中为 `DBM` 做迭代的方式：

```rust,ignore
struct Dbm { ... }

impl Dbm {
    /* ... */
    pub fn keys<'it>(&'it self) -> DbmKeysIter<'it> { ... }
    /* ... */
}

struct DbmKeysIter<'it> {
    owner: &'it Dbm,
}

impl<'it> Iterator for DbmKeysIter<'it> { ... }
```

得益于 Rust 的保证，这干净、地道且安全。然而，考虑直白的 API 翻译会是什么样：

```rust,ignore
#[no_mangle]
pub extern "C" fn dbm_iter_new(owner: *const Dbm) -> *mut DbmKeysIter {
    // 此 API 是个坏主意！真实应用请改用基于对象的设计。
}
#[no_mangle]
pub extern "C" fn dbm_iter_next(
    iter: *mut DbmKeysIter,
    key_out: *const datum
) -> libc::c_int {
    // 此 API 是个坏主意！真实应用请改用基于对象的设计。
}
#[no_mangle]
pub extern "C" fn dbm_iter_del(*mut DbmKeysIter) {
    // 此 API 是个坏主意！真实应用请改用基于对象的设计。
}
```

此 API 丢失了一条关键信息：迭代器的生命周期不得超过拥有它的 `Dbm` 对象的生命周期。库的用户可能以导致迭代器活过其所迭代数据的方式使用它，从而读到未初始化内存。

下面用 C 写的示例包含一个稍后会解释的 bug：

```C
int count_key_sizes(DBM *db) {
    // 不要使用此函数。它有一个微妙但严重的 bug！
    datum key;
    int len = 0;

    if (!dbm_iter_new(db)) {
        dbm_close(db);
        return -1;
    }

    int l;
    while ((l = dbm_iter_next(owner, &key)) >= 0) { // 用 -1 表示错误
        free(key.dptr);
        len += key.dsize;
        if (l == 0) { // 迭代器结束
            dbm_close(owner);
        }
    }
    if l >= 0 {
        return -1;
    } else {
        return len;
    }
}
```

这个 bug 很经典。当迭代器返回迭代结束标记时会发生以下情况：

1. 循环条件将 `l` 设为零，因 `0 >= 0` 而进入循环。
2. 长度被增加，此时增量为零。
3. if 语句为真，于是关闭数据库。此处本应有 break 语句。
4. 循环条件再次执行，对已关闭的对象调用 `next`。

关于这个 bug 最糟糕的部分？如果 Rust 实现足够小心，这段代码多数时候能工作！若 `Dbm` 对象的内存没有被立即复用，内部检查几乎肯定会失败，导致迭代器返回 `-1` 表示错误。但偶尔它会造成段错误，甚至更糟，造成无意义的内存损坏！

这一切都无法由 Rust 避免。从它的视角看，它把这些对象放在堆上，返回指向它们的指针，并放弃了对其生命周期的控制。C 代码必须简单地“表现良好”。

程序员必须阅读并理解 API 文档。尽管有人认为这在 C 中是家常便饭，但良好的 API 设计可以降低这一风险。POSIX 的 `DBM` API 通过 *将迭代器的所有权与其父对象合并* 做到了这一点：

```C
datum   dbm_firstkey(DBM *);
datum   dbm_nextkey(DBM *);
```

于是，所有生命周期被绑定在一起，此类不安全得以防止。

## 缺点 {#disadvantages}

然而，这一设计选择也有若干缺点，同样应当考虑。

首先，API 本身变得不那么有表达力。对于 POSIX DBM，每个对象只有一个迭代器，且每次调用都会改变其状态。这比几乎任何语言中的迭代器都更受限，尽管它是安全的。或许对于其他相关对象——其生命周期不那么层次化——这种限制比安全性的代价更大。

其次，取决于 API 各部分的关系，可能需要大量设计工作。许多较容易的设计点有其他相关模式：

- [将类型收拢到包装器中](02-type-consolidation-into-wrappers/) 将多个 Rust 类型组合进一个不透明的“对象”

- [地道的错误处理](../../idioms/09-foreign-function-interface-ffi/01-idiomatic-errors/) 解释用整数码与哨兵返回值（如 `NULL` 指针）进行错误处理

- [接受字符串](../../idioms/09-foreign-function-interface-ffi/02-accepting-strings/) 允许以最少的不安全代码接受字符串，并且比
  [传递字符串](../../idioms/09-foreign-function-interface-ffi/03-passing-strings/) 更容易做对

然而，并非每个 API 都能这样完成。程序员需要根据其受众做出最佳判断。
