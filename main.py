from tkinter import *
#from ngram import build_ngram_counts
from ngram import *

# n and k values (more info see ngram.py)
n = 2
k = 3

# create the window
root = Tk()

# create text field
textField = Text(root, width=50)
textField.grid(row=0, column=0, rowspan=3)

# text label widget for displaying predicted next words
nextTokenLabel = Label(root, text="no prediction found in model")
nextTokenLabel.grid(row=3, column=0)

# build the ngram model for predicting next words
model = build_all_ngram_model(n)

# function used to generate & display predicted next words using the ngram model build previously
# called when generateButton is clicked
def generateNextToken():
    textEntered = textField.get("1.0", "end-1c")
    endTuple = last_n_token(textEntered, n) # last n tokens of textEntered as a tuple
    predictWordsList = next_predict_words(model, endTuple) # list containing 2 elements: list of next predictions and list of their probability
    
    # convert predictWordsList to a string that can be displayed
    wordsListStr = ""
    if (predictWordsList == []): # if no predict found in model
        wordsListStr = "no prediction found in model"
    else: # if predict found in model, convert predictWordList into str
        for i in range(len(predictWordsList[0])):
            word = predictWordsList[0][i]
            freq = predictWordsList[1][i]
            wordsListStr += "[" + word + ": " + "{:.2f}".format(freq) + "]"

    nextTokenLabel.config(text=wordsListStr)
    return

def update_model(n: int):
    global model 
    model = build_all_ngram_model(n)
    return

# if file not added, then add it to all_model_files.txt. Then call update_model
# return bool indicate if file successfully added
def update_model_with_file(file: str) -> bool:
    fileAdded = add_file_to_model(file)
    update_model(n)
    return fileAdded

def addFileButtonCommand():
    file = fileNameText.get("1.0", "end-1c")
    fileAdded = update_model_with_file(file)
    if (fileAdded):
        uploadedFileLabel.config(text="added file "+file)
    else:
        uploadedFileLabel.config(text="updated model")
    return

# create generate button
generateButton = Button(root, text="generate next", command=generateNextToken)
generateButton.grid(row=4, column=0)

## Input box for uploading file to the word predicting model
# frame that deals with uploading files START --------------------------------------------------------
fileUploadFrame = Frame(root)
fileUploadFrame.grid(row=0, column=1)

# text for entering name of file to be uploaded, with label explaining that
enterFileLabel = Label(fileUploadFrame, text="Enter file name")
enterFileLabel.grid(row=0, column=1)
fileNameText = Text(fileUploadFrame, height=2, width=25)
fileNameText.grid(row=1, column=1)

# label that display the last file uploaded
uploadedFileLabel = Label(fileUploadFrame, text="")
uploadedFileLabel.grid(row=4, column=1)

# button for upload text file for data in the n-gram model
addFileButton = Button(fileUploadFrame, text="upload model", command=addFileButtonCommand)
addFileButton.grid(row=2, column=1)

# message to tell if successful uploaded
uploadMessageLabel = Label(fileUploadFrame)
uploadMessageLabel.grid(row=3, column=1)
# frame that deals with uploading files END ----------------------------------------------------------


root.mainloop()