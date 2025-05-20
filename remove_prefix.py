import os
import sys
import argparse
import re
import datetime

def has_prefix(filename):
    """判断文件名是否有单字母前缀（如 'A 文件.txt'）"""
    pattern = r'^([A-Z]) (.+)$'
    return re.match(pattern, filename)

def remove_prefix(filename):
    """移除单字母前缀（如 'A 文件.txt' -> '文件.txt'）"""
    pattern = r'^([A-Z]) (.+)$'
    match = re.match(pattern, filename)
    if match:
        return match.group(2)
    return filename

def process_files(directory, do_rename=True, log_file=None):
    count = 0
    log_entries = []
    start_time = datetime.datetime.now()
    log_entries.append(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_entries.append(f"处理目录: {directory}")
    log_entries.append(f"模式: {'预览' if not do_rename else '实际去除前缀'}")
    log_entries.append("-" * 80)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if has_prefix(filename):
                new_filename = remove_prefix(filename)
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)

                # 如果新文件名已存在且不是自己，则跳过
                if os.path.exists(new_path) and old_path != new_path:
                    log_entry = f"跳过: {old_path} -> {new_path} (目标文件已存在)"
                    print(log_entry)
                    log_entries.append(log_entry)
                    continue

                if do_rename:
                    try:
                        os.rename(old_path, new_path)
                        log_entry = f"去除前缀: {old_path} -> {new_path}"
                        print(log_entry)
                        log_entries.append(log_entry)
                        count += 1
                    except Exception as e:
                        log_entry = f"错误: 无法重命名 {old_path}: {str(e)}"
                        print(log_entry)
                        log_entries.append(log_entry)
                else:
                    log_entry = f"预览: {old_path} -> {new_path}"
                    print(log_entry)
                    log_entries.append(log_entry)
                    count += 1
            else:
                # 没有前缀的文件，记录但不处理
                log_entry = f"无前缀: {os.path.join(root, filename)} (未做更改)"
                log_entries.append(log_entry)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log_entries.append("-" * 80)
    log_entries.append(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_entries.append(f"耗时: {duration}")
    log_entries.append(f"{'预览' if not do_rename else '实际去除前缀'} {count} 个文件")

    if log_file:
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                for entry in log_entries:
                    f.write(f"{entry}\n")
            print(f"日志已保存到: {log_file}")
        except Exception as e:
            print(f"保存日志时出错: {str(e)}")
    return count

def remove_prefix_files(directory, log_file=None):
    return process_files(directory, do_rename=True, log_file=log_file)

def preview_remove_prefix(directory, log_file=None):
    return process_files(directory, do_rename=False, log_file=log_file)

def main():
    parser = argparse.ArgumentParser(description="批量去除文件名前缀工具")
    parser.add_argument("-d", "--directory", default="D:\\AllRoms\\SFC",
                        help="要处理的目录路径 (默认: D:\\AllRoms\\SFC)")
    parser.add_argument("-p", "--preview", action="store_true",
                        help="预览模式，不实际重命名文件")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"错误: 目录不存在 - {args.directory}")
        return 1

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "remove_prefix_log.txt")

    print(f"开始处理目录: {args.directory}")
    if args.preview:
        print("预览模式: 不会实际重命名文件")
        count = preview_remove_prefix(args.directory, log_file)
        print(f"预览完成! 将会去除前缀 {count} 个文件")
    else:
        count = remove_prefix_files(args.directory, log_file)
        print(f"完成! 共去除前缀 {count} 个文件")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 