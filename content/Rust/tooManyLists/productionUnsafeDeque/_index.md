+++
title = "6 生产级不安全双端队列"
date = 2026-08-23T16:06:00+08:00
weight = 60
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://rust-unofficial.github.io/too-many-lists/sixth.html](https://rust-unofficial.github.io/too-many-lists/sixth.html)

我们终于走到了这里。我最大的宿敌：**[std::collections::LinkedList][linked-list]，双向链表双端队列**。

那个我试图摧毁、却失败了的东西。

故事要从 2014 年接近尾声说起，那时我们正快速逼近 Rust 1.0——Rust 的首次稳定版发布。我那时负责照看 `std::collections`，在当年我们亲切地称它为 libcollections。

libcollections 多年来一直是大家各种「可爱点子」和「有点用的东西」的倾倒场。在 Rust 还是一门稚嫩实验语言时，这倒也无妨；但若我的孩子们要离巢、要被稳定下来，它们就得证明自己的价值。

在此之前我一直鼓励、呵护它们，但现在是时候让它们为自己的失败接受审判了。

我伸出利爪，凿入基岩，为我最愚蠢的孩子们刻下墓碑。一座骇人的纪念碑，被我摆在镇中心，供所有人瞻仰：

**[Kill TreeMap, TreeSet, TrieMap, TrieSet, LruCache and EnumSet](https://github.com/rust-lang/rust/pull/19955)**

它们的命运已定，因为我的话就是绝对的。其他集合被我的残暴吓坏了，但它们尚未逃过母亲的怒火。我很快又带回来两块墓碑：

**[Deprecate BitSet and BitVec](https://github.com/rust-lang/rust/pull/26034)**

Bit 双子比倒下的同伴更狡猾，但缺乏逃脱我的力量。多数人以为我的工作已经结束，但我很快又干掉了一个：

**[Deprecate VecMap](https://github.com/rust-lang/rust/pull/26734)**

VecMap 试图靠隐身苟活——它又小又无害！但那不足以满足我心目中未来的 libcollections。

我环顾这片土地，看看还剩下什么：

* Vec 和 VecDeque——健壮而简单，计算的心脏。
* HashMap 和 HashSet——强大而睿智，计算的大脑。
* BTreeMap 和 BTreeSet——笨拙但必要，计算的肝脏。
* BinaryHeap——灵巧而敏捷，计算的脚踝。

我满意地点点头。简单有效。我的工作完——

不，[DList](https://github.com/rust-lang/rust/blob/0a84308ebaaafb8fd89b2fd7c235198e3ec21384/src/libcollections/dlist.rs)，不可能！我以为你在那场悲惨的垃圾回收事故里死了！那绝对是个意外，绝不是故意的！

它假死脱身，换了新名字，但仍是它：LinkedList，计算界阴险而不可靠的阴谋家。

我向所有愿意倾听的人宣扬它的恶行，但人心不为所动。LinkedList 是个能言善辩的魔鬼，让周围所有人都相信它是某种计算领域根本而自然的数据结构。它甚至说服了 C++，让它成为[*那个* list](https://en.cppreference.com/w/cpp/container/list)！

「标准库里怎么能没有 *LinkedList*？」

很容易！轻而易举！

「它是非平凡的 unsafe 代码，放在标准库里很合理！」

GPU 驱动和视频编解码器也是，libcollections 可是极简主义！

但 alas，在我忙着对付它的兄弟姐妹时，LinkedList 拉拢了太多盟友，变得过于强大。

我逃进实验室，试图造出某种[邪恶克隆体](https://github.com/contain-rs/linked-list)或[强化赛博格仿生人](https://github.com/contain-rs/blist)来与之抗衡并摧毁它，但研究经费断了，因为我的研究「过于邪恶地充满杀意」之类的废话。

LinkedList 赢了。我战败，被迫流亡。

但你现在在这里。你已经走了这么远。想必你现在能理解 LinkedList 堕落的深度了！来，我会向你展示摧毁它所需的一切——实现一个 unsafe 生产级双向链表双端队列所需的一切。

生产级到什么程度？我们要彻底重写我古老的 Rust 1.0 链表 crate——那个客观上比 std 里更好的版本。那个在稳定 Rust 上就有 Cursor 的，2015 年的！而 2022 年的标准库仍然没有！




[linked-list]: https://github.com/rust-lang/rust/blob/master/library/alloc/src/collections/linked_list.rs
