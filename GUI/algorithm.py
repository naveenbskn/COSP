
import speech_recognition as sr
#from langdetect import detect

def pyn_language_detector(soundi):
	AUDIO_FILE = (soundi)
	r = sr.Recognizer()
	with sr.AudioFile(AUDIO_FILE) as source:
	    
	    audio = r.listen(source) # read the entire audio file
	variables = ["en-US", "fr-FR","ta-IN"]


	for y in variables:
		try:
			x=r.recognize_google(audio,language = y)
			word=x.split()
			#print(word)
			if len(word)>=25:
			#print(y)
				break
		except:
			a=1
	#language=detect(x)
	#if(language==y[:2]):
	return(y)

#lang_code=array.index(max(array))