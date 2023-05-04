import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:universal_html/html.dart' as html;
import 'storage.dart';

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
