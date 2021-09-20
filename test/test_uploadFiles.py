from unittest import TestCase
import os
from src.environments.UploadFiles import UploadFiles


class TestUploadFiles(TestCase):

    def test_upload_local_files(self):
        uploadFiles = UploadFiles()
        filePath = os.path.abspath("./data")
        uploadFiles.uploadLocalFile('environments.library.envwik8',
                                    'enwik8.gz',
                                    filePath,
                                    'The enwik8 data was downloaded from the Hutter prize page: http://prize.hutter1.net/')

