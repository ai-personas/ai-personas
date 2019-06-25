import numpy as np
import tensorflow as tf

def generate_brain():
    return Model()

def learn(model, inputs, outputs, epoch):
    global_step = tf.train.get_or_create_global_step()
    logdir = '/tmp/tb'
    writer = tf.contrib.summary.create_file_writer(logdir)
    writer.set_as_default()

    X = transform_feed(inputs)
    Y = transform_feed(outputs)
    for i in range(epoch):
        global_step.assign_add(1)
        with tf.contrib.summary.record_summaries_every_n_global_steps(1):
            optimizer = tf.train.AdamOptimizer(0.001)
            _grad = grad(model, X, Y)
            optimizer.apply_gradients(zip(_grad, model.variables))

def self_evaluate(model, inputs, outputs):
    logdir = '/tmp/tb'
    writer = tf.contrib.summary.create_file_writer(logdir)
    writer.set_as_default()

    epoch_accuracy = tf.contrib.eager.metrics.Accuracy()
    predicted = model.call(transform_feed(inputs))
    epoch_accuracy(predicted, outputs)
    print(epoch_accuracy.result())
    return epoch_accuracy.result()

class Model(tf.keras.Model):
  def __init__(self):
    super(Model, self).__init__(name='')
    self.dense1 = tf.keras.layers.Dense(256, input_shape=(16,), activation='tanh')
    self.dense2 = tf.keras.layers.Dense(16, input_shape=(256,), activation='tanh')

  def call(self, inputs):
      x1 = self.dense1(inputs)
      x2 = self.dense2(x1)
      return x2

def loss(model, inputs, targets):
  error = model(inputs) - targets
  return tf.reduce_mean(tf.square(error))

def grad(model, inputs, targets):
    with tf.GradientTape() as grad_tape:
        loss_val = loss(model, inputs, targets)
        tf.contrib.summary.scalar('loss', loss_val)
    return grad_tape.gradient(loss_val, model.variables)

def transform_feed(feed):
    feed_bit_size = 16
    x = np.zeros((len(feed), feed_bit_size))
    for i in range(len(feed)):
        bits = intTo2sCompStr(feed[i], feed_bit_size)
        for k, c in enumerate(list(bits)):
            x[i, k] = int(c)
    return x

def intTo2sCompStr(num, bitWidth):
    num &= 0xffff
    formatStr = '{:0'+str(bitWidth)+'b}'
    ret =  formatStr.format(int(num))
    return ret
