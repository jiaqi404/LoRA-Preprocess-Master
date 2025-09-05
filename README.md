# LoRA Preprocess Master

LoRA Preprocess Master is a simple GUI tool for one-click preprocessing and automatic captioning of LoRA model datasets.

## Features

- Image preprocessing: resize and crop images
- Automatic captioning: add descriptive text to training images. Now [blip](https://huggingface.co/Salesforce/blip-image-captioning-base) model available.
- Batch processing: efficiently handle lots of images
- User-friendly graphical interface: no programming experience required
- One-click operation: simplify preparation work before LoRA model training

## How to Use

1. Clone this repository to your local machine
2. Install required dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application
    ```bash
    python app.py
    ```
4. Use the GUI to select your dataset folder, configure processing parameters, and click "Start"

## System Requirements

- Python 3.12
- CUDA-compatible GPU recommended for faster processing

## Acknowledgement

- [Sun-Valley-ttk-theme](https://github.com/rdbende/Sun-Valley-ttk-theme) for Tkinter theme
- [blip](https://huggingface.co/Salesforce/blip-image-captioning-base)

Thanks to their works on open source <3