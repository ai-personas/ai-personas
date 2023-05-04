import 'dart:async';

import 'package:flutter/material.dart';

import '../json_fixes/parsing.dart';

class Console extends ChangeNotifier {
  Console._internal();
  static final Console _instance = Console._internal();
  ValueNotifier<List<Map<String, dynamic>>> _output = ValueNotifier([]);

  ValueNotifier<List<Map<String, dynamic>>> get output => _output;

  Completer<void> _stdoutRenderedCompleter = Completer<void>();
  VoidCallback? _onStdoutRendered;

  void stdin(String input, {Color textColor = Colors.white}) {
    stdout(input, textColor: textColor);
  }

  set onStdoutRendered(VoidCallback? callback) {
    _onStdoutRendered = callback;
  }

  Future<void> stdout(String message, {Color textColor = Colors.white}) async {
    if (message.contains('\r')) {
      // Handle the carriage return (\r) character.
      List<String> parts = message.split('\r');
      for (int i = 0; i < parts.length; i++) {
        if (i == 0) {
          _output.value = List.from(_output.value)
            ..add({'text': parts[i], 'color': textColor});
        } else {
          _output.value = List.from(_output.value)
            ..[_output.value.length - 1] = {'text': parts[i], 'color': textColor};
        }
      }
    } else {
      _output.value = List.from(_output.value)
        ..add({'text': message, 'color': textColor});
    }
    _onStdoutRendered?.call();
    await _stdoutRenderedCompleter.future;
    _stdoutRenderedCompleter = Completer<void>();
    await showAsciiRotate();
  }

  void stdoutRenderComplete() {
    if (!_stdoutRenderedCompleter.isCompleted) {
      _stdoutRenderedCompleter.complete();
    }
  }

  Future<Map<String, dynamic>> printAssistantThoughts(String aiName, String assistantReply) async {
    Map<String, dynamic> assistantReplyJson = {};

    try {
      assistantReplyJson = JsonFixer.fixAndParseJson(assistantReply);
    } catch (e) {
      await stdout("Error: Invalid JSON in assistant thoughts\n", textColor: Colors.red);
      await stdout(assistantReply, textColor: Colors.red);
      // Note: attempt_to_fix_json_by_finding_outermost_brackets and fix_and_parse_json
      // functions are not implemented here.
      return assistantReplyJson;
    }

    Map<String, dynamic> assistantThoughts = assistantReplyJson['thoughts'] ?? {};
    String assistantThoughtsText = assistantThoughts['text'] ?? '';
    String assistantThoughtsReasoning = assistantThoughts['reasoning'] ?? '';
    dynamic assistantThoughtsPlan = assistantThoughts['plan'];
    String assistantThoughtsCriticism = assistantThoughts['criticism'] ?? '';
    String assistantThoughtsSpeak = assistantThoughts['speak'] ?? '';

    String divider = '----------------------------------------';
    await stdout(divider, textColor: Colors.blue);

    await stdout('${aiName.toUpperCase()} THOUGHTS:', textColor: Colors.yellow);
    await stdout(assistantThoughtsText, textColor: Colors.white70);
    await stdout('REASONING:', textColor: Colors.yellow);
    await stdout(assistantThoughtsReasoning, textColor: Colors.white70);

    if (assistantThoughtsPlan != null) {
      await stdout('PLAN:', textColor: Colors.yellow);

      if (assistantThoughtsPlan is List) {
        assistantThoughtsPlan = assistantThoughtsPlan.join('\n');
      } else if (assistantThoughtsPlan is Map) {
        assistantThoughtsPlan = assistantThoughtsPlan.toString();
      }

      List<String> lines = assistantThoughtsPlan.split('\n');
      for (String line in lines) {
        line = line.trimLeft().replaceAll(RegExp(r'^-'), '').trim();
        await stdout('- $line', textColor: Colors.green);
      }
    }

    await stdout('CRITICISM:', textColor: Colors.yellow);
    await stdout(assistantThoughtsCriticism, textColor: Colors.white70);
    await stdout('SPEAK:', textColor: Colors.yellow);
    await stdout(assistantThoughtsSpeak, textColor: Colors.white70);

    return assistantReplyJson;
  }

  Completer<String> _yesOrNoCompleter = Completer<String>();
  VoidCallback? _onYesOrNoCalled;

  Future<String> yesOrNo(String message, {Color textColor=Colors.yellow}) {
    stdout(message, textColor: textColor);
    _onYesOrNoCalled?.call();
    return _yesOrNoCompleter.future.then((result) {
      stdout(result, textColor: Colors.green);
      return result;
    });
  }

  set onYesOrNoCalled(VoidCallback? callback) {
    _onYesOrNoCalled = callback;
  }

  void answerYes() {
    _yesOrNoCompleter.complete('yes');
    _yesOrNoCompleter = Completer<String>();
  }

  void answerNo() {
    _yesOrNoCompleter.complete('no');
    _yesOrNoCompleter = Completer<String>();
  }

  Completer<String> _userInputCompleter = Completer<String>();
  VoidCallback? _onUserInputCalled;

  set onUserInputCalled(VoidCallback? callback) {
    _onUserInputCalled = callback;
  }

  Future<String> getUserInput(String message, {Color textColor = Colors.yellow, bool displayInput = true}) {
    stdout(message, textColor: textColor);
    _onUserInputCalled?.call();
    return _userInputCompleter.future.then((result) {
      if (displayInput) {
        stdout(result, textColor: Colors.green);
      }
      return result;
    });
  }

  void userInputComplete(String input) {
    stdout(input, textColor: Colors.green);
    _userInputCompleter.complete(input);
    _userInputCompleter = Completer<String>();
  }

  Future<String> getSecret(String beforeMsg, String afterMsg, {Color textColor = Colors.yellow}) {
    return getUserInput(beforeMsg, displayInput: false).then((input) {
      stdout(afterMsg, textColor: Colors.cyan);
      return input;
    });
  }

  Completer<void> _showRotateCompleter = Completer<void>();
  VoidCallback? _onShowRotateCalled;

  set onShowRotateCalled(VoidCallback? callback) {
    _onShowRotateCalled = callback;
  }

  Future<void> showAsciiRotate() async {
    _onShowRotateCalled?.call();
    await _showRotateCompleter.future;
  }

  void asciiRotateRenderComplete() {
    if (!_showRotateCompleter.isCompleted) {
      _showRotateCompleter.complete();
      _showRotateCompleter = Completer<void>();
    }
  }
}

final Console console = Console._internal();
