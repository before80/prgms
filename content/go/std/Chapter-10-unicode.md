+++
title = "第10章：字符是怎么存储的——Unicode 和 Unicode/UTF8"
weight = 100
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第10章：字符是怎么存储的——Unicode 和 Unicode/UTF8

> *"程序员的三大错觉：1. 字符串长度就是字符数；2. 一个字符就是一个字节；3. emoji 不过是彩色的 ASCII。"*
> 
> 本章将无情粉碎你的第三大错觉，顺便让你认清前两个。

---

## 10.1 Unicode/UTF8 包解决什么问题：程序不只处理英文字母，还要处理中文、日文、emoji

想象一下，你的程序只认识英文字母。它看到 `Hello` 会很开心，看到 `你好` 就傻眼了——"这是什么鬼符号？"

这就是 Unicode 要解决的问题：**给世界上所有字符分配一个唯一编号**，无论它是英文、汉字、日文假名，还是那个让你在群里社死的 😂。

而 UTF-8 则是**把这个编号存储到计算机里的方式**。Go 语言从诞生之日起就选择 UTF-8 作为字符串的编码方式，这是一个让很多语言羡慕嫉妒恨的决定。

**专业词汇解释：**

- **Unicode**：国际标准化组织（ISO）制定的一套字符集，为世界上每一种文字系统中的每一个字符分配唯一的编号（码点）。
- **UTF-8**：一种变长编码格式，用 1 到 4 个字节来存储 Unicode 码点。ASCII 字符用 1 字节，汉字用 3 字节，emoji 用 4 字节。
- **码点（Code Point）**：Unicode 中每个字符的唯一标识，格式为 `U+XXXX`，如 `U+0041` 代表字母 A。

```go
package main

import "fmt"

func main() {
    // Go 字符串默认是 UTF-8 编码
    s := "Hello 你好 👋"
    fmt.Println("字符串内容：", s)
    // 打印结果：字符串内容： Hello 你好 👋
    
    // 字节长度 vs 字符长度
    fmt.Println("字节长度：", len(s))
    // 打印结果：字节长度： 16（emoji 占用 4 字节，中文每个占用 3 字节）
    
    // 按字符遍历
    count := 0
    for range s {
        count++
    }
    fmt.Println("字符数量：", count)
    // 打印结果：字符数量： 9
}
```

---

## 10.2 Unicode/UTF8 核心原理：Go 字符串是 UTF-8 编码的字节序列，变长 1~4 字节

在 Go 的世界里，字符串是一个**只读的字节切片**。每个字符（rune）可能占用 1 到 4 个字节——这就是为什么你不能简单地用 `len(s)` 来获取"字符数"。

```go
package main

import "fmt"

func main() {
    // 1 字节字符（ASCII）
    a := "A"
    fmt.Printf("'A' -> 字节数：%d, 字节内容：%v\n", len(a), []byte(a))
    // 打印结果：'A' -> 字节数：1, 字节内容：[65]
    
    // 2 字节字符（部分欧洲文字，如é）
    e := "é"
    fmt.Printf("'é' -> 字节数：%d, 字节内容：%v\n", len(e), []byte(e))
    // 打印结果：'é' -> 字节数：2, 字节内容：[195 169]
    
    // 3 字节字符（汉字）
    z := "中"
    fmt.Printf("'中' -> 字节数：%d, 字节内容：%v\n", len(z), []byte(z))
    // 打印结果：'中' -> 字节数：3, 字节内容：[228 184 173]
    
    // 4 字节字符（emoji）
    emoji := "😀"
    fmt.Printf("'😀' -> 字节数：%d, 字节内容：%v\n", len(emoji), []byte(emoji))
    // 打印结果：'😀' -> 字节数：4, 字节内容：[240 159 152 128]
}
```

```
┌─────────────────────────────────────────────────────────────┐
│                    UTF-8 编码长度规则                         │
├─────────┬───────────────┬───────────────────────────────────┤
│ 字节数  │ 首字节格式     │ 有效码点范围                       │
├─────────┼───────────────┼───────────────────────────────────┤
│ 1 字节  │ 0xxxxxxx      │ U+0000 ~ U+007F (ASCII)           │
│ 2 字节  │ 110xxxxx      │ U+0080 ~ U+07FF                   │
│ 3 字节  │ 1110xxxx      │ U+0800 ~ U+FFFF                   │
│ 4 字节  │ 11110xxx      │ U+10000 ~ U+10FFFF                │
└─────────┴───────────────┴───────────────────────────────────┘
```

**专业词汇解释：**

- **字节切片（Byte Slice）**：`[]byte`，Go 中表示一段原始二进制数据。
- **符文（Rune）**：`int32` 的别名，代表一个 Unicode 码点。

---

## 10.3 Unicode 基础：U+4E2D 代表汉字"中"，U+0041 代表"A"，U+1F600 代表"😀"

Unicode 码点就像是字符的**身份证号**。`U+4E2D` 就是汉字"中"的身份证号，`U+1F600` 是 emoji "😀"的身份证号。

记住这个规律：Unicode 码点范围从 `U+0000` 到 `U+10FFFF`，涵盖了人类所有文字符号。

```go
package main

import "fmt"

func main() {
    // 获取字符的 Unicode 码点
    fmt.Printf("'A' 的码点：U+%04X\n", 'A')
    // 打印结果：'A' 的码点：U+0041
    
    fmt.Printf("'中' 的码点：U+%04X\n", '中')
    // 打印结果：'中' 的码点：U+4E2D
    
    fmt.Printf("'😀' 的码点：U+%04X\n", '😀')
    // 打印结果：'😀' 的码点：U+1F600
    
    // 从码点反向查询
    // U+0041 = 65 (字符 'A')
    fmt.Printf("U+0041 对应的字符：%c\n", 0x0041)
    // 打印结果：U+0041 对应的字符：A
    
    // U+4E2D = 20013 (汉字"中")
    fmt.Printf("U+4E2D 对应的字符：%c\n", 0x4E2D)
    // 打印结果：U+4E2D 对应的字符：中
    
    // U+1F600 = 128512 (emoji "😀")
    fmt.Printf("U+1F600 对应的字符：%c\n", 0x1F600)
    // 打印结果：U+1F600 对应的字符：😀
}
```

---

## 10.4 UTF-8 编码原理：0xxxxxxx（1字节）、110xxxxx 10xxxxxx（2字节）、1110xxxx 10xxxxxx 10xxxxxx（3字节）、11110xxx 10xxxxxx 10xxxxxx 10xxxxxx（4字节）

UTF-8 的设计堪称**优雅与效率的完美结合**：

1. **兼容 ASCII**：ASCII 字符（0-127）保持单字节存储，高位为 0
2. **自同步**：任何字符的首字节都能让你知道它需要多少字节
3. **无歧义**：后续字节都以 `10` 开头，不会与首字节混淆

