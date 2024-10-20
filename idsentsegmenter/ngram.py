#!/usr/bin/env python

from typing import List

class NGram:
    def __init__(self, n: int):
        self.n = n
        pass

    def get_ngram(self, word_list: List[str]) -> List[str]:
        """
        Get n-gram of a word lists.
        :param word_list:
        :return:
        """
        return list(zip(*[word_list[i:] for i in range(self.n)]))


# test ngram
# tokens = ['saya', 'makan', 'bakso', 'bersama', 'dia', '.']

# ngram = NGram(n=2)
# print(ngram.get_ngram(tokens))
