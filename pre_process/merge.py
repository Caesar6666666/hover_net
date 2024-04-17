# 将两个文件夹下，同名的图片合并成一张图片
# 两个文件夹下的图片数量必须相同

import os
from PIL import Image

# 设置两个文件夹的路径
folder1 = 'tiles'
folder2 = '/home/liusunyan/hover_net/dataset/sample_tiles/pred/overlay'

# 获取两个文件夹下的所有文件名
files1 = os.listdir(folder1)
files2 = os.listdir(folder2)

# 检查两个文件夹下的文件数量是否相同
# assert len(files1) == len(files2)

# 创建一个新的文件夹用于保存合并后的图片
output_dir = 'merged_tiles'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 合并图片
for i in range(len(files1)):
    if files1[i] in files2:
        # 打开两个文件夹下的图片
        img1 = Image.open(os.path.join(folder1, files1[i]))
        img2 = Image.open(os.path.join(folder2, files1[i]))
        
        # 创建一个新的图片，将两张图片拼接在一起
        new_img = Image.new('RGB', (img1.width + img2.width, img1.height))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (img1.width, 0))
        
        # 保存拼接后的图片
        new_img.save(os.path.join(output_dir, files1[i]))   