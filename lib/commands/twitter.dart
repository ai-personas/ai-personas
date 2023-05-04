import 'dart:io';
import 'package:dotenv/dotenv.dart';
import 'package:twitter_api_v2/twitter_api_v2.dart' as v2;

Future<void> sendTweet(String tweetText) async {
  final twitter = v2.TwitterApi(
    bearerToken: 'YOUR_TOKEN_HERE',
    oauthTokens: const v2.OAuthTokens(
      consumerKey: 'YOUR_CONSUMER_KEY_HERE',
      consumerSecret: 'YOUR_CONSUMER_SECRET_HERE',
      accessToken: 'YOUR_ACCESS_TOKEN_HERE',
      accessTokenSecret: 'YOUR_ACCESS_TOKEN_SECRET_HERE',
    ),

    retryConfig: v2.RetryConfig(
      maxAttempts: 5,
      onExecute: (event) => print(
        'Retry after ${event.intervalInSeconds} seconds... '
            '[${event.retryCount} times]',
      ),
    ),

    //! The default timeout is 10 seconds.
    timeout: Duration(seconds: 20),
  );

  try {
    final response = await twitter.tweets.createTweet(
      text: 'Tweet with uploaded media',
    );
    print('Tweet sent successfully! ${response.toJson()}');
  } on HttpException catch (e) {
    print('Error sending tweet: ${e.message}');
  }
}
