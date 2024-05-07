from tkinter import *
#from ngram import build_ngram_counts
from ngram import *

# n and k values (more info see ngram.py)
n = 2
k = 3
# name of model file
model = "model.txt"

# create the window
root = Tk()

# create text field
textField = Text(root, width=50)
textField.grid(row=0, column=0, rowspan=3)

# text label widget for displaying predicted next words
nextTokenLabel = Label(root, text="no prediction found in model")
nextTokenLabel.grid(row=3, column=0)

# build the ngram model for predicting next words
words2 = ["the", "child", "will", "the", "child", "can", "the",
							"child", "will", "the", "child", "may", "go", "home", "."]
#model = build_ngram_model(words2, n, k)
model = build_ngram_model(parse_file("file.txt"), n, k)

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

# create generate button
generateButton = Button(root, text="generate next", command=generateNextToken)
generateButton.grid(row=4, column=0)



root.mainloop()