from unittest import TestCase

from personas.persona import Persona
from personas.train import Train
import sys


class TestPersona(TestCase):
    def test_create_persona(self):
        return

    def test_training(self):
        train = Train('p123')
        train.run()
