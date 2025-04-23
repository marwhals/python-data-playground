import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon (needed once)
nltk.download('vader_lexicon')

# Create a SentimentIntensityAnalyzer object
sia = SentimentIntensityAnalyzer()

# Example sentence
happy_text = "This new phone is amazing! I'm so happy with it 😍"
sad_text = "I hate this phone, it has made me very sad 😭"
# Get sentiment scores
scores_happy = sia.polarity_scores(happy_text)
scores_sad = sia.polarity_scores(sad_text)

# Output the results -- generally speaking these two sentences should be opposites
print(scores_happy) #{'neg': 0.0, 'neu': 0.497, 'pos': 0.503, 'compound': 0.8436}
print(scores_sad) #{'neg': 0.503, 'neu': 0.497, 'pos': 0.0, 'compound': -0.796}
