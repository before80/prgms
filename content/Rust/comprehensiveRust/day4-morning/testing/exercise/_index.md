+++
title = "4.4 练习：Luhn 算法"
date = 2026-08-11T11:30:00+08:00
weight = 182
type = "docs"
description = "练习：Luhn 算法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/testing/exercise.html](https://google.github.io/comprehensive-rust/testing/exercise.html)

# 4.4 练习：Luhn 算法

[Luhn 算法](https://en.wikipedia.org/wiki/Luhn_algorithm) 用于验证信用卡号。该算法接收一个字符串作为输入，并按以下步骤验证信用卡号：

- 忽略所有空格。拒绝少于两位数字的号码。拒绝字母及其他非数字字符。

- 从**右到左**，每隔一位将数字加倍：对于 `1234`，加倍 `3` 和 `1`；对于 `98765`，加倍 `6` 和 `8`。

- 加倍后若结果大于 9，则将各位数字相加。例如加倍 `7` 得到 `14`，再变成 `1 + 4 = 5`。

- 将所有未加倍与加倍后的数字求和。

- 若总和以 `0` 结尾，则该信用卡号有效。

所提供的代码给出了一个有缺陷的 Luhn 算法实现，以及两个基本单元测试，它们确认算法的大部分逻辑已正确实现。

把下面的代码复制到 <https://play.rust-lang.org/>，再编写额外测试以发现所给实现中的缺陷，并修复你找到的所有 bug。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub fn luhn(cc_number: &str) -> bool {
    let mut sum = 0;
    let mut double = false;

    for c in cc_number.chars().rev() {
        if let Some(digit) = c.to_digit(10) {
            if double {
                let double_digit = digit * 2;
                sum +=
                    if double_digit > 9 { double_digit - 9 } else { double_digit };
            } else {
                sum += digit;
            }
            double = !double;
        } else {
            continue;
        }
    }

    sum % 10 == 0
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_valid_cc_number() {
        assert!(luhn("4263 9826 4026 9299"));
        assert!(luhn("4539 3195 0343 6467"));
        assert!(luhn("7992 7398 713"));
    }

    #[test]
    fn test_invalid_cc_number() {
        assert!(!luhn("4223 9826 4026 9299"));
        assert!(!luhn("4539 3195 0343 6476"));
        assert!(!luhn("8273 1232 7352 0569"));
    }
}
```
