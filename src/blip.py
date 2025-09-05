import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

count = 0

def caption_image(input_path, output_path, cache_dir="model/blip-image-captioning-base", trigger_word=""):
    global count
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", cache_dir=cache_dir)
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base", cache_dir=cache_dir)

    for filename in os.listdir(input_path):
        if filename.lower().endswith(('.jpg', '.png')):
            file_path = os.path.join(input_path, filename)
            
            with Image.open(file_path) as img:
                inputs = processor(img, return_tensors="pt")
                out = model.generate(**inputs)
                caption = processor.decode(out[0], skip_special_tokens=True)
                
            if trigger_word:
                caption = f"{trigger_word}, {caption}"
            
            # Save caption to a text file
            txt_filename = f"img{count}.txt"
            txt_path = os.path.join(output_path, txt_filename)
            with open(txt_path, "w") as f:
                f.write(caption)
            
            count += 1
            print(f"Processed {filename} -> {txt_filename}")