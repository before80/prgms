+++
title = "第41章：Apache"
weight = 410
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第四十一章：Apache

Apache HTTP Server（俗称 Apache）是资历最老的 Web 服务器之一——1995 年诞生，而 Nginx 要到 2004 年才出现。近些年 Nginx 在份额上增长很快，但 Apache 凭借丰富的模块生态和 `.htaccess` 的灵活性（不重载服务器就能改配置，WordPress 这类 CMS 尤其依赖它），依旧稳稳占着一大块地盘。

> 本章配套视频：Apache配置全攻略，搞定它就能搞定大部分Web服务。

## 41.1 Apache 安装

### 41.1.1 apt install apache2

Ubuntu/Debian安装Apache：

```bash
# 安装
sudo apt update
sudo apt install apache2

# 查看版本
apache2 -v
```

```bash
Server version: Apache/2.4.52 (Ubuntu)
Server built:   2023-10-26T13:58:16
```

```bash
# 启动并设置开机自启
sudo systemctl start apache2
sudo systemctl enable apache2

# 查看状态
sudo systemctl status apache2
```

```bash
apache2.service - The Apache HTTP Server
   Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2026-03-23 10:00:00 CST; 1min 30s ago
```

安装完成后，访问服务器IP，应该能看到Apache的默认欢迎页面。

### 41.1.2 a2enmod：启用模块

Apache 的功能几乎都靠模块拼装。Debian / Ubuntu 上用 `a2enmod`（apache2 enable module）来开关模块：

```bash
# 查看已启用的模块（-M 列出模块，-V 显示编译与版本信息）
apache2ctl -M

# 等价写法
apachectl -M
```

```text
Loaded Modules:
 core_module (static)
 so_module (static)
 ...
 rewrite_module (shared)
 ssl_module (shared)
```

```bash
# 查看有哪些模块可以启用
ls /etc/apache2/mods-available/

# 启用模块
sudo a2enmod rewrite        # URL 重写
sudo a2enmod ssl            # HTTPS
sudo a2enmod headers        # 修改响应头
sudo a2enmod proxy          # 反向代理
sudo a2enmod proxy_fcgi     # 转发给 php-fpm 等 FastCGI 后端

# 禁用模块
sudo a2dismod rewrite
```

改完模块**必须让 Apache 重新读取配置**才生效：

```bash
# 先测语法，再重载（reload 是优雅的，不会断开已有连接）
sudo apache2ctl configtest
sudo systemctl reload apache2
```

> `a2enmod` 做的事其实很简单：在 `/etc/apache2/mods-enabled/` 里建两个软链接，指向 `mods-available/` 里对应的 `.load`（怎么加载模块）和 `.conf`（模块配置）。所以"启用了模块却不生效"，多半是改完忘了 `reload`，或者主配置里缺了 `IncludeOptional mods-enabled/*.load`。
>
> 另外注意：`a2enmod php8.1` 只有在装过 `libapache2-mod-php8.1` 之后才有意义——`a2enmod` 只负责启用，不会帮你把软件包装上。

## 41.2 Apache 目录结构

### 41.2.1 /etc/apache2/

Apache的配置目录结构：

```bash
ls -la /etc/apache2/
```

```bash
apache2.conf        # 主配置文件
envvars             # 环境变量
ports.conf          # 端口配置
conf-available/     # 可用配置
conf-enabled/       # 已启用配置
mods-available/     # 可用模块
mods-enabled/       # 已启用模块
sites-available/    # 可用站点
sites-enabled/      # 已启用站点
magic
```

### 41.2.2 apache2.conf：主配置

```bash
# 查看主配置文件
cat /etc/apache2/apache2.conf
```

```bash
# 主配置文件包含以下内容
ServerRoot "/etc/apache2"
Mutex file:${APACHE_LOCK_DIR} default
PidFile ${APACHE_PID_FILE}
Timeout 300
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 5

# 这些是模块加载
IncludeOptional mods-enabled/*.load
IncludeOptional mods-enabled/*.conf

# 用户/组
User ${APACHE_RUN_USER}
Group ${APACHE_RUN_GROUP}

# 引入配置
Include ports.conf
IncludeOptional conf-enabled/*.conf
IncludeOptional sites-enabled/*.conf
```

## 41.3 虚拟主机配置

### 41.3.1 sites-available/：编写站点配置

```bash
# 创建虚拟主机配置文件
sudo vim /etc/apache2/sites-available/example.com.conf
```

