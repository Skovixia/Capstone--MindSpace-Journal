# -*- coding: utf-8 -*-
import numpy as np
import nltk
import zipfile
import os
import string
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

#dictionary for mapping class to emotion in text
labelToEmotion = {4: 'Sadness', 2: 'Joy', 0: 'Anger', 3: 'Love', 1: 'Fear', 5: 'Surprise'}

#setting absolute path to the directory with script
scriptDir = os.path.dirname(__file__)
# Go back one directory
parentDir = os.path.dirname(scriptDir)

#path to the zip file
zipFile = os.path.join(parentDir, 'data', 'glove50d.zip')


#extracting file directly into the 'data' directory
with zipfile.ZipFile(zipFile, 'r') as zip_ref:
    zip_ref.extractall('data')
    print("File extracted successfully.")

unZipped = os.path.join(parentDir, 'data', 'glove.6B.50d.txt')

#getting glove embeddings from the glove file 
words = dict()
def addToDict(d, filename):
  with open(filename, 'r', encoding='utf-8') as f:
    for line in f.readlines():
      line = line.split(' ')
      try:
        d[line[0]] = np.array(line[1:], dtype = float)
      except:
        continue

addToDict(words, unZipped)


tokenizer = nltk.RegexpTokenizer(r"\w+")

lemmatizer = WordNetLemmatizer()

#tokenizing and some cleaning (preprocessing)
def messageToTokenList(s):
  tokens = tokenizer.tokenize(s)
  tokens = [word for word in tokens if word not in string.punctuation]
  lowercaseTokens = [t.lower() for t in tokens]
  lemmatizedTokens = [lemmatizer.lemmatize(t) for t in lowercaseTokens]
  usefulTokens = [t for t in lemmatizedTokens if t in words]
  return usefulTokens

def messageToWordVec(message, wordDict = words):
  processedTokensList = messageToTokenList(message)
  vectors = []
  for token in processedTokensList:
    if token not in wordDict:
      continue
    tokenVector = wordDict[token]
    vectors.append(tokenVector)
  return np.array(vectors, dtype=float)

def padX(X, desiredSeqLen=50):
    padded_X = np.zeros((len(X), desiredSeqLen, 50))
    for i, x in enumerate(X):
        xSeqLen = x.shape[0]
        if xSeqLen > desiredSeqLen:
            padded_X[i] = x[:desiredSeqLen]
        else:
            padded_X[i, :xSeqLen] = x
    return padded_X.astype(float)

#function for emotional prediction for lstm model
def LSTMpredictEmotions(model, sampleTexts, wordDict):
    #preprocess each sentence
    preprocessedSamples = [messageToWordVec(text, wordDict) for text in sampleTexts]

    #padding sequences to a fixed length
    paddedSamples = padX(preprocessedSamples)
   
    try:
      predictions = model.predict(paddedSamples)
      print(predictions)
    except UnicodeEncodeError as e:
      print("UnicodeEncodeError:", e)
    
    return predictions
