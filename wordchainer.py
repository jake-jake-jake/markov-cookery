#!/usr/bin/env python3

from os import path, listdir
import random
import string

class successor_dict(dict):
    ''' Dictionary of successors following a word, with counts for weight.'''

    def __init__(self):
        self.count = 0
        self.successors = self.keys()
        self.weighted = False
        self.out_list = []

    def _increment(self):
        ''' Increment count and set self.weighted to False.'''
        self.count += 1
        self.weighted = False
        return self

    def _make_weighted_out_list(self):
        ''' Generate list of successors.'''
        self.weighted = True
        self.out_list = []
        for word, count in self.items():
            for _ in range(count):
                self.out_list.append(word)
        assert len(self.out_list) == self.count
        return self

    def choose_successor(self):
        ''' Choose next word based on probabilities of input texts.'''
        if self.count == len(self.successors):
            return random.choice([successor for successor in self.successors])
        else:
            if not self.weighted:
                self._make_weighted_out_list()
            return self.out_list[random.randrange(self.count)]


class WordChainer:
    ''' Class for constructing a Markov chain from text files. '''

    def __init__(self):
        self.links = dict()

    @staticmethod
    def _open_file(filename):
        ''' Open file, read it in entirely, split words, return that list.'''
        with open(filename, 'r') as f:
            content = f.read()
        return content.split()  # Worry about preserving newline chars later.

    @staticmethod
    def _find_successors(word_list):
        ''' Yield successor for each word in list.'''
        marks = '\[]_/'
        for i, word in enumerate(word_list):
            try:
                yield word.strip(marks), word_list[i+1].strip(marks)
            except IndexError:
                return

    def _add_successor(self, word, successor):
        ''' Add word successors to self.links instance variable.'''
        if word not in self.links:
            self.links[word] = successor_dict()
            self.links[word][successor] = 1
            self.links[word]._increment()
            return self
        elif successor not in self.links[word]:
            self.links[word][successor] = 1
            self.links[word]._increment()
            return self
        else:
            self.links[word][successor] += 1
            self.links[word]._increment()
            return self

    def _get_start_word(self):
        ''' Choose word at random; if it is a sentence ender, rechoose.'''
        word = random.choice([word for word in self.links.keys()])
        if not word[-1] == '.':
            return word
        else:
            return self._get_start_word()

    def add_words(self, filename):
        ''' Make weighted Markov chain from text file.'''
        file_words = self._open_file(filename)
        successors = self._find_successors(file_words)
        for word, successor in successors:
            self._add_successor(word, successor)

    def words(self, length, start_word=None):
        ''' Return words from Markov chain, beginning at optional start_word'''
        if not start_word:
            start_word = random.choice([word for word in self.links.keys()])
        words = [start_word.capitalize()]
        try:
            next_word = self.links[start_word].choose_successor()
        except KeyError:
            print('start_word not in chain. Leave blank for random word.')
            return None
        for _ in range(length):
            words.append(next_word)
            next_word = self.links[next_word].choose_successor()
        words = ' '.join(words)
        if words[-1] in string.punctuation:
            words = words[:-1]
        return words + '.'

    def sentence(self, start_word=None):
        ''' Return a sentence of length, with start_word. '''
        if not start_word:
            start_word = self._get_start_word()
        try:
            next_word = self.links[start_word].choose_successor()
        except KeyError:
            print('start_word not in chain. Leave blank for random word.')
            return None
        sent = []
        sent.append(start_word.capitalize())
        while not next_word[-1] == '.':
            if next_word == 'To':
                sent[-1] = sent[-1] + '.'
                break
            sent.append(next_word)
            next_word = self.links[next_word].choose_successor()
        else:
            sent.append(next_word)
        return ' '.join(sent)


recipes = WordChainer()
title = WordChainer()

def main(debug=True):
    p = path.join('texts', '1600s')
    recipes.add_words(path.join(p, 'accomplisht_cook_STRIPPED.txt'))
    recipes.add_words(path.join(p, 'closet_of_sir_digby_STRIPPED.txt'))
    recipes.add_words(path.join(p, 'eales_receipts_STRIPPED.txt'))
    title.add_words(path.join(p, '1600s_titles.txt'))


if __name__ == '__main__':
    main()

print(title.words(5))
print(recipes.sentence())