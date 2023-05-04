import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:html/parser.dart' show parse;
import 'package:html/dom.dart';

bool isLocalFile(String url) {
  final localPrefixes = [
    'file:///',
    'file://localhost/',
    'file://localhost',
    'http://localhost',
    'http://localhost/',
    'https://localhost',
    'https://localhost/',
    'http://2130706433',
    'http://2130706433/',
    'https://2130706433',
    'https://2130706433/',
    'http://127.0.0.1/',
    'http://127.0.0.1',
    'https://127.0.0.1/',
    'https://127.0.0.1',
    'https://0.0.0.0/',
    'https://0.0.0.0',
    'http://0.0.0.0/',
    'http://0.0.0.0',
    'http://0000',
    'http://0000/',
    'https://0000',
    'https://0000/',
  ];
  return localPrefixes.any((prefix) => url.startsWith(prefix));
}

Future<String> getResponse(String url) async {
  if (isLocalFile(url)) {
    throw Exception('Access to local files is restricted');
  }

  final response = await http.get(Uri.parse(url));

  if (response.statusCode >= 400) {
    throw Exception('Error: HTTP ${response.statusCode} error');
  }

  return response.body;
}

Future<String> scrapeText(String url) async {
  final response = await getResponse(url);
  final document = parse(response);

  document.querySelectorAll('script, style').forEach((element) {
    element.remove();
  });

  return document.body!.text.trim();
}

Future<List<String>> scrapeLinks(String url) async {
  final response = await getResponse(url);
  final document = parse(response);

  document.querySelectorAll('script, style').forEach((element) {
    element.remove();
  });

  return document
      .querySelectorAll('a[href]')
      .map<String>((element) => element.attributes['href']!)
      .toList();
}

class Message {
  final String role;
  final String content;

  Message({required this.role, required this.content});

  Map<String, String> toJson() {
    return {
      'role': role,
      'content': content,
    };
  }
}

Message createMessage(String chunk, String question) {
  return Message(
    role: 'user',
    content:
    '"""$chunk""" Using the above text, answer the following question: "$question"'
        ' -- if the question cannot be answered using the text, summarize the text.',
  );
}
