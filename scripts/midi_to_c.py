from mido import MidiFile

class Tempo():
    def __init__(self, time, ticks_per_beat) -> None:
        self.time = time
        self.ticks_per_beat = ticks_per_beat

class Note():
    def __init__(self, time_played, frequency, ticks_per_beat) -> None:
        self.time_played = round(time_played)
        self.time_stopped = 0
        self.frequency = frequency
        self.ticks_per_beat = ticks_per_beat

    def __str__(self) -> str:
        return "{" + str(self.time_played) + "," + str(self.frequency) + "," + str(self.time_stopped) + "}"

class Song():
    usec_per_beat = 500_000
    clocks_per_click = 0
    total_times = []
    keys = []
    tempochanges = []
    final_8_buzzer_song = [ [], [], [], [], [], [], [], [] ]

    def __init__(self, song_path:str, length_in_s:int, ticks_per_beat:int) -> None:
        self.song_path = song_path
        self.length_in_s = length_in_s
        self.ticks_per_beat = ticks_per_beat

    def append_note(self, note_to_append:Note) -> None:
        success = False
        for buzzer in self.final_8_buzzer_song:
            buzzer_is_free = True
            for note in buzzer:
                if note.time_stopped == 0:
                    buzzer_is_free = False 
            if buzzer_is_free:
                buzzer.append(note_to_append)
                success = True
                break
        return success

    def end_note(self, time_stopped, frequency):
        success = False
        for buzzer in self.final_8_buzzer_song:
            for note in buzzer:
                if frequency == note.frequency and note.time_stopped == 0:
                    note.time_stopped = round(time_stopped)
                    success = True
                    break
            if success:
                break
        return success

    def __str__(self) -> str:
        ret_str = "\n"
        ret_str += "File path:      " + self.song_path + "\n"
        ret_str += "Length:         " + str(round(self.length_in_s, 3)) + " s\n"
        ret_str += "Ticks / beat:   " + str(self.ticks_per_beat) + " \n"
        ret_str += "Keys of tracks: " + str(self.keys) + " \n"

        for track_id, total_time in enumerate(self.total_times):
            ret_str += "Length track " + str(track_id) + ": " + str(round(self.total_times[track_id] / 1_000_000, 3)) + " s\n"

        for buzzer_id, buzzer in enumerate(self.final_8_buzzer_song):
            ret_str += "Notes buzzer " + str(buzzer_id) + ": " + str(len(self.final_8_buzzer_song[buzzer_id])) + "\n"

        ret_str += ("=" * 80) + "\n"
        ret_str += "unsigned long song[8][][] = {   // 8 Buzzers playing N notes consisting of 3 parameters: time played in us, frequency in Hz and time stopped in us\n"
        first_buzzer = True
        for buzzer_id, buzzer in enumerate(self.final_8_buzzer_song):
            first_note = True
            if not first_buzzer:
                ret_str += ",\n"
            first_buzzer = False
            ret_str += "    {"
            for note_id, note in enumerate(self.final_8_buzzer_song[buzzer_id]):
                if not first_note:
                    ret_str += ","
                    if note_id % 5 == 0:
                        ret_str += "\n" + "        "
                else:
                    ret_str += "\n" + "        "
                first_note = False
                ret_str += str(self.final_8_buzzer_song[buzzer_id][note_id])
            ret_str += "\n    }"
        ret_str += "\n}"
        
        return ret_str

class MidiToC():

    @staticmethod
    def note_to_frequency(note):
        default_a = 440 # frequency of A (coomon value is 440Hz)
        return round((default_a / 32) * (2 ** ((note - 9) / 12)))

    @staticmethod
    def convert_midi_to_c(file_path):
        print("Converting midi to C...")
        mid = MidiFile(file_path, clip=True)
        output_song = Song(file_path, mid.length, mid.ticks_per_beat)
        current_tempo = 0

        for track_id, track in enumerate(mid.tracks):
            output_song.total_times.append(0)
            output_song.keys.append("?")

            for msg in track:
                msg_type = msg.type

                if msg.time and current_tempo > 0:
                    output_song.total_times[track_id] += msg.time * (current_tempo / output_song.ticks_per_beat)

                if msg.type == 'note_on' and msg.velocity == 0:
                    msg_type = 'note_off'

                if msg.is_meta:
                    if msg_type == 'time_signature':
                        output_song.clocks_per_click = msg.clocks_per_click
                    elif msg_type == 'key_signature':
                        output_song.keys[track_id] = msg.key
                    elif msg_type == 'set_tempo':
                        current_tempo = msg.tempo
                    elif msg_type == 'end_of_track':
                        break
                elif msg_type == 'note_on':
                    output_song.append_note(Note(output_song.total_times[track_id], MidiToC.note_to_frequency(msg.note), current_tempo))
                elif msg_type == 'note_off':
                    output_song.end_note(output_song.total_times[track_id], MidiToC.note_to_frequency(msg.note))

        print("Done!")
        return output_song

def main():
    song = MidiToC.convert_midi_to_c('kesenai_tsumi.mid')
    print("Song:", song)

if __name__ == "__main__":
    main()

