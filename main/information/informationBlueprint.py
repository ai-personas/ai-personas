import imp
import os


class InformationBlueprint(object):

    PROTO_PYTHON_EXTENSION = "_pb2.py"
    INFORMATION_BLUEPRINT = "informationBlueprint_"

    def get(self, version):
        bluePrintName = self.INFORMATION_BLUEPRINT + version + self.PROTO_PYTHON_EXTENSION

        information_blueprint_path = os.path.abspath(os.path.join(bluePrintName))
        print(information_blueprint_path)
        # informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()
        #
        # print(list(informationBlueprint.DESCRIPTOR.fields_by_name.keys()))
        #
        # for f in informationBlueprint.DESCRIPTOR.fields:
        #     print(f.type)

inf = InformationBlueprint()
inf.get("v1")
