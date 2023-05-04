import 'package:http/http.dart' as http;
import 'package:html/parser.dart' show parse;
import 'package:html/dom.dart';
import 'package:web_scraper/web_scraper.dart';

Future<String> scrapeText(String url) async {
  final webScraper = WebScraper();
  String text = '';

  try {
    if (await webScraper.loadWebPage(url)) {
      Document document = parse(webScraper.getPageContent());
      document.querySelectorAll('script, style').forEach((element) {
        element.remove();
      });

      text = document.body!.text.trim();
    }
  } catch (e) {
    text = 'Error: $e';
  }

  return text;
}

Future<List<String>?> scrapeLinks(String url) async {
  final webScraper = WebScraper();
  List<String>? links;

  try {
    if (await webScraper.loadWebPage(url)) {
      Document document = parse(webScraper.getPageContent());
      document.querySelectorAll('script, style').forEach((element) {
        element.remove();
      });

      links = document.querySelectorAll('a[href]').map<String>((element) {
        final anchor = element.attributes['href']!;
        return anchor.startsWith('http') ? anchor : '$url$anchor';
      }).toList();
    }
  } catch (e) {
    print('Error: $e');
  }

  return links;
}
