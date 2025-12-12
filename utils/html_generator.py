def escape_html(text):
    """Escape HTML special characters"""
    if text is None:
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def generate_css():
    """Generate CSS as Python string"""
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .search-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }

        input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .info-box {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }

        .warning-box {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }

        .results {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            color: white;
        }

        .stat-card.positive {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }

        .stat-card.negative {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }

        .stat-card.neutral {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }

        .stat-card.total {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 1rem;
            opacity: 0.9;
        }

        .sentiment-bar {
            height: 40px;
            display: flex;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 30px;
        }

        .bar-positive {
            background: #38ef7d;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
        }

        .bar-negative {
            background: #f45c43;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
        }

        .bar-neutral {
            background: #00f2fe;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
        }

        .sources-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .sources-section h3 {
            margin-bottom: 15px;
            color: #667eea;
        }

        .source-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
        }

        .source-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            background: white;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }

        .source-name {
            font-weight: 500;
            color: #333;
        }

        .source-count {
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .extreme-examples {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }

        .extreme-section h3 {
            margin-bottom: 15px;
            font-size: 1.3rem;
            color: #333;
        }

        .article-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }

        .article-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .article-card.positive {
            border-left-color: #38ef7d;
        }

        .article-card.negative {
            border-left-color: #f45c43;
        }

        .article-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
            line-height: 1.4;
        }

        .article-text {
            margin-bottom: 15px;
            line-height: 1.6;
            color: #555;
        }

        .article-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: #666;
            flex-wrap: wrap;
            gap: 10px;
        }

        .article-source {
            font-weight: 600;
            color: #667eea;
        }

        .article-confidence {
            background: #38ef7d;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 600;
        }

        .article-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }

        .article-link:hover {
            text-decoration: underline;
        }

        .error {
            background: #f45c43;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-size: 1.1rem;
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 2rem;
            }
            
            .extreme-examples {
                grid-template-columns: 1fr;
            }
            
            .input-group {
                flex-direction: column;
            }

            .source-list {
                grid-template-columns: 1fr;
            }
        }
    """

def generate_form(is_configured, topic):
    """Generate form HTML using Python"""
    topic_value = escape_html(topic) if topic else ''
    
    status_html = ''
    if is_configured:
        status_html = '''
            <div class="info-box">
                ✓ News API is configured and ready to analyze news articles
            </div>
        '''
    else:
        status_html = '''
            <div class="warning-box">
                ⚠️ News API is not configured. Please set your NEWS_API_KEY environment variable.
                <br><br>
                Get your free API key at: <a href="https://newsapi.org" target="_blank" style="color: #856404; font-weight: bold;">newsapi.org</a>
            </div>
        '''
    
    form_html = f'''
        <div class="search-section">
            <form method="POST" action="/analyze">
                <div class="input-group">
                    <input 
                        type="text" 
                        name="topic"
                        placeholder="Enter a topic to analyze (e.g., climate change, artificial intelligence, cryptocurrency)"
                        required
                        value="{topic_value}"
                    >
                    <button type="submit">Analyze News</button>
                </div>
                {status_html}
            </form>
        </div>
    '''
    return form_html

def generate_results_html(results, topic):
    """Generate results section using Python"""
    if not results:
        return ''
    
    # Overall stats cards
    stats_html = f'''
        <div class="results">
            <div class="overall-stats">
                <h2>News Sentiment Analysis for "{escape_html(topic)}"</h2>
                <p style="color: #666; margin-bottom: 20px;">Analyzed {results['total_articles']} news articles</p>
                
                <div class="stats-grid">
                    <div class="stat-card positive">
                        <div class="stat-value">{results['positive_percentage']:.1f}%</div>
                        <div class="stat-label">Positive Coverage</div>
                    </div>
                    <div class="stat-card negative">
                        <div class="stat-value">{results['negative_percentage']:.1f}%</div>
                        <div class="stat-label">Negative Coverage</div>
                    </div>
                    <div class="stat-card neutral">
                        <div class="stat-value">{results['neutral_percentage']:.1f}%</div>
                        <div class="stat-label">Neutral Coverage</div>
                    </div>
                    <div class="stat-card total">
                        <div class="stat-value">{results['total_articles']}</div>
                        <div class="stat-label">Total Articles</div>
                    </div>
                </div>
                
                <div class="sentiment-bar">
                    <div class="bar-positive" style="width: {results['positive_percentage']}%">
                        {results['positive_percentage']:.0f}%
                    </div>
                    <div class="bar-negative" style="width: {results['negative_percentage']}%">
                        {results['negative_percentage']:.0f}%
                    </div>
                    <div class="bar-neutral" style="width: {results['neutral_percentage']}%">
                        {results['neutral_percentage']:.0f}%
                    </div>
                </div>
            </div>
    '''
    
    # Top sources section
    if results.get('top_sources'):
        stats_html += '''
            <div class="sources-section">
                <h3>📰 Top News Sources</h3>
                <div class="source-list">
        '''
        
        for source, count in results['top_sources']:
            stats_html += f'''
                <div class="source-item">
                    <span class="source-name">{escape_html(source)}</span>
                    <span class="source-count">{count}</span>
                </div>
            '''
        
        stats_html += '''
                </div>
            </div>
        '''
    
    # Extreme examples
    positive_articles_html = generate_articles_html(results['extreme_examples']['most_positive'], 'positive')
    negative_articles_html = generate_articles_html(results['extreme_examples']['most_negative'], 'negative')
    
    stats_html += f'''
            <div class="extreme-examples">
                <div class="extreme-section">
                    <h3>🌟 Most Positive Coverage</h3>
                    {positive_articles_html}
                </div>
                <div class="extreme-section">
                    <h3>⚠️ Most Negative Coverage</h3>
                    {negative_articles_html}
                </div>
            </div>
        </div>
    '''
    
    return stats_html

def generate_articles_html(articles, sentiment_type):
    """Generate HTML for articles list"""
    if not articles:
        return '<p style="color: #666;">No articles found</p>'
    
    articles_html = []
    for article in articles:
        text = article['text']
        
        # Split title and description
        parts = text.split('. ', 1)
        title = parts[0]
        description = parts[1] if len(parts) > 1 else ''
        
        # Truncate description
        if len(description) > 150:
            description = description[:150] + '...'
        
        confidence = article['confidence'] * 100
        source = article.get('source', 'Unknown')
        url = article.get('url', '')
        
        article_html = f'''
            <div class="article-card {escape_html(sentiment_type)}">
                <div class="article-title">{escape_html(title)}</div>
                {f'<div class="article-text">{escape_html(description)}</div>' if description else ''}
                <div class="article-meta">
                    <span class="article-source">{escape_html(source)}</span>
                    <span class="article-confidence">Confidence: {confidence:.0f}%</span>
                    {f'<a href="{escape_html(url)}" target="_blank" class="article-link">Read More →</a>' if url else ''}
                </div>
            </div>
        '''
        articles_html.append(article_html)
    
    return ''.join(articles_html)

def generate_html_page(is_configured, results, error, topic):
    """Main function to generate complete HTML page using only Python"""
    
    css = generate_css()
    form_html = generate_form(is_configured, topic)
    results_html = generate_results_html(results, topic) if results else ''
    error_html = f'<div class="error">❌ {escape_html(error)}</div>' if error else ''
    
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Sentiment Analyzer</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 News Sentiment Analyzer</h1>
            <p class="subtitle">Real-time sentiment analysis of global news coverage</p>
        </header>

        {form_html}
        {results_html}
        {error_html}
    </div>
</body>
</html>'''
    
    return full_html