```go
package main

import "fmt"

func main() {
    // 演示不同字节数字符的二进制结构
    demonstrate := func(s string, desc string) {
        fmt.Printf("\n%s '%s':\n", desc, s)
        fmt.Printf("  字节数：%d\n", len(s))
        fmt.Printf("  字节内容（十六进制）：")
        for _, b := range []byte(s) {
            fmt.Printf("%02X ", b)
        }
        fmt.Printf("\n  字节内容（二进制）：")
        for _, b := range []byte(s) {
            fmt.Printf("%08b ", b)
        }
        fmt.Printf("\n")
    }
    
    demonstrate("A", "1字节字符（ASCII）")
    // 字节内容（二进制）：01000001 
    // 规则：0xxxxxxx
    
    demonstrate("é", "2字节字符")
    // 字节内容（二进制）：11000011 10101001
    // 规则：110xxxxx 10xxxxxx
    
    demonstrate("中", "3字节字符（汉字）")
    // 字节内容（二进制）：11100100 10111000 10101101
    // 规则：1110xxxx 10xxxxxx 10xxxxxx
    
    demonstrate("😀", "4字节字符（emoji）")
    // 字节内容（二进制）：11110000 10011111 10011000 10000000
    // 规则：11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
}
```

```
┌──────────────────────────────────────────────────────────────────┐
│                      UTF-8 编码规则图解                            │
├──────┬──────────────────────────────────────────────────────────┤
│ 1字节 │ 0xxxxxxx                                                 │
│      │ ↑                                                         │
│      │ 固定0，表示单字节                                          │
├──────┼──────────────────────────────────────────────────────────┤
│ 2字节 │ 110xxxxx 10xxxxxx                                        │
│      │ ↑↑                                                        │
│      │ 11表示需要2字节，10表示是后续字节                          │
├──────┼──────────────────────────────────────────────────────────┤
│ 3字节 │ 1110xxxx 10xxxxxx 10xxxxxx                               │
│      │ ↑↑↑                                                       │
│      │ 111表示需要3字节，后两个10是后续字节                       │
├──────┼──────────────────────────────────────────────────────────┤
│ 4字节 │ 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx                      │
│      │ ↑↑↑↑                                                      │
│      │ 1111表示需要4字节，后三个10是后续字节                      │
└──────┴──────────────────────────────────────────────────────────┘
```

**专业词汇解释：**

- **自同步（Self-Synchronizing）**：UTF-8 的一个优良特性，任何字符的起始字节都是唯一的，不会出现在其他字符的后续字节中。
- **首字节（Leading Byte）**：字符编码的第一个字节，决定了字符占用多少字节。
- **后续字节（Continuation Byte）**：字符编码的第 2、3、4 个字节，格式固定为 `10xxxxxx`。

---

## 10.5 UTF-16 代理对：为什么需要、UTF-16 用 2 字节，超过 65535 的字符需要代理对

UTF-16 曾经是 Windows、Java 和 JavaScript 的心头好——它用 2 字节表示所有字符。但这有个致命问题：**2 字节只能表示 65536 个字符**，而 Unicode 有超过 100 万个字符！

解决方案就是**代理对（Surrogate Pair）**：用一对 2 字节的值来表示一个超出 BMP（基本多文种平面）的字符。

```go
package main

import "fmt"

func main() {
    // 在 Go 中处理 UTF-16（需要编码转换）
    // 注意：Go 原生字符串是 UTF-8，不是 UTF-16
    
    // UTF-16 代理对原理
    // emoji "😀" 的码点是 U+1F600
    // 它超出了 BMP (U+0000 ~ U+FFFF)，需要用代理对表示
    
    // 代理对计算公式：
    // 高代理 = 0xD800 + ((codePoint - 0x10000) >> 10)
    // 低代理 = 0xDC00 + ((codePoint - 0x10000) & 0x3FF)
    
    emoji := '😀'
    codePoint := uint32(emoji)
    
    highSurrogate := 0xD800 + ((codePoint-0x10000)>>10)
    lowSurrogate := 0xDC00 + ((codePoint-0x10000)&0x3FF)
    
    fmt.Printf("emoji '😀' 码点：U+%X\n", codePoint)
    // 打印结果：emoji '😀' 码点：U+1F600
    
    fmt.Printf("UTF-16 代理对：高代理 U+%X，低代理 U+%X\n", highSurrogate, lowSurrogate)
    // 打印结果：UTF-16 代理对：高代理 U+D83D，低代理 U+DE00
    
    // 在 UTF-16 中，"😀" 表示为两个字节：[D83D DE00]
    // 而在 UTF-8 中，同一个字符表示为四个字节：[F0 9F 98 80]
}
```

```
┌─────────────────────────────────────────────────────────────┐
│              Unicode 平面与 UTF-16 代理对关系                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BMP (基本多文种平面)                                         │
│  U+0000 ~ U+FFFF                                            │
│  ├─ ASCII: U+0000 ~ U+007F (0xxxxxxx)                       │
│  ├─ 中文: U+4E00 ~ U+9FFF                                   │
│  └─ 代理对范围: U+D800 ~ U+DFFF (保留给代理对!)              │
│                                                             │
│  补充平面 (SMP)                                              │
│  U+10000 ~ U+1FFFF                                          │
│  └─ emoji、一些古文字等                                     │
│     需要用 UTF-16 代理对表示                                  │
│                                                             │
│  编码对比:                                                   │
│  ┌─────────┬──────────┬──────────┐                          │
│  │  字符   │  UTF-8   │  UTF-16  │                          │
│  ├─────────┼──────────┼──────────┤                          │
│  │  'A'   │   41     │   0041   │                          │
│  │  '中'  │ E4B8AD   │   4E2D   │                          │
│  │  '😀'  │ F09F9880 │ D83DDE00 │ ← 代理对！               │
│  └─────────┴──────────┴──────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

**专业词汇解释：**

- **BMP（Basic Multilingual Plane）**：Unicode 的基本多文种平面，U+0000 到 U+FFFF，包含世界上大部分常用字符。
- **代理对（Surrogate Pair）**：UTF-16 用于表示超出 BMP 范围字符的特殊机制，使用 U+D800-U+DFFF 这个保留范围来编码。
- **SMP（Supplementary Multilingual Plane）**：Unicode 补充多文种平面，U+10000 到 U+1FFFF，包含 emoji、历史文字等。

---

## 10.6 Unicode 包：字符分类与判断

`unicode` 包是 Go 标准库的**瑞士军刀**，专门用于 Unicode 字符的分类、转换和判断。无论你是想判断一个字符是数字、字母还是标点，这个包都能帮你搞定。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    // unicode 包的核心功能：字符分类
    // 这些函数都接受一个 rune（Unicode 码点）作为参数
    
    testChar := func(r rune, name string) {
        fmt.Printf("\n字符 '%c' (U+%04X):\n", r, r)
        fmt.Printf("  IsDigit:  %v (是数字?)\n", unicode.IsDigit(r))
        fmt.Printf("  IsLetter: %v (是字母?)\n", unicode.IsLetter(r))
        fmt.Printf("  IsUpper:  %v (是大写?)\n", unicode.IsUpper(r))
        fmt.Printf("  IsLower:  %v (是小写?)\n", unicode.IsLower(r))
        fmt.Printf("  IsSpace:  %v (是空格?)\n", unicode.IsSpace(r))
        fmt.Printf("  IsPunct:  %v (是标点?)\n", unicode.IsPunct(r))
        fmt.Printf("  IsPrint:  %v (可打印?)\n", unicode.IsPrint(r))
        fmt.Printf("  IsControl:%v (控制字符?)\n", unicode.IsControl(r))
    }
    
    testChar('7', "数字")
    // 打印结果：IsDigit: true, IsLetter: false, ...
    
    testChar('A', "大写字母")
    // 打印结果：IsDigit: false, IsLetter: true, IsUpper: true, ...
    
    testChar('a', "小写字母")
    // 打印结果：IsDigit: false, IsLetter: true, IsUpper: false, IsLower: true, ...
    
    testChar('中', "汉字")
    // 打印结果：IsDigit: false, IsLetter: true, IsUpper: false, IsLower: false, ...
    
    testChar(' ', "空格")
    // 打印结果：IsSpace: true, ...
    
    testChar('😂', "emoji")
    // 打印结果：IsLetter: false, IsDigit: false, IsPunct: false, ...
}
```

