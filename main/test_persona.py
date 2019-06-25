# from school import School
# from personaDef import PersonaDef
from energyServer.energy import Energy
from environments.books.random_integers.generate_env_random_integers import generate_environment_random_integers
from personas.generate_persona_rpt01 import generate_persona_rpt01
import tensorflow as tf

tf.compat.v1.enable_eager_execution()


def test_persona():
    generate_environment_random_integers()
    persona_def = generate_persona_rpt01()
    energy = Energy('localhost')
    energy.to(persona_def)
    return

