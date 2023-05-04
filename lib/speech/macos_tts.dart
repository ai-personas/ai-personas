import 'dart:io';
import 'base.dart';

class MacOSTTS extends VoiceBase {
  @override
  void setup() {}

  @override
  Future<bool> speech(String text, {int voiceIndex = 0}) async {
    try {
      if (voiceIndex == 0) {
        await Process.run('say', [text]);
      } else if (voiceIndex == 1) {
        await Process.run('say', ['-v', 'Ava (Premium)', text]);
      } else {
        await Process.run('say', ['-v', 'Samantha', text]);
      }
      return true;
    } catch (e) {
      print('Error: $e');
      return false;
    }
  }
}
