import 'dart:async';
import 'package:ai_personas/persona/persona.dart';

import '../config/app_config.dart';
import '../config/config_keys.dart';
import '../llm_utils.dart';
import '../utils/console.dart';
import 'package:openai_client/src/model/openai_chat/chat_message.dart';

Stream<String> splitText(String text, {int maxLength = 8192}) async* {
  final paragraphs = text.split('\n');
  var currentLength = 0;
  var currentChunk = [];

  for (final paragraph in paragraphs) {
    if (currentLength + paragraph.length + 1 <= maxLength) {
      currentChunk.add(paragraph);
      currentLength += paragraph.length + 1;
    } else {
      yield currentChunk.join('\n');
      currentChunk = [paragraph];
      currentLength = paragraph.length + 1;
    }
  }

  if (currentChunk.isNotEmpty) {
    yield currentChunk.join('\n');
  }
}

Future<String> summarizeText(
    String url, String text, String question) async {
  if (text.isEmpty) {
    return "Error: No text to summarize";
  }

  Persona persona = await Persona.getCurrentPersona;
  final textLength = text.length;
  print('Text length: $textLength characters');

  final summaries = [];
  final chunks = await splitText(text).toList();
  final scrollRatio = 1 / chunks.length;

  for (var i = 0; i < chunks.length; i++) {
    await console.stdout('Adding chunk ${i + 1} / ${chunks.length} to memory');

    final memoryToAdd = 'Source: $url\nRaw content part#${i + 1}: ${chunks[i]}';

    await persona.addDataToMemory(memoryToAdd);

    await console.stdout('Summarizing chunk ${i + 1} / ${chunks.length}');
    final messages = [createMessage(chunks[i], question)];

    final summary = await createChatCompletion(
      model: cfg[ConfigKeys.fastLLMModel],
      messages: messages,
    );
    summaries.add(summary);
    await console.stdout('Added chunk ${i + 1} summary to memory');

    final memoryToAdd2 =
        'Source: $url\nContent summary part#${i + 1}: $summary';

    await persona.addDataToMemory(memoryToAdd2);
  }

  await console.stdout('Summarized ${chunks.length} chunks.');

  final combinedSummary = summaries.join('\n');
  final messages = [createMessage(combinedSummary, question)];

  return createChatCompletion(
    model: cfg[ConfigKeys.fastLLMModel],
    messages: messages,
  );
}

ChatMessage createMessage(String chunk, String question) {
  return ChatMessage(
    role: 'user',
    content:
    '"""$chunk""" Using the above text, answer the following question: '
        '"$question" -- if the question cannot be answered using the text, '
        'summarize the text.',
  );
}