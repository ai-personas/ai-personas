import 'package:ai_personas/utils/console.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppConfig {
  static Map<String, dynamic> config = {
    'debugMode': true,
    'continuousMode': true,
    'continuousLimit': 1000,
    'speakMode': false,
    'skipReprompt': false,
    'seleniumWebBrowser': 'chrome',
    'aiSettingsFile': 'ai_settings.yaml',
    'fastLLMModel': 'gpt-3.5-turbo',
    'smartLLMModel': 'gpt-4',
    'fastTokenLimit': 4000,
    'smartTokenLimit': 8000,
    'browseChunkMaxLength': 8192,
    'browseSummaryMaxToken': 300,
    'openaiApiKey': '',
    'temperature': 1,
    'useAzure': false,
    'executeLocalCommands': false,
    'elevenlabsApiKey': '',
    'elevenlabsVoice1Id': '',
    'elevenlabsVoice2Id': '',
    'useMacOsTts': false,
    'useBrianTts': false,
    'githubApiKey': '',
    'githubUsername': '',
    'googleApiKey': '',
    'customSearchEngineId': '',
    'pineconeApiKey': '',
    'pineconeEnvironment': '',
    'weaviateHost': '',
    'weaviatePort': '',
    'weaviateProtocol': 'http',
    'weaviateUsername': '',
    'weaviatePassword': '',
    'weaviateScopes': '',
    'weaviateEmbeddedPath': '',
    'weaviateApiKey': '',
    'useWeaviateEmbedded': false,
    'milvusAddr': 'localhost:19530',
    'milvusCollection': 'autogpt',
    'imageProvider': '',
    'huggingfaceApiToken': '',
    'huggingfaceAudioToTextModel': '',
    'userAgent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'redisHost': 'localhost',
    'redisPort': '6379',
    'redisPassword': '',
    'wipeRedisOnStart': false,
    'memoryBackend': 'local',
  };

  static Future<void> loadConfig() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    config.forEach((key, value) {
      if (value is bool) {
        config[key] = prefs.getBool(key) ?? value;
      } else if (value is int) {
        config[key] = prefs.getInt(key) ?? value;
      } else if (value is double) {
        config[key] = prefs.getDouble(key) ?? value;
      } else if (value is String) {
        config[key] = prefs.getString(key) ?? value;
      }
    });
  }

  static Future<void> saveConfig(String key) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    dynamic value = config[key];

    if (value is bool) {
      await prefs.setBool(key, value);
    } else if (value is int) {
      await prefs.setInt(key, value);
    } else if (value is double) {
      await prefs.setDouble(key, value);
    } else if (value is String) {
      await prefs.setString(key, value);
    }
  }

  static Future<void> saveAllConfig(List<String> keys) async {
    for (String key in keys) {
      await saveConfig(key);
    }
  }

  static Future<void> checkApiKeys() async {
    bool allKeysProvided;
    do {
      allKeysProvided = true;

      // Check if the openaiApiKey exists and is not empty.
      if (config['openaiApiKey'] == null || config['openaiApiKey'].isEmpty) {
        allKeysProvided = false;
        await console.stdout('Warning: openaiApiKey does not exist or is empty.', textColor: Colors.redAccent);
        String? input = await console.getSecret('Please enter your OpenAI API key:', 'OpenAI API key configuration updated!');
        if (input != null && input.isNotEmpty) {
          config['openaiApiKey'] = input;
          await saveConfig('openaiApiKey');
        }
      }

      // Check if the googleApiKey exists and is not empty.
      if (config['googleApiKey'] == null || config['googleApiKey'].isEmpty) {
        allKeysProvided = false;
        await console.stdout('Warning: googleApiKey does not exist or is empty.', textColor: Colors.redAccent);
        String? input = await console.getSecret('Please enter your Google API key:', 'Google API key configuration updated!');
        if (input != null && input.isNotEmpty) {
          config['googleApiKey'] = input;
          await saveConfig('googleApiKey');
        }
      }

      // Check if the customSearchEngineId exists and is not empty.
      if (config['customSearchEngineId'] == null || config['customSearchEngineId'].isEmpty) {
        allKeysProvided = false;
        await console.stdout('Warning: customSearchEngineId does not exist or is empty.', textColor: Colors.redAccent);
        String? input = await console.getSecret('Please enter your custom search engine ID:','Custom search engine ID configuration updated!');
        if (input != null && input.isNotEmpty) {
          config['customSearchEngineId'] = input;
          await saveConfig('customSearchEngineId');
        }
      }
    } while (!allKeysProvided);
  }

}

final Map<String, dynamic> cfg = AppConfig.config;
