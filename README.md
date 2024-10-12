# shortfarm

Full automation of Youtube Shorts creation, without needing OpenAI API keys.

In BETA! Until subtitles, graphics, and automatic background music is added, using this may not be the best idea for your channel.

## Installation

### Prerequisites
Run this to install all requirements:

`pip install -r requirements.txt`

Then get a YouTube API key.

### Installing
1. Clone the repository locally.
3. You may have to start a venv before install requirements.
4. Add your API key for youtube to .env
5. Add two gameplay videos in `gameplay` (named `gameplay_1.mp4` and 2). I recommend Minecraft and Cluster Trucks, you can use https://cobalt.tools/ to download videos. If you are lazy, you can download and add [these videos](https://drive.google.com/drive/folders/1qToyKgKDLOPgoMj_EMhA6qusV4xCr4Sb?usp=sharing).
7. Run `shorts.py`

## Usage

To use this script:
1. Literally just run it and wait, you will start seeing youtube videos being uploaded (and upon running the script a video is created, after that every 1 hour a new video is created and sent to big brother Google).

To get API keys:

TODO

## Credits

Binary-Bytes created the baseplate. I added Youtube integration, automation, etc.

Script does not generate any graphics like images. Subtitles will be added soon.