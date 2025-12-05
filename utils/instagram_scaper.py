import requests
from datetime import datetime

class InstagramScraper:
    def __init__(self, rapidapi_key):
        self.rapidapi_key = rapidapi_key
        self.base_url = "https://instagram-scraper-api2.p.rapidapi.com/v1"
    
    def is_configured(self):
        return self.rapidapi_key is not None
    
    def scrape(self, topic, limit=50):
        if not self.rapidapi_key:
            return []
        
        posts = []
        
        try:
            # Search hashtags
            url = f"{self.base_url}/hashtag"
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
            }
            
            querystring = {"hashtag": topic.replace('#', '').replace(' ', '')}
            
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'items' in data['data']:
                    for item in data['data']['items'][:limit]:
                        caption = ''
                        if 'caption' in item and item['caption']:
                            caption = item['caption'].get('text', '')
                        
                        post_data = {
                            'text': caption,
                            'author': item.get('user', {}).get('username', 'unknown'),
                            'created_at': datetime.fromtimestamp(
                                item.get('taken_at', 0)
                            ).isoformat() if item.get('taken_at') else datetime.now().isoformat(),
                            'likes': item.get('like_count', 0),
                            'url': f"https://instagram.com/p/{item.get('code', '')}",
                            'platform': 'instagram',
                            'id': item.get('id', '')
                        }
                        
                        if caption:  # Only include posts with captions
                            posts.append(post_data)
            
        except Exception as e:
            print(f"Instagram scraping error: {e}")
            return []
        
        return posts
