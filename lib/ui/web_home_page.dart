import 'package:ai_personas/persona/persona.dart';
import 'package:ai_personas/ui/consoleUI.dart';
import 'package:ai_personas/ui/events/persona_change_event.dart';
import 'package:ai_personas/ui/global.dart';
import 'package:ai_personas/utils/persona_downloader.dart';
import 'package:flutter/material.dart';

import 'config_page.dart';

class WebHomePage extends StatefulWidget {
  // Add this static method to create an instance of WebHomePage
  static WebHomePage MainPage() => WebHomePage();

  @override
  _WebHomePageState createState() => _WebHomePageState();
}

class _WebHomePageState extends State<WebHomePage> {
  String personaName = '';

  @override
  void initState() {
    super.initState();
    eventBus.on<PersonaChangeEvent>().listen((event) {
      setState(() {
        personaName = event.personaName;
      });
    });
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
                          if (personaName.isNotEmpty)
                            InkWell(
                              onTap: () {
                                PersonaDownloader.downloadPersona(personaName);
                              },
                              child: Icon(
                                Icons.download,
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

}
