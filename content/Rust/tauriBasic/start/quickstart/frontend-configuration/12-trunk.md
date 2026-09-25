+++
title = "12 Trunk"
date = 2026-09-25T21:31:08+08:00
weight = 12
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/trunk/](https://tauri.app/start/frontend/trunk/)

Trunk 是 Rust 的 WASM Web 应用打包工具。你可以在 https://trunk-rs.github.io/trunk/ 进一步了解 Trunk。本指南基于 Trunk 0.17.5。

## 检查清单

- 使用 SSG，Tauri 官方不支持基于服务器的方案。
- 设置 `serve.ws_protocol = "ws"`，以便移动端开发时热重载 WebSocket 能正常连接。
- 启用 `withGlobalTauri`，确保 Tauri API 可通过 `window.__TAURI__` 变量使用，并可用 `wasm-bindgen` 导入。

## 示例配置

1. 更新 Tauri 配置

   ```json
   // tauri.conf.json
   {
     "build": {
       "beforeDevCommand": "trunk serve",
       "beforeBuildCommand": "trunk build",
       "devUrl": "http://localhost:8080",
       "frontendDist": "../dist"
     },
     "app": {
       "withGlobalTauri": true
     }
   }
   ```

2. 更新 Trunk 配置

   ```toml
   # Trunk.toml
   [watch]
   ignore = ["./src-tauri"]

   [serve]
   ws_protocol = "ws"
   ```
