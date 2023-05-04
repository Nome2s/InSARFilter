import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from goldstein_filter import goldstein_filter
from phase2raster import phase2raster
from write_int import write_int
from read_int import read_int


def browse_button_callback():
    file_path.set(filedialog.askopenfilename(filetypes=[("Interferogram files", "*.int")]))


def process_button_callback():
    alpha = float(alpha_entry.get())
    window_size = int(window_size_entry.get())
    step_size = int(step_size_entry.get())

    file = file_path.get()

    if file:
        data = read_int(file, width)

        # Display original image
        plt.figure()
        plt.imshow(np.angle(data), cmap='jet', vmin=-np.pi, vmax=np.pi)
        plt.colorbar()
        plt.title("Original Image")
        plt.show()

        # Perform Goldstein filtering
        filtered_data = goldstein_filter(data, alpha, window_size, step_size)

        # Display filtered image
        plt.figure()
        plt.imshow(np.angle(filtered_data), cmap='jet', vmin=-np.pi, vmax=np.pi)
        plt.colorbar()
        plt.title("Filtered Image")
        plt.show()

        # Display amplitude images (logarithmic scale)
        plt.figure()
        plt.imshow(np.log10(np.abs(data)), cmap='gray')
        plt.colorbar()
        plt.title("Original Amplitude Image (log10)")
        plt.show()

        plt.figure()
        plt.imshow(np.log10(np.abs(filtered_data)), cmap='gray')
        plt.colorbar()
        plt.title("Filtered Amplitude Image (log10)")
        plt.show()

        # Save filtered data
        out_file_name = "filtered_data.int"
        write_int(out_file_name, filtered_data)

        # Save filtered image as raster
        out_image_file_name = "filtered_data.tif"
        phase2raster(filtered_data, out_image_file_name)


# 图像宽度
width = 2551

# Create main window
root = tk.Tk()
root.title("Goldstein Filter")

file_path = tk.StringVar()

# Create labels, entries and buttons
file_path_label = tk.Label(root, text="待处理文件路径:")
file_path_label.grid(row=0, column=0, padx=5, pady=5)

browse_button = tk.Button(root, text="浏览", command=browse_button_callback)
browse_button.grid(row=0, column=1, padx=5, pady=5)

alpha_label = tk.Label(root, text="滤波参数:")
alpha_label.grid(row=1, column=0, padx=5, pady=5)
alpha_entry = tk.Entry(root)
alpha_entry.insert(0, "0.5")
alpha_entry.grid(row=1, column=1, padx=5, pady=5)

window_size_label = tk.Label(root, text="滑动窗口大小:")
window_size_label.grid(row=2, column=0, padx=5, pady=5)
window_size_entry = tk.Entry(root)
window_size_entry.insert(0, "32")
window_size_entry.grid(row=2, column=1, padx=5, pady=5)

step_size_label = tk.Label(root, text="滑动窗口步长:")
step_size_label.grid(row=3, column=0, padx=5, pady=5)
step_size_entry = tk.Entry(root)
step_size_entry.insert(0, "8")
step_size_entry.grid(row=3, column=1, padx=5, pady=5)

process_button = tk.Button(root, text="处理", command=process_button_callback)
process_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Run main loop
root.mainloop()