**专业词汇解释：**

- **字符分类（Character Classification）**：根据 Unicode 标准，将字符划分为不同类别，如数字（Nd）、字母（Ll）、标点（P）等。
- **码点（Code Point）**：Unicode 中每个字符的唯一标识，即 `rune` 类型。

---

## 10.7 unicode.IsDigit：是否是数字

`IsDigit` 函数用于判断一个字符是否是**十进制数字**（Unicode 类别 Nd）。它不仅能识别 `0-9`，还能识别中文数字 `〇一二三`、阿拉伯数字 `١٢٣` 等各种Unicode 数字。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    // 测试各种"数字"
    chars := []rune{
        '0',        // ASCII 数字
        '9',
        '①',        // 上标数字
        '½',        // 分数（不是数字！）
        '七',        // 中文数字
        '〇',        // 中文零
        '١',        // 阿拉伯数字
    }
    
    fmt.Println("=== IsDigit 测试 ===")
    for _, c := range chars {
        fmt.Printf("'%c' (U+%04X): IsDigit = %v\n", c, c, unicode.IsDigit(c))
    }
    
    // 打印结果分析：
    // '0': IsDigit = true（ASCII 数字）
    // '9': IsDigit = true
    // '①': IsDigit = true（上标数字）
    // '½': IsDigit = false（分数不是数字，是数字符号）
    // '七': IsDigit = true（中文数字）
    // '〇': IsDigit = true（中文零）
    // '١': IsDigit = true（阿拉伯数字）
}
```

**专业词汇解释：**

- **Unicode 类别 Nd（Decimal Number）**：十进制数字字符，包括各种文字中的数字形式。
- **数字符号（Number Symbol）**：如分数 `½`、数字运算符，它们不是数字字符。

---

## 10.8 unicode.IsLetter：是否是字母

`IsLetter` 函数用于判断一个字符是否是**字母**。这里的"字母"定义比较宽泛，涵盖了各种文字系统的字母、汉字、日文假名等。简单来说，只要你认为它是"文字"，它大概率就是 `true`。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []rune{
        'A',        // 英文字母
        'a',
        '中',        // 汉字
        'あ',        // 日文平假名
        'ア',        // 日文片假名
        'α',        // 希腊字母
        '①',        // 上标数字（不是字母！）
        ' ',        // 空格（不是字母！）
        '_',        // 下划线（不是字母！）
    }
    
    fmt.Println("=== IsLetter 测试 ===")
    for _, c := range chars {
        fmt.Printf("'%c' (U+%04X): IsLetter = %v\n", c, c, unicode.IsLetter(c))
    }
    
    // 打印结果：
    // 'A': IsLetter = true
    // 'a': IsLetter = true
    // '中': IsLetter = true
    // 'あ': IsLetter = true
    // 'ア': IsLetter = true
    // 'α': IsLetter = true
    // '①': IsLetter = false
    // ' ': IsLetter = false
    // '_': IsLetter = false
}
```

---

## 10.9 unicode.IsUpper、unicode.IsLower：是否是大写/小写字母

这两个函数专门用于判断**拉丁字母**的大小写。它们只对有大小写之分的字符返回 `true`，对中文、日文等没有大小写概念的文字，返回 `false`。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []rune{
        'A',        // 大写英文字母
        'a',        // 小写英文字母
        'Z',
        'z',
        '中',        // 汉字（无大小写）
        'α',        // 希腊字母（有小写）
        'Α',        // 希腊字母（大写）
        '①',        // 数字（无大小写）
    }
    
    fmt.Println("=== IsUpper / IsLower 测试 ===")
    for _, c := range chars {
        fmt.Printf("'%c' (U+%04X): IsUpper = %-5v IsLower = %v\n", 
            c, c, unicode.IsUpper(c), unicode.IsLower(c))
    }
    
    // 打印结果：
    // 'A': IsUpper = true   IsLower = false
    // 'a': IsUpper = false  IsLower = true
    // 'Z': IsUpper = true   IsLower = false
    // 'z': IsUpper = false  IsLower = true
    // '中': IsUpper = false IsLower = false
    // 'α': IsUpper = false IsLower = true
    // 'Α': IsUpper = true   IsLower = false
    // '①': IsUpper = false IsLower = false
}
```

---

## 10.10 unicode.IsSpace：哪些字符算空格

`IsSpace` 函数会识别所有 Unicode 中的**空白字符**，不仅仅是常见的空格键产生的空格，还包括 Tab、换行、回车以及各种语言中的特殊空白字符。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []struct {
        r    rune
        name string
    }{
        {' ', "普通空格",},
        {'\t', "Tab制表符",},
        {'\n', "换行符",},
        {'\r', "回车符",},
        {'\u00A0', "不间断空格（NBSP）",},
        {'\u3000', "全角空格（日文）",},
        {'　', "中文全角空格",},
        {'\v', "垂直制表符",},
        {'\f', "换页符",},
    }
    
    fmt.Println("=== IsSpace 测试 ===")
    for _, item := range chars {
        fmt.Printf("%s '%c' (U+%04X): IsSpace = %v\n", 
            item.name, item.r, item.r, unicode.IsSpace(item.r))
    }
    
    // 打印结果：
    // 普通空格 ' ': IsSpace = true
    // Tab制表符: IsSpace = true
    // 换行符: IsSpace = true
    // 回车符: IsSpace = true
    // 不间断空格: IsSpace = true
    // 全角空格: IsSpace = true
    // 中文全角空格: IsSpace = true
    // 垂直制表符: IsSpace = true
    // 换页符: IsSpace = true
}
```

