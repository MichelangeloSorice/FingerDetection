import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.models import Sequential
from keras.losses import SparseCategoricalCrossentropy


def create_out_folder(dir):
    try:
        os.mkdir(dir)
    except OSError:
        print("Creation of the directory %s failed" % dir)
    else:
        print("Successfully created the directory %s " % dir)
    return dir


def plot_history(history, test_out):
    loss_plot = os.path.join(test_out, "loss_plt.png")
    plt.plot(history.history['loss'], label='Sparse Cat. Cross Entropy (train data)')
    plt.plot(history.history['val_loss'], label='Sparse Cat. Cross Entropy (validation data)')
    plt.title('SCCE for model')
    plt.ylabel('SCCE value')
    plt.xlabel('No. epoch')
    plt.legend(loc="upper left")
    plt.savefig(loss_plot)
    plt.show()

def save_history(history, test_out):
    history_csv_file = os.path.join(test_out, 'history.csv')

    # convert the history.history dict to a pandas DataFrame:
    hist_df = pd.DataFrame(history.history)
    with open(history_csv_file, mode='w') as f:
        hist_df.to_csv(f)


def save_summary(model, test_out):
    summary_file = os.path.join(test_out, 'model_summary.txt')
    print(model.summary(), file=open(summary_file, 'w'))


path = os.getcwd()
dataset = os.path.join(path, "dataset")
test_out = create_out_folder(os.path.join(path, "training_res"))

# loading data
train_data = np.load(os.path.join(dataset, "train_data.npy"))
train_pred = np.load(os.path.join(dataset, "train_pred.npy"))

test_data = np.load(os.path.join(dataset, "test_data.npy"))
test_pred = np.load(os.path.join(dataset, "test_pred.npy"))

# Shuffling data
idx = np.random.permutation(len(train_data))
trdata_sh, trpred_sh = train_data[idx], train_pred[idx]

idx = np.random.permutation(len(test_data))
tsdata_sh, tspred_sh = test_data[idx], test_pred[idx]

print(train_data.shape)
print(train_pred.shape)
print(test_data.shape)
print(test_pred.shape)

# Preparing model
overfitCallback = EarlyStopping(monitor='val_loss', patience=10)

model = Sequential([
    Conv2D(32, kernel_size=(3, 3), input_shape=(40, 40, 1), activation='relu'),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax'),
])

# Use sparse version of categorical crossentropy as sample can have a single class - NB requires data as single array
model.compile('adam', loss=SparseCategoricalCrossentropy(), metrics=['sparse_categorical_accuracy'])

history = model.fit(trdata_sh, trpred_sh, validation_data=(tsdata_sh, tspred_sh), epochs=100, callbacks=[overfitCallback])

model.save(os.path.join(test_out, 'model.h5'))
save_history(history, test_out)
plot_history(history, test_out)
save_summary(model, test_out)
