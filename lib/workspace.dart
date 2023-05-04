import 'dart:io';
import 'package:path/path.dart' as path;

class WorkspaceUtils {
  static final String workspacePath = path.join(Directory.current.path, 'auto_gpt_workspace');

  static void ensureWorkspaceDirectory() {
    Directory(workspacePath).createSync(recursive: true);
  }

  static String pathInWorkspace(String relativePath) {
    return path.joinAll([workspacePath, relativePath]);
  }

  static String safePathJoin(String base, List<String> paths) {
    final joinedPath = path.joinAll([base, ...paths]);

    if (!path.isWithin(base, joinedPath)) {
      throw ArgumentError("Attempted to access path '$joinedPath' outside of working directory '$base'.");
    }

    return joinedPath;
  }
}
