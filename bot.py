
import tweepy
import openai
import schedule
import time

# Twitter API credentials
API_KEY = "Your_API_Key"
API_SECRET = "Your_API_Secret"
ACCESS_TOKEN = "Your_Access_Token"
ACCESS_TOKEN_SECRET = "Your_Access_Token_Secret"

# OpenAI API credentials
openai.api_key = "Your_OpenAI_API_Key"

# Tweepy authentication
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Generate a tweet using OpenAI
def generate_tweet():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant generating engaging tweets."},
                {"role": "user", "content": "Create a tweet about technology, motivation, or trending topics."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        tweet_content = response["choices"][0]["message"]["content"].strip()
        return tweet_content
    except Exception as e:
        print("Error generating tweet:", e)
        return None

# Post a tweet
def post_tweet():
    tweet = generate_tweet()
    if tweet:
        try:
            api.update_status(tweet)
            print("Tweet posted:", tweet)
        except Exception as e:
            print("Error posting tweet:", e)

# Reply to mentions
def reply_to_mentions():
    try:
        mentions = api.mentions_timeline(count=5, tweet_mode="extended")
        for mention in mentions:
            if not mention.favorited:  # Avoid replying to the same mention multiple times
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an assistant replying to tweets."},
                        {"role": "user", "content": f"Reply to this tweet: {mention.full_text}"}
                    ],
                    max_tokens=50,
                    temperature=0.7
                )
                reply_content = response["choices"][0]["message"]["content"].strip()
                api.update_status(
                    status=f"@{mention.user.screen_name} {reply_content}",
                    in_reply_to_status_id=mention.id
                )
                api.create_favorite(mention.id)
                print(f"Replied to @{mention.user.screen_name}: {reply_content}")
    except Exception as e:
        print("Error replying to mentions:", e)

# Schedule tweets and replies
schedule.every().day.at("10:00").do(post_tweet)
schedule.every(2).hours.do(reply_to_mentions)

# Running the bot
print("Bot is running...")

while True:
    schedule.run_pending()
    time.sleep(1)
