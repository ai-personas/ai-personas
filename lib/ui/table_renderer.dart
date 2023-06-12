import 'package:ai_personas/persona/persona.dart';
import 'package:ai_personas/utils/persona_downloader.dart';
import 'package:flutter/material.dart';

typedef OnRowDeleted = void Function(Map<String, Map<String, String>> row);

class TableRenderer extends StatefulWidget {
  final List<Map<String, Map<String, String>>> data;
  final Function(Map<String, Map<String, String>>) onRowSelected;
  final OnRowDeleted onRowDeleted;

  const TableRenderer({
    Key? key,
    required this.data,
    required this.onRowSelected,
    required this.onRowDeleted
  }) : super(key: key);

  @override
  _TableRendererState createState() => _TableRendererState();
}

class _TableRendererState extends State<TableRenderer> {
  List<Map<String, Map<String, String>>>? data;

  @override
  void initState() {
    super.initState();
    data = List.from(widget.data);  // Create a copy of the initial data
  }

  void onRowDeleted(Map<String, Map<String, String>> row) {
    setState(() {
      data!.remove(row);
    });
  }

  @override
  Widget build(BuildContext context) {
    return SelectableTable(
      data: data!,  // Use the stateful data instead
      onRowSelected: (selectedRow) {
        widget.onRowSelected(selectedRow);
      },
      onRowDeleted: onRowDeleted,
    );
  }
}

typedef OnRowSelected = void Function(Map<String, Map<String, String>> row);

class SelectableTable extends StatefulWidget {
  final List<Map<String, Map<String, String>>> data;
  final OnRowSelected onRowSelected;
  final OnRowDeleted onRowDeleted;

  SelectableTable({required this.data, required this.onRowSelected, required this.onRowDeleted});

  @override
  _SelectableTableState createState() => _SelectableTableState();
}

class _SelectableTableState extends State<SelectableTable> {
  Map<String, Map<String, String>>? rowToDelete;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.fromLTRB(10, 20, 10, 10),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.green),
      ),
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Theme(
          data: Theme.of(context).copyWith(dividerColor: Colors.green),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Previous Personas',
                style: TextStyle(
                  fontSize: 24,
                  color: Colors.white,
                ),
              ),
              Align(
                alignment: Alignment.centerLeft,
                child: DataTable(
                  headingRowColor: MaterialStateProperty.all(Colors.transparent),
                  dataRowColor: MaterialStateProperty.all(Colors.transparent),
                  columns: const <DataColumn>[
                    DataColumn(
                      label: Text(
                        'Persona',
                        style: TextStyle(
                          fontFamily: 'RobotoMono',
                          fontSize: 18,
                          height: 1.4,
                          color: Colors.yellow,
                        ),
                      ),
                    ),
                    DataColumn(
                      label: Text(
                        'Version',
                        style: TextStyle(
                          fontFamily: 'RobotoMono',
                          fontSize: 18,
                          height: 1.4,
                          color: Colors.yellow,
                        ),
                      ),
                    ),
                    DataColumn(
                      label: Text(
                        'Action',
                        style: TextStyle(
                          fontFamily: 'RobotoMono',
                          fontSize: 18,
                          height: 1.4,
                          color: Colors.yellow,
                        ),
                      ),
                    ),
                  ],
                  rows: widget.data.map((row) {
                    return DataRow(
                      cells: <DataCell>[
                        DataCell(
                          Text(
                            row['persona']?['value'] ?? '',
                            style: const TextStyle(
                              fontFamily: 'RobotoMono',
                              fontSize: 18,
                              height: 1.4,
                              color: Colors.green,
                            ),
                          ),
                        ),
                        DataCell(
                          Text(
                            row['version']?['value'] ?? '',
                            style: const TextStyle(
                              fontFamily: 'RobotoMono',
                              fontSize: 18,
                              height: 1.4,
                              color: Colors.green,
                            ),
                          ),
                        ),
                        DataCell(
                          Row(
                            children: [
                              if (row['action']?['button'] != null)
                                ElevatedButton(
                                  child: Text(
                                    row['action']?['button'] ?? '',  // Provide '' as default value
                                    style: TextStyle(
                                      fontSize: 14,
                                      color: Colors.white,
                                    ),
                                  ),
                                  style: ElevatedButton.styleFrom(
                                      minimumSize: const Size(100, 40),
                                      textStyle: const TextStyle(fontSize: 18),
                                      primary: Colors.green),
                                  onPressed: () {
                                    widget.onRowSelected(row);
                                  },
                                ),
                              if (row['action']?['download']! == 'true')
                                IconButton(
                                  icon: Icon(Icons.download_outlined),
                                  color: Colors.green,
                                  onPressed: () async {
                                    await PersonaDownloader.downloadPersona(row['persona']?['value'] ?? '');
                                  },
                                ),
                              if (row['action']?['delete']! == 'true')
                                IconButton(
                                  icon: Icon(Icons.delete),
                                  color: Colors.red,
                                  onPressed: () async {
                                    try {
                                      await Persona.deletePersona(row['persona']?['value'] ?? '', row['version']?['value'] ?? '');
                                      widget.onRowDeleted(row);  // Pass the row that was deleted to the callback
                                    } catch (e) {
                                      print('Failed to delete persona: $e');
                                    }
                                  },
                                ),
                            ],
                          ),
                        ),
                      ],
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
