from PIL import Image
import os

count = 0

def preprocess_image(input_path, output_path, target_size=1024, cut_to_square=True, img_format="JPEG"):
    global count
    for filename in os.listdir(input_path):
        if filename.lower().endswith(('.jpg', '.png')):
            file_path = os.path.join(input_path, filename)
            
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Calculate cropping area to make the image square by removing excess width or height
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
                    # Crop the image
                    img_cropped = img.crop((left, top, right, bottom))
                width, height = img_cropped.size

                # Resize the image so that the longer side is target_size, and the shorter side is scaled proportionally
                if width > height:
                    new_width = target_size
                    new_height = int((target_size/ width) * height)
                else:
                    new_height = target_size
                    new_width = int((target_size / height) * width)
                img_resized = img_cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save the preprocessed image
                os.makedirs(output_path, exist_ok=True)
                if img_format == "JPEG":
                    output_filename = "img" + str(count) + ".jpg"
                    img_resized.save(os.path.join(output_path, output_filename), format="JPEG")
                elif img_format == "PNG":
                    output_filename = "img" + str(count) + ".png"
                    img_resized.save(os.path.join(output_path, output_filename), format="PNG")

                # Update counter
                count += 1