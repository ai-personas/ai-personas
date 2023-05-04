import 'package:flutter_tts/flutter_tts.dart';
import 'base.dart';

class GTTSVoice extends VoiceBase {
  final FlutterTts _flutterTts = FlutterTts();

  @override
  void setup() {
    // No setup needed for the FlutterTts package
  }

  @override
  Future<bool> speech(String text, {int voiceIndex = 0}) async {
    // The voiceIndex parameter is not used in this implementation
    // You can implement voice selection using the methods provided by the FlutterTts package if needed
    await _flutterTts.speak(text);
    return true;
  }
}
