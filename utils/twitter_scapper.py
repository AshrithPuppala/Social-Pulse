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
                self.client = None
    
    def is_configured(self):
        return bool(self.bearer_token)
    
    def scrape(self, topic, max_results=100):
        """Scrape Twitter/X posts about a topic"""
        if not self.client:
            raise Exception("Twitter API not configured")
        
        posts = []
        
        try:
            # Search recent tweets
            query = f"{topic} -is:retweet lang:en"
            
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username']
            )
            
            if not response.data:
                return posts
            
            # Create user lookup dictionary
            users = {}
            if response.includes and 'users' in response.includes:
                for user in response.includes['users']:
                    users[user.id] = user.username
            
            for tweet in response.data:
                username = users.get(tweet.author_id, 'unknown')
                metrics = tweet.public_metrics or {}
                
                post_data = {
                    'text': tweet.text,
                    'author': username,
                    'platform': 'twitter',
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else datetime.now().isoformat(),
                    'engagement': metrics.get('like_count', 0) + metrics.get('retweet_count', 0) + metrics.get('reply_count', 0)
                }
                posts.append(post_data)
        
        except tweepy.TweepyException as e:
            print(f"Twitter scraping error: {e}")
            raise Exception(f"Failed to scrape Twitter: {str(e)}")
        except Exception as e:
            print(f"Twitter error: {e}")
            raise Exception(f"Failed to scrape Twitter: {str(e)}")
        
        return posts
