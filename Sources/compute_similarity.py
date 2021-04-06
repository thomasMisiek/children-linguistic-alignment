import nltk
import settings
import editdistance
from utterance import Utterance
from sklearn.metrics.pairwise import cosine_similarity


def get_data(row1, row2, vocabulary_gloss, model, fw, precondition):

    """
        Pre-process data, creates embedding, part of speech, etc... of row1 and row2,
        computes linguistic similarities between both utterances, return these measures
        and complementary information in a dictionnary.

        :param row1: A row of a pre-processed Dataframe, the row contain all useful
        informations about an utterance
        :type row1: pandas.Series
        :param row2: A row of a pre-processed Dataframe, the row contain all
        useful informations about an utterance
        :type row2: pandas.Series
        :param vocabulary_gloss: List of five dictionnaries mapping words to their age
        of acquisition, according to different thresholds
        :type vocabulary_gloss: list of dict{str:int}
        :param model: The spacy model that will be used to create embeddings of utterances,
        tokenise them and create parts of speech
        :type model: spacy.lang.en.English (or other languages)
        :param fw: The list of function words of the specified language, retrieved from Spacy
        :type fw: set
        :param precondition: Can have three values: "normal", "rand_in" and "rand_ex",
        define if row1 and row2 are respectively strictly consecutives, or at least in the same transcript,
        or finally chosen at random in the whole CHILDES corpus
        :type precondition: str

        :returns: A dictionnary containing all the linguistic similarities measures and relevant
        informations about the couple of utterance represented by row1 and row2
        :rtype: None

    """

    # pre-process further the utterances represented by row1 and row2, create embeddings,
    # parts of speech, search for unknown and function words ...
    utt1 = Utterance(row1.gloss, row1.speaker_id, row1.type)
    utt2 = Utterance(row2.gloss, row2.speaker_id, row2.type)
    utt1.expand(model, fw)
    utt2.expand(model, fw)

    condition = get_condition(row1, row2, precondition)

    if row1.speaker_code in settings.child_cond:
        child_row = row1
        adult_row = row2
        child_utt = utt1
        adult_utt = utt2
    else:
        child_row = row2
        adult_row = row1
        child_utt = utt2
        adult_utt = utt1

    [vocabulary_1, vocabulary_3, vocabulary_10, vocabulary_20, vocabulary_50] = vocabulary_gloss

    lexical_unigrams_nbr = get_simple_ngrams_nbr(utt1.tokens_gloss,utt2.tokens_gloss,1)
    lexical_bigrams_nbr = get_simple_ngrams_nbr(utt1.tokens_gloss,utt2.tokens_gloss,2)
    lexical_trigrams_nbr = get_simple_ngrams_nbr(utt1.tokens_gloss,utt2.tokens_gloss,3)
    syntax_unigrams_nbr = get_simple_ngrams_nbr(utt1.pos_gloss,utt2.pos_gloss,1)
    syntax_bigrams_nbr = get_simple_ngrams_nbr(utt1.pos_gloss,utt2.pos_gloss,2)
    syntax_trigrams_nbr = get_simple_ngrams_nbr(utt1.pos_gloss,utt2.pos_gloss,3)
    syntax_minus_lexic_bigrams_nbr = get_syntax_minus_lexical_ngrams_nbr(utt1.tokens_gloss,utt2.tokens_gloss, utt1.pos_gloss,utt2.pos_gloss,2)
    syntax_minus_lexic_trigrams_nbr = get_syntax_minus_lexical_ngrams_nbr(utt1.tokens_gloss,utt2.tokens_gloss, utt1.pos_gloss,utt2.pos_gloss,3)

    oov_nbr_1, oov_list_1 = out_of_child_vocab(adult_utt.tokens_gloss, child_row.target_child_age, vocabulary_1)
    oov_nbr_3, oov_list_3 = out_of_child_vocab(adult_utt.tokens_gloss, child_row.target_child_age, vocabulary_3)
    oov_nbr_10, oov_list_10 = out_of_child_vocab(adult_utt.tokens_gloss, child_row.target_child_age, vocabulary_10)
    oov_nbr_20, oov_list_20 = out_of_child_vocab(adult_utt.tokens_gloss, child_row.target_child_age, vocabulary_20)
    oov_nbr_50, oov_list_50 = out_of_child_vocab(adult_utt.tokens_gloss, child_row.target_child_age, vocabulary_50)

    semantic_similarity = get_cosine_similarity(utt1.embedding_gloss, utt2.embedding_gloss)

    lev_dist = nltk.edit_distance(utt1.tokens_gloss, utt2.tokens_gloss)

    # from child_age to parent_sex is only relevant for the normal condition
    res = {

          "condition": condition,
          "child_age": row1.target_child_age,
          "child_sex": row1.target_child_sex,
          "child_id": row1.target_child_id,
          "parent_sex": parent_sex(adult_row),
          "child_utterance_order": child_row.utterance_order,
          "adult_utterance_order": adult_row.utterance_order,
          "child_transcript_id": child_row.transcript_id,
          "adult_transcript_id": adult_row.transcript_id,
          "child_corpus_name": child_row.corpus_name,
          "adult_corpus_name": adult_row.corpus_name,

          "semantic_similarity": semantic_similarity,
          "editdistance": lev_dist,

          "child_utt": child_utt.modified_gloss,
          "adult_utt": adult_utt.modified_gloss,

          "child_num_morphemes": child_row.num_morphemes,
          "adult_num_morphemes": adult_row.num_morphemes,

          "child_unknown_words": str(list(child_utt.gloss_unknowns)),
          "adult_unknown_words": str(list(adult_utt.gloss_unknowns)),

          "child_unknown_words_nbr": child_utt.gloss_unknowns_nbr,
          "adult_unknown_words_nbr": adult_utt.gloss_unknowns_nbr,

          "child_stopwords": str(list(child_utt.gloss_stopw)),
          "adult_stopwords": str(list(adult_utt.gloss_stopw)),

          "child_stopwords_nbr": child_utt.gloss_stopw_nbr,
          "adult_stopwords_nbr": adult_utt.gloss_stopw_nbr,

          "child_final_tokens": str(list(child_utt.final_tokens_gloss)),
          "adult_final_tokens": str(list(adult_utt.final_tokens_gloss)),

          "child_final_tokens_nbr": child_utt.final_tokens_gloss_nbr,
          "adult_final_tokens_nbr": adult_utt.final_tokens_gloss_nbr,

          "lexical_unigrams_nbr": lexical_unigrams_nbr,
          "lexical_bigrams_nbr": lexical_bigrams_nbr,
          "lexical_trigrams_nbr": lexical_trigrams_nbr,
          "syntax_unigrams_nbr": syntax_unigrams_nbr,
          "syntax_bigrams_nbr": syntax_bigrams_nbr,
          "syntax_trigrams_nbr": syntax_trigrams_nbr,
          "syntax_minus_lexic_bigrams_nbr": syntax_minus_lexic_bigrams_nbr,
          "syntax_minus_lexic_trigrams_nbr": syntax_minus_lexic_trigrams_nbr,

          "out_of_child_vocab_nbr_1": oov_nbr_1,
          "ooc_vocab_words_1": oov_list_1,
          "out_of_child_vocab_nbr_3": oov_nbr_3,
          "ooc_vocab_words_3": oov_list_3,
          "out_of_child_vocab_nbr_10": oov_nbr_10,
          "ooc_vocab_words_10": oov_list_10,
          "out_of_child_vocab_nbr_20": oov_nbr_20,
          "ooc_vocab_words_20": oov_list_20,
          "out_of_child_vocab_nbr_50": oov_nbr_50,
          "ooc_vocab_words_50": oov_list_50

          }

    return res


