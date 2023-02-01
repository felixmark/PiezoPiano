from mido import MidiFile

class MidiToC():

    @staticmethod
    def note_to_frequency(note):
        default_a = 440 # frequency of A (coomon value is 440Hz)
        return round((default_a / 32) * (2 ** ((note - 9) / 12)))

    @staticmethod
    def convert_midi_to_c(file_path):
        mid = MidiFile(file_path, clip=True)

        # One list for each piezo speaker
        song = [[],[],[],[],[],[],[],[]]

        print("Length in s:", round(mid.length))
        print("Tracks:", len(mid.tracks))

        for i, track in enumerate(mid.tracks):
            print("="*80)
            print('Track {}: {}'.format(i, track.name))
            print("="*80)
            for msg in track:
                if msg.is_meta:
                    if msg.type == 'time_signature':
                        print("Time signature:", msg.numerator, "/", msg.denominator, "@", msg.clocks_per_click, "clocks per tick")
                    elif msg.type == 'key_signature':
                        print("Track key:", msg.key)
                    elif msg.type == 'end_of_track':
                        break
                    else:
                        print("Meta:", msg)
                elif msg.type == 'note_on':
                    print("Frequency:", MidiToC.note_to_frequency(msg.note), "Channel:", msg.channel, "Velocity:", msg.velocity, "Time:", msg.time)
                elif msg.type == 'control_change':
                    # Do not adjust volume
                    continue
                else:
                    print("Other:", msg)

        return song

def main():
    song = MidiToC.convert_midi_to_c('Hoshi no Koe - Mikako kara no Tayori.mid')
    print("Song:", song)

if __name__ == "__main__":
    main()

