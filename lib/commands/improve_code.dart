import 'dart:convert';
import '../llm_utils.dart';

Future<String> improveCode(List<String> suggestions, String code) async {
  String functionString =
      "def generate_improved_code(suggestions: List[str], code: str) -> str:";
  List<String> args = [jsonEncode(suggestions), code];
  String descriptionString =
      "Improves the provided code based on the suggestions"
      " provided, making no other changes.";

  return await callAiFunction(functionString, args, descriptionString);
}
