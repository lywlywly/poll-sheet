import cv2
import numpy as np

narr = np.full((1440, 2560, 3), 10)
# F = np.full((1440, 2560), 255)
# O = np.full((1440, 2560), 0)
# A = np.full((1440, 2560), 165)
# B = np.full((1440, 2560), 203)
# C = np.full((1440, 2560), 242)
#
# narr[..., 0] = A
# narr[..., 1] = B
# narr[..., 2] = C

cv2.imwrite('10.jpg', narr)
