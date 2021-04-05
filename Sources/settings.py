from spacy.lang.fr.stop_words import STOP_WORDS as STOP_WORDS_en
from spacy.lang.es.stop_words import STOP_WORDS as STOP_WORDS_es
from spacy.lang.zh.stop_words import STOP_WORDS as STOP_WORDS_zh
from spacy.lang.ja.stop_words import STOP_WORDS as STOP_WORDS_ja
from spacy.lang.de.stop_words import STOP_WORDS as STOP_WORDS_de
from spacy.lang.fr.stop_words import STOP_WORDS as STOP_WORDS_fr

def init():
    """
        This module declares variables that are used by functions of different modules
    """

    global adult_cond
    global child_cond
    global mother_cond
    global father_cond
    global unknown

    global dic_childes
    global dic_spacy
    global dic_SW

    # speaker identifiers name used in the CHILDES corpus
    adult_cond = ["MOT", "FAT", "MAM", "ADU", "MOM", "DAD", "PAP", "PAD", "MAD", "VAT", "MUT"]
    child_cond = ["CHI"]
    mother_cond = ["MOT", "MAM", "MOM", "MAD", "MUT"]
    father_cond = ["FAT", "DAD", "PAP", "PAD", "VAT"]
    unknown = "ADU"

    # names of the languages in the childes database
    dic_childes = {"English" : "eng", "Spanish" : "spa", "Chinese" : "zho", "Japanese" : "jpn", "German" : "deu", "French" : "fra"}
    # names of the spacy's corpus for each language
    dic_spacy = {"English" : "en_core_web_lg", "Spanish" : "es_core_news_lg", "Chinese" : "zh_core_web_lg", "Japanese" : "ja_core_news_lg", "German" : "de_core_news_lg", "French" : "fr_core_news_lg"}
    # names of the spacy's stop_words list for each language
    dic_SW = {"English" : STOP_WORDS_en, "Spanish" : STOP_WORDS_es, "Chinese" : STOP_WORDS_zh, "Japanese" : STOP_WORDS_ja, "German" : STOP_WORDS_de, "French" : STOP_WORDS_fr}
