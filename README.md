# children-linguistic-alignment

children-linguistic-alignment allows to compute the semantic, lexical and syntactic similarity of couples
of consecutive utterances retrieved from the CHILDES database, as well as several other measures.
6 languages available: English, French, Spanish, German, Chinese and Japanese.

## Installation

Install the project by cloning it on your computer or by downloading a compressed version

## Usage

Use the Run notebook, where an example call is already set up

Or you can also run the script run.py

For example: python run.py French_20_25 French 20 25 True
<br />

<ul>
<li>with French_20_25 being the name of the directory where the results will be stored (can be any name). Mandatory</li>
<li>with French being the language used to retrieve data from CHILDES (can be either of the 6 mentionned earlier). Mandatory</li>
<li>with 20 being the minimal age to be considered (min:10, max:80, included). Mandatory</li>
<li>with 25 being the maximal age to be considered (min:10, max:80, included). Mandatory</li>
<li>and True stating if the program is in test mode or not. Optional, default value: False</li>
</ul>

You should run a test first to ensure everything run fine, it should take 5 minutes.
Complete generation (10 month to 80) on my laptop take around two days for the English dataset (biggest CHILDES dataset), and around 6 hours for the other languages.

## Contributing
Please contact thomas.misiek@gmail.com to report any problem or if you want to add something to the code

## License

## Methods and how to interpret the results

After the end of a run, all the results are stored in Databases/your_directory_name/results.
To each treated age correspond a CSV file containing similarity measurements and other relevant data.
Here is an exhaustive list of the columns of the CSV file, what is contained in them, and how it is processed.
</br></br>


#### condition:

"rand_ex" if both utterances are taken at random in the whole CHILDES dataset (of the same language).
</br>
"rand_in" if both utterances are taken at random in the same transcript (conversation).
</br>
"chi->par" if the child speak first then the parent, and both utterances are strictly consecutive.
</br>
"par->chi" if the parent speak first then the child, and both utterances are strictly consecutive.
</br>
In "rand_in" and "rand_ex", the direction of speech make no sense, as utterances are almost never consecutive
</br>
Only single utterances are considered, groups of consecutive, uninterrupted utterances by the same speaker are not clustered,
so in all conditions, only the last and first utterance of a cluster might be taken into account.
</br>
In all conditions, both a parent and a child sentence are selected.
</br></br>


#### child_age:

The age of the target child in the transcript, only relevant for "chi->par", "par->chi" and "rand_in".
</br>
In "rand_ex" this is the age of the target child from the transcript from which the child utterance was retrieved. In this condition, the adult might have been speaking to a child of a different age.
</br></br>


#### child_sex:

The sex of the target child in the transcript, once again, only relevant for "chi->par", "par->chi" and "rand_in", for the same reason as for child_age.
</br></br>


#### child_id:

The id of the target child in the transcript, once again, only relevant for "chi->par", "par->chi" and "rand_in", for the same reason as for child_age.
</br></br>


#### parent_sex:

The sex of the target child in the transcript, once again, only relevant for "chi->par", "par->chi" and "rand_in", for the reversed reason as for child_age. This time the parent sex comes from the transcript from which the parent utterance was retrieved.
</br></br>


#### child_utterance_order:

Order of the utterance in its transcript, ie: 0 if it is the first sentences uttered in the transcript, 1 if it is the second...
</br>
It might be irrelevant for the "rand_ex" condition as child and adult utterances do not come from the same transcript
</br></br>


#### adult_utterance_order:

Same as child_utterance_order, but this time for the parent
</br></br>


#### child_transcript_id:

Id of the transcript from which the child utterance was retrieved
</br></br>


#### adult_transcript_id:

Id of the transcript from which the adult utterance was retrieved
</br></br>


#### child_corpus_name:

Name of the corpus from which the child utterance was retrieved
</br></br>


#### adult_corpus_name:

Name of the corpus from which the adult utterance was retrieved
</br></br>


#### semantic_similarity:

