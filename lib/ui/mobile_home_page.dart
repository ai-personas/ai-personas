import 'package:ai_personas/ui/consoleUI.dart';
import 'package:flutter/material.dart';

import 'config_page.dart';

class MobileHomePage extends StatefulWidget {
  // Add this static method to create an instance of WebHomePage
  static MobileHomePage MainPage() => MobileHomePage();

  @override
  _MobileHomePageState createState() => _MobileHomePageState();
}

class _MobileHomePageState extends State<MobileHomePage> {
  Future<void> _init() async {
  }

  @override
  void initState() {
    super.initState();
    _init();
  }

  void _showPopupMenu(BuildContext context, Offset offset) async {
    final screenWidth = MediaQuery.of(context).size.width;
    final result = await showMenu<String>(
      context: context,
      position: RelativeRect.fromLTRB(screenWidth - 200, offset.dy - 40, 0, 0),
      items: <PopupMenuEntry<String>>[
        const PopupMenuItem<String>(
          value: 'config',
          child: Text('Config', style: TextStyle(color: Colors.white)),
        ),
      ],
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: BorderSide(color: Colors.white, width: 1),
      ),
      color: Colors.black,
    );

    if (result == 'config') {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => ConfigPage()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            color: Colors.black,
            child: ConsoleUI(),
          ),
          SafeArea(
            child: Align(
              alignment: Alignment.topRight,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: InkWell(
                  onTap: () {
                    final RenderBox overlay = Overlay.of(context)!.context.findRenderObject() as RenderBox;
                    final Offset offset = overlay.localToGlobal(Offset.zero);
                    _showPopupMenu(context, offset);
                  },
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Image.asset(
                        'assets/logo.jpeg',
                        width: 40,
                        height: 40,
                      ),
                      Icon(
                        Icons.menu,
                        size: 24,
                        color: Colors.white,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
