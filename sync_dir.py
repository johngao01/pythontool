import os.path
import shutil
import csv
from pathlib import Path
from datetime import datetime

src_folder = Path(r'C:\Users\16498\Desktop\medias')
dst_folders = {
    'passport': Path(r'G:\medias'),
    'drive': Path(r'E:\medias')
}

result = []  # 用于保存结果的列表


def copy_file(src_file, dst_file):
    if dst_file.exists() and dst_file.stat().st_size > src_file.stat().st_size:
        return False
    shutil.copy2(src_file, dst_file)
    return True


def main():
    for src_file in src_folder.glob('**/*'):
        if src_file.is_file():
            row = [str(src_file)]
            for dst_name, dst_folder in dst_folders.items():
                try:
                    dst_file = dst_folder / src_file.relative_to(src_folder)
                except ValueError:
                    continue
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                success = copy_file(src_file, dst_file)
                row.append(str(dst_file)) if success else row.append('')
            row.append(str(os.path.getsize(src_file)))
            row.append(datetime.fromtimestamp(os.path.getctime(src_file)).strftime("%Y-%m-%d %H:%M:%S"))
            print('\t'.join(row))
            result.append(row)
            src_file.unlink()  # 删除已处理完的文件


def last_work():
    # 清除空文件夹
    for folder in list(src_folder.glob('**/*'))[::-1]:
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()

    # 将结果追加写入CSV文件
    with open('result.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(['index', 'source', 'passport_dst', 'drive_dst', 'size', 'file_create_time'])
        for i, row in enumerate(result):
            writer.writerow([i + 1] + row)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        last_work()
