# from school import School
from personaMeta import PersonaMeta


def test_persona():
    # persona =  createPersona('test', 'kandhasamy', 'Ramesh_school')
    # persona_def = get_persona('test')
    # persona =  createPersona('test3', 'mnist_cnn_dna', 'Ramesh_school')
    # persona_def = get_persona('test3')

    persona_name, persona_age = get_name_and_age()
    persona_meta = PersonaMeta()
    persona_meta.create_age_0(persona_name, 'mnist_siamese', 'Ramesh_school')

    # persona =  createPersona(persona_name, 'mnist_siamese', 'Ramesh_school')
    # add_new_age(persona_name)

    # persona_def = get_persona(persona_name)
    # env = json.loads(persona_def.age.environments, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # if env.school:
    #     School().schedule(persona_def)


def get_name_and_age():
    return ('test4', '0')



