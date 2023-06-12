import 'dart:async';

abstract class MemoryBase {
  Future<String> add(String data);

  Future<List<String>?> get(String data);

  Future<String> clear();

  Future<List<String>> getRelevant(String data, {int numRelevant = 5});

  Future<Map<String, dynamic>> getStats();

  String toJsonString();
}
