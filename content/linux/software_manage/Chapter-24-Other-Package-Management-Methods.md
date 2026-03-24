+++
title = "第24章：其他包管理方式"
weight = 240
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第二十四章：其他包管理方式

除了传统的APT、YUM/DNF之外，Linux世界还有很多其他的软件管理方式。

有的像"外卖APP"一样帮你自动下载安装（Snap、Flatpak），有的像"自己做菜"需要从头编译源码（编译安装）。

这一章，我们来聊聊这些"非主流"的包管理方式，扩宽你的Linux视野！

---

## 24.1 Snap 包管理：通用软件包

**Snap**是Canonical（Ubuntu的母公司）推出的通用包管理器。特点是**自包含**——snap包包含了软件运行所需的一切，不依赖系统库。

### 24.1.1 snap install 包名

```bash
# 安装一个snap包（以VS Code为例）
sudo snap install code --classic

# 如果没有snapd，先安装
sudo apt install snapd
```

```bash
# snap install的输出
# 2026-03-23T14:00:00+08:00 INFO Waiting for automatic snapd restart...
# code from VS Code installed
```

> [!NOTE]
> 注意：服务器软件（如nginx、mysql）通常通过apt/yum安装，不需要也不推荐用snap安装。snap适合安装那些官方仓库里没有、但开发者提供了snap包的桌面软件（如VS Code、Slack、Spotify等）。

### 24.1.2 snap list：列出

```bash
# 列出已安装的snap包
snap list

# 输出大概是：
# Name    Version    Rev   Tracking       Publisher   Notes
# core18  20220201   1270  latest/stable    canonical  base
# code    95.0.424   100  latest/stable    vscode    classic
```

### 24.1.3 snap remove：删除

```bash
# 删除code snap包
sudo snap remove code

# 输出：
# code removed
```

### 24.1.4 Snap 换源：国内加速

Snap默认从Canonical服务器下载，在中国可能很慢。可以配置国内镜像：

```bash
# 设置snap镜像（华为云）
sudo snap set system snapshot.root-directory=/var/lib/snapd/snapshots
sudo systemctl restart snapd.service

# 或者使用阿里云的snap源
sudo bash -c 'cat > /etc/apt/sources.list.d/snap-store.list << EOF
deb http://mirrors.aliyun.com/snap/canonical /
EOF'

sudo apt update
```

> [!NOTE]
> Snap的国内镜像配置比较复杂，而且不是所有snap包都能用镜像。如果你在国内，建议优先用apt安装。

---

## 24.2 Flatpak 包管理：沙盒软件

**Flatpak**是另一个通用包管理器，特点是**沙盒隔离**——每个Flatpak应用都运行在独立的环境里，不会影响系统其他部分。

### 24.2.1 flatpak install

```bash
# 安装flatpak（如果还没有）
sudo apt install flatpak

# 添加flathub仓库（最大的Flatpak仓库）
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# 从flathub安装一个应用
flatpak install flathub org.videolan.VLC

# 或者安装GNOME软件中心
flatpak install flathub org.gnome.Software
```

```bash
# 安装过程会提示确认
# Flatpak system operation needs to be authorized by pkexec
# Authentication required to install software
```

### 24.2.2 flathub 仓库

**Flathub**是Flatpak最大的社区仓库，包含成千上万个应用：

```bash
# 搜索应用
flatpak search vlc

# 输出：
# VLC media player    org.videolan.VLC    A multi-platform multimedia player
```

```bash
# 卸载应用
flatpak uninstall org.videolan.VLC

# 更新所有flatpak
flatpak update
```

---

## 24.3 AppImage 便携软件：无需安装

**AppImage**是一种"绿色软件"概念——下载下来就能直接运行，**不需要安装**，也不需要root权限！

### 24.3.1 chmod +x 运行

```bash
# 下载一个AppImage文件
wget https://example.com/app.AppImage

# 赋予执行权限
chmod +x app.AppImage

# 直接运行！
./app.AppImage
```

### 24.3.2 不需要 root

AppImage的独特之处在于：
- **不需要root权限**就能运行
- **不需要安装**到系统
- **不会污染系统环境**
- 可以放在U盘里随身带着走

```bash
# AppImage就像一个"可执行ISO"
# 下载 -> chmod +x -> 运行

# 推荐把AppImage放到 ~/Applications 目录
mkdir -p ~/Applications
mv app.AppImage ~/Applications/
~/Applications/app.AppImage
```

> [!TIP]
> AppImage适合那些系统仓库里没有、或者版本很旧的软件。比如某些开发工具、设计软件等。

---

## 24.4 源码编译安装：configure、make、make install

这是最"硬核"的安装方式——从源代码开始，自己编译、自己安装。

### 24.4.1 安装编译工具：apt install build-essential

```bash
# 安装编译所需的工具链
sudo apt install build-essential

# 这会安装：
# - gcc (C编译器)
# - g++ (C++编译器)
# - make (构建工具)
# - libc6-dev (C库开发文件)
```

