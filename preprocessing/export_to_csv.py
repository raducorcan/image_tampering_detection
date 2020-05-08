import numpy as np

from preprocessing.create_input_data import create_data

"""
only used in feature extraction
not part of the training pipeline
"""


def export_to_csv(gen, filename):
    with open(filename, 'w') as f:
        for x, y in gen:
            f.write(",".join(x) + f',{y}\n')


def raw_image_to_csv():
    train_gen = create_data('Training')
    test_gen = create_data('Test')
    val_gen = create_data('Validation')

    export_to_csv(train_gen, '../res/new/training.csv')
    export_to_csv(test_gen, '../res/new/test.csv')
    export_to_csv(val_gen, '../res/new/validation.csv')


raw_image_to_csv()
