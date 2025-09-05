# LoRA Preprocess Master

**LoRA Preprocess Master** is a simple GUI tool for one-click preprocessing and automatic captioning of LoRA model datasets.

<img width="400" alt="LoRA Preprocess Master 2025_9_6 0_47_49" src="https://github.com/user-attachments/assets/b5a0ee89-0a81-4245-b3ef-4f2fe25c3319" />

## Features

- Batch Image Preprocessing
  - Batch resize images to common LoRA training sizes (512 for SD1.5, 1024 for SDXL, or custom).
  - Option to crop to square.
  - Output format conversion (JPEG / PNG).
- Automatic captioning
  - Integrated image captioning models (Now [BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) is available).
  - Batch adding trigger words.
  - Cache directory support for efficiency.
- One-click Workflow
  - Simply set input and output folders, enable the features you want, and click Start.

## Roadmap

- ☑️ Add support for more captioning models (e.g. [JoyCaption](https://github.com/fpgaminer/joycaption) and [CogVLM](https://github.com/zai-org/CogVLM)).
- ☑️ Different mode for image captioning: Tag or Caption.

## How to Use

1. Clone this repo
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

## Contributing

Contributions are welcome!

- Open issues for bugs or feature requests.
- Submit PRs with improvements.

## Acknowledgement

- [Sun-Valley-ttk-theme](https://github.com/rdbende/Sun-Valley-ttk-theme) for Tkinter theme
- [blip](https://huggingface.co/Salesforce/blip-image-captioning-base)

Thanks to their works on open source <3
