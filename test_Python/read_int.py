import numpy as np

def read_int(file_name, width):
    data = np.fromfile(file_name, dtype=np.float32)
    count = len(data)
    data = data[0::2] + 1j * data[1::2]
    lines = count // (width * 2)
    data = data.reshape((width, lines)).T
    return data
