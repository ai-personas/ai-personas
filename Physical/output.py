import theano 
from theano import tensor as T 
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.cm as cm 

X = T.fmatrix() 
Y = T.fmatrix() 

w_h1 = init_weights((40000, 400)) 
w_h2 = init_weights((400, 200)) 
w_h3 = init_weights((200, 40000)) 

def model(X,w_h1,w_h2,w_h3,p_drop_input, p_drop_hidden):
    X = dropout(X, p_drop_input) 
    w_o_h1=rectify(T.dot(X, w_h1)) 
    w_o_h1= dropout(w_o_h1, p_drop_input) 
    w_o_h2=rectify(T.dot(w_o_h1, w_h2)) 
    w_o_h2= dropout(w_o_h2, p_drop_input) 
    py_x = softmax(T.dot(w_o_h2, w_h3)) 
    return py_x 

def dropout(X, p=0.): 
    if p > 0: 
    retain_prob = 1 - p 
    X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX) 
    X /= retain_prob 
    return X 

def rectify(X): 
    return T.maximum(X, 0.) 

def softmax(X): 
    e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x')) 
    return e_x / e_x.sum(axis=1).dimshuffle(0, 'x') 

def floatX(X): 
    return np.asarray(X, dtype=theano.config.floatX) 

def init_weights(shape): 
    return theano.shared(floatX(np.random.randn(*shape) * 0.01)) 

def RMSprop(cost, params, lr=0.001, rho=0.9, epsilon=1e-6): 
    grads = T.grad(cost=cost, wrt=params) 
    updates = [] 
    for p, g in zip(params, grads): 
        acc = theano.shared(p.get_value() * 0.) 
        acc_new = rho * acc + (1 - rho) * g ** 2 
        gradient_scaling = T.sqrt(acc_new + epsilon) 
        g = g / gradient_scaling 
        updates.append((acc, acc_new)) 
        updates.append((p, p - lr * g)) 
    return updates 

noise_y_x = model(X,w_h1,w_h2,w_h3)
cost = T.mean(T.nnet.categorical_crossentropy(noise_y_x, Y))
params = [w_h1,w_h2,w_h3]
updates = RMSprop(cost, params, lr=0.001) 
train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True) 
predict = theano.function(inputs=[X], outputs=py_x, allow_input_downcast=True) 
