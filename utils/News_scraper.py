import requests
from datetime import datetime, timedelta

class NewsScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    def is_configured(self):
        return bool(self.api_key)
    
    def scrape(self, topic, limit=100):
        """Scrape news articles about a topic using News API"""
        if not self.api_key:
            raise Exception("News API not configured")
        
        posts = []
        
        try:
            # Search for articles from the last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            # Use the Everything endpoint for comprehensive search
            url = f"{self.base_url}/everything"
            
            params = {
                'q': topic,
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'from': from_date,
                'pageSize': min(limit, 100)  # Max 100 per request
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'ok' and 'articles' in data:
                    for article in data['articles']:
                        # Combine title and description for better sentiment analysis
                        text = f"{article.get('title', '')}. {article.get('description', '')}"
                        
                        # Skip articles without meaningful content
                        if not text.strip() or text.strip() == '.':
                            continue
                        
                        post_data = {
                            'text': text,
                            'author': article.get('source', {}).get('name', 'Unknown Source'),
                            'created_at': article.get('publishedAt', datetime.now().isoformat()),
                            'url': article.get('url', ''),
                            'platform': 'news',
                            'id': article.get('url', ''),
                            'source': article.get('source', {}).get('name', 'Unknown')
                        }
                        
                        posts.append(post_data)
                
                elif data.get('status') == 'error':
                    error_code = data.get('code', 'unknown')
                    error_message = data.get('message', 'Unknown error')
                    
                    if error_code == 'rateLimited':
                        raise Exception("News API rate limit exceeded (100 requests/day on free tier)")
                    elif error_code == 'apiKeyInvalid':
                        raise Exception("Invalid News API key")
                    else:
                        raise Exception(f"News API error: {error_message}")
            
            elif response.status_code == 401:
                raise Exception("Invalid News API key")
            elif response.status_code == 429:
                raise Exception("News API rate limit exceeded")
            else:
                raise Exception(f"News API returned status code {response.status_code}")
        
        except requests.exceptions.Timeout:
            raise Exception("News API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to News API: {str(e)}")
        except Exception as e:
            if "News API" in str(e):
                raise
            else:
                print(f"News scraping error: {e}")
                raise Exception(f"Failed to scrape news: {str(e)}")
        
        return posts[:100]  # Return max 100 articles
