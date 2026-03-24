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

Apache HTTP Server（俗称Apache）是世界上部署最广泛的Web服务器之一，资历比互联网还老——它1995年就诞生了，Nginx那时候还没出生。虽然近年来Nginx的份额在上升，但Apache凭借其丰富的功能和.htaccess的便利性（不用重载服务器就能改配置，WordPress用户爱死它了），仍然是很多场景的首选。

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

### 41.1.2 a2enmod 启用模块

Apache通过模块扩展功能，用`a2enmod`启用模块：

```bash
# 查看已启用模块
apache2ctl -M
```

```bash
Loaded Modules:
 core_module (static)
 so_module (static)
 ...

# 查看所有可用模块
ls /etc/apache2/mods-available/

# 启用模块
sudo a2enmod rewrite          # 启用URL重写
sudo a2enmod ssl              # 启用SSL/TLS
sudo a2enmod headers          # 启用HTTP头修改
sudo a2enmod proxy            # 启用代理模块
sudo a2enmod proxy_fcgi       # 启用FastCGI代理

# 禁用模块
sudo a2dismod rewrite

# 重启Apache使模块生效
sudo systemctl restart apache2
```

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

### 41.3.1 sites-available/

在`sites-available/`目录创建虚拟主机配置：

```bash
# 创建虚拟主机配置文件
sudo vim /etc/apache2/sites-available/example.com.conf
```

```bash
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/example.com

    # 日志
    ErrorLog ${APACHE_LOG_DIR}/example.com.error.log
    CustomLog ${APACHE_LOG_DIR}/example.com.access.log combined

    # 默认目录设置
    <Directory /var/www/example.com>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

关键配置项：

- `ServerName`：主域名
- `ServerAlias`：别名（可选）
- `DocumentRoot`：网站根目录
- `Directory`：目录权限配置
- `Options -Indexes`：禁止目录浏览（安全加固）
- `AllowOverride All`：允许.htaccess覆盖配置（WordPress必需）

### 41.3.2 sites-enabled/

启用站点：用`a2ensite`创建符号链接，用`a2dissite`删除。

```bash
# 启用站点
sudo a2ensite example.com.conf

# 禁用站点
sudo a2dissite example.com.conf

# 重载配置
sudo systemctl reload apache2

# 重启服务
sudo systemctl restart apache2
```

```bash
# 查看已启用站点
ls -la /etc/apache2/sites-enabled/
```

```bash
lrwxrwxrwx 1 root root 33 Mar 23 10:00 000-default.conf -> /etc/apache2/sites-available/000-default.conf
lrwxrwxrwx 1 root root 33 Mar 23 10:05 example.com.conf -> /etc/apache2/sites-available/example.com.conf
```

## 41.4 .htaccess：目录级配置

.htaccess是Apache的"分布式配置文件"——它放在网站目录里，不需要重启Apache就能生效。它就像贴在门上的便利贴，你想改什么规则，直接贴上去就行，不用去找物业（服务器管理员）拿钥匙开门。

> **为什么重要**：WordPress、Drupal等CMS系统大量依赖.htaccess实现URL重写、缓存控制等功能。

```bash
# .htaccess示例：禁止访问敏感文件
<FilesMatch "\.(env|log|ini|conf)$">
    Require all denied
</FilesMatch>

# 禁止访问隐藏文件
<FilesMatch "^\.">
    Require all denied
</FilesMatch>

# 启用URL重写
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
</IfModule>
```

> **AllowOverride**：.htaccess能否生效，取决于Directory配置中的`AllowOverride`参数。如果设置为`None`，.htaccess会被完全忽略。

```bash
# 在VirtualHost或Directory配置中
<Directory /var/www/example.com>
    AllowOverride All    # 允许.htaccess覆盖所有配置
</Directory>
```

## 41.5 重写规则

### 41.5.1 mod_rewrite

mod_rewrite是Apache最强大的URL重写模块。

```bash
# 确保已启用rewrite模块
sudo a2enmod rewrite
```

### 41.5.2 RewriteRule

RewriteRule的基本语法：

```bash
RewriteRule Pattern Substitution [flags]
```

```bash
# 永久重定向
RewriteRule ^old-page\.html$ /new-page.html [R=301,L]

# 临时重定向
RewriteRule ^news/(.*)$ /articles/$1 [R=302,L]

# 内部重写（URL不变）
RewriteRule ^api/v1/(.*)$ /api/v2/$1 [L]
```

常用flag：

| Flag | 说明 |
|------|------|
| R=301 | 301永久重定向 |
| R=302 | 302临时重定向 |
| L | Last，最后一条规则 |
| NC | 不区分大小写 |
| QSA | 追加查询字符串 |

**WordPress的.htaccess**（最常见的RewriteRule配置）：

```bash
# /var/www/example.com/.htaccess
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /

    # 强制HTTPS
    RewriteCond %{HTTPS} off [OR]
    RewriteCond %{HTTP_HOST} !^www\. [NC]
    RewriteRule ^(.*)$ https://www.%{HTTP_HOST}/$1 [R=301,L]

    # WordPress固定链接
    RewriteRule ^index\.php$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.php [L]
