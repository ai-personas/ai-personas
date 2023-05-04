// import 'package:flutter/material.dart';
// import 'package:shared_preferences/shared_preferences.dart';
// import 'package:ai_personas/config/AppConfig.dart';
//
// class ConfigPage extends StatefulWidget {
//   @override
//   _ConfigPageState createState() => _ConfigPageState();
// }
//
// class _ConfigPageState extends State<ConfigPage> {
//   List<String> displayedKeys = [
//     'continuousMode',
//     'continuousLimit',
//     'fastLLMModel',
//     'smartLLMModel',
//     'openaiApiKey',
//     'temperature',
//     'googleApiKey',
//     'customSearchEngineId',
//     'memoryBackend',
//   ];
//
//   Map<String, String> descriptions = {
//     'continuousMode': 'Continuous mode',
//     'continuousLimit': 'Limit for continuous mode',
//     'fastLLMModel': 'Fast LLM model',
//     'smartLLMModel': 'Smart LLM model',
//     'openaiApiKey': 'Enter your OpenAI API key',
//     'temperature': 'Adjust the randomness of generated text',
//     'googleApiKey': 'Enter your Google API key',
//     'customSearchEngineId': 'Enter your custom search engine ID',
//     'memoryBackend': 'Choose the memory backend'
//   };
//
//   Map<String, List<String>> dropdownItems = {
//     'fastLLMModel': ['gpt-3.5-turbo'],
//     'smartLLMModel': ['gpt-4'],
//     'memoryBackend': ['local'],
//   };
//
//   @override
//   void initState() {
//     super.initState();
//     AppConfig.loadConfig().then((_) {
//       setState(() {
//         // No specific change in the state, but this will trigger a rebuild.
//       });
//     });
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return Theme(
//       data: ThemeData(
//         brightness: Brightness.dark,
//       ),
//       child: Scaffold(
//         appBar: AppBar(
//           title: Text('Configuration'),
//           backgroundColor: Colors.black,
//         ),
//         body: SafeArea(
//           child: ListView.builder(
//             itemCount: displayedKeys.length,
//             itemBuilder: (BuildContext context, int index) {
//               String key = displayedKeys[index];
//               dynamic value = AppConfig.config[key];
//               String? description = descriptions[key];
//
//               return Column(
//                 crossAxisAlignment: CrossAxisAlignment.start,
//                 children: [
//                   ListTile(
//                     title: Text(
//                       description != null ? description : key,
//                       style:
//                           TextStyle(fontWeight: FontWeight.w400, fontSize: 20),
//                     ),
//                   ),
//                   if (value is bool)
//                     SwitchListTile(
//                       value: value,
//                       onChanged: (bool newValue) async {
//                         setState(() {
//                           AppConfig.config[key] = newValue;
//                         });
//                         await AppConfig.saveConfig(key);
//                       },
//                     )
//                   else if (value is int || value is double)
//                     TextFormFieldWidget(
//                       initialValue: value.toString(),
//                       keyboardType: TextInputType.numberWithOptions(
//                           decimal: value is double),
//                       onSaved: (String newValue) async {
//                         setState(() {
//                           if (value is int) {
//                             AppConfig.config[key] =
//                                 int.tryParse(newValue) ?? value;
//                           } else {
//                             AppConfig.config[key] =
//                                 double.tryParse(newValue) ?? value;
//                           }
//                         });
//                         await AppConfig.saveConfig(key);
//                       },
//                     )
//                   else if (dropdownItems.containsKey(key))
//                     DropdownFieldWidget(
//                       initialValue: value.toString(),
//                       items: dropdownItems[key]!,
//                       onChanged: (String newValue) async {
//                         setState(() {
//                           AppConfig.config[key] = newValue;
//                         });
//                         await AppConfig.saveConfig(key);
//                       },
//                     )
//                   else
//                     TextFormFieldWidget(
//                       initialValue: value.toString(),
//                       keyboardType: TextInputType.text,
//                       onSaved: (String newValue) async {
//                         setState(() {
//                           AppConfig.config[key] = newValue;
//                         });
//                         await AppConfig.saveConfig(key);
//                       },
//                     ),
//                   Divider(),
//                 ],
//               );
//             },
//           ),
//         ),
//       ),
//     );
//   }
// }
//
// class TextFormFieldWidget extends StatefulWidget {
//   final String initialValue;
//   final TextInputType keyboardType;
//   final Function(String) onSaved;
//
//   TextFormFieldWidget(
//       {required this.initialValue,
//       required this.keyboardType,
//       required this.onSaved});
//
//   @override
//   _TextFormFieldWidgetState createState() => _TextFormFieldWidgetState();
// }
//
// class _TextFormFieldWidgetState extends State<TextFormFieldWidget> {
//   final _formKey = GlobalKey<FormState>();
//
//   @override
//   Widget build(BuildContext context) {
//     return Form(
//       key: _formKey,
//       child: ListTile(
//         subtitle: TextFormField(
//           initialValue: widget.initialValue,
//           keyboardType: widget.keyboardType,
//           onFieldSubmitted: (value) {
//             if (_formKey.currentState!.validate()) {
//               _formKey.currentState!.save();
//             }
//           },
//           validator: (value) {
//             if (widget.keyboardType ==
//                     TextInputType.numberWithOptions(decimal: false) &&
//                 value != null &&
//                 int.tryParse(value) == null) {
//               return 'Please enter a valid integer';
//             }
//             return null;
//           },
//           onSaved: (value) {
//             if (value != null) {
//               widget.onSaved(value);
//             }
//           },
//         ),
//       ),
//     );
//   }
// }
//
// class DropdownFieldWidget extends StatefulWidget {
//   final String initialValue;
//   final List<String> items;
//   final Function(String) onChanged;
//
//   DropdownFieldWidget(
//       {required this.initialValue,
//       required this.items,
//       required this.onChanged});
//
//   @override
//   _DropdownFieldWidgetState createState() => _DropdownFieldWidgetState();
// }
//
// class _DropdownFieldWidgetState extends State<DropdownFieldWidget> {
//   String? _selectedValue;
//
//   @override
//   void initState() {
//     super.initState();
//     _selectedValue = widget.initialValue;
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return ListTile(
//       subtitle: DropdownButton<String>(
//         value: _selectedValue,
//         items: widget.items.map((String value) {
//           return DropdownMenuItem<String>(
//             value: value,
//             child: Text(value),
//           );
//         }).toList(),
//         onChanged: (String? newValue) {
//           setState(() {
//             _selectedValue = newValue;
//           });
//           widget.onChanged(newValue!);
//         },
//       ),
//     );
//   }
// }
//
//

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:ai_personas/config/AppConfig.dart';

class ConfigPage extends StatefulWidget {
  @override
  _ConfigPageState createState() => _ConfigPageState();
}

class _ConfigPageState extends State<ConfigPage> {
  Map<String, dynamic> initialConfig = {};

  List<String> displayedKeys = [
    'continuousMode',
    'continuousLimit',
    'fastLLMModel',
    'smartLLMModel',
    'openaiApiKey',
    'temperature',
    'googleApiKey',
    'customSearchEngineId',
    'memoryBackend',
  ];

  Map<String, String> descriptions = {
    'continuousMode': 'Continuous mode',
    'continuousLimit': 'Limit for continuous mode',
    'fastLLMModel': 'Fast LLM model',
    'smartLLMModel': 'Smart LLM model',
    'openaiApiKey': 'Enter your OpenAI API key',
    'temperature': 'Adjust the randomness of generated text',
    'googleApiKey': 'Enter your Google API key',
    'customSearchEngineId': 'Enter your custom search engine ID',
    'memoryBackend': 'Choose the memory backend'
  };

  Map<String, List<String>> dropdownItems = {
    'fastLLMModel': ['gpt-3.5-turbo'],
    'smartLLMModel': ['gpt-4'],
    'memoryBackend': ['local'],
  };

  @override
  void initState() {
    super.initState();
    AppConfig.loadConfig().then((_) {
      setState(() {
        initialConfig = Map<String, dynamic>.from(AppConfig.config);
      });
    });
  }

  void _saveValue(String key, dynamic value) {
    setState(() {
      AppConfig.config[key] = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData(
        brightness: Brightness.dark,
      ),
      child: Scaffold(
        appBar: AppBar(
          title: Text('Configuration'),
          backgroundColor: Colors.black,
        ),
        body: SafeArea(
          child: ListView.builder(
            itemCount: displayedKeys.length,
            itemBuilder: (BuildContext context, int index) {
              String key = displayedKeys[index];
              dynamic value = AppConfig.config[key];
              String? description = descriptions[key];

              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  ListTile(
                    title: Text(
                      description != null ? description : key,
                      style: TextStyle(fontWeight: FontWeight.w400, fontSize: 20),
                    ),
                  ),
                  if (value is bool)
                    SwitchListTile(
                      value: value,
                      onChanged: (bool newValue) {
                        setState(() {
                          AppConfig.config[key] = newValue;
                        });
                      },
                    )
                  else if (value is int || value is double)
                    TextFormFieldWidget(
                      initialValue: value.toString(),
                      keyboardType: TextInputType.numberWithOptions(
                          decimal: value is double),
                      onSaved: (String newValue) {
                        setState(() {
                          if (value is int) {
                            AppConfig.config[key] =
                                int.tryParse(newValue) ?? value;
                          } else {
                            AppConfig.config[key] =
                                double.tryParse(newValue) ?? value;
                          }
                        });
                      },
                    )
                  else if (dropdownItems.containsKey(key))
                      DropdownFieldWidget(
                        initialValue: value.toString(),
                        items: dropdownItems[key]!,
                        onChanged: (String newValue) {
                          setState(() {
                            AppConfig.config[key] = newValue;
                          });
                        },
                      )
                    else
                      TextFormFieldWidget(
                        initialValue: value.toString(),
                        keyboardType: TextInputType.text,
                        onSaved: (String newValue) {
                          setState(() {
                            AppConfig.config[key] = newValue;
                          });
                        },
                      ),
                  Divider(),
                ],
              );
            },
          ),
        ),
        floatingActionButton: Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            FloatingActionButton(
              heroTag: 'cancelButton',
              onPressed: () {
                setState(() {
                  AppConfig.config = Map<String, dynamic>.from(initialConfig);
                });
                Navigator.pop(context);
              },
              child: Icon(Icons.cancel),
            ),
            SizedBox(width: 10),
            FloatingActionButton(
              heroTag: 'saveButton',
              onPressed: () async {
                await AppConfig.saveAllConfig(displayedKeys);
                Navigator.pop(context);
              },
              child: Icon(Icons.save),
            ),
          ],
        ),
      ),
    );
  }

}

