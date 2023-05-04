import '../config/AppConfig.dart';
import '../config/ConfigKeys.dart';
import 'local_memory.dart';
import 'memory_base.dart';

final List<String> supportedMemory = ["local", "no_memory"];

// Declare a global variable to store the memory instance
MemoryBase? _memoryInstance;

Future<MemoryBase> getMemory({bool init = false}) async {
  // If the memory instance exists and init is false, return the existing instance
  if (_memoryInstance != null && !init) {
    return _memoryInstance!;
  }

  // If init is true, create a new memory instance based on the memory backend
  switch (cfg[ConfigKeys.memoryBackend]) {
    default:
      _memoryInstance = await LocalCache.create(cfg[ConfigKeys.memoryIndex]);
      if (init) {
        _memoryInstance!.clear();
      }
  }

  return _memoryInstance!;
}

List<String> getSupportedMemoryBackends() {
  return supportedMemory;
}
