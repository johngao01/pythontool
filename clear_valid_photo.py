import os
import hashlib
from multiprocessing import Pool
import pandas as pd
from PIL import Image


def is_valid_image(file_path):
    try:
        with Image.open(file_path) as image:
            image.verify()
        return True
    except (IOError, SyntaxError):
        return False


def process_image(file_path):
    file_info = {"File Path": file_path, "File Size": os.path.getsize(file_path),
                 "Save Time": os.path.getmtime(file_path)}

    if is_valid_image(file_path):
        file_info['valid'] = '1'
    else:
        file_info['valid'] = '0'
    with open(file_path, "rb") as file:
        content = file.read()
        md5_hash = hashlib.md5(content).hexdigest()
        file_info["MD5"] = md5_hash
    return file_info


if __name__ == '__main__':
    folder_path = r"C:\Users\16498\Desktop\medias\jpxgmn"  # 替换为您的文件夹路径
    pool = Pool()
    invalid_images = []
    index = 0
    for root, dirs, files in os.walk(folder_path):
        for image_file in files:
            index += 1
            if index % 1000 == 0:
                print(len(invalid_images))
            image_path = os.path.join(root, image_file)
            print(index)
            result = pool.apply_async(process_image, (image_path,))
            invalid_image = result.get()
            if invalid_image:
                invalid_images.append(invalid_image)
    pool.close()
    pool.join()

    if invalid_images:
        df = pd.DataFrame(invalid_images)
        df.to_csv("invalid_images1.csv", index=False)
        print("Invalid images saved to 'invalid_images1.csv'.")
    else:
        print("No invalid images found.")
