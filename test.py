# Install pip install nltk
import nltk
from nltk.corpus import words

nltk.download('words')  # Download the words corpus (do this once)

word_list = words.words()

print(len(word_list))  # Print the number of words
print(word_list[:10]) # Print the first 10 words