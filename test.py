# Install pip install nltk
# import nltk
# from nltk.corpus import words
#
# nltk.download('words')  # Download the words corpus (do this once)
#
# word_list = words.words()
#
# print(len(word_list))  # Print the number of words
# print(word_list[:10]) # Print the first 10 words


import nltk
import ssl

from nltk.corpus import words

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('words')

word_list = words.words()

print(len(word_list))  # Print the number of words
print(word_list[:100]) # Print the first 10 words
