+++
title = "07-调试器"
date = 2026-08-18T08:45:00+08:00
weight = 40
type = "docs"
description = "调试器 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes/debugger.html](https://doc.rust-lang.org/reference/attributes/debugger.html)

r[attributes.debugger]
# 调试器

下列[属性][attributes]用于在使用 GDB 或 WinDbg 等第三方调试器时增强调试体验。

<!-- template:attributes -->
r[attributes.debugger.debugger_visualizer]
## `debugger_visualizer` 属性

r[attributes.debugger.debugger_visualizer.intro]
*`debugger_visualizer` [属性][attributes]*可将调试器可视化文件嵌入到调试信息中。这会改善显示值时的调试体验。

> [!EXAMPLE]
> <!-- ignore: requires external files-->
> ```rust
> #![debugger_visualizer(natvis_file = "Example.natvis")]
> #![debugger_visualizer(gdb_script_file = "example.py")]
> ```

r[attributes.debugger.debugger_visualizer.syntax]
`debugger_visualizer` 属性使用 [MetaListNameValueStr] 语法指定其输入。必须指定下列键之一：

- [`natvis_file`][attributes.debugger.debugger_visualizer.natvis]
- [`gdb_script_file`][attributes.debugger.debugger_visualizer.gdb]

r[attributes.debugger.debugger_visualizer.allowed-positions]
`debugger_visualizer` 属性只能应用于[模块][module]或 crate 根。

r[attributes.debugger.debugger_visualizer.duplicates]
`debugger_visualizer` 属性可在同一形式上使用任意次数。所有指定的可视化文件都会被加载。

r[attributes.debugger.debugger_visualizer.natvis]
### 将 `debugger_visualizer` 与 Natvis 一起使用

r[attributes.debugger.debugger_visualizer.natvis.intro]
Natvis 是面向 Microsoft 调试器（如 Visual Studio 与 WinDbg）的基于 XML 的框架，使用声明式规则自定义类型的显示方式。关于 Natvis 格式的详细信息，参见 Microsoft 的 [Natvis 文档][Natvis documentation]。

r[attributes.debugger.debugger_visualizer.natvis.msvc]
该属性仅支持在 `-windows-msvc` 目标上嵌入 Natvis 文件。

r[attributes.debugger.debugger_visualizer.natvis.path]
Natvis 文件的路径由 `natvis_file` 键指定，该路径相对于源文件。

> [!EXAMPLE]
> <!-- ignore: requires external files and msvc -->
> ```rust ignore
> #![debugger_visualizer(natvis_file = "Rectangle.natvis")]
>
> struct FancyRect {
>     x: f32,
>     y: f32,
>     dx: f32,
>     dy: f32,
> }
>
> fn main() {
>     let fancy_rect = FancyRect { x: 10.0, y: 10.0, dx: 5.0, dy: 5.0 };
>     println!("set breakpoint here");
> }
> ```
>
> `Rectangle.natvis` 包含：
>
> ```xml
> <?xml version="1.0" encoding="utf-8"?>
> <AutoVisualizer xmlns="http://schemas.microsoft.com/vstudio/debugger/natvis/2010">
>     <Type Name="foo::FancyRect">
>       <DisplayString>({x},{y}) + ({dx}, {dy})</DisplayString>
>       <Expand>
>         <Synthetic Name="LowerLeft">
>           <DisplayString>({x}, {y})</DisplayString>
>         </Synthetic>
>         <Synthetic Name="UpperLeft">
>           <DisplayString>({x}, {y + dy})</DisplayString>
>         </Synthetic>
>         <Synthetic Name="UpperRight">
>           <DisplayString>({x + dx}, {y + dy})</DisplayString>
>         </Synthetic>
>         <Synthetic Name="LowerRight">
>           <DisplayString>({x + dx}, {y})</DisplayString>
>         </Synthetic>
>       </Expand>
>     </Type>
> </AutoVisualizer>
> ```
>
> 在 WinDbg 下查看时，`fancy_rect` 变量将显示如下：
>
> ```text
> > Variables:
>   > fancy_rect: (10.0, 10.0) + (5.0, 5.0)
>     > LowerLeft: (10.0, 10.0)
>     > UpperLeft: (10.0, 15.0)
>     > UpperRight: (15.0, 15.0)
>     > LowerRight: (15.0, 10.0)
> ```

r[attributes.debugger.debugger_visualizer.gdb]
### 将 `debugger_visualizer` 与 GDB 一起使用

r[attributes.debugger.debugger_visualizer.gdb.pretty]
GDB 支持使用称为*美化打印机*（pretty printer）的结构化 Python 脚本，描述类型应如何在调试器视图中可视化。关于美化打印机的详细信息，参见 GDB 的[美化打印文档][pretty printing documentation]。

