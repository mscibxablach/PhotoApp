import numpy as np
import cv2

class ImageUtils:
    @staticmethod
    def convert_inmemory_file_to_cv2_image(inmemory_file):
        nparr = np.fromstring(inmemory_file, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return img