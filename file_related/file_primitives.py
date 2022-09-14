import os
import json

STRUCT_FILE_NAME = 'tree_structure.json'


def deleteFile(fileName):
    folderPath = os.path.abspath('notes')  
    files = os.listdir(folderPath)

    path = os.path.join(folderPath, fileName)

    if fileName in files:
        os.remove(path)

def hasStructureFile(file = STRUCT_FILE_NAME):
    folderPath = os.path.abspath('notes')  
    files = os.listdir(folderPath)

    if file in files:
        return True
    
    return False

def getStructure(file = STRUCT_FILE_NAME) -> dict:
    folderPath = os.path.abspath('notes')  
    path = os.path.join(folderPath, file)

    with open(path, 'r') as fp:
        data = json.load(fp)
    
    return data


def saveStructure(s, file = STRUCT_FILE_NAME):
    folderPath = os.path.abspath('notes')
    path = os.path.join(folderPath, file)

    with open(path, 'w') as fp:
        json.dump(s, fp)

def deleteNodeFromStructure(id):
    s = getStructure()
    try:
        s.pop(id)
    except:
        print('There is no node to be deleted')    
    
    saveStructure(s)