from kerasPhysical import KerasSoftPhysical


class Energy():

    def power(self, brain, personaDef):
        if personaDef.softPhysical == 'keras':
            keras = KerasSoftPhysical()

