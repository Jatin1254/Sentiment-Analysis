## AURTHOR

Jatin Meena

## INTRODUCTION

This Python script performs web scraping on a list of URLs provided in an Excel file, extracts content from each URL, and performs sentiment analysis on the extracted text. It calculates various metrics such as sentiment scores, average sentence length, percentage of complex words, and more.

## SETUP

Steps to setup project for your needs: It is highly recommended that you use Python 3.8+ .

1. git clone --recursive https://github.com/Jatin1254/Sentiment-Analysis

2. cd Sentiment-Analysis

3. pip install -r requirements.txt (It will automatically install all the dependencies)

4. Place your input excel file in the current directry

5. python ext_txt.py (This can be used to create text data that will be creating content.txt and sentiment_analysis.txt file sepratly)
   (or)
   python ext_xl.py (This can be used to create excel file which contains all the information)

 ## APPROACH

 1. **Data Extraction**: The code starts by reading URLs from an Excel file ('input.xlsx'). It uses the requests library to send HTTP GET 'requests' to each URL and fetches the HTML content.

 2. **Data Processing**: After fetching the HTML content, the code uses 'BeautifulSoup' to parse the HTML and extract relevant information such as the title and main content of the web page.

 3. **Text Analysis**: Various text analysis tasks are performed on the extracted content, including:
    > Sentiment analysis using the VADER sentiment analysis tool.
    > Calculating average sentence length, average words per sentence, and fog index.
    > Identifying complex words (words with more than two syllables).
    > Counting personal pronouns.
    > Calculating average word length.

 4. **Data Storage**: The results of the analysis are then stored in text files in a directory structure corresponding to each URL.

 5. **Error Handling**: Error handling is implemented to deal with cases where the HTTP request fails or the required HTML elements are 
not found.

 6. **Dependencies**: The code relies on external libraries such as 'requests', 'beautifulsoup4', 'pandas', 'nltk', and 'vaderSentiment'. It also uses data from the NLTK library for stopwords.

 7. **Output**: Finally, the code prints the URL and URL ID for each processed URL, providing feedback to the user about the progress of the data extraction and analysis.

 ## FILES

 > ext_txt.py: This can be used to create text data that will be creating content.txt and sentiment_analysis.txt file sepratly.

 > ect_xl.py: This can be used to create excel file which contains all the information.

 > data: This contains the extracted data in content.txt and Sentiment Analysis data in sentiment_analysis.txt.

 > Input.xlsx: This is the input data provided by **Blackcoffer**.

 > output.xlsx: This contains the analysed data.

 > requirements.txt: This contains the dependencies required to run the script.

