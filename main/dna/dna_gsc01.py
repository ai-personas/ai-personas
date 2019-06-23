import numpy as np
import tensorflow as tf

def generate_brain():
    return Model()

def learn(model, inputs, outputs):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

    training_outputs = tf.one_hot(indices=outputs[0], depth=2, dtype=tf.float64)
    training_inputs = np.reshape(inputs[i, :], (1, 3920))

    print(np.shape(training_outputs))
    print(np.shape(training_inputs))

    print("Initial loss: {:.3f}".format(loss(model, training_inputs, training_outputs)))

    # Training loop
    for i in range(1000):
        training_inputs = np.reshape(inputs[i, :], (1, 3920))
        training_outputs = tf.one_hot(indices=outputs[i], depth=2, dtype=tf.float64)
        grads = grad(model, training_inputs, training_outputs)
        optimizer.apply_gradients(zip(grads, [model.W, model.B]),
                                  global_step=tf.train.get_or_create_global_step())
        if i % 20 == 0:
            print("Loss at step {:03d}: {:.3f}".format(i, loss(model, training_inputs, training_outputs)))

    print("Final loss: {:.3f}".format(loss(model, training_inputs, training_outputs)))
    print("W = {}, B = {}".format(model.W.numpy(), model.B.numpy()))


class Model(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()

        self.W = tf.get_variable(
            name='weights1',
            initializer=tf.truncated_normal_initializer(stddev=0.001),
            shape=[3920, 2], dtype=tf.float64)

        self.B = tf.get_variable(
            name='bias1', initializer=tf.zeros_initializer, shape=[2], dtype=tf.float64)

    def call(self, inputs):
        return tf.add(tf.matmul(inputs, self.W), self.B)


# The loss function to be optimized
def loss(model, inputs, targets):
    #   print(inputs.dtype)
    #   print(targets.dtype)
    #   print(model(inputs).dtype)
    error = model(inputs) - targets
    return tf.reduce_mean(tf.square(error))


def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, [model.W, model.B])


