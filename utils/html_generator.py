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
            margin-bottom: 20px;
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
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .platform-selection {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 15px;
        }

        .platform-checkbox {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        .platform-checkbox input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .platform-status {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
        }

        .info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
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
        }

        .bar-negative {
            background: #f45c43;
        }

        .bar-neutral {
            background: #00f2fe;
        }

        .platform-result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .platform-result h3 {
            margin-bottom: 15px;
            color: #667eea;
            font-size: 1.5rem;
        }

        .platform-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .platform-stat {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .platform-stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #667eea;
        }

        .platform-stat-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
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
        }

        .post-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }

        .post-card.positive {
            border-left-color: #38ef7d;
        }

        .post-card.negative {
            border-left-color: #f45c43;
        }

        .post-text {
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .post-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #666;
            flex-wrap: wrap;
            gap: 10px;
        }

        .post-author {
            font-weight: 600;
        }

        .post-platform {
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
        }

        .post-confidence {
            color: #38ef7d;
            font-weight: 600;
        }

        .error {
            background: #f45c43;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
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
            
            .platform-selection {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    """

def generate_form(available_platforms, topic):
    """Generate form HTML using Python"""
    topic_value = escape_html(topic) if topic else ''
    
    platform_checkboxes = []
    for platform in ['twitter', 'instagram']:
        display_name = 'Twitter / X' if platform == 'twitter' else platform.capitalize()
        checked = 'checked' if platform in available_platforms else ''
        disabled = '' if platform in available_platforms else 'disabled'
        
        checkbox_html = f'''
            <label class="platform-checkbox">
                <input type="checkbox" name="platforms" value="{platform}" {checked} {disabled}>
                <span>{display_name}</span>
            </label>
        '''
        platform_checkboxes.append(checkbox_html)
    
    platform_status = ''
    if available_platforms:
        platforms_list = ', '.join([p.capitalize() for p in available_platforms])
        platform_status = f'''
            <div class="platform-status info">
                ✓ Available platforms: {platforms_list}
            </div>
        '''
    
    form_html = f'''
        <div class="search-section">
            <form method="POST" action="/analyze">
                <div class="input-group">
                    <input 
                        type="text" 
                        name="topic"
                        placeholder="Enter a topic (e.g., climate change, AI, bitcoin)"
                        required
                        value="{topic_value}"
                    >
                    <button type="submit">Analyze</button>
                </div>
                
                <div class="platform-selection">
                    {"".join(platform_checkboxes)}
                </div>

                {platform_status}
            </form>
        </div>
    '''
    return form_html

def generate_results_html(results, topic):
    """Generate results section using Python"""
    if not results:
        return ''
    
    overall = results['overall']
    
    # Overall stats cards
    stats_html = f'''
        <div class="results">
            <div class="overall-stats">
                <h2>Overall Sentiment for "{escape_html(topic)}"</h2>
                <div class="stats-grid">
                    <div class="stat-card positive">
                        <div class="stat-value">{overall['positive_percentage']:.1f}%</div>
                        <div class="stat-label">Positive</div>
                    </div>
                    <div class="stat-card negative">
                        <div class="stat-value">{overall['negative_percentage']:.1f}%</div>
                        <div class="stat-label">Negative</div>
                    </div>
                    <div class="stat-card neutral">
                        <div class="stat-value">{overall['neutral_percentage']:.1f}%</div>
                        <div class="stat-label">Neutral</div>
                    </div>
                    <div class="stat-card total">
                        <div class="stat-value">{overall['total_posts']}</div>
                        <div class="stat-label">Total Posts</div>
                    </div>
                </div>
                
                <div class="sentiment-bar">
                    <div class="bar-positive" style="width: {overall['positive_percentage']}%"></div>
                    <div class="bar-negative" style="width: {overall['negative_percentage']}%"></div>
                    <div class="bar-neutral" style="width: {overall['neutral_percentage']}%"></div>
                </div>
            </div>
    '''
    
    # Platform-specific results
    for platform, data in results['platforms'].items():
        platform_name = platform.capitalize()
        
        if 'error' in data:
            stats_html += f'''
                <div class="platform-result">
                    <h3>{platform_name}</h3>
                    <p style="color: #f45c43;">Error: {escape_html(data['error'])}</p>
                </div>
            '''
        else:
            stats_html += f'''
                <div class="platform-result">
                    <h3>{platform_name}</h3>
                    <div class="platform-stats">
                        <div class="platform-stat">
                            <div class="platform-stat-value">{data['positive_percentage']:.1f}%</div>
                            <div class="platform-stat-label">Positive</div>
                        </div>
                        <div class="platform-stat">
                            <div class="platform-stat-value">{data['negative_percentage']:.1f}%</div>
                            <div class="platform-stat-label">Negative</div>
                        </div>
                        <div class="platform-stat">
                            <div class="platform-stat-value">{data['neutral_percentage']:.1f}%</div>
                            <div class="platform-stat-label">Neutral</div>
                        </div>
                        <div class="platform-stat">
                            <div class="platform-stat-value">{data['total_posts']}</div>
                            <div class="platform-stat-label">Total Posts</div>
                        </div>
                    </div>
                </div>
            '''
    
    # Extreme examples
    positive_posts_html = generate_posts_html(results['extreme_examples']['most_positive'], 'positive')
    negative_posts_html = generate_posts_html(results['extreme_examples']['most_negative'], 'negative')
    
    stats_html += f'''
            <div class="extreme-examples">
                <div class="extreme-section">
                    <h3>🌟 Most Positive Opinions</h3>
                    {positive_posts_html}
                </div>
                <div class="extreme-section">
                    <h3>⚠️ Most Negative Opinions</h3>
                    {negative_posts_html}
                </div>
            </div>
        </div>
    '''
    
    return stats_html

def generate_posts_html(posts, sentiment_type):
    """Generate HTML for posts list"""
    if not posts:
        return '<p style="color: #666;">No posts found</p>'
    
    posts_html = []
    for post in posts:
        text = post['text']
        truncated_text = text[:200] + '...' if len(text) > 200 else text
        confidence = post['confidence'] * 100
        
        post_html = f'''
            <div class="post-card {escape_html(sentiment_type)}">
                <div class="post-text">{escape_html(truncated_text)}</div>
                <div class="post-meta">
                    <span class="post-author">@{escape_html(post['author'])}</span>
                    <span class="post-platform">{escape_html(post['platform'])}</span>
                    <span class="post-confidence">Confidence: {confidence:.1f}%</span>
                </div>
            </div>
        '''
        posts_html.append(post_html)
    
    return ''.join(posts_html)

def generate_html_page(available_platforms, results, error, topic):
    """Main function to generate complete HTML page using only Python"""
    
    css = generate_css()
    form_html = generate_form(available_platforms, topic)
    results_html = generate_results_html(results, topic) if results else ''
    error_html = f'<div class="error">{escape_html(error)}</div>' if error else ''
    
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Pulse Calculator</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Social Pulse Calculator</h1>
            <p class="subtitle">Real-time sentiment analysis across social media platforms</p>
        </header>

        {form_html}
        {results_html}
        {error_html}
    </div>
</body>
</html>'''
    
    return full_html
