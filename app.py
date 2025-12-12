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

# More balanced credible sources list
CREDIBLE_SOURCES = {
    # Major International News
    'BBC News', 'Reuters', 'The Associated Press', 'Associated Press', 'AP News',
    'The New York Times', 'The Washington Post', 'The Guardian', 'CNN', 'Al Jazeera English',
    'Financial Times', 'Bloomberg', 'The Wall Street Journal', 'NPR', 'ABC News',
    'CBS News', 'NBC News', 'PBS', 'TIME', 'Politico', 'The Atlantic', 'The Economist',
    
    # Indian News
    'The Times of India', 'The Hindu', 'Hindustan Times', 'Indian Express',
    'NDTV', 'The Economic Times', 'Business Standard', 'Mint', 'ThePrint',
    'The Wire', 'Scroll.in', 'News18', 'India Today', 'FirstPost',
    
    # Tech & Business  
    'TechCrunch', 'Ars Technica', 'The Verge', 'Wired', 'Forbes',
    'Business Insider', 'CNBC', 'MarketWatch', 'Fortune', 'Fast Company',
    'VentureBeat', 'Engadget', 'ZDNet', 'CNET', 'TechRadar', 'The Next Web',
    
    # Science & Specialized
    'Nature', 'Science', 'New Scientist', 'Scientific American',
    'National Geographic', 'Smithsonian', 'Live Science', 'Space.com',
    
    # Sports
    'ESPN', 'Sports Illustrated', 'The Athletic', 'Sky Sports', 'BBC Sport',
    
    # Entertainment & Culture
    'Variety', 'The Hollywood Reporter', 'Entertainment Weekly', 'Rolling Stone',
    'Billboard', 'Pitchfork', 'IGN', 'GameSpot', 'Polygon'
}

def is_credible_source(source_name):
    """Check if a source is credible"""
    if not source_name:
        return False
    
    source_lower = source_name.lower().strip()
    
    # Check for exact or partial matches
    for credible in CREDIBLE_SOURCES:
        credible_lower = credible.lower()
        if credible_lower == source_lower:
            return True
        if credible_lower in source_lower or source_lower in credible_lower:
            return True
    
    # Allow sources with .com, .org, .net extensions (common for news sites)
    # but exclude obvious spam/low quality domains
    spam_indicators = ['blog', 'wordpress', 'medium.com', 'tumblr', 'facebook', 'twitter']
    if any(indicator in source_lower for indicator in spam_indicators):
        return False
    
    return False

def check_relevance(article, topic):
    """Check if article is relevant to the topic"""
    topic_lower = topic.lower()
    text_lower = article.get('text', '').lower()
    title_lower = article.get('title', '').lower()
    
    # Topic keywords
    topic_words = set(topic_lower.split())
    
    # Count how many topic words appear in title or text
    matches_in_title = sum(1 for word in topic_words if len(word) > 2 and word in title_lower)
    matches_in_text = sum(1 for word in topic_words if len(word) > 2 and word in text_lower)
    
    # Article is relevant if topic words appear in title or multiple times in text
    if matches_in_title > 0 or matches_in_text >= 2:
        return True
    
    # Also check for full topic phrase
    if topic_lower in title_lower or topic_lower in text_lower:
        return True
    
    return False

def validate_article_quality(article):
    """Validate that article has meaningful content"""
    text = article.get('text', '')
    
    # Minimum length check
    if len(text) < 30:
        return False
    
    # Must have some sentence structure
    if '. ' not in text and len(text) < 80:
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
                error=f'No news articles found for "{topic}". Try different keywords or a broader topic.',
                results=None,
                topic=topic
            )
            return html
        
        # Filter for quality and relevance
        quality_articles = []
        for article in all_articles:
            # Check quality first
            if not validate_article_quality(article):
                continue
            
            # Check relevance to topic
            if not check_relevance(article, topic):
                continue
            
            # Check if source is credible (more lenient now)
            if is_credible_source(article.get('source', '')):
                quality_articles.append(article)
        
        # If credible filter is too strict, fall back to all relevant articles
        if len(quality_articles) < 5:
            quality_articles = [a for a in all_articles 
                              if validate_article_quality(a) and check_relevance(a, topic)]
        
        if not quality_articles:
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error=f'No relevant news articles found for "{topic}". Try using different keywords or a more specific/general topic.',
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
        
        # Get extreme examples
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
