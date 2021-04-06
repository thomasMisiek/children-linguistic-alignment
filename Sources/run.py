#!/usr/bin/python

import sys
from generate_database import process_similarities

if len(sys.argv) < 5:
    sys.exit("Not enough arguments")

if sys.argv[2] not in ["English", "French", "Spanish", "German", "Chinese", "Japanese"]:
    sys.exit("Language should be either: English, French, Spanish, German, Chinese, Japanese")

if int(sys.argv[3]) < 10:
    sys.exit("Too low min_age: min:10")
if int(sys.argv[4]) < 11:
    sys.exit("Too low max_age: min:11")

if int(sys.argv[3]) > 79:
    sys.exit("Too high min_age: max:79")
if int(sys.argv[4]) > 80:
    sys.exit("Too high max_age: max:80")

if len(sys.argv) > 5 and (sys.argv[5] != "True" and sys.argv[5] != "False"):
    print("test should be either True or False")

test = sys.argv[5] == "True"
process_similarities(sys.argv[1], sys.argv[2], age_min = int(sys.argv[3]), age_max = int(sys.argv[4]), test = test)
