import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models import LdaModel
from gensim.corpora import Dictionary

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load NLTK resources (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Sample text data (replace this with your own dataset)
data = pd.DataFrame({
    'text': [
        "Topic modeling is a powerful technique for finding hidden themes in text data.",
        "Natural Language Processing (NLP) is an essential aspect of topic modeling.",
        "Text preprocessing involves tasks like tokenization, stop words removal, and lemmatization.",
        "Topic modeling can be used in various domains such as social media analysis, customer reviews, and more."
    ]
})

# Data cleaning and preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]
    return words

data['processed_text'] = data['text'].apply(preprocess_text)

# Word frequency analysis
word_freq = pd.Series([word for sublist in data['processed_text'] for word in sublist]).value_counts()

# Word cloud visualization (optional)
import matplotlib.pyplot as plt
from wordcloud import WordCloud

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Topic modeling
dictionary = Dictionary(data['processed_text'])
corpus = [dictionary.doc2bow(text) for text in data['processed_text']]
lda_model = LdaModel(corpus, num_topics=2, id2word=dictionary, passes=10)

# Topic visualization
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(f"Topic {topic[0]}: {topic[1]}")
