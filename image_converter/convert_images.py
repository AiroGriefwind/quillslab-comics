from PIL import Image
import os
import re

def convert_to_a4(input_path, output_path):
    # A4尺寸 (210mm x 297mm) 換算為像素 (300 DPI)
    a4_width_px = int(210 / 25.4 * 300)
    a4_height_px = int(297 / 25.4 * 300)
    
    # 打開原始圖片
    original_image = Image.open(input_path)
    
    # 計算新圖片的寬度比例，確保寬度與A4對齊
    new_width = a4_width_px
    scale_ratio = new_width / original_image.width
    new_height = int(original_image.height * scale_ratio)
    
    # 調整圖片大小
    resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 創建A4大小的白色背景
    background = Image.new("RGB", (a4_width_px, a4_height_px), "white")
    
    # 將調整大小的圖片粘貼到白色背景上，居中對齊
    paste_position = (0, (a4_height_px - new_height) // 2)
    background.paste(resized_image, paste_position)
    
    # 保存結果
    background.save(output_path)

# 批量處理資料夾中的所有圖片
input_folder = "input_images"
output_folder = "output_images"

# 確保輸出資料夾存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 處理所有圖片
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        # 使用正則表達式解析檔名
        match = re.match(r'heip(\d{3})_(\d{4})_圖層-(\d+)', filename)
        
        if match:
            page_number = match.group(1)  # 頁碼
            layer_number = match.group(3)  # 圖層
            
            # 生成新的檔名
            new_filename = f"{int(page_number)}.{layer_number}.png"
            
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, new_filename)
            
            convert_to_a4(input_path, output_path)
            print(f"處理 {filename} -> {new_filename}")
        else:
            print(f"無法解析檔名: {filename}")
