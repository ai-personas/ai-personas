import 'dart:async';
import 'dart:io';

abstract class VoiceBase {
  Uri? _url;
  Map<String, String>? _headers;
  String? _apiKey;
  List<dynamic> _voices = [];
  final _mutex = Mutex();

  VoiceBase() {
    setup();
  }

  Future<bool> say(String text, {int voiceIndex = 0}) async {
    return await _mutex.synchronized(() async {
      return await speech(text, voiceIndex: voiceIndex);
    });
  }

  void setup();

  Future<bool> speech(String text, {int voiceIndex});
}

class Mutex {
  final _lock = Lock();

  Future<T> synchronized<T>(Future<T> Function() func) async {
    await _lock.acquire();
    try {
      return await func();
    } finally {
      _lock.release();
    }
  }
}

class Lock {
  bool _locked = false;

  Future<void> acquire() async {
    while (_locked) {
      await Future.delayed(Duration(milliseconds: 10));
    }
    _locked = true;
  }

  void release() {
    _locked = false;
  }
}
