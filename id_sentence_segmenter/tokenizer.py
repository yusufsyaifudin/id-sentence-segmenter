#!/usr/bin/env python



import string
from typing import List
from id_sentence_segmenter.utils.dict_abbreviations import ABBREVIATIONS_DICT
from id_sentence_segmenter.utils.dict_tld import TLD_DICT

from id_sentence_segmenter.utils.dict_tokens import END_OF_SENTENCE_CHARS_TOKEN
from id_sentence_segmenter.utils.dict_tokens import NOT_END_OF_SENTENCE

from id_sentence_segmenter.char_analyzer import CharAnalyzer
from id_sentence_segmenter.char_analyzer import is_abbreviation
from id_sentence_segmenter.char_analyzer import is_numerical_value
from id_sentence_segmenter.char_analyzer import is_word_abbr


class Tokenizer:
    def __init__(self, sentence=""):
        self.sentence = sentence
        self.words = self.sentence.split()


        self.abbreviations_dict = ABBREVIATIONS_DICT
        self.tld_dict = TLD_DICT

    def get_tokens(self) -> List[str]:
        tokens: List[str] = []
        for word_index in range(0, len(self.words)):
            # Current word is dot (.) but the last word is not end of sentence token.
            if "." in self.words[word_index] and self.words[word_index][-1] not in END_OF_SENTENCE_CHARS_TOKEN:
                split_item = self.words[word_index].split(".")
                if len(split_item) != 2:
                    end_list: str = split_item[-1]
                    start_list: str = ".".join(split_item[:-1])

                    split_item: list[str] = [start_list, end_list]

                # check whether this word is TLD or not (test tld)
                str_item_1: str = split_item[1].translate(
                    str.maketrans("", "", string.punctuation)
                )

                str_item_1 = "".join([".", str_item_1.lower()])

                # If TLD, then append as token and continue. Otherwise, check if it is the last word or not.
                if str_item_1 in self.tld_dict:
                    tokens.append(self.words[word_index])
                    continue

            # If current word is the
            # last word of sentences is a token that exist on end of sentence token list.
            if word_index == (len(self.words) - 1) and self.words[word_index][-1] in END_OF_SENTENCE_CHARS_TOKEN:
                if is_word_abbr(self.words[word_index][:-1].lower()):
                    tokens.append(self.words[word_index])
                else:
                    char_analyzer = CharAnalyzer(self.words[word_index][:-1]).token_words()
                    if len(char_analyzer) > 1:
                        is_numeric: bool = is_numerical_value()
                        if is_numeric:
                            if "".join(char_analyzer) != "":
                                tokens.append("".join(char_analyzer))
                        else:
                            abbreviation = is_abbreviation()
                            if abbreviation:
                                if "".join(char_analyzer) != "":
                                    tokens.append("".join(char_analyzer))
                            else:
                                for i in char_analyzer:
                                    tokens.append(i)
                    else:
                        if "".join(char_analyzer) != "":
                            tokens.append("".join(char_analyzer))

                    tokens.append(self.words[word_index][-1])
                continue

            char_analyzer: List[str] = CharAnalyzer(word=self.words[word_index]).token_words()
            if len(char_analyzer) > 1:
                is_numeric: bool = is_numerical_value(tokens=char_analyzer)
                if is_numeric and "".join(char_analyzer) != "":
                    tokens.append("".join(char_analyzer))
                else:
                    abbreviation = is_abbreviation(tokens=char_analyzer)
                    if abbreviation:
                        if char_analyzer[-1] in NOT_END_OF_SENTENCE:
                            tokens.append("".join(char_analyzer[:-1]))
                            tokens.append("".join(char_analyzer[-1]))
                        else:
                            tokens.append("".join(char_analyzer))
                    else:
                        for i in char_analyzer:
                            tokens.append(i)

            elif "".join(char_analyzer) != "":
                tokens.append("".join(char_analyzer))

        return tokens


# test
# sentence = "JAKARTA, KOMPAS.com - Mitsubishi Xpander masih mendominasi penjualan PT Mitsubishi Motors Krama Yudha Sales Indonesia (MMKSI) pada Januari 2019."
# test = Tokenizer(sentence).get_tokens()

# print(test)
