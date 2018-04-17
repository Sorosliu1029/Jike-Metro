# coding: utf-8

from keras.layers import Bidirectional, Concatenate, Permute, Dot, Input, LSTM, Multiply
from keras.layers import RepeatVector, Dense, Activation, Lambda
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.models import load_model, Model
import keras.backend as K
import numpy as np
import sys
from datetime import datetime

from utils import *

def load(m, locale):
    # dataset, human_vocab, machine_vocab, inv_machine_vocab
    return load_dataset(m, locale)

def preprocess(dataset, human_vocab, machine_vocab, Tx, Ty):
    # X, Y, Xoh, Yoh
    return preprocess_data(dataset, human_vocab, machine_vocab, Tx, Ty)

def one_step_attention(a, s_prev):
    s_prev = repeator(s_prev)
    concat = concatenator([a, s_prev])
    e = densor(concat)
    alphas = activator(e)
    context = dotor([alphas, a])
    
    return context

def model(Tx, Ty, n_a, n_s, human_vocab_size, machine_vocab_size):
    X = Input(shape=(Tx, human_vocab_size))
    s0 = Input(shape=(n_s,), name='s0')
    c0 = Input(shape=(n_s,), name='c0')
    s = s0
    c = c0
    
    outputs = []
    
    a = Bidirectional(LSTM(n_a, return_sequences=True))(X)
    
    for t in range(Ty):
        context = one_step_attention(a, s)
        s, _, c = post_activation_LSTM_cell(context, initial_state=[s, c])
        out = output_layer(s)
        outputs.append(out)
    
    model = Model(inputs = [X, s0, c0], outputs = outputs, name='TranslationModel')
    
    return model
    

if __name__ == '__main__':
    m = pow(10, int(sys.argv[1]))
    locale = sys.argv[2]
    assert locale in ('zh', 'en')

    print('Use dataset with {} in {}'.format(m, locale))

    dataset, human_vocab, machine_vocab, inv_machine_vocab = load(m, locale)
    Tx = 15
    Ty = 9
    X, Y, Xoh, Yoh = preprocess(dataset, human_vocab, machine_vocab, Tx, Ty)

    repeator = RepeatVector(Tx, name='rep')
    concatenator = Concatenate(axis=-1, name='conc')
    densor = Dense(1, activation='relu', name='densor')
    activator = Activation(softmax, name='attention_weights')
    dotor = Dot(axes=1, name='doter')

    n_a = 32
    n_s = 64
    post_activation_LSTM_cell = LSTM(n_s, return_state = True, name='post_activation')
    output_layer = Dense(len(machine_vocab), activation=softmax, name='output')

    md = model(Tx, Ty, n_a, n_s, len(human_vocab), len(machine_vocab))

    opt = Adam(lr=0.005, beta_1=0.9, beta_2=0.999, decay=0.01)
    md.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    s0 = np.zeros((m, n_s))
    c0 = np.zeros((m, n_s))
    outputs = list(Yoh.swapaxes(0,1))

    epochs = int(sys.argv[3])

    print('Train with {} epochs'.format(epochs))
    md.fit([Xoh, s0, c0], outputs, epochs=epochs, batch_size=100)

    test_dataset, *_ = load(100, locale)
    test_X, _ = zip(*test_dataset)
    test_X = test_X + (
        '逗你玩',
        '啥都不会',
        '分钟秒',
        '小时天',
    )
    test_s0 = np.zeros((len(test_X), n_s))
    test_c0 = np.zeros((len(test_X), n_s))
    predicted = run_examples(md, human_vocab, inv_machine_vocab, test_X, Tx, test_s0, test_c0)

    for p in predicted:
        print('human:   ', p[0])
        print('machine: ', p[1])
        print()
   
    now = datetime.now().strftime('%m%d-%H-%M')
    md.save_weights('parse_time_{}.h5'.format(now))