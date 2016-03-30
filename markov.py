#!/usr/bin/env python3

from os import path, listdir
import random

class successor_dict(dict):
    ''' Dictionary of successors following a word, with counts for weight.'''

    def __init__(self):
        self.count = 0
        self.successors = self.keys()

    def choose_successor(self):
        if self.count == len(self.successors):
            return random.choice([successor
                                  for successor in self.successors])
        else:
            print('HEY JAKE IMPLEMENT WEIGHTED CHOICE MKAY?')
            return random.choice([successor
                                  for successor in self.successors])

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
        for i, word in enumerate(word_list):
            try:
                yield word, word_list[i+1]
            except IndexError:
                return

    def _add_successor(self, word, successor):
        ''' Add word successors to self.links instance variable.'''
        if word not in self.links:
            self.links[word] = successor_dict()
            self.links[word][successor] = 1
            self.links[word].count += 1
            return self
        elif successor not in self.links[word]:
            self.links[word][successor] = 1
            self.links[word].count += 1
            return self
        else:
            self.links[word][successor] += 1
            self.links[word].count += 1
            return self

    def add_words(self, filename):
        ''' Make weighted Markov chain from text file.'''
        file_words = self._open_file(filename)
        successors = self._find_successors(file_words)
        for word, successor in successors:
            self._add_successor(word, successor)

    def recipe(self, length, start_word=None):
        ''' Return words from Markov chain, beginning at optional start_word'''
        if not start_word:
            start_word = random.choice([word for word in self.links.keys()])
        recipe = [start_word]
        try:
            next_word = self.links[start_word].choose_successor()
        except KeyError:
            print('%s not in chain. Leave blank for random word.' % start_word)
            return None
        for _ in range(length):
            recipe.append(next_word)
            next_word = self.links[next_word].choose_successor()
        recipe = ' '.join(recipe)
        if not recipe[-1] == ['.']:
            recipe += '.'
        return recipe

chain = WordChainer()
def main(debug=True):
    texts = listdir('texts')
    for text in texts:
        chain.add_words(path.join('texts', text))
    print('Words in chain:', len(chain.links))

if __name__ == '__main__':
    main()