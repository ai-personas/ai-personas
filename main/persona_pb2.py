# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: persona.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='persona.proto',
  package='persona',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rpersona.proto\x12\x07persona\"\x8a\x02\n\x07Persona\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x64na\x18\x02 \x01(\t\x12\x14\n\x0csoftPhysical\x18\x03 \x01(\t\x12\x14\n\x0chardPhysical\x18\x04 \x01(\t\x12!\n\x03\x61ge\x18\x05 \x01(\x0b\x32\x14.persona.Persona.Age\x12%\n\x05\x62rain\x18\x06 \x01(\x0b\x32\x16.persona.Persona.Brain\x1a@\n\x03\x41ge\x12\x0b\n\x03old\x18\x01 \x01(\x04\x12\x16\n\x0eknowledgeCycle\x18\x02 \x01(\x04\x12\x14\n\x0c\x65nvironments\x18\x03 \x01(\t\x1a,\n\x05\x42rain\x12\x11\n\tmodelJson\x18\x01 \x01(\t\x12\x10\n\x08modelUrl\x18\x02 \x01(\tb\x06proto3')
)




_PERSONA_AGE = _descriptor.Descriptor(
  name='Age',
  full_name='persona.Persona.Age',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='old', full_name='persona.Persona.Age.old', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='knowledgeCycle', full_name='persona.Persona.Age.knowledgeCycle', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='environments', full_name='persona.Persona.Age.environments', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=183,
  serialized_end=247,
)

_PERSONA_BRAIN = _descriptor.Descriptor(
  name='Brain',
  full_name='persona.Persona.Brain',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='modelJson', full_name='persona.Persona.Brain.modelJson', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='modelUrl', full_name='persona.Persona.Brain.modelUrl', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=293,
)

_PERSONA = _descriptor.Descriptor(
  name='Persona',
  full_name='persona.Persona',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='persona.Persona.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dna', full_name='persona.Persona.dna', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='softPhysical', full_name='persona.Persona.softPhysical', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hardPhysical', full_name='persona.Persona.hardPhysical', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='age', full_name='persona.Persona.age', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='brain', full_name='persona.Persona.brain', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PERSONA_AGE, _PERSONA_BRAIN, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=293,
)

_PERSONA_AGE.containing_type = _PERSONA
_PERSONA_BRAIN.containing_type = _PERSONA
_PERSONA.fields_by_name['age'].message_type = _PERSONA_AGE
_PERSONA.fields_by_name['brain'].message_type = _PERSONA_BRAIN
DESCRIPTOR.message_types_by_name['Persona'] = _PERSONA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Persona = _reflection.GeneratedProtocolMessageType('Persona', (_message.Message,), dict(

  Age = _reflection.GeneratedProtocolMessageType('Age', (_message.Message,), dict(
    DESCRIPTOR = _PERSONA_AGE,
    __module__ = 'persona_pb2'
    # @@protoc_insertion_point(class_scope:persona.Persona.Age)
    ))
  ,

  Brain = _reflection.GeneratedProtocolMessageType('Brain', (_message.Message,), dict(
    DESCRIPTOR = _PERSONA_BRAIN,
    __module__ = 'persona_pb2'
    # @@protoc_insertion_point(class_scope:persona.Persona.Brain)
    ))
  ,
  DESCRIPTOR = _PERSONA,
  __module__ = 'persona_pb2'
  # @@protoc_insertion_point(class_scope:persona.Persona)
  ))
_sym_db.RegisterMessage(Persona)
_sym_db.RegisterMessage(Persona.Age)
_sym_db.RegisterMessage(Persona.Brain)


# @@protoc_insertion_point(module_scope)
