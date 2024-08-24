from fileNgramModel import *
from tkinter import *

class TkinterGUI:
    def __init__(self, displayNum: int, model: FileNgramModel) -> None:
        self.displayNum = displayNum    # number of predictions displayed
        self.model = model    # the n-gram model

    def create_gui(self) -> None:
        self.root = Tk()    # create the window
        self.create_gui_predict_area()
        self.create_gui_file_upload_frame()
        self.root.mainloop()

    # create text field for entering text, label widget that display prediction, and button to generate prediction
    def create_gui_predict_area(self) -> None:
        # function used to generate & display predicted next words using the ngram model build previously
        # called when generateButton is clicked
        def generateButtonCommand():
            textEntered = textField.get("1.0", "end-1c")
            endTuple = last_n_token(textEntered, self.model.n) # last n tokens of textEntered as a tuple
            predictWordsList = next_predict_words(self.model.model, endTuple) # list containing 2 elements: list of next predictions and list of their probability
            
            # convert predictWordsList to a string that can be displayed
            wordsListStr = ""
            if (predictWordsList == []): # if no predict found in model
                wordsListStr = "no prediction found in model"
            else: # if predict found in model, convert predictWordList into str
                for i in range(min(len(predictWordsList[0]), self.displayNum)):
                    word = predictWordsList[0][i]
                    freq = predictWordsList[1][i]
                    wordsListStr += "[" + word + ": " + "{:.2f}".format(freq) + "]"

            nextTokenLabel.config(text=wordsListStr)
            return
        
        # create text field
        textField = Text(self.root, width=50)
        textField.grid(row=0, column=0, rowspan=3)

        # text label widget for displaying predicted next words
        nextTokenLabel = Label(self.root, text="no prediction found in model")
        nextTokenLabel.grid(row=3, column=0)

        # create generate button
        generateButton = Button(self.root, text="generate next", command=generateButtonCommand)
        generateButton.grid(row=4, column=0)

    # create file upload frame that contains the following:
    def create_gui_file_upload_frame(self) -> None:
        def addFileButtonCommand():
            file = fileNameText.get("1.0", "end-1c")
            fileAdded = self.model.add_file_to_model(file)
            self.model.update_model()
            if (fileAdded):
                uploadedFileLabel.config(text="added file "+file)
            else:
                uploadedFileLabel.config(text="model updated")
            return

        fileUploadFrame = Frame(self.root)
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
        addFileButton = Button(fileUploadFrame, text="update model", command=addFileButtonCommand)
        addFileButton.grid(row=2, column=1)

        # message to tell if successful uploaded
        uploadMessageLabel = Label(fileUploadFrame)
        uploadMessageLabel.grid(row=3, column=1)
