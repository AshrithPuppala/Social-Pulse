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
            articles = news_scraper.scrape(topic, limit=100)
        except Exception as e:
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error=str(e),
                results=None,
                topic=topic
            )
            return html
        
        if not articles:
            html = generate_html_page(
                is_configured=news_scraper.is_configured(),
                error=f'No news articles found for "{topic}". Try a different topic or broader search terms.',
                results=None,
                topic=topic
            )
            return html
        
        # Analyze sentiment for each article
        analyzed_articles = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in articles:
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
            'articles': analyzed_articles[:100],  # Limit display to 100
            'total_articles': total,
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
