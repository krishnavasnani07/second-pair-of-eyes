from faster_whisper import WhisperModel

model = WhisperModel("base")

def transcribe_audio(audio_file):

    segments, info = model.transcribe(audio_file)

    text = ""

    for segment in segments:
        text += segment.text

    return text