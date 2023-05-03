import os
import tkinter as tk
from tkinter import filedialog
from goldstein_filter import main as goldstein_filter_main
from gen_tif import main as gen_tif_main
from lxml import etree
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Goldstein Filter & TIF Generator")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.file_name = tk.StringVar()
        self.filter_strength = tk.DoubleVar(value=0.5)
        self.window_size = tk.IntVar(value=32)
        self.step_size = tk.IntVar(value=8)
        self.output_info = tk.StringVar()

        tk.Label(self, text="Input file:").pack()
        tk.Entry(self, textvariable=self.file_name).pack()
        tk.Button(self, text="Browse", command=self.browse_file).pack()

        tk.Label(self, text="Filter strength:").pack()
        tk.Entry(self, textvariable=self.filter_strength).pack()

        tk.Label(self, text="Window size:").pack()
        tk.Entry(self, textvariable=self.window_size).pack()

        tk.Label(self, text="Step size:").pack()
        tk.Entry(self, textvariable=self.step_size).pack()

        tk.Button(self, text="Apply Filter & Generate TIF", command=self.apply_filter_and_generate_tif).pack()

        tk.Label(self, textvariable=self.output_info).pack()

        image_frame = tk.Frame(self)
        image_frame.pack(pady=10)

        before_image_container = tk.Frame(image_frame)
        before_image_container.pack(side=tk.LEFT, padx=10)

        self.before_image_label = tk.Label(before_image_container, image=None)
        self.before_image_label.pack()
        tk.Label(before_image_container, text="").pack()

        after_image_container = tk.Frame(image_frame)
        after_image_container.pack(side=tk.RIGHT, padx=10)

        self.after_image_label = tk.Label(after_image_container, image=None)
        self.after_image_label.pack()
        self.filter_info_label = tk.Label(after_image_container, text="")
        self.filter_info_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_name.set(file_path)

    def apply_filter_and_generate_tif(self):
        if not self.file_name.get():
            print("Please select an input file.")
            return

        output_folder = f"filtered_f{self.filter_strength.get()}_w{self.window_size.get()}_s{self.step_size.get()}"
        os.makedirs(output_folder, exist_ok=True)

        output_file = os.path.join(output_folder, "filtered_" + os.path.basename(self.file_name.get()))

        goldstein_filter_main(self.file_name.get(), output_folder, self.filter_strength.get(), self.window_size.get(),
                              self.step_size.get())

        xml_file = self.file_name.get() + '.xml'
        tree = etree.parse(xml_file)
        width = int(tree.findtext('.//property[@name="width"]/value'))
        height = int(tree.findtext('.//property[@name="length"]/value'))

        gen_tif_main(output_file, width, height)

        output_message = f"Filtered and generated TIF for {self.file_name.get()} with filter strength {self.filter_strength.get()}, window size {self.window_size.get()}, and step size {self.step_size.get()}"
        self.output_info.set(output_message)

        filter_info = f"Filtered Image (f={self.filter_strength.get()}, w={self.window_size.get()}, s={self.step_size.get()})"
        self.filter_info_label.config(text=filter_info)

        # 显示原始图像
        before_image = Image.open(self.file_name.get().replace(".int", ".int.tif"))
        before_image.thumbnail((200, 200), Image.LANCZOS)
        before_photo = ImageTk.PhotoImage(before_image)
        self.before_image_label.config(image=before_photo)
        self.before_image_label.image = before_photo

        # 显示滤波后的图像
        after_image = Image.open(output_file.replace(".int", ".int.tif"))
        after_image.thumbnail((200, 200), Image.LANCZOS)
        after_photo = ImageTk.PhotoImage(after_image)
        self.after_image_label.config(image=after_photo)
        self.after_image_label.image = after_photo


if __name__ == "__main__":
    app = App()
    app.mainloop()
