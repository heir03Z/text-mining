import random
import sys
from unicodedata import category
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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
words = process_file('data/words.txt', skip_header=False)
print(hist)
print(words)


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
    rdmdic = []
    for word, freq in hist.items():
        rdmdic.extend([word] * freq)
    return random.choice(rdmdic)


def sentiment_analysis():
    """This functions provides a sentiment analysis of Leviathan."""
    leviathan = ""
    f = open('data/Leviathan.txt')
    for line in f:
        leviathan.append(line)
    return leviathan
    score = SentimentIntensityAnalyzer().polarity_scores(leviathan)


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

    words = process_file('data/words.txt', skip_header=False)
    diff = subtract(hist, words)
    for word in diff:
        print(word, end=' ')
    print(subtract(hist, words))

    print("\n\nHere are some random words from the book")
    for i in range(100):
        print(random_word(hist), end=' ')
    
    score = SentimentIntensityAnalyzer().polarity_scores(leviathan)
    print("Summary Statistics of sentimental analysis of Leviathan is:")
    print(score)


if __name__ == '__main__':
    main()
