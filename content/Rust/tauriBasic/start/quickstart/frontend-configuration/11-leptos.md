+++
title = "11 Leptos"
date = 2026-09-25T21:31:08+08:00
weight = 11
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/leptos/](https://tauri.app/start/frontend/leptos/)

Leptos 是一个基于 Rust 的 Web 框架。你可以在其[官方网站](https://leptos.dev/)进一步了解 Leptos。本指南基于 Leptos 0.6 版本。

## 检查清单

- 使用 SSG，Tauri 官方不支持基于服务器的方案。
- 设置 `serve.ws_protocol = "ws"`，以便移动端开发时热重载 WebSocket 能正常连接。
- 启用 `withGlobalTauri`，确保 Tauri API 可通过 `window.__TAURI__` 变量使用，并可用 `wasm-bindgen` 导入。

## 示例配置

1. 更新 Tauri 配置

   ```json
   // src-tauri/tauri.conf.json
   {
     "build": {
       "beforeDevCommand": "trunk serve",
       "devUrl": "http://localhost:1420",
       "beforeBuildCommand": "trunk build",
       "frontendDist": "../dist"
     },
     "app": {
       "withGlobalTauri": true
     }
   }
   ```

2. 更新 Trunk 配置

   ```toml
   // Trunk.toml
   [build]
   target = "./index.html"

   [watch]
   ignore = ["./src-tauri"]

   [serve]
   port = 1420
   open = false
   ws_protocol = "ws"

   ```
