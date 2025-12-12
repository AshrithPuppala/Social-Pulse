import requests
from datetime import datetime, timedelta

class NewsScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2/everything'
    
    def is_configured(self):
        """Check if API key is configured"""
        return self.api_key and self.api_key != 'your_news_api_key_here'
    
    def scrape(self, topic, limit=100):
        """
        Scrape news articles for a given topic
        Returns list of articles with text, source, and URL
        """
        if not self.is_configured():
            raise Exception('News API key not configured')
        
        try:
            # Calculate date range (last 30 days for better results)
            to_date = datetime.now()
            from_date = to_date - timedelta(days=30)
            
            # Make API request with improved parameters
            params = {
                'q': topic,  # Search query
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'relevancy',  # Sort by relevance instead of date
                'pageSize': min(limit, 100),  # API max is 100
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 426:
                raise Exception('News API requires upgrade. The free tier has limited access. Please try a more general topic.')
            
            if response.status_code == 401:
                raise Exception('Invalid News API key. Please check your NEWS_API_KEY.')
            
            if response.status_code == 429:
                raise Exception('Rate limit exceeded. Please wait a moment and try again.')
            
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != 'ok':
                error_msg = data.get('message', 'Unknown error from News API')
                raise Exception(f'News API error: {error_msg}')
            
            articles_data = data.get('articles', [])
            
            if not articles_data:
                return []
            
            # Process articles
            processed_articles = []
            for article in articles_data:
                # Skip articles without content
                if not article.get('title') and not article.get('description'):
                    continue
                
                # Combine title and description for better analysis
                title = article.get('title', '').strip()
                description = article.get('description', '').strip()
                content = article.get('content', '').strip()
                
                # Create full text (prioritize description over content)
                text_parts = []
                if title:
                    text_parts.append(title)
                if description:
                    text_parts.append(description)
                elif content:
                    # Use content if no description, but clean it
                    content_clean = content.split('[+')[0].strip()  # Remove "read more" parts
                    if content_clean:
                        text_parts.append(content_clean)
                
                full_text = '. '.join(text_parts)
                
                # Skip if text is too short
                if len(full_text) < 20:
                    continue
                
                processed_article = {
                    'text': full_text,
                    'title': title,
                    'description': description or content,
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', '')
                }
                
                processed_articles.append(processed_article)
            
            return processed_articles
        
        except requests.exceptions.Timeout:
            raise Exception('Request timed out. Please try again.')
        except requests.exceptions.RequestException as e:
            raise Exception(f'Network error: {str(e)}')
        except Exception as e:
            if 'News API' in str(e):
                raise
            raise Exception(f'Error scraping news: {str(e)}')
