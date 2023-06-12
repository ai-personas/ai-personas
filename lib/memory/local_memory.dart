import 'dart:convert';
import 'dart:math' as math;
import 'dart:typed_data';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:ai_personas/llm_utils.dart';
import 'package:path/path.dart' as p;
import 'memory_base.dart';
import 'package:ai_personas/utils/storage/storage.dart';

const int embedDim = 1536;

class CacheContent {
  List<String> texts;
  Float32List embeddings;

  CacheContent({List<String>? texts, Float32List? embeddings})
      : this.texts = texts ?? [],
        this.embeddings = embeddings ?? Float32List(0);

  Map<String, dynamic> toJson() {
    return {
      'texts': texts,
      'embeddings': embeddings.toList(),
    };
  }
}

class LocalCache extends MemoryBase {
  late String personaName;
  late CacheContent data;
  late Storage _storage;

  // Private constructor
  LocalCache._(String memoryIndex) {
    personaName = memoryIndex;
    _storage = kIsWeb ? WebStorage() : MobileStorage();
  }

  // Static method to create an instance of LocalCache
  static Future<MemoryBase> create(String memoryIndex) async {
    LocalCache cache = LocalCache._(memoryIndex);
    await cache._initialize('{}');
    return cache;
  }

  Future<void> _initialize(String? fileContent) async {
    if (fileContent == null || fileContent.trim().isEmpty) {
      fileContent = '{}';
    }

    try {
      Map<String, dynamic> loaded = json.decode(fileContent);
      List<double> doubleList = _parseEmbeddingsList(loaded['embeddings']);
      data = CacheContent(
        texts: List<String>.from(loaded['texts'] ?? []),
        embeddings: Float32List.fromList(doubleList),
      );
    } on FormatException {
      print("Error: The content is not in JSON format.");
      data = CacheContent();
    }
  }

  List<double> _parseEmbeddingsList(dynamic value) {
    if (value == null || !(value is List)) {
      return [];
    }

    List<dynamic> list = value;
    List<double> result = [];

    try {
      result = list.map((e) => e as double).toList();
    } catch (e) {
      print('Error parsing embeddings list: $e');
    }

    return result;
  }

  Future<String> add(String text) async {
    if (text.contains("Command Error:")) {
      return "";
    }
    data.texts.add(text);

    List<double> embeddingList = await createEmbeddingWithAda(text);
    Float32List embedding = Float32List.fromList(embeddingList);

    int oldLength = data.embeddings.length;
    int newLength = oldLength + embedding.length;
    Float32List newEmbeddings = Float32List(newLength);
    newEmbeddings.setRange(0, oldLength, data.embeddings);
    newEmbeddings.setRange(oldLength, newLength, embedding);
    data.embeddings = newEmbeddings;

    return text;
  }

  String toJsonString() {
    return jsonEncode({
      "provider": "Local",
      "data": data.toJson()
    });
  }

  static Future<LocalCache> load(String jsonString) async {
    LocalCache cache = LocalCache._('');

    try {
      // Decode the JSON string
      Map<String, dynamic> jsonData = json.decode(jsonString);

      // Load data
      if (jsonData.containsKey('data')) {
        Map<String, dynamic> dataJson = jsonData['data'];

        List<double> doubleList = cache._parseEmbeddingsList(dataJson['embeddings']);
        cache.data = CacheContent(
          texts: List<String>.from(dataJson['texts'] ?? []),
          embeddings: Float32List.fromList(doubleList),
        );
      } else {
        print("No data found in the provided JSON string.");
      }
    } catch (e) {
      print("Error in loading from JSON string: $e");
    }

    return cache;
  }

  Future<String> clear() async {
    data = CacheContent();
    return "Obliviated";
  }

  Future<List<String>?> get(String data) async {
    return await getRelevant(data, numRelevant: 1);
  }

  Future<List<String>> getRelevant(String text, {int numRelevant = 5}) async {
    List<double> embeddingList = await createEmbeddingWithAda(text);
    Float32List embedding = Float32List.fromList(embeddingList);

    // Implement matrix-vector multiplication and find scores for each row of the matrix
    List<double> scores = _dotProduct(data.embeddings, embedding);

    // Get indices for top-k winning scores
    List<int> topKIndices = _topKIndices(scores, numRelevant);

    // Return texts for those indices
    return [for (int i in topKIndices) data.texts[i]];
  }

  List<double> _dotProduct(Float32List matrix, Float32List vector) {
    int numRows = matrix.length ~/ embedDim;
    List<double> scores = List<double>.filled(numRows, 0);

    for (int i = 0; i < numRows; i++) {
      for (int j = 0; j < embedDim; j++) {
        scores[i] += matrix[i * embedDim + j] * vector[j];
      }
    }

    return scores;
  }

  List<int> _topKIndices(List<double> scores, int k) {
    List<int> indices = List<int>.generate(scores.length, (i) => i);
    indices.sort((a, b) => scores[b].compareTo(scores[a]));
    return indices.sublist(0, math.min(k, indices.length));
  }

  Future<Map<String, dynamic>> getStats() async {
    int numRows = data.embeddings.length ~/ embedDim;
    return {
      'texts': data.texts.length,
      'embeddings': [numRows, embedDim],
    };
  }
}