# return the ngrams that are in ngrams1 and at the same time in ngrams2
# ngrams -> list of tuples
def intersection(ngrams1, ngrams2):
    if type(ngrams1) != list:
        raise TypeError("should be of type list")
    if type(ngrams2) != list:
        raise TypeError("should be of type list")
    return [value for value in ngrams1 if value in ngrams2]


# return the number of ngrams that are at the same time in str_list_1 and in str_list_2
# n defines the n in ngram
def get_simple_ngrams_nbr(str_list_1, str_list_2, n):
    # ngrams return a generator, hence the cast
    ngrams1 = list(nltk.ngrams(str_list_1, n))
    ngrams2 = list(nltk.ngrams(str_list_2, n))
    return len(intersection(ngrams1, ngrams2))


def get_syntax_minus_lexical_ngrams_nbr(words_list_1, words_list_2, pos_1, pos_2, n):
    """
        Search for grammatical ngrams that are not lexical ngrams, in other words,
        gramatically identical series of words that are not lexically the same.

        :param words_list_1: the list of words contained in the first utterance
        :type words_list_1: str list
        :param words_list_2: the list of words contained in the second utterance
        :type words_list_2: str list
        :param pos_1: The part of speech in the first utterance
        :type pos_1: str list
        :param pos_2: The part of speech in the second utterance
        :type pos_2: str list
        :param n: n defines the n in ngram
        :type n: int

        :returns: The number of grammatical ngrams that are not lexical ngrams
        :rtype: int
    """
    # intuitively, part of speech should be aligned and hence of same length than the tokenised sentence
    if len(words_list_1) != len(pos_1) or len(words_list_2) != len(pos_2):
        return "ERROR"

    res = 0

    for i in range(len(words_list_1)):
        for j in range(len(words_list_2)):
            if words_list_1[i] != words_list_2[j] and pos_1[i] == pos_2[j]:
                 res += 1
    return res


