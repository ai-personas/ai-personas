
class PredefinedLambda:

    @staticmethod
    def euclidean_distance(vects):
        from keras import backend as K
        x, y = vects
        sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
        return K.sqrt(K.maximum(sum_square, K.epsilon()))

