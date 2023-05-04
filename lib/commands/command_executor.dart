import 'dart:convert';

import 'package:ai_personas/commands/web_browser.dart';
import 'package:ai_personas/config/ConfigKeys.dart';
import 'google_search.dart';
import 'package:ai_personas/config/AppConfig.dart';

class CommandExecutor {

  bool isValidInt(String value) {
    try {
      int.parse(value);
      return true;
    } catch (e) {
      return false;
    }
  }

  static dynamic getCommand(String? commandStr) {
    if (commandStr == null) {
      return ['Error:', "Missing 'command' object in JSON"];
    }

    try {
      final commandJson = jsonDecode(commandStr);

      if (commandJson is! Map) {
        return ['Error:', "'response_json' object is not dictionary $commandJson"];
      }

      if (commandJson['name'] == null) {
        return ['Error:', "Missing 'name' field in 'command' object"];
      }

      final commandName = commandJson['name'];
      final arguments = commandJson['args'] ?? {};

      return [commandName, arguments];
    } catch (e) {
      return ['Error:', 'Invalid JSON'];
    }
  }

  static String mapCommandSynonyms(String commandName) {
    final synonyms = {
      'write_file': 'write_to_file',
      'create_file': 'write_to_file',
      'search': 'google',
    };

    return synonyms[commandName] ?? commandName;
  }

  static Future<String?> executeCommand(String commandName, Map<String, dynamic> arguments) async {
    try {
      commandName = mapCommandSynonyms(commandName);

      switch (commandName) {
        case 'google':
          // if (cfg[ConfigKeys.googleApiKey]?.isNotEmpty ?? false) {
            return await searchGoogle(arguments["input"] as String);
          // } else {
          //   return await ddgSearch(arguments["input"] as String);
          // }
        case 'memory_add':
        // Implement the memory_add logic here
          break;
        case 'browse_website':
        // Implement the browse_website logic here
          return fetchWebsiteContent(arguments['url'], arguments['question']);
        case 'read_file':
        // Implement the read_file logic here
          break;
        case 'write_to_file':
        // Implement the write_to_file logic here
          break;
        case 'append_to_file':
        // Implement the append_to_file logic here
          break;
        case 'delete_file':
        // Implement the delete_file logic here
          break;
        case 'search_files':
        // Implement the search_files logic here
          break;
        case 'do_nothing':
          return "No action performed.";
        case 'task_complete':
        // Implement the shutdown logic here
          break;
        default:
          return "Unknown command '$commandName'. Please refer to the 'COMMANDS' list for available commands and only respond in the specified JSON format.";
      }
    } catch (e) {
      return 'Error: ${e.toString()}';
    }

    // Return a default message in case none of the commands were executed
    return null;
  }

  void shutdown() {
    print('Shutting down...');
  }

}


