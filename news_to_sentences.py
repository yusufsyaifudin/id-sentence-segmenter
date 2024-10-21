# import sentence segmentation class 
from id_sentence_segmenter.sentence_segmentation import SentenceSegmentation

news_content: str
# open sample news content 
with open("news_example.txt", "r") as fio:
    news_content = fio.read()

print("news content: ")
print(news_content)

print("-" * 82)

# create sentence segmenter instance from SentenceSegmentation class
sentence_segmenter = SentenceSegmentation()

# parse text to sentences 
sentences = sentence_segmenter.get_sentences(news_content)

print("news sentences: ")
# print sentences from previous sentence segmentation process
for i, sent in enumerate(sentences):
    print(f"{i:3}: {sent}")
