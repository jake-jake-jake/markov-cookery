#!/usr/bin/env python3

from collections import Counter
from os import path
import random
import string


class SuccessorDict(Counter):
    ''' Dictionary of successors following a token, with counts for weight.'''
    def __init__(self):
        self.count = 0
        self.out_list = []

    def _make_out_list(self):
        ''' Generate list of all successors; each successor has an entry for each occurrence.'''
        self.count = sum(self.values())
        self.out_list = list(self.elements())
        return self

    def choose_successor(self):
        ''' Choose next word by choosing random index of from self.out_list (a list of self.elements()).'''
        if not self.out_list:
            self._make_out_list()
        return self.out_list[random.randrange(self.count)]


class WordChainer:
    ''' Class for constructing a Markov chain from text files. '''
    def __init__(self):
        self.links = dict()
        self.start_tokens = set()
        self.starts = []

    @staticmethod
    def _open_file(filename):
        ''' Open file, read it in entirely, split words, return that list.'''
        with open(filename, 'r') as f:
            content = f.read()
        return content.split()

    @staticmethod
    def _find_successors(word_list):
        ''' Yield successor for each bigram in word_list.'''
        for i, word in enumerate(word_list):
            try:
                yield (word, word_list[i + 1]), word_list[i + 2]
            except IndexError:
                return

    def _add_successor(self, token, successor):
        ''' Add token successors to self.links instance variable.'''
        if token not in self.links:
            self.links[token] = SuccessorDict()
        self.links[token][successor] += 1
        return self

    def _get_token(self):
        ''' Choose token at random from self.starts, a list from set of bigrams that start sentences.'''
        if not self.starts:
            self.starts = list(self.start_tokens)
        choice = random.choice(self.starts)
        return choice

    def add_words(self, filename):
        ''' Make weighted Markov chain from text file.'''
        file_words = self._open_file(filename)
        successors = self._find_successors(file_words)
        for token, successor in successors:
            if token[0][-1] == '.':
                self.start_tokens.add((token[1], successor))
            self._add_successor(token, successor)

    
    def sentence(self, token=None):
        ''' Return a sentence of length, beginning with optional token. '''
        if not token:
            token = self._get_token()
        first_words = ' '.join(token)
        if first_words[-1] == '.':
            return first_words

        sent = [first_words]
        next_word = self.links[token].choose_successor()
        while not next_word[-1] == '.':
            token = token[1], next_word
            sent.append(next_word)
            next_word = self.links[token].choose_successor()
        else:
            sent.append(next_word)
        return ' '.join(sent)


recipes = WordChainer()
titles = WordChainer()


def main():
    p = path.join('texts', '1600s')
    recipes.add_words(path.join(p, 'accomplisht_cook_STRIPPED.txt'))
    recipes.add_words(path.join(p, 'closet_of_sir_digby_STRIPPED.txt'))
    recipes.add_words(path.join(p, 'eales_receipts_STRIPPED.txt'))
    titles.add_words(path.join(p, '1600s_titles.txt'))


if __name__ == '__main__':
    main()
