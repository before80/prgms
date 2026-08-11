+++
title = "2.5 练习：巫师的物品栏"
date = 2026-08-11T11:30:00+08:00
weight = 148
type = "docs"
description = "练习：巫师的物品栏 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/exercise.html](https://google.github.io/comprehensive-rust/borrowing/exercise.html)

# 2.5 练习：巫师的物品栏

本练习中，你将运用已学的借用与所有权知识管理巫师的物品栏。

- 巫师有一组法术。你需要实现向物品栏添加法术、以及从中施放法术的函数。

- 法术有有限的使用次数。当法术没有剩余使用次数时，必须从巫师的物品栏中移除。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Spell {
    name: String,
    cost: u32,
    uses: u32,
}

struct Wizard {
    spells: Vec<Spell>,
    mana: u32,
}

impl Wizard {
    fn new(mana: u32) -> Self {
        Wizard { spells: vec![], mana }
    }

    // TODO: 实现 `add_spell`，取得法术的所有权并将其加入巫师的物品栏。
    fn add_spell(..., spell: ...) {
        todo!()
    }

    // TODO: 实现 `cast_spell`，从物品栏借用法术并施放。
    // 巫师的 mana 应减少法术的消耗，法术的使用次数应减 1。
    //
    // 若巫师 mana 不足，法术应失败。
    // 若法术没有剩余使用次数，则从物品栏中移除。
    fn cast_spell(..., name: ...) {
        todo!()
    }
}

fn main() {
    let mut merlin = Wizard::new(100);
    let fireball = Spell { name: String::from("Fireball"), cost: 10, uses: 2 };
    let ice_blast = Spell { name: String::from("Ice Blast"), cost: 15, uses: 1 };

    merlin.add_spell(fireball);
    merlin.add_spell(ice_blast);

    merlin.cast_spell("Fireball"); // Casts successfully
    merlin.cast_spell("Ice Blast"); // Casts successfully, then removed
    merlin.cast_spell("Ice Blast"); // Fails (not found)
    merlin.cast_spell("Fireball"); // Casts successfully, then removed
    merlin.cast_spell("Fireball"); // Fails (not found)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_spell() {
        let mut wizard = Wizard::new(10);
        let spell = Spell { name: String::from("Fireball"), cost: 5, uses: 3 };
        wizard.add_spell(spell);
        assert_eq!(wizard.spells.len(), 1);
    }

    #[test]
    fn test_cast_spell() {
        let mut wizard = Wizard::new(10);
        let spell = Spell { name: String::from("Fireball"), cost: 5, uses: 3 };
        wizard.add_spell(spell);

        wizard.cast_spell("Fireball");
        assert_eq!(wizard.mana, 5);
        assert_eq!(wizard.spells.len(), 1);
        assert_eq!(wizard.spells[0].uses, 2);
    }

    #[test]
    fn test_cast_spell_insufficient_mana() {
        let mut wizard = Wizard::new(10);
        let spell = Spell { name: String::from("Fireball"), cost: 15, uses: 3 };
        wizard.add_spell(spell);

        wizard.cast_spell("Fireball");
        assert_eq!(wizard.mana, 10);
        assert_eq!(wizard.spells.len(), 1);
        assert_eq!(wizard.spells[0].uses, 3);
    }

    #[test]
    fn test_cast_spell_not_found() {
        let mut wizard = Wizard::new(10);
        wizard.cast_spell("Fireball");
        assert_eq!(wizard.mana, 10);
    }

    #[test]
    fn test_cast_spell_removal() {
        let mut wizard = Wizard::new(10);
        let spell = Spell { name: String::from("Fireball"), cost: 5, uses: 1 };
        wizard.add_spell(spell);

        wizard.cast_spell("Fireball");
        assert_eq!(wizard.mana, 5);
        assert_eq!(wizard.spells.len(), 0);
    }
}
```

> - 本练习的目标是练习所有权与借用的核心概念，尤其是：在持有对集合某个元素的引用时，不能修改该集合。
> - `add_spell` 应取得 `Spell` 的所有权，并将其移入 `Wizard` 的物品栏。
> - `cast_spell` 是练习的核心。它需要：
>   1. 找到法术（按索引或引用）。
>   2. 检查 mana 并减少它。
>   3. 减少法术的 `uses`。
>   4. 若 `uses == 0` 则移除法术。
> - **借用检查器冲突：** 若学员试图持有对法术的引用（例如 `let spell = &mut self.spells[i]`），然后在该引用仍在同一作用域中「存活」时调用 `self.spells.remove(i)`，借用检查器会报错。这是展示如何组织代码以满足借用检查器的好机会（例如使用索引，或确保在修改前结束借用）。