def get_cosine_similarity(feature_vec_1, feature_vec_2):
    """
        :param feature_vec_1: A 300 dimension embedding, representing the first utterance
        :type feature_vec_1: numpy.ndarray([float]*300)
        :param feature_vec_2: A 300 dimension embedding, representing the second utterance
        :type feature_vec_2: numpy.ndarray([float]*300)

        :returns: The cosine similarity between both vectors in parameters, value between 0 and 1
        :rtype: float
    """
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]


def out_of_child_vocab(words, age, vocabulary):
    """
        Search for words that are considered not to be known by a children of a
        specified age, in a given sentence

        :param words: the words prononced in a sentence
        :type words: str list
        :param age: the age of a child
        :type age: int
        :param vocabulary: The dictionnary encoding the age of acquisition of words according to the data of CHILDES
        :type vocabulary: dict{str:int}

        :returns: The number of still unknown words in the sentence in parameter, and the list of these unknown words
        :rtype: int, list[str]
    """
    nbr_unknown = 0
    unknown_words = []
    # words that are prononced less than 10 times in the whole CHILDES database
    # are not present in vocabulary
    for word in words:

        if word in vocabulary and vocabulary[word] > age:
            unknown_words.append(word)
            nbr_unknown += 1

    return nbr_unknown, unknown_words


def get_condition(row1, row2, precondition):
    """
        Specify the condition of the interaction between a child and his parent,
        which can be of 4 different types (see returns)

        :param row1: A row of a pre-processed Dataframe, the row contain all useful
        informations about an utterance
        :type row1: pandas.Series
        :param row2: A row of a pre-processed Dataframe, the row contain all
        useful informations about an utterance
        :type row2: pandas.Series
        :param precondition: Can have three values: "normal", "rand_in" and "rand_ex",
        define if row1 and row2 are respectively strictly consecutives, or at least in the same transcript,
        or finally chosen at random in the whole CHILDES corpus
        :type precondition: str

        :returns: "chi->par" if the child speak first then the parent,
        "par->chi" if the parent speak first then the child, "rand_in" or "rand_ex" otherwise,
        as in these last two condition, the direction of speech make non sense, as utterances are non consecutive
        :rtype: str
    """
    if precondition == "normal":
        if row1.speaker_code in settings.child_cond and row2.speaker_code in settings.adult_cond:
            return "chi->par"
        return "par->chi"
    else:
        return precondition


def parent_sex(row):
    """
        :param row1: A Dataframe row containing all useful informations about an utterance
        :type row1: pandas.Series
        :returns: the sex of the parent
        :rtype: str
    """
    if row.speaker_code in settings.mother_cond:
        return "female"
    elif row.speaker_code in settings.father_cond:
        return "male"
    else:
        return "unknown"
