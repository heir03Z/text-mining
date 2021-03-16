import random
import sys
from unicodedata import category
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import markovify


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

    stps = ''.join([
        chr(i) for i in range(sys.maxunicode)
        if category(chr(i)).startswith("P")
    ])

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

    return hist


def skip_gutenberg_header(fp):
    """Reads from fp until it finds the line that ends the header.
    fp: open file object
    """
    for line in fp:
        if line.startswith('*** START OF THIS PROJECT'):
            break


hist = process_file('data/Leviathan.txt', skip_header=True)
words = process_file('data/alice.txt', skip_header=False)
# print(hist)
# print(words)


def total_words(hist):
    """Returns the total of the frequencies in a histogram."""
    return sum(hist.values())


def different_words(hist):
    """Returns the number of different words in a histogram."""
    return len(hist)


def most_common(hist, excluding_stopwords=False):
    """Makes a list of word-freq pairs in descending order of frequency.
    hist: map from word to frequency
    returns: list of (frequency, word) pairs
    """
    # Create a list, freq_word_list
    # use for loop over the dic
    # get the word, freq from list
    # create a tuple (freq, word)
    # append the tuple to freq_word_list
    # sort freq_word_list
    # return it
    freq_word_list = []
    for word, freq in hist.items():
        t = (freq, word)
        freq_word_list.append(t)
        freq_word_list.sort(reverse=True)
    return freq_word_list


def print_most_common(hist, num=10):
    """Prints the most commons words in a histgram and their frequencies.
    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    # for freq, word in t[0:10]:
    #     print(word, '\t', freq)
    # return print_most_common
    pass


def subtract(d1, d2):
    """Returns a dictionary with all keys that appear in d1 but not d2.
    d1, d2: dictionaries
    """
    dic = []
    for word in d1.keys():
        if word in d2:
            continue
        dic.append(word)
    return dic


def random_word(hist):
    """Chooses a random word from a histogram.
    The probability of each word is proportional to its frequency.
    """
    # rdmdic = []
    # for word, freq in hist.items():
    #     rdmdic.extend([word] * freq)
    # return random.choice(rdmdic)
    words = []
    freqs = []
    total_freq = 0
    for word, freq in hist.items():
        total_freq += freq
        words.append(word)
        freqs.append(total_freq)
    
    x = random.randint(0, total_freq - 1)
    index = bisect(freqs, x)
    return words[index]


def pair_sim(f):
    f = TfidfVectorizer().fit_transform(hist.keys())
    ans = cosine_similarity(f)
    return ans


# Below uses markovify to generate random sentenses.
with open("data/Leviathan.txt", "r", encoding='utf-8') as f:
    text = f.read()

textmodel = markovify.Text(text)

print("Here are 2 long, 5 short random sentences generated from origin text")
for i in range(2):
    print(textmodel.make_sentence())
for sentense in range(5):
    print(textmodel.make_short_sentence(200))


def main():
    hist = process_file('data/Leviathan.txt', skip_header=True)
    print(hist)
    print('Total number of words:', total_words(hist))
    print('Number of different words:', different_words(hist))
    t = most_common(hist, excluding_stopwords=True)
    print('The most common words are:')
    for freq, word in t[0:10]:
        print(word, '\t', freq)

    print("The words in Leviathan that aren't in Alice are:")

    words = process_file('data/alice.txt', skip_header=False)
    diff = subtract(hist, words)
    for word in diff:
        print(word, end=' ')
    print(subtract(hist, words))

    print("\n\nHere are some random words from the book")
    for i in range(100):
        print(random_word(hist), end=' ')

    leviath = json.dumps(hist)
    score = SentimentIntensityAnalyzer().polarity_scores(leviath)
    print("Sentiment analysis of Leviathanis:", score)

    print(pair_sim(hist))

    # Below uses markovify to generate random sentenses.
    with open("data/Leviathan.txt", "r", encoding='utf-8') as f:
        text = f.read()

    textmodel = markovify.Text(text)

    print("Here are 2 long, 5 short random sentences generated from origin")
    for i in range(2):
        print(textmodel.make_sentence())
    for sentense in range(5):
        print(textmodel.make_short_sentence(200))


if __name__ == '__main__':
    main()

# Here is text similarity with very wired result which will be
# discussed in assignment report.
# S = np.asarray(pair_sim(hist))
# dissimilarities = 1 - S
# coord = MDS(dissimilarity='precomputed').fit_transform(dissimilarities)

# plt.scatter(coord[:, 0], coord[:, 1])
# for i in range(coord.shape[0]):
#     plt.annotate(str(i), (coord[i, :]))

# plt.show()
