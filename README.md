# DownGit - GitHub 仓库下载工具

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)

一个通过 GitHub API 下载仓库中某一文件/文件夹的 Python 工具（而不用下载整个仓库），的支持递归下载整个目录结构。

## ✨ 功能特性

- 递归下载 GitHub 仓库任意目录
- 保留原始文件目录结构
- 支持私有仓库（需配置 Token）
- 自定义本地保存路径
- 实时下载进度显示

## 🛠 安装使用

### 1.安装所需库
```bash
pip install requests
```

### 2. 获取 GitHub Token

由于 GitHub API 未登录请求限制较多（每小时仅 60 次），建议使用 **Personal Access Token** 提升限额：

1. 登录 GitHub。
2. 进入 **Settings → Developer settings → Personal access tokens → Tokens (classic)**。
3. 点击 **Generate new token**，填写名称，权限可只勾选 `repo`（公共仓库可不勾选权限）。
4. 复制生成的 Token

### 3. 修改脚本

在脚本中找到：

```
GITHUB_TOKEN = "填自己的"
```

将 `"填自己的"` 替换为你自己的 Token。

### 4. 运行脚本

```
python downgit.py
```

按照提示输入：

```
请输入 GitHub 仓库完整链接: https://github.com/owner/repo/tree/master/path/to/dir
请输入下载内容要保存的文件夹名或相对路径(如a/b/c,则会生成3层目录): myfolder
```

下载完成会显示：

```
ok
```

## 示例

例如，下载 `https://github.com/user/project/tree/master/docs` 下的所有文件：

```
请输入 GitHub 仓库完整链接: https://github.com/user/project/tree/master/docs
请输入下载内容要保存的文件夹名或相对路径(如a/b/c,则会生成3层目录): docs_backup
```

目录结构将会是：

```
project/
└── docs_backup/
    ├── file1.md
    ├── file2.md
    └── subdir/
        └── file3.md
```

## 注意事项

- 如果下载路径包含子目录，请务必使用 **GitHub 仓库网页中复制的完整链接**。
- 下载失败的文件会在控制台显示警告信息，但不会影响其他文件的下载。

## 更新日志
### 2025-08-12
* 修改了文件保存路径
* 修改了原本写死的master分支，改为自动判断
* 修复了递归路径无法正常识别的问题