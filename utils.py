import numpy as np
import librosa.display as lbdis
import matplotlib.pyplot as plt
from audio_processor import AudioProcessor
import os

from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


def save_data(save_dir, data, fname='data.npy'):
    np.save(os.path.join(save_dir, fname), np.vstack(data))
    print("Data has been saved to {:s}/{:s}".format(save_dir, fname))


def visualize_waves(path, frame_per_second):
    AP = AudioProcessor(feature_length=30,
                        frame_per_second=frame_per_second,
                        path=path)
    origin = AP.audio_data
    kernel = AP.get_window(method='square')
    audio = AP._conv1D(kernel, origin)
    avg_zero_rate = AP.get_avg_zero_rate(origin, kernel)
    energy = AP.get_energy(origin, kernel)
    boundary = AP.get_boundary(energy)

    features = AP.get_global_feature()

    # visualize
    plt.figure(1)
    lbdis.waveplot(audio, sr=frame_per_second)
    plt.title('windowed')
    plt.show()

    plt.figure(2)
    lbdis.waveplot(origin, sr=48000)
    plt.title("origin")
    plt.show()

    plt.figure(3)
    lbdis.waveplot(avg_zero_rate, sr=frame_per_second)
    plt.title('azr')
    plt.show()

    plt.figure(4)
    lbdis.waveplot(energy, sr=frame_per_second)
    plt.title('energy')
    plt.show()

    plt.figure(5)
    lbdis.waveplot(audio[boundary[0]:boundary[1] + 1], sr=frame_per_second)
    plt.title('cropped_avg')
    plt.show()

    plt.figure(6)
    lbdis.waveplot(energy[boundary[0]:boundary[1] + 1], sr=frame_per_second)
    plt.title('cropped energy')
    plt.show()

    print(len(audio))
    print("number of features", len(features))
    print(features[0])
    features = np.array(features)
    print(features.shape)


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(np.floor(cm * 10000)/100)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.show()
    return ax