```bash
# 验证安装
gcc --version

# 输出大概是：
# gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0
```

### 24.4.2 ./configure：检查环境

```bash
# 1. 下载源码
wget http://nginx.org/download/nginx-1.24.0.tar.gz

# 2. 解压
tar -zxf nginx-1.24.0.tar.gz
cd nginx-1.24.0

# 3. 运行configure脚本，检查编译环境
./configure

# 输出大概是：
# checking for OS
#  + Linux 5.15.0 x86_64
# checking for C compiler ... gcc
# checking for PCRE library ... found
# checking for OpenSSL library ... found
# Configuration summary
#   nginx path prefix: "/usr/local/nginx"
#   nginx binary file: "/usr/local/nginx/sbin/nginx"
#   nginx modules path: "/usr/local/nginx/modules"
#   nginx configuration prefix: "/usr/local/nginx/conf"
```

### 24.4.3 ./configure --prefix=/usr/local：指定安装路径

```bash
# 指定安装到/usr/local/nginx（而不是默认位置）
./configure --prefix=/usr/local/nginx

# 其他常用选项：
# --with-http_ssl_module     启用SSL模块
# --with-http_gzip_module   启用gzip模块
# --with-http_v2_module     启用HTTP/2支持
```

### 24.4.4 make：编译

```bash
# 4. 编译（这步最耗时）
make

# 输出：
# cc -o objs/nginx ./core/nginx.o ...
# cc -o objs/nginx ./http/ngx_http.o ...
# [编译输出省略...]
# objs/nginx was built
```

### 24.4.5 make -j$(nproc)：多核编译

如果你的CPU有很多核心，可以用`-j`参数**并行编译**，大幅加速！

```bash
# 查看CPU核心数
nproc

# 输出：
# 8

# 使用所有核心并行编译
make -j$(nproc)

# 编译速度提升明显！

> [!NOTE]
> 注意：`$(nproc)` 会自动获取CPU核心数，如果是8核，就相当于 `make -j8`。也可以手动指定数字，比如 `make -j4` 表示用4个核心同时编译。

### 24.4.6 make install：安装

```bash
# 5. 安装（需要root权限）
sudo make install

# 安装完成，nginx被安装到 --prefix 指定的目录
/usr/local/nginx/sbin/nginx -v

# 输出：
# nginx version: nginx/1.24.0
```

> [!WARNING]
> 编译安装的软件不受包管理器管理——不会自动更新、卸载麻烦。建议新手尽量用包管理器安装！

---

## 24.5 依赖问题解决：手动安装依赖

编译源码经常遇到"缺库"的问题，configure会报错说找不到某个库。

```bash
# configure报错示例：
# ./configure: error: the HTTP rewrite module requires the PCRE library.
# You can either disable the module by using --without-http_rewrite_module
# option, or install the PCRE library into the system.
```

### 解决方法1：安装缺失的库

```bash
# Debian/Ubuntu
sudo apt install libpcre3-dev libssl-dev zlib1g-dev

# 或者安装所有常用开发库
sudo apt install build-essential libssl-dev libpcre3-dev zlib1g-dev
```

### 解决方法2：禁用需要该库的功能

```bash
# 如果你不需要rewrite功能
./configure --without-http_rewrite_module
```

```bash
# 查看configure的所有选项
./configure --help
```

### 常用开发库对照表

| 库 | Debian/Ubuntu包名 | 用途 |
|---|------------------|------|
| PCRE | `libpcre3-dev` | rewrite模块需要 |
| SSL | `libssl-dev` | HTTPS支持 |
| zlib | `zlib1g-dev` | gzip压缩 |
| libxml2 | `libxml2-dev` | XML解析 |
| libxslt | `libxslt-dev` | XSLT转换 |

---

## 本章小结

本章我们学习了Linux的其他包管理方式：

### 🔑 核心知识点

1. **Snap通用包管理器**：
   - 自包含，不依赖系统库
   - `snap install 包名`：安装
   - `snap list`：列出已安装
   - `snap remove 包名`：卸载

2. **Flatpak沙盒包管理器**：
   - 应用运行在隔离环境
   - `flatpak install flathub 包名`：安装
   - `flatpak update`：更新

3. **AppImage便携软件**：
   - 不需要安装，不需要root
   - `chmod +x xxx.AppImage` 然后 `./xxx.AppImage` 运行

4. **源码编译安装**：
   - 流程：`./configure` -> `make` -> `make install`
   - `make -j$(nproc)` 多核加速
   - 需要手动安装依赖库

### 💡 记住这个原则

> **能用包管理器就用包管理器，编译安装是最后的手段！** 除非你有特殊需求，否则不要轻易尝试源码编译。

---

**当前时间：2026年3月23日 21:52:03**
**已完成"第二十四章"！🎉**

