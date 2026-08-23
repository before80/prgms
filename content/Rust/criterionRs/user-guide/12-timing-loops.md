+++
title = "2.12-计时循环"
date = 2026-08-22T20:00:00+08:00
weight = 14
type = "docs"
description = "iter、iter_with_setup 等计时方式"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Criterion.rs Documentation](https://bheisler.github.io/criterion.rs/book/)

# 计时循环 {#timing-loops}


> 原文链接: [https://bheisler.github.io/criterion.rs/book/user_guide/timing_loops.html](https://bheisler.github.io/criterion.rs/book/user_guide/timing_loops.html)


[`Bencher`](https://bheisler.github.io/criterion.rs/criterion/struct.Bencher.html) 结构体提供多种函数，实现不同的计时循环以测量函数性能。本页说明这些计时循环的工作原理，以及在不同场景下应选用哪一种。

## `iter`

最简单的计时循环是 `iter`。对于大多数基准测试，它应是默认选择。`iter` 在紧凑循环中调用基准测试 N 次，并记录整个循环的耗时。由于它只进行两次测量（循环前后的时间），且循环内不做其他事情，`iter` 的测量开销实际上为零——意味着它能准确测量小到单条处理器指令的函数性能。

然而，`iter` 也有局限。若基准测试返回实现了 Drop 的值，它会在循环内被 drop，drop 函数的时间会计入测量。此外，有些基准测试需要每次迭代的准备工作。例如排序算法基准测试可能需要未排序数据，但我们不希望生成未排序数据影响测量。`iter` 无法做到这一点。

## `iter_with_large_drop`

`iter_with_large_drop` 针对第一个问题。此时，基准测试返回的值会被收集到 `Vec` 中，在测量完成后再 drop。这会引入少量测量开销，意味着测量值会略高于函数的真实运行时间。这种开销几乎总是可以忽略，但应意识到它的存在。极快的基准测试（例如数百皮秒或更小范围）或返回非常大结构的基准测试可能产生更多开销。

除测量开销外，`iter_with_large_drop` 还有自身限制。将返回值收集到 `Vec` 会使用堆内存，且用量不由用户控制，而取决于迭代次数，迭代次数又取决于基准测试设置和被测函数的运行时间。基准测试可能在收集待 drop 的值时耗尽内存。

## `iter_batched` / `iter_batched_ref`

`iter_batched` 和 `iter_batched_ref` 是计时循环复杂度的下一步。这些计时循环接受两个闭包而非一个。第一个闭包无参数并返回 `T` 类型的值——用于生成准备数据。例如，准备函数可能克隆一个未排序向量，用于排序函数基准测试。第二个闭包是被测函数，接受 `T`（`iter_batched`）或 `&mut T`（`iter_batched_ref`）。

这两种计时循环生成一批输入，并测量对批内所有值执行基准测试的时间。与 `iter_with_large_drop` 一样，它们也会将基准测试返回值收集到 `Vec` 中并在不计时的情况下稍后 drop。然后生成另一批输入，重复该过程，直到测得足够多的基准测试迭代。请记住，仅当基准测试会修改输入时才需要这样做——若输入恒定，可复用同一输入值，基准测试应使用 `iter`。

两种计时循环都接受第三个参数来控制批次大小。若批次过大，可能在生成输入和收集输出时耗尽内存。若过小，可能引入不必要的测量开销。为便于使用，Criterion 通过 [`BatchSize`](https://bheisler.github.io/criterion.rs/criterion/enum.BatchSize.html) 枚举提供三种预定义批次大小选择——`SmallInput`、`LargeInput` 和 `PerIteration`。也可以（不推荐）手动设置批次大小。

`SmallInput` 应是大多数基准测试的默认选择。它针对准备值较小（小到可在内存中安全存放数百万个值）且输出同样较小或不存在的基准测试进行调优。`SmallInput` 产生的测量开销最小（与 `iter_with_large_drop` 相当，因此对几乎所有基准测试都可忽略），但使用的内存最多。

若输入或输出的规模大到 `SmallInput` 占用过多内存，应使用 `LargeInput`。`LargeInput` 产生的测量开销略高于 `SmallInput`，但对几乎所有基准测试仍小到可忽略。

`PerIteration` 强制批次大小为 1。即生成单个准备输入、计时函数执行一次、丢弃准备数据和输出，然后重复。这会产生大量测量开销——比其他选项高出数个数量级，足以影响数百纳秒范围的基准测试。应尽可能避免使用 `PerIteration`。然而，当输入或输出极大，或持有有限资源（如文件句柄）时，有时必须使用它。

虽然强烈建议坚持使用预定义设置，但必要时 Criterion.rs 也允许用户选择自己的批次大小。可通过 `BatchSize::NumBatches` 或 `BatchSize::NumIterations` 实现，分别指定每样本的批次数或每批的迭代次数。这些选项应仅在必要时使用，因为用户需要手动调优以获得准确结果。不过，当所有预定义选项都不适用时，它们仍可作为选项。`NumBatches` 通常应优先于 `NumIterations`，因为其测量开销通常更小，但 `NumIterations` 对批次大小提供更多控制，某些情况下可能需要。

## `iter_custom`

这是一种特殊的「计时循环」，依赖你自己完成计时。其他计时循环接受在循环中调用 N 次的 lambda，而它接受形如 `FnMut(iters: u64) -> M::Value` 的 lambda——即接受迭代次数并返回测量值。通常，对于默认的 `WallTime` 测量，这将是 `Duration`，其他测量可能使用其他类型（更多细节参见[自定义测量](../13-custom-measurements/)页面）。该 lambda 可执行测量所需的任何操作。

当需要做的事情不符合通常的「在循环中调用函数」方式时，使用 `iter_custom`。例如，可用于：

* 通过发送迭代次数并接收耗时来基准测试外部进程
* 测量线程池执行 N 个任务所需时间，以观察锁竞争或池大小如何影响挂钟时间

尽量将测量例程中的开销保持在最低；Criterion.rs 仍会使用其正常的预热/目标时间逻辑，该逻辑基于挂钟时间。若测量例程每次测量耗时很长，可能扰乱计算并导致 Criterion.rs 运行过少迭代（更不用说基准测试会耗时很长）。因此，最好在运行基准测试之前完成繁重准备，如启动进程或线程。

## 若函数运行时间小于测量开销该怎么办？

Criterion.rs 的计时循环经过精心设计，尽可能降低测量开销。对于大多数基准测试，测量开销可以安全忽略，因为大多数基准测试的真实运行时间相对开销非常大。然而，运行时间与开销相差不大的基准测试可能难以测量。

若你认为基准测试相对于测量开销很小，首先应调整计时循环以降低开销。首选 `iter` 或配合 `SmallInput` 的 `iter_batched`，因为这些选项产生的测量开销最小。一般而言，使用更大批次的 `iter_batched` 产生更少开销，因此将 `PerIteration` 替换为具有合适批次大小的 `NumIterations` 通常可降低开销。然而，批次大小也可能过大，反而增加（而非减少）开销。

若仍不足，唯一办法是对更大的函数进行基准测试。在基准测试内手动固定次数执行例程很诱人，但这与 `NumIterations` 已做的事等价。唯一区别是 Criterion.rs 能考虑 `NumIterations` 并显示单次迭代的正确运行时间，而非多次。相反，应考虑在更高层次进行基准测试。

需要强调，测量开销仅对非常快且会修改输入的函数有意义。对于较慢的函数（粗略地说，纳秒级或更大，或对 `PerIteration` 为微秒级，假设相当现代的 x86_64 处理器和操作系统或等价环境），测量开销没有实质影响。对于只读取输入而不修改或消耗输入的函数，可使用 `iter` 循环让所有迭代共享一个值，其开销实际上为零。

## 已弃用的计时循环

在较旧的 Criterion.rs 基准测试（2.10 之前）中，可能看到另外两种计时循环：`iter_with_setup` 和 `iter_with_large_setup`。`iter_with_setup` 等价于配合 `PerIteration` 的 `iter_batched`。`iter_with_large_setup` 等价于配合 `NumBatches(1)` 的 `iter_batched`。两者产生的测量开销都远大于 `SmallInput`。此外，`large_setup` 也使用更多内存。两者都应更新为使用 `iter_batched`，最好配合 `SmallInput`。它们为向后兼容而保留，但已不再出现在 API 文档中。