```apache
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/example.com

    ErrorLog ${APACHE_LOG_DIR}/example.com.error.log
    CustomLog ${APACHE_LOG_DIR}/example.com.access.log combined

    <Directory /var/www/example.com>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

关键配置项：

- `ServerName`：主域名；`ServerAlias`：别名（让多个域名指向同一站点）
- `DocumentRoot`：网站根目录
- `<Directory ...>`：对该目录的访问控制
- `Options -Indexes`：禁止目录浏览。少了它，目录里没有 `index.html` 时就会把文件清单列出来
- `AllowOverride All`：允许该目录下用 `.htaccess` 覆盖配置（WordPress 这类 CMS 需要，严格说只需要 `FileInfo`）
- `Require all granted`：Apache 2.4 的授权语法，表示允许所有人访问

> **老教程里的 `Order allow,deny` / `Allow from all` 在 2.4 上已经失效**，那是 2.2 时代的写法。看到这两种语法混在一起，说明配置是从不同年代抄来的。
>
> 另外 `Options +FollowSymLinks` 和 `+SymLinksIfOwnerMatch` 有区别：前者允许跟随指向任何位置的软链接，后者要求软链接的属主与 Apache 运行用户一致。共享主机场景下后者更安全，代价是每个请求都要多做一次检查。

### 41.3.2 sites-enabled/：启用与禁用站点

`a2ensite` / `a2dissite` 负责在 `sites-enabled/` 里建立或删除软链接：

```bash
# 启用站点
sudo a2ensite example.com.conf

# 禁用站点
sudo a2dissite example.com.conf

# 先测语法，再让配置生效
sudo apache2ctl configtest
sudo systemctl reload apache2
```

```bash
# 确认已经启用
ls -l /etc/apache2/sites-enabled/
```

```text
000-default.conf -> /etc/apache2/sites-available/000-default.conf
example.com.conf -> /etc/apache2/sites-available/example.com.conf
```

> **改站点配置只需要 `reload`。** `restart` 会短暂中断服务，只有改监听端口、换模块、换 MPM 时才需要。
>
> 还要注意上面那个 `000-default.conf`：它是装 Apache 时自带的默认站点，监听 `*:80` 且没有 `ServerName` 限制。当请求的 `Host` 匹配不上任何 `ServerName` 时，Apache 会交给**第一个加载的** VirtualHost，通常就是它。生产环境一般直接 `sudo a2dissite 000-default` 关掉。

## 41.4 .htaccess：目录级配置

`.htaccess` 是 Apache 特有的"分布式配置文件"：放进网站目录就能生效，**不用改主配置、也不用重启服务**。WordPress、Drupal 这类 CMS 大量依赖它做 URL 重写等事，这也是不少人选 Apache 的理由。

```apache
# .htaccess 示例：禁止访问敏感文件
<FilesMatch "\.(env|log|ini|conf)$">
    Require all denied
</FilesMatch>

# 禁止访问以点开头的隐藏文件（.git、.env 等）
<FilesMatch "^\.">
    Require all denied
</FilesMatch>

# 启用 URL 重写
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
</IfModule>
```

想让它生效，前提是所在目录的 `AllowOverride` 不是 `None`：

```apache
<Directory /var/www/example.com>
    # All = 允许覆盖所有类别的指令
    AllowOverride All
</Directory>
```

> **`AllowOverride All` 是"方便"换来的取舍，代价值得知道：**
>
> - **性能**：Apache 处理每个请求时，都要从站点根目录一路往下逐个检查每一层的 `.htaccess`。目录越深、文件越多，这个开销越明显
> - **安全**：能写 `.htaccess` 就等于能在你的服务器上改配置。如果站点允许用户上传文件、又没限制上传目录的执行权限，攻击者可以塞一个 `.htaccess` 把某个脚本按 PHP 执行
>
> 所以两条建议：能用主配置解决就别用 `.htaccess`；确实需要时，把 `AllowOverride` 收窄到真正需要的类别（最常见的是 `AllowOverride FileInfo`，够 WordPress 重写用），而不是一律 `All`。

## 41.5 重写规则

### 41.5.1 mod_rewrite

mod_rewrite是Apache最强大的URL重写模块。

```bash
# 确保已启用rewrite模块
sudo a2enmod rewrite
```

### 41.5.2 RewriteRule 与常用 flag

基本语法：

```apache
RewriteRule 匹配模式 替换目标 [flags]
```

```apache
# 永久重定向（返回 301，地址栏会变）
RewriteRule ^old-page\.html$ /new-page.html [R=301,L]