**专业词汇解释：**

- **NBSP（No-Break Space）**：`U+00A0`，不间断空格，用于防止行首出现孤立字符。
- **全角空格（Ideographic Space）**：`U+3000`，宽度等于一个汉字的空格，常见于日文排版。

---

## 10.11 unicode.IsControl：是否是控制字符

控制字符是那些**不显示在屏幕上，但对文本处理有特殊意义**的字符。比如换行符 `\n`、回车符 `\r`、Tab `\t` 等。`IsControl` 函数帮助你识别它们。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []struct {
        r    rune
        name string
    }{
        {'\n', "换行符 LF"},
        {'\r', "回车符 CR"},
        {'\t', "Tab制表符"},
        {'\0', "空字符 NUL"},
        {' ', "普通空格（不是控制字符！）"},
        {'a', "字母 'a'（不是控制字符！）"},
        {'中', "汉字（不是控制字符！）"},
        {'\x1B', "ESC 转义符"},
        {'\a', "响铃符 BEL"},
    }
    
    fmt.Println("=== IsControl 测试 ===")
    for _, item := range chars {
        fmt.Printf("%s (U+%04X): IsControl = %v\n", 
            item.name, item.r, unicode.IsControl(item.r))
    }
    
    // 打印结果：
    // 换行符 LF (U+000A): IsControl = true
    // 回车符 CR (U+000D): IsControl = true
    // Tab制表符 (U+0009): IsControl = true
    // 空字符 NUL (U+0000): IsControl = true
    // 普通空格: IsControl = false ← 空格是图形字符！
    // 字母 'a': IsControl = false
    // 汉字: IsControl = false
    // ESC 转义符 (U+001B): IsControl = true
    // 响铃符 BEL (U+0007): IsControl = true
}
```

**专业词汇解释：**

- **控制字符（Control Character）**：Unicode 类别 Cc（Control），包括 ASCII 控制字符（0-31 和 127），用于控制设备或文本格式。
- **图形字符（Graphic Character）**：包括字母、数字、标点、符号、空格等可见或可打印的字符。

---

## 10.12 unicode.IsPrint：是否是可打印字符

`IsPrint` 函数判断一个字符是否是**可打印字符**。可打印字符包括字母、数字、标点、符号和空格。不可打印的包括控制字符和尚未分配的码点。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []struct {
        r    rune
        name string
    }{
        {' ', "空格",},
        {'a', "字母",},
        {'中', "汉字",},
        {'!', "标点",},
        {'\n', "换行符",},
        {'\t', "Tab",},
        {'\x00', "空字符",},
        {'\uFFFD', "替换字符（显示为�）",},
    }
    
    fmt.Println("=== IsPrint 测试 ===")
    for _, item := range chars {
        fmt.Printf("%s (U+%04X): IsPrint = %v\n", 
            item.name, item.r, unicode.IsPrint(item.r))
    }
    
    // 打印结果：
    // 空格: IsPrint = true
    // 字母: IsPrint = true
    // 汉字: IsPrint = true
    // 标点: IsPrint = true
    // 换行符: IsPrint = false
    // Tab: IsPrint = false
    // 空字符: IsPrint = false
    // 替换字符: IsPrint = true（虽然显示为�，但它是合法字符）
}
```

---

## 10.13 unicode.IsPunct：是否是标点符号

`IsPunct` 函数用于判断一个字符是否是**标点符号**。这里的标点包括常见的英文标点（如 `!?,.`）以及各种语言中的引号、括号、连接号等。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []rune{
        '.', ',', '!', '?', ';', ':', "'", '"',
        '(', ')', '[', ']', '{', '}',
        '-', '—', '…', '《', '》', '「', '」',
        '/', '\\', '@', '#', '$', '%', '&',
        '中', 'a', '1', ' ', '\n',
    }
    
    fmt.Println("=== IsPunct 测试 ===")
    for _, c := range chars {
        fmt.Printf("'%c' (U+%04X): IsPunct = %v\n", c, c, unicode.IsPunct(c))
    }
    
    // 打印结果：
    // '.': IsPunct = true
    // ',': IsPunct = true
    // '!': IsPunct = true
    // '《': IsPunct = true（中文书名号）
    // '「': IsPunct = true（中文引号）
    // '/': IsPunct = true
    // '@': IsPunct = true
    // '中': IsPunct = false（汉字不是标点）
    // 'a': IsPunct = false（字母不是标点）
    // '1': IsPunct = false（数字不是标点）
    // ' ': IsPunct = false（空格不是标点）
    // '\n': IsPunct = false（换行符不是标点）
}
```

---

## 10.14 unicode.ToUpper、unicode.ToLower：大小写转换

这两个函数用于**拉丁字母的大小写转换**。对于没有大小写概念的文字（如中文），它们会返回原字符不变。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []rune{
        'a', 'z', 'A', 'Z',
        'ö',    // 德语字母
        'α',    // 希腊字母
        '中',    // 汉字
        '1',    // 数字
    }
    
    fmt.Println("=== 大小写转换测试 ===")
    for _, c := range chars {
        upper := unicode.ToUpper(c)
        lower := unicode.ToLower(c)
        fmt.Printf("'%c' (U+%04X) → ToUpper: '%c', ToLower: '%c'\n", 
            c, c, upper, lower)
    }
    
    // 打印结果：
    // 'a' → ToUpper: 'A', ToLower: 'a'
    // 'z' → ToUpper: 'Z', ToLower: 'z'
    // 'A' → ToUpper: 'A', ToLower: 'a'
    // 'Z' → ToUpper: 'Z', ToLower: 'z'
    // 'ö' → ToUpper: 'Ö', ToLower: 'ö'（德语特殊字母转换）
    // 'α' → ToUpper: 'Α', ToLower: 'α'（希腊字母转换）
    // '中' → ToUpper: '中', ToLower: '中'（汉字不变）
    // '1' → ToUpper: '1', ToLower: '1'（数字不变）
}
```

---

## 10.15 unicode.ToTitle：转换为首字母大写

