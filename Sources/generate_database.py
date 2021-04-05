from compute_similarity import get_data
from compute_vocabulary import create_vocabulary

import os
import re
import sys
import csv
import time
import glob
import admin
import spacy
import pickle
import pandas as pd
from os import path
import subprocess as sub
from random import randint
from gensim.models import KeyedVectors

import settings


def process_similarities(directory, language, age_min, age_max, test):

    """
        Retrieve raw data from the CHILDES database, pre-process it and compute
        the linguistic similarities measures.

        :param directory: The name of the directory in which all the intermediate
        and results data files will be stored
        :type directory: str
        :param language: The language from which CHILDES transcripts will be selected
        :type directory: str
        :param age_min: The minimum target childs age at which utterances will be retrieved
        :type age_min: int
        :param age_max: The maximum target childs age at which utterances will be retrieved
        :type age_max: int
        :param test: If True, only a small amount of utterances will be selected for each age,
        in order to accelerate processing. It is a development oriented parameter
        :type test: bool

        :returns: Nothing, but results like linguistic similarities are saved in
        several CSV files in the specified directory, one CSV for each target child age
        :rtype: None

        .. seealso:: Run.ipynb notebook
        .. warning:: language parameter values should either be: "English", "French", "Spanish",
        "German", "Chinese" or "Japanese.
    """
    # create a specific directory for tests, to avoid erasing previously generated data
    if test:
        directory += "_test"

    if not os.path.isdir("../Databases/"+directory):
        print("Beginning the creation of a new database \n")
    else:
        print("Expanding the already existing "+directory+" database \n")

    # this is necessary as a parameter need to be modified on windows
    # for processing of japanese and chinese characters
    if language == "Japanese" or language == "Chinese":
        admin.runAsAdmin()


    print("\nInitializing settings")
    settings.init()

    print("\nCreating the initial directories architecture")
    create_architecture(directory)

    print("\nRetrieving raw data from CHILDES")
    retrieve_childes_data(directory, language, age_min, age_max, test)

    print("\nCharging the stop-words")
    fw = settings.dic_SW[language]

    if not os.path.isdir("../Databases/"+directory+"/vocabulary"):
        print("\nCreating the vocabulary")
        create_vocabulary(directory, [1,3,10,20,50])
    print("\nCharging the vocabulary")
    vocabulary = get_vocab(directory)

    print("\nCharging the spacy model ")
    nlp = spacy.load(settings.dic_spacy[language])

    print("\nExpanding each transcripts objects by processing embeddings of each utterances")
    for age in range(age_min, age_max+1):
        expand_data(age, nlp, fw, directory, vocabulary)

    print("\nDone, all data is accessible in '../Databases/"+directory+"/results.csv'")


# Creates the target directory and its subfolders if they don't exist
def create_architecture(directory):

    if not os.path.isdir("../Databases"):
        os.mkdir("../Databases")
        print("Created a 'Databases' folder")
    else:
        print("'Databases' folder already exist")

    if not os.path.isdir("../Databases/"+directory):
        os.mkdir("../Databases/"+directory)
        print("Created a 'Databases/"+directory+"' folder")
    else:
        print("'Databases/"+directory+"' folder already exist")

    if not os.path.isdir("../Databases/"+directory+"/raw"):
        os.mkdir("../Databases/"+directory+"/raw")
        print("Created a 'Databases/"+directory+"/raw' folder")
    else:
        print("'Databases/"+directory+"/raw' folder already exist")

    if not os.path.isdir("../Databases/"+directory+"/modified"):
        os.mkdir("../Databases/"+directory+"/modified")
        print("Created a 'Databases/"+directory+"/modified' folder")
    else:
        print("'Databases/"+directory+"/modified' folder already exist")

    if not os.path.isdir("../Databases/"+directory+"/results"):
        os.mkdir("../Databases/"+directory+"/results")
        print("Created a 'Databases/"+directory+"/results' folder")
    else:
        print("'Databases/"+directory+"/results' folder already exist")


