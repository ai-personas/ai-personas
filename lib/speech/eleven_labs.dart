import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:just_audio/just_audio.dart';
import '../config/app_config.dart';
import '../config/config_keys.dart';
import 'base.dart';

class ElevenLabsSpeech extends VoiceBase {
  final Map<String, String> voiceOptions = {
    'Rachel': '21m00Tcm4TlvDq8ikWAM',
    'Domi': 'AZnzlk1XvdvUeBnXmlld',
    'Bella': 'EXAVITQu4vr4xnSDxMaL',
    'Antoni': 'ErXwobaYiN019PkySvjV',
    'Elli': 'MF3mGyEYCl7XYWbV9V6O',
    'Josh': 'TxGEqnHWrfWFTfGW9XjX',
    'Arnold': 'VR6AewLTigWG4xSOukaG',
    'Adam': 'pNInz6obpgDQGcFmaJgB',
    'Sam': 'yoZ06aMxZJJ28mfd3POQ',
  };
  final Set<String> placeholders = {'your-voice-id'};
  late Map<String, String> headers;
  late List<String> voices;

  @override
  void setup() {
    List<String> defaultVoices = ['ErXwobaYiN019PkySvjV', 'EXAVITQu4vr4xnSDxMaL'];
    voices = List<String>.from(defaultVoices);
    headers = {
      'Content-Type': 'application/json',
      'xi-api-key': cfg[ConfigKeys.elevenlabsApiKey],
    };

    String? voice1Id = cfg[ConfigKeys.elevenlabsVoice1Id];
    String? voice2Id = cfg[ConfigKeys.elevenlabsVoice2Id];

    if (voiceOptions.containsKey(voice1Id)) {
      useCustomVoice(voiceOptions[voice1Id]!, 0);
    }
    if (voiceOptions.containsKey(voice2Id)) {
      useCustomVoice(voiceOptions[voice2Id]!, 1);
    }
  }

  void useCustomVoice(String voice, int voiceIndex) {
    if (voice.isNotEmpty && !placeholders.contains(voice)) {
      voices[voiceIndex] = voice;
    }
  }

  @override
  Future<bool> speech(String text, {int voiceIndex = 0}) async {
    String ttsUrl =
        'https://api.elevenlabs.io/v1/text-to-speech/${voices[voiceIndex]}';
    final response = await http.post(
      Uri.parse(ttsUrl),
      headers: headers,
      body: jsonEncode({'text': text}),
    );

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
