import os
import sys
import argparse
import re
import datetime
from pypinyin import pinyin, Style

def get_first_letter(filename):
    """获取文件名的首字母，如果是中文则获取拼音首字母"""
    name = os.path.splitext(filename)[0]
    if not name:
        return ""
        
    # 检查首字符是否是中文
    if '\u4e00' <= name[0] <= '\u9fff':
        # 获取拼音首字母
        py = pinyin(name[0], style=Style.FIRST_LETTER)
        return py[0][0].upper() if py and py[0] else ""
    else:
        # 非中文直接返回首字母
        return name[0].upper() if name[0].isalpha() else ""

def remove_existing_prefix(filename):
    """移除已存在的单字母前缀 (如 'A ', 'B ' 等)"""
    # 匹配模式: 单个大写字母后跟一个空格
    pattern = r'^([A-Z]) (.+)$'
    match = re.match(pattern, filename)
    if match:
        return match.group(2)  # 返回不带前缀的文件名
    return filename  # 如果没有匹配的前缀，返回原始文件名

def process_files(directory, do_rename=True, log_file=None):
    """处理目录下的所有文件，可选择是否实际重命名"""
    count = 0
    log_entries = []
    
    # 记录开始时间
    start_time = datetime.datetime.now()
    log_entries.append(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_entries.append(f"处理目录: {directory}")
    log_entries.append(f"模式: {'预览' if not do_rename else '实际重命名'}")
    log_entries.append("-" * 80)
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 先移除可能存在的前缀
            clean_filename = remove_existing_prefix(filename)
            
            # 如果文件名已经被清理，记录一下
            prefix_removed = (clean_filename != filename)
            
            # 获取首字母
            first_letter = get_first_letter(clean_filename)
            if not first_letter:
                continue
                
            # 构建新文件名
            new_filename = f"{first_letter} {clean_filename}"
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)
            
            # 如果新旧路径相同（已经是正确格式），则跳过
            if old_path == new_path:
                log_entry = f"跳过: {old_path} (已经是正确格式)"
                print(log_entry)
                log_entries.append(log_entry)
                continue
                
            # 如果新文件名已存在且不是自己，则跳过
            if os.path.exists(new_path) and old_path != new_path:
                log_entry = f"跳过: {old_path} -> {new_path} (目标文件已存在)"
                print(log_entry)
                log_entries.append(log_entry)
                continue
                
            if do_rename:
                try:
                    os.rename(old_path, new_path)
                    if prefix_removed:
                        log_entry = f"重命名: {old_path} -> {new_path} (移除旧前缀并添加新前缀)"
                    else:
                        log_entry = f"重命名: {old_path} -> {new_path}"
                    print(log_entry)
                    log_entries.append(log_entry)
                    count += 1
                except Exception as e:
                    log_entry = f"错误: 无法重命名 {old_path}: {str(e)}"
                    print(log_entry)
                    log_entries.append(log_entry)
            else:
                # 预览模式，只显示将要进行的操作
                if prefix_removed:
                    log_entry = f"预览: {old_path} -> {new_path} (移除旧前缀并添加新前缀)"
                else:
                    log_entry = f"预览: {old_path} -> {new_path}"
                print(log_entry)
                log_entries.append(log_entry)
                count += 1
    
    # 记录结束时间和统计信息
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log_entries.append("-" * 80)
    log_entries.append(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_entries.append(f"耗时: {duration}")
    log_entries.append(f"{'预览' if not do_rename else '实际重命名'} {count} 个文件")
    
    # 将日志写入文件
    if log_file:
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                for entry in log_entries:
                    f.write(f"{entry}\n")
            print(f"日志已保存到: {log_file}")
        except Exception as e:
            print(f"保存日志时出错: {str(e)}")
    
    return count

def rename_files(directory, log_file=None):
    """重命名目录下的所有文件"""
    return process_files(directory, do_rename=True, log_file=log_file)

def preview_files(directory, log_file=None):
    """预览目录下的所有文件重命名操作"""
    return process_files(directory, do_rename=False, log_file=log_file)

def main():
    parser = argparse.ArgumentParser(description="文件批量重命名工具")
    parser.add_argument("-d", "--directory", default="D:\\Roms\\ExcellentRoms",
                        help="要处理的目录路径 (默认: D:\\Roms\\ExcellentRoms)")
    parser.add_argument("-p", "--preview", action="store_true",
                        help="预览模式，不实际重命名文件")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"错误: 目录不存在 - {args.directory}")
        return 1
    
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "log.txt")
    
    print(f"开始处理目录: {args.directory}")
    
    if args.preview:
        print("预览模式: 不会实际重命名文件")
        count = preview_files(args.directory, log_file)
        print(f"预览完成! 将会重命名 {count} 个文件")
    else:
        count = rename_files(args.directory, log_file)
        print(f"完成! 共重命名 {count} 个文件")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())