# children-linguistic-alignment

children-linguistic-alignment allows to compute the semantic, lexical and syntactic similarity between couples
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
<li>with French_20_25 being the name of the directory where the results will be stored (can be any name) but mandatory</li>
<li>with French being the language used to retrieve data from CHILDES. Mandatory</li>
<li>with 20 being the minimal age to be considered. Mandatory</li>
<li>with 25 being the maximal age to be considered. Mandatory</li>
<li>and True stating if the program is in test mode or not. Optional, default value: False</li>
</ul>

## Contributing
Please contact thomas.misiek@gmail.com to report any bug or if you want to add something to the code

## License

## Methods and how to interpret the results

After the end of a run, all the results are stored in Databases/your_directory_name/results.
To each treated age correspond a CSV file containing similarity measurements and other relevant data.
Here is an exhaustive list of the columns of the CSV file, what is contained in them, and how it is processed.

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
</br>

#### child_age:

The age of the target child in the transcript, only relevant for "chi->par", "par->chi" and "rand_in".
</br>
In "rand_ex" this is the age of the target child from the transcript from which the child utterance was retrieved. In this condition, the adult might have been speaking to a child of a different age.
</br>

#### child_sex:

The sex of the target child in the transcript, once again, only relevant for "chi->par", "par->chi" and "rand_in", for the same reason as for child_age.
</br>

#### child_id:

The id of the target child in the transcript, once again, only relevant for "chi->par", "par->chi" and "rand_in", for the same reason as for child_age.
</br>

#### parent_sex:

The sex of the target child in the transcript, once again, only relevant for "chi->par", "par->chi" and "rand_in", for the reversed reason as for child_age. This time the parent sex comes from the transcript from which the parent utterance was retrieved.
</br>

#### child_utterance_order:

Order of the utterance in its transcript, ie: 0 if it is the first sentences uttered in the transcript, 1 if it is the second...
</br>
It might be irrelevant for the "rand_ex" condition as child and adult utterances do not come from the same transcript
</br>

#### adult_utterance_order:

Same as child_utterance_order, but this time for the parent
</br>

#### child_transcript_id:

Id of the transcript from which the child utterance was retrieved
</br>

#### adult_transcript_id:

Id of the transcript from which the adult utterance was retrieved
</br>

#### child_corpus_name:

Name of the corpus from which the child utterance was retrieved
</br>

#### adult_corpus_name:

Name of the corpus from which the adult utterance was retrieved
</br>

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
</br>

#### editdistance:

Int that represent the Levenshtein distance between child and parent utterancse.
</br>
The Levenshtein distance is the number of deletions, insertions, or substitutions that are required to transform one string (the source) into another (the target).
</br>
Here the atomic level is the word (or the token), not the character.
</br>

#### child_utt:

A version of the original child utterance where any underscore has been removed.
</br>
Here the CHILDES "gloss" version of utterances have been used, as data are generally more complete than for the "stem" version of utterances. "gloss" utterances are the original transcription of the recorded conversations, sometimes even capturing mispronunciations from the speaker. Only the stem of each word has been saved in the "stem" version of utterances, which isn't relevant here.
</br>
For more informations, see the CHILDES documentation.
</br>

#### adult_utt:

A version of the original adult utterance where any underscore has been removed

</br>
Here the CHILDES "gloss" version of utterances have been used, as data are generally more complete than for the "stem" version of utterances. "gloss" utterances are the original transcription of the recorded conversations, sometimes even capturing mispronunciations from the speaker. Only the stem of each word has been saved in the "stem" version of utterances, which isn't relevant here.
</br>
For more informations, see the CHILDES documentation.
</br>

#### child_tokens:

A tokenized version of the original child utterance, after any underscore has been removed.
</br>
Tokenisation done using a Spacy model that is specific to the language selected by the user.
</br>

#### adult_tokens:

