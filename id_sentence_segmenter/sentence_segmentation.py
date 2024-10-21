#!/usr/bin/env python

import re
import string
from typing import List

from id_sentence_segmenter.utils.dict_abbreviations import ABBREVIATIONS_DICT
from id_sentence_segmenter.utils.dict_tld import TLD_DICT


FIRST_CHAR_TOKEN = ['"']
END_CHARS_TOKEN = [".", "?", "!"]
POTENTIAL_END_QUOTE = [","]
QUOTE_TRANSLATION = ["\u201d", "\u201c"]


class SentenceSegmentation:
    def __init__(self):
        self.abbreviations_dict = ABBREVIATIONS_DICT
        self.tld_dict = TLD_DICT

    def get_sentences(self, document=""):
        # remove \n\t
        document = re.sub(pattern=r'\s+', repl=" ", string=document.strip())

        # replace quotes
        document = document.replace(QUOTE_TRANSLATION[0], '"')
        document = document.replace(QUOTE_TRANSLATION[1], '"')

        doc_strings: str = document

        word_lists: List[str] = doc_strings.strip().split()

        quote_word: bool = False
        first_quote: bool = False
        first_word_index: int = 0
        processed_word_lists: List[str] = []
        sentence_lists: List[str] = []

        for x in range(0, len(word_lists)):
            # print(word_lists[x])
            if "." in word_lists[x] and word_lists[x][-1] != ".":
                split_item = word_lists[x].split(".")

                # merge
                if len(split_item) != 2:
                    endlist = split_item[-1]
                    startlist = ".".join(split_item[:-1])

                    split_item = [startlist, endlist]

                # print(splitItem)

                # test tld
                str_item_1 = split_item[1].translate(
                    str.maketrans("", "", string.punctuation)
                )
                str_item_1 = "".join([".", str_item_1.lower()])

                if str_item_1 not in self.tld_dict:
                    # if abbreviations
                    if (split_item[0].lower() not in self.abbreviations_dict) and (
                        split_item[1][0].isupper() or split_item[1][0] in ['"']
                    ):
                        split_str = ["".join([split_item[0], "."]), split_item[1]]
                        processed_word_lists.append(split_str[0].strip())
                        processed_word_lists.append(split_str[1].strip())

                # in a tld domain
                else:
                    split_str = "".join([split_item[0], ".", split_item[1]])
                    processed_word_lists.append(split_str.strip())

            else:
                processed_word_lists.append(word_lists[x].strip())

        len_words = len(processed_word_lists)
        for i in range(0, len_words):
            # print(processed_word_lists[i])
            # check first char of words, if first char is ('"') then find close quote, it might before ('.') char
            first_char = processed_word_lists[i][0]

            if not quote_word and first_char in FIRST_CHAR_TOKEN:
                if processed_word_lists[i].count('"') > 1:
                    # just single quote
                    quote_word = False
                    first_quote = False

                else:
                    quote_word = True
                    first_quote = True
                    pass

            if first_quote and quote_word:
                quote_word = True
                first_quote = False
                pass

            # find another close '"'
            if not first_quote and quote_word:
                if '"' in processed_word_lists[i]:
                    if processed_word_lists[i][-1] in END_CHARS_TOKEN:
                        last_word_index = i + 1
                        # print('terminate on token: ', processed_word_lists[last_word_index])
                        sentence = " ".join(
                            processed_word_lists[first_word_index:last_word_index]
                        )
                        sentence_lists.append(sentence)

                        first_word_index = last_word_index

                        # set false
                        quote_word = False
                        first_quote = False
                        pass

                    elif processed_word_lists[i][-1] == '"' or processed_word_lists[i][-1] in POTENTIAL_END_QUOTE:
                        quote_word = False
                        first_quote = False
                        pass

                else:
                    pass

            if not quote_word and not first_quote:
                if i == (len_words - 1):
                    last_word_index = i + 1
                    sentence = " ".join(
                        processed_word_lists[first_word_index:last_word_index]
                    )
                    sentence_lists.append(sentence)
                    break

                else:
                    if self.check_is_end_of_sentence(processed_word_lists[i]):
                        last_word_index = i + 1

                        sentence = " ".join(processed_word_lists[first_word_index:last_word_index])
                        sentence_lists.append(sentence)

                        first_word_index = last_word_index
                    else:
                        pass

        return sentence_lists

    def check_is_end_of_sentence(self, word: str):
        end_char = word[-1]

        if end_char not in END_CHARS_TOKEN:
            return False

        # print(word[:-1])
        if word[:-1].lower() in self.abbreviations_dict:
            return False

        if word[:-1].isdigit() and len(word[:-1]) > 2:
            return True

        # short name such as J. Jr. L. K. etc
        if len(word[:-1]) > 2:
            return True

        return False

# test
# test_str = """
# Pada kompetisi ini tersedia hadiah utama berupa 1 unit Vivo V15, hadiah kedua 7 unit Headphone, dan hadiah ketiga berupa 7 unit Backpack eksklusif Vivo.Aktivitas digital selanjutnya adalah Go Guess, Go Up! yang telah berjalan di akun media sosial dari JD.ID, Akulaku, Shopee, Tokopedia, Lazada, dan Blibli.com.
# """
# print('raw text: ')
# print(test_str)
# print('-' * 64)
# print('sentences: ')
# test = SentenceSegmentation(test_str).get_sentences()
# for i in range(0, len(test)):
#     print('{} - {}'.format(i + 1, test[i]))
