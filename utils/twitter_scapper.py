import tweepy
from datetime import datetime

class TwitterScraper:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.client = None
        
        if self.is_configured():
            try:
                self.client = tweepy.Client(bearer_token=bearer_token)
            except Exception as e:
                print(f"Twitter initialization error: {e}")
    
    def is_configured(self):
        return self.bearer_token is not None
    
    def scrape(self, topic, limit=100):
        if not self.client:
            return []
        
        posts = []
        
        try:
            # Search recent tweets
            response = self.client.search_recent_tweets(
                query=f"{topic} -is:retweet lang:en",
                max_results=min(limit, 100),
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username']
            )
            
            if not response.data:
                return []
            
            # Create a mapping of user IDs to usernames
            users = {}
            if response.includes and 'users' in response.includes:
                for user in response.includes['users']:
                    users[user.id] = user.username
            
            for tweet in response.data:
                username = users.get(tweet.author_id, 'unknown')
                
                post_data = {
                    'text': tweet.text,
                    'author': username,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else datetime.now().isoformat(),
                    'likes': tweet.public_metrics['like_count'] if tweet.public_metrics else 0,
                    'retweets': tweet.public_metrics['retweet_count'] if tweet.public_metrics else 0,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'platform': 'twitter',
                    'id': tweet.id
                }
                posts.append(post_data)
        
        except Exception as e:
            print(f"Twitter scraping error: {e}")
            return []
        
        return posts
