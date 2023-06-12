import 'package:flutter/material.dart';

class MultiSelectDropdown extends StatefulWidget {
  final String patternKey;
  final Map<String, String> options;
  final String entirePattern;
  final Function(String, Map<String, String>) onSaved;

  MultiSelectDropdown({required this.patternKey, required this.options, required this.entirePattern, required this.onSaved});

  @override
  _MultiSelectDropdownState createState() => _MultiSelectDropdownState();
}

class _MultiSelectDropdownState extends State<MultiSelectDropdown> {
  Map<String, String> _availableOptions = {};
  Map<String, String> _selectedOptions = {};

  @override
  void initState() {
    super.initState();
    _availableOptions = {...widget.options};
  }

  void _onOptionSelected(String? selectedKey) {
    setState(() {
      if (selectedKey != null) {
        _selectedOptions[selectedKey] = '${_selectedOptions.length + 3}. ${_availableOptions[selectedKey]!}';
        _availableOptions.remove(selectedKey);
      }
    });
    widget.onSaved(widget.entirePattern, _selectedOptions);
  }

  void _onOptionRemoved(String optionKey) {
    setState(() {
      _selectedOptions.remove(optionKey);
      _availableOptions[optionKey] = widget.options[optionKey]!;
    });
    widget.onSaved(widget.entirePattern, _selectedOptions);
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData(
        popupMenuTheme: PopupMenuThemeData(
          color: Colors.black,
          shape: RoundedRectangleBorder(
            side: BorderSide(color: Colors.green, width: 1.0),
            borderRadius: BorderRadius.circular(4.0),
          ),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ..._selectedOptions.entries.map((option) {
            var index = _selectedOptions.keys.toList().indexOf(option.key) + 1;
            return Row(
              children: [
                Flexible(
                  child: Text(
                    option.value,
                    style: TextStyle(color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18.0),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.delete, color: Colors.red, size: 16.0),
                  onPressed: () => _onOptionRemoved(option.key),
                ),
              ],
            );
          }).toList(),
          if (_availableOptions.isNotEmpty)
            DropdownButton<String>(
              items: _availableOptions.keys.map((key) {
                return DropdownMenuItem(
                  child: Container(
                    padding: EdgeInsets.symmetric(vertical: 4.0, horizontal: 8.0),
                    decoration: BoxDecoration(
                      border: Border(
                        bottom: BorderSide(color: Colors.green.withOpacity(0.5), width: 0.5),
                      ),
                    ),
                    child: Text(
                      key,
                      style: TextStyle(color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18.0),
                    ),
                  ),
                  value: key,
                );
              }).toList(),
              hint: Text(
                'Select option',
                style: TextStyle(color: Colors.green, fontFamily: 'RobotoMono', fontSize: 18.0),
              ),
              onChanged: _onOptionSelected,
              dropdownColor: Colors.black,
            ),
        ],
      ),
    );
  }

}