# 临时重定向（返回 302）
RewriteRule ^news/(.*)$ /articles/$1 [R=302,L]

# 内部重写（地址栏不变，浏览器完全察觉不到）
RewriteRule ^api/v1/(.*)$ /api/v2/$1 [L]
```

常用 flag：

| Flag | 说明 |
|------|------|
| `R=301` / `R=302` | 发送重定向（永久 / 临时）。不写 `R` 就是内部重写 |
| `L` | Last，本轮的规则匹配到此停止（但在 `.htaccess` 里，重写后的结果还会被重新处理一轮） |
| `END` | 彻底停止，不再重新处理。想"重写完就结束"，`END` 比 `L` 更可靠 |
| `NC` | No Case，匹配时不区分大小写 |
| `QSA` | Query String Append，把原 URL 的查询串接到新地址后面 |
| `NE` | No Escape，不对替换结果里的特殊字符做转义（需要保留 `#`、`?` 时用） |
| `F` | Forbidden，直接返回 403 |
| `G` | Gone，直接返回 410（资源已永久移除） |
| `P` | Proxy，把请求交给 mod_proxy 转发（需要启用 proxy 模块） |

`RewriteCond` 是 `RewriteRule` 的条件，可以叠加多条（默认是"并且"，加 `[OR]` 变成"或者"）：

```apache
# 只有文件、目录都不存在时，才把请求交给 index.php 处理
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
```

**WordPress 的 .htaccess**（最常见的 RewriteRule 用法）：

```apache
# /var/www/example.com/.htaccess
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /

    # 统一到 www + HTTPS
    RewriteCond %{HTTPS} off [OR]
    RewriteCond %{HTTP_HOST} !^www\. [NC]
    RewriteCond %{HTTP_HOST} ^(?:www\.)?(.+)$ [NC]
    RewriteRule ^ https://www.%1%{REQUEST_URI} [R=301,L]

    # WordPress 固定链接：交给 index.php 处理
    RewriteRule ^index\.php$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.php [L]
</IfModule>
```

> 这里顺便指出一个真实的坑。网上很常见的写法只有两条条件：
>
> ```apache
> RewriteCond %{HTTPS} off [OR]
> RewriteCond %{HTTP_HOST} !^www\. [NC]
> RewriteRule ^(.*)$ https://www.%{HTTP_HOST}/$1 [R=301,L]
> ```
>
> 它的问题是：当请求"已经是 HTTPS，但域名本来就没带 www"时没毛病；可如果遇到"HTTP + 域名已经带 www"，替换目标里再拼一次 `www.` 就会得到 `https://www.www.example.com/...`。上面先用 `%{HTTP_HOST} ^(?:www\.)?(.+)$` 把可选的 `www.` 吃掉、再用 `%1` 引用，就不会重复了。

## 41.6 认证配置

### 41.6.1 Basic Auth

HTTP Basic 认证是最简单的 Web 认证方式：浏览器弹出用户名密码框，把 `用户名:密码` 用 Base64 编码后放进 `Authorization` 请求头发给服务器。

```bash
# 用 -c 初始化密码文件（-c 会覆盖已有文件，只在第一次用！）
sudo htpasswd -c /etc/apache2/.htpasswd admin

# 之后追加用户，千万不要再带 -c
sudo htpasswd /etc/apache2/.htpasswd anotheruser

# 用 bcrypt 存储（比默认的 apr1/MD5 更抗暴力破解）
sudo htpasswd -B /etc/apache2/.htpasswd admin
```

密码文件内容大致是这样（哈希值仅为示例）：

```text
admin:$apr1$Zx8kQ2nQ$T1lq9m0Hd2oP4yV7bJ2uX0
anotheruser:$2y$05$kQ3mD9pY1sV7cL2nR8tZa.6dU4wE9fB1gH3jK5mN7oP
```

> `$apr1$` 是 MD5 变体，`$2y$` 是 bcrypt（用 `-B` 参数生成）。另外这个文件**必须放在网站根目录之外**（`/etc/apache2/` 正合适），否则可能被人直接下载走。

在 `.htaccess` 或 `VirtualHost` 里启用：

```apache
# .htaccess
AuthType Basic
AuthName "Restricted Area"
AuthUserFile /etc/apache2/.htpasswd
Require valid-user
```

