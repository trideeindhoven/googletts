#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import config
import json
import base64

class GoogleTTS:
    def __init__(self):
        self.url          = "https://texttospeech.googleapis.com/v1/text:synthesize"
        self.apiKey       = config.config['googleAPIkey']
        self.voice        = {'name': None, 'languageCode': None}
        self.httpSession  = requests.session()
        self.audioConfig  = {'audioEncoding':    config.config['audioEncoding'], 
                             'speakingRate':     config.config['speakingRate'],
                             'pitch':            config.config['pitch'],
                             'volumeGainDb':     config.config['volumeGainDb'],
                             'sampleRateHertz':  config.config['sampleRateHertz'],
                             'effectsProfileId': config.config['effectsProfileId']
                            }
        self.content = None

    def setVoice(self, name, languageCode):
        self.voice['name']         = name
        self.voice['languageCode'] = languageCode

    def produce(self, text=None, ssml=None):
        if text is None and ssml is None:
                print("No text or ssml to produce")
                return

        data = {
                "input": {},
                "voice": {"name":  self.voice['name'], "languageCode": self.voice['languageCode']},
                "audioConfig": self.audioConfig
               }

        if text is not None:
            data['input']['text'] =  text
        if ssml is not None:
            data['input']['ssml'] =  ssml

        headers = {"content-type": "application/json", "X-Goog-Api-Key": self.apiKey }

        r = self.httpSession.post(url=self.url, json=data, headers=headers)
        self.content = json.loads(r.content)

    def audio(self):
        return base64.b64decode(self.content['audioContent'])


#this only runs as a test, but not if imported
if __name__ == "__main__":
  tts = GoogleTTS()
  tts.setVoice(name='nl-NL-Wavenet-E', languageCode='nl-NL')
  ssml = "<speak>Goededag. Dit is een computerstem. Een fijne dag nog.</speak>"
  tts.produce(ssml=ssml)
  audio = tts.audio()

  fileExt = "wav"
  if config.config['audioEncoding'] == 'LINEAR16':
    fileExt = 'wav'
  elif config.config['audioEncoding'] == 'MP3':
    fileExt = 'mp3'

  with open('/tmp/tts.'+fileExt, 'wb') as audioFile:
    audioFile.write(audio)

