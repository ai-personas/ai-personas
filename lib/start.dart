import 'dart:async';
import 'dart:io';

import 'package:ai_personas/config/AppConfig.dart';
import 'package:ai_personas/persona/persona.dart';
import 'package:ai_personas/speech/say.dart';
import 'package:flutter/material.dart';
import 'package:ai_personas/persona/persona_main.dart';
import 'package:ai_personas/utils/console.dart';
import 'package:ai_personas/prompt.dart';
import 'package:ai_personas/memory/memory.dart';

Future<void> start() async {
  await AppConfig.checkApiKeys();

  PersonaMain personaMain = PersonaMain(
    nextActionCount: 0,
    prompt: await constructPrompt(),
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

