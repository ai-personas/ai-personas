import 'dart:async';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';

// Make sure to import your speech classes here
import 'brian.dart';
import 'macos_tts.dart';
import 'gtts.dart';
import 'eleven_labs.dart';
import '../config/AppConfig.dart';
import '../config/ConfigKeys.dart';
import 'base.dart'; // Import base.dart to use Mutex from base.dart

class TextToSpeech {
  dynamic defaultVoiceEngine = GTTSVoice();
  dynamic voiceEngine;

  static final TextToSpeech _instance = TextToSpeech._();

  factory TextToSpeech() {
    return _instance;
  }

  TextToSpeech._() {
    if (cfg[ConfigKeys.elevenlabsApiKey].isNotEmpty) {
      voiceEngine = ElevenLabsSpeech();
    } else if (cfg[ConfigKeys.useMacOsTts] == 'True') {
      voiceEngine = MacOSTTS();
    } else if (cfg[ConfigKeys.useBrianTts] == 'True') {
      voiceEngine = BrianSpeech();
    } else {
      voiceEngine = GTTSVoice();
    }
  }

  final Mutex _mutex = Mutex(); // Using Mutex from base.dart

  static Future<void> sayText(String text, {int voiceIndex = 0}) async {
    return _instance._mutex.synchronized(() async {
      bool success = await _instance.voiceEngine.say(text, voiceIndex);
      if (!success) {
        await _instance.defaultVoiceEngine.say(text);
      }
    });
  }
}
