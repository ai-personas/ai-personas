import 'dart:convert';
import 'package:ai_personas/memory/memory.dart';
import 'package:ai_personas/memory/memory_base.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/services.dart';

class Persona {
  static String currentPersona = '';

  static String version = '0.1.2';
  String name;
  List<Map<String, dynamic>> environment;
  List<Map<String, dynamic>> fullMessageHistory;
  MemoryBase? memory;
  String context;
  DateTime createdAt;

  bool _isLoaded = false;

  static final Persona _singleton = Persona._internal();

  factory Persona() {
    return _singleton;
  }

  Persona._internal(
      { name,
        List<Map<String, dynamic>>? environment,
        List<Map<String, dynamic>>? fullMessageHistory,
        this.memory,
        context,
        DateTime? createdAt})
      : name = name ?? '',
        environment = environment ?? [],
        fullMessageHistory = fullMessageHistory ?? [],
        context = context ?? '',
        createdAt = createdAt ?? DateTime.now();

  static Future<Persona> get getCurrentPersona async {
    if (!_singleton._isLoaded) {
      final prefs = await SharedPreferences.getInstance();
      String key = 'aipersonas_${currentPersona}_${version}';
      final jsonString = prefs.getString(key) ?? '{}';

      if (jsonString != '{}') {
        await _singleton.loadPersona(json.decode(jsonString));
      } else {
        throw Exception('Not found persona named: ${currentPersona}');
      }
      _singleton._isLoaded = true;
    }

    return _singleton;
  }

  static Future<List<Map<String, Map<String, String>>>> getAllPersonas() async {
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();
    List<Map<String, Map<String, String>>> personas = [];

    for (var key in keys) {
      if (key.startsWith('aipersonas_')) {
        final parts = key.split('_');
        if (parts.length == 3) { // Ensure the key can be split into exactly 3 parts
          personas.add({
            'persona': {
              'value': parts[1],
            },
            'version': {
              'value': parts[2],
            },
            'action': {
              'button': 'Select',
              'download': 'true',
              'delete': 'true',
            },
          });
        } else {
          print("Invalid key format found in SharedPreferences: $key");
        }
      } else if (key == 'persona') {
        // Handle old key format
        final jsonString = prefs.getString('persona') ?? '{}';
        final personaJson = json.decode(jsonString);
        personas.add({
          'persona': {
            'value': personaJson['name'],
          },
          'version': {
            'value': '0.1.1', // Since old version doesn't store version
          },
          'action': {
            'download': 'true',
            'delete': 'true',
          },
        });
      }
    }

    return personas;
  }

  static Future<Persona> getPersona(String personaName) async {
      //save existing persona
      if (_singleton._isLoaded) {
        _singleton.save();
      }
      final prefs = await SharedPreferences.getInstance();
      String key = 'aipersonas_${personaName}_${version}';
      final jsonString = prefs.getString(key) ?? '';

      if (jsonString != '') {
        await _singleton.loadPersona(json.decode(jsonString));
        currentPersona = personaName;
      } else {
        throw Exception('Not found persona named: ${personaName}');
      }
      _singleton._isLoaded = true;
    return _singleton;
  }

  static Future<Persona> createPersona(String personaName, String initialContext) async {
    if (currentPersona != '') {
      //save current persona
      _singleton.save();
    }
    _singleton.name = personaName;
    _singleton.memory = await createMemory(personaName: personaName);
    _singleton.context = initialContext;
    _singleton.fullMessageHistory = [];
    _singleton.createdAt = DateTime.now();
    currentPersona = personaName;
    await _singleton.save();
    return _singleton;
  }

  Future<void> loadPersona(Map<String, dynamic> personaJson) async {
    version = personaJson['version'];
    name = personaJson['name'];
    memory = await loadMemory(jsonStr: personaJson['memory']);
    fullMessageHistory = List<Map<String, dynamic>>.from(
        personaJson['fullMessageHistory'] ?? []);
    context = personaJson['context'];
  }

  Future<void> save() async {
    final persona = {
      'version': version,
      'name': name,
      'environment': environment,
      'fullMessageHistory': fullMessageHistory,
      'memory': memory!.toJsonString(),
      'context': context
    };
    final jsonString = jsonEncode(persona);
    final prefs = await SharedPreferences.getInstance();
    String key = 'aipersonas_${name}_${version}';
    prefs.setString(key, jsonString);
  }

  static Future<void> deletePersona(String personaName, String version) async {
    final prefs = await SharedPreferences.getInstance();
    String key = 'aipersonas_${personaName}_${version}';
    if (prefs.containsKey(key)) {
      prefs.remove(key);
    } else {
      throw Exception('No persona found with name: ${personaName} and version: ${version}');
    }
  }

  // Method to add a new message to fullMessageHistory
  void addMessageToHistory(Map<String, dynamic> message) {
    fullMessageHistory.add(message);
  }

  static Future<String> getContext() async {
    String contextFilePath = 'assets/autogpt_context_template.txt';
    String context = await rootBundle.loadString(contextFilePath);
    return context;
  }

  Future<void> addDataToMemory(String data) async {
    memory?.add(data);
    await save();
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'name': name,
      'environment': environment,
      'fullMessageHistory': fullMessageHistory,
      'memory': memory?.toJsonString(),
      'context': context,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  String getJson() {
    return jsonEncode(toJson());
  }
}
