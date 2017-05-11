"""
script to create a new text document and save it and name
"""

import os

def Make_new_doc():
    "asks for the filename input and creates the file"
    FolderPath = r"C:\Notes"
    new_doc_name = raw_input('Enter document name>>')+".txt"
    FilePath = os.path.join(FolderPath,new_doc_name)
    if os.path.isdir(FolderPath):
        pass
    else:
        os.mkdir(FolderPath)

    if os.path.isfile(FilePath):
        pass
    else:
        open(FilePath,'a')
        if os.path.exists(FilePath):
            print "File created"
        else:
            print "File not created"
    try:
        os.system('start notepad++ ' + FilePath)
    except:
        os.system(FilePath)


Make_new_doc()