def retrieve_childes_data(directory, language, age_min, age_max, test):

    """
        Retrieve raw data from the CHILDES database and pre-process it in
        preparation of the computing of the similarities measures.

        :param directory: The name of the directory in which all the intermediate
        and results data files will be stored
        :type directory: str
        :param language: The language from which CHILDES transcripts will be selected
        :type directory: str
        :param age_min: The minimum target childs age at which utterances will be retrieved
        :type age_min: int
        :param age_max: The maximum target childs age at which utterances will be retrieved
        :type age_max: int
        :param test: If True, only a small amount of utterances will be selected for each age,
        in order to accelerate processing. It is a development oriented parameter
        :type test: bool

        :returns: Nothing, but pre-processed CSV representing all the utterances
        retrieved from the specified language transcripts of CHILDES are saved
        in the specified directory.
        :rtype: None

        .. seealso:: Run.ipynb notebook
        .. warning:: The rscript that the charge_age function calls can fail
        trying to retrieve a specific age transcript's utterances for several
        times, mainly in case of failed connection from either CHILDES server or
        the user computer, if after several unsuccessful attempts to retrieve
        the data, the calls keep failing, the program will stop.
    """

    if os.path.isfile("../Databases/"+directory+"/original_merged.csv"):
        print("\nAll raw data has already been retrieved from CHILDES")
        print("\n'Databases/"+directory+"/original_merged.csv' file already exist")

    else:
        for age in range(age_min, age_max+1):
            if not os.path.isfile("../Databases/"+directory+"/raw/"+str(age)+".csv"):
                print("Currently retrieving utterances for the " +str(age) + " month age")
                charge_age(directory, settings.dic_childes[language], age, 100, 3)
            else:
                print("'Databases/"+directory+"/raw/"+str(age)+".csv' file already exist")

        # reduce the number of utterances for each age to 1000 to speed up the process
        if test:
            extension = 'csv'
            all_filenames = [filename for filename in glob.glob('../Databases/'+directory+'/raw/*.{}'.format(extension))]
            for filename in all_filenames:
                df = pd.read_csv(filename, engine="python", encoding='utf-8')
                df = df[0:1000]
                df.to_csv(filename,index=False, encoding='utf-8')

        print("All the raw transcripts were stored by target children's age as CSV files in the 'Databases/"+directory+"/raw' folder")

        print("\nPreprocessing all raw files")

        for age in range(age_min, age_max+1):
            raw_filename = "../Databases/"+directory+"/raw/"+str(age)+".csv"
            modified_filename = "../Databases/"+directory+"/modified/"+str(age)+".csv"
            if os.path.isfile(modified_filename):
                print(modified_filename+" file already exist")
            else:
                print("Creating the '"+modified_filename+"' file")

                df = pd.read_csv(raw_filename, engine="python", encoding='utf-8')
                df["target_child_age"] = df["target_child_age"].astype(int)
                del df["Unnamed: 0"]
                df = df.sort_values(["target_child_age", "transcript_id", "utterance_order"], ascending=[True, True, True])
                # reset index, otherwise index restart at each age
                df = df.reset_index()
                # is useful to allow restarting of the process without loosing what was previously generated
                df["Indice"] = df.index
                df = df[df['gloss'].notna()]

                df.to_csv("../Databases/"+directory+"/modified/"+str(age)+".csv", index=False, encoding='utf-8')


def charge_age(directory, language, age, delay = 100, trial_nbr = 5, failure_nbr = 0):

    """
        Recursive function that retrieve all english utterances of a certain age (in month)
        from the CHILDES corpus by calling an rscript, and store these utterances and their
        related informations unordered in a CSV file

        :param directory: The name of the directory in which the CSV file containing
        raw unordered data retrieved from CHILDES will be stored
        :type directory: str

        :param language: The first three letters of the language selected by the user
        (languages IDs in CHILDES are the first three letter of the language)
        :type language: str

        :param age: The age of the target child in the transcripts from which utterances
        will be retrieved
        :type age: int

        :param delay: Time to wait before considering the trial to retrieve data has been
        unsuccessful
        :type delay: int

        :param trial_nbr: Number of trial that are left to retrieve the data, a trial
        is considered failed when the delay has been passed
        :type trial_nbr: int

        :param failure_nbr: Number of trial that has been failed until now
        :type failure_nbr: int

        :returns: Nothing
        :rtype: None

        .. seealso:: create_database() function
        .. warning:: The rscript that the charge_age function calls can fail
        trying to retrieve a specific age transcript's utterances for several
        times, mainly in case of failed connection from either CHILDES server or
        the user computer, if after several unsuccessful attempts to retrieve
        the data the calls keel failing, the program will stop.
        .. note:: Nothing
        .. todo:: Nothing
    """
    # command that will activate the rscript
    cmd_line = [r"C:\Program Files\R\R-3.6.1\bin\Rscript", "script_get_raw_trscrpt.R", language, str(age), "../Databases/"+directory+"/raw/"]
    sub.Popen(cmd_line)

    # creation of the timer to measure the delay
    now = time.time()
    future  = now + delay
    # while the delay hasn't been passed and the CSV file creation is not done
    while time.time() < future and not os.path.isfile("../Databases/"+directory+"/raw/"+str(age)+".csv"):
        # delay to allow the OS to save the CSV file before letting the program
        # search for it
        time.sleep(0.4)
    # if the delay has passed without creation of CSV file
    if not os.path.isfile("../Databases/"+directory+"/raw/"+str(age)+".csv"):
        # if there is still trials left
        if trial_nbr > 0:
            print("The delay of retrieval for children of age: "+str(age)+" months has passed "+str(failure_nbr+1)+ " times")
            charge_age(directory, language, age, delay, trial_nbr-1, failure_nbr + 1)
        else:
            sys.exit("There has been recurring problems during retrieval of data for children of age: "+str(age)+" months, the program will stop")


