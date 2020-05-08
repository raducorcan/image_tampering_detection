import os

from keras import Input, Model
from keras.callbacks import ModelCheckpoint
from keras.engine.saving import load_model
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

from preprocessing.utils import load_data


def create_nn():
    input_shape = Input((270,))
    layer = Dense(270, activation='relu')(input_shape)
    layer = Dense(128, activation='relu')(layer)
    layer = Dense(64, activation='relu')(layer)
    layer = Dense(2, activation='softmax')(layer)

    model = Model(input_shape, layer)
    return model


def create_nn_v2():
    input_shape = Input((270,))
    layer = Dense(270, activation='relu')(input_shape)
    layer = Dense(64, activation='relu')(layer)
    layer = Dense(64, activation='relu')(layer)
    layer = Dense(32, activation='relu')(layer)
    layer = Dense(2, activation='softmax')(layer)

    model = Model(input_shape, layer)
    return model


def train_nn():
    # model = create_nn()
    model = create_nn_v2()

    # model = load_model('../res/models/BAD_model_authbias.hdf5')
    model_path = os.path.join('../res/models/BAD_model_dropout.hdf5')
    checkpoint = ModelCheckpoint(model_path,
                                 monitor='val_accuracy',
                                 save_best_only=True,
                                 mode='max')
    callbacks = [checkpoint]

    # initial lr = 1e-3, decay = 1e-4, batch size = 64
    # transfer learn lr = 1e-5, decay = 1e-4, batch size = 256
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=1e-3, decay=1e-4), metrics=['accuracy'])
    train_samples = 216526
    validation_samples = 56572
    batch_size = 128
    epochs = 150
    train_gen = load_data('training', batch_size, mode='train')
    val_gen = load_data('validation', batch_size, mode='train')

    model.summary()
    model_info = model.fit_generator(
        train_gen,
        steps_per_epoch=train_samples // batch_size,
        epochs=epochs,
        verbose=1,
        callbacks=callbacks,
        validation_data=val_gen,
        validation_steps=validation_samples // batch_size)


train_nn()
