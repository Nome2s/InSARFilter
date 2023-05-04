import numpy as np

def write_int(file_name, data):
    data = data.T
    data = data.ravel()
    imag_data = np.sin(data)
    real_data = np.cos(data)
    count = 2 * len(data)
    output_data = np.zeros(count)
    output_data[0::2] = real_data
    output_data[1::2] = imag_data
    output_data.astype(np.float32).tofile(file_name)