Float comprised between 0 and 1. The closer it is to 1, the higher the semantic similarity between the child and adult utterances.
</br>
It it computed by first tokenising both utterances using a Spacy model, specific to the language selected.
</br>
Tokens unknown to the Spacy models are removed from the utterances, function words (specified by Spacy) are removed too.
</br>
Each of the remaining tokens are transformed into a 300 dimension embedding using word2vec, then each of these embeddings are
summed to create one representation of the whole sentence.
</br>
The two resulting 300 dimension vectors representing the child and the adult utterances are used to compute the cosine similarity, which is our proxy for the semantic similarity.
</br></br>


#### editdistance:

Int that represent the Levenshtein distance between child and parent utterancse.
</br>
The Levenshtein distance is the number of deletions, insertions, or substitutions that are required to transform one string (the source) into another (the target).
</br>
Here the atomic level is the word (or the token), not the character.
</br></br>


#### child_utt:

A version of the original child utterance where any underscore has been removed.
</br>
Here the CHILDES "gloss" version of utterances have been used, as data are generally more complete than for the "stem" version of utterances. "gloss" utterances are the original transcription of the recorded conversations, sometimes even capturing mispronunciations from the speaker. Only the stem of each word has been saved in the "stem" version of utterances, which isn't relevant here.
</br>
For more informations, see the CHILDES documentation.
</br></br>


#### adult_utt:

A version of the original adult utterance where any underscore has been removed

</br>
Here the CHILDES "gloss" version of utterances have been used, as data are generally more complete than for the "stem" version of utterances. "gloss" utterances are the original transcription of the recorded conversations, sometimes even capturing mispronunciations from the speaker. Only the stem of each word has been saved in the "stem" version of utterances, which isn't relevant here.
</br>
For more informations, see the CHILDES documentation.
</br></br>


#### child_tokens:

A tokenized version of the original child utterance, after any underscore has been removed.
</br>
Tokenisation done using a Spacy model that is specific to the language selected by the user.
</br></br>


#### adult_tokens:

A tokenized version of the original adult utterance, after any underscore has been removed.
</br>
Tokenisation done using a Spacy model that is specific to the language selected by the user.
</br></br>


#### child_tokens_nbr:

Number of tokens in child_tokens, best estimation of the number of words in the original utterance.
</br></br>


#### adult_tokens_nbr:

Number of tokens in adult_tokens, best estimation of the number of words in the original utterance.
</br></br>


#### child_num_morphemes:

Number of morphemes in the child utterance
</br></br>


#### adult_num_morphemes:

Number of morphemes in the adult utterance
</br></br>


#### child_pos:

Part of speech of the child. Created using a Spacy model, specific to the language selected by the user.
It should be the same length as child_tokens.
</br></br>


#### adult_pos:

Part of speech of the adult. Created using a Spacy model, specific to the language selected by the user.
It should be the same length as adult_tokens.
</br></br>


#### child_pos_nbr:

Number of grammatical functions in child_pos
</br></br>


#### adult_pos_nbr:

Number of grammatical functions in adult_pos
</br></br>


#### child_unknown_words:

List of the unknown words in the child utterance. Unknown words are here, words that are not recognized in the Spacy model,
or words like "xxx", "xxxx", "yyy", "yyyy" that were used in the CHILDES corpus as a way to indicate that the speaker word was
not recognizable. Duplicates are not deleted.
</br></br>


#### adult_unknown_words:

List of the unknown words in the adult utterance. Unknown words are here, words that are not recognized in the Spacy model,
or words like "xxx", "xxxx", "yyy", "yyyy" that were used in the CHILDES corpus as a way to indicate that the speaker word was
not recognizable. Duplicates are not deleted.
</br></br>


#### child_unknown_words_nbr:

Number of words in child_unknown_words
</br></br>


#### adult_unknown_words_nbr:

Number of words in adult_unknown_words
</br></br>


#### child_stopwords:

List of the function words (also stop-words) that were found in the child utterance, specifically child_tokens.
Function words were defined for each language by Spacy.
</br></br>


#### adult_stopwords:

List of the function words (also stop-words) that were found in the adult utterance, specifically adult_tokens.
Function words were defined for each language by Spacy.
</br></br>


#### child_stopwords_nbr:

Number of words in child_stopwords
</br></br>


#### adult_stopwords_nbr:

