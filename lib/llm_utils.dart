import 'dart:async';
import 'package:ai_personas/config/config_keys.dart';
import 'package:openai_client/openai_client.dart';
import 'package:openai_client/src/model/openai_chat/chat_message.dart';
import 'config/app_config.dart';

OpenAIConfiguration loadConfiguration() {
  return OpenAIConfiguration(
    apiKey: cfg[ConfigKeys.openaiApiKey],
  );
}

Future<String> callAiFunction(String function, List<String> args, String description, {String? model}) async {
  model ??= 'text-davinci-002';

  args = args.map((arg) => arg != null ? arg.toString() : "None").toList();
  String argsString = args.join(", ");
  List<ChatMessage> messages = [
    ChatMessage(
      role: 'system',
      content: 'You are now the following python function: ```# $description\n$function```\n\nOnly respond with your `return` value.',
    ),
    ChatMessage(
      role: 'user',
      content: argsString,
    ),
  ];

  return await createChatCompletion(model: model, messages: messages, temperature: 0);
}

Future<String> createChatCompletion({required List<ChatMessage> messages, String? model, double? temperature, int? maxTokens}) async {
  model ??= 'text-davinci-002';
  temperature ??= 0.9;

  // Create a new client.
  final client = OpenAIClient(
    configuration: loadConfiguration(),
  );

  // Create a chat.
  final chat = await client.chat.create(
    model: model,
    messages: messages,
    temperature: temperature,
    maxTokens: maxTokens,
  ).data;

  // Close the client and terminate the [http] connection.
  client.close();

  return chat.choices[0].message.content;
}

Future<List<double>> createEmbeddingWithAda(String text) async {
  int numRetries = 10;
  int backoff;

  // Create a new client.
  final client = OpenAIClient(
    configuration: loadConfiguration(),
  );

  List<double> embedding = [];

  for (int attempt = 0; attempt < numRetries; attempt++) {
    backoff = 2 ^ (attempt + 2);

    try {
      final response = await client.embeddings.create(
        model: 'text-embedding-ada-002',
        input: [text],
      ).data;

      if (response.data.isNotEmpty) {
        embedding = List<double>.from(response.data[0].embedding);
        break;
      } else {
        if (attempt == numRetries - 1) {
          throw Exception('Failed to get response after $numRetries retries');
        }
        await Future.delayed(Duration(seconds: backoff));
      }
    } catch (e) {
      throw Exception('An error occurred: $e');
    }
  }

  // Close the client and terminate the [http] connection.
  client.close();

  return embedding;
}