</IfModule>
```

## 41.6 认证配置

### 41.6.1 Basic Auth

HTTP Basic认证是最简单的Web认证方式：

```bash
# 创建密码文件（首次需要加-c参数）
sudo htpasswd -c /etc/apache2/.htpasswd admin

# 添加新用户
sudo htpasswd /etc/apache2/.htpasswd anotheruser

# 查看密码文件
cat /etc/apache2/.htpasswd
```

```bash
admin:$apr1$8K2nKj$7VxJGH1QjGzD0M1M3KjKj1
anotheruser:$apr1$9M2nKj$7VxJGH1QjGzD0M1M3KjKj2
```

在.htaccess或VirtualHost中配置Basic认证：

```bash
# .htaccess
AuthType Basic
AuthName "Restricted Area"
AuthUserFile /etc/apache2/.htpasswd
Require valid-user
```

或者在VirtualHost中配置：

```bash
<Directory /var/www/example.com/admin>
    AuthType Basic
    AuthName "Admin Panel"
    AuthUserFile /etc/apache2/.htpasswd
    Require valid-user
</Directory>
```

### 41.6.2 Digest Auth

HTTP Digest认证比Basic认证安全（密码不会明文传输），但配置较复杂：

```bash
# 需要启用auth_digest模块
sudo a2enmod auth_digest

# 创建密码文件（需要使用htdigest命令）
sudo htdigest -c /etc/apache2/.htdigest "Admin Area" admin
```

## 41.7 模块管理

### 41.7.1 a2enmod

```bash
# 启用模块
sudo a2enmod module_name

# 示例
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod rewrite
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_fcgi
sudo a2enmod php8.1            # 启用PHP模块（如果有的话）
```

### 41.7.2 a2dismod

```bash
# 禁用模块
sudo a2dismod module_name

# 示例：禁用不需要的模块
sudo a2dismod autoindex        # 禁用目录浏览
sudo a2dismod status           # 禁用服务器状态页面
```

## 41.8 MPM 多进程处理

MPM（Multi-Processing Module）是Apache处理并发连接的核心模块，有三种模式。

### 41.8.1 prefork：多进程

prefork是最传统的MPM模式，每个请求用一个子进程处理，互不干扰。

```bash
# 查看当前使用的MPM
apache2ctl -V | grep -i mpm

# 查看当前加载的MPM模块
apache2ctl -M | grep mpm_
```

```bash
# 在/etc/apache2/mpm-prefork.conf中配置
<IfModule mpm_prefork_module>
    StartServers             5
    MinSpareServers          5
    MaxSpareServers         10
    MaxRequestWorkers      150
    MaxConnectionsPerChild   0
</IfModule>
```

- `StartServers`：启动时创建的子进程数
- `MinSpareServers`：最小空闲进程数
- `MaxSpareServers`：最大空闲进程数
- `MaxRequestWorkers`：最大并发工作进程数
- `MaxConnectionsPerChild`：每个子进程处理的最大连接数（0=无限制）

### 41.8.2 worker：多进程+多线程

worker模式使用多进程+多线程，每个进程有多个线程，更节省内存。

```bash
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

### 41.8.3 event：事件驱动

event是Apache 2.4引入的新MPM，基于worker但专为长连接优化。

```bash
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

> **选择建议**：event模式是未来的主流，就像电动牙刷正在取代手动牙刷——更先进、更省力。但某些老旧的PHP模块（说的就是mod_php）不支持event模式，就像有些老人还是觉得手动牙刷刷得更干净。这种情况下，只能退回worker甚至prefork模式。生产环境建议用event，如果有问题再退回到worker或prefork。

```bash
# 查看Apache编译时默认启用的MPM
apache2ctl -V | grep "MPM"

# 切换MPM（需要先禁用当前MPM）
sudo a2dismod mpm_prefork
sudo a2enmod mpm_event
sudo systemctl restart apache2
```

---

## 本章小结

本章我们全面学习了Apache的配置：

- **Apache安装**：`apt install apache2`，`a2enmod`启用模块
- **目录结构**：`/etc/apache2/`下的配置文件组织
- **apache2.conf**：主配置文件，包含模块加载和配置引入
- **虚拟主机**：sites-available/创建配置，a2ensite启用
- **.htaccess**：分布式配置文件，AllowOverride控制是否生效
- **重写规则**：mod_rewrite模块，RewriteRule语法，WordPress固定链接
- **认证配置**：Basic Auth（htpasswd），Digest Auth（htdigest）
- **模块管理**：a2enmod启用，a2dismod禁用
- **MPM多进程处理**：prefork（多进程）、worker（多进程+多线程）、event（事件驱动）

Apache和Nginx各有优劣。Apache胜在.htaccess的灵活性，Nginx胜在高并发性能。两者都是Linux服务器管理者的必备技能。
