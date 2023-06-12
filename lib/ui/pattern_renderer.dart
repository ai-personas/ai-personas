import 'dart:convert';

import 'package:ai_personas/ui/dropdown.dart';
import 'package:flutter/material.dart';

typedef OnInputCompleted = void Function(Map<String, String> result);

class PatternRenderer extends StatelessWidget {
  final String text;
  Map<String, String> patternSub = {};
  Map<String, String> _userInputs = {};
  final OnInputCompleted onInputCompleted;

  PatternRenderer({required this.text, required this.onInputCompleted});

  List<Widget> _parseText() {
    List<Widget> widgets = [];
    final pattern = RegExp(r'<\{key: ([^,]+), type: ([^,]+), label: ([^,]+)(, options: (\{.*\}))?\}>');
    final matches = pattern.allMatches(text);

    int lastIndex = 0;

    for (final match in matches) {
      // Add text before the pattern
      widgets.add(Text(text.substring(lastIndex, match.start),
        style: const TextStyle(color: Colors.white70, fontFamily: 'RobotoMono', fontSize: 18), ));

      // Process the pattern
      final entirePattern = match.group(0);
      final key = match.group(1);
      final type = match.group(2);
      final label = match.group(3);

      switch (type) {
        case 'input':
          _userInputs[key!] = '';
          widgets.add(_buildInput(key!, label!, entirePattern!));
          break;
        case 'list':
          _userInputs[key!] = '';
          widgets.add(_buildList(key!, label!, entirePattern!));
          break;
        case 'select':
          final options = match.group(5);
          Map<String, String>? optionsMap;
          optionsMap = (jsonDecode(options!) as Map<String, dynamic>).map(
                  (key, value) => MapEntry(key, value.toString())
          );
          patternSub[entirePattern!] = '';
          widgets.add(_buildSelect(key!, label!, entirePattern!, optionsMap));
          break;
        case 'button':
          widgets.add(_buildButton(label!));
          patternSub[entirePattern!] = '';
          break;
        case 'title':
          widgets.add(_buildTitle(label!));
          patternSub[entirePattern!] = '';
          break;
      }

      lastIndex = match.end;
    }

    widgets.add(Text(
      text.substring(lastIndex),
      style: const TextStyle(color: Colors.white70, fontFamily: 'RobotoMono', fontSize: 18),
    ));

    return widgets;
  }

  Widget _buildTitle(String titleText) {
    return Text(
      titleText,
      style: const TextStyle(
        fontSize: 24, // Adjust the font size as needed
        color: Colors.yellow,
        fontFamily: 'RobotoMono',
      ),
    );
  }

  ValueNotifier<String> _validationErrorNotifier = ValueNotifier('');

  Widget _buildButton(String label) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ValueListenableBuilder(
          valueListenable: _validationErrorNotifier,
          builder: (context, String value, child) {
            return value.isNotEmpty
                ? Text(
              value,
              style: const TextStyle(
                color: Colors.red,
                fontFamily: 'RobotoMono',
                fontSize: 18,
              ),
            )
                : Container(); // Display an empty container when there's no error
          },
        ),
        const SizedBox(height: 10), // Add a SizedBox to give a fixed amount of space
        Container(
          alignment: Alignment.centerLeft,
          child: ElevatedButton(
            onPressed: () {
              _validationErrorNotifier.value = '';

              for (final key in _userInputs.keys) {
                if (_userInputs[key]!.trim().isEmpty) {
                  _validationErrorNotifier.value = 'Please fill out Persona Name, Role and Goals.';
                  return;
                }
              }

              if (_validationErrorNotifier.value.isEmpty) {
                String finalText = _generateFinalText(text);
                _userInputs['finalText'] = finalText;
                onInputCompleted(_userInputs);
              }
            },
            child: Text(
              label,
              style: const TextStyle(
                color: Colors.black,
              ),
            ),
            style: ElevatedButton.styleFrom(
              minimumSize: Size(100, 50),
              textStyle: TextStyle(fontSize: 20),
              primary: Colors.yellow,
            ),
          ),
        ),
      ],
    );
  }

  String _generateFinalText(String text) {
    String finalText = text;
    patternSub.forEach((key, value) {
      finalText = finalText.replaceAll(key, value);
    });
    return finalText;
  }

  Widget _buildInput(String key, String placeholder, String entirePattern) {
    return _EditableInput(
      patternKey: key,
      placeholder: placeholder,
      entirePattern: entirePattern,
      onSaved: (entirePattern, input) {
        patternSub[entirePattern] = input;
        _userInputs[key] = input;
      },
    );
  }

  Widget _buildList(String key, String placeholder, String entirePattern) {
    return EditableList(
      patternKey: key,
      placeholder: placeholder,
      entirePattern: entirePattern,
      onSaved: (entirePattern, input) {
        patternSub[entirePattern] = input;
        _userInputs[key] = input;
      },
    );
  }

  Widget _buildSelect(String key, String label, String pattern, Map<String, String>? options) {
    return MultiSelectDropdown(
      patternKey: key,
      options: options!,
      entirePattern: pattern,
      onSaved: (selectedPattern, selectedOptions) {
        patternSub[selectedPattern] = selectedOptions.values.join('\n');
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: _parseText(),
      ),
    );
  }
}

