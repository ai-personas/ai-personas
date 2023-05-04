import 'package:tiktoken/tiktoken.dart';

int countMessageTokens(List<Map<String, dynamic>> messages, {String modelName = 'gpt-3.5-turbo-0301'}) {
  Tiktoken encoding = encodingForModel(modelName);

  int tokensPerMessage;
  int tokensPerName;

  if (modelName == 'gpt-3.5-turbo') {
    return countMessageTokens(messages, modelName: 'gpt-3.5-turbo-0301');
  } else if (modelName == 'gpt-4') {
    return countMessageTokens(messages, modelName: 'gpt-4-0314');
  } else if (modelName == 'gpt-3.5-turbo-0301') {
    tokensPerMessage = 4;
    tokensPerName = -1;
  } else if (modelName == 'gpt-4-0314') {
    tokensPerMessage = 3;
    tokensPerName = 1;
  } else {
    throw Exception("numTokensFromMessages() is not implemented for model $modelName. "
        "See https://github.com/openai/openai-python/blob/main/chatml.md for "
        "information on how messages are converted to tokens.");
  }

  int numTokens = 0;
  for (Map<String, dynamic> message in messages) {
    numTokens += tokensPerMessage;
    message.forEach((key, value) {
      numTokens += encoding.encode(value).length;
      if (key == 'name') {
        numTokens += tokensPerName;
      }
    });
  }
  numTokens += 3; // Every reply is primed with assistant
  return numTokens;
}

int countStringTokens(String string, String modelName) {
  Tiktoken encoding = encodingForModel(modelName);
  return encoding.encode(string).length;
}
