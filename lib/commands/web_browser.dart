import 'package:ai_personas/preprocessing/text.dart';
import 'package:html/dom.dart' as dom;
import 'package:html/parser.dart' as html_parser;
import 'package:http/http.dart' as http;

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

