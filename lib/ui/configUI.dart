import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:ai_personas/config/AppConfig.dart';

class ConfigUI extends StatefulWidget {
  @override
  _ConfigUIState createState() => _ConfigUIState();
}

class _ConfigUIState extends State<ConfigUI> {
  List<String> displayedKeys = [
    'continuousMode',
    'continuousLimit',
    'skipReprompt',
    'fastLLMModel',
    'smartLLMModel',
    'browseChunkMaxLength',
    'browseSummaryMaxToken',
    'openaiApiKey',
    'temperature',
    'googleApiKey',
    'customSearchEngineId',
    'memoryIndex',
    'memoryBackend',
  ];

  @override
  void initState() {
    super.initState();
    AppConfig.loadConfig();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Config UI"),
      ),
      body: SafeArea(
        child: ListView.builder(
          itemCount: displayedKeys.length,
          itemBuilder: (BuildContext context, int index) {
            String key = displayedKeys[index];
            dynamic value = AppConfig.config[key];

            if (value is bool) {
              return SwitchListTile(
                title: Text(
                  key,
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                value: value,
                onChanged: (bool newValue) async {
                  setState(() {
                    AppConfig.config[key] = newValue;
                  });
                  await AppConfig.saveConfig(key);
                },
              );
            } else if (value is int || value is double) {
              return ListTile(
                title: Text(
                  key,
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: TextFormField(
                  initialValue: value.toString(),
                  keyboardType: TextInputType.number,
                  onChanged: (String newValue) async {
                    setState(() {
                      if (value is int) {
                        AppConfig.config[key] = int.tryParse(newValue) ?? value;
                      } else {
                        AppConfig.config[key] = double.tryParse(newValue) ?? value;
                      }
                    });
                    await AppConfig.saveConfig(key);
                  },
                ),
              );
            } else {
              return ListTile(
                title: Text(
                  key,
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: TextFormField(
                  initialValue: value.toString(),
                  onChanged: (String newValue) async {
                    setState(() {
                      AppConfig.config[key] = newValue;
                    });
                    await AppConfig.saveConfig(key);
                  },
                ),
              );
            }
          },
        ),
      ),
    );
  }
}
