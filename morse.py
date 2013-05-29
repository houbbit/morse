#!/usr/bin/env python
#
#
# Program name:         morse.py
# Written by:           Laurens Houben
# Date and version No:  20130416
#
# Description:
# A python script to translate human readable text into morse.
# The morse code will be visualised inside the active terminal,
# and played back over the default soundcard.
# The playback is done at 10 words per minute (10wpm)
#
# Dependencies:
# python-alsaaudio

""" Example of how it runs:

$ ./morse.py "Laurens Houben"
L    a  u   r   e n  s     H    o   u   b    e n
.-.. .- ..- .-. . -. ...   .... --- ..- -... . -.

"""
# according to http://en.wikipedia.org/wiki/Morse_code#Representation.2C_timing_and_speeds
# International Morse code is composed of five elements:
#   short mark, dot or "dit" (.); "dot duration" is one unit long
#   longer mark, dash or "dah" (-); three units long
#   inter-element gap between the dots and dashes within a character; one dot duration or one unit long
#   short gap (between letters); three units long
#   medium gap (between words); seven units long


# Een DAH zijn drie DIT's.
# Ruimte tussen DIT's en DAH's is een DIT.
# Ruimte tussen twee letters is een DIT.
# Ruimte tussen twee woorden is DIT DAH DAH.

import sys, math, alsaaudio
DIT = 30
DAH = 3 * DIT
OCTAVE = 2                              # 1 == 441 Hz, 2 == 882 Hz, ...
nowave = '\0' * 150

#Dictionary aanmaken met morsecodes:
morsecodes = {
  ' ' : ' ',
  '@' : '.--.-.',
  '=' : '-...-',
  '_' : '..--.-',
  '-' : '-....-',
  ',' : '--..--',
  ';' : '-.-.-.',
  ':' : '---...',
  '?' : '..--..',
  '!' : '-.-.--',
  '/' : '-..-.',
  '.' : '.-.-.-',
  "'" : '.----.',
  '"' : '.-..-.',
  '(' : '-.--.',
  ')' : '-.--.-',
  '$' : '...-..-',
  '&' : '.-...',
  '+' : '.-.-.',
  '0' : '-----',
  '1' : '.----',
  '2' : '..---',
  '3' : '...--',
  '4' : '....-',
  '5' : '.....',
  '6' : '-....',
  '7' : '--...',
  '8' : '---..',
  '9' : '----.',
  'A' : '.-',
  'B' : '-...',
  'C' : '-.-.',
  'D' : '-..',
  'E' : '.',
  'F' : '..-.',
  'G' : '--.',
  'H' : '....',
  'I' : '..',
  'J' : '.---',
  'K' : '-.-',
  'L' : '.-..',
  'M' : '--',
  'N' : '-.',
  'O' : '---',
  'P' : '.--.',
  'Q' : '--.-',
  'R' : '.-.',
  'S' : '...',
  'T' : '-',
  'U' : '..-',
  'V' : '...-',
  'W' : '.--',
  'X' : '-..-',
  'Y' : '-.--',
  'Z' : '--..'
}

# Borrowed the following calculation from:
# http://svn.python.org/projects/python/branches/pep-0384/Demo/scripts/morse.py
#
# Een sinus in 100 samples bij 44.1 kHz is een toon van 441Hz.
# Als we twee sinussen genereren per 100 samples, krijgen we een toon van 882Hz.
# 882Hz klinkt morse-achtig.
def maakwave(octave):
    sinewave = ''
    for i in range(100):
        val = int(math.sin(math.pi * i * octave / 50.0) * 30000)
        sinewave += chr((val >> 8) & 255) + chr(val & 255)
    return sinewave

# String omzetten naar morse code met een \001 ASCII character (Start of heading).
def genereermorse(line):
    regel = ''
    for c in line:
        try:
            regel += morsecodes[c.upper()] + '\001'
        except KeyError:
            pass
    return regel

# Speel een lijn morse code.
def play(line, dev, wave):
    for c in line:
        if c == '.':
            sine(dev, DIT, wave)
        elif c == '-':
            sine(dev, DAH, wave)
        else:                   # spatie
            pause(dev, DAH + DIT)
        pause(dev, DIT)

def sine(dev, length, wave):
    for i in range(length):
        dev.write(wave)

def pause(dev, length):
    for i in range(length):
        dev.write(nowave)

def main():
    args = sys.argv[1:]
    wave = maakwave(OCTAVE)
    dev = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
    dev.setrate(44100)
    dev.setperiodsize(2)
    dev.setchannels(1)
    if args:
        source = [' '.join(args)]
    else:
        print "+=============================================================+"
        print "| Voer de tekst in en geef <Enter> om de regel af te sluiten. |"
        print "| Druk vervolgens op CTRL-D om de invoer af te spelen.        |"
        print "+=============================================================+"
        print
        source = iter(sys.stdin.readline, '')
    for line in source:
        for c in line:
            if c.upper() in morsecodes:
                print c.ljust(int(len(genereermorse(c))-1), ' '),
            else:
                pass
        print
        print genereermorse(line).replace('\001', ' ')
        play(genereermorse(line), dev, wave)

if __name__ == '__main__':
    main()

