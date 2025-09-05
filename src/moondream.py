import os
from PIL import Image
from transformers import AutoModelForCausalLM
import torch

count = 0

def caption_image(input_path, output_path, cache_dir="", trigger_word=""):
    global count

    if not torch.cuda.is_available():
        return "CUDA is not available. MoonDream model requires GPU acceleration."

    model = AutoModelForCausalLM.from_pretrained(
        "vikhyatk/moondream2",
        revision="2025-06-21",
        trust_remote_code=True,
        cache_dir=cache_dir,
        device_map={"": "cuda"}
    )

    for filename in os.listdir(input_path):
        if filename.lower().endswith(('.jpg', '.png')):
            file_path = os.path.join(input_path, filename)
            
            with Image.open(file_path) as img:
                for t in model.caption(img, length="normal", stream=True)["caption"]:
                    # Streaming generation example, supported for caption() and detect()
                    print(t, end="", flush=True)
                caption = model.caption(img, length="normal")
                
            if trigger_word:
                caption = f"{trigger_word}, {caption}"
            
            # Save caption to a text file
            txt_filename = f"img{count}.txt"
            txt_path = os.path.join(output_path, txt_filename)
            with open(txt_path, "w") as f:
                f.write(caption)
            
            count += 1
            print(f"moondream Processed {filename} -> {txt_filename}")

    return "MoonDream captioning completed."