+++
title = "5 前端配置"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/](https://tauri.app/start/frontend/)

Tauri 不绑定特定前端，开箱即支持大多数前端框架。不过有时框架需要一点额外配置才能与 Tauri 集成。下面列出了推荐配置的框架。

如果某个框架没有列出，它可能无需额外配置就能与 Tauri 配合，也可能只是尚未被记录。欢迎贡献文档，为可能需要额外配置的框架补充说明，帮助 Tauri 社区中的其他人。

## 配置检查清单

从概念上讲，Tauri 充当静态 Web 托管。你需要为 Tauri 提供一个文件夹，其中包含可由 Tauri 提供的 webview 访问的 HTML、CSS、JavaScript，可能还有 WASM。

下面是前端与 Tauri 集成时常见场景的检查清单：

- 使用静态站点生成（SSG）、单页应用（SPA）或经典的多页应用（MPA）。Tauri 原生不支持基于服务器的方案（例如 SSR）。
- 进行移动端开发时，需要某种能把前端托管在你内网 IP 上的开发服务器。
- 应用与 API 之间要使用规范的客户端—服务器关系（不要使用 SSR 那种混合方案）。

## JavaScript

对于大多数项目，我们推荐使用 [Vite](https://vitejs.dev/)：既适用于 React、Vue、Svelte 和 Solid 等 SPA 框架，也适用于纯 JavaScript 或 TypeScript 项目。这里列出的其它指南大多介绍如何使用元框架（Meta-Framework），因为它们通常是为 SSR 设计的，因此需要特殊配置。

- [Vite（推荐）](6-vite/)
- [Next.js](7-nextjs/)
- [Nuxt](8-nuxt/)
- [Qwik](9-qwik/)
- [SvelteKit](10-sveltekit/)

## Rust

- [Leptos](11-leptos/)
- [Trunk](12-trunk/)

<br />

{{% alert title="没有列出你的框架？" %}}

没有看到你使用的框架？它可能无需任何额外配置就能与 Tauri 配合。请阅读[配置检查清单](#配置检查清单)，逐项检查常见配置。

{{% /alert %}}
