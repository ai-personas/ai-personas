import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:ai_personas/config/ConfigKeys.dart';
import 'package:ai_personas/config/AppConfig.dart';
import 'package:flutter/material.dart';
import '../chat.dart';
import '../commands/web_browser.dart';
import 'persona.dart';
import '../memory/memory.dart';
import '../speech/say.dart';
import '../json_fixes/bracket_termination.dart';
import '../memory/memory_base.dart';
import 'package:ai_personas/app.dart';
import 'package:ai_personas/utils/console.dart';
import 'package:ai_personas/commands/command_executor.dart';

class PersonaMain {
  Persona? persona;
  int nextActionCount;
  String prompt;
  String userInput;
  TextToSpeech textToSpeech;
  dynamic arguments;
  MemoryBase? memory;

  PersonaMain({
    required this.nextActionCount,
    required this.prompt,
    required this.userInput,
    required this.textToSpeech});

  Future<void> startInteractionLoop() async {
    persona = await Persona.getPersona;
    String aiName = persona!.name;
    int loopCount = 0;
    String commandName = '';
    memory = await getMemory(init: false);

    while (true) {
      loopCount++;
      checkContinuousLimit(loopCount);

      String assistantReply;
      try {
        assistantReply = await chatWithPersona(
            persona, prompt, userInput,
            cfg[ConfigKeys.fastTokenLimit]);
        await console.printAssistantThoughts(aiName, assistantReply);
        commandName = extractCommandNameFromReply(assistantReply);
        speakCommandName(commandName);

        if (!cfg[ConfigKeys.continuousMode] && nextActionCount == 0) {
          final result = await getUserInputForCommandAuthorization(commandName, aiName);
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
    arguments = commandData[1];
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
    memory!.add(memoryToAdd);

    await console.stdout('SYSTEM:', textColor: Colors.yellow);
    if (cmdResult != null && !cmdResult!.startsWith('Error:')) {
      persona?.addMessageToHistory(createChatMessage('system', result));
      await console.stdout(result, textColor: Colors.white70);
    } else {
      persona?.addMessageToHistory(createChatMessage('system', 'Unable to execute command'));
      await console.stdout('Unable to execute command', textColor: Colors.red);
    }
  }
}