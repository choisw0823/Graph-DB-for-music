from music21 import converter, corpus, instrument, midi, note, chord, pitch, stream, roman

class MIDI:
    def __init__(self, name):
        self.path = '/home/ec2-user/Dataset/'+name[0]+'/'+name[1]+'/'+name[2]+'/'+name
        self.mf = None
        self.midi = self.openMidi(self.path, True) 


    #open midi file
    def openMidi(self, midi_path, remove_drums):
        mf = midi.MidiFile()
        mf.open(midi_path)
        mf.read()
        mf.close()
        self.mf = mf
        #Removing Drum
        if (remove_drums):
            for i in range(len(mf.tracks)):
                mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]

        return midi.translate.midiFileToStream(mf)

    #return instrument list
    def instrument(self):
        instrument_list = []
        for track in self.mf.tracks:
            for e in track.events:
                if "PROGRAM" in repr(e) or "NAME" in repr(e):
                    i = midi.translate.midiEventsToInstrument(e)
                    if (i.instrumentName != None or i.instrumentName != 'all Channel'):
                        instrument_list.append(i.instrumentName)
        return list(set(instrument_list))
    
    #return key(조성)
    def key(self):
        chords = self.midi.chordify()
        temp_midi = stream.Score()
        temp_midi.insert(0, chords)
        keySignature = temp_midi.analyze('key')

        return keySignature
    
    #return time signature(박자)
    def timeSignature(self):
        timeSignature = self.midi.getTimeSignatures()[0]
        return str(timeSignature.beatCount) + '/' + str(timeSignature.denominator)

    def tempo(self):
        midi_file = music21.converter.parse(self.path)
        tempo = midi_file.analyze('tempo')

        return tempo

    #return chords list
    def extractChords(self):
        ret = []

        chords = self.midi.chordify()
        temp_midi = stream.Score()
        temp_midi.insert(0, chords)
        key = self.key()
        max_notes_per_chord = 4

        for m in chords.measures(0, None):
            if (type(m) != stream.Measure):
                continue 
            count_dict = dict()
            bass_note = self.noteCount(m, count_dict)
            if (len(count_dict)<1):
                ret.append("-")
                continue
            
            sorted_items = sorted(count_dict.items(), key=lambda x:x[1])

            sorted_notes = [item[0] for item in sorted_items[-max_notes_per_chord:]]

            measure_chord = chord.Chord(sorted_notes)

            # Convert the chord to the functional roman representation
            # to make its information independent of the music key.
            roman_numeral = roman.romanNumeralFromChord(measure_chord, key)
            ret.append(self.simplifyRomanName(roman_numeral))
        
        return list(set(ret))

    def noteCount(self, measure, count_dict):
        bass_note = None
        for chord in measure.recurse().getElementsByClass('Chord'):
            # All notes have the same length of its chord parent.
            note_length = chord.quarterLength
            for note in chord.pitches:          
            # If note is "C5", note.name is "C". We use "C5"
            # style to be able to detect more precise inversions.
                note_name = str(note) 
                if (bass_note is None or bass_note.ps > note.ps):
                    bass_note = note
                
                if note_name in count_dict:
                    count_dict[note_name] += note_length
                else:
                    count_dict[note_name] = note_length
        
        return bass_note

    def simplifyRomanName(self, roman_numeral):
         # Chords can get nasty names as "bII#86#6#5",
        # in this method we try to simplify names, even if it ends in
        # a different chord to reduce the chord vocabulary and display
        # chord function clearer.
        ret = roman_numeral.romanNumeral
        inversion_name = None
        inversion = roman_numeral.inversion()
    
        # Checking valid inversions.
        if ((roman_numeral.isTriad() and inversion < 3) or (inversion < 4 and (roman_numeral.seventh is not None or roman_numeral.isSeventh()))):
            inversion_name = roman_numeral.inversionName()
        if (inversion_name is not None):
            ret = ret + str(inversion_name)
        
        elif (roman_numeral.isDominantSeventh()): ret = ret + "M7"
        elif (roman_numeral.isDiminishedSeventh()): ret = ret + "o7"
        return ret


if __name__=='__main__':
    midi_name = '9cfd10de320309c0d6f492bb6718379e.mid'
    M = MIDI(midi_name)
    print(M.instrument())
    print(M.key())
    print(M.extractChords())
    print(M.timeSignature())

