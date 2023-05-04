// persona_config_storage.dart

import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class Persona {
  String version;
  String name;
  String role;
  List<String> goals;
  List<Map<String, dynamic>> fullMessageHistory;

  Persona({
    this.version = '0.1.1',
    this.name = '',
    this.role = '',
    List<String>? aiGoals,
    List<Map<String, dynamic>>? fullMessageHistory,
  })  : goals = aiGoals ?? [],
        fullMessageHistory = fullMessageHistory ?? [];

  static Future<Persona> get getPersona async {
    final prefs = await SharedPreferences.getInstance();
    // String key = '${prefs.getString('name')}_${prefs.getString('version')}';
    final jsonString = prefs.getString('persona') ?? '{}';
    final personaJson = json.decode(jsonString);

    return Persona(
        name: personaJson['name'] ?? '',
        role: personaJson['role'] ?? '',
        aiGoals: List<String>.from(personaJson['goals'] ?? []),
        fullMessageHistory: List<Map<String, dynamic>>.from(
            personaJson['fullMessageHistory'] ?? []));
  }

  Future<void> save() async {
    final config = {
      'version': version,
      'name': name,
      'role': role,
      'goals': goals,
      'fullMessageHistory': fullMessageHistory,
    };
    final jsonString = jsonEncode(config);
    final prefs = await SharedPreferences.getInstance();
    // String key = '${name}_$version';
    prefs.setString('persona', jsonString);
  }

  // Method to add a new message to fullMessageHistory
  void addMessageToHistory(Map<String, dynamic> message) {
    fullMessageHistory.add(message);
  }
}
