import numpy as np
import sys
from lxml import etree
import os

def read_interferogram(file_name, width, height):
    # 从二进制文件中读取干涉图数据并将其重新整形为二维矩阵
    data = np.fromfile(file_name, dtype=np.complex64).reshape((height, width))
    return data

def write_interferogram(file_name, data):
    # 将干涉图数据写入二进制文件
    data.astype(np.complex64).tofile(file_name)

def goldstein_filter(interferogram, filter_strength, window_size, step_size):
    # 对给定的干涉图执行 Goldstein 滤波
    height, width = interferogram.shape
    filtered_interferogram = np.zeros_like(interferogram)

    # 在干涉图上移动滤波窗口并应用滤波器
    for y in range(0, height - window_size, step_size):
        for x in range(0, width - window_size, step_size):
            # 提取当前滤波窗口
            window = interferogram[y:y+window_size, x:x+window_size]
            # 计算窗口的二维傅立叶变换
            spectrum = np.fft.fft2(window)
            # 计算滤波器掩模
            snr = np.abs(spectrum) / np.sqrt(filter_strength)
            mask = np.where(snr > 1, 1, snr)
            # 应用滤波器掩模
            filtered_spectrum = spectrum * mask
            # 计算逆傅立叶变换并将其添加到过滤后的干涉图中
            filtered_window = np.fft.ifft2(filtered_spectrum)
            filtered_interferogram[y:y+window_size, x:x+window_size] = filtered_window

    return filtered_interferogram

def main(file_name, output_folder, filter_strength=0.5, window_size=32, step_size=8):
    # 解析 XML 文件以获取干涉图的宽度和高度
    xml_file = file_name + '.xml'
    tree = etree.parse(xml_file)
    width = int(tree.findtext('.//property[@name="width"]/value'))
    height = int(tree.findtext('.//property[@name="length"]/value'))

    # 读取干涉图并应用 Goldstein 滤波
    interferogram = read_interferogram(file_name, width, height)
    filtered_interferogram = goldstein_filter(interferogram, filter_strength, window_size, step_size)

    # 将过滤后的干涉图写入输出文件
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
