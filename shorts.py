# Import everything
from dotenv import load_dotenv
import random
import os
from g4f.client import Client
from g4f.Provider import DDG
from random_word import RandomWords
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
load_dotenv()
r = RandomWords()
client = Client(provider=DDG)

# Ask for video info
title = "example"
option = "yes"

if option == 'yes':
    # Generate theme using g4f
    theme_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Give a very very short phrase of an interesting topic. The theme should be interesting but not complicated or deep. {r.get_random_word()}"}],
    )
    theme = theme_response.choices[0].message.content
    print(f"\nGenerated theme: {theme}")

    # Generate content using g4f
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Act as an script writer who writes engaging and professional scripts for tiktok shorts. you never do a grammatical mistake and write very engaging scripts that touches the viewers' attention. At the beginning of the video you never forget to add a viral hook that will catch the viewers attention and will break the scroll. Your scripts are so loved by users that they subscribe and follow the channel. Don't mention any channel's name but at appropriate point tell the viewer to like the video and follow or subscribe the channel or account. (Remember tiktok shorts have max limit of 1 min). Do not use ANY markdown or indicators; you're only making the speaking part of the script and the user will handle all other elements. Everything you generate should be English. Now Generate content on - \"{theme}\""}],
    )
    generated_content = chat_completion.choices[0].message.content
    print("\nGenerated content:")
    print(generated_content)

    yes_no = input('\nIs this fine? (yes/no) >  ')
    if yes_no == 'yes':
        content = generated_content
    else:
        content = input('\nEnter >  ')
else:
    content = input('\nEnter the content of the video >  ')

# Create the directory
if os.path.exists('generated') == False:
    os.mkdir('generated')

# Generate speech for the video
speech = gTTS(text=content, lang='en', tld='ca', slow=False)
speech.save("generated/speech.mp3")

gp = random.choice(["1", "2"])
start_point = random.randint(1, 480)
audio_clip = AudioFileClip("generated/speech.mp3")

if (audio_clip.duration + 1.3 > 58):
    print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
    exit()

print('\n')

### VIDEO EDITING ###

# Trim a random part of minecraft gameplay and slap audio on it
video_clip = VideoFileClip("gameplay/gameplay_" + gp + ".mp4").subclip(start_point, start_point + audio_clip.duration + 1.3)
final_clip = video_clip.set_audio(audio_clip)

# Resize the video to 9:16 ratio
w, h = final_clip.size
target_ratio = 1080 / 1920
current_ratio = w / h

if current_ratio > target_ratio:
    # The video is wider than the desired aspect ratio, crop the width
    new_width = int(h * target_ratio)
    x_center = w / 2
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center)
else:
    # The video is taller than the desired aspect ratio, crop the height
    new_height = int(w / target_ratio)
    x_center = w / 2
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center)

# Write the final video
final_clip.write_videofile("generated/" + title + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)