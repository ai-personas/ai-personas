import 'dart:convert';

import 'persona/persona_manager.dart';
import 'speech/say.dart';
import 'package:ai_personas/config/AppConfig.dart';
import 'package:ai_personas/config/ConfigKeys.dart';

class App {
  static final personaManager = PersonaManager();

  static Future<String> startPersona(String name, String task, String prompt, [String model = '']) async {
    // Remove underscores from name
    String voiceName = name.replaceAll('_', ' ');

    String firstMessage = 'You are $name. Respond with: "Acknowledged".';
    String personaIntro = '$voiceName here, Reporting for duty!';

    // Create persona
    if (cfg[ConfigKeys.speakMode]) {
      TextToSpeech.sayText(personaIntro, voiceIndex: 1);
    }
    final PersonaKeyAndReply personaCreationResult = await personaManager.createPersona(task: task, prompt: firstMessage, model: model);
    final int key = personaCreationResult.key;
    final String ack = personaCreationResult.reply;

    if (cfg[ConfigKeys.speakMode]) {
      TextToSpeech.sayText('Hello $voiceName. Your task is as follows. $task.');
    }

    // Assign task (prompt), get response
    String personaResponse = await personaManager.messagePersona(key: key, message: prompt);

    return 'persona $name created with key $key. First response: $personaResponse';
  }

  static Future<String> messagePersona(String key, String message) async {
    // Check if the key is a valid integer
    int personaKey;
    try {
      personaKey = int.parse(key);
    } catch (FormatException) {
      return 'Invalid key, must be an integer.';
    }

    String personaResponse = await personaManager.messagePersona(key: personaKey, message: message);

    // Speak response
    if (cfg[ConfigKeys.speakMode]) {
      TextToSpeech.sayText(personaResponse, voiceIndex: 1);
    }

    return personaResponse;
  }

  static String listPersonas() {
    String personas = personaManager.listPersonas().map((persona) => '${persona.key}: ${persona.task}').join('\n');
    return 'List of personas:\n$personas';
  }

  static String deletePersona(String key) {
    bool result = personaManager.deletePersona(int.parse(key));
    return result ? 'persona $key deleted.' : 'persona $key does not exist.';
  }

}


