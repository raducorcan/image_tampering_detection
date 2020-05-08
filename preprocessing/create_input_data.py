import os
import random

import numpy as np
from PIL import Image

from preprocessing.feature_encoding import get_feature_encoding
from preprocessing.utils import from_tp_to_tpgt_filename, normalize

im_dir = "..\\..\\datasets\\CASIA 2.0\\CASIA 2.0\\"
gt_dir = "..\\..\\datasets\\CASIA 2 Groundtruth\\CASIA 2 Groundtruth\\"
block_size = 32


def get_disjoint_blocks(image):
    im_w, im_h = image.size
    pixels = np.array(image.getdata()).reshape((im_h, im_w, 3))
    disjoint_blocks = [pixels[i:i + block_size, j:j + block_size]
                        for i in range(0, im_h - im_h % block_size, block_size) for j in range(0, im_w - im_w % block_size, block_size)
                       ]
    disjoint_blocks = np.asarray(disjoint_blocks)
    return disjoint_blocks


def create_data(data_type):
    x, y = [], []
    for im_type in ['Tp', 'Au']:
        for filename in os.listdir(os.path.join(im_dir, data_type, im_type)):
            if filename.lower() == 'thumbs.db':
                continue
            image = Image.open(os.path.join(im_dir, data_type, im_type, filename)).convert('YCbCr')
            disjoint_blocks = get_disjoint_blocks(image)

            if im_type == 'Tp':
                gt_image = Image.open(os.path.join(gt_dir, from_tp_to_tpgt_filename(filename))).convert('RGB')
                disjoint_blocks_gt = get_disjoint_blocks(gt_image)

            for i in range(len(disjoint_blocks)):
                block = disjoint_blocks[i]
                if im_type == 'Au' and random.random() < 0.4:
                    yield normalize(get_feature_encoding(block), mapping=str), 0
                else:
                    gt_block = disjoint_blocks_gt[i]
                    if 255 in gt_block:
                        yield normalize(get_feature_encoding(block), mapping=str), 1
                    elif random.random() < 0.4:
                        yield normalize(get_feature_encoding(block), mapping=str), 0

            image.close()
            gt_image.close()
