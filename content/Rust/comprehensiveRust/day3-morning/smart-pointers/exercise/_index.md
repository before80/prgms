+++
title = "3.4 练习：二叉树"
date = 2026-08-11T11:30:00+08:00
weight = 137
type = "docs"
description = "练习：二叉树 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/smart-pointers/exercise.html](https://google.github.io/comprehensive-rust/smart-pointers/exercise.html)

# 3.4 练习：二叉树

二叉树是一种树形数据结构，每个节点都有两个子节点（左与右）。我们将创建一棵每个节点存储一个值的树。对给定节点 N，N 的左子树中所有节点的值都更小，右子树中所有节点的值都更大。同一值在树中只应存储一次，即没有重复节点。

实现下列类型，使给定测试通过。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 二叉树中的一个节点。
#[derive(Debug)]
struct Node<T: Ord> {
    value: T,
    left: Subtree<T>,
    right: Subtree<T>,
}

/// 可能为空的子树。
#[derive(Debug)]
struct Subtree<T: Ord>(Option<Box<Node<T>>>);

/// 用二叉树存储一组值的容器。
///
/// 若同一值被多次添加，也只存储一次。
#[derive(Debug)]
pub struct BinaryTree<T: Ord> {
    root: Subtree<T>,
}

impl<T: Ord> BinaryTree<T> {
    fn new() -> Self {
        Self { root: Subtree::new() }
    }

    fn insert(&mut self, value: T) {
        self.root.insert(value);
    }

    fn has(&self, value: &T) -> bool {
        self.root.has(value)
    }

    fn len(&self) -> usize {
        self.root.len()
    }
}

// 为 `Node` 实现 `new`。
// 为 `Subtree` 实现 `new`、`insert`、`len` 与 `has`。

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn len() {
        let mut tree = BinaryTree::new();
        assert_eq!(tree.len(), 0);
        tree.insert(2);
        assert_eq!(tree.len(), 1);
        tree.insert(1);
        assert_eq!(tree.len(), 2);
        tree.insert(2); // not a unique item
        assert_eq!(tree.len(), 2);
        tree.insert(3);
        assert_eq!(tree.len(), 3);
    }

    #[test]
    fn has() {
        let mut tree = BinaryTree::new();
        fn check_has(tree: &BinaryTree<i32>, exp: &[bool]) {
            let got: Vec<bool> =
                (0..exp.len()).map(|i| tree.has(&(i as i32))).collect();
            assert_eq!(&got, exp);
        }

        check_has(&tree, &[false, false, false, false, false]);
        tree.insert(0);
        check_has(&tree, &[true, false, false, false, false]);
        tree.insert(4);
        check_has(&tree, &[true, false, false, false, true]);
        tree.insert(4);
        check_has(&tree, &[true, false, false, false, true]);
        tree.insert(3);
        check_has(&tree, &[true, false, false, true, true]);
    }

    #[test]
    fn unbalanced() {
        let mut tree = BinaryTree::new();
        for i in 0..100 {
            tree.insert(i);
        }
        assert_eq!(tree.len(), 100);
        assert!(tree.has(&50));
    }
}
```
