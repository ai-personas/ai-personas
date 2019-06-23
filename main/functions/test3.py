from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import math
import os.path
import random
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
from tensorflow.python.ops import io_ops
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat

tf.enable_eager_execution()

def get_audio_output(wav_filename):
    wav_loader = io_ops.read_file(wav_filename)
    wav_decoder = contrib_audio.decode_wav(wav_loader)
    return wav_decoder

def write_audio_output(wav_output_filename, data, sample_rate):
    wav_encoder = contrib_audio.encode_wav(data, sample_rate)
    io_ops.write_file(wav_output_filename, wav_encoder)

karoke = get_audio_output('/home/ramesh/data/karoke/track/GuruvayurAppa.wav')
song = get_audio_output('/home/ramesh/data/karoke/song/GuruvayurAppa.wav')
# write_audio_output('/home/ramesh/data/karoke/track/GuruvayurAppa_out.wav', data.audio, data.sample_rate)
print(karoke.audio)

class Model(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        # self.dense1 = tf.keras.layers.Dense(units=100)
        # self.dense2 = tf.keras.layers.Dense(units=100)
        # self.lstm1 = tf.keras.layers.LSTM(128, dropout=0.2, recurrent_dropout=0.2)

    def call(self, inputs):
        # result = self.dense1(input)
        # result = self.dense2(result)
        # result = self.lstm1(inputs)
        return

# The loss function to be optimized
def loss(model, inputs, targets):
    pred = model(inputs)
    return tf.losses.absolute_difference(targets, pred)

def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, [model.W1, model.B1, model.W2, model.B2, model.W3, model.B3])


model = Model()
# model.compile(loss=loss, optimizer='adam')
# model.fit(karoke, song, batch_size=10)

# optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
#
# print(np.shape(data))
# print(np.shape(labels))
# labels = labels.astype(int)
# print(labels)
#
# training_outputs = tf.one_hot(indices=labels[0], depth=2, dtype=tf.int64)
# training_outputs = np.reshape(training_outputs, (1, 2))
# training_inputs = np.reshape(data[i, :], (1, 3920))
# # training_inputs = np.repeat(training_inputs,2,axis=1)
# # training_inputs = np.reshape(training_inputs, (2,3920))
#
# print(np.shape(training_outputs))
# print(np.shape(training_inputs))
#
# print("Initial loss: {:.3f}".format(loss(model, training_inputs, training_outputs)))
#
# # Training loop
# for i in range(2000):
#     training_inputs = np.reshape(data[i, :], (1, 3920))
#     #   training_inputs = np.repeat(training_inputs,2,axis=1)
#     #   training_inputs = np.reshape(training_inputs, (2,3920))
#     training_outputs = tf.one_hot(indices=labels[i], depth=2, dtype=tf.int64)
#     training_outputs = np.reshape(training_outputs, (1, 2))
#     grads = grad(model, training_inputs, training_outputs)
#     optimizer.apply_gradients(zip(grads, [model.W1, model.B1, model.W2, model.B2, model.W3, model.B3]),
#                               global_step=tf.train.get_or_create_global_step())
#     if i % 20 == 0:
#         print("Loss at step {:03d}: {:.3f}".format(i, loss(model, training_inputs, training_outputs)))
#
# print("Final loss: {:.3f}".format(loss(model, training_inputs, training_outputs)))
# # print("W = {}, B = {}".format(model.W.numpy(), model.B.numpy()))
