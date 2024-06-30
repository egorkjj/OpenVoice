import torch
from TTS.api import TTS

device =  "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
txt = '''Брат, привет. Прости, сейчас не дома, чуть-чуть занят, не смогу ответить. Перезвоню тебе позже, как время будет.'''
tts.tts_to_file(text=txt, speaker_wav=["morgen.wav"], file_path="output3.wav", language="ru")