from unittest import TestCase

from personas.persona import Persona
from personas.train import Train
import sys

class TestPersona(TestCase):
    def test_create_persona(self):
        persona = Persona()
        persona_spec = {

        }
        persona.create_persona(persona_spec, 'abcd')
        return

    def test_training(self):
        sys.argv = ['test', '.././data/enwik8.gz']
        train = Train('p123')
        train.run()