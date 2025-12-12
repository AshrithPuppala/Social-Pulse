from textblob import TextBlob
import re

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer using TextBlob with enhanced accuracy"""
        # Enhanced word lists for better detection
        self.strong_positive = [
            'excellent', 'outstanding', 'exceptional', 'brilliant', 'fantastic',
            'wonderful', 'amazing', 'incredible', 'perfect', 'superb', 'triumph',
            'revolutionary', 'breakthrough', 'phenomenal', 'magnificent'
        ]
        
        self.strong_negative = [
            'terrible', 'horrible', 'awful', 'disaster', 'catastrophe', 'crisis',
            'devastating', 'tragic', 'worst', 'failed', 'failure', 'collapsed',
            'corruption', 'scandal', 'controversial', 'criticized', 'condemned',
            'threat', 'dangerous', 'risk', 'concern', 'alarm', 'warning'
        ]
        
        # Negative context words that should increase negative weight
        self.negative_context = [
            'death', 'killed', 'died', 'war', 'attack', 'violence', 'conflict',
            'protest', 'riot', 'injured', 'victim', 'loss', 'damage', 'destroy',
            'fire', 'flood', 'earthquake', 'storm', 'pandemic', 'disease'
        ]
        
        # Positive context words
        self.positive_context = [
            'success', 'win', 'victory', 'achievement', 'growth', 'improve',
            'innovation', 'progress', 'advance', 'celebrate', 'honor', 'award',
            'recovery', 'solution', 'agreement', 'peace', 'cooperation'
        ]
    
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
    
    def check_word_presence(self, text_lower, word_list):
        """Check how many words from a list are present in text"""
        return sum(1 for word in word_list if word in text_lower)
    
    def analyze(self, text):
        """
        Analyze sentiment of text using TextBlob with enhanced accuracy
        Returns: dict with 'label' (positive/negative/neutral) and 'score' (confidence)
        """
        try:
            # Clean text
            cleaned_text = self.clean_text(text)
            
            if not cleaned_text or len(cleaned_text) < 3:
                return {'label': 'neutral', 'score': 0.5}
            
            text_lower = cleaned_text.lower()
            
            # Analyze with TextBlob
            blob = TextBlob(cleaned_text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Check for strong sentiment words
            strong_pos_count = self.check_word_presence(text_lower, self.strong_positive)
            strong_neg_count = self.check_word_presence(text_lower, self.strong_negative)
            
            # Check for context words
            pos_context_count = self.check_word_presence(text_lower, self.positive_context)
            neg_context_count = self.check_word_presence(text_lower, self.negative_context)
            
            # Adjust polarity based on context and strong words
            context_adjustment = 0
            
            # Strong words have more weight
            if strong_pos_count > 0:
                context_adjustment += 0.15 * strong_pos_count
            if strong_neg_count > 0:
                context_adjustment -= 0.15 * strong_neg_count
            
            # Context words add moderate weight
            if pos_context_count > 0:
                context_adjustment += 0.08 * pos_context_count
            if neg_context_count > 0:
                context_adjustment -= 0.08 * neg_context_count
            
            # Apply context adjustment
            adjusted_polarity = polarity + context_adjustment
            adjusted_polarity = max(-1, min(1, adjusted_polarity))  # Clamp to [-1, 1]
            
            # More sensitive thresholds for better classification
            if adjusted_polarity > 0.05:  # Lowered from 0.1
                label = 'positive'
                # Calculate confidence based on adjusted polarity
                score = min(abs(adjusted_polarity) * 1.2, 1.0)
            elif adjusted_polarity < -0.05:  # Lowered from -0.1
                label = 'negative'
                score = min(abs(adjusted_polarity) * 1.2, 1.0)
            else:
                label = 'neutral'
                score = 0.7  # Medium confidence for neutral
            
            # Boost confidence for very subjective text (strong opinions)
            if subjectivity > 0.7 and label != 'neutral':
                score = min(score * 1.15, 1.0)
            
            # Ensure minimum confidence based on strong word presence
            if strong_pos_count > 0 and label == 'positive':
                score = max(score, 0.7)
            if strong_neg_count > 0 and label == 'negative':
                score = max(score, 0.7)
            if neg_context_count > 1 and label == 'negative':
                score = max(score, 0.65)
            
            return {
                'label': label,
                'score': round(score, 3)
            }
        
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            # Fallback to enhanced keyword matching
            return self._enhanced_sentiment(text)
    
    def _enhanced_sentiment(self, text):
        """Enhanced fallback sentiment analysis using keyword matching"""
        if not text:
            return {'label': 'neutral', 'score': 0.5}
        
        text_lower = str(text).lower()
        
        # More comprehensive word lists
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'love', 'best', 'wonderful',
            'fantastic', 'awesome', 'happy', 'perfect', 'beautiful', 'incredible',
            'brilliant', 'outstanding', 'superb', 'terrific', 'fabulous', 'nice',
            'success', 'win', 'victory', 'achievement', 'growth', 'improve',
            'celebrate', 'honor', 'award', 'breakthrough', 'innovative'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'worst', 'hate', 'horrible', 'poor',
            'disappointing', 'sad', 'angry', 'useless', 'pathetic', 'disgusting',
            'annoying', 'frustrating', 'ugly', 'stupid', 'boring', 'waste',
            'disaster', 'crisis', 'threat', 'danger', 'risk', 'concern', 'alarm',
            'death', 'killed', 'war', 'attack', 'violence', 'conflict', 'scandal',
            'corruption', 'controversial', 'criticized', 'condemned', 'failed'
        ]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate ratio for better classification
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {'label': 'neutral', 'score': 0.6}
        
        pos_ratio = positive_count / total_sentiment_words
        neg_ratio = negative_count / total_sentiment_words
        
        # More nuanced classification
        if pos_ratio > 0.6:
            return {'label': 'positive', 'score': 0.75}
        elif neg_ratio > 0.6:
            return {'label': 'negative', 'score': 0.75}
        elif positive_count > negative_count:
            return {'label': 'positive', 'score': 0.65}
        elif negative_count > positive_count:
            return {'label': 'negative', 'score': 0.65}
        else:
            return {'label': 'neutral', 'score': 0.6}
