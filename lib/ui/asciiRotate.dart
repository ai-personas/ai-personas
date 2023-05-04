import 'package:flutter/material.dart';

class AsciiRotate extends StatefulWidget {
  @override
  _AsciiRotateState createState() => _AsciiRotateState();
}

class _AsciiRotateState extends State<AsciiRotate> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<String> _characters = ['-', '\\', '|', '/'];

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (BuildContext context, Widget? child) {
        int _currentCharacterIndex =
        ((_controller.value * _characters.length) % _characters.length).floor();
        return Text(
          _characters[_currentCharacterIndex],
          style: const TextStyle(color: Colors.white, fontFamily: 'RobotoMono', fontSize: 16),
        );
      },
    );
  }
}
