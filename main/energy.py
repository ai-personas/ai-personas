from kerasPhysical import KerasSoftPhysical


class Energy():

    def power(self, persona_def, x_train, y_train, x_test, y_test):
        if persona_def.softPhysical == 'keras':
            keras = KerasSoftPhysical(persona_def)
            keras.teach(x_train, y_train, x_test, y_test)
