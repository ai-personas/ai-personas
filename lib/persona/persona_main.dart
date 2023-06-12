import 'dart:async';

import 'package:ai_personas/commands/command_executor.dart';
import 'package:ai_personas/config/app_config.dart';
import 'package:ai_personas/config/config_keys.dart';
import 'package:ai_personas/ui/events/persona_change_event.dart';
import 'package:ai_personas/ui/global.dart';
import 'package:ai_personas/utils/console.dart';
import 'package:flutter/material.dart';

import '../chat.dart';
import '../json_fixes/bracket_termination.dart';
import '../speech/say.dart';
import 'persona.dart';

class PersonaMain {
  Persona? persona;
  int nextActionCount;
  String userInput;
  TextToSpeech textToSpeech;
  dynamic arguments;

  PersonaMain({
    required this.nextActionCount,
    required this.userInput,
    required this.textToSpeech});

  Future<void> startInteractionLoop() async {
    await AppConfig.loadConfig();
    List<Map<String, Map<String, String>>> prevPersonas  = await Persona.getAllPersonas();

    if (prevPersonas.isEmpty) {
      // Directly go to "Create new Persona" if no previous personas exist
      await createNewPersona();
    } else {
      // If previous personas exist, show selection options
      Map<String, dynamic> selected = await console.groupedActions({"group": [
        {"button": {"buttonText": "Create new Persona", "returnVal": {'name': 'Create new Persona'}}},
        {"table": prevPersonas}
      ]});
      if (selected['name'] == 'Create new Persona') {
        await createNewPersona();
      } else {
        persona = await Persona.getPersona(selected['persona']['value']!);
      }
    }
    eventBus.fire(PersonaChangeEvent(Persona.currentPersona));
    printAllAssistantThoughts(Persona.currentPersona, persona!.fullMessageHistory);
    await console.showAsciiRotate();

    await AppConfig.checkApiKeys();
    persona = await Persona.getCurrentPersona;

    String personaName = persona!.name;
    int loopCount = 0;
    String commandName = '';

    while (true) {
      loopCount++;
      checkContinuousLimit(loopCount);

      String assistantReply;
      try {
        assistantReply = await chatWithPersona(
            persona, userInput,
            cfg[ConfigKeys.fastTokenLimit]);
        await console.printAssistantThoughts(personaName, assistantReply);
        commandName = extractCommandNameFromReply(assistantReply);
        speakCommandName(commandName);

        if (!cfg[ConfigKeys.continuousMode] && nextActionCount == 0) {
          final result = await getUserInputForCommandAuthorization(commandName, personaName);
          userInput = result['userInput']!;
          commandName = result['commandName']!;
          if (userInput == 'EXIT') {
            break;
          }
        } else {
          await console.stdout(
              'NEXT ACTION: COMMAND = ${commandName.toString()} ARGUMENTS = ${arguments.toString()}',
              textColor: Colors.cyan);
        }

        await processCommandResult(commandName, arguments, assistantReply);
      } catch (e) {
        await console.stdout('Error: ${e.toString()}', textColor: Colors.red);
        break; // Terminate the loop if an exception occurs
      }
      await persona!.save();
      if (!cfg[ConfigKeys.continuousMode] && nextActionCount == 0 && commandName != 'do_nothing') {
        await console.yesOrNo("Continue?");
      }
      // Decrease nextActionCount if it's not zero
      if (nextActionCount > 0) {
        nextActionCount--;
      }
    }
  }

  Future<void> createNewPersona() async {
    Map<String, String> cxtTemplate = await console.patternText(await Persona.getContext());
    await console.stdout('Persona - ${cxtTemplate['personaName']!}', textColor: Colors.yellow, fontSize: 22);
    await console.stdout(cxtTemplate['finalText']!, textColor: Colors.white70);
    await console.showAsciiRotate();
    persona = await Persona.createPersona(cxtTemplate['personaName']!, cxtTemplate['finalText']!);
  }

  Future<void> checkContinuousLimit(int loopCount) async {
    if (cfg[ConfigKeys.continuousMode] &&
        cfg[ConfigKeys.continuousLimit] > 0 &&
        loopCount > cfg[ConfigKeys.continuousLimit]) {
      await console.stdout(
          'Continuous Limit Reached: ${cfg[ConfigKeys.continuousLimit]}',
          textColor: Colors.yellow);
      throw Exception('Continuous limit reached');
    }
  }

  String extractCommandNameFromReply(String assistantReply) {
    var commandData = CommandExecutor.getCommand(
        extractJsonCommand(assistantReply));
    String commandName = commandData[0];
    arguments =  commandData[1];
    return commandName;
  }

  void speakCommandName(String commandName) {
    if (cfg[ConfigKeys.speakMode]) {
      TextToSpeech.sayText('I want to execute $commandName');
    }
  }

  Future<Map<String, String>> getUserInputForCommandAuthorization(String commandName, String aiName) async {
    userInput = '';
    await console.stdout('NEXT ACTION: COMMAND = $commandName ARGUMENTS = $arguments', textColor: Colors.cyan);
    await console.stdout(
        "Enter 'y' to authorize command, 'y -N' to run N continuous "
            "commands, 'n' to exit program, or enter feedback for "
            '$aiName...');

    while (true) {
      String consoleInput = await console.getUserInput("Input:");

      if (consoleInput.toLowerCase() == 'y') {
        userInput = 'GENERATE NEXT COMMAND JSON';
        await console.stdout('-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=', textColor: Colors.amber);
        break;
      } else if (consoleInput.toLowerCase().startsWith('y -')) {
        try {
          nextActionCount = int.parse(consoleInput.split(' ')[1]);
          userInput = 'GENERATE NEXT COMMAND JSON';
        } catch (e) {
          await console.stdout(
              'Invalid input format. Please enter "y -n" where n is '
                  'the number of continuous tasks.');
          continue;
        }
        break;
      } else if (consoleInput.toLowerCase() == 'n') {
        userInput = 'EXIT';
        await console.stdout('Exiting...');
        break;
      } else {
        userInput = consoleInput;
        commandName = 'human_feedback';
        break;
      }
    }

    return {'userInput': userInput, 'commandName': commandName};
  }

  Future<void> processCommandResult(String commandName, dynamic arguments, String assistantReply) async {
    String? result;
    String? cmdResult;
    if (commandName == 'human_feedback') {
      result = 'Human feedback: $userInput';
    } else {
      cmdResult = await CommandExecutor.executeCommand(commandName, arguments);
      if (cmdResult!.startsWith('Error:')) {
        result = 'Command ${commandName} threw the following error: ${cmdResult.toString()}';
      } else {
        result = 'Command ${commandName} returned: ${cmdResult.toString()}';
      }
    }

    String memoryToAdd = 'Assistant Reply: $assistantReply \nResult: ${result.toString()}';
    await persona?.addDataToMemory(memoryToAdd);

    await console.stdout('SYSTEM:', textColor: Colors.yellow);
    if (cmdResult != null && !cmdResult!.startsWith('Error:')) {
      persona?.addMessageToHistory(createChatMessage('system', result));
      await console.stdout(result, textColor: Colors.white70);
    } else {
      persona?.addMessageToHistory(createChatMessage('system', 'Unable to execute command'));
      await console.stdout('Unable to execute command', textColor: Colors.red);
    }
  }

  void printAllAssistantThoughts(String personaName, List<Map<String, dynamic>> fullMessageHistory) async {
    for (var message in fullMessageHistory) {
      if (message['role'] == 'assistant') {
        await console.printAssistantThoughts(personaName, message['content']);
      }
    }
  }
}