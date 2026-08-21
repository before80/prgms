+++
title = "02-视为未定义行为"
date = 2026-08-18T08:45:00+08:00
weight = 110
type = "docs"
description = "视为未定义行为 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/behavior-considered-undefined.html](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

r[undefined]
# 视为未定义行为

r[undefined.intro]
若 Rust 代码表现出下列任一行为，则该代码不正确。这包括 `unsafe` 块与 `unsafe` 函数中的代码。`unsafe` 仅意味着避免未定义行为是程序员的责任；它并不改变 Rust 程序绝不能导致未定义行为这一事实。

r[undefined.soundness]
编写 `unsafe` 代码时，程序员有责任确保任何与该 `unsafe` 代码交互的安全代码都无法触发这些行为。对任意安全客户端都满足此性质的 `unsafe` 代码称为*健全（sound）*；若安全代码可能误用 `unsafe` 代码从而表现出未定义行为，则它是*不健全（unsound）*的。

> **警告**
> 下列列表并非穷尽；它可能增长或缩减。对于不安全代码中何为允许、何为不允许，尚无 Rust 语义的形式化模型，因此可能还有更多被视为不安全的行为。我们也保留将来把该列表中某些行为定为已定义的权利。换言之，本列表并不表示任何内容在未来所有 Rust 版本中都*必定*始终是未定义的（但我们将来可能对某些列表项作出此类承诺）。
>
> 在编写不安全代码之前，请阅读 [Rustonomicon]。

r[undefined.race]
* 数据竞争。

r[undefined.pointer-access]
* 访问（从中加载或向其存储）一个[悬垂][dangling]的、或[基于未对齐指针][based on a misaligned pointer]的 place。

