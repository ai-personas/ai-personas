// import 'package:flutter/gestures.dart';
// import 'package:flutter/material.dart';
// import '../utils/console.dart';
// import 'asciiRotate.dart';
// import 'dart:ui';
//
// class ConsoleUI extends StatefulWidget {
//   @override
//   _ConsoleUIState createState() => _ConsoleUIState();
// }
//
// class _ConsoleUIState extends State<ConsoleUI> {
//   TextEditingController _inputController = TextEditingController();
//   bool _showYesNoButtons = false;
//   bool _showUserInput = false;
//   bool _showRotate = false;
//   ScrollController _scrollController = ScrollController();
//   TextSelection? _selection;
//   OverlayEntry? _selectionOverlay;
//
//   void _stdin() {
//     console.userInputComplete(_inputController.text);
//     _inputController.clear();
//     setState(() {
//       _showUserInput = false;
//       _showRotate = true;
//     });
//   }
//
//   @override
//   void initState() {
//     super.initState();
//     console.onYesOrNoCalled = () {
//       setState(() {
//         _showYesNoButtons = true;
//       });
//     };
//     console.onUserInputCalled = () {
//       setState(() {
//         _showUserInput = true;
//       });
//     };
//     console.onStdoutRendered = () {
//       setState(() {
//         // Add a small delay to ensure that the new items are added to the list
//         // and the scroll position is recalculated
//         Future.delayed(Duration(milliseconds: 50), () {
//           _scrollToEnd();
//         });
//       });
//     };
//     console.onShowRotateCalled = () {
//       setState(() {
//         _showRotate = true;
//       });
//     };
//   }
//
//   void _scrollToEnd() {
//     WidgetsBinding.instance!.addPostFrameCallback((_) {
//       _scrollController.animateTo(
//         _scrollController.position.maxScrollExtent,
//         duration: Duration(milliseconds: 200),
//         curve: Curves.easeOut,
//       );
//     });
//   }
//
//   Widget _buildYesNoButtons() {
//     return Row(
//       children: [
//         ElevatedButton(
//           onPressed: () {
//             console.answerYes();
//             setState(() {
//               _showYesNoButtons = false;
//               _showRotate = true;
//             });
//           },
//           child: Text('Yes'),
//         ),
//         SizedBox(width: 8),
//         ElevatedButton(
//           onPressed: () {
//             console.answerNo();
//             setState(() {
//               _showYesNoButtons = false;
//               _showRotate = true;
//             });
//           },
//           child: Text('No'),
//         ),
//       ],
//     );
//   }
//
//   Widget _buildUserInput() {
//     return Padding(
//       padding: const EdgeInsets.only(top: 8.0),
//       child: TextField(
//         controller: _inputController,
//         style: TextStyle(color: Colors.green, fontFamily: 'Courier'),
//         decoration: InputDecoration(
//           labelText: '',
//           labelStyle: TextStyle(color: Colors.green),
//           enabledBorder: OutlineInputBorder(
//             borderSide: BorderSide(color: Colors.green),
//           ),
//           focusedBorder: OutlineInputBorder(
//             borderSide: BorderSide(color: Colors.green),
//           ),
//         ),
//         onSubmitted: (value) => _stdin(),
//       ),
//     );
//   }
//
//   Widget _buildAsciiRotate() {
//     return AsciiRotate();
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return Container(
//       color: Colors.black,
//       padding: EdgeInsets.all(8.0),
//       child: Column(
//         children: [
//           Expanded(
//             child: ValueListenableBuilder<List<Map<String, dynamic>>>(
//               valueListenable: console.output,
//               builder: (BuildContext context,
//                   List<Map<String, dynamic>> _output, Widget? child) {
//                 return RawScrollbar(
//                   controller: _scrollController,
//                   isAlwaysShown: true,
//                   thumbColor: Colors.grey,
//                   radius: Radius.circular(3),
//                   thickness: 8.0,
//                   child: ListView.builder(
//                     controller: _scrollController,
//                     itemCount: _output.length +
//                         (_showYesNoButtons ? 1 : 0) +
//                         (_showUserInput ? 1 : 0) +
//                         (_showRotate ? 1 : 0),
//                     itemBuilder: (BuildContext context, int index) {
//                       if (_showYesNoButtons && index == _output.length) {
//                         return _buildYesNoButtons();
//                       }
//                       if (_showUserInput && index == _output.length) {
//                         return _buildUserInput();
//                       }
//                       if (_showRotate && index == _output.length) {
//                         WidgetsBinding.instance!.addPostFrameCallback((_) {
//                           console.asciiRotateRenderComplete();
//                         });
//                         return _buildAsciiRotate();
//                       }
//
//                       if (index < _output.length) {
//                         // Call stdoutRenderComplete after rendering the current line
//                         WidgetsBinding.instance!.addPostFrameCallback((_) {
//                           console.stdoutRenderComplete();
//                         });
//
//                         return Padding(
//                           padding: const EdgeInsets.symmetric(vertical: 2.0),
//                           child: SelectableText(
//                             _output[index]['text'],
//                             style: TextStyle(
//                               color: _output[index]['color'],
//                               fontFamily: 'RobotoMono',
//                               fontSize: 18,
//                               height: 1.4
//                             ),
//                           ),
//                         );
//                       } else {
//                         return SizedBox.shrink();
//                       }
//
//                     },
//                   ),
//                 );
//               },
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import '../utils/console.dart';
import 'asciiRotate.dart';
import 'dart:ui';

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
  }

  void _scrollToEnd() {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: Duration(milliseconds: 200),
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
          child: Text('Yes'),
        ),
        SizedBox(width: 8),
        ElevatedButton(
          onPressed: () {
            console.answerNo();
            setState(() {
              _showYesNoButtons = false;
              _showRotate = true;
            });
          },
          child: Text('No'),
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
        style: TextStyle(color: Colors.green, fontFamily: 'Courier'),
        decoration: InputDecoration(
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
                      (_showRotate ? 1 : 0),
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
                              fontSize: 18,
                              height: 1.4
                          ),
                        ),
                      );
                    } else {
                      return SizedBox.shrink();
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
