import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:universal_html/html.dart' as html;

// Export the appropriate storage implementation based on the platform
export 'web_storage.dart' if (dart.library.html) 'mobile_storage.dart';

abstract class Storage {
  Future<void> save(String key, String value);
  Future<String?> load(String key);
  Future<void> clear(String key);
}

class MobileStorage implements Storage {
  @override
  Future<void> save(String key, String value) async {
    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/$key');
    await file.writeAsString(value);
  }

  @override
  Future<String?> load(String key) async {
    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/$key');
    if (await file.exists()) {
      return await file.readAsString();
    }
    return null;
  }

  @override
  Future<void> clear(String key) async {
    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/$key');
    if (await file.exists()) {
      await file.delete();
    }
  }
}

class WebStorage implements Storage {
  @override
  Future<void> save(String key, String value) async {
    html.window.localStorage[key] = value;
  }

  @override
  Future<String?> load(String key) async {
    return html.window.localStorage[key];
  }

  @override
  Future<void> clear(String key) async {
    html.window.localStorage.remove(key);
  }
}
