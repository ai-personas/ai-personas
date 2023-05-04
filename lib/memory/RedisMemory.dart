// import 'dart:convert';
// import 'dart:typed_data';
// import 'package:flutter/material.dart';
// import 'package:provider/provider.dart';
// import 'package:redis/redis.dart';
// import 'package:colorize/colorize.dart';
// import '../config/RedisConfig.dart';
// import 'memory_base.dart';
//
// class RedisMemory {
//   final RedisConfig cfg;
//   late Command _redis;
//   late int vecNum;
//
//   static const int dimension = 1536;
//   final logger = Logger();
//
//   RedisMemory(BuildContext context, this.cfg) {
//     final redisConnection = RedisConnection();
//     redisConnection
//         .connect(cfg.redisHost, cfg.redisPort)
//         .then((Command command) {
//       _redis = command;
//       if (cfg.redisPassword.isNotEmpty) {
//         _redis.send_object(["AUTH", cfg.redisPassword]);
//       }
//       // Add code to handle SCHEMA and create index here.
//       // Dart does not have a native RediSearch package.
//       // You may need to execute raw Redis commands using _redis.send_object([...])
//
//       if (cfg.wipeRedisOnStart) {
//         _redis.send_object(["FLUSHALL"]);
//       }
//
//       _redis.send_object(["GET", "${cfg.memoryIndex}-vec_num"]).then((response) {
//         vecNum = (response == null) ? 0 : int.parse(utf8.decode(response));
//       });
//     }).catchError((e) {
//       logger.writeLog(
//         'Error: ',
//         'FAILED TO CONNECT TO REDIS',
//         const TextStyle(color: Colors.red, fontSize: 18),
//       );
//       throw e;
//     });
//
//   }
//
//   Future<String> add(String data) async {
//     if (data.contains("Command Error:")) {
//       return "";
//     }
//     List<double> vector = await getAdaEmbedding(data);
//     var vectorBytes = Float32List.fromList(vector).buffer.asUint8List();
//
//     Map<String, dynamic> dataDict = {
//       "data": data,
//       "embedding": vectorBytes
//     };
//
//     await _redis.send_object(["HSET", "${cfg.memoryIndex}:${vecNum}", "data", data, "embedding", vectorBytes]);
//     vecNum++;
//     await _redis.send_object(["SET", "${cfg.memoryIndex}-vec_num", vecNum]);
//
//     return "Inserting data into memory at index: $vecNum:\n" "data: $data";
//   }
//
//   Future<List<dynamic>?> getRelevant(String data, [int numRelevant = 5]) async {
//     List<double> queryEmbedding = await getAdaEmbedding(data);
//
//     // Implement the RediSearch search functionality here.
//     // Dart does not have a native RediSearch package.
//     // You may need to execute raw Redis commands using _redis.send_object([...])
//
//     // Replace this with actual search results from Redis.
//     List<Map<String, dynamic>> searchResults = [];
//
//     return searchResults.map((result) => result['data']).toList();
//   }
//
//   Future<String> clear() async {
//     await _redis.send_object(["FLUSHALL"]);
//     return "Obliviated";
//   }
//
//   Future<Map<String, dynamic>?> getStats() async {
//     // Add code to retrieve index information here.
//     // Dart does not have a native RediSearch package.
//     // You may need to execute raw Redis commands using _redis.send_object([...])
//
//     // Replace this with the actual stats from Redis.
//     Map<String, dynamic> indexStats = {};
//
//     return indexStats;
//   }
// }