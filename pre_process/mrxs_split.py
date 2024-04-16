import openslide
from PIL import Image
import os
import numpy as np

# 设置MRXS文件路径
slide_path = '/home/liusiyan/hover_net/data/slide-2024-04-10T15-59-53-R1-S2.mrxs'

# 打开MRXS文件
slide = openslide.OpenSlide(slide_path)

# 创建输出目录
output_dir = 'tiles'
os.makedirs(output_dir, exist_ok=True)

# 设置要裁剪的小图尺寸
tile_size = (1000,1000)

# 选择缩放级别，0是最高分辨率，数字越大分辨率越低
level = 0

# 获取指定级别下的图像大小
level_width, level_height = slide.level_dimensions[level]
print(f"Level {level} dimensions: {level_width} x {level_height}")
# 计算在指定级别下能裁剪出多少个小图
cols, rows = level_width // tile_size[0], level_height // tile_size[1]

# 设置空白/黑色图片的阈值
blank_black_threshold = 0.96  # 如果图片中超过80%的像素是空白或黑色的，那么我们就认为这是一张空白/黑色图片

count = 0
# 裁剪并保存小图
for row in range(rows):
    for col in range(cols):
        # 计算小图在大图中的位置
        x, y = col * tile_size[0], row * tile_size[1]
        # 使用read_region读取小图
        region = slide.read_region((x, y), level, tile_size)
        # 转换为RGB格式，因为read_region返回的是带有alpha通道的图像
        region = region.convert("RGB")
        # 将图像转换为NumPy数组以便分析
        region_np = np.array(region)

        # # 计算白色和黑色像素的比例
        # white_pixels = np.sum(np.all(region_np >= 240, axis=2))  # 白色像素的阈值
        # black_pixels = np.sum(np.all(region_np <= 15, axis=2))    # 黑色像素的阈值
        # total_pixels = np.product(region_np.shape[:2])
        # white_black_ratio = (white_pixels + black_pixels) / total_pixels

        # # 如果白色和黑色像素的比例低于阈值，则保存图片
        # if white_black_ratio < blank_black_threshold:
        #     # 保存有用的小图
        # judge a tile is blank or not
        # if the tile is blank, then skip it
        if np.mean(region_np) < 200:
            # 将图片100张拼成一张图片

            continue

        # tile_name = f"tile_{row}_{col}_level{level}.png"
        # #将图片缩放0.5倍 保存
        # region = region.resize((500, 500))
        # region.save(os.path.join(output_dir, tile_name))

# 关闭slide对象
slide.close()

print("Non-blank and non-black tiles have been saved to:", output_dir)
