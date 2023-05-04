import 'package:tuple/tuple.dart';
import 'config/AppConfig.dart';
import 'config/ConfigKeys.dart';
import 'persona/persona.dart';
import 'package:ai_personas/prompt_generator.dart';
import 'package:ai_personas/utils/console.dart';
import 'package:flutter/material.dart';
import 'package:ai_personas/persona_setup.dart';

String getPrompt() {

  // Initialize the PromptGenerator object
  final promptGenerator = PromptGenerator();

  // Add constraints to the PromptGenerator object
  promptGenerator.addConstraint(
      '~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.');
  promptGenerator.addConstraint(
      'If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.');
  promptGenerator.addConstraint('No user assistance');
  promptGenerator.addConstraint(
      'Exclusively use the commands listed in double quotes e.g. "command name"');
  promptGenerator.addConstraint(
      'Use subprocesses for commands that will not terminate within a few minutes');

  // Define the command list
  List<Tuple3<String, String, Map<String, String>>> commands = [
    const Tuple3('Google Search', 'google', {'input': '<search>'}),
    const Tuple3('Browse Website', 'browse_website',
    {'url': '<url>', 'question': '<what_you_want_to_find_on_website>'}),
    const Tuple3('Task Complete (Shutdown)', 'task_complete',
    {'reason': '<reason>'}),
    const Tuple3('Do Nothing', 'do_nothing', {}),
  ];

  // Add commands to the PromptGenerator object
  for (final command in commands) {
    promptGenerator.addCommand(command.item1, command.item2, command.item3);
  }

  // Add resources to the PromptGenerator object
  promptGenerator.addResource(
      'Internet access for searches and information gathering.');
  promptGenerator.addResource(
      'GPT-3.5 powered AiPersonas for delegation of simple tasks.');

  // Add performance evaluations to the PromptGenerator object
  promptGenerator.addPerformanceEvaluation(
      'Continuously review and analyze your actions to ensure you are performing to the best of your abilities.');
  promptGenerator.addPerformanceEvaluation(
      'Constructively self-criticize your big-picture behavior constantly.');
  promptGenerator.addPerformanceEvaluation(
      'Reflect on past decisions and strategies to refine your approach.');
  promptGenerator.addPerformanceEvaluation(
      'Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.');

  // Generate the prompt string
  return promptGenerator.generatePromptString();
}

Future<String> constructPrompt() async {
  Persona persona = await Persona.getPersona;
  if (persona.name != '') {
    await console.stdout('Welcome back! Would you like me to return to being ${persona.name}?', textColor: Colors.green);
    String userRes = await console.yesOrNo(
        'Continue with the last settings?\nName:  ${persona.name}\nRole:  ${persona.role}\nGoals: ${persona.goals}\nContinue (y/n): ');

    if (userRes.toLowerCase() == 'yes') {
      for (var message in persona.fullMessageHistory) {
        if (message['role'] == 'assistant') {
          String assistantContent = message['content'];
          await console.printAssistantThoughts(persona.name, assistantContent);
        }
      }
    } else {
      persona = Persona();
    }
  }

  if (persona.name == '') {
    persona = await promptUser();
    persona.save();
  }

  String promptStart =
      'Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications.';

  String fullPrompt =
      'You are ${persona.name}, ${persona.role}\n$promptStart\n\nGOALS:\n\n';

  for (int i = 0; i < persona.goals.length; i++) {
    fullPrompt += '${i + 1}. ${persona.goals[i]}\n';
  }

  fullPrompt += '\n\n${getPrompt()}';

  return fullPrompt;
}

