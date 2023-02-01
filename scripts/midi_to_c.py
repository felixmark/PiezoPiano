from mido import MidiFile

def noteToFreq(note):
    a = 440 #frequency of A (coomon value is 440Hz)
    return round((a / 32) * (2 ** ((note - 9) / 12)))

mid = MidiFile('Hoshi no Koe - Mikako kara no Tayori.mid', clip=True)
print(mid)

for msg in mid:
    print(msg)
    if msg.type == 'note_on':
        print(noteToFreq(msg.note))
        print(noteToFreq(msg.channel))
        print(noteToFreq(msg.velocity))
        print(noteToFreq(msg.time))
    else:
        print(msg)