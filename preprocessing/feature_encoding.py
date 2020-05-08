import numpy as np
import pywt


def split_in_components(block):
    return [pixel[0] for line in block for pixel in line], \
           [pixel[1] for line in block for pixel in line], \
           [pixel[2] for line in block for pixel in line]


def get_feature_encoding(block):
    encoding = []
    y, cb, cr = split_in_components(block)
    for comp in [y, cb, cr]:
        comp = np.asarray(comp).reshape(len(block[0]), len(block))
        for i in range(1, 6):
            cA, (cH2, cV2, cD2), (cH1, cV1, cD1), (cH0, cV0, cD0) = pywt.wavedec2(comp, f'db{i}', level=3)
            for el in [cH2, cV2, cD2, cH1, cV1, cD1, cH0, cV0, cD0]:  # drop approximation coefficients
                encoding.extend([np.mean(el), np.std(el)])
                # encoding.extend([np.sum(el), np.mean(el), np.std(el)])
    return encoding
