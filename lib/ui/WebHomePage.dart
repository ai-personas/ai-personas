import 'dart:io';

import 'package:ai_personas/persona/persona.dart';
import 'package:ai_personas/ui/consoleUI.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import '../utils/console.dart';
import 'ConfigPage.dart';
import 'package:share_plus/share_plus.dart';
import 'dart:html' as html;
import 'package:flutter/foundation.dart' show kIsWeb;

class WebHomePage extends StatefulWidget {
  @override
  _WebHomePageState createState() => _WebHomePageState();
}

class _WebHomePageState extends State<WebHomePage> {
  Future<void> _init() async {
    // final localCache = await LocalCache.create(cfg[ConfigKeys.memoryIndex]);
    //
    // await localCache.add("{'text': 'Some text'}");
    // final relevantTexts = await localCache.getRelevant('Query text', numRelevant: 5);
    // print(relevantTexts);
  }

  void _showConfigDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return Dialog(
          child: Container(
            width: MediaQuery.of(context).size.width * 0.5,
            height: MediaQuery.of(context).size.height * 0.8,
            child: ConfigPage(),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: ConstrainedBox(
          constraints: BoxConstraints(
            maxWidth: 800, // Adjust this value according to your desired maximum width
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SafeArea(
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween, // Add this line
                    children: [
                      Row(
                        children: [
                          Image.asset(
                            'assets/logo.jpeg',
                            width: 40,
                            height: 40,
                          ),
                          SizedBox(width: 8),
                          Text(
                            'AiPersonas',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                            ),
                          ),
                        ],
                      ),
                      Row(
                        children: [
                          InkWell(
                            onTap: () {
                              _showConfigDialog(context);
                            },
                            child: Icon(
                              Icons.settings,
                              size: 24,
                              color: Colors.white,
                            ),
                          ),
                          SizedBox(width: 8),
                          InkWell(
                            onTap: () {
                              _downloadContent();
                            },
                            child: Icon(
                              Icons.download, // Add the download icon
                              size: 24,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                child: ConsoleUI(),
              ),
              SizedBox(height: 16),
              SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _downloadContent() async {
    List<Map<String, dynamic>> consoleOutput = console.output.value;
    String content = consoleOutput.map((entry) => entry['text']).join('\n');

    if (kIsWeb) {
      // Create a Blob with the console output content
      final blob = html.Blob([content]);

      // Create an anchor element with a download attribute
      final anchor = html.AnchorElement(href: html.Url.createObjectUrlFromBlob(blob));
      Persona persona = await Persona.getPersona;
      anchor.download = '${persona.name}.txt';

      // Trigger the download by simulating a click on the anchor element
      anchor.click();
    } else {
      // Get the temporary directory
      final tempDir = await getTemporaryDirectory();
      File tempFile = File('${tempDir.path}/console_output.txt');

      // Write the console output to a temporary file
      await tempFile.writeAsString(content);

      // Share the file using the share_plus package
      await Share.shareFiles([tempFile.path], mimeTypes: ['text/plain']);
    }
  }

}
