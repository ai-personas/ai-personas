import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';
import 'package:path_provider/path_provider.dart';
import 'package:image/image.dart';

class Config {
  String huggingfaceApiToken;
  String openaiApiKey;
  String imageProvider;

  Config({
    required this.huggingfaceApiToken,
    required this.openaiApiKey,
    required this.imageProvider,
  });
}

final CFG = Config(
  huggingfaceApiToken: 'your_huggingface_api_token',
  openaiApiKey: 'your_openai_api_key',
  imageProvider: 'dalle',
);

Future<String> generateImage(String prompt) async {
  String filename = '${Uuid().v4()}.jpg';

  if (CFG.imageProvider == 'dalle') {
    return await generateImageWithDalle(prompt, filename);
  } else if (CFG.imageProvider == 'sd') {
    return await generateImageWithHf(prompt, filename);
  } else {
    return 'No Image Provider Set';
  }
}

Future<String> generateImageWithHf(String prompt, String filename) async {
  const String apiUrl =
      'https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4';

  if (CFG.huggingfaceApiToken == null) {
    throw Exception(
        'You need to set your Hugging Face API token in the config file.');
  }

  var headers = {
    'Authorization': 'Bearer ${CFG.huggingfaceApiToken}',
  };

  var response = await http.post(
    Uri.parse(apiUrl),
    headers: headers,
    body: jsonEncode({'inputs': prompt}),
  );

  Image image = Image.fromBytes(width: 256, height: 256, bytes: response.bodyBytes.buffer);
  print('Image Generated for prompt: $prompt');

  Directory appDocDir = await getApplicationDocumentsDirectory();
  File file = File('${appDocDir.path}/$filename');
  file.writeAsBytesSync(encodeJpg(image));

  return 'Saved to disk: $filename';
}

Future<String> generateImageWithDalle(String prompt, String filename) async {
  String openaiApiKey = CFG.openaiApiKey;

  if (openaiApiKey.isEmpty) {
    throw ArgumentError("You need to set your OpenAI API key.");
  }
  Map<String, String> headers = {
    "Authorization": "Bearer $openaiApiKey",
    "Content-Type": "application/json",
  };

  http.Response response = await http.post(
    Uri.parse("https://api.openai.com/v1/images/generations"),
    headers: headers,
    body: jsonEncode({
      "model": "image-alpha-001",
      "prompt": prompt,
      "n": 1,
      "size": "256x256",
      "response_format": "url",
    }),
  );

  Map<String, dynamic> responseData = jsonDecode(response.body);
  print("Image Generated for prompt: $prompt");

  String imageUrl = responseData['data'][0]['url'];
  http.Response imageResponse = await http.get(Uri.parse(imageUrl));

  // Get a suitable directory for saving the image
  Directory appDocDir = await getApplicationDocumentsDirectory();
  String imagePath = appDocDir.path + '/' + filename;

  // Save the image to disk
  File imageFile = File(imagePath);
  await imageFile.writeAsBytes(imageResponse.bodyBytes);

  return "Saved to disk: $filename";
}
