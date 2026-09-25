+++
title = "5 AUR"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/aur/](https://tauri.app/distribute/aur/)

# 发布到 Arch 用户仓库

## 设置

首先前往 `https://aur.archlinux.org` 注册一个账号。请务必添加正确的 ssh 密钥。接着用下面的命令克隆一个空的 git 仓库。

```sh
git clone https://aur.archlinux.org/your-repo-name
```

完成上述步骤后，创建一个名为 `PKGBUILD` 的文件。文件创建好后就可以进入下一步了。

### 编写 PKGBUILD 文件

```ini
pkgname=<pkgname>
pkgver=1.0.0
pkgrel=1
pkgdesc="Description of your app"
arch=('x86_64' 'aarch64')
url="https://github.com/<user>/<project>"
license=('MIT')
depends=('cairo' 'desktop-file-utils' 'gdk-pixbuf2' 'glib2' 'gtk3' 'hicolor-icon-theme' 'libsoup' 'pango' 'webkit2gtk-4.1')
options=('!strip' '!emptydirs')
install=${pkgname}.install
source_x86_64=("${url}/releases/download/v${pkgver}/appname_${pkgver}_amd64.deb")
source_aarch64=("${url}/releases/download/v${pkgver}/appname_${pkgver}_arm64.deb")
```

- 在文件顶部定义你的包名，并把它赋给变量 `pkgname`。
- 设置 `pkgver` 变量。通常最好在 source 变量中使用这个变量，以提高可维护性。
- `pkgdesc` 变量会显示在你 AUR 仓库的页面上，告诉访客你的应用是做什么的。
- `arch` 变量控制哪些架构可以安装你的包。
- `url` 变量虽然不是必需的，但有助于让你的包看起来更专业。
- `install` 变量指定 .install 脚本的名称，该脚本会在安装、移除或升级包时运行。
- `depends` 变量包含让应用能运行所需的依赖列表。对任何 Tauri 应用，你都必须包含上面展示的所有依赖。
- `source` 变量是必需的，它定义你上游软件包的位置。你可以通过在变量名末尾添加架构来让 `source` 成为架构特定的。

### 生成 `.SRCINFO`

要把仓库推送到 AUR，你必须生成一个 `.SRCINFO` 文件。可以用下面的命令完成。

```sh
makepkg --printsrcinfo > .SRCINFO
```

### 测试

测试应用非常简单。你只需在与 `PKGBUILD` 文件相同的目录中运行 `makepkg`，看看它是否能工作。

### 发布

最后，测试阶段结束后，你可以用以下命令把应用发布到 AUR（Arch 用户仓库）。

```sh
git add .

git commit -m "Initial Commit"

git push
```

如果一切顺利，你的仓库现在应该会出现在 AUR 网站上。

## 示例

### 从 Debian 包中提取

```ini
# Maintainer:
# Contributor:
pkgname=<pkgname>
pkgver=1.0.0
pkgrel=1
pkgdesc="Description of your app"
arch=('x86_64' 'aarch64')
url="https://github.com/<user>/<project>"
license=('MIT')
depends=('cairo' 'desktop-file-utils' 'gdk-pixbuf2' 'glib2' 'gtk3' 'hicolor-icon-theme' 'libsoup' 'pango' 'webkit2gtk-4.1')
options=('!strip' '!debug')
install=${pkgname}.install
source_x86_64=("${url}/releases/download/v${pkgver}/appname_${pkgver}_amd64.deb")
source_aarch64=("${url}/releases/download/v${pkgver}/appname_${pkgver}_arm64.deb")
sha256sums_x86_64=('ca85f11732765bed78f93f55397b4b4cbb76685088553dad612c5062e3ec651f')
sha256sums_aarch64=('ed2dc3169d34d91188fb55d39867713856dd02a2360ffe0661cb2e19bd701c3c')
package() {
	# 提取包数据
	tar -xvf data.tar.gz -C "${pkgdir}"

}
```

```ini
post_install() {
	gtk-update-icon-cache -q -t -f usr/share/icons/hicolor
	update-desktop-database -q
}

post_upgrade() {
	post_install
}

post_remove() {
	gtk-update-icon-cache -q -t -f usr/share/icons/hicolor
	update-desktop-database -q
}

```

### 从源码构建

```ini
# Maintainer:
pkgname=<pkgname>-git
pkgver=<pkgver>
pkgrel=1
pkgdesc="Description of your app"
arch=('x86_64' 'aarch64')
url="https://github.com/<user>/<project>"
license=('MIT')
depends=('cairo' 'desktop-file-utils' 'gdk-pixbuf2' 'glib2' 'gtk3' 'hicolor-icon-theme' 'libsoup' 'pango' 'webkit2gtk-4.1')
makedepends=('git' 'openssl' 'appmenu-gtk-module' 'libappindicator-gtk3' 'librsvg' 'cargo' 'pnpm' 'nodejs')
provides=('<pkgname>')
conflicts=('<binname>' '<pkgname>')
source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
	cd <project>
	( set -o pipefail
	  git describe --long --abbrev=7 2>/dev/null | sed 's/\([^-]*-g\)/r\1/;s/-/./g' ||
	  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short=7 HEAD)"
	)
}

prepare() {
	cd <project>
	pnpm install
}

build() {
	cd <project>
	pnpm tauri build -b deb
}

package() {
	cp -a <project>/src-tauri/target/release/bundle/deb/<project>_${pkgver}_*/data/* "${pkgdir}"
}
```
