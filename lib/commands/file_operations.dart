import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as p;

const String LOG_FILE = 'file_logger.txt';
final String WORKSPACE_PATH = Directory.current.path;
final String LOG_FILE_PATH = p.join(WORKSPACE_PATH, LOG_FILE);

bool checkDuplicateOperation(String operation, String filename) {
  String logContent = readFile(LOG_FILE);
  String logEntry = '$operation: $filename\n';
  return logContent.contains(logEntry);
}

void logOperation(String operation, String filename) {
  String logEntry = '$operation: $filename\n';

  if (!File(LOG_FILE_PATH).existsSync()) {
    File(LOG_FILE_PATH).writeAsStringSync('File Operation Logger ', encoding: utf8);
  }

  appendToFile(LOG_FILE, logEntry, shouldLog: false);
}

Iterable<String> splitFile(String content, {int maxLength = 4000, int overlap = 0}) sync* {
  int start = 0;
  int contentLength = content.length;

  while (start < contentLength) {
    int end = start + maxLength;
    String chunk;
    if (end + overlap < contentLength) {
      chunk = content.substring(start, end + overlap - 1);
    } else {
      chunk = content.substring(start, contentLength);
      if (chunk.length <= overlap) break;
    }
    yield chunk;
    start += maxLength - overlap;
  }
}

String readFile(String filename) {
  try {
    String filePath = p.join(WORKSPACE_PATH, filename);
    return File(filePath).readAsStringSync(encoding: utf8);
  } catch (e) {
    return 'Error: ${e.toString()}';
  }
}

void ingestFile(
    String filename, dynamic memory, {
      int maxLength = 4000,
      int overlap = 200,
    }) {
  try {
    print('Working with file $filename');
    String content = readFile(filename);
    int contentLength = content.length;
    print('File length: $contentLength characters');

    List<String> chunks = splitFile(content, maxLength: maxLength, overlap: overlap).toList();

    int numChunks = chunks.length;
    for (int i = 0; i < numChunks; i++) {
      print('Ingesting chunk ${i + 1} / $numChunks into memory');
      String memoryToAdd = 'Filename: $filename\nContent part#${i + 1}/$numChunks: ${chunks[i]}';
      memory.add(memoryToAdd);
    }

    print('Done ingesting $numChunks chunks from $filename.');
  } catch (e) {
    print('Error while ingesting file \'$filename\': ${e.toString()}');
  }
}

String writeToFileSync(String filename, String text) {
  if (checkDuplicateOperation('write', filename)) {
    return 'Error: File has already been updated.';
  }
  try {
    String filePath = p.join(WORKSPACE_PATH, filename);
    String directory = p.dirname(filePath);
    if (!Directory(directory).existsSync()) {
      Directory(directory).createSync(recursive: true);
    }
    File(filePath).writeAsStringSync(text, encoding: utf8);
    logOperation('write', filename);
    return 'File written to successfully.';
  } catch (e) {
    return 'Error: ${e.toString()}';
  }
}

String appendToFile(String filename, String text, {bool shouldLog = true}) {
  try {
    String filePath = p.join(WORKSPACE_PATH, filename);
    File(filePath).writeAsStringSync(text, mode: FileMode.append, encoding: utf8);

    if (shouldLog) {
      logOperation('append', filename);
    }

    return 'Text appended successfully.';
  } catch (e) {
    return 'Error: ${e.toString()}';
  }
}

String deleteFile(String filename) {
  if (checkDuplicateOperation('delete', filename)) {
    return 'Error: File has already been deleted.';
  }
  try {
    String filePath = p.join(WORKSPACE_PATH, filename);
    File(filePath).deleteSync();
    logOperation('delete', filename);
    return 'File deleted successfully.';
  } catch (e) {
    return 'Error: ${e.toString()}';
  }
}

List<String> searchFiles(String directory) {
  List<String> foundFiles = [];

  String searchDirectory = directory.isEmpty || directory == '/'
      ? WORKSPACE_PATH
      : p.join(WORKSPACE_PATH, directory);

  for (final entity in Directory(searchDirectory).listSync(recursive: true)) {
    if (entity is File && !p.basename(entity.path).startsWith('.')) {
      String relativePath = p.relative(entity.path, from: WORKSPACE_PATH);
      foundFiles.add(relativePath);
    }
  }

  return foundFiles;
}

Future<String> downloadFile(String url, String filename) async {
  String safeFilename = p.join(WORKSPACE_PATH, filename);
  try {
    print('Downloading file from $url');
    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      File(safeFilename).writeAsBytesSync(response.bodyBytes);
      return 'Successfully downloaded and locally stored file: "$filename"!';
    } else {
      return 'Failed to download file. Server responded with status code: ${response.statusCode}';
    }
  } catch (e) {
    return 'Error: ${e.toString()}';
  }
}
