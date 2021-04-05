#! /usr/bin/env RScript
library(childesr)

args = commandArgs(trailingOnly=TRUE)
lang = args[1]
age = strtoi(args[2], 10)
dir = args[3]


utterances  = get_utterances(age = age,language = lang)
f <- file(paste0(dir,age,".csv"), "wb")
write.csv(x = utterances[c(2,3,6,8,9,10,11,12,13,15,17,18,24,25,26,27)], file = f, eol="\n", fileEncoding = 'utf-8')
