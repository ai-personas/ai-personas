import 'dart:async';
import 'dart:convert';
import 'dart:math';

import 'package:ai_personas/config/app_config.dart';
import 'package:ai_personas/config/config_keys.dart';
import 'package:ai_personas/persona/persona.dart';
import 'package:openai_client/src/model/openai_chat/chat_message.dart';
import 'package:tuple/tuple.dart';

import 'llm_utils.dart';
import 'token_counter.dart';


Map<String, dynamic> createChatMessage(String role, String content) {
  return {
    'role': role,
    'content': content,
  };
}

Tuple4<int, int, int, List<Map<String, dynamic>>> generateFullContext(
    String context,
    String relevantMemory,
    List<Map<String, dynamic>> fullMessageHistory,
    String model) {
  List<Map<String, dynamic>> currentContext = [
    createChatMessage('system', context),
    createChatMessage(
        'system', 'The current time and date is ${DateTime.now()}'),
    createChatMessage(
        'system', 'This reminds you of these events from your past:\n'
        '$relevantMemory\n\n'),
  ];

  int nextMessageToAddIndex = fullMessageHistory.length - 1;
  int insertionIndex = currentContext.length;
  int currentTokensUsed = countMessageTokens(currentContext, modelName: model);

  return Tuple4(
      nextMessageToAddIndex, currentTokensUsed, insertionIndex, currentContext);
}

Future<List<String>> getRelevantMemory(
    List<Map<String, dynamic>> fullMessageHistory) async {
  if (fullMessageHistory == null || fullMessageHistory.isEmpty) {
    return [];
  }

  Persona persona = await Persona.getCurrentPersona;
  List<String> relMemoryList = await persona.memory!.getRelevant(
      fullMessageHistory
          .sublist(max(0, fullMessageHistory.length - 9))
          .join(),
      numRelevant: 10);

  return relMemoryList;
}

Future<String> chatWithPersona(Persona? persona, String userInput,
    int tokenLimit) async {
  while (true) {
      String model = cfg[ConfigKeys.fastLLMModel];

      List<String> relevantMemoryList = await getRelevantMemory(persona!.fullMessageHistory);

      int sendTokenLimit = tokenLimit - 1000;

      Tuple4<int, int, int, List<Map<String, dynamic>>> contextData =
      generateFullContext(persona.context, relevantMemoryList.join("\n"), persona.fullMessageHistory, model);

      int nextMessageToAddIndex = contextData.item1;
      int currentTokensUsed = contextData.item2;
      int insertionIndex = contextData.item3;
      List<Map<String, dynamic>> currentContext = contextData.item4;

      while (currentTokensUsed > 2500) {
        if (relevantMemoryList.isNotEmpty) {
          relevantMemoryList.removeLast();
        }
        contextData = generateFullContext(
            persona.context, relevantMemoryList.join("\n"), persona.fullMessageHistory, model);

        nextMessageToAddIndex = contextData.item1;
        currentTokensUsed = contextData.item2;
        insertionIndex = contextData.item3;
        currentContext = contextData.item4;
      }

      currentTokensUsed +=
          countMessageTokens(
              [createChatMessage('user', userInput)], modelName: model);

      while (nextMessageToAddIndex >= 0) {
        Map<String, dynamic> messageToAdd =
        persona.fullMessageHistory[nextMessageToAddIndex];

        int tokensToAdd = countMessageTokens([messageToAdd], modelName: model);
        if (currentTokensUsed + tokensToAdd > sendTokenLimit) {
          break;
        }

        currentContext.insert(insertionIndex, messageToAdd);
        currentTokensUsed += tokensToAdd;
        nextMessageToAddIndex -= 1;
      }

      currentContext.add(createChatMessage('user', userInput));

      int tokensRemaining = tokenLimit - currentTokensUsed;

      List<ChatMessage> chatMessages = currentContext.map((message) => ChatMessage.fromJson(json.encode(message))).toList();
      String assistantReply = await createChatCompletion(
        model: model,
        messages: chatMessages,
        maxTokens: tokensRemaining,
      );

      persona.addMessageToHistory(createChatMessage('user', userInput));
      persona.addMessageToHistory(createChatMessage('assistant', assistantReply));

      return assistantReply;
  }
}
