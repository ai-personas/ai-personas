import 'dart:convert';
import 'package:ai_personas/config/app_config.dart';
import 'package:ai_personas/config/config_keys.dart';
import 'package:ai_personas/llm_utils.dart';
import 'package:ai_personas/memory/memory_base.dart';
import 'package:pinecone/pinecone.dart';

class PineconeMemory extends MemoryBase {
  String personaName;
  final int dimension = 1536;
  final IndexMetric metric = IndexMetric.cosine;

  PineconeClient client;
  String? host;
  String? environment;

  PineconeMemory._(this.client, this.personaName, this.environment);

  static Future<PineconeMemory> create(String environment, String personaName) async {
    String apiKey = cfg[ConfigKeys.pineconeApiKey];
    PineconeClient client = PineconeClient(apiKey: apiKey, environment: environment);
    personaName = personaName.toLowerCase();
    PineconeMemory pineconeMemory = PineconeMemory._(client, personaName, environment);
    await pineconeMemory._init();
    return pineconeMemory;
  }

  Future<void> _init() async {
    List<String> indexNames = await client.index.listIndexes();

    if (!indexNames.contains(personaName)) {
      await client.index.createIndex(
        body: IndexDefinition(
          name: personaName,
          dimension: dimension,
          metric: metric,
        ),
      );

      bool creating = true;
      while (creating) {
        print("Waiting for index to be created...");
        await Future.delayed(Duration(seconds: 10));
        final index = await client.index.describeIndex(indexName: personaName);
        creating = index.status.state != IndexState.ready;
      }
    }

    final indexMeta = await client.index.describeIndex(indexName: personaName);
    host = indexMeta.status.host;
  }

  Future<String> add(String data) async {
    List<double> vectorData = await createEmbeddingWithAda(data);
    final upsertRes = await client.vector(host: host!).upsert(
      body: UpsertRequest(
        vectors: [
          UpsertVector(id: DateTime.now().toString(), values: vectorData, metadata: {'data': data}),
        ],
      ),
    );

    String text = 'Inserting data into memory : $vectorData';
    return text;
  }

  Future<List<String>> getRelevant(String data, {int numRelevant = 5}) async {
    List<double> vectorData = await createEmbeddingWithAda(data);
    final queryRes = await client.vector(host: host!).query(
      body: QueryRequest(
        topK: numRelevant,
        includeValues: true,
        includeMetadata: true,
        vector: vectorData,
      ),
    );

    return queryRes.matches
        .map((match) => (match.metadata as Map<String, dynamic>)['data']?.toString())
        .where((element) => element != null)
        .toList()
        .cast<String>();
  }

  Future<String> clear() async {
    await client.index.deleteIndex(indexName: personaName);
    return 'Obliviated';
  }

  Future<Map<String, dynamic>> getStats() {
    return Future.value({});
  }

  void endSession() {
    client.endSession();
  }

  @override
  Future<List<String>?> get(String data) {
    return getRelevant(data);
  }

  String toJsonString() {
    return jsonEncode({
      "provider": "Pinecone",
      "dimension": dimension,
      "metric": metric.name,
      "index": personaName,
      "environment": environment
    });
  }

  static Future<PineconeMemory> load(String jsonString) async {
    Map<String, dynamic> jsonData = jsonDecode(jsonString);
    return create(jsonData['environment'], jsonData['index']);
  }

}
