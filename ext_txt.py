import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re  # Import the re module for regular expressions
import nltk
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Download stopwords data from NLTK
nltk.download('stopwords')

# Create a SentimentIntensityAnalyzer object
analyzer = SentimentIntensityAnalyzer()

# Function to count syllables in a word
def syllable_count(word):
    if not word:
        return 0

    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le"):
        count += 1
    if count == 0:
        count += 1
    return count

# Function to perform sentiment analysis and extract positive/negative words
def analyze_sentiment(text):
    # Analyze sentiment using VADER
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    # Initialize positive and negative scores
    positive_score = 0
    negative_score = 0
    
    # Count positive and negative words
    for word in text.split():
        if analyzer.polarity_scores(word)['compound'] >= 0.05:
            positive_score += 1
        elif analyzer.polarity_scores(word)['compound'] <= -0.05:
            negative_score += 1
    
    # Calculate polarity score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    total_words = len(text.split())
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)
    
    return compound_score, polarity_score, positive_score, negative_score, subjectivity_score

# Function to extract, analyze sentiment, and save data
def extract_analyze_and_save_data(url, url_id):
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''
        
        # Extract content
        content_div = soup.find('div', class_='td-post-content tagdiv-type')
        if content_div:
            content = ' '.join([p.get_text().strip() for p in content_div.find_all('p')])
        else:
            content = ''
        
        # Calculate average sentence length
        sentences = re.split(r'[.!?]+', content)
        num_sentences = len(sentences)
        words = content.split()
        num_words = len(words)
        average_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
        
        # Calculate average number of words per sentence
        average_words_per_sentence = num_words / num_sentences if num_sentences > 0 else 0
        
        # Identify complex words (words with more than two syllables)
        complex_words = [word for word in words if syllable_count(word) > 2]
        num_complex_words = len(complex_words)
        percentage_complex_words = (num_complex_words / num_words) * 100 if num_words > 0 else 0
        
        # Calculate Fog Index
        fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
        
        # Analyze sentiment
        compound_score, polarity_score, positive_score, negative_score, subjectivity_score = analyze_sentiment(content)
        
        # Get positive and negative words
        positive_words = [word for word in content.split() if analyzer.polarity_scores(word)['compound'] >= 0.05]
        negative_words = [word for word in content.split() if analyzer.polarity_scores(word)['compound'] <= -0.05]
        
        # Remove punctuation marks and convert to lowercase
        cleaned_words = [re.sub(r'[^\w\s]', '', word.lower()) for word in words]
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        cleaned_words = [word for word in cleaned_words if word not in stop_words]
        
        # Count cleaned words
        cleaned_word_count = len(cleaned_words)
        
        # Calculate syllable count per word
        syllable_counts_per_word = [syllable_count(word) for word in cleaned_words]
        
        # Count personal pronouns
        personal_pronouns = ['I', 'we', 'my', 'ours', 'us']
        personal_pronoun_count = sum(1 for word in content.split() if word.lower() in personal_pronouns)
        
        # Calculate average word length
        total_characters = sum(len(word) for word in cleaned_words)
        average_word_length = total_characters / num_words if num_words > 0 else 0
        
        # Create a directory if it doesn't exist to store the data
        folder_path = os.path.join('data', url_id)
        os.makedirs(folder_path, exist_ok=True)
        
        # Save sentiment analysis results
        with open(os.path.join(folder_path, 'sentiment_analysis.txt'), 'w') as file:
            file.write(f'Compound Score: {compound_score}\n')
            file.write(f'Polarity Score: {polarity_score}\n')
            file.write(f'Positive Score: {positive_score}\n')
            file.write(f'Negative Score: {negative_score}\n')
            file.write(f'Subjectivity Score: {subjectivity_score}\n')
            file.write(f'Average Sentence Length: {average_sentence_length}\n')
            file.write(f'Average Words Per Sentence: {average_words_per_sentence}\n')
            file.write(f'Complex Word Count: {num_complex_words}\n')
            file.write(f'Percentage of Complex Words: {percentage_complex_words}\n')
            file.write(f'Fog Index: {fog_index}\n')
            file.write(f'Cleaned Word Count: {cleaned_word_count}\n')
            file.write(f'Syllable Count Per Word: {syllable_counts_per_word}\n')
            file.write(f'Personal Pronoun Count: {personal_pronoun_count}\n')
            file.write(f'Average Word Length: {average_word_length}\n')
            file.write('\nPositive Words:\n')
            file.write('\n'.join(positive_words))
            file.write('\n\nNegative Words:\n')
            file.write('\n'.join(negative_words))
        
        # Save content
        with open(os.path.join(folder_path, 'content.txt'), 'w', encoding='utf-8') as file:

            file.write(title)
            file.write('\n\n')
            file.write(content)
    else:
        print("Failed to retrieve data from URL:", url, "Status code:", response.status_code)

# Read the Excel file
df = pd.read_excel('input.xlsx')

# Define the column names
urls_column = 'URL'
url_id_column = 'URL_ID'

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Get the URL and URL ID from the current row
    url = row[urls_column]
    url_id = row[url_id_column]
    
    # Print the URL and URL ID
    print("URL:", url)
    print("URL ID:", url_id)
    
    # Extract, analyze sentiment, and save data
    extract_analyze_and_save_data(url, url_id)
