import keras


class OutputTransformation:

    @staticmethod
    def output_transform_by_dna(transform_type, y, channel):
        # todo: transform for all output channel
        if transform_type == 'categorical to integer':
            return OutputTransformation.categorical_to_integer(y, channel)

    @staticmethod
    def categorical_to_integer(y, channel):
        # todo: specify output channel
        y_transformed = keras.utils.to_categorical(y, int(channel.size))
        return y_transformed