> **注意**
> 在 GDB 下调试二进制文件时，嵌入的美化打印机不会自动加载。
>
> 有两种方式启用嵌入式美化打印机的自动加载：
>
> 1. 启动 GDB 时传入额外参数，将目录或二进制文件显式加入自动加载安全路径：`gdb -iex "add-auto-load-safe-path safe-path path/to/binary" path/to/binary`。更多信息见 GDB 的[自动加载文档][auto-loading documentation]。
> 1. 在 `$HOME/.config/gdb` 下创建名为 `gdbinit` 的文件（若目录尚不存在，可能需要先创建）。向该文件添加以下行：`add-auto-load-safe-path path/to/binary`。

r[attributes.debugger.debugger_visualizer.gdb.path]
这些脚本通过 `gdb_script_file` 键嵌入，该路径相对于源文件。

> [!EXAMPLE]
> <!-- ignore: requires external files -->
> ```rust ignore
> #![debugger_visualizer(gdb_script_file = "printer.py")]
>
> struct Person {
>     name: String,
>     age: i32,
> }
>
> fn main() {
>     let bob = Person { name: String::from("Bob"), age: 10 };
>     println!("set breakpoint here");
> }
> ```
>
> `printer.py` 包含：
>
> ```python
> import gdb
>
> class PersonPrinter:
>     "Print a Person"
>
>     def __init__(self, val):
>         self.val = val
>         self.name = val["name"]
>         self.age = int(val["age"])
>
>     def to_string(self):
>         return "{} is {} years old.".format(self.name, self.age)
>
> def lookup(val):
>     lookup_tag = val.type.tag
>     if lookup_tag is None:
>         return None
>     if "foo::Person" == lookup_tag:
>         return PersonPrinter(val)
>
>     return None
>
> gdb.current_objfile().pretty_printers.append(lookup)
> ```
>
> 当将该 crate 的调试可执行文件传入 GDB[^rust-gdb] 时，`print bob` 将显示：
>
> ```text
> "Bob" is 10 years old.
> ```
>
> [^rust-gdb]: 注意：此处假定你使用的是 `rust-gdb` 脚本，该脚本会为 `String` 等标准库类型配置美化打印机。

[auto-loading documentation]: https://sourceware.org/gdb/onlinedocs/gdb/Auto_002dloading-safe-path.html
[attributes]: ../attributes.md
[Natvis documentation]: https://docs.microsoft.com/en-us/visualstudio/debugger/create-custom-views-of-native-objects
[pretty printing documentation]: https://sourceware.org/gdb/onlinedocs/gdb/Pretty-Printing.html

<!-- template:attributes -->
r[attributes.debugger.collapse_debuginfo]
## `collapse_debuginfo` 属性

r[attributes.debugger.collapse_debuginfo.intro]
*`collapse_debuginfo` [属性][attribute]*控制在为调用该宏的代码生成 debuginfo 时，是否将来自宏定义的代码位置折叠为与宏调用点关联的单一位置。

> [!EXAMPLE]
> ```rust
> #[collapse_debuginfo(yes)]
> macro_rules! example {
>     () => {
>         println!("hello!");
>     };
> }
> ```
>
> 使用调试器时，调用 `example` 宏可能会表现得像在调用一个函数。也就是说，当你单步到调用点时，它可能显示宏调用本身，而不是展开后的代码。

<!-- TODO: I think it would be nice to extend this to explain a little more about why this is useful, and the kinds of scenarios where you would want one vs the other. See https://github.com/rust-lang/rfcs/pull/2117 for some guidance. -->

r[attributes.debugger.collapse_debuginfo.syntax]
`collapse_debuginfo` 属性的语法为：

```grammar,attributes
@root CollapseDebuginfoAttribute -> `collapse_debuginfo` `(` CollapseDebuginfoOption `)`

CollapseDebuginfoOption ->
      `yes`
    | `no`
    | `external`
```

r[attributes.debugger.collapse_debuginfo.allowed-positions]
`collapse_debuginfo` 属性只能应用于 [`macro_rules` 定义][`macro_rules` definition]。

r[attributes.debugger.collapse_debuginfo.duplicates]
`collapse_debuginfo` 属性在同一宏上只能使用一次。

r[attributes.debugger.collapse_debuginfo.options]
`collapse_debuginfo` 属性接受以下选项：

- `#[collapse_debuginfo(yes)]` —— 在 debuginfo 中折叠代码位置。
- `#[collapse_debuginfo(no)]` —— 在 debuginfo 中不折叠代码位置。
- `#[collapse_debuginfo(external)]` —— 仅当宏来自其他 crate 时，才在 debuginfo 中折叠代码位置。

r[attributes.debugger.collapse_debuginfo.default]
对于没有该属性的宏，默认行为为 `external`，除非它们是内置宏。对于内置宏，默认值为 `yes`。

> **注意**
> `rustc` 有一个 [`-C collapse-macro-debuginfo`] CLI 选项，可覆盖默认行为以及任何 `#[collapse_debuginfo]` 属性的值。

[`-C collapse-macro-debuginfo`]: ../../rustc/codegen-options/index.html#collapse-macro-debuginfo
[`macro_rules` definition]: ../macros-by-example.md
[attribute]: ../attributes.md
[module]: ../items/modules.md
