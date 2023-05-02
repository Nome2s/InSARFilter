import os
import tkinter as tk
from tkinter import filedialog
from goldstein_filter import main as goldstein_filter_main
from gen_tif import main as gen_tif_main
from lxml import etree

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Goldstein Filter & TIF Generator")
        self.geometry("600x300")

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

        self.columnconfigure(1, weight=1)

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

        print(
            f"Filtered and generated TIF for {self.file_name.get()} with filter strength {self.filter_strength.get()}, window size {self.window_size.get()}, and step size {self.step_size.get()}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
