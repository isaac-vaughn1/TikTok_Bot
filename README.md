# TikTok_Bot 
This Python bot automatically creates TikTok videos of an AI voice reading Reddit stories

## Features
- Reddit Story Retrieval: Automatically retrieves Reddit posts from aspecified subreddit
- AI Voiceover: Converts the text of a Reddit post into speech using TikTok's AI voices
- Video Creation: Automatically generates videos with a voiceover, background video, and subtitles
- Custom Videos: Allows you to choose background video, AI voice, and more

## Installation
1. Clone Repository:
```
git clone https://github.com/isaac-vaughn1/TikTok_Bot.git
cd TikTok_Bot
```
2. Install Required Packages from requirements.txt:
```
pip install -r requirements.txt
```
3. Install ImageMagick:
ImageMagick is required for subtitle overlaying. Install it using the following commands:
- On macOS (with Homebrew):
```
brew install imagemagick
```
- On Windows:

  Download ImageMagick from their [official site](https://imagemagick.org/index.php)
## Setting Up Environmental Variables
To use this bot, you will need to configure several environmental variables. Here are the steps to get each one:
1. **CLIENT_ID** and **CLIENT_SECRET**:
    - These are used to authenticate with Reddit's API via [PRAW](https://praw.readthedocs.io/en/stable/)
    - To obtain them:
      1. Go to [Reddit's app preferences](https://www.reddit.com/prefs/apps)
      2. Scroll down to the "Developed Applications" section and click on "Create App" or "Create Another App".
      3. Fill out the form
         - **Name:** Name your app
         - **App Type:** Select 'script'
         - **Redirect URI:** You can use 'http://localhost:8000'
         - **Description:** Optional
      4. After creating the app, you'll see the **CLIENT_ID** and **CLIENT_SECRET**. The **CLIENT_ID** is the string below "personal use script" and the **CLIENT_SECRET** is shown in the field labeled "secret".
2. **USER_AGENT**:
    - This is required by Reddit to identify your bot.
    - Create a string that describes your bot and includes your Reddit username. For example: `USER_AGENT='TikTok Bot by u/your_reddit_username'`
3. **SESSION_ID**:
    - This is required to access AI voices offered by the [TikTok TTS API](https://github.com/oscie57/tiktok-voice)
      1. Log in to the [TikTok Web App](https://www.tiktok.com/)
      2. Install the [Cookie Editor](https://cookie-editor.com/) extension for your browser
      3. Open the extension and look for `sessionid`
      4. Copy and paste it
4. **MAGICK_PATH**:
    - A common issue during testing was that ImageMagick wasn't recognized in the system's `PATH`. This problem was resolved by specifying the full path to `magick` as a separate environment variable, which should help prevent unecessary troubleshooting
      1. Ensure that the directory containing magick is included in your system’s `PATH` environment variable and find it's location with the following commands:
        - **On Windows:**
          - Open the Command Prompt and run: `where magick`
        - **On macOS:**
          - Open Terminal and run: `which magick`
      2. This command will show the full path to `magick`. Set the **MAGICK_PATH** environment variable to this path. For example:
         ```
         MAGICK_PATH='C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe'
         ```
5. Setting up the `.env` file
   - Create a `.env` file in the root directory of the project and format as follows:
     ```
     CLIENT_ID='your_client_id'
     CLIENT_SECRET='your_client_secret'
     USER_AGENT='TikTok Bot by u/your_reddit_username'
     SESSION_ID='your_tiktok_session_id'
     MAGICK_PATH=your_magick_path
     ```
     
## Usage
After downloading required software and setting up the `.env` file, the bot should be ready to run
1. _Optional_ Customize data found in `Configure.json` to create your very own video
2. Run the program:
```
python main.py
```
Results will be found in the root folder of the project

## Troubleshooting
- Using the most recent version of PyTorch can cause issues when loading the Whisper API (as of 8/13/24). To Fix:
  1. Uninstall torch:
     ```
     pip uninstall torch
     ```
  2. Resinstall a 2.x.x version of torch:
     ```
     pip install torch==2.2.2
     ```
- If you had to install a 2.x.x version of PyTorch, you will also have to downgrade NumPy to a 1.x version:
```
pip install numpy<2
```

## Contributing
Feel free to open issues or submit pull requests to improve this bot.

## License
This project is licensed under the MIT License - see the [LICENSE](License) file for details.
