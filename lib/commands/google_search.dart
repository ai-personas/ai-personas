import 'dart:convert';
import 'package:ai_personas/config/AppConfig.dart';
import 'package:ai_personas/config/ConfigKeys.dart';
import 'package:html/parser.dart';
import 'package:http/http.dart' as http;

Future<String> searchGoogle(String query) async {
  // Send a request to the Google Custom Search API
  final response = await http.get(
    Uri.parse('https://www.googleapis.com/customsearch/v1?q=$query&cx=${cfg[ConfigKeys.customSearchEngineId]}&key=${cfg[ConfigKeys.googleApiKey]}'),
  );

  if (response.statusCode == 200) {
    // If the request is successful, parse the JSON response
    Map<String, dynamic> jsonResponse = json.decode(response.body);

    // Extract the items results from the response
    List<dynamic> items = jsonResponse['items'];

    // Create a list of JSON objects with the specified structure
    List<Map<String, dynamic>> searchResults = items.map((item) {
      return {
        'title': item['title'],
        'href': item['link'],
        'body': item['snippet'],

      };
    }).toList();

    // Convert the list of JSON objects to a JSON string
    return json.encode(searchResults);
  } else {
    throw Exception('Failed to search Google: ${response.body}');
  }
}



Future<String> ddgSearch(String query, {int numResults = 8}) async {
  List<Map<String, dynamic>> searchResults = [];

  if (query.isEmpty) {
    return jsonEncode(searchResults);
  }

  final results = await ddg(query, maxResults: numResults);

  if (results.isEmpty) {
    return jsonEncode(searchResults);
  }

  searchResults.addAll(results);
  return jsonEncode(searchResults);
}

Future<List<Map<String, dynamic>>> ddg(String query, {required int maxResults}) async {
  List<Map<String, dynamic>> results = [];
  final searchUrl = 'https://duckduckgo.com/html/?q=$query';
  final response = await http.get(Uri.parse(searchUrl));

  if (response.statusCode == 200) {
    var document = parse(response.body);
    var searchElements = document.querySelectorAll('.result');
    for (var element in searchElements.take(maxResults)) {
      final titleElement = element.querySelector('.result__title');
      final snippetElement = element.querySelector('.result__snippet');
      final linkElement = element.querySelector('.result__url');
      if (titleElement != null && snippetElement != null && linkElement != null) {
        results.add({
          'title': titleElement.text,
          'snippet': snippetElement.text,
          'link': linkElement.attributes['href'] ?? '',
        });
      }
    }
  }
  return results;
}



