import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:just_audio/just_audio.dart';
import 'base.dart';

class BrianSpeech extends VoiceBase {
  @override
  void setup() {}

  @override
  Future<bool> speech(String text, {int voiceIndex = 0}) async {
    String ttsUrl =
        'https://api.streamelements.com/kappa/v2/speech?voice=Brian&text=$text';
    final response = await http.get(Uri.parse(ttsUrl));

    if (response.statusCode == 200) {
      final audioPlayer = AudioPlayer();
      await audioPlayer.setUrl(ttsUrl);
      await audioPlayer.play();
      await audioPlayer.dispose();
      return true;
    } else {
      print('Request failed with status code: ${response.statusCode}');
      print('Response content: ${response.body}');
      return false;
    }
  }
}
