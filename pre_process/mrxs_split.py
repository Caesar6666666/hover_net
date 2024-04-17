import openslide
from PIL import Image
import os
import numpy as np

# 设置MRXS文件路径
slide_path = '/home/liusunyan/hover_net/data/slide-2024-04-10T15-59-53-R1-S2.mrxs'

# 打开MRXS文件
slide = openslide.OpenSlide(slide_path)

# 创建输出目录
output_dir = 'tiles'
os.makedirs(output_dir, exist_ok=True)

blank_output_dir = 'blank_tiles'
os.makedirs(blank_output_dir, exist_ok=True)
# 设置要裁剪的小图尺寸
tile_size = (1000, 1000)

# 选择缩放级别，0是最高分辨率
level = 0

# 获取指定级别下的图像大小
level_width, level_height = slide.level_dimensions[level]
print(f"Level {level} dimensions: {level_width} x {level_height}")

# 计算在指定级别下能裁剪出多少个小图
cols, rows = level_width // tile_size[0], level_height // tile_size[1]

# 设置空白/黑色图片的阈值
invalid_pixel_threshold = 0.96  # 如果图片中超过96%的像素是空白或黑色的，那么我们就认为这是一张空白/黑色图片

# 存储废弃的小图
discarded_tiles = []

useful_tiles = []

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
        white_pixels = np.sum(np.all(region_np >= [240, 240, 240], axis=2))  # 定义接近白色的阈值
        black_pixels = np.sum(np.all(region_np <= [15, 15, 15], axis=2))  # 定义接近黑色的阈值
        total_pixels = region_np.shape[0] * region_np.shape[1]
        
        # 如果无效像素比例超过阈值，则认为图片无效
        if (white_pixels + black_pixels) / total_pixels > invalid_pixel_threshold:
            # discarded_tiles.append(region)
            # # 当达到100张废弃图片时，拼接并保存
            # if len(discarded_tiles) == 100:
            #     # 拼接图片
            #     stitched_image = Image.new('RGB', (10 * tile_size[0], 10 * tile_size[1]))
            #     for i, tile in enumerate(discarded_tiles):
            #         stitched_image.paste(tile, ((i % 10) * tile_size[0], (i // 10) * tile_size[1]))
            #     # 缩放图片
            #     stitched_image = stitched_image.resize((int(stitched_image.width / 20), int(stitched_image.height / 20)))
            #     # 保存图片
            #     stitched_image.save(os.path.join(blank_output_dir, f"discarded_stitched_{row}_{col}.png"))
            #     # 清空废弃图片列表
            #     discarded_tiles = []
            pass
        else:
            region.resize((500,500))
            region.save(os.path.join(output_dir,  f"1useful_{row}_{col}.png"))
            # useful_tiles.append(region)
            # # 保存图片
            # if len(useful_tiles) == 100:
            #     # 拼接图片
            #     stitched_image = Image.new('RGB', (10 * tile_size[0], 10 * tile_size[1]))
            #     for i, tile in enumerate(useful_tiles):
            #         stitched_image.paste(tile, ((i % 10) * tile_size[0], (i // 10) * tile_size[1]))
            #     # 缩放图片
            #     stitched_image = stitched_image.resize((int(stitched_image.width / 10), int(stitched_image.height / 10)))
            #     # 保存图片
            #     stitched_image.save(os.path.join(output_dir, f"useful_stitched_{row}_{col}.png"))
            #     # 清空有效图片列表
            #     useful_tiles = []

# # 处理剩余的废弃图片（如果不足100张）
# if discarded_tiles:
#     stitched_image = Image.new('RGB', (10 * tile_size[0], 10 * tile_size[1]))
#     for i, tile in enumerate(discarded_tiles):
#         stitched_image.paste(tile, ((i % 10) * tile_size[0], (i // 10) * tile_size[1]))
#     stitched_image = stitched_image.resize((int(stitched_image.width / 10), int(stitched_image.height / 10)))
#     stitched_image.save(os.path.join(blank_output_dir, f"discarded_stitched_remaining.png"))

# if useful_tiles:
#     stitched_image = Image.new('RGB', (10 * tile_size[0], 10 * tile_size[1]))
#     for i, tile in enumerate(useful_tiles):
#         stitched_image.paste(tile, ((i % 10) * tile_size[0], (i // 10) * tile_size[1]))
#     stitched_image = stitched_image.resize((int(stitched_image.width / 10), int(stitched_image.height / 10)))
#     stitched_image.save(os.path.join(output_dir, f"useful_stitched_remaining.png"))
# 关闭slide对象
slide.close()

print("Non-blank and non-black tiles have been saved to:", output_dir)
