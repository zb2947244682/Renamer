import os
import argparse

def split_txt_file(input_file, lines_per_file=100):
    """将大文本文件分割成多个小文件，每个文件包含指定行数"""
    try:
        # 获取文件名和扩展名
        base_name = os.path.basename(input_file)
        file_name, file_ext = os.path.splitext(base_name)
        dir_path = os.path.dirname(input_file)
        
        # 读取原始文件
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 计算需要分割的文件数量
        total_lines = len(lines)
        num_files = (total_lines // lines_per_file) + (1 if total_lines % lines_per_file else 0)
        
        # 分割文件
        for i in range(num_files):
            start = i * lines_per_file
            end = start + lines_per_file
            chunk = lines[start:end]
            
            # 生成新文件名
            new_file_name = f"{file_name}_{i+1}{file_ext}"
            new_file_path = os.path.join(dir_path, new_file_name)
            
            # 写入新文件
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.writelines(chunk)
            
            print(f"已创建: {new_file_path}")
        
        print(f"完成! 共分割成 {num_files} 个文件")
        return num_files
    except Exception as e:
        print(f"错误: 处理文件时出错 - {str(e)}")
        return 0

def main():
    parser = argparse.ArgumentParser(description="大文本文件分割工具")
    parser.add_argument("-f", "--file", required=True, 
                        help="要分割的文本文件路径")
    parser.add_argument("-n", "--number", type=int, default=100,
                        help="每个分割文件包含的行数 (默认: 100)")
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.file):
        print(f"错误: 文件不存在 - {args.file}")
        return 1
    
    if args.number <= 0:
        print("错误: 行数必须大于0")
        return 1
    
    print(f"开始处理文件: {args.file}")
    split_txt_file(args.file, args.number)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())