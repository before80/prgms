+++
title = "5 嵌入附加文件"
date = 2026-09-25T21:31:08+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/resources/](https://tauri.app/develop/resources/)

你可能需要在应用打包中加入一些不属于前端（即你的 `frontendDist`）的文件，或者文件太大不适合内联进二进制文件。我们把这类文件称为 `resources`（资源）。

## 配置

要打包你选定的文件，请在 `tauri.conf.json` 文件的 `bundle` 对象中添加 `resources` 属性。

要包含一组文件：

**写法**

{{< tabpane text=true persist=disabled >}}
{{% tab header="语法" %}}

```json
{
  "bundle": {
    "resources": [
      "./path/to/some-file.txt",
      "/absolute/path/to/textfile.txt",
      "../relative/path/to/jsonfile.json",
      "some-folder/",
      "resources/**/*.md"
    ]
  }
}
```

{{% /tab %}}

{{% tab header="说明" %}}

```json5
{
  "bundle": {
    "resources": [
      // 会被放到 `$RESOURCE/path/to/some-file.txt`
      "./path/to/some-file.txt",

      // 绝对路径的根会被替换为 `_root_`，
      // 因此 `textfile.txt` 会被放到 `$RESOURCE/_root_/absolute/path/to/textfile.txt`
      "/absolute/path/to/textfile.txt",

      // 相对路径中的 `..` 会被替换为 `_up_`，
      // 因此 `jsonfile.json` 会被放到 `$RESOURCE/_up_/relative/path/to/textfile.txt`
      "../relative/path/to/jsonfile.json",

      // 如果路径是目录，整个目录会被复制到 `$RESOURCE` 目录，
      // 并保留原有结构，例如：
      //   - `some-folder/file.txt`                   -> `$RESOURCE/some-folder/file.txt`
      //   - `some-folder/another-folder/config.json` -> `$RESOURCE/some-folder/another-folder/config.json`
      // 这等同于 `some-folder/**/*`
      "some-folder/",

      // 你也可以通过 glob 模式一次包含多个文件。
      // `resources` 内所有 `.md` 文件都会被放到 `$RESOURCE/resources/`，
      // 并保留原有目录结构，例如：
      //   - `resources/index.md`      -> `$RESOURCE/resources/index.md`
      //   - `resources/docs/setup.md` -> `$RESOURCE/resources/docs/setup.md`
      "resources/**/*.md"
    ]
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
打包后的文件会位于 `$RESOURCES/` 中，并保留原有目录结构，
例如：`./path/to/some-file.txt` -> `$RESOURCE/path/to/some-file.txt`

要精细控制文件复制到何处，请改用映射（map）形式：

**写法**

{{< tabpane text=true persist=disabled >}}
{{% tab header="语法" %}}

```json
{
  "bundle": {
    "resources": {
      "/absolute/path/to/textfile.txt": "resources/textfile.txt",
      "relative/path/to/jsonfile.json": "resources/jsonfile.json",
      "resources/": "",
      "docs/**/*md": "website-docs/"
    }
  }
}
```

{{% /tab %}}

{{% tab header="说明" %}}

```json5
{
  "bundle": {
    "resources": {
      // `textfile.txt` 会被放到 `$RESOURCE/resources/textfile.txt`
      "/absolute/path/to/textfile.txt": "resources/textfile.txt",

      // `jsonfile.json` 会被放到 `$RESOURCE/resources/jsonfile.json`
      "relative/path/to/jsonfile.json": "resources/jsonfile.json",

      // 把整个目录复制到 `$RESOURCE`，并保留原有结构，
      // 目标为 ""，表示会直接放进资源目录 `$RESOURCE`，例如：
      //   - `resources/file.txt`                -> `$RESOURCE/file.txt`
      //   - `resources/some-folder/config.json` -> `$RESOURCE/some-folder/config.json`
      "resources/": "",

      // 使用 glob 模式时，行为与列表形式不同：
      // 所有匹配的文件会被放到目标目录，且不保留原有文件结构
      // 例如：
      //   - `docs/index.md`         -> `$RESOURCE/website-docs/index.md`
      //   - `docs/plugins/setup.md` -> `$RESOURCE/website-docs/setup.md`
      "docs/**/*md": "website-docs/"
    }
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
关于 `$RESOURCE` 在各平台上解析到哪里，请参阅 [`resource_dir`](https://docs.rs/tauri/latest/tauri/path/struct.PathResolver.html#method.resource_dir) 的文档。

<details>
<summary>源路径语法</summary>

在下面的说明中，“目标资源目录”指的是对象写法中冒号后面的值，或数组写法中按原文件路径重建出的位置。

- `"dir/file.txt"`：把 `file.txt` 文件复制进目标资源目录。
- `"dir/"`：把**所有文件和目录**都_递归_复制进目标资源目录。如果你想同时保留文件与目录的文件系统结构，请使用这个写法。
- `"dir/*"`：把 `dir` 目录中的所有文件_非递归地_（子目录会被忽略）复制进目标资源目录。
- `"dir/**`：会报错，因为 `**` 只匹配目录，因此找不到任何文件。
- `"dir/**/*"`：把 `dir` 目录中的所有文件_递归地_（`dir/` 中的所有文件以及所有子目录中的所有文件）复制进目标资源目录。
- `"dir/**/**`：会报错，因为 `**` 只匹配目录，因此找不到任何文件。

</details>

## 解析资源文件路径

要解析资源文件的路径，不必手动计算路径，请使用以下 API。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="Rust" %}}

在 Rust 侧，你需要一个 [`PathResolver`](https://docs.rs/tauri/latest/tauri/path/struct.PathResolver.html) 实例，可以从 [`App`](https://docs.rs/tauri/latest/tauri/struct.App.html) 和 [`AppHandle`](https://docs.rs/tauri/latest/tauri/struct.AppHandle.html) 获取，
然后调用 [`PathResolver::resolve`](https://docs.rs/tauri/latest/tauri/path/struct.PathResolver.html#method.resolve)：

```rust
  .setup(|app| {
    let resource_path = app.path().resolve("lang/de.json", BaseDirectory::Resource)?;
    Ok(())
  })
```

在命令中使用：

```rust
fn hello(handle: tauri::AppHandle) {
  let resource_path = handle.path().resolve("lang/de.json", BaseDirectory::Resource)?;
}
```

{{% /tab %}}

{{% tab header="JavaScript" %}}

在 JavaScript 中解析路径，请使用 [`resolveResource`](https://tauri.app/reference/javascript/api/namespacepath/#resolveresource)：

```javascript
import { resolveResource } from '@tauri-apps/api/path';
const resourcePath = await resolveResource('lang/de.json');
```

{{% /tab %}}

{{< /tabpane >}}
### 路径语法

API 调用中的路径既可以是像 `folder/json_file.json` 这样的普通相对路径（解析为 `$RESOURCE/folder/json_file.json`），
也可以是像 `../relative/folder/toml_file.toml` 这样的路径（解析为 `$RESOURCE/_up_/relative/folder/toml_file.toml`）。
这些 API 使用与你编写 `tauri.conf.json > bundle > resources` 时相同的规则，例如：

```json
{
  "bundle": {
    "resources": ["folder/json_file.json", "../relative/folder/toml_file.toml"]
  }
}
```

```rust
let toml_path = app.path().resolve("../relative/folder/toml_file.toml", BaseDirectory::Resource)?;
```

### Android

目前资源以 asset 的形式存储在 APK 中，因此这些 API 的返回值不是普通的文件系统路径，
我们在这里使用了一个特殊 URI 前缀 `asset://localhost/`，它可以配合 [`fs` 插件](../../plugin/9-filesystem/)使用。
这样你就可以通过 [`FsExt::fs`](https://docs.rs/tauri-plugin-fs/latest/tauri_plugin_fs/trait.FsExt.html#tymethod.fs) 读取文件：

```rust
let json = app.fs().read_to_string(&resource_path);
```

如果你希望或必须让资源文件位于真实文件系统上，请通过 [`fs` 插件](../../plugin/9-filesystem/)手动把内容复制出来。

## 读取资源文件

在这个示例中，我们想打包额外的 i18n json 文件，如下所示：

```
.
├── src-tauri/
│   ├── tauri.conf.json
│   ├── lang/
│   │   ├── de.json
│   │   └── en.json
│   └── ...
└── ...
```

```json
{
  "bundle": {
    "resources": ["lang/*"]
  }
}
```

```json
{
  "hello": "Guten Tag!",
  "bye": "Auf Wiedersehen!"
}
```

### Rust

在 Rust 侧，你需要一个 [`PathResolver`](https://docs.rs/tauri/latest/tauri/path/struct.PathResolver.html) 实例，可以从 [`App`](https://docs.rs/tauri/latest/tauri/struct.App.html) 和 [`AppHandle`](https://docs.rs/tauri/latest/tauri/struct.AppHandle.html) 获取：

```rust
  .setup(|app| {
    // 指定的路径必须遵循 `tauri.conf.json > bundle > resources` 中定义的相同语法
    let resource_path = app.path().resolve("lang/de.json", BaseDirectory::Resource)?;

    let json = std::fs::read_to_string(&resource_path).unwrap();
    // 或者在处理 Android 时改用文件系统插件
    // let json = app.fs().read_to_string(&resource_path);

    let lang_de: serde_json::Value = serde_json::from_str(json).unwrap();

    // 这会把 'Guten Tag!' 打印到终端
    println!("{}", lang_de.get("hello").unwrap());

    Ok(())
  })
```

```rust
fn hello(handle: tauri::AppHandle) -> String {
    let resource_path = handle.path().resolve("lang/de.json", BaseDirectory::Resource)?;

    let json = std::fs::read_to_string(&resource_path).unwrap();
    // 或者在处理 Android 时改用文件系统插件
    // let json = handle.fs().read_to_string(&resource_path);

    let lang_de: serde_json::Value = serde_json::from_str(json).unwrap();

    lang_de.get("hello").unwrap()
}
```

### JavaScript

在 JavaScript 侧，你既可以使用上面那样的命令并通过 `await invoke('hello')` 调用它，也可以使用 [`fs` 插件](../../plugin/9-filesystem/)访问这些文件。

使用 [`fs` 插件](../../plugin/9-filesystem/)时，除了[基本设置](../../plugin/9-filesystem/#设置)之外，你还需要配置访问控制列表，启用所需的插件 API 以及访问 `$RESOURCE` 文件夹的权限：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    "fs:allow-resource-read-recursive"
  ]
}
```

{{% alert title="注意" %}}
这里我们使用 `fs:allow-resource-read-recursive` 来允许对完整的 `$RESOURCE` 文件夹、文件及子目录进行完整递归读取访问。
更多信息请阅读[作用域权限](../../plugin/9-filesystem/#作用域)了解其它选项，或阅读[作用域](../../plugin/9-filesystem/#作用域)了解更细粒度的控制。
{{% /alert %}}

```javascript
import { resolveResource } from '@tauri-apps/api/path';
import { readTextFile } from '@tauri-apps/plugin-fs';

const resourcePath = await resolveResource('lang/de.json');
const langDe = JSON.parse(await readTextFile(resourcePath));
console.log(langDe.hello); // 这会把 'Guten Tag!' 打印到 devtools 控制台
```

## 权限

由于使用列表形式时我们会把相对路径中的 `../` 替换为 `_up_`、把绝对路径的根替换为 `_root_`，
这些文件会位于资源目录下的子文件夹中。
要在 Tauri 的[权限系统](../../security/4-capabilities/)中允许这些路径，
请使用 `$RESOURCE/**/*` 来允许对这些文件的递归访问。

### 示例

打包这样一个文件：

```json
{
  "bundle": {
    "resources": ["../relative/path/to/jsonfile.json"]
  }
}
```

配合 [`fs` 插件](../../plugin/9-filesystem/)使用：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-stat",
    "fs:allow-read-text-file",
    "fs:allow-resource-read-recursive",
    {
      "identifier": "fs:scope",
      "allow": ["$RESOURCE/**/*"],
      "deny": ["$RESOURCE/secret.txt"]
    }
  ]
}
```

配合 [`opener` 插件](../../plugin/18-opener/)使用：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    {
      "identifier": "opener:allow-open-path",
      "allow": [
        {
          "path": "$RESOURCE/**/*"
        }
      ]
    }
  ]
}
```
