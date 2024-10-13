# shortfarm

Full automation of Youtube Shorts creation, without needing OpenAI API keys. `Version 0.9`

In BETA! Until AI graphics and background music is added, using this may not be the best idea for your channel. 

This has been tested on latest, and I have a channel using this that has videos automatically posted to it every 5 hours. A public demo channel may also go up.

This is not recommended for total beginners since it requires a little bit of work and modification in the code in some cases. You don't need to know Python though, if you know a similar language (or use common sense/ChatGPT) you should be good.

## Installation

### Prerequisites
Run this to install all requirements:

`pip install -r requirements.txt`

Ensure `ffmpeg` and `ImageMagick` are installed on your device. This is necessary.

Then get YouTube credentials and put them in client_secrets.json. See `https://developers.google.com/youtube/v3/guides/uploading_a_video` for more info, or find details in step 3.

### Installing
1. Clone the repository locally.
3. You may have to start a venv before install requirements (make the venv directory `venv`). After that, `exit` the venv. Use `bash start.sh` after the first venv setup + dependencies install. 
6. Signup/Go to Google Developers, create an API key for Youtube Data API v3 (search it up if you don't know how), then create OAuth keys, and make sure your account is one of the testers. You will get a client secret and client ID. use them, replace the values in example.client_secrets.json and remove `example.` from the start of the filename.
4. Enter the venv for now, and run `python upload_video.py`, you will be greeted with an authentication thing. Follow the instructions, authenticate youself and credentials will be created for you.
5. Add three gameplay videos in `gameplay` (named `gameplay_1.mp4` 2 and 3, change the line `gp = random.choice(["1", "2", "3"])` if you want to change the amount of gameplay videos). I recommend Minecraft and Cluster Trucks, you can use https://cobalt.tools/ to download videos. If you are lazy, you can download and add [these videos](https://drive.google.com/drive/folders/1qToyKgKDLOPgoMj_EMhA6qusV4xCr4Sb?usp=sharing) then change how many videos there are from 3 to 2.
7. Run `bash start.sh`

## Usage

To use this script:
1. Literally just run it and wait, the script will create a video from absolute scratch using AI

To change fonts, change the ttf file in fonts/font.ttf

To change actual captioning when written to the video, see `# [JUMPHERE] to create subtitles with black highlight` in `shorts.py`


## Credits

- Binary-Bytes: baseplate. 
- @doxr: integrations, free AI, captioning, etc

Script does not generate any graphics like images. Planned for later.

AI services used for free:
- g4f: script generation, title/description/keywords, etc
- DeepInfra: free OpenAI whisper API for subtitles

Feel free to fork this as a baseplate to create other types of videos. I may create a Reddit version where instead of creating a topic with AI, the Reddit read API for video topics (ex. `r/AmItheAsshole`)