import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.corpora.dictionary import Dictionary  # Correct the import statement
from gensim.models.ldamodel import LdaModel
from wordcloud import WordCloud

# Load NLTK resources (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Read data from CSV file
df = pd.read_csv('data.csv')

# Data cleaning and preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if isinstance(text, str):  # Check if the value is a string
        words = word_tokenize(text.lower())
        words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]
        return words
    else:
        return []  # Return an empty list for non-string values

df.dropna(subset=['Review'], inplace=True)  # Drop rows with missing values in 'Review' column
df['processed_text'] = df['Review'].apply(preprocess_text)

# Create Document-Term Matrix
dictionary = Dictionary(df['processed_text'])  # Use Dictionary method of corpora
corpus = [dictionary.doc2bow(text) for text in df['processed_text']]

# Topic Modeling (LDA)
num_topics = 50 # Adjust the number of topics as needed
lda_model = LdaModel(corpus, id2word=dictionary, passes=10)

# Print and Interpret Topics
print("Topics:")
for topic in lda_model.print_topics():
    print(topic)

# Topic Distribution in Documents
document_topics = [dict(lda_model[doc]) for doc in corpus]  # Process the output of LDA model
df['topics'] = document_topics

# Visualization (Optional - Requires matplotlib)

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Function to create a word cloud for each topic
def create_word_cloud(lda_model, dictionary):
    for topic_num in range(num_topics):
        words = lda_model.show_topic(topic_num, topn=20)  # Get top 20 words for each topic
        word_freq = {word: freq for word, freq in words}
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Word Cloud for Topic {topic_num+1}")
        plt.show()

# Create and display word clouds for each topic
create_word_cloud(lda_model, dictionary)