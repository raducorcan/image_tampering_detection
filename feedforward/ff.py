import base64
import os

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

from preprocessing.create_input_data import get_disjoint_blocks, block_size
from preprocessing.feature_encoding import get_feature_encoding
from preprocessing.utils import normalize


class Detector:
    def __init__(self):
        self.model = tf.keras.models.load_model("./res/models/model.hdf5")

    @staticmethod
    def neighbour_count(label_matrix, i, j):
        dl = [-1, -1, 0, 1, 1, 1, 0, -1]
        dc = [0, 1, 1, 1, 0, -1, -1, -1]
        count = 0
        for k in range(8):
            if len(label_matrix) > i + dl[k] >= 0 and len(label_matrix[0]) > j + dc[k] >= 0:
                if label_matrix[i + dl[k], j + dc[k]] >= 0.7:
                    count += 1
        return count

    @staticmethod
    def get_coords(index, im_w):
        blocks_per_line = im_w // block_size
        line = index // blocks_per_line
        col = index % blocks_per_line
        x = line * block_size
        y = col * block_size
        return x, y

    def label_blocks(self, img):
        im_w, im_h = img.size
        rows = im_h // block_size
        cols = im_w // block_size
        label_matrix = np.zeros((rows, cols))

        blocks = get_disjoint_blocks(img)
        for i in range(len(blocks)):
            block = blocks[i]
            x, y = Detector.get_coords(i, im_w)

            in_data = normalize(get_feature_encoding(block))
            in_data = np.reshape(in_data, (1, 270))
            out = self.model.predict(in_data)[0]

            label_matrix[x // block_size, y // block_size] = out[-1]
        return label_matrix

    def feedforward(self, filename):
        img_show = Image.open(filename)
        img = Image.open(filename).convert('YCbCr')
        im_w, im_h = img.size
        rows = im_h // block_size
        cols = im_w // block_size
        gray = Image.fromarray(np.zeros((rows * block_size, cols * block_size)))
        label_matrix = self.label_blocks(img)

        all, tp = 0, 0
        for i in range(rows):
            for j in range(cols):
                all += 1
                right = (i, j + 1) if j + 1 < cols else (i, j - 1)
                down = (i + 1, j) if i + 1 < rows else (i - 1, j)
                right_down = 0
                if i + 1 < rows and j + 1 < cols:
                    right_down = i + 1, j + 1
                elif i + 1 < rows and j + 1 >= cols:
                    right_down = i + 1, j - 1
                elif i + 1 >= rows and j + 1 < cols:
                    right_down = i - 1, j + 1
                else:
                    right_down = i - 1, j - 1
                label_matrix[i, j] = 0.25 * (
                            label_matrix[i, j] + label_matrix[right_down] + label_matrix[right] + label_matrix[down])

                x = i * block_size
                y = j * block_size
                if label_matrix[i, j] >= 0.6:
                    tp += 1
                    # red contour squares
                    img_show = cv2.rectangle(np.ascontiguousarray(img_show), (y, x), (y + block_size, x + block_size),
                                             (255, 0, 0), 2)

                temp = int(label_matrix[i, j] * 255) if label_matrix[i, j] >= 0.6 else 0
                # grayscale filled squares
                gray = cv2.rectangle(np.ascontiguousarray(gray), (y, x), (y + block_size, x + block_size),
                                     (temp, temp, temp), -1)
        img_show = cv2.cvtColor(np.ascontiguousarray(img_show), cv2.COLOR_BGR2RGB)

        cv2.imwrite("./res/temp/sent.png", img_show)
        cv2.imwrite("./res/temp/sent_gray.png", gray)

        with open('./res/temp/sent.png', 'rb') as im:
            enc = base64.b64encode(im.read())
        with open('./res/temp/sent_gray.png', 'rb') as im:
            enc_gray = base64.b64encode(im.read())

        os.remove("./res/temp/sent.png")
        os.remove("./res/temp/sent_gray.png")
        return enc.decode('UTF-8'), enc_gray.decode('UTF-8'), (tp * 100) / all if all != 0 else 0