`ToTitle` 函数将字符转换为**标题形式**。对于拉丁字母，这通常与大写形式相同；但对于某些特殊字母，标题形式可能与大写不同。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    chars := []rune{
        'a', 'h', 'o',
        'ß',        // 德语 sharp S（ß → SS）
        'ǳ',        // 拉丁字母 Dz 的单字符
        '①',        // 数字
        '中',        // 汉字
    }
    
    fmt.Println("=== ToTitle 测试 ===")
    fmt.Println("字符      ToUpper   ToTitle")
    for _, c := range chars {
        upper := unicode.ToUpper(c)
        title := unicode.ToTitle(c)
        fmt.Printf("'%c' (U+%04X)   '%c'      '%c'\n", c, c, upper, title)
    }
    
    // 打印结果：
    // 'a' (U+0061)   'A'      'A'
    // 'h' (U+0068)   'H'      'H'
    // 'o' (U+006F)   'O'      'O'
    // 'ß' (U+00DF)   'S'      'S'（大写/标题都变成 S）
    // 'ǳ' (U+01F3)   'Ǳ'      'ǲ'（标题形式与大写不同）
    // '①' (U+2460)   '①'      '①'（数字不变）
    // '中' (U+4E2D)   '中'      '中'（汉字不变）
}
```

**专业词汇解释：**

- **标题形式（Title Case）**：主要用于多字母单词的首字母大写形式。在 Unicode 中，某些特殊字母的标题形式可能与普通大写形式不同。

---

## 10.16 unicode.SimpleFold：Unicode 简单折叠

`SimpleFold` 是一个有趣的函数，它返回**与给定字符等价的下一个字符**，用于大小写不敏感的比较。这个"下一个"遵循 Unicode 的简单折叠规则。

```go
package main

import (
    "fmt"
    "unicode"
)

func main() {
    // SimpleFold 返回下一个"折叠"字符
    // 对于 ASCII 字母，它在大小写之间切换
    
    fmt.Println("=== SimpleFold 测试 ===")
    
    // ASCII 字母的折叠路径
    fmt.Printf("'a' 的折叠: '%c'\n", unicode.SimpleFold('a'))
    // 打印结果：'a' 的折叠: 'A'
    fmt.Printf("'A' 的折叠: '%c'\n", unicode.SimpleFold('A'))
    // 打印结果：'A' 的折叠: 'a'
    
    // 多次调用 SimpleFold 会形成一个循环
    fmt.Println("\n'a' 的折叠循环:")
    r := 'a'
    for i := 0; i < 10; i++ {
        fmt.Printf("  %d: '%c' (U+%04X)\n", i, r, r)
        r = unicode.SimpleFold(r)
    }
    
    // 打印结果：a → A → a → A → ...（在两个字符之间循环）
    
    // 德语 ß 的折叠
    fmt.Println("\n'ß' 的折叠循环:")
    r = 'ß'
    for i := 0; i < 5; i++ {
        fmt.Printf("  %d: '%c' (U+%04X)\n", i, r, r)
        r = unicode.SimpleFold(r)
    }
    // 打印结果：ß → S → s → ß（形成3个字符的循环）
}
```

**专业词汇解释：**

- **Unicode 折叠（Unicode Folding）**：大小写不敏感比较时使用的字符映射规则。`SimpleFold` 按照 Unicode 标准定义的顺序遍历这些等价字符。

---

## 10.17 unicode/utf8.DecodeRune：把 UTF-8 字节序列解码成 Unicode 码点

`utf8.DecodeRune` 是将 UTF-8 字节序列**转换为人话（Unicode 码点）**的函数。它接收一个字节切片的前 1~4 个字节，并返回对应的 rune 值和实际消费的字节数。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    // DecodeRune 接收 []byte，返回 (rune, int)
    // 第二个返回值表示消费了多少字节
    
    tests := [][]byte{
        []byte{'A'},                   // 1 字节 ASCII
        []byte("中"),                  // 3 字节汉字
        []byte("😀"),                  // 4 字节 emoji
        []byte("Hello"),               // 混合
    }
    
    fmt.Println("=== DecodeRune 测试 ===")
    for _, data := range tests {
        if len(data) == 0 {
            continue
        }
        r, size := utf8.DecodeRune(data)
        fmt.Printf("字节: %v (% X) → 字符: '%c' (U+%04X), 占用 %d 字节\n", 
            data, data, r, r, size)
    }
    
    // 打印结果：
    // 字节: [65] (41) → 字符: 'A' (U+0041), 占用 1 字节
    // 字节: [228 184 173] (E4 B8 AD) → 字符: '中' (U+4E2D), 占用 3 字节
    // 字节: [240 159 152 128] (F0 9F 98 80) → 字符: '😀' (U+1F600), 占用 4 字节
    // 字节: [72 101 108 108 111] → 字符: 'H' (U+0048), 占用 1 字节
    
    // 部分字节序列
    fmt.Println("\n=== 不完整字节序列 ===")
    partial := []byte{0xE4} // "中" 的首字节（不完整）
    r, size := utf8.DecodeRune(partial)
    fmt.Printf("不完整序列 [% X]: rune='%c' (U+%X), size=%d\n", 
        partial, r, r, size)
    // 打印结果：不完整序列 [E4]: rune='?' (U+FFFD), size=1
    // 当输入不完整时，返回替换字符 U+FFFD
}
```

**专业词汇解释：**

- **替换字符（Replacement Character）**：`U+FFFD`，通常显示为 `�`，用于表示无法解码的字节序列。
- **解码（Decode）**：将二进制数据（字节）转换为更高层次的表示（码点）。

---

## 10.18 unicode/utf8.EncodeRune：把 Unicode 码点编码成 UTF-8 字节序列

