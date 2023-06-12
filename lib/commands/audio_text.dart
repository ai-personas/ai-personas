import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';
import '../config/config_keys.dart';
import '../workspace.dart';

Future<String> readAudioFromFile(String audioPath) async {
  final filePath = WorkspaceUtils.pathInWorkspace(audioPath);
  final file = File(filePath);
  final audio = await file.readAsBytes();
  return readAudio(audio);
}

Future<String> readAudio(List<int> audio) async {
  final model = cfg[ConfigKeys.huggingfaceAudioToTextModel];
  final apiUrl = "https://api-inference.huggingface.co/models/$model";
  final apiToken = cfg[ConfigKeys.huggingfaceApiToken];
  final headers = {"Authorization": "Bearer $apiToken"};

  if (apiToken == null) {
    throw Exception("You need to set your Hugging Face API token in the config file.");
  }

  final response = await http.post(
    Uri.parse(apiUrl),
    headers: headers,
    body: audio,
  );

  final text = jsonDecode(response.body)["text"];
  return "The audio says: $text";
}
