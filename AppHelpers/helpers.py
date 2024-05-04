from keras.models import load_model
from joblib import load
from AppHelpers.lstmHelpers import parentDir
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import os

#relative path of models
mp = os.path.join(parentDir, 'models', 'GloVeLSTMmodel.h5')
LSTMmodel = load_model(mp)
nbModel = load(os.path.join(parentDir, 'models', 'nbModel.pkl'))
cv, lrModel = load(os.path.join(parentDir, 'models', 'lrModel.pkl'))

#loading pretrained roberta model for sentiment analysis
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

###Functions
#gets polarity score from roberta model
def polarityScoresRoberta(example):
    encodedText = tokenizer(example, return_tensors='pt')
    output= model(**encodedText)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores

    scoresDict={
        'Negative' : float(scores[0]),
        'Neutral' : float(scores[1]),
        'Positive' : float(scores[2])
    }
    #determines sentiment with highest polarity score
    sentiments = ['Negative', 'Neutral', 'Positive']
    dominantSentiment = sentiments[np.argmax(scores)]
    return dominantSentiment, scoresDict


#prediction probabilities for lr and nb models
def getPredictionProba(model, entry):
    transformedDocx = cv.transform([entry])
    results = model.predict_proba(transformedDocx.reshape(1, -1))
    return results

#prediction for lr and nb models
def predictEmotions(model, entry):
    transformedDocx = cv.transform([entry])
    results = model.predict(transformedDocx.reshape(1,-1))  # Make predictions
    return results[0]


# Define the function to determine the final predicted emotion
def determineFinalEmotion(dominantSentiment, topTwoEmotions, combinedProbTopTwo):
    if dominantSentiment == 'Positive':
        possibleEmotions = ['Joy', 'Love', 'Surprise']
    elif dominantSentiment == 'Negative':
        possibleEmotions = ['Anger', 'Sadness', 'Fear','Surprise']
    else:
        return 'Neutral'
    
    sameSentimentEmotions = [emotion for emotion in possibleEmotions if emotion in topTwoEmotions]
    if len(sameSentimentEmotions) > 0:
        return max(sameSentimentEmotions, key=lambda x: combinedProbTopTwo[topTwoEmotions.index(x)])
    
    # If none of the possible emotions are in topTwoEmotions, choose the one with the highest combined probability
    maxProbIdx = np.argmax(combinedProbTopTwo)
    return topTwoEmotions[maxProbIdx]
