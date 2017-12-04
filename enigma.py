#! /usr/bin/env python3
import sys
from easygui import *

class Enigma:
	# Constructor/Initialize Enigma machine
	def __init__(self, set1, set2, set3):
        	self.numcycles = 0
        	self.rotors = []

		# Settings for the machine
		# We locked in only 3 rotors
		self.rotorsettings = [("III", set3),
				    ("II", set2),
				    ("I", set1)]
		# We arbitrarily chose Reflector B
		self.reflectorsetting = "B"
		self.plugboardsetting = []

		# Create the plugboard
		self.plugboard = Plugboard(self.plugboardsetting)

		# Create each of the rotors
		for i in range(len(self.rotorsettings)):
		    	self.rotors.append(Rotor(self.rotorsettings[i]))

		# Create reflector
		self.reflector = Reflector(self.reflectorsetting)

	# Simple print function of setup information
	def print_setup(self):
		print()
		# Print rotor sequence
		print("Rotor sequence: (right to left)")
		for r in self.rotors:
		    	print(r.setting, "\t", r.sequence)

		print()
		# Print Reflector's sequence
		print("Reflector sequence:")
		print(self.reflector.setting, "\t", self.reflector.sequence, "\n")

		# Print Plugboard settings; if any
		print("Plugboard settings:")
		print(self.plugboard.mapping, "\n")

	# Reset the machine's rotors to default state:
	def reset(self):
		self.numcycles = 0
		# Iterate throught the rotors
		for r in self.rotors:
	    		r.reset()

	# Encrypt a single character
	def encrypt(self, c):

		# Force all messages to upper case
		# Note: there is a bug when try to pass messages in lower case
		c = c.upper()
		
		# Check if it is a letter
		if (not c.isalpha()):
	    		return c

		# Rotate everytime there is an input
		self.rotors[0].rotate()

		# Double step
		if self.rotors[1].base[0] in self.rotors[1].notch:
		    	self.rotors[1].rotate()

		# Normal stepping
		for i in range(len(self.rotors) - 1):
	    		if(self.rotors[i].turnover):
		        	self.rotors[i].turnover = False
		        	self.rotors[i + 1].rotate()

		# Passthrough the plugboard forward
		index = self.plugboard.forward(c)

		# Move through each of the rotors from III->II->I
		for r in self.rotors:
		    	index = r.forward(index)

		# Pass through reflector B
		index = self.reflector.forward(index)

		# Move back through rotors in reverse: I->II->II
		for r in reversed(self.rotors):
			index = r.reverse(index)

		# Passthrough the plugboard reverse
		c = self.plugboard.reverse(index)

		return c
class Rotor:
	"""
	Setting Wiring                      Notch   Window  Turnover
	Base    ABCDEFGHIJKLMNOPQRSTUVWXYZ
	I       EKMFLGDQVZNTOWYHXUSPAIBRCJ  Y       Q       R
	II      AJDKSIRUXBLHWTMCQGZNPYFVOE  M       E       F
	III     BDFHJLCPRTXVZNYEIWGAKMUSQO  D       V       W

	Inverted Wiring
	Base    ABCDEFGHIJKLMNOPQRSTUVWXYZ
	I	UWYGADFPVZBECKMTHXSLRINQOJ
	II	AJPCZWRLFBDKOTYUQGENHXMIVS
	III	TAGBPCSDQEUFVNZHYIXJWLRKOM

	"""

	# Constructor to initialize Rotor settings
	def __init__(self, settings):
		self.setting = settings[0]
		self.ringoffset = settings[1]
		self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.settings = {
		        "I":    ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["R"], ["Q"]],
		        "II":   ["AJDKSIRUXBLHWTMCQGZNPYFVOE", ["F"], ["E"]],
		        "III":  ["BDFHJLCPRTXVZNYEIWGAKMUSQO", ["W"], ["V"]]}
		self.turnovers = self.settings[self.setting][1]
		self.notch = self.settings[self.setting][2]
		self.sequence = None
		self.turnover = False
		self.reset()
		
	# Reset the rotors to default setting
	def reset(self):
		self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.sequence = self.settings[self.setting][0]
		for _ in range(self.ringoffset):
            		self.rotate()

	# Move right to left through the rotor
	def forward(self, index):
        	return self.base.index(self.sequence[index])

	# Move left to right back through the rotor
    	def reverse(self, index):
        	return self.sequence.index(self.base[index])

	# Rotate the rotor once
	def rotate(self):
		self.base = self.base[1:] + self.base[:1]
		self.sequence = self.sequence[1:] + self.sequence[:1]

		if(self.base[0] in self.turnovers):
	    		self.turnover = True

class Reflector:
	"""
	Setting     Wiring
    	Base        ABCDEFGHIJKLMNOPQRSTUVWXYZ
    	B           YRUHQSLDPXNGOKMIEBFZCWVJAT

	"""
	
	# Constructor for Reflector
	def __init__(self, setting):
		self.setting = setting
		self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.settings = {"B":    "YRUHQSLDPXNGOKMIEBFZCWVJAT"}

		self.sequence = self.sequence_settings()

	# Setup initial sequence for Reflector
    	def sequence_settings(self):
        	return self.settings[self.setting]

	# Input into reflector   	
	def forward(self, index):
        	return self.sequence.index(self.base[index])

class Plugboard:
	# Constructor for Plugboard
	def __init__(self, mapping):
		mapping = [("A", "B"), ("C", "D")]
		self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.mapping = {}

		for m in self.base:
	    		self.mapping[m] = m

		for m in mapping:
		    	self.mapping[m[0]] = m[1]
		    	self.mapping[m[1]] = m[0]
	
	# Forward route through the plugboard
	def forward(self, c):
        	return self.base.index(self.mapping[c])

	# Backward route through the plugboard
    	def reverse(self, index):
        	return self.mapping[self.base[index]]

def main():
	# Create GUI
	msg = "Enter machine settings"
	title = "Enigma Machine"
	fieldNames = ["Rotor1","Rotor2","Rotor3","Input"]
	fieldValues = []  # we start with blanks for the values
	fieldValues = multenterbox(msg,title, fieldNames)

	# make sure that none of the fields was left blank
	while 1:
	    if fieldValues == None: break
	    errmsg = ""
	    for i in range(len(fieldNames)):
	      if fieldValues[i].strip() == "":
		errmsg = errmsg + ('"%d" is a required field.\n\n' % fieldNames[i])
	    if errmsg == "": break # no problems found
	    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

	# Initialize an Enigma machine
	# Read inputs from the gui - fieldValues[]
	machine = Enigma(int(fieldValues[0]),int(fieldValues[1]),int(fieldValues[2]))
	# Output
	ciphertext = ""

	try:
		# Read input when running program
		# Input is now from gui
		plaintext = fieldValues[3]
		# Print the machine's setup
		machine.print_setup()

		# Print the initial message
		print("Plaintext", "\t", plaintext)
		# Loop through each character of message
		# and feed into the machine's encrypt program
		for character in plaintext:
		    	ciphertext += machine.encrypt(character)

		# Print out the encrypted message
		print("Ciphertext", "\t", ciphertext)

		# Reset and Decode same message
		machine.reset()
		plaintext = ""
		for character in ciphertext:
	    		plaintext += machine.encrypt(character)

		print("Plaintext", "\t", plaintext, "\n")
	except IndexError:
		for plaintext in sys.stdin:
	    		for character in plaintext:
				sys.stdout.write(machine.encrypt(character))

if __name__ == '__main__':
	main()
