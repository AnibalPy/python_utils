import whisper
import os

model = whisper.load_model("base")
result = model.transcribe("./Audios/prueba_pepita.mp3")
print(result["text"])

# save TXT
with open(os.path.join("./Audios/", "prueba_pepita.txt"), "w", encoding="utf-8") as txt:
    txt.write(result["text"])

# save SRT (subtítulos)
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

with open(os.path.join("./Audios/", "prueba_pepita.srt"), "w", encoding="utf-8") as srt:
    for i, segment in enumerate(result["segments"], start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt.write(f"{i}\n{start} --> {end}\n{text}\n\n")

