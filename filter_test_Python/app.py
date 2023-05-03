import os
import tkinter as tk
from tkinter import filedialog
from goldstein_filter import main as goldstein_filter_main, read_interferogram
from gen_tif import main as gen_tif_main
from lxml import etree
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Goldstein Filter & TIF Generator")
        self.geometry("1200x600")

        self.file_name = tk.StringVar()
        self.filter_strength = tk.DoubleVar(value=0.5)
        self.window_size = tk.IntVar(value=32)
        self.step_size = tk.IntVar(value=8)

        tk.Label(self, text="Input file:").grid(row=0, column=0, sticky="w")
        tk.Entry(self, textvariable=self.file_name).grid(row=0, column=1, sticky="ew")
        tk.Button(self, text="Browse", command=self.browse_file).grid(row=0, column=2)

        tk.Label(self, text="Filter strength:").grid(row=1, column=0, sticky="w")
        tk.Entry(self, textvariable=self.filter_strength).grid(row=1, column=1, sticky="ew")

        tk.Label(self, text="Window size:").grid(row=2, column=0, sticky="w")
        tk.Entry(self, textvariable=self.window_size).grid(row=2, column=1, sticky="ew")

        tk.Label(self, text="Step size:").grid(row=3, column=0, sticky="w")
        tk.Entry(self, textvariable=self.step_size).grid(row=3, column=1, sticky="ew")

        tk.Button(self, text="Apply Filter & Generate TIF", command=self.apply_filter_and_generate_tif).grid(row=4, columnspan=3)

        self.output_info = tk.StringVar()
        tk.Label(self, textvariable=self.output_info).grid(row=5, columnspan=3)

        self.before_image_label = tk.Label(self)
        self.before_image_label.grid(row=6, column=0, columnspan=3)

        self.after_image_label = tk.Label(self)
        self.after_image_label.grid(row=6, column=3, columnspan=3)

        self.columnconfigure(1, weight=1)



    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_name.set(file_path)

    def display_image(self, file_path, label):
        img = Image.open(file_path)
        img.thumbnail((500, 500))  # Resize the image to fit the GUI
        photo = ImageTk.PhotoImage(img)

        label.config(image=photo)
        label.image = photo

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

        # Display the images
        input_tif_file = self.file_name.get().replace('.int', '.int.tif')
        self.display_image(input_tif_file, self.before_image_label)
        self.display_image(output_file + ".tif", self.after_image_label)

if __name__ == "__main__":
    app = App()
    app.mainloop()

