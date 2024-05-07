# the n-gram model: predict the next word in a text based on the previous n words

from utilities import *

# Returns an ordered list of words with bad characters processed (removed) from the text in the file given by file_name.
# clean up the text data base
def parse_file(filename : str) -> list:
    myfile = open(filename, "r")
    content = myfile.read()
    output = []
    word = ""

    for i in content:
        #print(i)
        if (i in BAD_CHARS):    #bad character: ignore
            continue

        elif ((i == " ") or (i == "\n") or (i == "\t")):    #space/enter/tab: end of a word
            if (word != ""):
                output.append(word)
            word = ""
            continue

        else:    #letter or valid punctuation: what we want to be in the list
            #print(i)
            if (i not in VALID_PUNCTUATION):    #letter
                word += i
            else:    #punctuation
                if (word != ""):
                    output.append(word)
                output.append(i)
                word = ""
            continue
        
    # word at the end of file
    if (word != ""):
        output.append(word)

    for j in range(len(output)):
        if (output[j].upper() not in ALWAYS_CAPITALIZE):
            output[j] = output[j].lower()
        else:
            output[j] = output[j].upper()

    myfile.close()
    return output

# same as parse_file, but gives the text in str directly (instead of giving a file)
def parse_text(text : str) -> list:
    output = []
    word = ""

    for i in text:
        #print(i)
        if (i in BAD_CHARS):    #bad character: ignore
            continue

        elif ((i == " ") or (i == "\n") or (i == "\t")):    #space/enter/tab: end of a word
            if (word != ""):
                output.append(word)
            word = ""
            continue

        else:    #letter or valid punctuation: what we want to be in the list
            #print(i)
            if (i not in VALID_PUNCTUATION):    #letter
                word += i
            else:    #punctuation
                if (word != ""):
                    output.append(word)
                output.append(i)
                word = ""
            continue
        
    # word at the end of file
    if (word != ""):
        output.append(word)

    for j in range(len(output)):
        if (output[j].upper() not in ALWAYS_CAPITALIZE):
            output[j] = output[j].lower()
        else:
            output[j] = output[j].upper()

    return output

# Build the raw ngram model: returns n-grams dictionary and counts of the words that follow the n-gram:
#  - key: N-gram in a tuple. 
#  - value: will be a list containing two lists:
#    First list contains the words, second list contains counts of the corresponding word.
def build_ngram_counts(words, n):
    ngram_dict = {}
    for i in range(len(words)-n): # loop through all words that could be start of n-gram
        key_tuple = tuple(words[i:i+n])
        word = words[i+n]
        if (key_tuple not in ngram_dict): # tuple is new, create a new key-value pair in dictionary
            ngram_dict[key_tuple] = [[word], [1]]
        else: # if tuple appeared before
            if (word in ngram_dict[key_tuple][0]):
                ngram_dict[key_tuple][1][ngram_dict[key_tuple][0].index(word)] += 1
            else:
                ngram_dict[key_tuple][0].append(word)
                ngram_dict[key_tuple][1].append(1)
    return ngram_dict

# return n-gram dictionary. counts: dict, prune_len: int
# for each n-gram, only keep the first prune_len most frequent following words
# when there's a tie, keep all words in the tie
def prune_ngram_counts(counts, prune_len):
    new_dict = {}
    for key, value in counts.items():
        value_converted = convert_counts_format(value) # convert format of value into list of s[word, frequency] pairs
        value_converted.sort(key=lambda pair: pair[1], reverse=True) # sort the list of [word, frequency] pairs based on frequency of words
        words = []
        frequency = []
        if (len(value[0]) > prune_len): # if the n-gram has more than prune_len following words
            for i in range(prune_len):
                element = value_converted[i]
                words.append(element[0])
                frequency.append(element[1])
            min_freq = frequency[-1] # minimum of frequency kept
            next_index = prune_len
            #print(key, value_converted, min_freq)
            while(next_index<len(value[0]) and value_converted[next_index][1]==min_freq): # loop as long as there's the tie
                words.append(value_converted[next_index][0])
                frequency.append(value_converted[next_index][1])
                next_index += 1
            new_dict[key] = [words, frequency]
        else: # otherwise, only sort by most frequent to least frequent
            #new_dict[key] = value
            for i in range(len(value[0])):
                element = value_converted[i]
                words.append(element[0])
                frequency.append(element[1])
            new_dict[key] = [words, frequency]
    return new_dict
