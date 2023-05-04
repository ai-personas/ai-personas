import 'dart:convert';

import '/llm_utils.dart';
import 'package:openai_client/src/model/openai_chat/chat_message.dart';

class PersonaManager {
  PersonaManager._privateConstructor();

  static final PersonaManager _instance = PersonaManager._privateConstructor();

  factory PersonaManager() {
    return _instance;
  }

  int _nextKey = 0;
  final Map<int, PersonaTuple> _personas = {};

  Future<PersonaKeyAndReply> createPersona(
      {required String task, required String prompt, required String model}) async {
    final messages = [
      {'role': 'user', 'content': prompt},
    ];

    List<ChatMessage> chatMessages = messages.map((message) => ChatMessage.fromJson(json.encode(message))).toList();
    final personaReply = await createChatCompletion(model: model, messages: chatMessages);
    messages.add({'role': 'assistant', 'content': personaReply});

    final key = _nextKey;
    _nextKey += 1;
    _personas[key] = PersonaTuple(task, messages, model);

    return PersonaKeyAndReply(key, personaReply);
  }

  Future<String> messagePersona({required dynamic key, required String message}) async {
    final PersonaTuple tuple = _personas[int.parse(key.toString())]!;
    final task = tuple.task;
    final messages = tuple.messages;
    final model = tuple.model;

    messages.add({'role': 'user', 'content': message});

    List<ChatMessage> chatMessages = messages.map((message) => ChatMessage.fromJson(json.encode(message))).toList();
    final personaReply = await createChatCompletion(model: model, messages: chatMessages);
    messages.add({'role': 'assistant', 'content': personaReply});

    return personaReply;
  }

  List<PersonaKeyAndTask> listPersonas() {
    return _personas.entries.map((entry) => PersonaKeyAndTask(entry.key, entry.value.task)).toList();
  }

  bool deletePersona(dynamic key) {
    try {
      _personas.remove(int.parse(key.toString()));
      return true;
    } catch (e) {
      return false;
    }
  }
}

class PersonaTuple {
  final String task;
  final List<Map<String, String>> messages;
  final String model;

  PersonaTuple(this.task, this.messages, this.model);
}

class PersonaKeyAndReply {
  final int key;
  final String reply;

  PersonaKeyAndReply(this.key, this.reply);
}

class PersonaKeyAndTask {
  final int key;
  final String task;

  PersonaKeyAndTask(this.key, this.task);
}
