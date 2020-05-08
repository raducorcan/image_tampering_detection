import random

import numpy as np


def normalize(x, mapping=float):
    mean = np.mean(x)
    std_dev = np.std(x)
    x = list(map(lambda e: (e - mean) / std_dev, x))
    x = list(map(mapping, x))
    return x


def from_tp_to_tpgt_filename(tp_filename):
    name, ext = tp_filename.split(".")
    return f'{name}_gt.png'


def load_data(data_type, batch_size, mode):
    with open(f'../res/new/{data_type}.csv') as f:
        while True:
            x = []
            y = []
            while len(x) < batch_size:
                line = f.readline()
                if line == "":
                    f.seek(0)
                    line = f.readline()
                    if mode == 'test':
                        break

                parts = line.strip("\n").split(",")
                label = int(parts[-1])
                x_val = list(map(float, parts[:-1]))
                x.append(x_val)
                y.append([1, 0] if label == 0 else [0, 1])
            yield (np.array(x), np.array(y))
            # yield (np.array(x), np.array(x))

            # for line in f:
            #     parts = line.split(",")
            #     x = list(map(float, parts[:-1]))
            #     y = int(parts[-1])
            #     yield {'input_1': np.asarray(x)}, {'output': y}


def shuffle():
    fid = open("../res/new/training.csv", "r")
    li = fid.readlines()
    fid.close()

    random.shuffle(li)

    fid = open("../res/new/sh_training.csv", "w")
    fid.writelines(li)
    fid.close()

# shuffle()