`EncodeRune` 是 `DecodeRune` 的逆操作：接收一个 Unicode 码点（rune），返回其 UTF-8 编码的字节序列。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    runes := []rune{
        'A',        // U+0041
        '中',       // U+4E2D
        '😀',       // U+1F600
        0x80,       // U+0080（第一个非 ASCII 字符）
        0xFFFF,     // U+FFFF（BMP 最后一个字符）
    }
    
    fmt.Println("=== EncodeRune 测试 ===")
    for _, r := range runes {
        var buf [utf8.UTFMax]byte
        n := utf8.EncodeRune(buf[:], r)
        fmt.Printf("U+%04X '%c' → % X (占用 %d 字节)\n", r, r, buf[:n], n)
    }
    
    // 打印结果：
    // U+0041 'A' → [41] (占用 1 字节)
    // U+4E2D '中' → [E4 B8 AD] (占用 3 字节)
    // U+1F600 '😀' → [F0 9F 98 80] (占用 4 字节)
    // U+0080 → [C2 80] (占用 2 字节)
    // U+FFFF → [EF BF BF] (占用 3 字节)
    
    // EncodeRune 会截断超出 UTFMax 的部分
    fmt.Println("\n=== 超出有效码点范围 ===")
    invalid := rune(0x110000) // 超出 Unicode 范围（最大 U+10FFFF）
    var buf [utf8.UTFMax]byte
    n := utf8.EncodeRune(buf[:], invalid)
    fmt.Printf("U+%X → % X (占用 %d 字节)\n", invalid, buf[:n], n)
    // 打印结果：U+110000 → [EF BF BD] (替换字符！)
}
```

---

## 10.19 unicode/utf8.RuneCountInString：按字符计算字符串长度

这是一个**拯救无数新手程序员**的函数。当你 `len("你好")` 得到 6 而不是 2 而抓狂时，`RuneCountInString` 就是你的救星。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    strings := []string{
        "Hello",
        "你好",
        "Hello 你好",
        "😀😂😜",
        "a中b英c文d",
    }
    
    fmt.Println("=== RuneCountInString 测试 ===")
    for _, s := range strings {
        byteLen := len(s)
        runeCount := utf8.RuneCountInString(s)
        fmt.Printf("%q: 字节长度=%d, 字符数量=%d\n", s, byteLen, runeCount)
    }
    
    // 打印结果：
    // "Hello": 字节长度=5, 字符数量=5
    // "你好": 字节长度=6, 字符数量=2
    // "Hello 你好": 字节长度=12, 字符数量=8
    // "😀😂😜": 字节长度=12, 字符数量=3
    // "a中b英c文d": 字节长度=13, 字符数量=7
    
    // 手动遍历对比
    fmt.Println("\n=== 手动遍历 vs RuneCountInString ===")
    s := "a中b"
    count := 0
    for range s {
        count++
    }
    fmt.Printf("手动遍历 count=%d, RuneCountInString=%d\n", 
        count, utf8.RuneCountInString(s))
}
```

---

## 10.20 unicode/utf8.Valid、unicode/utf8.ValidString：验证是否是合法 UTF-8

当你从网络、文件或用户输入获取数据时，最好验证一下它是不是合法的 UTF-8。`Valid` 和 `ValidString` 就是你的**UTF-8 质检员**。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    // ValidString 接收字符串，返回是否合法
    tests := []string{
        "Hello",
        "你好",
        "😀",
        "a\xffb",         // 包含非法字节 FF
        "a\xc0\x80b",     // 包含非规范字节序列
        string([]byte{0xF0, 0x9F, 0x98}), // 不完整的 emoji
    }
    
    fmt.Println("=== ValidString 测试 ===")
    for _, s := range tests {
        valid := utf8.ValidString(s)
        fmt.Printf("%q: 合法=%v\n", s, valid)
    }
    
    // 打印结果：
    // "Hello": 合法=true
    // "你好": 合法=true
    // "😀": 合法=true
    // "a\xffb": 合法=false（非法字节）
    // "a\xc0\x80b": 合法=false（非规范编码）
    // "a\xe2\x98": 合法=false（不完整序列）
    
    // Valid 接收字节切片
    fmt.Println("\n=== Valid 测试（字节切片）===")
    valid := utf8.Valid([]byte("Hello"))
    fmt.Printf("[]byte(\"Hello\"): 合法=%v\n", valid)
    
    invalid := []byte{0x80} // 孤立的延续字节
    valid = utf8.Valid(invalid)
    fmt.Printf("[]byte{0x80}: 合法=%v\n", valid)
}
```

**专业词汇解释：**

- **合法 UTF-8（Valid UTF-8）**：符合 UTF-8 编码规范的字节序列，包括正确的字节长度、首字节格式和后续字节格式。
- **非规范编码（Non-Canonical Encoding）**：虽然能解码出正确的字符，但不符合 UTF-8 的最优编码规则，如 `0xC0 0x80` 解码为 U+0000（应该用 `0x00`）。

---

## 10.21 unicode/utf8.DecodeLastRune、DecodeLastRuneInString：解码最后一个字符

`DecodeLastRune` 和 `DecodeLastRuneInString` 从字符串或字节切片的**末尾**开始解码，返回最后一个完整的 Unicode 码点。这在日志处理、路径解析等场景很有用。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    tests := []string{
        "Hello",
        "你好",
        "😀Hello",
        "a中b英",
        "😀",
        "ab",           // 只有 ASCII
    }
    
    fmt.Println("=== DecodeLastRuneInString 测试 ===")
    for _, s := range tests {
        r, size := utf8.DecodeLastRuneInString(s)
        fmt.Printf("%q: 最后字符='%c' (U+%04X), 占用 %d 字节\n", 
            s, r, r, size)
    }
    
    // 打印结果：
    // "Hello": 最后字符='o' (U+006F), 占用 1 字节
    // "你好": 最后字符='好' (U+597D), 占用 3 字节
    // "😀Hello": 最后字符='o' (U+006F), 占用 1 字节
    // "a中b英": 最后字符='英' (U+82F1), 占用 3 字节
    // "😀": 最后字符='😀' (U+1F600), 占用 4 字节
    // "ab": 最后字符='b' (U+0062), 占用 1 字节
    
    // 字节切片版本
    fmt.Println("\n=== DecodeLastRune 测试（字节切片）===")
    data := []byte("Hello 😀")
    r, size := utf8.DecodeLastRune(data)
    fmt.Printf("最后字符='%c' (U+%04X), 占用 %d 字节\n", r, r, size)
    // 打印结果：最后字符='😀' (U+1F600), 占用 4 字节
}
```

---

## 10.22 unicode/utf8.RuneStart：判断字节是否是 UTF-8 字符的首字节

