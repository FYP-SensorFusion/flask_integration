import 'package:http/http.dart' as http;

fetch_data(String url) async {
  http.Response response = await http.post(Uri.parse(url));
  print("Response.body = ${response.body}");
  return response.body;
}

Future<String> fetchData(String url) async {
  final uri = Uri.parse(url);
  final query = uri.queryParameters['query'];

  if (query == null) {
    throw Exception('Missing required query parameter "query" in the URL.');
  }

  final response = await http.post(uri, body: {'query': query});
  print("Response.body = ${response.body}");
  return response.body;
}