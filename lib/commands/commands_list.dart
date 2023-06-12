class CommandsList {
  static const Map<String, dynamic> commands = {
    'Google Search': 'Google Search: "google", args: "input": "<search>"',
    'Browse Website': 'Browse Website: "browse_website", args: "url": "<url>", "question": "<what_you_want_to_find_on_website>"',
  };

  static dynamic getValue(String key) {
    return commands[key];
  }
}