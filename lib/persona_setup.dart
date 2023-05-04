import 'package:flutter/material.dart';

import 'persona/persona.dart';
import 'utils/console.dart';

Future<Persona> promptUser() async {
  String personaName = "";
  // Construct the prompt
  await console.stdout("Welcome to AiPersonas!", textColor: Colors.green);

  await console.stdout("Create an Ai Persona:", textColor: Colors.green);
  await console.stdout("Enter the name of your Persona and its role below. Entering nothing will load defaults.", textColor: Colors.green);

  await console.stdout("Name your Persona: (For example, 'Electronica')", textColor: Colors.green);

  personaName = await console.getUserInput("Persona Name: ");
  if (personaName.isEmpty) {
    personaName = "Electronica";
  }

  await console.stdout(personaName + " here!", textColor: Colors.green);

  // Get AI Role from User
  await console.stdout("Describe your Ai Persona's role: ", textColor: Colors.green);
  await console.stdout("For example, 'an persona 'Electronica' designed to autonomously develop and run businesses with the sole goal of increasing your net worth.'", textColor: Colors.green);

  String aiRole = await console.getUserInput("$personaName is: ");
  if (aiRole.isEmpty) {
    aiRole =
    "an AI designed to autonomously develop and run businesses with the sole goal of increasing your net worth.";
  }

  await console.stdout("Enter up to 5 goals for your Ai Persona: ", textColor: Colors.green);
  await console.stdout("For example: \nIncrease net worth, Grow Twitter Account, Develop and manage multiple businesses autonomously'", textColor: Colors.green);

  List<String> aiGoals = [];
  for (int i = 0; i < 5; i++) {
    String aiGoal = await console.getUserInput("Goal ${i + 1}: ");
    if (aiGoal.isEmpty) {
      break;
    }
    aiGoals.add(aiGoal);
  }
  if (aiGoals.isEmpty) {
    aiGoals = [
      "Increase net worth",
      "Grow Twitter Account",
      "Develop and manage multiple businesses autonomously",
    ];
  }

  return Persona(name: personaName, role: aiRole, aiGoals: aiGoals);
}