`RuneStart` 是一个**低调但实用**的函数，它告诉你一个字节是否可能是 UTF-8 字符的首字节。如果你在遍历字节时想知道当前位置是否是一个新字符的起点，这个函数就派上用场了。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    // 测试各种字节值
    bytes := []byte{
        0x00, 0x41, 0x7F,  // ASCII 范围（0x00-0x7F）
        0x80, 0xBF,        // 延续字节范围
        0xC0, 0xC1,        // 非法首字节
        0xC2, 0xDF,        // 2字节首字节范围
        0xE0, 0xEF,        // 3字节首字节范围
        0xF0, 0xF4,        // 4字节首字节范围
        0xF5, 0xFF,        // 非法首字节（超出 Unicode 范围）
    }
    
    fmt.Println("=== RuneStart 测试 ===")
    for _, b := range bytes {
        isStart := utf8.RuneStart(b)
        fmt.Printf("0x%02X (%08b): RuneStart=%v\n", b, b, isStart)
    }
    
    // 打印结果（关键点）：
    // 0x41 (01000001): RuneStart=true  ← ASCII 字符的首字节
    // 0x80 (10000000): RuneStart=false ← 延续字节！
    // 0xBF (10111111): RuneStart=false ← 延续字节！
    // 0xC2 (11000010): RuneStart=true  ← 2字节字符的首字节
    // 0xE0 (11100000): RuneStart=true  ← 3字节字符的首字节
    // 0xF0 (11110000): RuneStart=true  ← 4字节字符的首字节
    // 0xC0 (11000000): RuneStart=true  ← 虽然是首字节格式，但是非法的
    // 0xF5 (11110101): RuneStart=true  ← 虽然是首字节格式，但超出 Unicode 范围
    
    // 实际应用：检查字符串中的字符边界
    fmt.Println("\n=== 实际应用：标记字符边界 ===")
    s := "Hi中😀"
    fmt.Printf("字符串: %q\n", s)
    fmt.Printf("字节位置: ")
    for i, b := range []byte(s) {
        marker := " "
        if utf8.RuneStart(b) {
            marker = "|"
        }
        fmt.Printf("%s%02X", marker, b)
    }
    fmt.Println()
    // 打印结果：|48|69|E4|B8|AD|F0|9F|98|80
    //           ↑      ↑  ↑  ↑  ↑
    //           H      中的首字节      emoji的首字节
}
```

---

## 10.23 遍历字符串的两种方式：for i, b := range []byte(s) vs for i, r := range s

这是 Go 语言中最容易踩坑的地方之一！`range` 遍历字符串时，**索引是字节索引，值是 rune（码点）**；而 `range` 遍历字节切片时，**索引还是字节索引，值是单个字节**。

```go
package main

import "fmt"

func main() {
    s := "Hi中😀"
    
    fmt.Println("=== 遍历字符串（for i, r := range s）===")
    for i, r := range s {
        fmt.Printf("字节索引: %d, 字符: '%c', 码点: U+%04X\n", i, r, r)
    }
    // 打印结果：
    // 字节索引: 0, 字符: 'H', 码点: U+0048
    // 字节索引: 1, 字符: 'i', 码点: U+0069
    // 字节索引: 2, 字符: '中', 码点: U+4E2D
    // 字节索引: 5, 字符: '😀', 码点: U+1F600  ← 注意！索引跳过了"中"的3字节
    
    fmt.Println("\n=== 遍历字节切片（for i, b := range []byte(s)）===")
    for i, b := range []byte(s) {
        fmt.Printf("字节索引: %d, 字节值: 0x%02X ('%c')\n", i, b, b)
    }
    // 打印结果：
    // 字节索引: 0, 字节值: 0x48 ('H')
    // 字节索引: 1, 字节值: 0x69 ('i')
    // 字节索引: 2, 字节值: 0xE4
    // 字节索引: 3, 字节值: 0xB8
    // 字节索引: 4, 字节值: 0xAD
    // 字节索引: 5, 字节值: 0xF0
    // 字节索引: 6, 字节值: 0x9F
    // 字节索引: 7, 字节值: 0x98
    // 字节索引: 8, 字节值: 0x80
    
    // 错误演示：直接用字节索引访问字符串
    fmt.Println("\n=== 危险操作：s[n] 是字节，不是字符 ===")
    fmt.Printf("s[0] = '%c' (正确，是 'H')\n", s[0])
    fmt.Printf("s[2] = 0x%02X (错误！这是'中'的首字节，不是字符)\n", s[2])
    fmt.Printf("s[2:3] = '%c' (正确，用切片截取完整的 UTF-8 字符)\n", s[2])
    // 如果一定要按字节访问后再解码：
    r, _ := utf8.DecodeRune(s[2:])
    fmt.Printf("utf8.DecodeRune(s[2:]) = '%c' (安全解码)\n", r)
}
```

```
┌─────────────────────────────────────────────────────────────┐
│                 字符串遍历方式对比                            │
├──────────────────────┬──────────────────────────────────────┤
│ for i, r := range s  │ for i, b := range []byte(s)          │
├──────────────────────┼──────────────────────────────────────┤
│ i: 字节索引           │ i: 字节索引                           │
│ r: rune (码点)        │ b: byte (单字节)                     │
├──────────────────────┼──────────────────────────────────────┤
│ 自动处理多字节字符     │ 需要手动处理多字节字符                  │
├──────────────────────┼──────────────────────────────────────┤
│ 推荐遍历方式          │ 需要按字节操作时使用                     │
└──────────────────────┴──────────────────────────────────────┘
```

---

## 10.24 字符索引 vs 字节索引：s[3] 可能踩雷

想象一下，你想知道字符串第 3 个字符是什么，然后自信满满地写了 `s[3]`——恭喜你，你可能拿到的是一个 emoji 的中间字节，然后一脸问号地看着输出 `?`。

```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    // 这个字符串的字节布局：
    // H   i   中                       😀
    // 48  69  E4 B8 AD                F0 9F 98 80
    // 0   1   2   3   4               5   6   7   8
    //       ────────────              ────────────────
    //         "中" (3字节)              "😀" (4字节)
    
    s := "Hi中😀"
    
    fmt.Println("=== 字节索引 vs 字符索引 ===")
    fmt.Printf("字符串: %q\n", s)
    fmt.Printf("字节长度: %d, 字符长度: %d\n\n", len(s), utf8.RuneCountInString(s))
    
    fmt.Println("字节布局:")
    for i, b := range []byte(s) {
        fmt.Printf("  [%d] 0x%02X\n", i, b)
    }
    
    fmt.Println("\n=== 危险操作演示 ===")
    fmt.Printf("s[0] = 0x%02X = '%c' (正确，ASCII 'H')\n", s[0], s[0])
    fmt.Printf("s[1] = 0x%02X = '%c' (正确，ASCII 'i')\n", s[1], s[1])
    fmt.Printf("s[2] = 0x%02X (错误！这是'中'的首字节，不是完整字符)\n", s[2])
    fmt.Printf("s[3] = 0x%02X (错误！这是'中'的第二个字节)\n", s[3])
    fmt.Printf("s[4] = 0x%02X (错误！这是'中'的第三个字节)\n", s[4])
    fmt.Printf("s[5] = 0x%02X (正确！'😀'的首字节)\n", s[5])
    
    // 正确做法：用 utf8.DecodeRune 解码
    fmt.Println("\n=== 正确做法 ===")
    // 获取第 N 个字符（0-indexed）
    getNthChar := func(s string, n int) rune {
        for i, r := range s {
            if i == n {
                return r
            }
        }
        return 0
    }
    
    fmt.Printf("第 0 个字符: '%c'\n", getNthChar(s, 0)) // 'H'
    fmt.Printf("第 1 个字符: '%c'\n", getNthChar(s, 1)) // 'i'
    fmt.Printf("第 2 个字符: '%c'\n", getNthChar(s, 2)) // '中'
    fmt.Printf("第 3 个字符: '%c'\n", getNthChar(s, 3)) // '😀'
}
```

**专业词汇解释：**

- **字节索引（Byte Index）**：字符串中每个字节的位置编号，从 0 开始。
- **字符索引（Character Index）**：字符串中每个 Unicode 字符的位置编号，从 0 开始。
- **多字节字符（Multi-byte Character）**：需要 2 个或更多字节表示的字符，如汉字（3字节）和 emoji（4字节）。

---

## 10.25 unicode/utf16 包：UTF-16 编码与解码

虽然 Go 原生使用 UTF-8，但有时候你不得不与 UTF-16 打交道——比如 Windows API、JavaScript 的 `String` 类型，或者某些网络协议。`unicode/utf16` 包就是你的翻译官。

```go
package main

