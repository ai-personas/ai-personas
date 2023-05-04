String balanceBrackets(String inputText) {
  int openBraces = 0;
  int openBrackets = 0;
  String balancedText = '';

  for (int i = 0; i < inputText.length; i++) {
    String currentChar = inputText[i];

    if (currentChar == '{') {
      openBraces++;
    } else if (currentChar == '}') {
      if (openBraces > 0) {
        openBraces--;
      } else {
        continue;
      }
    } else if (currentChar == '[') {
      openBrackets++;
    } else if (currentChar == ']') {
      if (openBrackets > 0) {
        openBrackets--;
      } else {
        continue;
      }
    }

    balancedText += currentChar;
  }

  while (openBraces > 0) {
    balancedText += '}';
    openBraces--;
  }

  while (openBrackets > 0) {
    balancedText += ']';
    openBrackets--;
  }

  return balancedText;
}

String extractJson(String inputText) {
  String jsonText = '';
  RegExp jsonPattern = RegExp(r'\{[\s\S]*\}');
  Match? jsonMatch = jsonPattern.firstMatch(inputText);

  jsonText = jsonMatch!.group(0)!;
  jsonText = balanceBrackets(jsonText);
  return jsonText;
}
