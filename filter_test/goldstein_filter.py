import numpy as np
import sys
from lxml import etree

def read_interferogram(file_name, width, height):
    data = np.fromfile(file_name, dtype=np.complex64).reshape((height, width))
    return data

def write_interferogram(file_name, data):
    data.astype(np.complex64).tofile(file_name)

def goldstein_filter(interferogram, filter_strength, window_size, step_size):
    height, width = interferogram.shape
    filtered_interferogram = np.zeros_like(interferogram)

    for y in range(0, height - window_size, step_size):
        for x in range(0, width - window_size, step_size):
            window = interferogram[y:y+window_size, x:x+window_size]
            spectrum = np.fft.fft2(window)
            snr = np.abs(spectrum) / np.sqrt(filter_strength)
            mask = np.where(snr > 1, 1, snr)
            filtered_spectrum = spectrum * mask
            filtered_window = np.fft.ifft2(filtered_spectrum)
            filtered_interferogram[y:y+window_size, x:x+window_size] = filtered_window

    return filtered_interferogram

def main(file_name, filter_strength=0.5, window_size=32, step_size=8):
    xml_file = file_name + '.xml'
    tree = etree.parse(xml_file)
    width = int(tree.findtext('.//property[@name="width"]/value'))
    height = int(tree.findtext('.//property[@name="length"]/value'))

    interferogram = read_interferogram(file_name, width, height)
    filtered_interferogram = goldstein_filter(interferogram, filter_strength, window_size, step_size)

    output_file = 'filtered_' + file_name
    write_interferogram(output_file, filtered_interferogram)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        print("Usage: python goldstein_filter.py <file_name> [<filter_strength> <window_size> <step_size>]")
        sys.exit(1)

    if len(sys.argv) > 2:
        filter_strength = float(sys.argv[2])
        window_size = int(sys.argv[3])
        step_size = int(sys.argv[4])
        main(file_name, filter_strength, window_size, step_size)
    else:
        main(file_name)