```apache
<Directory /var/www/example.com/admin>
    AuthType Basic
    AuthName "Admin Panel"
    AuthUserFile /etc/apache2/.htpasswd
    Require valid-user
</Directory>
```

> **必须配合 HTTPS 使用。** Basic 认证只是把密码做了 Base64 编码，**这不是加密**——Base64 解码是零门槛的，网络中间人抓包就直接看到明文密码。所以 Basic Auth 一定要跑在 TLS 之上（内网也建议如此）。
>
> 改完配置记得 `sudo systemctl reload apache2`。

### 41.6.2 Digest Auth：了解即可

Digest 认证传输的是密码摘要而不是密码本身，理论上比 Basic 安全：

```bash
# 需要启用 auth_digest 模块
sudo a2enmod auth_digest

# 用 htdigest 创建密码文件，必须指定"域"（realm）名字，且要和配置里的 AuthName 一致
sudo htdigest -c /etc/apache2/.htdigest "Admin Area" admin
```

> 但**实际项目中很少用它**：Digest 基于 MD5，早已被认为不够强；浏览器端的体验、后端集成也都比较麻烦（很多人第一次配 Digest 会被"realm 名字不一致就登录失败"卡住）。现实中的选择通常是 **Basic Auth + HTTPS**，或者干脆上 OAuth / OIDC 这类统一认证。

## 41.7 模块管理

### 41.7.1 a2enmod

```bash
# 语法：a2enmod 模块名
sudo a2enmod module_name

# 常用示例
sudo a2enmod ssl                          # HTTPS 支持
sudo a2enmod headers                      # 用 Header 指令改响应头
sudo a2enmod rewrite                      # URL 重写
sudo a2enmod proxy proxy_http proxy_fcgi   # 反向代理 / 转发给 php-fpm
sudo a2enmod deflate                      # 响应压缩（相当于 Nginx 的 gzip）
sudo a2enmod expires                      # 用 Expires 头控制缓存
sudo a2enmod remoteip                     # 还原经过代理后的真实客户端 IP
```

> `a2enmod` 只是建立软链接，**不会安装软件包**。比如 `a2enmod php8.3` 需要先装好 `libapache2-mod-php8.3`；启用 `proxy_fcgi` 之后，一般还要配 `SetHandler "proxy:unix:/run/php/php8.3-fpm.sock|fcgi://localhost"` 才能真正把请求交给 php-fpm。

### 41.7.2 a2dismod

```bash
# 语法：a2dismod 模块名
sudo a2dismod module_name

# 常用示例：关掉用不上的模块，减小攻击面
sudo a2dismod autoindex        # 目录浏览
sudo a2dismod status           # /server-status 状态页
sudo a2dismod userdir          # 每个用户家目录下的站点（/~user）
sudo a2dismod cgi              # 老式 CGI
```

> 关掉模块后同样要 `sudo apache2ctl configtest && sudo systemctl reload apache2`。**没把握就别乱关**——有些模块（如 `mpm_*`、`authz_core`）是必需的，关掉会直接起不来。
## 41.8 MPM：Apache 的并发模型

MPM（Multi-Processing Module）决定 Apache 怎么处理并发连接，直接影响性能与内存占用。Apache 2.4 有三种。

### 41.8.1 prefork：一个请求一个进程

最传统的模式：每个请求交给一个独立的子进程。进程之间完全隔离，某个请求出问题不影响别人；代价是内存开销大（每个进程几 MB 起步），高并发下内存很快见底。

```bash
# 查看当前使用的 MPM
apache2ctl -V | grep -i "Server MPM"

# 查看已加载的 MPM 模块
apache2ctl -M | grep mpm_
```

```apache
# 实际配置文件在 /etc/apache2/mods-available/mpm_prefork.conf
<IfModule mpm_prefork_module>
    StartServers             5
    MinSpareServers          5
    MaxSpareServers         10
    MaxRequestWorkers      150
    MaxConnectionsPerChild   0
</IfModule>
```

- `StartServers`：启动时预先创建的进程数
- `MinSpareServers` / `MaxSpareServers`：空闲进程数的上下限，Apache 会在这个范围内动态增减
- `MaxRequestWorkers`：**同时处理的请求数上限**。prefork 下就等于进程数上限，设太大内存会爆
- `MaxConnectionsPerChild`：一个子进程处理多少个连接后自我销毁（防止内存泄漏累积）。旧名字是 `MaxRequestsPerChild`，老教程里常见旧名

