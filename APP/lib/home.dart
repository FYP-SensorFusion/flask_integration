import 'dart:convert';

import 'package:flutter/material.dart';

import 'function.dart';


class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  String url = '';
  var data;
  String output = 'Initial Output';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Simple Flask App'),
      ),
      body: Center(
        child: Container(
          padding: EdgeInsets.all(20),
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            TextField(
              onChanged: (value) =>
              // url = 'http://10.0.2.2:5000/api?query=' + value.toString(),
              url = 'http://10.0.2.2:5000/?query=$value',
            ),
            TextButton(
              onPressed: () async {
                data = await fetchData(url);
                setState(() {
                  output = data;
                });
              },
              child: Text(
                'Enter Sentence',
                style: TextStyle(fontSize: 40, color: Colors.green),
              ),
            ),
            Text(output, style: TextStyle(fontSize: 30, color: Colors.black54),)
          ]),
        ),
      ),
    );
  }
}
