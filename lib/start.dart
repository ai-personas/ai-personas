import 'dart:async';

import 'package:ai_personas/persona/persona_main.dart';
import 'package:ai_personas/speech/say.dart';
import 'package:ai_personas/utils/console.dart';

Future<void> start() async {

  PersonaMain personaMain = PersonaMain(
    nextActionCount: 0,
    userInput: (
        "Determine which next command to use, and respond using the"
            " format specified above:"
    ),
    textToSpeech: TextToSpeech(),
  );

  // Start the interaction loop
  await personaMain.startInteractionLoop();
  await console.yesOrNo("Continue");

}

