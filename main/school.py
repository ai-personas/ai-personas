import json

from keras.datasets import mnist

from kerasPhysical import KerasSoftPhysical


class School():

    def schedule(self, personaDef):
        #TODO: check previous passed grades????

        school = json.loads(personaDef.age.environments)
        dna = json.loads(personaDef.dna)

        train_img_count = int(school.grades[0].courses[0].image_count)
        test_img_count = int(school.grades[0].test[0].image_count)

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        if school.grades[0].courses[0].data_provider == 'keras.mnist':
            (x_train, y_train), (x_test, y_test) = mnist.load_data()

        x_train = x_train.reshape(train_img_count, 784)
        x_test = x_test.reshape(test_img_count, 784)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255

        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')

        return

    def power(self, brain, personaDef):
        if personaDef.softPhysical == 'keras':
            keras = KerasSoftPhysical()


