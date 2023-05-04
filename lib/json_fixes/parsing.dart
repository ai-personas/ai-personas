import 'dart:convert';
import '../json_fixes/auto_fix.dart';

class JsonFixer {
  static const String JSON_SCHEMA = '''
{
    "command": {
        "name": "command name",
        "args": {
            "arg name": "value"
        }
    },
    "thoughts": {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\\n- list that conveys\\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    }
}
''';

  static String correctJson(String jsonToLoad, {bool debugMode = false}) {
    try {
      if (debugMode) {
        print("json: $jsonToLoad");
      }
      jsonDecode(jsonToLoad);
      return jsonToLoad;
    } catch (e) {
      if (debugMode) {
        print("json loads error: $e");
      }
      // Note: fix_invalid_escape, add_quotes_to_property_names,
      // and balance_braces functions are not implemented here.
      return jsonToLoad;
    }
  }

  static dynamic fixAndParseJson(String jsonToLoad, {bool tryToFixWithGpt = true, bool debugMode = false}) {
    try {
      jsonToLoad = jsonToLoad.replaceAll('\t', '');
      return jsonDecode(jsonToLoad);
    } catch (e) {
      // Do nothing
    }

    try {
      jsonToLoad = correctJson(jsonToLoad, debugMode: debugMode);
      return jsonDecode(jsonToLoad);
    } catch (e) {
      // Do nothing
    }

    try {
      int braceIndex = jsonToLoad.indexOf('{');
      String maybeFixedJson = jsonToLoad.substring(braceIndex);
      int lastBraceIndex = maybeFixedJson.lastIndexOf('}');
      maybeFixedJson = maybeFixedJson.substring(0, lastBraceIndex + 1);
      return jsonDecode(maybeFixedJson);
    } catch (e) {
      return tryAiFix(tryToFixWithGpt, e, jsonToLoad);
    }
  }

  static dynamic tryAiFix(bool tryToFixWithGpt, Object exception, String jsonToLoad) {
    if (!tryToFixWithGpt) {
      throw exception;
    }

    print(
        "Warning: Failed to parse AI output, attempting to fix.\nIf you see this warning frequently, it's likely that your prompt is confusing the AI. Try changing it up slightly.");

    // Note: JSON_SCHEMA is not defined here. You need to
    // define JSON_SCHEMA before using it.
    String aiFixedJson = JsonFixerWithSchema.fixJson(jsonToLoad, JSON_SCHEMA);

    if (aiFixedJson != "failed") {
      return jsonDecode(aiFixedJson);
    }

    // This allows the AI to react to the error message,
    // which usually results in it correcting its ways.
    print("Failed to fix AI output, telling the AI.");
    return jsonToLoad;
  }
}
