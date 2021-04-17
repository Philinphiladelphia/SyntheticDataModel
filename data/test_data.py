from PIL import Image
import os
import numpy as np
import json

def getTestData():
    imageFiles = os.listdir("./data/images")
    jsonData = json.load(open("data/test_data.json", "r"))

    imageArray = []
    jsonArray = []

    for f in imageFiles:
        img = Image.open("./data/images/" + f)
        imageArray.append(np.array(img))
        jsonArray.append(jsonData)

    return np.array(imageArray), np.array(jsonArray)