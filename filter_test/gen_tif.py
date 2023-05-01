import numpy as np
import sys
import rasterio
import matplotlib.pyplot as plt
from rasterio.transform import Affine


def read_interferogram(file_name, width, height):
    data = np.fromfile(file_name, dtype=np.complex64).reshape((height, width))
    return data


def save_phase_tif(phase_data, output_file):
    transform = Affine.translation(0.5, 0.5) * Affine.scale(1, -1)

    with rasterio.open(
            output_file,
            'w',
            driver='GTiff',
            height=phase_data.shape[0],
            width=phase_data.shape[1],
            count=1,
            dtype=phase_data.dtype,
            crs='+proj=latlong',
            transform=transform,
    ) as dst:
        dst.write(phase_data, 1)


def main(file_name, width, height):
    interferogram = read_interferogram(file_name, width, height)
    phase_data = np.angle(interferogram)

    cmap = plt.get_cmap('hsv')
    phase_color = cmap((phase_data + np.pi) / (2 * np.pi))
    phase_color_uint8 = (phase_color * 255).astype(np.uint8)

    output_file = file_name.replace('.int', '.int.tif')
    save_phase_tif(phase_color_uint8, output_file)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        file_name = sys.argv[1]
        width = int(sys.argv[2])
        height = int(sys.argv[3])
    else:
        print("Usage: python gen_tif.py <file_name> <width> <height>")
        sys.exit(1)

    main(file_name, width, height)
