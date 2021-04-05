import re
import numpy as np
from operator import add


class Utterance:

    """
    Represent an utterance from a transcript. Allow simpler representation of data
    to compute similarities between couple of utterance.

    :param gloss: The original utterance, as it was prononced by the speaker, unaltered, unprocessed
    :type gloss: str
    :param speaker_id: the id of the speaker
    :type speaker_id: int
    :param typeu: type of the sentence, ex: question, declarative ...
    :type typeu: str

    :ivar original_gloss: The original utterance, as it was prononced by the speaker, unaltered, unprocessed
    :vartype original_gloss: str
    :ivar speaker_id: the id of the speaker
    :vartype speaker_id: int
    :ivar type: type of the sentence, ex: question, declarative ...
    :vartype type: str
    :ivar modified_gloss: Version of original_gloss without any underscore, to simplify Spacy task
    :vartype modified_gloss: str

    :ivar tokens_gloss: Tokenized version of modified_gloss, the split is done by the Spacy model, not by str.split()
    :vartype tokens_gloss: numpy.ndarray([str])
    :ivar length_gloss: The number of tokens in tokens_gloss
    :vartype length_gloss: int

    :ivar gloss_stopw: A string array reprensentation of the function words found in tokens_gloss
    :vartype gloss_stopw: numpy.ndarray([str])
    :ivar gloss_stopw_nbr: The number of function words in tokens_gloss
    :vartype gloss_stopw_nbr: int

    :ivar gloss_unknowns: A string array reprensentation of the unknown words found in tokens_gloss
    :vartype gloss_unknowns: numpy.ndarray([str])
    :ivar gloss_unknowns_nbr: The number of unknown words in tokens_gloss
    :vartype gloss_unknowns_nbr: int

    :ivar final_tokens_gloss: A string array representation of the tokens present in tokens_gloss, from which unknowns words and function words have been removed
    :vartype final_tokens_gloss: numpy.ndarray([str])
    :ivar final_tokens_gloss_nbr: The number of words in final_tokens_gloss
    :vartype final_tokens_gloss_nbr: int

    :ivar embedding_gloss: The 300 dimension embedding representing the utterance, minus its function words and unknown words
    :vartype embedding_gloss: numpy.ndarray([float]*300)
    """

    def __init__(self, gloss, speaker_id, typeu):

        self.original_gloss = gloss
        self.speaker_id = speaker_id
        self.type = typeu
        self.modified_gloss = self.modify(self.original_gloss)

        self.tokens_gloss = None
        self.length_gloss = None

        self.gloss_stopw = None
        self.gloss_stopw_nbr = None

        self.gloss_unknowns = None
        self.gloss_unknowns_nbr = None

        self.final_tokens_gloss = None
        self.final_tokens_gloss_nbr = None

        self.embedding_gloss = None


    def modify(self, s):
        """
            Substitute every underscore character in s with a space and return the result
            It is used to allow Spacy to recognize words that have been saved in CHILDES
            separated with an underscore

            :param s: The string to modify
            :type s: str

            :returns: the modified version of s
            :rtype: str

            .. warning:: Might throw non catched Exception ?
        """
        return " ".join(re.sub("_", ' ', s).split())


    def expand(self, model, stop_words):

        """
            Pre-process data in preparation for the linguistic similarities measurements
            Pre-processin incudes tokenization, stop-words removing, unknown-words removing
            and embedding creation.

            :param model: The Spacy model used to compute the embedding, and tokenize the utterance
            :type model: spacy.lang.eng.English (or other language)
            :param stop_words: The list of function words
            :type stop_words: set

            :returns: Nothing, all changes are saved in the utterance's attributes
            :rtype: None
        """

        # tokenisation
        # tmp_gloss is a Spacy object: spacy.tokens.doc.Doc
        tmp_gloss = model(self.modified_gloss)
        self.tokens_gloss = list(map(str,tmp_gloss))
        self.length_gloss = len(self.tokens_gloss)

        # finding function words
        self.gloss_stopw = self.get_stop_words(self.tokens_gloss, stop_words)
        self.gloss_stopw_nbr = len(self.gloss_stopw)

        # finding unknown words
        self.gloss_unknowns = self.get_unknowns(tmp_gloss)
        self.gloss_unknowns_nbr = len(self.gloss_unknowns)

        # removing function words and unknown words from the tokens
        self.final_tokens_gloss = self.remove_tokens(self.tokens_gloss, self.gloss_stopw, self.gloss_unknowns)
        self.final_tokens_gloss_nbr = len(self.final_tokens_gloss)

        # creating the embedding
        self.embedding_gloss = self.compute_simi(self.final_tokens_gloss, tmp_gloss)

        # creating the part of speech
        self.pos_gloss = np.array([str(token.pos_) for token in tmp_gloss])


    def get_stop_words(self, str_array, sw_list):
        """
            Find every function words (stop words) listed in sw_list that are present in str_array

            :param str_array: array of words found in the original utterance
            :type str_array: numpy.ndarray([str])
            :param sw_list: The list of function words
            :type sw_list: set

            :returns: A string array reprensentation of the function words found in str_array
            :rtype: numpy.ndarray([str])
        """
        res = np.array([word for word in str_array if word in sw_list])

        return res


    def get_unknowns(self, str_tokens):
        """
            Find every unknown words that are present in str_tokens

            :param str_tokens: array of tokens (Spacy object) found in the original utterance
            :type str_tokens: spacy.tokens.doc.Doc

            :returns: A string array reprensentation of the unknown words found in str_tokens
            :rtype: numpy.ndarray([str])
        """
        res = np.array([str(word) for word in str_tokens if not word.is_oov or str(word) == "xxx" or str(word) == "xxxx" or str(word) == "yyy" or str(word) == "yyyy"])

        return res


    def remove_tokens(self, str_array, stop_words, unknowns):
        """
            Find every unknown words that are present in str_tokens

            :param str_array: array of words found in the original utterance
            :type str_array: numpy.ndarray([str])
            :param stop_words: A list of the function words found in str_array
            :type stop_words: numpy.ndarray([str])
            :param unknowns: A list of the unknown words found in str_array
            :type unknowns: numpy.ndarray([str])

            :returns: A string array representation of the tokens present in str_array, from which unknowns and function words have been removed
            :rtype: numpy.ndarray([str])
        """
        res = np.array([word for word in list(str_array) if word not in list(stop_words) and word not in list(unknowns)])

        return res


    def compute_simi(self, str_array, str_tokens):

        """
            Create a 300 dimension embedding representing the utterance

            :param str_array: array of words found in the original utterance, but from which function words and unknown words have been removed
            :type str_array: numpy.ndarray([str])
            :param str_tokens: array of tokens (Spacy object) found in the original utterance
            :type str_tokens: spacy.tokens.doc.Doc

            :returns: A 300 dimension vector, sum of the embeddings linked to each words contained in str_array
            :rtype: numpy.ndarray([float]*300)
        """
        # create an embedding for each word in str_tokens
        dict_word_vector = {}
        res = np.array([0]*300)
        for token in str_tokens:
            dict_word_vector[str(token)] = token.vector

        # successively add each embedding linked to a word in str_array
        for word in str_array:
            res = np.array(list(map(add, list(dict_word_vector[word]), list(res))))

        return res
