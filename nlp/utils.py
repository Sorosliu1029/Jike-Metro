import numpy as np
from keras.utils import to_categorical
import keras.backend as K
import matplotlib.pyplot as plt


def load_dataset(n, locale):
    human_vocab = set()
    machine_vocab = set()
    dataset = []

    with open('dataset_{}_{}.txt'.format(locale, n), 'rt', encoding='utf-8') as f:
        for line in f.readlines():
            m, h = line.split(',')
            m, h = m.ljust(9), h.strip()
            dataset.append((h, m))
            human_vocab.update(tuple(h))
            machine_vocab.update(tuple(m))

    human = dict(zip(sorted(human_vocab) + ['<unk>', '<pad>'],
                     list(range(len(human_vocab) + 2))))
    inv_machine = dict(enumerate(sorted(machine_vocab)))
    machine = {v: k for k, v in inv_machine.items()}

    return dataset, human, machine, inv_machine


def preprocess_data(dataset, human_vocab, machine_vocab, Tx, Ty):
    X, Y = zip(*dataset)

    X = np.array([string2int(i, Tx, human_vocab) for i in X])
    Y = np.array([string2int(t, Ty, machine_vocab) for t in Y])

    Xoh = np.array(list(map(lambda x: to_categorical(x, num_classes=len(human_vocab)), X)))
    Yoh = np.array(list(map(lambda x: to_categorical(x, num_classes=len(machine_vocab)), Y)))

    return X, Y, Xoh, Yoh


def string2int(string, length, vocab):
    if len(string) > length:
        string = string[:length]

    rep = list(map(lambda x: vocab[x] if x in vocab else vocab['<unk>'], string))

    if len(string) < length:
        rep += [vocab['<pad>']] * (length - len(string))

    return rep


def int2string(ints, inv_vocab):
    return [inv_vocab[i] for i in ints]

def softmax(x, axis=1):
    """Softmax activation function.
    # Arguments
        x : Tensor.
        axis: Integer, axis along which the softmax normalization is applied.
    # Returns
        Tensor, output of softmax transformation.
    # Raises
        ValueError: In case `dim(x) == 1`.
    """
    ndim = K.ndim(x)
    if ndim == 2:
        return K.softmax(x)
    elif ndim > 2:
        e = K.exp(x - K.max(x, axis=axis, keepdims=True))
        s = K.sum(e, axis=axis, keepdims=True)
        return e / s
    else:
        raise ValueError('Cannot apply softmax to a tensor that is 1D')

def run_examples(model, input_vocabulary, inv_output_vocabulary, examples, Tx, s0, c0):
    source = np.array([string2int(example, Tx, input_vocabulary) for example in examples])
    source = np.array(list(map(lambda x: to_categorical(x, num_classes=len(input_vocabulary)), source)))
    prediction = model.predict([source, s0, c0])
    prediction = np.argmax(prediction, axis = -1).transpose()

    predicted = []
    for i in range(len(examples)):
        output = [inv_output_vocabulary[int(j)] for j in prediction[i]]
        predicted.append(''.join(output))

    return zip(examples, predicted)
