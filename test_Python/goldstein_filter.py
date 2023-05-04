import numpy as np
from scipy.signal import convolve2d

def goldstein_filter(cpx, alpha, window_size, step_size):
    K = np.ones((3, 3))
    K = K / K.sum()
    K = np.fft.fftshift(np.fft.fft2(K))

    rows, cols = cpx.shape
    out_cpx = np.zeros((rows, cols))

    for ii in range(0, rows, step_size):
        for jj in range(0, cols, step_size):
            mm = ii + window_size - 1
            if mm > rows:
                mm = rows
            nn = jj + window_size - 1
            if nn > cols:
                nn = cols
            window = cpx[ii:mm, jj:nn]
            H = np.fft.fft2(window)
            H = np.fft.fftshift(H)
            S = convolve2d(np.abs(H), K, mode='same')
            S = S / S.max()
            S = S ** alpha
            H = H * S
            H = np.fft.ifftshift(H)
            window = np.fft.ifft2(H)
            out_cpx[ii:mm, jj:nn] = np.angle(window)

    idx = np.isnan(np.angle(cpx))
    out_cpx[idx] = 0
    idx = (np.angle(cpx) == 0)
    out_cpx[idx] = 0
    out_cpx = np.cos(out_cpx) + 1j * np.sin(out_cpx)
    return out_cpx
