from textblob import TextBlob
import re

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer using TextBlob (lightweight, no ML models needed)"""
        pass
    
    def clean_text(self, text):
        """Clean text for sentiment analysis"""
        if not text:
            return ''
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', str(text))
        # Remove mentions and hashtags symbols (keep the words)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def analyze(self, text):
        """
        Analyze sentiment of text using TextBlob
        Returns: dict with 'label' (positive/negative/neutral) and 'score' (confidence)
        """
        try:
            # Clean text
            cleaned_text = self.clean_text(text)
            
            if not cleaned_text or len(cleaned_text) < 3:
                return {'label': 'neutral', 'score': 0.5}
            
            # Analyze with TextBlob
            blob = TextBlob(cleaned_text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Determine sentiment label and confidence
            if polarity > 0.1:
                label = 'positive'
                score = min(abs(polarity), 1.0)
            elif polarity < -0.1:
                label = 'negative'
                score = min(abs(polarity), 1.0)
            else:
                label = 'neutral'
                score = 1.0 - abs(polarity)
            
            # Boost confidence if text is very subjective (strong opinion)
            if subjectivity > 0.7:
                score = min(score * 1.2, 1.0)
            
            return {
                'label': label,
                'score': round(score, 3)
            }
        
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            # Fallback to simple keyword matching
            return self._simple_sentiment(text)
    
    def _simple_sentiment(self, text):
        """Simple fallback sentiment analysis using keyword matching"""
        if not text:
            return {'label': 'neutral', 'score': 0.5}
        
        text_lower = str(text).lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'love', 'best', 'wonderful',
            'fantastic', 'awesome', 'happy', 'perfect', 'beautiful', 'incredible',
            'brilliant', 'outstanding', 'superb', 'terrific', 'fabulous', 'nice'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'worst', 'hate', 'horrible', 'poor',
            'disappointing', 'sad', 'angry', 'useless', 'pathetic', 'disgusting',
            'annoying', 'frustrating', 'ugly', 'stupid', 'boring', 'waste'
        ]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {'label': 'positive', 'score': 0.75}
        elif negative_count > positive_count:
            return {'label': 'negative', 'score': 0.75}
        else:
            return {'label': 'neutral', 'score': 0.6}
