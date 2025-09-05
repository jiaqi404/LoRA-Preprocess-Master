from PIL import Image
import os

# 定义数据集路径和预处理路径
# dataset_path = "original/"
# preprocessed_path = "preprocessed3/"

count = 0

# 数据集预处理
def preprocess_image(input_path, output_path, target_size=1024, cut_to_square=True, img_format="JPEG"):
    global count
    for filename in os.listdir(input_path):
        if filename.lower().endswith(('.jpg', '.png')):
            file_path = os.path.join(input_path, filename)
            
            with Image.open(file_path) as img:
                width, height = img.size
                
                # 计算裁剪区域，裁掉过宽或过长的部分，使图像变为正方形
                img_cropped = img
                if cut_to_square:
                    if width > height:
                        left = (width - height) // 2
                        top = 0
                        right = left + height
                        bottom = height
                    else:
                        top = (height - width) // 2
                        left = 0
                        bottom = top + width
                        right = width
                    # 裁剪图像
                    img_cropped = img.crop((left, top, right, bottom))
                width, height = img_cropped.size

                # 使图像的长边为img_size，短边按比例缩放
                if width > height:
                    new_width = target_size
                    new_height = int((target_size/ width) * height)
                else:
                    new_height = target_size
                    new_width = int((target_size / height) * width)
                img_resized = img_cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 保存预处理后的图像
                os.makedirs(output_path, exist_ok=True)
                if img_format == "JPEG":
                    output_filename = "img" + str(count) + ".jpg"
                    img_resized.save(os.path.join(output_path, output_filename), format="JPEG")
                elif img_format == "PNG":
                    # output_filename = os.path.splitext(filename)[0] + ".png"
                    output_filename = "img" + str(count) + ".png"
                    img_resized.save(os.path.join(output_path, output_filename), format="PNG")

                # 更新计数器
                count += 1

# 执行预处理
# preprocess_image(input_path=dataset_path, output_path=preprocessed_path, target_size=512, cut_to_square=False, img_format="JPEG")