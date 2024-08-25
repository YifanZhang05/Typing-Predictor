**About word predictor**

Based on the last n entered words, use the text in file.txt to predict the next word. 
Can modify n value (initially 2) and number of predictions displayed (initially 3)

How to use:
  - Put sample text file in file.txt. Word prediction will be based on text in this file
  - Run main.py. You will see a GUI with a textbox and a button that says "generate text"
  - Enter some words and click "generate text". You will see a list of predicted next word and the possibility for each of them.

How to update text database
  - the program makes predictions based on given files containing text. 
  - The list of those files is stored in "all_model_files.txt"
  - to add new text used by the model, put the name of file containing text in the textbox "enter file name", then click "update model"
  - to update the model after editing an added text file, just click "update model"