> **`MaxRequestWorkers` 该写多少？** 先看单个进程的实际内存占用（`ps` 看 RSS），再按"可用内存 ÷ 单进程占用"估算。比如每个进程 30MB、愿意给 Apache 留 1GB，那大约是 30 出头，而不是无脑写 150。

### 41.8.2 worker：多进程 + 多线程

worker 让每个子进程维护多个线程，一个线程处理一个请求。线程比进程轻得多，同样的内存能撑起更多并发。

```apache
<IfModule mpm_worker_module>
    StartServers             2
    MinSpareThreads         25
    MaxSpareThreads         75
    ThreadLimit             64
    ThreadsPerChild         25
    MaxRequestWorkers      150
    MaxConnectionsPerChild   0
</IfModule>
```

注意 `MaxRequestWorkers` 的含义变了：它是**总线程数上限**，而同一进程内的线程共享内存，所以总体比 prefork 省得多。前提是所用模块必须线程安全。

### 41.8.3 event：现代默认，专治长连接

event 建立在 worker 之上，额外解决了一个老问题：**Keep-Alive 的空闲连接不再占着工作线程**。在 worker / prefork 下，客户端连上来但暂时不发请求，它占用的线程或进程就干等着；连接一多，工作单元被"闲人"占满，新用户就被拒。event 用一个专门的监听线程接管这类连接，工作线程只处理真正有数据的请求。

```apache
<IfModule mpm_event_module>
    StartServers             2
    MinSpareThreads         25
    MaxSpareThreads         75
    ThreadLimit             64
    ThreadsPerChild         25
    MaxRequestWorkers      150
    MaxConnectionsPerChild   0
</IfModule>
```

> **怎么选？** 现代系统（Debian 12 / Ubuntu 22.04 及以后）默认就是 event，一般不用动。
>
> 唯一常见的例外是 **mod_php**：它把 PHP 解释器嵌进 Apache，不是线程安全的，因此**只能配 prefork**。这也是"用了 mod_php 就享受不到 event 优势"的原因。更好的做法是让 Apache 通过 `proxy_fcgi` 把请求转给独立的 `php-fpm` 进程，这样就能安心用 event。

```bash
# 查看 MPM 是否为编译默认值
apache2ctl -V | grep -i "Server MPM"

# 切换 MPM：必须先禁用当前的，再启用新的（两个 MPM 不能同时启用）
sudo a2dismod mpm_prefork
sudo a2enmod mpm_event
sudo apache2ctl configtest
sudo systemctl restart apache2      # 换 MPM 必须 restart，reload 不够
```

---
---

## 本章小结

本章把 Apache 的日常操作走了一遍：

- **安装**：`apt install apache2`；用 `systemctl` 管理服务，`apache2ctl configtest` 检查语法
- **模块管理**：`a2enmod` / `a2dismod` 开关模块（本质是 `mods-enabled/` 里的软链接），改完要 `reload`
- **目录结构**：`/etc/apache2/` 下 `apache2.conf` 是主入口，`ports.conf` 管端口，`*-available` 与 `*-enabled` 成对出现
- **虚拟主机**：在 `sites-available/` 写配置，用 `a2ensite` 启用；同端口下第一个加载的 VirtualHost 是默认站点，记得处理 `000-default`
- **`.htaccess`**：目录级配置，灵活但每请求都要逐层查找解析，也带来安全风险；能用主配置就别用，`AllowOverride` 尽量收窄
- **重写**：`RewriteRule` + `RewriteCond`，`[R=301,L]` 跳转、`[L]` 停止、`[END]` 彻底结束；也要留意上面 41.5.2 指出的重复拼 `www.` 的坑
- **认证**：`htpasswd` 做 Basic（务必配 HTTPS），`htdigest` 做 Digest（了解即可，实际少用）
- **MPM**：prefork（进程模型、内存开销大）、worker（进程 + 线程）、event（现代默认，长连接友好）；mod_php 只能配 prefork，更推荐改用 php-fpm

Apache 和 Nginx 不是非此即彼：Apache 的 `.htaccess` 与模块生态让老应用、CMS 部署起来很省心；Nginx 在高并发、静态资源和反向代理上更省资源。真实架构里两者经常同时出现——前面用 Nginx 做入口和负载均衡，后面用 Apache 承载那些依赖 `.htaccess` 的应用。
