# Renamer 批量文件处理工具集

## 项目简介
本项目提供了一组用于批量处理文件名的Python工具，适用于 Windows 和 Linux（Ubuntu 24）环境，支持文件名前缀的批量添加、去除，以及目录文件列表的导出。

## 功能说明
- **文本文件分割**：将大文本文件按指定行数分割成多个小文件，便于处理
- **renamer.py**：批量为文件名添加"首字母+空格"前缀（支持中文拼音首字母），可选择预览或实际重命名。
- **remove_prefix.py**：批量去除文件名的"单大写字母+空格"前缀，支持预览和日志。
- **list_files.py**：导出当前目录下所有文件（排除bat、txt、ps1脚本）的完整文件名列表，支持输出到剪贴板或txt文件。

## 环境依赖
- Python 3.7 及以上
- 依赖包：
  - pypinyin
  - pyperclip

安装依赖：
```shell
pip install -r requirements.txt
```

## 各脚本用法

### 1. 批量添加前缀（renamer.py）

### 2. 文本文件分割（split_txt.py）
```shell
python split_txt.py -f 文件路径 [-n 行数]  # 默认每100行分割一个文件
```
- 分割后的文件名格式为：原文件名_序号.扩展名
- 日志直接输出到控制台
```shell
python renamer.py -d 目录路径           # 实际重命名
python renamer.py -d 目录路径 -p        # 预览模式，不实际重命名
```
- 日志输出在脚本同目录下的 `log.txt`

### 2. 批量去除前缀（remove_prefix.py）
```shell
python remove_prefix.py -d 目录路径           # 实际去除前缀
python remove_prefix.py -d 目录路径 -p        # 预览模式，不实际重命名
```
- 日志输出在脚本同目录下的 `remove_prefix_log.txt`

### 3. 导出文件列表（list_files.py）
```shell
python list_files.py -d 目录路径              # 输出到剪贴板
python list_files.py -d 目录路径 -o 文件名.txt # 输出到指定txt文件
```
- 默认输出到剪贴板（需已安装pyperclip），如未安装会有提示。
- 只导出当前目录下的文件，不递归，不包含目录，排除bat、txt、ps1文件。

## 注意事项
- Windows 下建议用 PowerShell 或 CMD 运行脚本。
- Ubuntu 下直接用终端运行。
- 文件操作涉及重命名，请提前备份重要数据。

---
如有问题或建议，欢迎反馈！