A tokenized version of the original adult utterance, after any underscore has been removed.
</br>
Tokenisation done using a Spacy model that is specific to the language selected by the user.
</br>

#### child_tokens_nbr:

Number of tokens in child_tokens, best estimation of the number of words in the original utterance.
</br>

#### adult_tokens_nbr:

Number of tokens in adult_tokens, best estimation of the number of words in the original utterance.
</br>

#### child_num_morphemes:

Number of morphemes in the child utterance
</br>

#### adult_num_morphemes:

Number of morphemes in the adult utterance
</br>

#### child_pos:

Part of speech of the child. Created using a Spacy model, specific to the language selected by the user.
It should be the same length as child_tokens.
</br>

#### adult_pos:

Part of speech of the adult. Created using a Spacy model, specific to the language selected by the user.
It should be the same length as adult_tokens.
</br>

#### child_pos_nbr:

Number of grammatical functions in child_pos
</br>

#### adult_pos_nbr:

Number of grammatical functions in adult_pos
</br>

#### child_unknown_words:

List of the unknown words in the child utterance. Unknown words are here, words that are not recognized in the Spacy model,
or words like "xxx", "xxxx", "yyy", "yyyy" that were used in the CHILDES corpus as a way to indicate that the speaker word was
not recognizable. Duplicates are not deleted.
</br>

#### adult_unknown_words:

List of the unknown words in the adult utterance. Unknown words are here, words that are not recognized in the Spacy model,
or words like "xxx", "xxxx", "yyy", "yyyy" that were used in the CHILDES corpus as a way to indicate that the speaker word was
not recognizable. Duplicates are not deleted.
</br>

#### child_unknown_words_nbr:

Number of words in child_unknown_words
</br>

#### adult_unknown_words_nbr:

Number of words in adult_unknown_words
</br>

#### child_stopwords:

List of the function words (also stop-words) that were found in the child utterance, specifically child_tokens.
Function words were defined for each language by Spacy.
</br>

#### adult_stopwords:

List of the function words (also stop-words) that were found in the adult utterance, specifically adult_tokens.
Function words were defined for each language by Spacy.
</br>

#### child_stopwords_nbr:

Number of words in child_stopwords
</br>

#### adult_stopwords_nbr:

Number of words in adult_stopwords
</br>

#### child_final_tokens:

Tokens present in child_tokens minus tokens in child_stopwords and child_unknown_words
</br>

#### adult_final_tokens:

Tokens present in adult_tokens minus tokens in adult_stopwords and adult_unknown_words
</br>

#### child_final_tokens_nbr:

Number of words in child_final_tokens
</br>

#### adult_final_tokens_nbr:

Number of words in adult_final_tokens
</br>

#### lexical_unigrams_nbr:

Number of lexical unigrams found both in parent and child utterance (specifically child_tokens and adult_tokens).
In other words: number of words that are identical in both child and parent utterances.
</br>

#### lexical_bigrams_nbr:

Number of lexical bigrams found both in parent and child utterance (specifically child_tokens and adult_tokens).
In other words: number of pairs of strictly consecutive words that are identical in both child and parent utterances.
</br>

#### lexical_trigrams_nbr:

Number of lexical trigrams found both in parent and child utterance (specifically child_tokens and adult_tokens).
</br>

#### syntax_unigrams_nbr:

Number of syntactic unigrams found both in parent and child utterance (specifically child_pos and adult_pos).
In other words: number of grammatical functions that are identical in both child and parent utterances.
</br>

#### syntax_bigrams_nbr:

Number of syntactic bigrams found both in parent and child utterance (specifically child_pos and adult_pos).
In other words: number of pairs of stricly consecutive grammatical functions that are identical in both child and parent utterances.
</br>

#### syntax_trigrams_nbr:

Number of syntactic trigrams found both in parent and child utterance (specifically child_pos and adult_pos).
</br>

#### syntax_minus_lexic_bigrams_nbr:
