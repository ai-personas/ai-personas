# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scientists.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='scientists.proto',
  package='portraits',
  syntax='proto3',
  serialized_pb=_b('\n\x10scientists.proto\x12\tportraits\"\xcc\x01\n\x0bInformation\x12\x11\n\textractor\x18\x01 \x01(\t\x12=\n\x10trainingDataList\x18\x02 \x03(\x0b\x32#.portraits.Information.TrainingData\x12\x35\n\x0ctestDataList\x18\x03 \x03(\x0b\x32\x1f.portraits.Information.TestData\x1a\x1b\n\x0cTrainingData\x12\x0b\n\x03URL\x18\x01 \x01(\t\x1a\x17\n\x08TestData\x12\x0b\n\x03URL\x18\x01 \x01(\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_INFORMATION_TRAININGDATA = _descriptor.Descriptor(
  name='TrainingData',
  full_name='portraits.Information.TrainingData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='URL', full_name='portraits.Information.TrainingData.URL', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=211,
)

_INFORMATION_TESTDATA = _descriptor.Descriptor(
  name='TestData',
  full_name='portraits.Information.TestData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='URL', full_name='portraits.Information.TestData.URL', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=213,
  serialized_end=236,
)

_INFORMATION = _descriptor.Descriptor(
  name='Information',
  full_name='portraits.Information',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='extractor', full_name='portraits.Information.extractor', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trainingDataList', full_name='portraits.Information.trainingDataList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='testDataList', full_name='portraits.Information.testDataList', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_INFORMATION_TRAININGDATA, _INFORMATION_TESTDATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=236,
)

_INFORMATION_TRAININGDATA.containing_type = _INFORMATION
_INFORMATION_TESTDATA.containing_type = _INFORMATION
_INFORMATION.fields_by_name['trainingDataList'].message_type = _INFORMATION_TRAININGDATA
_INFORMATION.fields_by_name['testDataList'].message_type = _INFORMATION_TESTDATA
DESCRIPTOR.message_types_by_name['Information'] = _INFORMATION

Information = _reflection.GeneratedProtocolMessageType('Information', (_message.Message,), dict(

  TrainingData = _reflection.GeneratedProtocolMessageType('TrainingData', (_message.Message,), dict(
    DESCRIPTOR = _INFORMATION_TRAININGDATA,
    __module__ = 'scientists_pb2'
    # @@protoc_insertion_point(class_scope:portraits.Information.TrainingData)
    ))
  ,

  TestData = _reflection.GeneratedProtocolMessageType('TestData', (_message.Message,), dict(
    DESCRIPTOR = _INFORMATION_TESTDATA,
    __module__ = 'scientists_pb2'
    # @@protoc_insertion_point(class_scope:portraits.Information.TestData)
    ))
  ,
  DESCRIPTOR = _INFORMATION,
  __module__ = 'scientists_pb2'
  # @@protoc_insertion_point(class_scope:portraits.Information)
  ))
_sym_db.RegisterMessage(Information)
_sym_db.RegisterMessage(Information.TrainingData)
_sym_db.RegisterMessage(Information.TestData)


# @@protoc_insertion_point(module_scope)