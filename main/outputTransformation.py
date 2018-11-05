import keras


class OutputTransformation:

    @staticmethod
    def output_transform_by_dna(transform_type, y, dna):
        if transform_type == 'categorical to integer':
            return OutputTransformation.categorical_to_integer(y, dna)

    @staticmethod
    def categorical_to_integer(y, dna):
        y_transformed = keras.utils.to_categorical(y, int(dna.output[0].size))
        return y_transformed
