from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.AudioClip import AudioArrayClip
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import algorithm
import json
import os
import re
import plyer.platforms.win.notification
from plyer import notification


def call(path):

    notification.notify("COSP Notification", "Process Started")
    
   
    r = sr.Recognizer()
    videoclip = VideoFileClip(path)
    audioclip = videoclip.audio
    audio_array = audioclip.to_soundarray()
    audio = AudioArrayClip(audio_array,fps=44100)
    audioclip.write_audiofile("myAudio.wav")

    myaudio = AudioSegment.from_file("myAudio.wav" , "wav") 
    chunk_length_ms = 53000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
    notification.notify("COSP Notification", "Process Completed 25%")

    #Export all of the individual chunks as wav files

    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        #print ("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

    no_of_chunk=i
    notification.notify("COSP Notification", "Process Completed 35%")

    #print(no_of_chunk)
    soundi="chunk0.wav"
    ##################################################
    lang_code=algorithm.pyn_language_detector(soundi)
    notification.notify("COSP Notification", "Process Completed 50%")

    #######################################
    json_path = os.path.abspath(os.path.join(os.pardir, 'json_files'))
    if lang_code=="en-US":
        json_file=os.path.join(json_path, "englishbral.json")
    elif lang_code=="fr-FR":
        json_file=os.path.join(json_path, "frenchbral.json")
    elif lang_code=="ta-IN":
        json_file=os.path.join(json_path, "tamilbral.json")

    
    text=""
    notification.notify("COSP Notification", "Process Completed 60%")
    #print(lang_code)
    for k in range(no_of_chunk+1):
        soundi="chunk{0}.wav".format(k)
        AUDIO_FILE = (soundi)
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
        
            audio = r.listen(source)
        te=r.recognize_google(audio,language = lang_code)
        text=text+te
        os.remove(soundi)



    
    

    notification.notify("COSP Notification", "Process Completed 90%")       
            
    #print(text)
    f=open("deafword.doc","w",encoding='utf-8')
    f.write(text)
    f.close()

    notification.notify("COSP Notification", "Process Ended")
    
    s=open("temp.txt","r")
    line=s.read()
    save_location=line[25:-29]
    
    #print(save_location)
    q=open("deafword.doc","r",encoding='utf-8')
    qq=q.read()
    f=open(save_location,"w",encoding='utf-8')
    f.write(qq)
    q.close()
    f.close()
    os.remove("deafword.doc")
    os.remove("myaudio.wav")





# function to call when user press 
# the save button, a filedialog will 
# open and ask to save file 
    