Number of words in adult_stopwords
</br></br>


#### child_final_tokens:

Tokens present in child_tokens minus tokens in child_stopwords and child_unknown_words
</br></br>


#### adult_final_tokens:

Tokens present in adult_tokens minus tokens in adult_stopwords and adult_unknown_words
</br></br>


#### child_final_tokens_nbr:

Number of words in child_final_tokens
</br></br>


#### adult_final_tokens_nbr:

Number of words in adult_final_tokens
</br></br>


#### lexical_unigrams_nbr:

Number of lexical unigrams found both in parent and child utterance (specifically child_tokens and adult_tokens).
</br>
In other words: number of words that are identical in both child and parent utterances.
</br></br>


#### lexical_bigrams_nbr:

Number of lexical bigrams found both in parent and child utterance (specifically child_tokens and adult_tokens).
</br>
In other words: number of pairs of strictly consecutive words that are identical in both child and parent utterances.
</br></br>


#### lexical_trigrams_nbr:

Number of lexical trigrams found both in parent and child utterance (specifically child_tokens and adult_tokens).
</br></br>


#### syntax_unigrams_nbr:

Number of syntactic unigrams found both in parent and child utterance (specifically child_pos and adult_pos).
</br>
In other words: number of grammatical functions that are identical in both child and parent utterances.
</br></br>


#### syntax_bigrams_nbr:

Number of syntactic bigrams found both in parent and child utterance (specifically child_pos and adult_pos).
</br>
In other words: number of pairs of stricly consecutive grammatical functions that are identical in both child and parent utterances.
</br></br>


#### syntax_trigrams_nbr:

Number of syntactic trigrams found both in parent and child utterance (specifically child_pos and adult_pos).
</br></br>


#### syntax_minus_lexic_bigrams_nbr:

Number of syntactic bigrams that are not at the same time lexical bigrams.
In other words: number of pairs of consecutive words that are of the same grammatical function in the child and in the adult utterances, but which are not exactly, lexically similar.
</br></br>


#### syntax_minus_lexic_trigrams_nbr:

Number of syntactic trigrams that are not at the same time lexical trigrams.
</br></br>


#### out_of_child_vocab_nbr_1:

Number of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age.
Here, the age of acquisition (AoA) of a word is computed as the age where children younger than AoA have pronounced 1% of all its occurrences in the whole CHILDES dataset, of a specific language.
</br></br>


#### ooc_vocab_words_1:

List of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age and a 1% threshold. (see out_of_child_vocab_nbr_1)
</br></br>


#### out_of_child_vocab_nbr_3:

Number of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age.
Here, the age of acquisition (AoA) of a word is computed as the age where children younger than AoA have pronounced 3% of all its occurrences in the whole CHILDES dataset, of a specific language.
</br></br>


#### ooc_vocab_words_3:

List of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age and a 3% threshold. (see out_of_child_vocab_nbr_3)
</br></br>


#### out_of_child_vocab_nbr_10:

Number of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age.
Here, the age of acquisition (AoA) of a word is computed as the age where children younger than AoA have pronounced 10% of all its occurrences in the whole CHILDES dataset, of a specific language.
</br></br>


#### ooc_vocab_words_10:

List of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age and a 10% threshold. (see out_of_child_vocab_nbr_10)
</br></br>


#### out_of_child_vocab_nbr_20:

Number of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age.
Here, the age of acquisition (AoA) of a word is computed as the age where children younger than AoA have pronounced 20% of all its occurrences in the whole CHILDES dataset, of a specific language.
</br></br>


#### ooc_vocab_words_20:

List of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age and a 20% threshold. (see out_of_child_vocab_nbr_20)
</br></br>


#### out_of_child_vocab_nbr_50:

Number of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age.
Here, the age of acquisition (AoA) of a word is computed as the age where children younger than AoA have pronounced 50% of all its occurrences in the whole CHILDES dataset, of a specific language.
</br></br>


#### ooc_vocab_words_50:

List of words in the adult utterance (specifically adult_tokens) that are out of the child vocabulary considering his age and a 50% threshold. (see out_of_child_vocab_nbr_50)
</br></br>
