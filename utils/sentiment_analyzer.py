from textblob import TextBlob
import re

class SentimentAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            import nltk
            nltk.download('brown', quiet=True)
            nltk.download('punkt', quiet=True)
        except:
            pass
    
    def clean_text(self, text):
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def analyze(self, text):
        if not text or len(text.strip()) == 0:
            return {
                'label': 'neutral',
                'score': 0.0,
                'polarity': 0.0,
                'subjectivity': 0.0
            }
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Analyze with TextBlob
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment
        if polarity > 0.1:
            label = 'positive'
            score = min(abs(polarity), 1.0)
        elif polarity < -0.1:
            label = 'negative'
            score = min(abs(polarity), 1.0)
        else:
            label = 'neutral'
            score = 1.0 - abs(polarity)
        
        return {
            'label': label,
            'score': round(score, 3),
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3)
        }
    
    def batch_analyze(self, texts):
        return [self.analyze(text) for text in texts]
