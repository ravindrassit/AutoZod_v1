# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: autozad.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'autozad.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rautozad.proto\x12\x07\x61utozad\"#\n\x0bItemRequest\x12\x14\n\x0crequest_data\x18\x01 \x01(\t\"%\n\x0cItemResponse\x12\x15\n\rresponse_data\x18\x01 \x01(\t2I\n\x0f\x41utoZad_Service\x12\x36\n\x07GetItem\x12\x14.autozad.ItemRequest\x1a\x15.autozad.ItemResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'autozad_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ITEMREQUEST']._serialized_start=26
  _globals['_ITEMREQUEST']._serialized_end=61
  _globals['_ITEMRESPONSE']._serialized_start=63
  _globals['_ITEMRESPONSE']._serialized_end=100
  _globals['_AUTOZAD_SERVICE']._serialized_start=102
  _globals['_AUTOZAD_SERVICE']._serialized_end=175
# @@protoc_insertion_point(module_scope)