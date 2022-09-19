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
	#Rest note
	if midstr == "r":
		return 0
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
second_per_beat = 60/bpm
second_per_whole_note = 4 * second_per_beat

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

os.makedirs("sounds", exist_ok=True)
sound_id = 0
note_dict = dict()
for note_sublist in song:
	note_tuple = tuple(note_sublist)
	if note_tuple in note_dict:
		continue
	note_dict[note_tuple] = sound_id
	sound_id += 1

# Generate pitch id, start play time, and asset id list
song_pitch_time_sequence = []
start_time_point = 0.0
for note_sublist in song:
	note_tuple = tuple(note_sublist)
	note_str = note_tuple[0].replace("*","")
	if note_str != "r" and (not note_str[-1].isnumeric()):
		# Add default octave
		note_str = note_str + "4"
	song_pitch_time_sequence.append((MidiStringToInt(note_str), start_time_point, note_dict[note_tuple]))
	start_time_point += second_per_whole_note * 1/float(note_tuple[1])
print(song_pitch_time_sequence)

for note_tuple in note_dict.keys():
	pysynth.make_wav([list(note_tuple)], bpm = bpm, fn="sounds/"+str(note_dict[note_tuple]) +".wav")

pysynth.make_wav(song, bpm = bpm, fn="out.wav")

