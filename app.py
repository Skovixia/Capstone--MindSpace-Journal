# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, url_for, g
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv
import webview
from AppHelpers.lstmHelpers import LSTMpredictEmotions, labelToEmotion, words
from AppHelpers.helpers import *
load_dotenv()
#initializing Spotipy client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET")))

app = Flask(__name__, static_folder='static')


def inject_urls():
    return {
        'indexUrl': url_for('index'),
        'visualsUrl': url_for('visuals'),
        'aboutUrl': url_for('about')
    }

@app.before_request
def before_request():
    g.urls = inject_urls()
    # print(g.urls)

@app.route('/')
def index():
    return render_template('index.html', label_to_emotion=labelToEmotion, urls= g.urls)

@app.route('/visuals')
def visuals():
    return render_template('visuals.html',urls= g.urls)

@app.route('/about')
def about():
    return render_template('about.html',urls= g.urls)


@app.route('/predict-emotion', methods=['POST'])
def predict_emotion():

    #receives journal entry from the frontend
    journalEntry = request.form['journal_entry']

    nbProbabilities = getPredictionProba(nbModel, journalEntry)
    lrProbabilities = getPredictionProba(lrModel, journalEntry)

    #calling lstm model to predict emotion and calls probabilites of all emotions
    LSTMprobabilities = LSTMpredictEmotions(LSTMmodel, [journalEntry], words)

    # Combine probabilities for better predictions
    combinedProbs = (nbProbabilities + lrProbabilities + LSTMprobabilities) / 3

    #gets the indices of the top two emotions with the highest probabilities
    topTwoIndices = np.argsort(combinedProbs[0])[-2:]

    #gets the corresponding emotions
    topTwoEmotions = [labelToEmotion[idx] for idx in topTwoIndices]

    #calculates the combined probability for the top two emotions
    combinedProbTopTwo = combinedProbs[0][topTwoIndices]

    #getting the highest polarity score from roberta model 
    dominantSentimentRes, scores = polarityScoresRoberta(journalEntry)

    #determining the final predicted emotion based on user sentiment from the top 2 predicted emotions
    finalPredictionSent = determineFinalEmotion(dominantSentimentRes, topTwoEmotions, combinedProbTopTwo)

    playlists = fetchPlaylists(finalPredictionSent, dominantSentimentRes)

    #exctracting info from spotify API
    formatted_playlists = [{
        'name': item['name'],
        'url': item['external_urls']['spotify'],
        'image': item['images'][0]['url'] if item['images'] else os.path.join(scriptDir, 'images', 'placeholder.jpg'),  # Default placeholder image
    } for item in playlists['playlists']['items']]

    #return data
    response_data = {
        'predicted_emotion': finalPredictionSent, 
        #converting numpy array to list for JSON serialization
        'probabilities': combinedProbs.tolist(),
        'playlists': formatted_playlists,
        'sentiment_dict' : scores
    }

                # print statements for model predictions and analysis
#******************************************************************************************************************************************
    # print("NBProbabilities: ", nbProbabilities, "nbModel.classes_:", nbModel.classes_)
    # print("NBProb: ",np.argmax(nbProbabilities),": ", predictEmotions(nbModel, journalEntry))
    # print("LrProb: ",np.argmax(lrProbabilities),": ", predictEmotions(lrModel, journalEntry))
    # print("LrProbabilities: ", lrProbabilities)
    # print("LSTMProb: ", labelToEmotion[np.argmax(LSTMprobabilities)])
    #     #dominant index
    # dominantEmotionalIdx = np.argmax(combinedProbs)
    # print("dominantEmo: ", labelToEmotion[dominantEmotionalIdx])

    # print("Combined probs: ", combinedProbs)
    # finalPredictions = '/'.join(topTwoEmotions)

    # print("Final Prediction (Top Two Emotions):", finalPredictions)
    # print("Combined Probability (Top Two Emotions):", combinedProbTopTwo)
    # print("Dominant Sentiment: ",dominantSentimentRes)
    # print("Polarity Scores: ", scores)
    # print("final prediction based on Roberta sentiment: ", finalPredictionSent)
#******************************************************************************************************************************************

    return jsonify(response_data)
    

def fetchPlaylists(emotion, sentiment):
    #fetches playlists based on the predicted emotion
    playlists = sp.search(q=f'{emotion} {sentiment} hits', type='playlist')
    return playlists

if __name__ == '__main__':
    #app.run(debug=True)
    window = webview.create_window("Emotion Predictor", app)
    #starting the web view application
    webview.start()
    #app.run(host='0.0.0.0', port=5000)