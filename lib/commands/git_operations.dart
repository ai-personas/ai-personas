import 'dart:io';
import 'package:path/path.dart' as p;
import 'package:ai_personas/config/config_keys.dart';
import 'package:ai_personas/config/app_config.dart';

String WORKSPACE_PATH = 'your_workspace_path_here';

String pathInWorkspace(String path) {
  return p.join(WORKSPACE_PATH, path);
}

Future<String> cloneRepository(String repoUrl, String clonePath) async {
  List<String> splitUrl = repoUrl.split('//');
  String authRepoUrl = '//${cfg[ConfigKeys.githubUsername]}:${cfg[ConfigKeys.githubApiKey]}@${splitUrl[1]}';
  String safeClonePath = pathInWorkspace(clonePath);

  try {
    // Use the `git clone` command directly
    await Process.run('git', ['clone', '--depth', '1', authRepoUrl, safeClonePath]);
    return 'Cloned $repoUrl to $safeClonePath';
  } catch (e) {
    return 'Error: ${e.toString()}';
  }
}
