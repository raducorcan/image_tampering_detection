from preprocessing.utils import load_data
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix, precision_recall_curve, auc
from keras.engine.saving import load_model
import numpy as np
import matplotlib.pyplot as plt


def get_y_real():
    res = []
    with open('../res/new/test.csv', 'r') as f:
        for line in f:
            line = line.strip("\n")
            y_real = list(map(float, line.split(",")[-1]))
            res.append(y_real)
    return res


batch_size = 128
test_samples = 59285
test_gen = load_data('test', batch_size, mode='test')
model = load_model("../res/models/model.hdf5")

y_real = get_y_real()

Y_pred = model.predict_generator(test_gen, test_samples // batch_size + 1)
# y_pred = np.argmax(Y_pred, axis=1)
y_pred = []

for el in Y_pred:
    y_pred += [1 if el[1] >= 0.3 else 0]

print('Classification Report')
target_names = ['Authentic', 'Tampered']
print(classification_report(y_real, y_pred, target_names=target_names))
cm = confusion_matrix(
    list(map(lambda x: int(x[0]), y_real)),
    y_pred,
    normalize='true')

print(cm)
prec, rec, ll = precision_recall_curve(y_real, list(map(lambda x: x[1], Y_pred)))
plt.plot(rec, prec)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.show()
print(auc(rec, prec))
# plt.matshow(cm, cmap='binary')
# plt.show()



