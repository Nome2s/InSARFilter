import numpy as np
import sys
from lxml import etree
import os
import scipy
import scipy.signal

def read_interferogram(file_name, width, height):
    data = np.fromfile(file_name, dtype=np.complex64).reshape((height, width))
    return data

def write_interferogram(file_name, data):
    data.astype(np.complex64).tofile(file_name)

def goldstein_filter(interferogram, filter_strength, window_size, step_size):
    height, width = interferogram.shape
    filtered_interferogram = np.zeros_like(interferogram)

    K = np.ones((3, 3)) / 9
    K_fft = np.fft.fft2(K, s=(window_size, window_size))
    K_fft = np.fft.fftshift(K_fft)

    for y in range(0, height, step_size):
        for x in range(0, width, step_size):
            y_end = min(y + window_size, height)
            x_end = min(x + window_size, width)
            
            window = interferogram[y:y_end, x:x_end]
            spectrum = np.fft.fft2(window)
            spectrum_shifted = np.fft.fftshift(spectrum)

            S = scipy.signal.convolve2d(np.abs(spectrum_shifted), K, mode='same')
            S[np.isnan(S) | np.isinf(S)] = 0  # 添加这行代码
            S = S / np.max(S)
            S = S ** filter_strength

            filtered_spectrum_shifted = spectrum_shifted * S
            filtered_spectrum = np.fft.ifftshift(filtered_spectrum_shifted)

            filtered_window = np.fft.ifft2(filtered_spectrum)

            filtered_interferogram[y:y_end, x:x_end] = filtered_window

    mask = np.isnan(interferogram)
    filtered_interferogram[mask] = np.nan
    mask = np.angle(interferogram) == 0
    filtered_interferogram[mask] = 0

    return filtered_interferogram

def main(file_name, output_folder, filter_strength=0.5, window_size=32, step_size=8):
    xml_file = file_name + '.xml'
    tree = etree.parse(xml_file)
    width = int(tree.findtext('.//property[@name="width"]/value'))
    height = int(tree.findtext('.//property[@name="length"]/value'))

    interferogram = read_interferogram(file_name, width, height)
    filtered_interferogram = goldstein_filter(interferogram, filter_strength, window_size, step_size)

    output_file = os.path.join(output_folder, 'filtered_' + os.path.basename(file_name))
    write_interferogram(output_file, filtered_interferogram)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        output_folder = sys.argv[2]
    else:
        print("Usage: python goldstein_filter.py <file_name> <output_folder> [<filter_strength> <window_size> <step_size>]")
        sys.exit(1)

    if len(sys.argv) > 3:
        filter_strength = float(sys.argv[3])
        window_size = int(sys.argv[4])
        step_size = int(sys.argv[5])
        main(file_name, output_folder, filter_strength, window_size, step_size)
    else:
        main(file_name, output_folder)
