+++
title = "6 在 Neovim 中调试"
date = 2026-09-25T21:31:08+08:00
weight = 16
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/debug/neovim/](https://tauri.app/develop/debug/neovim/)

在 Neovim 中调试 Rust 代码有很多不同的插件可用。本指南将展示如何配置 `nvim-dap` 以及一些附加插件来调试 Tauri 应用。

### 前置条件

`nvim-dap` 扩展需要 `codelldb` 二进制文件。请从 https://github.com/vadimcn/codelldb/releases 下载适合你系统的版本并解压。稍后我们会在 `nvim-dap` 配置中指向它。

### 配置 nvim-dap

安装 [`nvim-dap`](https://github.com/mfussenegger/nvim-dap) 和 [`nvim-dap-ui`](https://github.com/rcarriga/nvim-dap-ui) 插件。按照它们 GitHub 页面上的说明操作，或者直接使用你喜欢的插件管理器。
注意 `nvim-dap-ui` 需要 `nvim-nio` 插件。

接下来，在你的 Neovim 配置中设置该插件：

```lua

dap.adapters.codelldb = {
  type = 'server',
  port = "${port}",
  executable = {
    -- 改成你的路径！
    command = '/opt/codelldb/adapter/codelldb',
    args = {"--port", "${port}"},
  }
}

dap.configurations.rust= {
  {
    name = "Launch file",
    type = "codelldb",
    request = "launch",
    program = function()
      return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/target/debug/', 'file')
    end,
    cwd = '${workspaceFolder}',
    stopOnEntry = false
  },
}
```

这套配置会在你每次启动调试器时，要求你指向想要调试的 Tauri 应用二进制文件。

可选地，你可以配置 `nvim-dap-ui` 插件，让它在每次调试会话开始和结束时自动切换调试器视图：

```lua
dapui.setup()

dap.listeners.before.attach.dapui_config = function()
  dapui.open()
end
dap.listeners.before.launch.dapui_config = function()
  dapui.open()
end
dap.listeners.before.event_terminated.dapui_config = function()
  dapui.close()
end
dap.listeners.before.event_exited.dapui_config = function()
  dapui.close()
end

```

最后，你可以修改断点在编辑器中的默认显示方式：

```lua
vim.fn.sign_define('DapBreakpoint',{ text ='🟥', texthl ='', linehl ='', numhl =''})
vim.fn.sign_define('DapStopped',{ text ='▶️', texthl ='', linehl ='', numhl =''})
```

### 启动开发服务器

由于我们不使用 Tauri CLI 启动应用，开发服务器不会自动启动。要在 Neovim 中控制开发服务器的状态，你可以使用 [overseer](https://github.com/stevearc/overseer.nvim/tree/master) 插件。

控制后台任务的最好方式是使用 [VS Code 风格任务](https://github.com/stevearc/overseer.nvim/blob/master/doc/guides.md#vs-code-tasks)配置。为此，请在项目目录中创建 `.vscode/tasks.json` 文件。

下面是使用 `trunk` 的项目的示例任务配置。

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "process",
      "label": "dev server",
      "command": "trunk",
      "args": ["serve"],
      "isBackground": true,
      "presentation": {
        "revealProblems": "onProblem"
      },
      "problemMatcher": {
        "pattern": {
          "regexp": "^error:.*",
          "file": 1,
          "line": 2
        },
        "background": {
          "activeOnStart": false,
          "beginsPattern": ".*Rebuilding.*",
          "endsPattern": ".*server listening at:.*"
        }
      }
    }
  ]
}
```

### 示例键位绑定

下面是启动和控制调试会话的示例键位绑定。

```lua
vim.keymap.set('n', '<F6>', function() dap.disconnect({ terminateDebuggee = true }) end)
vim.keymap.set('n', '<F10>', function() dap.step_over() end)
vim.keymap.set('n', '<F11>', function() dap.step_into() end)
vim.keymap.set('n', '<F12>', function() dap.step_out() end)
vim.keymap.set('n', '<Leader>b', function() dap.toggle_breakpoint() end)
vim.keymap.set('n', '<Leader>o', function() overseer.toggle() end)
vim.keymap.set('n', '<Leader>R', function() overseer.run_template() end)
```
