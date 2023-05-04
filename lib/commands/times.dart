import 'package:intl/intl.dart';

String getDateTime() {
  final now = DateTime.now();
  final formatter = DateFormat('yyyy-MM-dd HH:mm:ss');
  final formattedDate = formatter.format(now);
  return 'Current date and time: $formattedDate';
}
