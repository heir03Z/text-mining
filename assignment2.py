# import nltk
# nltk.download('vader_lexicon')
import random
import sys
from unicodedata import category


# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# sentence = 'Software Design is my favorite class because learning Python is so cool!'
# score = SentimentIntensityAnalyzer().polarity_scores(sentence)
# print(score)


# import numpy as np
# from sklearn.manifold import MDS
# import matplotlib.pyplot as plt

# # these are the similarities computed from the previous section
# S = np.asarray([[1., 0.90850572, 0.96451312, 0.97905034, 0.78340575],
#     [0.90850572, 1., 0.95769915, 0.95030073, 0.87322494],
#     [0.96451312, 0.95769915, 1., 0.98230284, 0.83381607],
#     [0.97905034, 0.95030073, 0.98230284, 1., 0.82953109],
#     [0.78340575, 0.87322494, 0.83381607, 0.82953109, 1.]])

# # dissimilarity is 1 minus similarity
# dissimilarities = 1 - S

# # compute the embedding
# coord = MDS(dissimilarity='precomputed').fit_transform(dissimilarities)

# plt.scatter(coord[:, 0], coord[:, 1])

# # Label the points
# for i in range(coord.shape[0]):
#     plt.annotate(str(i), (coord[i, :]))


# plt.show()


def process_file(filename, skip_header):
    """Makes a histogram that contains the words from a file.
    filename: string
    skip_header: boolean, whether to skip the Gutenberg header
    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding='UTF8')

    # TOOD explain skip_headler
    if skip_header:
        skip_gutenberg_header(fp)

    # stps = string.punctuation + string.whitespace
    # via: https://stackoverflow.com/questions/60983836/
    # complete-set-of-punctuation-marks-for-python-not-just-ascii

    for line in fp:
        if line.startswith('*** END OF THIS PROJECT'):
            break

        line = line.replace('-', ' ').replace(
            chr(8212), ' '
        )  # Unicode 8212 is the HTML decimal entity for em dash

        for word in line.split():
            # word could be 'Sussex.'
            word = word.strip(stps)
            word = word.lower()

            # update the dictionary
            hist[word] = hist.get(word, 0) + 1
    print(hist, "救命啊")
    return hist


def skip_gutenberg_header(fp):
    """This function reads fromfp until it finds the line that
    ends the header."""
    for line in fp:
        if line.startswith('*** START OF THIS PROJECT'):
            break


def total_words(hist):
    """Returns total word frequencies in a histogram"""
    return sum(hist.values())


def different_words(hist):
    """This func returns the number of different words in a his"""
    return len(hist)


def most_common(hist, excluding_stopwords=False):
    """This func makes a list of key-value pairs in descending order."""
    freq_word_list = []
    for word, freq in hist.items():
        t = (freq, word)
        freq_word_list.append(t)
        freq_word_list.sort(reverse=True)
    return freq_word_list


def print_most_common(hist, num=10):
    """This func prints out the most common words atheir frequencies."""
    pass


hist = process_file('data/Leviathan.txt', skip_header=True)
words = process_file('data/alice.txt', skip_header=False)
print(hist)
print(words)


def subtract(d1, d2):
    """Returns a dictionary with all keys that appear in d1 but not d2.
    d1, d2: dictionaries
    """
    dic = []
    for word in hist.keys():
        if word in words:
            continue
        dic.append(word)
    return dic


def random_word(hist):
    """Chooses a random word from a histogram.
    The probability of each word is proportional to its frequency.
    """
    rdmdic = []
    for word, freq in hist.items():
        rdmdic.extend([word] * freq)
    return random.choice(rdmdic)


def main():
    hist = process_file('data/Leviathan.txt', skip_header=True)
    print(hist)
    print('Total number of words:', total_words(hist))
    print('Number of different words:', different_words(hist))
    t = most_common(hist, excluding_stopwords=True)
    print('The most common words are:')
    for freq, word in t[0:10]:
        print(word, '\t', freq)

    print("The words in the book that aren't in the word list are:")

    # words = process_file('data/words.txt', skip_header=False)
    # diff = subtract(hist, words)
    # for word in diff.keys():
    #     print(word, end=' ')
    print(subtract(hist, words))

    print("\n\nHere are some random words from the book")
    for i in range(100):
        print(random_word(hist), end=' ')


if __name__ == '__main__':
    main()
