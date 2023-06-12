import 'package:ai_personas/start.dart';
import 'package:ai_personas/ui/mobile_home_page.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'ui/web_home_page.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();

// Start the concurrent tasks
  Future<void> startFuture = Future.delayed(Duration.zero, start);

  runApp(
    ChangeNotifierProvider(
      create: (context) => null,
      child: MyApp(),
    ),
  );

// Wait for the start method to complete
  await startFuture;
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    if (isWebPlatform()) {
      return WebHomePage();
    } else {
      return MobileHomePage();
    }
  }
}

bool isWebPlatform() {
  return identical(0, 0.0); // Returns true for web and false for mobile
}