# charge and return the age of acquisition dictionnaries of children, considering
# different thresholds
def get_vocab(directory):

    vocabularygloss1 = pickle.load( open("../Databases/"+directory+"/vocabulary/1.p", "rb" ) )
    vocabularygloss3 = pickle.load( open("../Databases/"+directory+"/vocabulary/3.p", "rb" ) )
    vocabularygloss10 = pickle.load( open("../Databases/"+directory+"/vocabulary/10.p", "rb" ) )
    vocabularygloss20 = pickle.load( open("../Databases/"+directory+"/vocabulary/20.p", "rb" ) )
    vocabularygloss50 = pickle.load( open("../Databases/"+directory+"/vocabulary/50.p", "rb" ) )

    return [vocabularygloss1, vocabularygloss3, vocabularygloss10, vocabularygloss20, vocabularygloss50]


def expand_data(age, model, fw, directory, vocabulary_gloss):

    """
        Use pre-processed CHILDES data from CSV files (see retrieve_childes_data()),
        compute embeddings and then similarities measures of couple of utterances between
        parents and target childs from a specific age.
        Store the results inside a CSV file.

        :param age: The target child age.
        :type age: int
        :param model: The spacy model that will be used to create embeddings of utterances,
        tokenise them and create parts of speech
        :type model: spacy.lang.en.English (or other languages)
        :param fw: The list of stop words retrieved from Spacy, and that will be
        removed from the computations
        :type fw: set
        :param directory: The name of the directory in which the CSV file containing
        the results will be saved, and in which pre-processed CSV are already stored
        :type directory: str
        :param vocabulary_gloss: List of five dictionnaries mapping words to their age
        of acquisition, according to different thresholds
        :type vocabulary_gloss: list of dict{str:int}

        :returns: Nothing, but the results are stored in a CSV file in the specified directory.
        :rtype: None

    """
    if os.path.isfile("../Databases/"+directory+"/results/"+str(age)+".csv"):
        print("\n"+str(age)+" month age has already been treated")
        return
    elif os.path.isfile("../Databases/"+directory+"/results/"+str(age)+"_processing.csv"):
        os.remove("../Databases/"+directory+"/results/"+str(age)+"_processing.csv")

    print("\nCurrently computing similarities for "+str(age)+" month age")

    df_final = pd.DataFrame(columns=get_column_names())
    # saving empty dataframe to erase potential previous one
    df_final.to_csv("../Databases/"+directory+"/results/"+str(age)+"_processing.csv", index=False, encoding='utf-8')

    df = pd.read_csv("../Databases/"+directory+"/modified/"+str(age)+".csv",engine="python", encoding='utf-8')

    with open("../Databases/"+directory+"/results/"+str(age)+"_processing.csv",'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        previous_row = None
        # df is specific to an age, and sub_df to a transcript
        sub_df = None
        previous_transcript_id = None

        # each row is an utterance
        for (i, row) in df.iterrows():
            # if its not the first row of df
            if previous_row is not None:

                # check that two rows are from a target child and a parent
                if check_couple(previous_row, row):


                    if sub_df is None or previous_transcript_id != previous_row.transcript_id:
                        sub_df = df[df["transcript_id"]==previous_row.transcript_id]
                        previous_transcript_id = previous_row.transcript_id

                    # random condition inside the transcript, rand_in_row and row
                    # are from parent and child but not necessarily consecutives
                    rand_in_row = get_random(sub_df, previous_row)
                    # randon condition outside the transcript, rand_in_row and row
                    # are from parent and child but might not be from the same transcript
                    rand_ex_row = get_random(df, previous_row)

                    # chi->par or par-chi condition, the two utterances are consecutives

                    data = get_data(previous_row, row, vocabulary_gloss, model, fw, "normal")
                    writer.writerow(list(data.values()))

                    data = get_data(previous_row, rand_in_row, vocabulary_gloss, model, fw, "rand_in")
                    writer.writerow(list(data.values()))

                    data = get_data(previous_row, rand_ex_row, vocabulary_gloss, model, fw, "rand_ex")
                    writer.writerow(list(data.values()))



            previous_row = row

    # change name of the current results file, to indicate
    # that processing is done and the file is complete and won't need to be erased
    # if the generation has to be stopped and rerun again
    os.rename("../Databases/"+directory+"/results/"+str(age)+"_processing.csv", "../Databases/"+directory+"/results/"+str(age)+".csv")


def get_random(df, row):

    """
        Try to find an utterance in df that has been prononced by a child if row
        has been prononced by an adult, and by an adult if row has been prononced
        by a child

        :param df: a DataFrame that contain either all the data of a transcript, or
        all the data of all corpuses of a specific language in CHILDES
        :type age: pandas.DataFrame
        :param row: a specific row of df, which represent an utterance
        :type row: pandas.core.series.Series

        :returns: Nothing, but the results are stored in a CSV file in the specified directory.
        :rtype: None

    """
    cpt_fail = 0
    # if the utterance described by row has been prononced by a parent
    if row.speaker_code in settings.adult_cond:
        res_row = None
        while res_row is None or res_row.speaker_code in settings.child_cond:
            # select a random row in df
            res_row = df.iloc[randint(0, len(df)-1)]
            cpt_fail += 1
            if cpt_fail > 1000:
                raise Exception("Too much attempts to find a fitting random utterance")

        return res_row

    # if the utterance described by row has been prononced by a child
    else:
        res_row = None
        while res_row is None or res_row.speaker_code in settings.adult_cond:
            # select a random row in df
            res_row = df.iloc[randint(0, len(df)-1)]
            cpt_fail += 1
            if cpt_fail > 1000:
                raise Exception("Too much attempts to find a fitting random utterance")

        return res_row


# check if two utterances, here rows of a Dataframe, are in the same transcript,
# are consecutives, and were prononced by a child and an adult
def check_couple(row1, row2):

    try:
        if row1.transcript_id != row2.transcript_id:
            raise Exception("Utterances are not from the same transcript")
        if not ((row1.speaker_code in settings.child_cond and row2.speaker_code in settings.adult_cond) or (row1.speaker_code in settings.adult_cond and row2.speaker_code in settings.child_cond)):
            raise Exception("Utterances do not share a chi->par or par->chi relation")
        if abs(row1.utterance_order - row2.utterance_order) != 1:
            raise Exception("Utterances are not consecutives")
    except:
        return False
    return True


# return the name of the column of the final CSV file containing all the results,
# like for exemple linguistic similarities measures.
def get_column_names():

    return ["type",
          "child_age",
          "child_sex",
          "child_id",
          "parent_sex",
          "transcript_id",
          "corpus_name",
          "id",
          "simi_gloss",
          "editdistance_gloss",

          "out_of_child_vocab_words_gloss-1",
          "ooc_vocab_words_gloss_nbr-1",
          "out_of_child_vocab_words_gloss-3",
          "ooc_vocab_words_gloss_nbr-3",
          "out_of_child_vocab_words_gloss-10",
          "ooc_vocab_words_gloss_nbr-10",
          "out_of_child_vocab_words_gloss-20",
          "ooc_vocab_words_gloss_nbr-20",
          "out_of_child_vocab_words_gloss-50",
          "ooc_vocab_words_gloss_nbr-50",

          "utt1_gloss",
          "utt2_gloss",

          "utt1_num_morphemes",
          "utt2_num_morphemes",

          "utt1_unknown_words_gloss",
          "utt2_unknown_words_gloss",

          "utt1_unknown_words_gloss_nbr",
          "utt2_unknown_words_gloss_nbr",

          "utt1_stopwords_gloss",
          "utt2_stopwords_gloss",

          "utt1_stopwords_gloss_nbr",
          "utt2_stopwords_gloss_nbr",

          "utt1_final_tokens_gloss",
          "utt2_final_tokens_gloss",

          "utt1_final_tokens_gloss_nbr",
          "utt2_final_tokens_gloss_nbr",

          "lexical_unigrams_nbr_gloss",
          "lexical_bigrams_nbr_gloss",
          "lexical_trigrams_nbr_gloss",
          "syntax_unigrams_nbr_gloss",
          "syntax_bigrams_nbr_gloss",
          "syntax_trigrams_nbr_gloss",
          "syntax_minus_lexic_bigrams_nbr_gloss",
          "syntax_minus_lexic_trigrams_nbr_gloss"]
