import 'dart:convert';

class PromptGenerator {
  List<String> constraints = [];
  List<Map<String, dynamic>> commands = [];
  List<String> resources = [];
  List<String> performanceEvaluation = [];
  Map<String, dynamic> responseFormat = {
    'thoughts': {
      'text': 'thought',
      'reasoning': 'reasoning',
      'plan': '- short bulleted\n- list that conveys\n- long-term plan',
      'criticism': 'constructive self-criticism',
      'speak': 'thoughts summary to say to user',
    },
    'command': {
      'name': 'command name',
      'args': {'arg name': 'value'}
    },
  };

  void addConstraint(String constraint) {
    constraints.add(constraint);
  }

  void addCommand(String commandLabel, String commandName, [Map<String, String>? args]) {
    if (args == null) {
      args = {};
    }

    Map<String, String> commandArgs = {for (var entry in args.entries) entry.key: entry.value};

    Map<String, dynamic> command = {
      'label': commandLabel,
      'name': commandName,
      'args': commandArgs,
    };

    commands.add(command);
  }

  String _generateCommandString(Map<String, dynamic> command) {
    String argsString = command['args'].entries.map((entry) => '"${entry.key}": "${entry.value}"').join(', ');
    return '${command["label"]}: "${command["name"]}", args: $argsString';
  }

  void addResource(String resource) {
    resources.add(resource);
  }

  void addPerformanceEvaluation(String evaluation) {
    performanceEvaluation.add(evaluation);
  }

  String _generateNumberedList(List<dynamic> items, [String itemType = 'list']) {
    if (itemType == 'command') {
      return List<String>.generate(items.length, (i) => '${i + 1}. ${_generateCommandString(items[i])}').join('\n');
    } else {
      return List<String>.generate(items.length, (i) => '${i + 1}. ${items[i]}').join('\n');
    }
  }

  String generatePromptString() {
    String formattedResponseFormat = JsonEncoder.withIndent('    ').convert(responseFormat);
    return 'Constraints:\n${_generateNumberedList(constraints)}\n\n'
        'Commands:\n${_generateNumberedList(commands, 'command')}\n\n'
        'Resources:\n${_generateNumberedList(resources)}\n\n'
        'Performance Evaluation:\n${_generateNumberedList(performanceEvaluation)}\n\n'
        'You should only respond in JSON format as described below \nResponse'
        ' Format: \n$formattedResponseFormat \nEnsure the response can be'
        ' parsed by Dart jsonDecode';
  }
}
