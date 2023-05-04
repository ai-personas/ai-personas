import 'package:openai_client/openai_client.dart';

// Create the configuration
final conf = OpenAIConfiguration(
    apiKey: 'Your API key',
    organizationId: 'Your organization ID', // Optional
);

// Create a new client
final openai = OpenAIClient(configuration: conf);