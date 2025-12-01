import requests
from datetime import datetime
import time

class InstagramScraper:
    def __init__(self, rapidapi_key):
        self.rapidapi_key = rapidapi_key
        self.base_url = "https://instagram-scraper-api2.p.rapidapi.com/v1"
        
    def is_configured(self):
        return bool(self.rapidapi_key)
    
    def scrape(self, topic, limit=100):
        """Scrape Instagram posts about a topic using hashtag search"""
        if not self.rapidapi_key:
            raise Exception("Instagram API (RapidAPI) not configured")
        
        posts = []
        
        try:
            # Clean topic for hashtag search
            hashtag = topic.replace(' ', '').replace('#', '')
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
            }
            
            # Search for hashtag
            url = f"{self.base_url}/hashtag"
            querystring = {"hashtag": hashtag}
            
            response = requests.get(url, headers=headers, params=querystring, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'items' in data['data']:
                    items = data['data']['items'][:limit]
                    
                    for item in items:
                        try:
                            caption_text = ''
                            if 'caption' in item and item['caption']:
                                if isinstance(item['caption'], dict) and 'text' in item['caption']:
                                    caption_text = item['caption']['text']
                                elif isinstance(item['caption'], str):
                                    caption_text = item['caption']
                            
                            username = 'unknown'
                            if 'user' in item and item['user']:
                                if isinstance(item['user'], dict) and 'username' in item['user']:
                                    username = item['user']['username']
                            
                            post_id = item.get('id', 'unknown')
                            
                            engagement = 0
                            if 'like_count' in item:
                                engagement += item['like_count']
                            if 'comment_count' in item:
                                engagement += item['comment_count']
                            
                            post_data = {
                                'text': caption_text if caption_text else f"Instagram post about {topic}",
                                'author': username,
                                'platform': 'instagram',
                                'url': f"https://instagram.com/p/{item.get('code', post_id)}",
                                'created_at': datetime.fromtimestamp(item.get('taken_at', time.time())).isoformat() if 'taken_at' in item else datetime.now().isoformat(),
                                'engagement': engagement
                            }
                            
                            if post_data['text'] and len(post_data['text']) > 10:
                                posts.append(post_data)
                        
                        except Exception as e:
                            print(f"Error processing Instagram item: {e}")
                            continue
            
            elif response.status_code == 429:
                raise Exception("Rate limit reached for Instagram API")
            else:
                raise Exception(f"Instagram API error: {response.status_code}")
        
        except requests.exceptions.Timeout:
            raise Exception("Instagram API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Instagram API: {str(e)}")
        except Exception as e:
            print(f"Instagram scraping error: {e}")
            raise Exception(f"Failed to scrape Instagram: {str(e)}")
        
        return posts[:100]  # Return max 100 posts
