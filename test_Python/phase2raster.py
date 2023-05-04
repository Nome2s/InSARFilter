import numpy as np
import cv2

def phase2raster(cpx, out_file_name):
    phase = np.angle(cpx)
    phase = (phase + np.pi) / (2 * np.pi)
    phase_rgb = cv2.applyColorMap((phase * 255).astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imwrite(out_file_name, phase_rgb)
