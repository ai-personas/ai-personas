
import random

import numpy as np


class InputTransformation:

    @staticmethod
    def input_transform_by_dna(transform_type, x, y):
        if transform_type == 'positiveNegativePair':
            return InputTransformation.createPositiveNegativePair(x, y, 10)

    @staticmethod
    def createPositiveNegativePair(x_train, y_train, num_classes):
        # create training+test positive and negative pairs
        digit_indices = [np.where(y_train == i)[0] for i in range(num_classes)]
        tr_pairs, tr_y = InputTransformation.create_pairs(x_train, digit_indices, num_classes)
        print("tr_y:", tr_y)
        return (tr_pairs, tr_y)


    @staticmethod
    def create_pairs(x, digit_indices, num_classes):
        '''Positive and negative pair creation.
        Alternates between positive and negative pairs.
        '''
        pairs = []
        labels = []
        n = min([len(digit_indices[d]) for d in range(num_classes)]) - 1
        print("create pair min:", n)
        for d in range(num_classes):
            for i in range(n):
                z1, z2 = digit_indices[d][i], digit_indices[d][i + 1]
                pairs += [[x[z1], x[z2]]]
                inc = random.randrange(1, num_classes)
                dn = (d + inc) % num_classes
                z1, z2 = digit_indices[d][i], digit_indices[dn][i]
                pairs += [[x[z1], x[z2]]]
                labels += [1, 0]
        return np.array(pairs), np.array(labels)


