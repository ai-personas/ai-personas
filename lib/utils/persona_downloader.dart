import 'dart:io';
import 'package:ai_personas/persona/persona.dart';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import 'dart:html' as html;

class PersonaDownloader {

  static Future<void> downloadPersona(String personaName) async {
    Persona persona = await Persona.getPersona(personaName);

    if (kIsWeb) {
      // Create a Blob with the console output content
      final blob = html.Blob([persona.getJson()]);

      // Create an anchor element with a download attribute
      final anchor = html.AnchorElement(href: html.Url.createObjectUrlFromBlob(blob));
      anchor.download = '${persona.name}.txt';

      // Trigger the download by simulating a click on the anchor element
      anchor.click();
    } else {
      // Get the temporary directory
      final tempDir = await getTemporaryDirectory();
      File tempFile = File('${tempDir.path}/console_output.txt');

      // Write the console output to a temporary file
      await tempFile.writeAsString(persona.getJson());

      // Share the file using the share_plus package
      await Share.shareFiles([tempFile.path], mimeTypes: ['text/plain']);
    }
  }
}
