import numpy as np
from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
#from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Reshape
#from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras import metrics
#import pickle
from keras.models import load_model
#from keras import backend as K
#from keras.callbacks import TensorBoard
#import matplotlib.pyplot as plt
#from keras.layers import Bidirectional
def top_10_accuracy(y_true, y_pred):
    return metrics.top_k_categorical_accuracy(y_true, y_pred, k=10)
def newpre(step,dim,modelname,x):
    model = Sequential()
    model.add(GRU(dim,input_shape=(step,dim)))
    model.compile(loss='mean_squared_error',optimizer='RMSprop',metrics=['accuracy'])
    model.load_weights(modelname)
    ypre = model.predict(x)[0].tolist()
    yprelist = []
    yprescore = []
    for k in range(10):
        yprelist.append(ypre.index(max(ypre)))
        yprescore.append(ypre[ypre.index(max(ypre))])
        ypre[ypre.index(max(ypre))]=0
    return yprelist,yprescore
#newpre(15,941,"a",11)