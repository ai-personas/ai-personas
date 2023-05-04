import 'dart:async';
import 'package:vector_math/vector_math.dart';

// You'll need to implement a Dart package or method to interact with the OpenAI API for embeddings.
import '../client/OpenAi.dart';

Future<List<double>> getAdaEmbedding(String text) async {
  text = text.replaceAll('\n', ' ');
  // Replace this with the actual OpenAI API call to create embeddings.
  // final embedding = await openai.embeddings.create(input: [text], model: 'text-embedding-ada-002');
  // return embedding.jsonBody['data'][0]['embedding'] as Vector;
  const int embedDim = 1536;
  return List<double>.filled(embedDim, 0.0);
}

abstract class MemoryBase {
  Future<String> add(String data);

  Future<List<String>?> get(String data);

  String clear();

  Future<List<String>> getRelevant(String data, {int numRelevant = 5});

  Map<String, dynamic> getStats();
}