class _EditableInput extends StatefulWidget {
  final String patternKey;
  final String placeholder;
  final String entirePattern;
  final Function(String, String) onSaved;

  _EditableInput({required this.patternKey, required this.placeholder, required this.entirePattern, required this.onSaved});

  @override
  __EditableInputState createState() => __EditableInputState();
}

class __EditableInputState extends State<_EditableInput> {
  TextEditingController _controller = TextEditingController();
  bool _isEditing = true;

  void _toggleEditing() {
    setState(() {
      _isEditing = !_isEditing;
      if (!_isEditing) {
        widget.onSaved(widget.entirePattern, _controller.text);
      }
    });
  }

  bool isValidInput() {
    return _controller.text.isNotEmpty;
  }

  @override
  Widget build(BuildContext context) {
    if (_isEditing) {
      return Row(
        children: [
          Expanded(
            child: TextFormField(
              controller: _controller,
              onFieldSubmitted: (value) {
                _toggleEditing();
              },
              style: const TextStyle(color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18),
              decoration: InputDecoration(
                hintText: widget.placeholder,
                hintStyle: const TextStyle(color: Colors.green),
                enabledBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.green),
                ),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.green),
                ),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.save, color: Colors.green),
            onPressed: _toggleEditing,
            tooltip: "Click to save",
          ),
        ],
      );
    } else {
      return Row(
        children: [
          Expanded(
            child: Text(
              _controller.text,
              softWrap: true,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.edit, color: Colors.green),
            onPressed: _toggleEditing,
          ),
        ],
      );
    }
  }
}

class EditableList extends StatefulWidget {
  final String patternKey;
  final String placeholder;
  final String entirePattern;
  final Function(String, String) onSaved;

  EditableList({required this.patternKey, required this.placeholder, required this.entirePattern, required this.onSaved});

  @override
  _EditableListState createState() => _EditableListState();
}

class _EditableListState extends State<EditableList> {
  List<String> _items = [];
  TextEditingController _controller = TextEditingController();
  int? _editingIndex;

  void _addItem(String item) {
    setState(() {
      _items.add('${_items.length + 1}. $item');
      widget.onSaved(widget.entirePattern, _items.join('\n'));
    });
  }

  void _updateItem(int index, String newItem) {
    setState(() {
      _items[index] = '${index + 1}. $newItem';
      widget.onSaved(widget.entirePattern, _items.join('\n'));
    });
  }

  void _deleteItem(int index) {
    setState(() {
      _items.removeAt(index);
      for (int i = index; i < _items.length; i++) {
        var splits = _items[i].split('. ');
        if (splits.length > 1) {
          _items[i] = '${i + 1}. ${splits.sublist(1).join('. ')}';
        }
      }
      widget.onSaved(widget.entirePattern, _items.join('\n'));
    });
  }

  void _toggleEditing([int? index]) {
    setState(() {
      if (_editingIndex == index) {
        _editingIndex = null;
      } else {
        _editingIndex = index;
        _controller.text = index != null ? _items[index].split('. ')[1] : '';
      }
    });
  }

  bool isValidInput() {
    return _items.isNotEmpty;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        for (int i = 0; i < _items.length; i++)
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: _editingIndex == i
                    ? TextFormField(
                  controller: _controller,
                  onFieldSubmitted: (value) {
                    _updateItem(i, value);
                    _toggleEditing();
                  },
                  style: TextStyle(color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18),
                  decoration: InputDecoration(
                    hintText: widget.placeholder,
                    hintStyle: TextStyle(color: Colors.green),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.green),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.green),
                    ),
                  ),
                )
                    : Padding(
                  padding: const EdgeInsets.symmetric(vertical: 10.0),
                  child: RichText(
                    text: TextSpan(
                      style: DefaultTextStyle.of(context).style,
                      children: <TextSpan>[
                        TextSpan(
                          text: _items[i],
                          style: const TextStyle(
                            color: Colors.green,
                            fontFamily: 'RobotoMono',
                            fontSize: 18,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              IconButton(
                icon: Icon(_editingIndex == i ? Icons.done : Icons.edit, color: Colors.green),
                onPressed: () => _toggleEditing(i),
              ),
              IconButton(
                icon: Icon(Icons.delete, color: Colors.red),
                onPressed: () => _deleteItem(i),
              ),
            ],
          ),
        if (_editingIndex == null && _items.isNotEmpty) // Add button when there are items and no input field active
          Row(
            children: [
              ElevatedButton(
                child: Text('Add More Goals'),
                onPressed: () {
                  _addItem('');
                  _toggleEditing(_items.length - 1);
                },
              ),
            ],
          ),
        if (_editingIndex == null && _items.isEmpty) // Display input field when list is empty
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  controller: _controller,
                  onFieldSubmitted: (value) {
                    _addItem(value);
                    _controller.clear();
                  },
                  style: TextStyle(color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18),
                  decoration: InputDecoration(
                    hintText: widget.placeholder,
                    hintStyle: TextStyle(color: Colors.green),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.green),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.green),
                    ),
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.save, color: Colors.green),
                onPressed: () {
                  _addItem(_controller.text);
                  _controller.clear();
                },
                tooltip: "Click to save",
              ),
            ],
          ),
      ],
    );
  }
}

