# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
from models_adapter import TextGenAdapter, ImageClassAdapter

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIT137 - AI GUI")
        self.geometry("1000x650")

        self.text_adapter = TextGenAdapter("distilgpt2")
        self.img_adapter = ImageClassAdapter("google/vit-base-patch16-224")

        self._build_ui()
        self._populate_model_info()

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        # Run tab
        run_frame = ttk.Frame(nb)
        nb.add(run_frame, text="Run Model")

        ttk.Label(run_frame, text="Select model:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.model_var = tk.StringVar(value="TextGen")
        model_choice = ttk.Combobox(run_frame, values=["TextGen", "ImageClass"], textvariable=self.model_var, state="readonly", width=20)
        model_choice.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(run_frame, text="Input (text or image path):").grid(row=1, column=0, sticky="nw", padx=6)
        self.input_text = tk.Text(run_frame, height=5, width=70)
        self.input_text.grid(row=2, column=0, columnspan=3, padx=6, pady=4)

        ttk.Button(run_frame, text="Choose File (for images)", command=self._choose_file).grid(row=3, column=0, padx=6, pady=6, sticky="w")
        ttk.Button(run_frame, text="Run", command=self._run_model).grid(row=3, column=1, padx=6, pady=6, sticky="w")

        ttk.Label(run_frame, text="Output:").grid(row=4, column=0, sticky="nw", padx=6, pady=(6,0))
        self.output_area = scrolledtext.ScrolledText(run_frame, height=12, width=90)
        self.output_area.grid(row=5, column=0, columnspan=3, padx=6, pady=6)

        # OOP explanation tab
        oop_frame = ttk.Frame(nb)
        nb.add(oop_frame, text="OOP Explanation")
        self.oop_text = scrolledtext.ScrolledText(oop_frame)
        self.oop_text.pack(fill="both", expand=True)
        self.oop_text.insert("end", self._generate_oop_text())
        self.oop_text.configure(state="disabled")

        # Model Info tab
        info_frame = ttk.Frame(nb)
        nb.add(info_frame, text="Model Info")
        self.info_text = scrolledtext.ScrolledText(info_frame)
        self.info_text.pack(fill="both", expand=True)
        self.info_text.configure(state="disabled")

    def _choose_file(self):
        path = filedialog.askopenfilename(filetypes=[("Image files","*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files","*.*")])
        if path:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("end", path)

    def _run_model(self):
        kind = self.model_var.get()
        user_input = self.input_text.get("1.0", "end").strip()
        self.output_area.delete("1.0", "end")
        if kind == "TextGen":
            out = self.text_adapter.run(user_input)
            if out is None:
                self.output_area.insert("end", "Error running text model. Check console.")
            else:
                self.output_area.insert("end", out)
        else:
            # expects a file path or PIL Image
            out = self.img_adapter.run(user_input)
            if out is None:
                self.output_area.insert("end", "Error running image model. Check console.")
            else:
                self.output_area.insert("end", str(out))

    def _generate_oop_text(self):
        return (
            "OOP concepts used in this project:\n\n"
            "- Encapsulation: ModelAdapter uses protected (_model_name) and private (__secret) attributes.\n"
            "- Polymorphism: ModelAdapter defines run(); TextGenAdapter and ImageClassAdapter implement it differently.\n"
            "- Method overriding: subclasses override run() and get_info() from ModelAdapter.\n"
            "- Multiple inheritance: HFModelMixin + ModelAdapter are combined in concrete adapters.\n"
            "- Multiple decorators: @log_call and @catch_exceptions applied to run() methods.\n"
        )

    def _populate_model_info(self):
        info = []
        for name, adapter in [("TextGen", self.text_adapter), ("ImageClass", self.img_adapter)]:
            info.append(f"{name} -> {adapter.get_info()}\n")
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("end", "\n".join(info))
        self.info_text.configure(state="disabled")
