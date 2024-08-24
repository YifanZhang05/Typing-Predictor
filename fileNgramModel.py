from ngram import *
from pathlib import Path

# Returns an ordered list of words with bad characters processed (removed) from the text in the file given by file_name.
# clean up the text data base
# same as parse_text but gives file instead of text
def _parse_file(filename : str) -> list:
    myfile = open(filename, "r")
    content = myfile.read()

    output = parse_text(content)

    myfile.close()
    return output


# ngram model with text data stored in file
class FileNgramModel:
    def __init__(self, n: int, allModelFile: str) -> None:
        self.n = n    # the n value
        self.allModeFile = allModelFile    # name of file store all text files used in the model
        self.model = {}    # the ngram model (dictionary)

    # call build_ngram_model for all files in "all_model_files.txt", put the models together
    def build_all_ngram_model(self) -> None:
        # idea: create a temp file/words list that combines everything, then call build_ngram_model on that
        all_model_files = open(self.allModeFile, "r+") # file containing name of all files added in model
        words_lst = []
        for line in all_model_files:
            if (line[-1] == "\n"):
                line = line[:-1]
                words_lst += (_parse_file(line))

        all_model_files.close()
        self.model = build_ngram_model(words_lst, self.n)
        return
    
    # add file to the n-gram model database
    # return bool to indicate success or not (success iff file exist)
    def add_file_to_model(self, text_file: str) -> bool:
        # check if file exists
        if (not Path(text_file).is_file()):
            # print("File not exist: " + text_file)
            return False

        all_model_files = open(self.allModeFile, "r+") # file containing name of all files added in model
        file_lst = []  # list of all model file names; same data as all_model_files but as a list
        for line in all_model_files:
            if (line[-1] == "\n"):
                line = line[:-1]
            file_lst.append(line)

        # check if file already added to model (i.e. text_file in the list of all_model_files)
        for file in file_lst:
            if (file == text_file):    # if found in all_model_files
                # print("File already added to the model")
                return True
            
        # if not found in all_model_files, add it
        # print("File not in model")
        all_model_files.write(text_file+"\n")

        all_model_files.close()
        return True
    
    # remove text_file from "all_model_files.txt"
    def remove_file_from_model(self, text_file: str) -> None:
        all_model_files = open(self.allModeFile, "r+") # file containing name of all files added in model
        file_lst = []  # list of all model file names; same data as all_model_files but as a list
        for line in all_model_files:
            if (line[-1] == "\n"):
                line = line[:-1]
            file_lst.append(line)

        # first clear all_model_files.txt, then write everything to all_model_files.txt except for text_file
        all_model_files.seek(0)
        all_model_files.truncate(0)
        for file in file_lst:
            if (file != text_file): 
                all_model_files.write(file+"\n")
        all_model_files.close()
        return

    def update_model(self) -> None:
        self.build_all_ngram_model()
        return
