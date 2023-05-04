import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:universal_html/html.dart' as html;
import 'storage.dart';
import 'dart:async';

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