import (
    "fmt"
    "unicode/utf16"
)

func main() {
    // UTF-16 编码的核心函数
    
    // 1. Encode：把 Unicode 码点序列转成 UTF-16
    runes := []rune{'H', 'i', '中', '😀'}
    utf16Arr := utf16.Encode(runes)
    
    fmt.Println("=== utf16.Encode ===")
    fmt.Printf("原始 rune: %c %c %c %c\n", runes[0], runes[1], runes[2], runes[3])
    fmt.Printf("UTF-16 编码: % X\n", utf16Arr)
    // 打印结果：UTF-16 编码: [48 69 4E2D D83D DE00]
    //                                              ↑↑↑↑
    //                                         代理对！
    
    // 2. Decode：把 UTF-16 转回 Unicode 码点
    decoded := utf16.Decode(utf16Arr)
    fmt.Println("\n=== utf16.Decode ===")
    fmt.Printf("UTF-16: % X\n", utf16Arr)
    fmt.Printf("解码 rune: %c %c %c %c\n", decoded[0], decoded[1], decoded[2], decoded[3])
    // 打印结果：解码 rune: H i 中 😀
    
    // 3. Append runes 到 []uint16 切片
    fmt.Println("\n=== utf16.AppendRune ===")
    buf := []uint16{'H', 'i'}
    buf = utf16.AppendRune(buf, '中')
    buf = utf16.AppendRune(buf, '😀')
    fmt.Printf("追加后的 UTF-16: % X\n", buf)
    // 打印结果：追加后的 UTF-16: [48 69 4E2D D83D DE00]
    
    // 4. 判断是否需要代理对（是否是补充平面字符）
    fmt.Println("\n=== 代理对判断 ===")
    testRunes := []rune{'A', '中', '😀', '你'}
    for _, r := range testRunes {
        isSurrogate := r >= 0x10000
        fmt.Printf("'%c' (U+%X): 需要代理对 = %v\n", r, r, isSurrogate)
    }
    // 打印结果：
    // 'A': 需要代理对 = false
    // '中': 需要代理对 = false
    // '😀': 需要代理对 = true
    // '你': 需要代理对 = false
}
```

```
┌─────────────────────────────────────────────────────────────┐
│                   UTF-8 vs UTF-16 对比                       │
├──────────────────────────┬──────────────────────────────────┤
│ UTF-8                     │ UTF-16                           │
├──────────────────────────┼──────────────────────────────────┤
│ 变长编码：1-4 字节         │ 基本定长：2 字节（代理对除外）     │
├──────────────────────────┼──────────────────────────────────┤
│ ASCII 兼容：1 字节         │ ASCII 不兼容：'A' = 00 41        │
├──────────────────────────┼──────────────────────────────────┤
│ 自同步：首字节可判断长度    │ 无自同步：需要额外机制            │
├──────────────────────────┼──────────────────────────────────┤
│ Go 语言默认编码           │ Windows、Java、JavaScript 默认    │
├──────────────────────────┼──────────────────────────────────┤
│ '中' = E4 B8 AD (3字节)   │ '中' = 4E 2D (2字节)             │
│ '😀' = F0 9F 98 80 (4字节)│ '😀' = D8 3D DE 00 (代理对)      │
└──────────────────────────┴──────────────────────────────────┘
```

**专业词汇解释：**

- **UTF-16 编码**：一种使用 2 字节表示大多数字符的编码格式。对于超出 BMP 的字符，使用代理对（4字节）表示。
- **代理对（Surrogate Pair）**：UTF-16 中用两个 16 位值（高代理和低代理）表示一个补充平面字符的机制。
- **补充平面（Supplementary Planes）**：Unicode 中 U+10000 及以上的字符，包括 emoji、历史文字等。

---

## 本章小结

恭喜你！你已经完成了 Unicode 和 UTF-8 的扫盲之旅。让我们来回顾一下今天学到的"生存技能"：

### 核心概念

| 概念 | 说明 |
|------|------|
| **Unicode** | 给世界上所有字符分配唯一编号（码点）的国际标准 |
| **UTF-8** | Go 字符串的编码格式，1-4 字节变长 |
| **码点（Code Point）** | Unicode 字符的唯一标识，如 `U+4E2D` |
| **Rune** | Go 中的 `int32` 类型，代表一个 Unicode 码点 |

### 常用函数速查

```go
// 判断类
unicode.IsDigit(r)    // 是数字？
unicode.IsLetter(r)   // 是字母？
unicode.IsUpper(r)    // 是大写？
unicode.IsLower(r)    // 是小写？
unicode.IsSpace(r)    // 是空白？
unicode.IsPunct(r)    // 是标点？
unicode.IsControl(r)  // 是控制字符？
unicode.IsPrint(r)    // 是可打印字符？

// 转换类
unicode.ToUpper(r)    // 转大写
unicode.ToLower(r)    // 转小写
unicode.ToTitle(r)    // 转标题形式
unicode.SimpleFold(r) // 下一个等价字符

// UTF-8 编解码
utf8.DecodeRune(p)              // 解码一个 rune
utf8.EncodeRune(p, r)          // 编码一个 rune
utf8.RuneCountInString(s)       // 按字符计数的字符串长度
utf8.ValidString(s)             // 验证是否合法 UTF-8
utf8.DecodeLastRuneInString(s)  // 解码最后一个 rune
utf8.RuneStart(b)               // 是否是首字节？

// UTF-16
utf16.Encode(runes)             // Unicode → UTF-16
utf16.Decode(utf16Arr)         // UTF-16 → Unicode
```

### 避坑指南

1. **永远不要用 `len(s)` 获取字符数**——它返回的是字节数
2. **永远不要用 `s[n]` 获取第 n 个字符**——它返回的是第 n 个字节
3. **遍历字符串用 `for _, r := range s`**——而不是遍历字节切片
4. **处理外部输入时验证 UTF-8**——用 `utf8.ValidString()`

### 一句话总结

> Go 的字符串是 UTF-8 编码的字节序列，字符数 ≠ 字节数，索引 ≠ 字符位置。

---

*"懂得了这些，你终于可以自信地说：我知道 emoji 为什么占 4 个字节了。"*
