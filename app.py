from flask import Flask, request
import os
from utils.news_scraper import NewsScraper
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.html_generator import generate_html_page
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize scraper and analyzer
news_scraper = NewsScraper(
    api_key=os.environ.get('NEWS_API_KEY')
)

sentiment_analyzer = SentimentAnalyzer()

# Credible news sources - major established outlets
CREDIBLE_SOURCES = {
    # International News
    'BBC News', 'Reuters', 'The Associated Press', 'The New York Times', 'The Washington Post',
    'The Guardian', 'CNN', 'Al Jazeera English', 'Financial Times', 'Bloomberg',
    'The Wall Street Journal', 'NPR', 'PBS NewsHour', 'The Economist', 'TIME',
    'Politico', 'The Atlantic', 'Foreign Policy', 'The Independent',
    
    # Indian News
    'The Times of India', 'The Hindu', 'Hindustan Times', 'Indian Express',
    'NDTV', 'The Economic Times', 'Business Standard', 'Mint', 'ThePrint',
    'The Wire', 'Scroll.in', 'News18', 'India Today', 'First Post',
    
    # Tech & Business
    'TechCrunch', 'Ars Technica', 'The Verge', 'Wired', 'Forbes',
    'Business Insider', 'CNBC', 'MarketWatch', 'Fortune',
    
    # Science & Health
    'Nature', 'Science Magazine', 'New Scientist', 'Scientific American',
    'National Geographic', 'Smithsonian Magazine'
}

def is_credible_source(source_name):
    """Check if a source is in our credible list"""
    if not source_name:
        return False
    
    source_lower = source_name.lower()
    
    # Check exact matches (case insensitive)
    for credible in CREDIBLE_SOURCES:
        if credible.lower() == source_lower:
            return True
        # Also check if credible source is contained in the name
        if credible.lower() in source_lower or source_lower in credible.lower():
            return True
    
    return False

def filter_credible_articles(articles):
    """Filter articles to only include credible sources"""
    credible_articles = []
    filtered_out = []
    
    for article in articles:
        source = article.get('source', 'Unknown')
        if is_credible_source(source):
            credible_articles.append(article)
        else:
            filtered_out.append(source)
    
    return credible_articles, filtered_out

def validate_article_quality(article):
    """Validate that article has meaningful content"""
    text = article.get('text', '')
    
    # Filter out articles with insufficient content
    if len(text) < 50:
        return False
    
    # Filter out articles that are just headlines without description
    if '. ' not in text and len(text) < 100:
        return False
    
    # Filter out common spam patterns
    spam_patterns = [
        'click here', 'subscribe now', 'sign up', 'download app',
        'watch video', 'see more', 'read full story here'
    ]
    
    text_lower = text.lower()
    spam_count = sum(1 for pattern in spam_patterns if pattern in text_lower)
    
    # If article is mostly spam/promotional content
    if spam_count > 2:
        return False
    
    return True

@app.route('/')
def index():
    is_configured = news_scraper.is_configured()
    html = generate_html_page(
        is_configured=is_configured,
        results=None,
        error=None,
        topic=None
    )
    return html

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        topic = request.form.get('topic', '').strip()
        
        if not topic:
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error='Please enter a topic to analyze',
                results=None,
                topic=topic
            )
            return html
        
        if not news_scraper.is_configured():
            html = generate_html_page(
                is_configured=False,
                error='News API is not configured. Please add your NEWS_API_KEY to environment variables.',
                results=None,
                topic=topic
            )
            return html
        
        # Scrape news articles
        try:
            all_articles = news_scraper.scrape(topic, limit=100)
        except Exception as e:
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error=str(e),
                results=None,
                topic=topic
            )
            return html
        
        if not all_articles:
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error=f'No news articles found for "{topic}". Try a different topic or broader search terms.',
                results=None,
                topic=topic
            )
            return html
        
        # Filter for credible sources only
        credible_articles, filtered_sources = filter_credible_articles(all_articles)
        
        # Validate article quality
        quality_articles = [a for a in credible_articles if validate_article_quality(a)]
        
        if not quality_articles:
            error_msg = f'No credible news articles found for "{topic}". '
            if filtered_sources:
                error_msg += 'Try a more mainstream topic covered by major news outlets.'
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error=error_msg,
                results=None,
                topic=topic
            )
            return html
        
        # Analyze sentiment for each article
        analyzed_articles = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in quality_articles:
            sentiment = sentiment_analyzer.analyze(article['text'])
            article['sentiment'] = sentiment['label']
            article['confidence'] = sentiment['score']
            analyzed_articles.append(article)
            
            if sentiment['label'] == 'positive':
                positive_count += 1
            elif sentiment['label'] == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(analyzed_articles)
        
        # Prepare results
        results = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'articles': analyzed_articles[:100],
            'total_articles': total,
            'total_found': len(all_articles),
            'filtered_count': len(all_articles) - total,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_percentage': round((positive_count / total * 100) if total > 0 else 0, 2),
            'negative_percentage': round((negative_count / total * 100) if total > 0 else 0, 2),
            'neutral_percentage': round((neutral_count / total * 100) if total > 0 else 0, 2)
        }
        
        # Get extreme examples (only from quality articles)
        positive_articles = [a for a in analyzed_articles if a['sentiment'] == 'positive']
        negative_articles = [a for a in analyzed_articles if a['sentiment'] == 'negative']
        
        positive_articles.sort(key=lambda x: x['confidence'], reverse=True)
        negative_articles.sort(key=lambda x: x['confidence'], reverse=True)
        
        results['extreme_examples'] = {
            'most_positive': positive_articles[:5],
            'most_negative': negative_articles[:5]
        }
        
        # Get source distribution
        source_counts = {}
        for article in analyzed_articles:
            source = article.get('source', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Sort sources by count
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        results['top_sources'] = top_sources
        
        html = generate_html_page(
            is_configured=news_scraper.is_configured(),
            results=results,
            error=None,
            topic=topic
        )
        return html
        
    except Exception as e:
        html = generate_html_page(
            is_configured=news_scraper.is_configured(),
            error=f'Analysis failed: {str(e)}',
            results=None,
            topic=request.form.get('topic', '')
        )
        return html

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'news_api_configured': news_scraper.is_configured()
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
