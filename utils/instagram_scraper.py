import requests
from datetime import datetime

class InstagramScraper:
    def __init__(self, rapidapi_key):
        self.rapidapi_key = rapidapi_key
        self.base_url = "https://instagram120.p.rapidapi.com"
    
    def is_configured(self):
        return self.rapidapi_key is not None
    
    def scrape(self, topic, limit=50):
        if not self.rapidapi_key:
            return []
        
        posts = []
        
        try:
            # Use the posts endpoint to search for hashtag posts
            url = f"{self.base_url}/api/instagram/posts"
            
            headers = {
                "x-rapidapi-key": self.rapidapi_key,
                "x-rapidapi-host": "instagram120.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            
            # Prepare the hashtag (remove # and spaces)
            clean_topic = topic.replace('#', '').replace(' ', '')
            
            # Request body as shown in your screenshot
            payload = {
                "username": clean_topic,  # Try using topic as username first
                "maxId": ""
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse the response - structure may vary
                if isinstance(data, dict):
                    items = data.get('data', {}).get('items', [])
                    if not items:
                        items = data.get('items', [])
                    if not items:
                        items = data.get('posts', [])
                    
                    for item in items[:limit]:
                        # Extract caption text
                        caption = ''
                        if isinstance(item, dict):
                            # Try different caption field structures
                            if 'caption' in item:
                                if isinstance(item['caption'], dict):
                                    caption = item['caption'].get('text', '')
                                else:
                                    caption = str(item['caption'])
                            elif 'text' in item:
                                caption = item['text']
                            elif 'edge_media_to_caption' in item:
                                edges = item.get('edge_media_to_caption', {}).get('edges', [])
                                if edges:
                                    caption = edges[0].get('node', {}).get('text', '')
                        
                        # Extract username
                        username = 'unknown'
                        if 'user' in item:
                            if isinstance(item['user'], dict):
                                username = item['user'].get('username', 'unknown')
                            else:
                                username = str(item['user'])
                        elif 'owner' in item:
                            if isinstance(item['owner'], dict):
                                username = item['owner'].get('username', 'unknown')
                        
                        # Extract timestamp
                        created_at = datetime.now().isoformat()
                        if 'taken_at' in item:
                            created_at = datetime.fromtimestamp(item['taken_at']).isoformat()
                        elif 'timestamp' in item:
                            created_at = datetime.fromtimestamp(item['timestamp']).isoformat()
                        elif 'taken_at_timestamp' in item:
                            created_at = datetime.fromtimestamp(item['taken_at_timestamp']).isoformat()
                        
                        # Extract engagement metrics
                        likes = 0
                        if 'like_count' in item:
                            likes = item['like_count']
                        elif 'edge_liked_by' in item:
                            likes = item['edge_liked_by'].get('count', 0)
                        
                        # Get post URL
                        post_id = item.get('id', item.get('code', ''))
                        post_url = f"https://instagram.com/p/{post_id}" if post_id else ''
                        
                        post_data = {
                            'text': caption if caption else f"Instagram post about {clean_topic}",
                            'author': username,
                            'created_at': created_at,
                            'likes': likes,
                            'url': post_url,
                            'platform': 'instagram',
                            'id': post_id
                        }
                        
                        # Only include posts with meaningful content
                        if caption and len(caption) > 10:
                            posts.append(post_data)
            
            elif response.status_code == 401:
                raise Exception("Invalid RapidAPI key for Instagram")
            elif response.status_code == 429:
                raise Exception("Instagram API rate limit exceeded")
            elif response.status_code == 403:
                raise Exception("Instagram API access forbidden - check your RapidAPI subscription")
            else:
                # Try alternative approach: search by hashtag directly
                try:
                    posts = self._search_by_hashtag(clean_topic, limit, headers)
                except:
                    raise Exception(f"Instagram API returned status {response.status_code}")
        
        except Exception as e:
            error_msg = str(e)
            if "Invalid RapidAPI key" in error_msg or "rate limit" in error_msg or "forbidden" in error_msg:
                raise Exception(error_msg)
            print(f"Instagram scraping error: {e}")
            return []
        
        return posts
    
    def _search_by_hashtag(self, hashtag, limit, headers):
        """Alternative method to search by hashtag"""
        posts = []
        
        # Try hashtag-specific endpoint if available
        url = f"{self.base_url}/api/instagram/hashtag"
        
        payload = {
            "hashtag": hashtag,
            "maxId": ""
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse hashtag response
            items = []
            if isinstance(data, dict):
                items = data.get('data', {}).get('items', [])
                if not items:
                    items = data.get('items', [])
                if not items:
                    items = data.get('edge_hashtag_to_media', {}).get('edges', [])
            
            for item in items[:limit]:
                # Handle edge-wrapped items
                if 'node' in item:
                    item = item['node']
                
                caption = ''
                if 'edge_media_to_caption' in item:
                    edges = item.get('edge_media_to_caption', {}).get('edges', [])
                    if edges:
                        caption = edges[0].get('node', {}).get('text', '')
                elif 'caption' in item:
                    caption = item.get('caption', {}).get('text', '') if isinstance(item['caption'], dict) else str(item['caption'])
                
                username = item.get('owner', {}).get('username', 'unknown') if isinstance(item.get('owner'), dict) else 'unknown'
                
                if caption and len(caption) > 10:
                    posts.append({
                        'text': caption,
                        'author': username,
                        'created_at': datetime.now().isoformat(),
                        'likes': item.get('edge_liked_by', {}).get('count', 0),
                        'url': f"https://instagram.com/p/{item.get('shortcode', '')}",
                        'platform': 'instagram',
                        'id': item.get('id', '')
                    })
        
        return posts
