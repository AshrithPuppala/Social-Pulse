from flask import Flask, request
import os
from utils.twitter_scraper import TwitterScraper
from utils.instagram_scraper import InstagramScraper
from utils.news_scraper import NewsScraper
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.html_generator import generate_html_page
import concurrent.futures
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize scrapers
twitter_scraper = TwitterScraper(
    bearer_token=os.environ.get('TWITTER_BEARER_TOKEN')
)

instagram_scraper = InstagramScraper(
    rapidapi_key=os.environ.get('RAPIDAPI_KEY')
)

news_scraper = NewsScraper(
    api_key=os.environ.get('NEWS_API_KEY')
)

sentiment_analyzer = SentimentAnalyzer()

def get_available_platforms():
    """Get list of configured platforms"""
    platforms = []
    if twitter_scraper.is_configured():
        platforms.append('twitter')
    if instagram_scraper.is_configured():
        platforms.append('instagram')
    if news_scraper.is_configured():
        platforms.append('news')
    return platforms

@app.route('/')
def index():
    available_platforms = get_available_platforms()
    html = generate_html_page(
        available_platforms=available_platforms,
        results=None,
        error=None,
        topic=None
    )
    return html

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        topic = request.form.get('topic', '').strip()
        platforms = request.form.getlist('platforms')
        
        if not topic:
            html = generate_html_page(
                available_platforms=get_available_platforms(),
                error='Please enter a topic',
                results=None,
                topic=topic
            )
            return html
        
        if not platforms:
            html = generate_html_page(
                available_platforms=get_available_platforms(),
                error='Please select at least one platform',
                results=None,
                topic=topic
            )
            return html
        
        results = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'platforms': {},
            'overall': {
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_posts': 0
            }
        }
        
        # Scrape data from selected platforms in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            
            if 'twitter' in platforms and twitter_scraper.is_configured():
                futures['twitter'] = executor.submit(twitter_scraper.scrape, topic)
            
            if 'instagram' in platforms and instagram_scraper.is_configured():
                futures['instagram'] = executor.submit(instagram_scraper.scrape, topic)
            
            if 'news' in platforms and news_scraper.is_configured():
                futures['news'] = executor.submit(news_scraper.scrape, topic)
            
            # Collect results
            for platform, future in futures.items():
                try:
                    posts = future.result(timeout=30)
                    
                    # Analyze sentiment for each post
                    analyzed_posts = []
                    positive_count = 0
                    negative_count = 0
                    neutral_count = 0
                    
                    for post in posts:
                        sentiment = sentiment_analyzer.analyze(post['text'])
                        post['sentiment'] = sentiment['label']
                        post['confidence'] = sentiment['score']
                        analyzed_posts.append(post)
                        
                        if sentiment['label'] == 'positive':
                            positive_count += 1
                        elif sentiment['label'] == 'negative':
                            negative_count += 1
                        else:
                            neutral_count += 1
                    
                    total = len(analyzed_posts)
                    
                    results['platforms'][platform] = {
                        'posts': analyzed_posts[:50],
                        'total_posts': total,
                        'positive_count': positive_count,
                        'negative_count': negative_count,
                        'neutral_count': neutral_count,
                        'positive_percentage': round((positive_count / total * 100) if total > 0 else 0, 2),
                        'negative_percentage': round((negative_count / total * 100) if total > 0 else 0, 2),
                        'neutral_percentage': round((neutral_count / total * 100) if total > 0 else 0, 2)
                    }
                    
                    # Update overall stats
                    results['overall']['positive_count'] += positive_count
                    results['overall']['negative_count'] += negative_count
                    results['overall']['neutral_count'] += neutral_count
                    results['overall']['total_posts'] += total
                    
                except Exception as e:
                    results['platforms'][platform] = {
                        'error': str(e),
                        'total_posts': 0
                    }
        
        # Calculate overall percentages
        total = results['overall']['total_posts']
        if total > 0:
            results['overall']['positive_percentage'] = round(
                (results['overall']['positive_count'] / total * 100), 2
            )
            results['overall']['negative_percentage'] = round(
                (results['overall']['negative_count'] / total * 100), 2
            )
            results['overall']['neutral_percentage'] = round(
                (results['overall']['neutral_count'] / total * 100), 2
            )
        else:
            results['overall']['positive_percentage'] = 0
            results['overall']['negative_percentage'] = 0
            results['overall']['neutral_percentage'] = 0
        
        # Get extreme examples
        all_posts = []
        for platform_data in results['platforms'].values():
            if 'posts' in platform_data:
                all_posts.extend(platform_data['posts'])
        
        # Sort by confidence and get extreme examples
        positive_posts = [p for p in all_posts if p['sentiment'] == 'positive']
        negative_posts = [p for p in all_posts if p['sentiment'] == 'negative']
        
        positive_posts.sort(key=lambda x: x['confidence'], reverse=True)
        negative_posts.sort(key=lambda x: x['confidence'], reverse=True)
        
        results['extreme_examples'] = {
            'most_positive': positive_posts[:5],
            'most_negative': negative_posts[:5]
        }
        
        html = generate_html_page(
            available_platforms=get_available_platforms(),
            results=results,
            error=None,
            topic=topic
        )
        return html
        
    except Exception as e:
        html = generate_html_page(
            available_platforms=get_available_platforms(),
            error=f'Analysis failed: {str(e)}',
            results=None,
            topic=request.form.get('topic', '')
        )
        return html

@app.route('/health')
def health():
    available = get_available_platforms()
    return {
        'status': 'healthy',
        'available_platforms': available
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
