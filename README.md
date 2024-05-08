# MindSpace Journalling Application


## A fully functional journalling application that utilizes machine learning to determine user emotion/mood to generate Spotify playlists.


Mindspace is a journalling application that uses machine learning models to determine user mood based on journal entries. It utilizes Flask for the backend, integrates with the Spotify API to recommend playlists based on the predicted emotion/sentiment, and employes NLP models for sentiment analysis and emotion prediction. 

The application includes a tab to the home page (the journal), an "About" page as well as a "Visuals/Datasets" page. The "Visuals/Datasets" tab provides the user with links to the datasets, several visuals and additional data about the models I trained for this project. Please feel free to explore the contents of these tabs!

### Prerequisites:
   + Ensure Python is installed on your device. If not, you can download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
      + NOTE: Make sure to add it to or ensure that it is a PATH variable on your system.
   + You are required to have or make a Spotify/ Spotify for Developers account.
      + Create a Spotify Developer Account at https://developer.spotify.com/dashboard/.


### Setup:

#### 1. Clone the repository:
+ Open the Powershell terminal in your IDE
```
git clone https://github.com/Skovixia/Capstone--MindSpace-Journal.git
```

#### 2. Navigate to the project directory via the terminal if not already in it:
```
cd path/to/Capstone--MindSpace-Journal
```
#### 3. Set up Spotify API credentials:

+ After logging in to Spotify for Developers, click on your account in the top right corner and select "Dashboard".
   + If you have issues loading the dashboard or have just created a new account, please ensure you have verified your email. 
   + Refresh the page and try to access the dashboard again.

+ Once you are in your dashboard, select "Create app".
   + What you enter in the fields does not matter, however, a valid URL is required. For that, you may enter "http://localhost:8080/".
        + Example:

        <img src="static\images\spotifyApp.png" alt="Spotify Create App fields" width="800" height="750">


+ Save your app and it should send you back into your dashboard
+ Select "Settings" in the top right corner of the dashboard to view the Client ID and select "view client secret" to see the client secret
+ In the project directory, rename ".env.example" to ".env".

+ Open the .env file in a text editor and replace the placeholder values with your actual Spotify API credentials:
    ```
    CLIENT_ID=your_spotify_client_id 
    CLIENT_SECRET=your_spotify_client_secret
    ```

#### 4. (Optional) Create and activate a virtual environment:

+ Run the following command to check the current execution policy:
        ```
        Get-ExecutionPolicy
        ```
   + If the execution policy is set to "Restricted," you need to change it to allow script execution. Run the following command:
        ```
        Set-ExecutionPolicy RemoteSigned -Scope Process
        ```
   + If the execution policy is "RemoteSigned", continue on.
+ Create the virtual environment:
    ```
    python -m venv venv
    ```
+ Activate the virtual environment:
   ```
    .\venv\Scripts\Activate.ps1
   ```
   + If you encounter a security error, follow the steps mentioned in Step 5 to change the execution policy and try activating the virtual environment again.
#### 5. Install the required dependencies:
   + NOTE: This may take a few minutes
```
pip install -r requirements.txt
```

#### 6. Run flask application to open application window:
```
python app.py
```

#### 7. Enter a journal entry to get predictions and playlists

#### 8. Explore tabs
   + "Visuals/Datasets":
          This will provide the user with visuals from training, along with links to the datasets used.

   + "About":
         This tab will provide a project overview that briefly describes the goals of MindSpace along with information on development.
   + "Journal":
         This tab will bring the user back to the journal entry form for predictions and playlists.

