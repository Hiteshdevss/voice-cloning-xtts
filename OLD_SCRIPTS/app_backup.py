from TTS.api import TTS
import os
os.environ["COQUI_TOS_AGREED"] = "1"

device = "cuda"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

#@spaces.GPU(enable_queue=True)
def clone(text, audio):
    tts.tts_to_file(text=text, speaker_wav="./Input_Voices/hitler.mp3", language="en", file_path="./output.wav")
    return "./output.wav"

clone("My German countrymen, men and women, (long pause) Changes of Government have occurred frequently in history, and in the history of our people.", "./output.wav")