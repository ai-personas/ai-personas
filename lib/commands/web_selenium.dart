import 'package:http/http.dart' as http;
import 'package:html/parser.dart' show parse;
import 'package:html/dom.dart';
import 'package:webdriver/async_io.dart';
import 'dart:async';

Future<void> browseWebsite(String url) async {
  final webDriver = await createDriver();
  String text = await scrapeTextWithWebDriver(webDriver, url);
  // Replace the following line with the actual text summarization logic.
  String summaryText = 'Summary of the text';
  List<String> links = await scrapeLinksWithWebDriver(webDriver, url);

  // Limit links to 5
  if (links.length > 5) {
    links = links.sublist(0, 5);
  }

  print('Answer gathered from website: $summaryText\n\nLinks: ${links.join(', ')}');
}

Future<String> scrapeTextWithWebDriver(WebDriver driver, String url) async {
  await driver.get(url);

  String pageSource = await driver.pageSource;
  Document document = parse(pageSource);

  for (Element script in document.querySelectorAll('script, style')) {
    script.remove();
  }

  String text = document.body!.text.trim();
  return text;
}

Future<List<String>> scrapeLinksWithWebDriver(WebDriver driver, String url) async {
  String pageSource = await driver.pageSource;
  Document document = parse(pageSource);

  for (Element script in document.querySelectorAll('script, style')) {
    script.remove();
  }

  List<String> links = [];

  for (Element link in document.querySelectorAll('a[href]')) {
    String href = link.attributes['href']!;
    // Add any additional link processing logic here.
    links.add(href);
  }

  return links;
}
