document.addEventListener('DOMContentLoaded', function() {
    console.log(labelToEmotion);
    //updates the character count for character limit
    const charCount = document.getElementById('char-count');

    document.getElementById('journal-entry').addEventListener('input' , function() {
        const count = this.value.length;
        charCount.textContent = count + '/500';

        if (count >=500){
            this.classList.add('limit-reached');
        } else {
            this.classList
        }
    });

    document.getElementById('journal-form').addEventListener('submit', function(event) {
        event.preventDefault();
        let journalEntry = document.getElementById('journal-entry').value;
        fetch('/predict-emotion', {
            method: 'POST',
            body: new URLSearchParams({
                'journal_entry': journalEntry
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            //displays predicted emotions and probabilities
            let emotionsDiv = document.getElementById('emotions');
            emotionsDiv.innerHTML = '<h2 class="sub-title">✨Overall Predicted Emotion ✨</h2>';
            if (data.predicted_emotion && data.probabilities) {
                let predictedEmotion = data.predicted_emotion;
                let sentimentDict = data.sentiment_dict;

                let emoticons = {
                    'Positive': '☀️', //positive sentiment
                    'Negative': '☁️', //negative sentiment
                    'Neutral': '🌱', //neutral sentiment
                };

                emotionsDiv.innerHTML += `<p class="predicted-emotion"><strong>${predictedEmotion}</strong> ${getEmoticon(predictedEmotion)}</p>`;

                //displaying sentiment dictionary with emojis
                let sentimentText = ''
                for (const [sentiment, score] of Object.entries(sentimentDict)) {
                    sentimentText += `${emoticons[sentiment]} ${sentiment}: ${(score * 100).toFixed(2)}% `;
                }
                sentimentText += '</p>';
                emotionsDiv.innerHTML += sentimentText;

                //displays emotion percentages
              let probabilitiesDiv = document.getElementById('emotion-probabilities');
              probabilitiesDiv.innerHTML = '<p><strong>Emotion Probabilities:</strong></p>';
              let totalProbability = data.probabilities[0].reduce((acc, cur) => acc + cur, 0);
              data.probabilities[0].forEach((probability, index) => {
                  let emotion = labelToEmotion[index];
                  let percentage = ((probability / totalProbability) * 100).toFixed(2);
                  probabilitiesDiv.innerHTML += `<p>${getEmoticon(emotion)} ${emotion}: ${percentage}%</p>`;
              });
                
            } else {
                emotionsDiv.innerHTML += '<p class="predicted-emotion">No predicted emotions or probabilities available.</p>';
            }

            //displaying Spotify playlists
            let playlistsDiv = document.getElementById('playlist-container');
            playlistsDiv.innerHTML = ''; // Clear previous playlists
            if (Array.isArray(data.playlists)) {
                data.playlists.forEach(item => {
                    playlistsDiv.innerHTML += `
                        <div class="playlist">
                            <a href="${item.url}" target="_blank">
                                <img src="${item.image}" alt="${item.name}" class="playlist-image">
                                <p class="playlist-name">${item.name}</p>
                            </a>
                        </div>`;
                });
            } else {
                playlistsDiv.innerHTML += '<p>No playlists available.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    //function to get emoji for an emotion
    function getEmoticon(emotion) {
        switch(emotion) {
            case 'Anger':
                return '🔴';
            case 'Fear':
                return '🟡';
            case 'Joy':
                return '🟢';
            case 'Love':
                return '💖';
            case 'Sadness':
                return '🔵';
            case 'Surprise':
                return '🟠';
            case 'Neutral':
                return '⚪';
            default:
                return '';
        }
    }

});
