#!/usr/bin/env python

"""
Parse a file in ABC music notation format and render with PySynth.

Usage:

note_list_to_assets.py note_list_filename [bpm] [--syn_b/--syn_c/--syn_d/--syn_e/--syn_p/--syn_s/--syn_samp]

Some of the definitions are borrowed from PlayABC 1.1

2012-07-17
"""

import ast
import sys
import os
if sys.version >= '3':
	import urllib.request, urllib.error, urllib.parse
else:
	import urllib2

# Reference: https://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python
def MidiStringToInt(midstr):
    Notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
    answer = 0
    i = 0
    #Note
    letter = midstr[:-1]
    for note in Notes:
        for form in note:
            if letter.upper() == form:
                answer = i
                break;
        i += 1
    #Octave
    answer += (int(midstr[-1]))*12
    return answer


sel = False
song = []

note_list_filename = sys.argv[1]

try: bpm = int(sys.argv[2])
except: bpm = 60

if "--syn_b" in sys.argv:
	import pysynth_b as pysynth
elif "--syn_s" in sys.argv:
	import pysynth_s as pysynth
elif "--syn_e" in sys.argv:
	import pysynth_e as pysynth
elif "--syn_c" in sys.argv:
	import pysynth_c as pysynth
elif "--syn_d" in sys.argv:
	import pysynth_d as pysynth
elif "--syn_p" in sys.argv:
	import pysynth_p as pysynth
elif "--syn_samp" in sys.argv:
	import pysynth_samp as pysynth
else:
	import pysynth

with open(note_list_filename, "r") as file:
	list_str = file.read();
	song = ast.literal_eval(list_str)

sound_id = 0
os.makedirs("sounds", exist_ok=True)

note_set = set()
for note_sublist in song:
	note_set.add(tuple(note_sublist))

for note_tuple in note_set:
	pysynth.make_wav([list(note_tuple)], bpm = bpm, fn="sounds/"+str(sound_id) +".wav")
	sound_id += 1

pysynth.make_wav(song, bpm = bpm, fn="out.wav")

