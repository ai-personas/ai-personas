import 'package:ai_personas/start.dart';
import 'package:ai_personas/ui/MobileHomePage.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'ui/WebHomePage.dart';
import 'utils/console.dart';

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


// import 'dart:async';
// import 'dart:convert';
// import 'dart:io';
// import 'dart:typed_data';
//
// import 'package:flutter/material.dart';
// import 'package:path_provider/path_provider.dart';
// import 'package:webview_flutter/webview_flutter.dart';
// import 'package:webview_flutter_android/webview_flutter_android.dart';
// import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';
//
// void main() => runApp(const MaterialApp(home: WebViewExample()));
//
// class WebViewExample extends StatefulWidget {
//   const WebViewExample({super.key});
//
//   @override
//   State<WebViewExample> createState() => _WebViewExampleState();
// }
//
// class _WebViewExampleState extends State<WebViewExample> {
//   late final WebViewController _controller;
//
//   @override
//   void initState() {
//     super.initState();
//
//     late final PlatformWebViewControllerCreationParams params;
//     if (WebViewPlatform.instance is WebKitWebViewPlatform) {
//       params = WebKitWebViewControllerCreationParams(
//         allowsInlineMediaPlayback: true,
//         mediaTypesRequiringUserAction: const <PlaybackMediaTypes>{},
//       );
//     } else {
//       params = const PlatformWebViewControllerCreationParams();
//     }
//
//     final WebViewController controller =
//     WebViewController.fromPlatformCreationParams(params);
//
//     controller
//       ..setJavaScriptMode(JavaScriptMode.unrestricted)
//       ..setBackgroundColor(const Color(0x00000000))
//       ..addJavaScriptChannel(
//         'Toaster',
//         onMessageReceived: (JavaScriptMessage message) {
//           ScaffoldMessenger.of(context).showSnackBar(
//             SnackBar(content: Text(message.message)),
//           );
//         },
//       )
//       ..loadRequest(Uri.parse('https://google.com')); // Load the desired URL
//
//     _controller = controller;
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text('Flutter WebView example'),
//       ),
//       body: WebViewWidget(controller: _controller),
//     );
//   }
// }

