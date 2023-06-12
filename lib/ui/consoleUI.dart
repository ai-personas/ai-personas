import 'dart:async';

import 'package:ai_personas/ui/pattern_renderer.dart';
import 'package:ai_personas/ui/table_renderer.dart';
import 'package:flutter/material.dart';
import '../utils/console.dart';
import 'ascii_rotate.dart';

class ConsoleUI extends StatefulWidget {
  @override
  _ConsoleUIState createState() => _ConsoleUIState();
}

class _ConsoleUIState extends State<ConsoleUI> {
  TextEditingController _inputController = TextEditingController();
  bool _showYesNoButtons = false;
  bool _showUserInput = false;
  bool _showRotate = false;
  ScrollController _scrollController = ScrollController();
  TextSelection? _selection;
  OverlayEntry? _selectionOverlay;
  FocusNode _inputFocusNode = FocusNode();
  FocusNode _yesButtonFocusNode = FocusNode();
  String? _patternText;

  void _stdin() {
    console.userInputComplete(_inputController.text);
    _inputController.clear();
    setState(() {
      _showUserInput = false;
      _showRotate = true;
    });
  }

  @override
  void initState() {
    super.initState();
    console.onYesOrNoCalled = () {
      setState(() {
        _showYesNoButtons = true;
      });
      // Request focus on the Yes button when shown
      WidgetsBinding.instance!.addPostFrameCallback((_) {
        FocusScope.of(context).requestFocus(_yesButtonFocusNode);
      });
    };
    console.onUserInputCalled = () {
      setState(() {
        _showUserInput = true;
      });
    };
    console.onStdoutRendered = () {
      setState(() {
        // Add a small delay to ensure that the new items are added to the list
        // and the scroll position is recalculated
        Future.delayed(Duration(milliseconds: 50), () {
          _scrollToEnd();
        });
      });
    };
    console.onShowRotateCalled = () {
      setState(() {
        _showRotate = true;
      });
    };
    console.onParseTextCalled = () {
      setState(() {
      });
    };
    console.onTableShown = () {
      setState(() {
      });
    };
    console.onButtonAdded = () {
      setState(() {
      });
    };
  }

  void _scrollToEnd() {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
      );
    });
  }

  Widget _buildYesNoButtons() {
    return Row(
      children: [
        ElevatedButton(
          // Assign the focus node to the Yes button
          focusNode: _yesButtonFocusNode,
          onPressed: () {
            console.answerYes();
            setState(() {
              _showYesNoButtons = false;
              _showRotate = true;
            });
          },
          child: const Text('Yes'),
        ),
      ],
    );
  }

  Widget _buildUserInput() {
    return Padding(
      padding: const EdgeInsets.only(top: 8.0),
      child: TextField(
        controller: _inputController,
        focusNode: _inputFocusNode,
        autofocus: true, // Add this line
        style: const TextStyle(color: Colors.green, fontFamily: 'Courier'),
        decoration: const InputDecoration(
          labelText: '',
          labelStyle: TextStyle(color: Colors.green),
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.green),
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.green),
          ),
        ),
        onSubmitted: (value) => _stdin(),
      ),
    );
  }

  Widget _buildAsciiRotate() {
    return AsciiRotate();
  }

  void _handleGroupedAction(Map<String, dynamic> response, int index) {
    console.groupedActionComplete(response);
    setState(() {
      console.output.value.removeAt(index);
      _showUserInput = false; // Update other UI states as needed
      _showRotate = false; // Update other UI states as needed
      // ... Update any other state as needed
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black,
      padding: EdgeInsets.all(8.0),
      child: Column(
        children: [
          Expanded(
            child: ValueListenableBuilder<List<Map<String, dynamic>>>(
              valueListenable: console.output,
              builder: (BuildContext context,
                  List<Map<String, dynamic>> _output, Widget? child) {
                return ListView.builder(
                  controller: _scrollController,
                  itemCount: _output.length +
                      (_showYesNoButtons ? 1 : 0) +
                      (_showUserInput ? 1 : 0) +
                      (_showRotate ? 1 : 0) +
                      (_patternText != null ? 1 : 0), // Add this line
                  itemBuilder: (BuildContext context, int index) {
                    if (_showYesNoButtons && index == _output.length) {
                      return _buildYesNoButtons();
                    }
                    if (_showUserInput && index == _output.length) {
                      return _buildUserInput();
                    }
                    if (_showRotate && index == _output.length) {
                      WidgetsBinding.instance!.addPostFrameCallback((_) {
                        console.asciiRotateRenderComplete();
                      });
                      return _buildAsciiRotate();
                    }
                    if (index <= _output.length && _output[index]['patternText'] != null) {
                      return PatternRenderer(
                        text: _output[index]['patternText'],
                        onInputCompleted: (result) {
                          console.patternTextComplete(result);
                          console.output.value.removeAt(index);
                        },
                      );
                    }
                    if (index <= _output.length && _output[index]['group'] != null) {
                      List<Map<String, dynamic>> group = _output[index]['group'];
                      List<Widget> groupWidgets = [];
                      for (Map<String, dynamic> action in group) {
                        if (action['table'] != null) {
                          groupWidgets.add(
                            TableRenderer(
                              data: action['table'],
                              onRowSelected: (selectedRow) {
                                _handleGroupedAction(selectedRow, index);
                              },
                              onRowDeleted: (Map<String, Map<String, String>> row) {
                              },
                            ),
                          );
                        }
                        if (action['button'] != null) {
                          Map<String, dynamic> buttonData = action['button'];
                          groupWidgets.add(
                            Align(
                              alignment: Alignment.centerLeft,
                              child: ElevatedButton(
                                style: ElevatedButton.styleFrom(
                                  minimumSize: Size(100, 50), // provide the minimum size of the button
                                  textStyle: TextStyle(fontSize: 18), // increase the font size
                                  primary: Colors.green,
                                ),
                                onPressed: () {
                                  _handleGroupedAction(buttonData['returnVal'], index);
                                },
                                child: Text(buttonData['buttonText']),
                              ),
                            ),
                          );
                        }
                      }
                      // Return a single widget that contains all of the widgets for the group.
                      return Column(children: groupWidgets);
                    }
                    if (index < _output.length) {
                      // Call stdoutRenderComplete after rendering the current line
                      WidgetsBinding.instance!.addPostFrameCallback((_) {
                        console.stdoutRenderComplete();
                      });

                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 2.0),
                        child: SelectableText(
                          _output[index]['text'],
                          style: TextStyle(
                              color: _output[index]['color'],
                              fontFamily: 'RobotoMono',
                              fontSize: _output[index]['fontSize'],
                              height: 1.4
                          ),
                        ),
                      );
                    } else {
                      return SizedBox.shrink(); // This should not be reachable
                    }
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

}
