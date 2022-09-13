import os

def deleteFile(fileName):
    folderPath = os.path.abspath('notes')  
    files = os.listdir(folderPath)

    path = os.path.join(folderPath, fileName)

    if fileName in files:
        os.remove(path)