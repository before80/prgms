+++
title = "6-常见问题"
date = 2026-08-22T20:00:00+08:00
weight = 29
type = "docs"
description = "Criterion.rs 常见问题解答"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 常见问题 {#faq}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/faq.html](https://bheisler.github.io/criterion.rs/book/faq.html)


## 在 CI 流水线中应如何运行 Criterion.rs 基准测试？

你可能不应该这样做（或者，如果你确实要跑，也不要依赖其结果）。Travis-CI、Github Actions 等云 CI 提供商使用的虚拟化会在基准测试过程中引入大量噪声，而 Criterion.rs 的统计分析只能有限地缓解这一点。这可能导致测得的性能出现大幅变化，即使代码的实际性能并未改变。更好的替代方案是使用 [Iai](https://github.com/bheisler/iai)。Iai 在 Cachegrind 内运行基准测试，直接统计指令数和内存访问次数。Iai 的测量结果不会因虚拟机变慢或暂停一段时间而失真，因此在虚拟化环境中应更可靠。

不过，无论你使用哪种基准测试工具，流程基本相同。你需要：

* 检出代码的主分支
* 构建并运行一次基准测试，以建立基线
* 然后切换到拉取请求分支
* 再次构建并运行基准测试，与基线进行比较

## `cargo bench` 对有效命令行选项报「Unrecognized Option」错误

默认情况下，Cargo 在基准测试时会隐式向你的 crate 添加 `libtest` 基准测试 harness，用于处理任何 `#[bench]` 函数，即使你没有这类函数。它会先编译并运行这个可执行文件，然后再运行其他基准测试。通常这没问题——它会检测到没有 `libtest` 基准测试需要执行并退出，让 Cargo 继续运行真正的基准测试。不幸的是，它会先检查命令行参数，一旦发现不认识的参数就会 panic。这会导致 Cargo 提前停止基准测试，永远不会执行 Criterion.rs 基准测试。

当使用 Criterion.rs 支持但 `libtest` 不支持的任何参数运行 `cargo bench` 时，就会出现这种情况。例如，`--verbose` 和 `--save-baseline` 会引发此问题，而 `--help` 不会。目前有两种变通方法：

你可以只运行你的 Criterion 基准测试，例如：

`cargo bench --bench my_benchmark -- --verbose`

注意，此处的 `my_benchmark` 对应 `Cargo.toml` 文件中基准测试的名称。

另一种选择是为你的 lib 或 app crate 禁用基准测试。例如，对于库 crate，可以在 `Cargo.toml` 中添加：

```toml
[lib]
bench = false
```

如果你的 crate 除了库之外还生成一个或多个二进制文件，可能还需要在 `Cargo.toml` 中添加类似记录：

```toml
[[bin]]
name = "my-binary"
path = "src/bin/my-binary.rs"
bench = false
```

这是因为 Cargo 会自动发现某些类型的二进制文件，并同样为它们启用默认基准测试 harness。

当然，这仅在你将所有基准测试定义在 `benches` 目录中时才有效。

更多细节请参阅 [Rust Issue #47241](https://github.com/rust-lang/rust/issues/47241)。

## 应如何对小型函数进行基准测试？

与对其他任何函数进行基准测试的方式完全相同。

有时有人建议，对小型（纳秒级）函数的基准测试应在内部多次迭代被测函数，以减少测量开销的影响。使用 Criterion.rs 时这 _不是_ 必需的，也不推荐。

为说明这一点，考虑以下基准测试：

```rust
fn compare_small(c: &mut Criterion) {
    let mut group = c.benchmark_group("small");
    group.bench_with_input("unlooped", 10, |b, i| b.iter(|| i + 10));
    group.bench_with_input("looped", 10, |b, i| b.iter(|| {
        for _ in 0..10000 {
            std::hint::black_box(i + 10);
        }
    }));
    group.finish();
}
```

该基准测试只是将两个数相加——几乎是最小的可执行函数。在我的计算机上，输出如下：

```
small/unlooped          time:   [270.00 ps 270.78 ps 271.56 ps]
Found 2 outliers among 100 measurements (2.00%)
  2 (2.00%) high severe
small/looped            time:   [2.7051 us 2.7142 us 2.7238 us]
Found 5 outliers among 100 measurements (5.00%)
  3 (3.00%) high mild
  2 (2.00%) high severe
```

2.714 微秒 / 10000 = 271.4 皮秒，结果基本一致。有趣的是，这略多于我第四代 Core i7 最大时钟频率 4.4 GHz 的一个周期，说明现代 CPU 的流水线非常出色。无论如何，Criterion.rs 能够准确测量低至单条指令的函数。有关 Criterion.rs 如何进行测量的更多细节，请参阅[分析流程](../analysis/)页面；有关如何选择计时循环以最小化测量开销，请参阅[计时循环](../user-guide/12-timing-loops/)页面。

## 何时应使用 `std::hint::black_box`？

`black_box` 是一个阻止某些编译器优化的函数。基准测试往往带有一定的人为性质，编译器可能利用这一点，在编译基准测试时生成比实际使用中更快的代码。特别是，被测函数常以常量参数调用，在某些情况下 rustc 可以在编译期完全求值该函数，并用常量替换函数调用。这会产生不自然地快的基准测试，无法反映代码在正常调用时的表现。因此，对常量输入进行 black-box 处理以阻止这种优化是有用的。

不过，你可能有一个预期会以一个或多个常量参数调用的函数。在这种情况下，你可能希望编写基准测试来代表该场景，并允许编译器优化常量参数。

大多数情况下，Criterion.rs 会为你处理这一点——如果你使用参数化基准测试，Criterion.rs 会自动对参数进行 black-box 处理，你无需做任何事。然而，如果你编写的是带参数函数的未参数化基准测试，这可能值得考虑。

## Cargo 对 Cargo.toml 中显式 `[[bench]]` 段打印警告

目前，Cargo 将 `benches` 目录中的任何 `*.rs` 文件视为基准测试，除非 `Cargo.toml` 中有一个或多个 `[[bench]]` 段。在这种情况下，自动发现会完全禁用。

在 Rust 2018 edition 中，Cargo 将改为 `[[bench]]` 不再禁用自动发现。如果你的 `benches` 目录包含非基准测试的源文件，更新后可能会破坏构建，因为 Cargo 会尝试将它们作为基准测试编译并失败。

有两种方法可以防止这种破坏。你可以显式关闭自动发现，如下所示：

```toml
[[package]]
autobenches = false
```

另一种选择是将那些非基准测试文件移到子目录（例如 `benches/benchmark_code`），这样它们就不会再被识别为基准测试。我推荐后一种方案。

注意，包含 `criterion_main!` 的文件是有效的基准测试，可以安全地保留在原位置。

## 我对源码做了微不足道的修改，Criterion.rs 却报告性能大幅变化。为什么？

别担心，Criterion.rs 没有坏，你（很可能）也没有做错什么。最常见的原因是优化器在修改后恰好以不同方式优化了你的函数。

像 LLVM（`rustc` 使用的后端）这样的优化编译器后端往往是复杂的系统，充满手工编写的模式匹配代码，用于检测何时可以进行特定优化，并试图猜测这是否会让代码更快。不幸的是，尽管在这些编译器上投入了大量工程工作，源码中看似微不足道的修改（例如改变行的顺序）往往就足以让这些优化器表现不同。此外，看似微小的修改（例如改变变量类型，或调用略有不同的函数，如 `unwrap` 与 `expect`）在底层的影响往往比源码文本的细微差异所暗示的要大得多。

如果你想了解更多（以及未来改善这一状况的一些提案），我推荐 Regehr 等人的[这篇论文](https://blog.regehr.org/archives/1619)。

在类似主题上，重要的是要记住，基准测试永远只是对函数真实性能的估计。如果优化器在基准测试这样的人为环境中能对性能产生显著影响，那么当你的函数被内联到各种不同的调用上下文中时又会怎样？优化器几乎肯定会对每个调用者做出不同决策。人们希望每个特化版本都会更快，但这无法保证。在优化编译器的世界里，函数的「真实性能」确实是个模糊的概念。

如果你仍然确信 Criterion.rs 出了问题，请提交 issue 描述该问题。

## 我对源码 _没有_ 做任何修改，Criterion.rs 却报告性能大幅变化。为什么？

通常这是因为基准测试环境并不完全相同。有很多因素会影响基准测试。其他进程可能正在使用 CPU 或内存。电池供电设备通常有降频 CPU 的省电模式（台式机上有时也会出现）。如果你的基准测试在 VM 内运行，同一物理机上可能有其他 VM 在争夺资源。

然而，有时即使没有变化也会发生这种情况。重要的是要记住，Criterion.rs 通过统计学检测回归和改进。总有一定概率你会随机得到异常快或异常慢的样本，足以让 Criterion.rs 将其检测为变化，尽管实际上并未发生变化。在非常大的基准测试套件中，每次运行基准测试时你可能都会看到若干此类虚假检测。

不幸的是，这是统计学中的根本权衡。要降低误检率，就必须降低对小变化的敏感度。反之，要提高对小变化的敏感度，就必须增加误检的概率。Criterion.rs 的默认设置在两者之间取得了普遍良好的平衡，但你可以根据需要调整设置。

## 直接运行基准测试可执行文件（不使用 Cargo）时，它们只打印「Success」。为什么？

当 Cargo 运行基准测试时，会向基准测试可执行文件传递 `--bench` 或 `--test` 命令行参数。Criterion.rs 会查找这些参数，并尝试运行基准测试或进入测试模式。特别是，当你运行 `cargo test --benches`（运行测试，包括测试基准测试）时，Cargo 不会传递这两个参数中的任何一个。这也许有些奇怪，因为 `cargo bench --test` 会同时传递 `--bench` 和 `--test`。无论如何，当 `--bench` 不存在，或 `--bench` 与 `--test` 同时存在时，Criterion.rs 基准测试会以测试模式运行。

## 我的基准测试编译失败，报错「use of undeclared type or module `<my_crate>`」

首先，请查阅[入门指南](https://bheisler.github.io/criterion.rs/book/getting_started.html)，确保 `Cargo.toml` 中的 `[[bench]]` 段配置正确。如果配置正确，请继续阅读。

这可能由两种不同的原因引起。

最常见的情况是尝试对二进制（而非库）crate 进行基准测试。Criterion.rs 不能用于对二进制 crate 进行基准测试（更多原因请参阅[已知限制](https://bheisler.github.io/criterion.rs/book/user_guide/known_limitations.html)页面）。通常的变通方法是将应用程序结构化为库 crate（实现应用程序的大部分功能）和二进制 crate（作为围绕库 crate 的薄包装，提供 CLI 等功能）。然后，你可以创建依赖库 crate 的 Criterion.rs 基准测试。

较少见的情况是库 crate 被配置为编译为 `cdylib`。要使用 Criterion.rs 对 crate 进行基准测试，你需要在 `Cargo.toml` 中设置同时生成 `rlib`。

## 如何对函数的一部分进行基准测试？

简短回答是——你无法准确做到。详细说明如下。

当有人问我这个问题时，我的第一反应总是「把函数的那部分提取成一个新函数，给它起个名字，然后对 _那个_ 函数进行基准测试」。这有点令人不满足，但这也是真正准确测量代码片段的唯一方法。你始终可以用 `#[inline(always)]` 标记它，告诉 rustc 在最终可执行文件中将其内联回原始调用点。

问题在于，系统时钟并非无限精确；`Instant::now` 报告的时钟时间有一定的（往往出乎意料地大）粒度。这意味着，如果 Criterion.rs 单独测量每次执行，对于耗时 1ms 的函数，它可能看到类似「0ms, 0ms, 0ms, 0ms, 0ms, 5ms, 0ms...」的时间序列。为缓解这一点，Criterion.rs 会多次迭代你的基准测试，将这种抖动分摊到每次迭代上。除非那部分代码已经容易拆分并放入独立函数，否则无法对代码的 _部分_ 运行这样的计时循环。否则，你只能单独计时每次迭代，从而产生最大可能的计时抖动。

不过，如果你确实需要这样做，并且可以接受降低的精度，可以使用 `Bencher::iter_custom` 按你想要的方式测量代码。`iter_custom` 的存在是为了处理多线程代码等复杂情况，或者——是的——测量函数的一部分。只需注意，测量精度由你自己负责。