class TextFormFieldWidget extends StatefulWidget {
  final String initialValue;
  final TextInputType keyboardType;
  final Function(String) onSaved;

  TextFormFieldWidget(
      {required this.initialValue,
      required this.keyboardType,
      required this.onSaved});

  @override
  _TextFormFieldWidgetState createState() => _TextFormFieldWidgetState();
}

class _TextFormFieldWidgetState extends State<TextFormFieldWidget> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: ListTile(
        subtitle: TextFormField(
          initialValue: widget.initialValue,
          keyboardType: widget.keyboardType,
          onChanged: (value) {
            if (_formKey.currentState!.validate()) {
              widget.onSaved(value);
            }
          },
          validator: (value) {
            if (widget.keyboardType ==
                TextInputType.numberWithOptions(decimal: false) &&
                value != null &&
                int.tryParse(value) == null) {
              return 'Please enter a valid integer';
            }
            return null;
          },
          onSaved: (value) {
            if (value != null) {
              widget.onSaved(value);
            }
          },
        ),
      ),
    );
  }
}


class DropdownFieldWidget extends StatefulWidget {
  final String initialValue;
  final List<String> items;
  final Function(String) onChanged;

  DropdownFieldWidget(
      {required this.initialValue,
      required this.items,
      required this.onChanged});

  @override
  _DropdownFieldWidgetState createState() => _DropdownFieldWidgetState();
}

class _DropdownFieldWidgetState extends State<DropdownFieldWidget> {
  String? _selectedValue;

  @override
  void initState() {
    super.initState();
    _selectedValue = widget.initialValue;
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      subtitle: DropdownButton<String>(
        value: _selectedValue,
        items: widget.items.map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList(),
        onChanged: (String? newValue) {
          setState(() {
            _selectedValue = newValue;
          });
          widget.onChanged(newValue!);
        },
      ),
    );
  }
}
