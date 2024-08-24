from gui import *

n = 2    # n value (more info see ngram.py)
displayNum = 3    # number of prediction displayed
all_model_files = "all_model_files.txt"    # file store name of all files that contain text used by model

model = FileNgramModel(n, all_model_files)
tkgui = TkinterGUI(displayNum, model)

# build the ngram model for predicting next words
model.build_all_ngram_model()

# create gui
tkgui.create_gui()
