// import 'dart:async';
// import 'dart:convert';
// import 'package:flutter/material.dart';
// import 'package:webview_flutter/webview_flutter.dart';
//
// Future<Map<String, String>?> getContent(String url, String textToInput) async {
//   final controller = WebViewController()
//     ..setJavaScriptMode(JavaScriptMode.unrestricted)
//     ..setBackgroundColor(const Color(0x00000000));
//
//   Completer<void> pageLoaded = Completer<void>();
//   bool pageLoadedCompleted = false;
//
//   controller.setNavigationDelegate(
//     NavigationDelegate(
//       onProgress: (int progress) {
//         // Update loading bar.
//       },
//       onPageStarted: (String url) {},
//       onPageFinished: (String url) {
//         // Mark the page as loaded when onPageFinished is called
//         if (!pageLoadedCompleted) {
//           pageLoaded.complete();
//           pageLoadedCompleted = true;
//         }
//       },
//       onWebResourceError: (WebResourceError error) {},
//       onNavigationRequest: (NavigationRequest request) {
//         if (request.url.startsWith('https://www.youtube.com/')) {
//           return NavigationDecision.prevent;
//         }
//         return NavigationDecision.navigate;
//       },
//     ),
//   );
//
//   await controller.loadRequest(Uri.parse(url));
//
//   // Wait for the page to load
//   await pageLoaded.future;
//
//   await Future.delayed(const Duration(seconds: 2));
//
//   // Fill the text area
//   await controller.runJavaScript('''
//     document.querySelector("textarea").value = "${textToInput}";
//   ''');
//
//   await Future.delayed(const Duration(seconds: 2));
//
//   final clickResult = await controller.runJavaScriptReturningResult('''
//     (() => {
//       const submitInputs = document.querySelectorAll('input[type="submit"]');
//       let clicked = false;
//       let debugInfo = [];
//
//       for (const input of submitInputs) {
//         debugInfo.push(input.value);
//         if (input.value.includes("Google Search")) {
//           input.click();
//           clicked = true;
//           break;
//         }
//       }
//
//       const documentText = document.documentElement.outerHTML;
//       debugInfo.push(documentText);
//
//       return { clicked: clicked, debugInfo: debugInfo };
//     })();
//   ''');
//
//   if (clickResult is Map<dynamic, dynamic>) {
//     if (clickResult['clicked'] == true) {
//       print('Click happened');
//     } else {
//       print('Click did not happen');
//       print('Debug info: ${clickResult['debugInfo']}');
//     }
//   } else {
//     print('Unexpected result type');
//   }
//
//   return null;
// }
//

import 'dart:convert';
import 'package:ai_personas/config/ConfigKeys.dart';
import 'package:ai_personas/memory/memory_base.dart';
import 'package:ai_personas/preprocessing/text.dart';
import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;
import 'package:html/dom.dart' as dom;

import '../config/AppConfig.dart';

Future<String> fetchWebsiteContent(String url, String question) async {
  // Send a request to the URL
  final response = await http.get(Uri.parse(url));

  if (response.statusCode == 200) {
    // If the request is successful, parse the HTML content
    dom.Document document = html_parser.parse(response.body);

    // Extract the text from relevant elements, like paragraphs or headings
    List<dom.Element> textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6');

    // Create a text summary by concatenating the text content of the elements
    String text = textElements.map((element) => element.text.trim()).join('\n\n');
    String summary = await summarizeText(url, text, question);

    return 'Answer gathered from website: $summary';
  } else {
    throw Exception('Failed to load website content');
  }
}

