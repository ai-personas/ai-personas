import '../llm_utils.dart';


Future<String> evaluateCode(String code) async {
  const functionString = "def analyze_code(code: str) -> List[str]:";
  final args = [code];
  const descriptionString = "Analyzes the given code and returns a list of suggestions for improvements.";

  return await callAiFunction(functionString, args, descriptionString);
}