r[undefined.place-projection]
* 执行违反[边界内指针算术](pointer#method.offset)要求的偏移性 place 投影。偏移性 place 投影是[字段表达式][project-field]、[元组索引表达式][project-tuple]或[数组/切片索引表达式][project-slice]。

r[undefined.alias]
* 打破指针别名规则。确切的别名规则尚未确定，但以下是一般原则的概要：

  * `&T` 必须指向在其存活期间不被突变的内存（[`UnsafeCell<U>`] 内部的数据除外）。
  * `&mut T` 必须指向在其存活期间不被任何非由该引用派生的指针读写、且没有其他引用指向的内存（无例外）。
  * 就这些规则而言，`Box<T>` 的处理方式类似于 `&'static mut T`。

  这些规则适用于*所有*引用与 `Box<T>`，包括存储在私有字段中的那些（例如，若你的类型有类型为 `&mut T` 的私有字段，则只要该类型的值存活，该引用就必须按上述意义保持唯一）。

  确切的存活时长未指定，但存在一些边界：

  * 对于引用，存活时长以上层借用检查器所赋予的语法生命周期为上界；其存活不能比该生命周期*更长*。
  * 每次解引用或重新借用引用或 box 时，都视其存活。
  * 每次将引用或 box 传入或从函数返回时，都视其存活。
  * 当引用（但不是 `Box`！）被传入函数时，它至少在该函数调用期间存活，再次地，若 `&T` 包含 [`UnsafeCell<U>`] 则除外。

  当这些类型的值作为复合类型的（嵌套）字段传递时，上述规则同样适用，但不适用于指针间接之后的情形。

r[undefined.immutable]
* 变异不可变字节。通过[常量提升][const-promoted]表达式可达的所有字节都是不可变的，通过 `static` 与 `const` 初始化器中的借用可达、且已被[生命周期延长][lifetime-extended]至 `'static` 的字节亦然。不可变绑定或不可变 `static` 所拥有的字节是不可变的，除非这些字节是 [`UnsafeCell<U>`] 的一部分。

  此外，共享引用[所指向][pointed to]的字节是不可变的，包括经由其他引用（共享与可变）以及 `Box` 传递可达的字节；传递性包括存储在复合类型字段中的那些引用。

  变异是指写入超过 0 个字节且与任何相关字节重叠（即便该写入并未改变内存内容）。

r[undefined.intrinsic]
* 经由编译器内建函数（intrinsic）引发未定义行为。

r[undefined.target-feature]
* 执行以当前平台不支持的平台特性编译的代码（见 [`target_feature`]），*除非*该平台明确将此记录为安全。

r[undefined.call]
* 以错误的[调用 ABI][abi] 调用函数，或展开越过不允许展开的栈帧（例如，将以 `"C-unwind"` 导入或转换的函数当作 `"C"` 函数或函数指针来调用）。

r[undefined.invalid]
* 产生[无效值][invalid-values]。每当一个值被赋给或从一个 place 读取、传入函数/原语运算，或从函数/原语运算返回时，都发生“产生”一个值。

r[undefined.asm]
* 不正确使用内联汇编。更多细节见编写使用内联汇编的代码时应遵循的[规则][rules]。

r[undefined.runtime]
* 违反 Rust 运行时的假设。Rust 运行时的大多数假设目前尚未明确文档化。
  * 与展开具体相关的假设，见 [panic 文档][unwinding-ffi]。
  * 运行时假定：若不执行栈帧所拥有局部变量的析构函数，则不会释放该 Rust 栈帧。像 `longjmp` 这类 C 函数可能违反此假设。

> **注意**
> 未定义行为影响整个程序。例如，在 C 中调用表现出 C 的未定义行为的函数，意味着你的整个程序包含未定义行为，也可能影响 Rust 代码。反之亦然，Rust 中的未定义行为可能对通过任何 FFI 调用执行的其他语言代码造成不利影响。

r[undefined.pointed-to]
## 所指向的字节

指针或引用“指向”的字节跨度由指针值与被指类型的大小（使用 `size_of_val`）决定。

r[undefined.misaligned]
## 基于未对齐指针的 place
[based on a misaligned pointer]: #places-based-on-misaligned-pointers

r[undefined.misaligned.ptr]
若在 place 计算过程中，最后一次 `*` 投影是在对其类型未对齐的指针上执行的，则称该 place“基于未对齐指针”。（若 place 表达式中没有 `*` 投影，则这是在访问局部或 `static` 的字段，rustc 将保证正确对齐。若有多次 `*` 投影，则每一次都会从内存加载待解引用的指针本身，且每一次加载都受对齐约束。注意，由于自动解引用，表面 Rust 语法中某些 `*` 投影可能被省略；此处考虑的是完全展开后的 place 表达式。）

例如，若 `ptr` 的类型为 `*const S` 且 `S` 的对齐为 8，则 `ptr` 必须 8 字节对齐，否则 `(*ptr).f` 就是“基于未对齐指针”。即便字段 `f` 的类型是 `u8`（即对齐为 1 的类型）也是如此。换言之，对齐要求来自被解引用指针的类型，*而不是*正在访问的字段的类型。

r[undefined.misaligned.load-store]
注意，基于未对齐指针的 place 仅在从中加载或向其存储时才导致未定义行为。

r[undefined.misaligned.raw]
对此类 place 使用 `&raw const`/`&raw mut` 是允许的。

r[undefined.misaligned.reference]
对 place 使用 `&`/`&mut` 要求字段类型对齐（否则程序将是“产生无效值”），这通常比要求基于已对齐指针的限制更宽松。

r[undefined.misaligned.packed]
在字段类型可能比包含它的类型更严格对齐的情况下（即 `repr(packed)`），取引用会导致编译器错误。这意味着基于已对齐指针总是足以确保新引用已对齐，但并非总是必要。

r[undefined.dangling]
## 悬垂指针
[dangling]: #dangling-pointers

r[undefined.dangling.def]
若引用/指针[所指向][points to]的并非所有字节都属于同一存活分配（因此它们尤其都必须属于*某个*分配），则该引用/指针是“悬垂”的。

r[undefined.dangling.zero-size]
若[大小为 0][zero-sized]，则该指针在平凡意义上永非“悬垂”（即便它是空指针）。

r[undefined.dangling.dynamic-size]
注意，动态大小类型（如切片与字符串）指向其整个范围，因此长度[元数据][metadata]绝不能过大，这一点很重要。

r[undefined.dangling.alloc-limit]
特别地，Rust 值的动态大小（由 `size_of_val` 决定）绝不能超过 `isize::MAX`，因为单个分配不可能大于 `isize::MAX`。

r[undefined.validity]
## 无效值
[invalid-values]: #invalid-values

r[undefined.validity.def]
Rust 编译器假定程序执行期间产生的所有值都是“有效”的，因此产生无效值即为立即 UB。

值是否有效取决于类型：

r[undefined.validity.bool]
* [`bool`] 值必须是 `false`（`0`）或 `true`（`1`）。

r[undefined.validity.fn-pointer]
* `fn` 指针值必须非空。

r[undefined.validity.char]
* `char` 值不得是代理项（即不得落在 `0xD800..=0xDFFF` 范围内），且必须小于或等于 `char::MAX`。

r[undefined.validity.never]
* `!` 值永远不得存在。

r[undefined.validity.scalar]
* 整数（`i*`/`u*`）、浮点值（`f*`）或裸指针必须已初始化，即不得从未初始化内存获得。

r[undefined.validity.str]
* `str` 值按 `[u8]` 处理，即必须已初始化。

r[undefined.validity.enum]
* `enum` 必须具有有效判别式，且该判别式所指示变体的所有字段在其各自类型上都必须有效。

r[undefined.validity.struct]
* `struct`、元组与数组要求所有字段/元素在其各自类型上有效。

r[undefined.validity.union]
* 对于 `union`，确切的有效性要求尚未决定。显然，完全能在安全代码中创建的所有值都是有效的。若联合体有一个[零大小][zero-sized]字段，则每个可能的值都有效。更多细节仍在[讨论中](https://github.com/rust-lang/unsafe-code-guidelines/issues/438)。

r[undefined.validity.reference-box]
* 引用或 [`Box<T>`] 必须已对齐且非空，不能是[悬垂][dangling]的，并且必须指向有效值（对于动态大小类型，使用由[元数据][metadata]确定的被指对象的实际动态类型）。注意最后一点（关于指向有效值）仍有一些争议。

r[undefined.validity.wide]
* 宽引用、[`Box<T>`] 或裸指针的[元数据][metadata]必须与[不定长尾部][unsized tail]的类型匹配：
  * `dyn Trait` 元数据必须是指向编译器为 `Trait` 生成的虚表的指针。（对于裸指针，此要求仍有一些争议。）
  * 切片（`[T]`）与 `str` 元数据必须是有效的 `usize`。

  此外，对于宽引用或 [`Box<T>`]，若元数据使被指值的总大小（由 `size_of_val` 决定）大于 `isize::MAX`，则该元数据无效。

  > [!NOTE]
  > 此界限针对整个被指值的大小，而不仅是其不定长尾部，并且它像约束切片或 `str` 长度一样约束 `dyn Trait` 元数据。有效的虚表描述的是不大于 `isize::MAX` 的擦除类型，但带大小的前缀仍可能使总大小超过该限制。

r[undefined.validity.valid-range]
* 若某类型具有自定义的有效值范围，则有效值必须落在该范围内。在标准库中，这影响 [`NonNull<T>`] 与 [`NonZero<T>`]。

  > [!NOTE]
  > `rustc` 通过不稳定的 `rustc_layout_scalar_valid_range_*` 属性实现这一点。

r[undefined.validity.const-provenance]
* **在[常量上下文][const contexts]中**：除上述内容外，常量求值期间还有更多与来源（provenance）相关的要求。任何持有纯整数数据的值（`i*`/`u*`/`f*` 类型以及 `bool` 与 `char`、枚举判别式，以及切片[元数据][metadata]）不得携带任何来源。任何持有指针数据的值（引用、裸指针、函数指针，以及 `dyn Trait` 元数据）必须要么不携带来源，要么所有字节都必须是同一原始指针值按正确顺序的片段。

  这意味着若指针具有来源，则将指针（引用、裸指针或函数指针）转换或以其他方式重解释为非指针类型（如整数）是未定义行为。

  > [!EXAMPLE]
  > 下列全部是 UB：
  >
  > ```rust,compile_fail
  > # use core::mem::MaybeUninit;
  > # use core::ptr;
  > // 不能将带有来源的指针重解释为整数，
  > // 否则该整数的字节将带有来源。
  > const _: usize = {
  >     let ptr = &0;
  >     unsafe { (&raw const ptr as *const usize).read() }
  > };
  >
  > // 不能重排带有来源的指针的字节，再将其解释为引用，
  > // 否则持有指针数据的值将具有顺序错误的指针片段。
  > const _: &i32 = {
  >     let mut ptr = &0;
  >     let ptr_bytes = &raw mut ptr as *mut MaybeUninit::<u8>;
  >     unsafe { ptr::swap(ptr_bytes.add(1), ptr_bytes.add(2)) };
  >     ptr
  > };
  > ```

r[undefined.validity.undef]
**注意：** 对于任何有效值集合受限的类型，未初始化内存也隐式无效。换言之，允许读取未初始化内存的唯一种情形是在 `union` 内部以及在“填充”（类型字段之间的空隙）中。

[`bool`]: types/boolean.md
[`const`]: items/constant-items.md
[abi]: items/external-blocks.md#abi
[const contexts]: const-eval.const-context
[`target_feature`]: attributes/codegen.md#the-target_feature-attribute
[`UnsafeCell<U>`]: std::cell::UnsafeCell
[Rustonomicon]: ../nomicon/index.html
[metadata]: dynamic-sized.pointer-types
[`NonNull<T>`]: core::ptr::NonNull
[`NonZero<T>`]: core::num::NonZero
[place expression context]: expressions.md#place-expressions-and-value-expressions
[rules]: inline-assembly.md#rules-for-inline-assembly
[points to]: #pointed-to-bytes
[pointed to]: #pointed-to-bytes
[project-field]: expressions/field-expr.md
[project-tuple]: expressions/tuple-expr.md#tuple-indexing-expressions
[project-slice]: expressions/array-expr.md#array-and-slice-indexing-expressions
[unsized tail]: dynamic-sized.tail
[unwinding-ffi]: panic.md#unwinding-across-ffi-boundaries
[const-promoted]: destructors.md#constant-promotion
[lifetime-extended]: destructors.md#temporary-lifetime-extension
[zero-sized]: glossary.zst
