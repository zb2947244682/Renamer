import os
import argparse

try:
    import pyperclip
    HAS_CLIP = True
except ImportError:
    HAS_CLIP = False

def list_files(directory):
    exclude_ext = {'.bat', '.txt', '.ps1'}
    files = [f for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f))
             and os.path.splitext(f)[1].lower() not in exclude_ext]
    content = f"当前目录：{directory}\n"
    content += "当前目录下的文件列表（每一行都是一个完整的文件名）：\n"
    for filename in files:
        content += f"{filename}\n"
    return content

def main():
    parser = argparse.ArgumentParser(description="列出当前目录下所有文件（排除bat、txt、ps1）")
    parser.add_argument("-d", "--directory", default=os.getcwd(), help="要列出的目录，默认当前目录")
    parser.add_argument("-o", "--output", default=None, help="输出的txt文件名，不指定则输出到剪贴板")
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        print(f"错误: 目录不存在 - {args.directory}")
        return 1
    content = list_files(args.directory)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"文件列表已保存到: {args.output}")
    else:
        if not HAS_CLIP:
            print("未安装pyperclip库，无法复制到剪贴板。请先运行: pip install pyperclip")
            return 1
        pyperclip.copy(content)
        print("文件列表已复制到剪贴板！")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main()) 