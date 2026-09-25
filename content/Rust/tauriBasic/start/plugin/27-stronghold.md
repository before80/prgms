+++
title = "27 Stronghold"
date = 2026-09-25T21:31:08+08:00
weight = 27
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/stronghold/](https://tauri.app/plugin/stronghold/)

使用 [IOTA Stronghold](https://github.com/iotaledger/stronghold.rs) 密钥管理引擎存储密钥与敏感数据。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add stronghold
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add stronghold
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add stronghold
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add stronghold
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add stronghold
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add stronghold
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-stronghold
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_stronghold::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-stronghold
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-stronghold
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-stronghold
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-stronghold
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-stronghold
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 用法

插件必须用一个密码哈希函数初始化，该函数接收密码字符串，并必须返回由它派生的 32 字节哈希。

### 使用 argon2 密码哈希函数初始化

Stronghold 插件提供了一个使用 [argon2](https://docs.rs/rust-argon2/latest/argon2/) 算法的默认哈希函数。

```rust
use tauri::Manager;

pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let salt_path = app
                .path()
                .app_local_data_dir()
                .expect("could not resolve app local data path")
                .join("salt.txt");
            app.handle().plugin(tauri_plugin_stronghold::Builder::with_argon2(&salt_path).build())?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 使用自定义密码哈希函数初始化

或者，你可以使用 `tauri_plugin_stronghold::Builder::new` 构造函数提供自己的哈希算法。

{{% alert title="注意" %}}
密码哈希必须正好是 32 字节。这是 Stronghold 的要求。
{{% /alert %}}

```rust
pub fn run() {
    tauri::Builder::default()
        .plugin(
            tauri_plugin_stronghold::Builder::new(|password| {
                // 在这里用 argon2、blake2b 或任何其它安全算法对密码做哈希
                // 下面是使用 `rust-argon2` crate 对密码做哈希的示例实现
                use argon2::{hash_raw, Config, Variant, Version};

                let config = Config {
                    lanes: 4,
                    mem_cost: 10_000,
                    time_cost: 10,
                    variant: Variant::Argon2id,
                    version: Version::Version13,
                    ..Default::default()
                };
                let salt = "your-salt".as_bytes();
                let key = hash_raw(password.as_ref(), salt, &config).expect("failed to hash password");

                key.to_vec()
            })
            .build(),
        )
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 从 JavaScript 使用

stronghold 插件在 JavaScript 中可用。

```javascript
import { Client, Stronghold } from '@tauri-apps/plugin-stronghold';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { Client, Stronghold } = window.__TAURI__.stronghold;
import { appDataDir } from '@tauri-apps/api/path';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { appDataDir } = window.__TAURI__.path;

const initStronghold = async () => {
	const vaultPath = `${await appDataDir()}/vault.hold`;
	const vaultPassword = 'vault password';
	const stronghold = await Stronghold.load(vaultPath, vaultPassword);

	let client: Client;
	const clientName = 'name your client';
	try {
		client = await stronghold.loadClient(clientName);
	} catch {
		client = await stronghold.createClient(clientName);
	}

	return {
		stronghold,
		client,
	};
};

// 向 store 插入一条记录
async function insertRecord(store: any, key: string, value: string) {
	const data = Array.from(new TextEncoder().encode(value));
	await store.insert(key, data);
}

// 从 store 读取一条记录
async function getRecord(store: any, key: string): Promise<string> {
	const data = await store.get(key);
	return new TextDecoder().decode(new Uint8Array(data));
}

const { stronghold, client } = await initStronghold();

const store = client.getStore();
const key = 'my_key';

// 向 store 插入一条记录
insertRecord(store, key, 'secret value');

// 从 store 读取一条记录
const value = await getRecord(store, key);
console.log(value); // 'secret value'

// 保存你的更新
await stronghold.save();

// 从 store 移除一条记录
await store.remove(key);
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "stronghold:default"
  ]
}
```