# helper function for prune_ngram_counts()
# convert [[a, b, c, d], [1, 2, 3, 4]] to [[a, 1], [b, 2], [c, 3], [d, 4]]
# doesn't change counts (the list passed into the function)
def convert_counts_format(counts):
    new_counts = []
    for i in range(len(counts[0])):
        new_counts.append([counts[0][i], counts[1][i]])
    return new_counts

# convert a list of counts to a list of probabilities
# [1, 2, 3, 4, 4, 6] -> [0.05, 0.1, 0.15, 0.2, 0.2, 0.3]. A total of 20, 1->1/20, 2->2/20, ...
def get_prob_from_count(counts):
    total = sum(counts)
    probList = []
    for i in counts:
        probList.append(i/total)
    return probList

# in the ngram dictionary, change value's 2nd list from count of each word to frequency of each word
def probify_ngram_counts(counts):
    output = counts
    for key, value in output.items():
        value[1] = get_prob_from_count(value[1])
    return output

# build the n-gram model from list of words after parse_file. 
# for each n-gram, only keep the top k most likely words
def build_ngram_model(words, n, k):
    ngram = build_ngram_counts(words, n)
    model = prune_ngram_counts(ngram, k)
    model_probify = probify_ngram_counts(model)
    return model_probify

# write given n-gram model to file, return name of the file
# file named as this:
# - raw n-gram model: raw_n_model.txt
# - not raw n-gram model: n_model.txt
# line1: n-gram; line2: list of next words; line3: list of freq/prob
# raw=True: write raw model: list in value contains frequency of all words
# raw=False: regular model: list contains limited number of probabilities
def write_model(model: dict, n: int, raw: bool) -> str:
    if (raw):
        file = open("raw_"+str(n)+"_model.txt", "w") # create the file
    else:
        file = open(str(n)+"_model.txt", "w") # create the file
    for key, value in model.items():
        for i in range(n):
            file.write(key[i])
            file.write(" ")
        file.write("\n")
        for i in range(len(value[0])): # write list of next words
            file.write(value[0][i])
            file.write(" ")
        file.write("\n")
        for i in range(len(value[0])): # write list of freq/prob
            file.write(str(value[1][i]))
            file.write(" ")
        file.write("\n")
    file.close()
    return file.name

# read n-gram model from file, return the model
# raw=True: the model on file contains freq of all possible words instead of probability of some most likely words
def read_model(filename: str, raw: bool) -> dict:
    file = open(filename, "r")
    model = {}
    count = 0 # 0: reading n-gram; 1: reading next words; 2: reading freq/probabilities
    ngram = tuple
    for line in file: # read file line by line
        #print(line)
        if (count == 0):
            # read n-gram
            ngram = tuple(line.split())
            count += 1
        elif (count == 1):
            # read words
            model[ngram] = []
            model[ngram].append(line.split())
            count += 1
        elif (count == 2):
            # read freq (raw) or probabilities (not raw)
            if (raw): 
                model[ngram].append([int(x) for x in line.split()])
            else:
                model[ngram].append([float(x) for x in line.split()])
            count = 0
    file.close()
    return model

# update both the raw model and model file based on a given text file
# only update if the file with the given name hasn't been added to the model
def update_model(raw_model_file: str, model_file: str, text_file: str) -> dict:
    all_model_files = open("all_model_files.txt", "r+") # file containing name of all files added in model
    file_lst = []  # list of all model file names; same data as all_model_files but as a list
    for line in all_model_files:
        if (line[-1] == "\n"):
            line = line[:-1]
        file_lst.append(line)

    # check if file already added to model (i.e. text_file in the list of all_model_files)
    for file in file_lst:
        if (file == text_file):
            print("File already added to the model")
            return

    # read given raw model file as dict (call it raw_model), get n value from file name

    # convert given text file into raw ngram model, call it text_file_raw_model

    # loop through text_file_raw_model and add data to raw_model

    # prune and probify the updated raw_model. This will be updated model

    # write updated raw_model and model to raw_model_file and model_file

    all_model_files.close()
    return

# given the ngram model (dict) and a ngram (tuple). Return a list predict_words:
# - predict_words[0]: a list of predicted words after the given ngram according to the model. Ordered most likely to least likely
# - predict_words[1]: a list of probabilities of the corresponding word
def next_predict_words(model: dict, ngram: tuple):
    if (ngram in model): # if ngram is in model: return the required list
        return model[ngram]
    else: # if ngram not in model: return empty list
        return []
    
# given a string, parse it into a list using parse_text. Return the last n elements/tokens of parsed list
def last_n_token(text: str, n: int) -> tuple:
    parsed = parse_text(text) # text parsed into list
    list_lastn = parsed[-n:]
    return tuple(list_lastn)