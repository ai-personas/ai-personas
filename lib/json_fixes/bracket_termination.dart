import 'dart:convert';
import '../config/AppConfig.dart';
import '../config/ConfigKeys.dart';
import '../speech/say.dart';
import 'json_fixer.dart';

String fixJsonString(String text) {
  List<String> jsonDataStrings = [];
  int braceCount = 0;
  int startIndex = 0;
  for (int i = 0; i < text.length; i++) {
    if (text[i] == '{') {
      if (braceCount == 0) {
        startIndex = i;
      }
      braceCount++;
    } else if (text[i] == '}') {
      braceCount--;
      if (braceCount == 0) {
        jsonDataStrings.add(text.substring(startIndex, i + 1));
      }
    }
  }
  return jsonDataStrings[0] ?? '';
}

String? extractJsonCommand(String jsonString) {
  String fixedJsonString;

  try {
    json.decode(jsonString);
    fixedJsonString = jsonString;
  } on Exception {
    try {
      fixedJsonString = extractJson(jsonString);
      json.decode(fixedJsonString);
    } on Exception {
      print('The input string could not be fixed or parsed as JSON.');
      return null;
    }
  }

  Map<String, dynamic> jsonData = json.decode(fixedJsonString);

  if (jsonData.containsKey('command')) {
    return json.encode(jsonData['command']);
  } else {
    print('The JSON object does not contain a "command" key.');
    return null;
  }
}

String attemptToFixJsonByFindingOutermostBrackets(String jsonString) {
  if (cfg[ConfigKeys.speakMode] && cfg[ConfigKeys.debugMode]) {
    TextToSpeech.sayText(
        "I have received an invalid JSON response from the OpenAI API. Trying to fix it now.");
  }
  print("Attempting to fix JSON by finding outermost brackets\n");

  try {
    final RegExp jsonPattern = RegExp(r"\{(?:[^{}]|(?R))*\}");
    final Match? jsonMatch = jsonPattern.firstMatch(jsonString);

    if (jsonMatch != null) {
      jsonString = jsonMatch.group(0)!;
      print('Apparently json was fixed.');
      if (cfg[ConfigKeys.speakMode] && cfg[ConfigKeys.debugMode]) {
        TextToSpeech.sayText("Apparently json was fixed.");
      }
    } else {
      throw FormatException("No valid JSON object found");
    }
  } on FormatException {
    print("Error: Invalid JSON: $jsonString\n");
    if (cfg[ConfigKeys.speakMode]) {
      TextToSpeech.sayText("Didn't work. I will have to ignore this response then.");
    }
    print("Error: Invalid JSON, setting it to empty JSON now.\n");
    jsonString = '{}';
  }

  return jsonString;
}

String? balanceBraces(String jsonString) {
  int openBracesCount = jsonString.split('{').length - 1;
  int closeBracesCount = jsonString.split('}').length - 1;

  while (openBracesCount > closeBracesCount) {
    jsonString += '}';
    closeBracesCount += 1;
  }

  while (closeBracesCount > openBracesCount) {
    jsonString = jsonString.substring(0, jsonString.length - 1);
    closeBracesCount -= 1;
  }

  try {
    jsonDecode(jsonString);
    return jsonString;
  } on FormatException {
    return null;
  }
}
