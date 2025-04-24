from mido import MidiFile
import json

name = "1"
bpm = 60
out = f"backend/json/{name}.json"
mid = f"backend/mids/{name}.mid"

mid = MidiFile(mid, clip=True)

for msg in mid.tracks[1]:
    print(msg)
