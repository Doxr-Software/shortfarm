from dotenv import load_dotenv
import random
import os
from g4f.client import Client
from g4f.Provider import DDG
from random_word import RandomWords
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
import requests
import base64
import json
import subprocess

load_dotenv()
r = RandomWords()
client = Client()

title = "example"
option = "yes"

if option == 'yes':
    theme_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Give a very very short phrase of an interesting topic. The theme should be interesting but not complicated or deep. {r.get_random_word()}"}],
    )
    theme = theme_response.choices[0].message.content
    print(f"\nGenerated theme: {theme}")

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Act as an script writer who writes engaging and professional scripts for tiktok shorts. you never do a grammatical mistake and write very engaging scripts that touches the viewers' attention. At the beginning of the video you never forget to add a viral hook that will catch the viewers attention and will break the scroll. Your scripts are so loved by users that they subscribe and follow the channel. Don't mention any channel's name but at appropriate point tell the viewer to like the video and follow or subscribe the channel or account. (Remember tiktok shorts have max limit of 1 min). It is recommended to create a much much shorter script than what would be 1 minute of speech. Essentially it should be about 2-3 small paragraphs of words. Do not use ANY markdown or indicators; you're only making the speaking part of the script and the user will handle all other elements. Everything you generate should be English. Now Generate content on - \"{theme}\""}],
    )
    generated_content = chat_completion.choices[0].message.content
    print("\nGenerated content:")
    print(generated_content)

    yes_no = 'yes'
    if yes_no == 'yes':
        content = generated_content
    else:
        content = input('\nEnter >  ')
else:
    content = input('\nEnter the content of the video >  ')

if not os.path.exists('generated'):
    os.mkdir('generated')

speech = gTTS(text=content, lang='en', tld='ca', slow=False)
speech.save("generated/speech.mp3")

def get_subtitles(audio_file):
    with open(audio_file, "rb") as file:
        audio_base64 = base64.b64encode(file.read()).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        'audio': f'data:audio/mpeg;base64,{audio_base64}',
        'chunk_level': 'word' 
    }
    
    response = requests.post('https://api.deepinfra.com/v1/inference/openai/whisper-large-v3-turbo', 
                             headers=headers, 
                             json=data)
    
    if response.status_code == 200:
        return response.json()['segments']
    else:
        print(f"Error: {response.status_code}")
        return None

subtitles = get_subtitles("generated/speech.mp3")

gp = random.choice(["1", "2", "3"])
start_point = random.randint(1, 480)
audio_clip = AudioFileClip("generated/speech.mp3")

if (audio_clip.duration + 1.3 > 58):
    print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
    exit()

print('\n')

### VIDEO EDITING ###

# Trim a random part of gameplay, add voiceover
video_clip = VideoFileClip("gameplay/gameplay_" + gp + ".mp4").subclip(start_point, start_point + audio_clip.duration + 1.3)
final_clip = video_clip.set_audio(audio_clip)

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

# [JUMPHERE] to create subtitles with black highlight
def create_subtitle_clips(subtitles, videosize):
    subtitle_clips = []
    
    for subtitle in subtitles:
        start_time = subtitle['start']
        end_time = subtitle['end']
        duration = end_time - start_time
        
        # Calculate vertical position (60% of video height)
        vertical_position = int(videosize[1] * 0.6)
        
        # Create text clip
        text_clip = TextClip(subtitle['text'], fontsize=60, color='white', font='fonts/font.ttf', 
                              size=(videosize[0], None), method='caption', align='center')
        
        text_width = text_clip.w
        
        # Create black background
        bg_clip = ColorClip(size=(text_width, text_clip.h + 10), color=(0,0,0))
        bg_clip = bg_clip.set_opacity(.6)
        
        # Composite text over background
        final_text_clip = CompositeVideoClip([bg_clip, text_clip.set_position('center')])
        
        # Set position to 60% of vertical
        final_text_clip = final_text_clip.set_position(('center', vertical_position))
        
        # Set timing
        final_text_clip = final_text_clip.set_start(start_time).set_duration(duration)
        
        subtitle_clips.append(final_text_clip)
    
    return subtitle_clips

# Add subtitles to the video
subtitle_clips = create_subtitle_clips(subtitles, final_clip.size)
final_clip_with_subtitles = CompositeVideoClip([final_clip] + subtitle_clips)

# Write the final video
final_clip_with_subtitles.write_videofile("generated/" + title + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

ai_title = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": f"Generate a short, captivating title for this script. Don't use quotes when creating the title. Script:\n{content}"}],
)
ai_title = ai_title.choices[0].message.content
ai_description = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": f"Generate a very short, captivating description for this script. Don't use quotes when creating the description. Script:\n{content}"}],
)
ai_description = ai_description.choices[0].message.content
ai_keywords = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": f"Generate a short list of 3-5 keywords, separate each with commas (no spaces in the list at all), based on the script. Script:\n{content}"}],
)
ai_keywords = ai_keywords.choices[0].message.content

print(ai_title, ai_description, ai_keywords)

# Upload the video
upload_command = f'python3 upload_video.py --file="generated/example.mp4" --title="{ai_title}" --description="{ai_description}" --keywords="{ai_keywords}" --category="24" --privacyStatus="public"'

subprocess.run(upload_command, shell=True)

print("Video generation and upload process completed.")