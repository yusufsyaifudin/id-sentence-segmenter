#!/usr/bin/env python
import copy
from typing import List

from id_sentence_segmenter.utils.dict_tokens import SHOULD_SPLIT_PUNCTUATION_CHARS
from id_sentence_segmenter.utils.dict_tokens import ALPHANUMERIC_CHARS
from id_sentence_segmenter.utils.dict_tokens import NUMERIC_CHARS

from id_sentence_segmenter.utils.dict_abbreviations import ABBREVIATIONS_DICT
from id_sentence_segmenter.utils.dict_tld import TLD_DICT


class CharAnalyzer:
    def __init__(self, word: str):
        
        self.number_of_split_true: int = 0
        self.number_of_split_false: int = 0
        self.number_of_numeric_token: int = 0
        self.word = word

    def token_words(self) -> List[str]:
        first_index_char: int = 0
        last_index_char: int = 0
        word_to_tokens: List[str] = []

        for word_index in range(0, len(self.word)):
            self.__check_alpha_numeric(char=self.word[word_index])
            self.__check_punctuation(char=self.word[word_index])
            self.__check_numeric(char=self.word[word_index])

            if self.number_of_split_true > self.number_of_split_false and self.number_of_numeric_token == 0:
                last_index_char = word_index
                if last_index_char == len(self.word) - 1:
                    if self.word[first_index_char:last_index_char] != "":
                        word_to_tokens.append( self.word[first_index_char:last_index_char])
                else:
                    if self.word[first_index_char:last_index_char] != "":
                        word_to_tokens.append(self.word[first_index_char:last_index_char])
                    if self.word[word_index] != "":
                        word_to_tokens.append(self.word[word_index])

                first_index_char = last_index_char + 1

            # Reset split after one iteration
            self.__reset_split()

        if last_index_char != (len(self.word) - 1) and self.word not in ["", " "]:
            word_to_tokens.append(self.word[first_index_char: len(self.word) + 1])
        elif last_index_char == (len(self.word) - 1):
            word_to_tokens.append(self.word[-1])

        # Finally reset.
        self.__reset_split()
        return word_to_tokens

    def __reset_split(self):
        self.number_of_split_true = 0
        self.number_of_split_false = 0
        self.number_of_numeric_token = 0

    def __check_alpha_numeric(self, char: str):
        if char not in ALPHANUMERIC_CHARS:
            self.number_of_split_true += 1
        else:
            self.number_of_split_false += 1

    def __check_punctuation(self, char: str):
        if char in SHOULD_SPLIT_PUNCTUATION_CHARS:
            self.number_of_split_true += 1
        else:
            self.number_of_split_false += 1

    def __check_numeric(self, char: str):
        if char in NUMERIC_CHARS:
            self.number_of_numeric_token += 1


def is_numerical_value(tokens: List[str]) -> bool:
    string: int = 0
    numeric: int = 0

    for token in tokens:
        for x in token:
            if x in NUMERIC_CHARS:
                numeric += 1
            else:
                string += 1
    if numeric > string:
        return True

    return False


def is_abbreviation(tokens: List[str]) -> bool:
    is_abr: int = 0
    not_abr: int = 0

    new_tokens: List[str] = copy.deepcopy(tokens)

    # remove last punctuation and check
    for x in range(0, len(new_tokens)):
        if new_tokens[-1] in [",", "!", "?"]:
            new_tokens = new_tokens[:-1]
        else:
            break

    check_words = "".join(new_tokens[:-1]).lower()
    if check_words in ABBREVIATIONS_DICT:
        is_abr += 1
        return True

    for x in new_tokens:
        if x != "." and x in ABBREVIATIONS_DICT:
            is_abr += 1
        else:
            not_abr += 1

    if is_abr > not_abr:
        return True

    return False


def is_word_abbr(word: str):
    if word in ABBREVIATIONS_DICT:
        return True

    return False


def is_tld_domain(word: str):
    if word in TLD_DICT:
        return True

    return False


