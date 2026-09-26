+++
title = "25 SQL"
date = 2026-09-25T21:31:08+08:00
weight = 25
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/sql/](https://tauri.app/plugin/sql/)

为前端提供通过 [sqlx](https://github.com/launchbadge/sqlx) 与 SQL 数据库通信的接口，支持 SQLite、MySQL 与 PostgreSQL。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add sql
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add sql
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add sql
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add sql
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add sql
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add sql
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-sql
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_sql::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-sql
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-sql
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-sql
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-sql
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-sql
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

该插件的所有 API 都可以通过 JavaScript 端绑定使用：

**数据库**

{{< tabpane text=true persist=disabled >}}

{{% tab header="SQLite" %}}

路径相对于 [`tauri::api::path::BaseDirectory::AppConfig`](https://docs.rs/tauri/2.0.0/tauri/path/enum.BaseDirectory.html#variant.AppConfig)。

```javascript
import Database from '@tauri-apps/plugin-sql';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const Database = window.__TAURI__.sql;

const db = await Database.load('sqlite:test.db');
await db.execute('INSERT INTO ...');
```

{{% /tab %}}

{{% tab header="MySQL" %}}

```javascript
import Database from '@tauri-apps/plugin-sql';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const Database = window.__TAURI__.sql;

const db = await Database.load('mysql://user:password@host/test');
await db.execute('INSERT INTO ...');
```

{{% /tab %}}

{{% tab header="PostgreSQL" %}}

```javascript
import Database from '@tauri-apps/plugin-sql';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const Database = window.__TAURI__.sql;

const db = await Database.load('postgres://user:password@host/test');
await db.execute('INSERT INTO ...');
```

{{% /tab %}}

{{< /tabpane >}}

## 语法

我们使用 [sqlx](https://docs.rs/sqlx/latest/sqlx/) 作为底层库，并采用它的查询语法。

**数据库**

{{< tabpane text=true persist=disabled >}}

{{% tab header="SQLite" %}}

替换查询数据时使用 "$#" 语法

```javascript
const result = await db.execute(
  'INSERT into todos (id, title, status) VALUES ($1, $2, $3)',
  [todos.id, todos.title, todos.status]
);

const result = await db.execute(
  'UPDATE todos SET title = $1, status = $2 WHERE id = $3',
  [todos.title, todos.status, todos.id]
);
```

{{% /tab %}}

{{% tab header="MySQL" %}}

替换查询数据时使用 "?"

```javascript
const result = await db.execute(
  'INSERT into todos (id, title, status) VALUES (?, ?, ?)',
  [todos.id, todos.title, todos.status]
);

const result = await db.execute(
  'UPDATE todos SET title = ?, status = ? WHERE id = ?',
  [todos.title, todos.status, todos.id]
);
```

{{% /tab %}}

{{% tab header="PostgreSQL" %}}

替换查询数据时使用 "$#" 语法

```javascript
const result = await db.execute(
  'INSERT into todos (id, title, status) VALUES ($1, $2, $3)',
  [todos.id, todos.title, todos.status]
);

const result = await db.execute(
  'UPDATE todos SET title = $1, status = $2 WHERE id = $3',
  [todos.title, todos.status, todos.id]
);
```

{{% /tab %}}

{{< /tabpane >}}

## 迁移

该插件支持数据库迁移，让你可以随时间管理数据库结构的演进。

### 定义迁移

迁移在 Rust 中使用 [`Migration`](https://docs.rs/tauri-plugin-sql/latest/tauri_plugin_sql/struct.Migration.html) 结构体定义。每个迁移都应包含唯一版本号、描述、要执行的 SQL，以及迁移类型（Up 或 Down）。

迁移示例：

```rust
use tauri_plugin_sql::{Migration, MigrationKind};

let migration = Migration {
    version: 1,
    description: "create_initial_tables",
    sql: "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);",
    kind: MigrationKind::Up,
};
```

如果你想使用文件中的 SQL，可以用 `include_str!` 引入：

```rust
use tauri_plugin_sql::{Migration, MigrationKind};

let migration = Migration {
    version: 1,
    description: "create_initial_tables",
    sql: include_str!("../drizzle/0000_graceful_boomer.sql"),
    kind: MigrationKind::Up,
};
```

### 把迁移加入插件 Builder

迁移通过插件提供的 [`Builder`](https://docs.rs/tauri-plugin-sql/latest/tauri_plugin_sql/struct.Builder.html) 结构体注册。使用 `add_migrations` 方法，为某个特定数据库连接把你的迁移加入插件。

添加迁移的示例：

```rust
use tauri_plugin_sql::{Builder, Migration, MigrationKind};

fn main() {
    let migrations = vec![
        // 在这里定义你的迁移
        Migration {
            version: 1,
            description: "create_initial_tables",
            sql: "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);",
            kind: MigrationKind::Up,
        }
    ];

    tauri::Builder::default()
        .plugin(
            tauri_plugin_sql::Builder::default()
                .add_migrations("sqlite:mydatabase.db", migrations)
                .build(),
        )
        ...
}
```

### 应用迁移

要在插件初始化时应用迁移，请把连接字符串加入 `tauri.conf.json` 文件：

```json
{
  "plugins": {
    "sql": {
      "preload": ["sqlite:mydatabase.db"]
    }
  }
}
```

另外，客户端的 `load()` 也会为给定的连接字符串运行迁移：

```ts
import Database from '@tauri-apps/plugin-sql';
const db = await Database.load('sqlite:mydatabase.db');
```

请确保迁移按正确顺序定义，并且可以安全地重复运行。

{{% alert title="注意" %}}
所有迁移都在一个事务中执行，从而保证原子性。如果任何迁移失败，整个事务都会回滚，数据库保持一致状态。
{{% /alert %}}

### 迁移管理

- **版本控制**：每个迁移必须有唯一的版本号。这对确保迁移按正确顺序应用至关重要。
- **幂等性**：以可以安全重复运行、不会引发错误或意外后果的方式编写迁移。
- **测试**：彻底测试迁移，确保它们按预期工作，且不会损害数据库的完整性。

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "sql:default",
    "sql:allow-execute"
  ]
}
```
