import re
import os
import glob
import pickle
import settings
import pandas as pd


def create_vocabulary(directory, thresholds):

    """
        Create a CSV file for each threshold in parameters, containing the age
        of acquisition of words found in the CHILDES corpus.
        Specifically, each resulting CSV file links every words that have been uttered more
        than 10 time by childrens in the CHILDES corpus, to an age of acquisition in month.
        This age (A) correspond to the moment where children younger
        than A have prononced a specific word (W) more than the threshold percentage
        out of all occurences of W in the whole CHILDES corpus.

        :param directory: The name of the directory in which all the pre-processed
        csv are stored
        :type directory: str
        :param thresholds: A list of the thresholds percentage after which a word
        is considered to be known by childrens. The percentage correspond to
        the number of time a word has been uttered by younger children in the whole
        CHILDES corpus, divided by the total number of time children (younger and older) have prononced it
        :type : int list

        :return: Nothing, the results are stored in CSV files
        :rtype: None

        .. seealso:: generate_database.create_database()
    """
    # to count number of occurences of words at each age
    occurences_per_age = {}
    # to count number of occurences of words with no consideration for the child age
    total = {}
    # will store all words that are found in the corpus
    words = []
    # will store all ages that are found in the corpus
    ages = []

    extension = 'csv'
    all_filenames = [i for i in glob.glob('../Databases/'+directory+'/modified/*.{}'.format(extension))]

    # each file correspond to a specific age and language of the CHILDES corpus
    for filename in all_filenames:
        print("Currently processing vocabulary using '"+filename+"' file data")
        df = pd.read_csv(filename)

        # each row is an utterance
        for (i, row) in df.iterrows():

            if row.target_child_age not in ages:
                ages.append(row.target_child_age)

            # if the utterance has been prononced by a child
            if row.speaker_code in settings.child_cond:

                tmp = str(row.gloss).split(" ")
                for word in tmp:
                    if word in occurences_per_age:
                        if row.target_child_age in occurences_per_age[word]:
                            occurences_per_age[word][row.target_child_age] += 1
                            total[word] += 1

                        else:
                            occurences_per_age[word][row.target_child_age] = 1
                            total[word] += 1
                    else:
                        occurences_per_age[word] = {}
                        occurences_per_age[word][row.target_child_age] = 1
                        total[word] = 1
                        words.append(word)

    # now that the number of occurence of each words at each age is known,
    # the age at which a word has been prononced more than a threshold, aka
    # age of acquisition, can be processed
    if not os.path.isdir("../Databases/"+directory+"/vocabulary"):
        os.mkdir("../Databases/"+directory+"/vocabulary")
    for threshold in thresholds:
        res = {}
        for word in occurences_per_age:
            sub_total = 0
            total = 0
            for age in sorted(list(occurences_per_age[word].keys())):
                total += occurences_per_age[word][age]

            for age in sorted(list(occurences_per_age[word].keys())):
                sub_total += occurences_per_age[word][age]

                if ((sub_total/total)*100) > threshold and total > 10:
                    # the age of acquisition has been found, stop the search
                    res[word] = age
                    break

        pickle.dump(res, open("../Databases/"+directory+"/vocabulary/"+str(threshold)+".p", "wb" ) )
        res = pd.DataFrame({"word":list(res.keys()), "age_of_acquisition":list(res.values())})
        res.to_csv("../Databases/"+directory+"/vocabulary/"+str(threshold)+'.csv')
