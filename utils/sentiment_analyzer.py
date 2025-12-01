from transformers import pipeline
import torch

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analysis pipeline"""
        try:
            # Use a smaller, faster model for sentiment analysis
            self.analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU
            )
        except Exception as e:
            print(f"Error loading sentiment model: {e}")
            self.analyzer = None
    
    def analyze(self, text):
        """
        Analyze sentiment of text
        Returns: dict with 'label' (positive/negative/neutral) and 'score' (confidence)
        """
        if not self.analyzer:
            # Fallback simple sentiment if model fails
            return self._simple_sentiment(text)
        
        try:
            # Clean and truncate text
            text = text.strip()[:512]  # Limit to 512 chars for speed
            
            if not text or len(text) < 3:
                return {'label': 'neutral', 'score': 0.5}
            
            # Get sentiment
            result = self.analyzer(text)[0]
            
            # Convert to our format
            label = result['label'].lower()
            score = result['score']
            
            # Map LABEL to positive/negative
            if label == 'positive':
                sentiment_label = 'positive'
            elif label == 'negative':
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
            
            # If confidence is low, mark as neutral
            if score < 0.6:
                sentiment_label = 'neutral'
            
            return {
                'label': sentiment_label,
                'score': score
            }
        
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return self._simple_sentiment(text)
    
    def _simple_sentiment(self, text):
        """Simple fallback sentiment analysis using keyword matching"""
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'wonderful', 
                         'fantastic', 'awesome', 'happy', 'perfect', 'beautiful', 'incredible']
        negative_words = ['bad', 'terrible', 'awful', 'worst', 'hate', 'horrible', 'poor',
                         'disappointing', 'sad', 'angry', 'useless', 'pathetic', 'disgusting']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {'label': 'positive', 'score': 0.7}
        elif negative_count > positive_count:
            return {'label': 'negative', 'score': 0.7}
        else:
            return {'label': 'neutral', 'score': 0.6}
