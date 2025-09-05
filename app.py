import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import sv_ttk
import os
from src.preprocess import preprocess_image
from src.blip import caption_image
from src.moondream import caption_image as moondream_caption_image

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LoRA Preprocess Master")
        self.root.geometry("600x800")
        # Fix window size
        self.root.resizable(False, False)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. Path input section
        self.create_path_section()
        
        # 2. Image preprocessing parameters section
        self.create_preprocessing_section()
        
        # 3. Image captioning parameters section
        self.create_captioning_section()

        # 4. Start button and log output section
        self.create_action_section()
    
    def create_path_section(self):
        path_frame = ttk.LabelFrame(self.main_frame, text="Path", padding="10")
        path_frame.pack(fill=tk.X, pady=5)
        
        # Input path
        ttk.Label(path_frame, text="Input Path").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = ttk.Entry(path_frame, width=40)
        self.input_path.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(path_frame, text="Browse...", command=lambda: self.browse_folder(self.input_path)).grid(row=0, column=2, pady=5)

        # Output path
        ttk.Label(path_frame, text="Output Path").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = ttk.Entry(path_frame, width=40)
        self.output_path.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(path_frame, text="Browse...", command=lambda: self.browse_folder(self.output_path)).grid(row=1, column=2, pady=5)

    def update_size_entry_state(self):
        if self.size_var.get() == "other":
            self.resize_value.config(state=tk.NORMAL)
        else:
            self.resize_value.delete(0, tk.END)
            self.resize_value.config(state=tk.DISABLED)

    def create_preprocessing_section(self):
        preproc_frame = ttk.LabelFrame(self.main_frame, text="Image Preprocessing", padding="10")
        preproc_frame.pack(fill=tk.X, pady=5)

        ttk.Label(preproc_frame, text="Enable Preprocessing?").grid(row=0, column=0, sticky=tk.W, pady=5)
        enable_preproc_frame = ttk.Frame(preproc_frame)
        enable_preproc_frame.grid(row=0, column=1, sticky=tk.W, pady=5, columnspan=2)

        self.enable_preproc_var = tk.BooleanVar(value=True)
        self.enable_preproc_square = ttk.Checkbutton(enable_preproc_frame, variable=self.enable_preproc_var)
        self.enable_preproc_square.pack(side=tk.LEFT, padx=2)

        # Resize options
        ttk.Label(preproc_frame, text="Resize").grid(row=1, column=0, sticky=tk.W, pady=5)
        size_frame = ttk.Frame(preproc_frame)
        size_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        self.size_var = tk.StringVar(value="512")
        self.size_512 = ttk.Radiobutton(size_frame, text="512 (SD1.5)", variable=self.size_var, value="512", 
                         command=self.update_size_entry_state)
        self.size_512.pack(side=tk.LEFT, padx=2)
        
        self.size_1024 = ttk.Radiobutton(size_frame, text="1024 (SDXL)", variable=self.size_var, value="1024",
                         command=self.update_size_entry_state)
        self.size_1024.pack(side=tk.LEFT, padx=2)

        self.size_other = ttk.Radiobutton(size_frame, text="Others", variable=self.size_var, value="other",
                         command=self.update_size_entry_state)
        self.size_other.pack(side=tk.LEFT, padx=2)
        
        self.resize_value = ttk.Entry(size_frame, width=6)
        self.resize_value.pack(side=tk.LEFT, padx=2)
        self.resize_value.insert(0, "")
        self.resize_value.config(state=tk.DISABLED)

        # Cut to Square option
        ttk.Label(preproc_frame, text="Crop to Square?").grid(row=2, column=0, sticky=tk.W, pady=5)
        cut_frame = ttk.Frame(preproc_frame)
        cut_frame.grid(row=2, column=1, sticky=tk.W, pady=5, columnspan=2)

        self.cut_square_var = tk.BooleanVar(value=False)
        self.cut_square = ttk.Checkbutton(cut_frame, variable=self.cut_square_var)
        self.cut_square.pack(side=tk.LEFT, padx=2)

        # Format options
        ttk.Label(preproc_frame, text="Output Format").grid(row=3, column=0, sticky=tk.W, pady=5)
        format_frame = ttk.Frame(preproc_frame)
        format_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.format_var = tk.StringVar(value="JPEG")
        self.format_jpg = ttk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, value="JPEG")
        self.format_jpg.pack(side=tk.LEFT, padx=2)
        
        self.format_png = ttk.Radiobutton(format_frame, text="PNG", variable=self.format_var, value="PNG")
        self.format_png.pack(side=tk.LEFT, padx=2)
    
    def create_captioning_section(self):
        caption_frame = ttk.LabelFrame(self.main_frame, text="Image Captioning", padding="10")
        caption_frame.pack(fill=tk.X, pady=5)

        ttk.Label(caption_frame, text="Enable Captioning?").grid(row=0, column=0, sticky=tk.W, pady=5)
        enable_caption_frame = ttk.Frame(caption_frame)
        enable_caption_frame.grid(row=0, column=1, sticky=tk.W, pady=5, columnspan=2)

        self.enable_caption_var = tk.BooleanVar(value=True)
        self.enable_caption = ttk.Checkbutton(enable_caption_frame, variable=self.enable_caption_var)
        self.enable_caption.pack(side=tk.LEFT, padx=2)

        # Model selection
        ttk.Label(caption_frame, text="Model").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_type = ttk.Combobox(caption_frame, values=["BLIP (CPU Friendly)", "MoonDream (About 5GB VRAM)"], width=25)
        self.model_type.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.model_type.current(0)

        # Cache and checkpoint paths
        ttk.Label(caption_frame, text="Cache Dir").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cache_dir = ttk.Entry(caption_frame, width=40)
        self.cache_dir.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(caption_frame, text="Browse...", command=lambda: self.browse_folder(self.cache_dir)).grid(row=2, column=2, pady=5)

        # Trigger Word input
        ttk.Label(caption_frame, text="Trigger Word").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.trigger_word = ttk.Entry(caption_frame, width=40)
        self.trigger_word.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
    
    def create_action_section(self):
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Start button
        start_button = ttk.Button(action_frame, text="Start", command=self.start_processing, width=80)
        start_button.pack(pady=10)
        
        # Log output area
        log_label = ttk.Label(action_frame, text="Console Log")
        log_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.log_area = scrolledtext.ScrolledText(action_frame, height=10)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area.config(state=tk.DISABLED)
    
    def browse_folder(self, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder_path)
    
    def log_message(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        self.root.update()
        
    def start_processing(self):
        # Get all parameters
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        
        # Validate paths
        if not input_path or not output_path:
            self.log_message("Error: Please type in input path and output path.")
            return
        
        if not os.path.exists(input_path):
            self.log_message(f"Error: Input path does not exist - {input_path}")
            return
        
        # Processing logic implementation
        self.log_message(f"Input path: {input_path}")
        enable_preproc = self.enable_preproc_var.get()
        if enable_preproc:
            self.log_message("\n=========== Start Preprocessing ===========")
            self.log_message(f"Resize={self.size_var.get()}, Crop={self.cut_square_var.get()}, Format={self.format_var.get()}")
            preprocess_image(
                input_path=input_path, 
                output_path=output_path, 
                target_size=int(float(self.size_var.get())), 
                cut_to_square=self.cut_square_var.get(), 
                img_format=self.format_var.get()
            )
        
        enable_caption = self.enable_caption_var.get()
        if enable_caption:
            self.log_message("\n=========== Start Captioning ===========")
            self.log_message(f"Model={self.model_type.get()}, Cache Dir={self.cache_dir.get()}, Trigger Word={self.trigger_word.get()}")
            if self.model_type.get() == "BLIP (CPU Friendly)":
                result = caption_image(
                    input_path=output_path, 
                    output_path=output_path, 
                    cache_dir=self.cache_dir.get() if self.cache_dir.get() else "model/", 
                    trigger_word=self.trigger_word.get()
                )
                if result:
                    self.log_message(result)
            elif self.model_type.get() == "MoonDream (About 5GB VRAM)":
                result = moondream_caption_image(
                    input_path=output_path,
                    output_path=output_path,
                    cache_dir=self.cache_dir.get() if self.cache_dir.get() else "model/",
                    trigger_word=self.trigger_word.get()
                )
                if result:
                    self.log_message(result)
        self.log_message(f"\n=========== Processing finished! ===========")
        self.log_message(f"Output path: {output_path}")


if __name__ == "__main__":
    root = tk.Tk()
    sv_ttk.set_theme("dark")  # Set theme
    app = ImageProcessingApp(root)
    root.mainloop()