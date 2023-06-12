import 'package:ai_personas/memory/pinecone_memory.dart';

import '../config/app_config.dart';
import '../config/config_keys.dart';
import 'local_memory.dart';
import 'memory_base.dart';

final List<String> supportedMemory = ["local", "pinecone", "no_memory"];

Future<MemoryBase> createMemory({String personaName = ''}) async {
  String memoryBackend = cfg[ConfigKeys.memoryBackend];
  if (!supportedMemory.contains(memoryBackend)) {
    throw Exception('Unsupported memory backend: $memoryBackend');
  }

  switch (memoryBackend) {
    case "local":
      return await LocalCache.create(personaName);
    case "pinecone":
      return await PineconeMemory.create(
          cfg[ConfigKeys.pineconeEnvironment],
          personaName);
    default:
      throw Exception('Unsupported memory backend: $memoryBackend');
  }
}

Future<MemoryBase> loadMemory({String jsonStr = ''}) async {
  String memoryBackend = cfg[ConfigKeys.memoryBackend];
  if (!supportedMemory.contains(memoryBackend)) {
    throw Exception('Unsupported memory backend: $memoryBackend');
  }

  switch (memoryBackend) {
    case "local":
      return await LocalCache.load(jsonStr);
    case "pinecone":
      return await PineconeMemory.load(jsonStr);
    default:
      throw Exception('Unsupported memory backend: $memoryBackend');
  }
}

