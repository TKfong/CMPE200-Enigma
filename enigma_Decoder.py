import sys

class Enigma:
    # Constructor/Initialize Enigma machine
    def __init__(self):
        self.numcycles = 0
        self.rotors = []

        # Settings for the machine
        # We locked in only 3 rotors
        self.rotorsettings = [("III", 0),
                              ("II", 0),
                              ("I", 0)]
        # We arbitrarily chose Reflector B
        self.reflectorsetting = "B"

        # Decoder variables
        self.s = 0
        self.list_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.list_known = []
        self.knownText = []
        self.dict_worng = {}
        self.dict_right = {}
        self.dict_index = {}
        self.dict_available = {}
        self.contradict_flag = False
        self.should_restart = True
        self.available = False
        self.rotorRotateCounts = 0
        self.count = 0
        self.changeRotorPosition = False
        self.allMapped = False

        # Create each of the rotors
        for i in range(len(self.rotorsettings)):
            self.rotors.append(Rotor(self.rotorsettings[i]))

        # Create reflector
        self.reflector = Reflector(self.reflectorsetting)

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
            if (self.rotors[i].turnover):
                self.rotors[i].turnover = False
                self.rotors[i + 1].rotate()
        self.rotorRotateCounts = self.rotorRotateCounts + 1

        # Passthrough the plugboard forward
        index = self.indexOf_list(self.dict_right[c])

        # Move through each of the rotors from III->II->I
        for r in self.rotors:
            index = r.forward(index)

        # Pass through reflector B
        index = self.reflector.forward(index)

        # Move back through rotors in reverse: I->II->III
        for r in reversed(self.rotors):
            index = r.reverse(index)

        # Passthrough the plugboard reverse
        c = self.list_letters[index]

        return c                # returns last rotor III value on the return journey 

    # prints the rotor setup
    def print_setup(self):
		print()
		# Print rotor sequence
		for r in self.rotors:
		    	print(r.setting, "\t", r.sequence)
    # Initialize the available Map to default state 
    def initAvailableMap(self):
        for i in self.list_letters:
            self.dict_available[i] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # Returns index of the value from the available map
    def indexOf(self, key, value):
        for i, l in enumerate(self.dict_available[key]):
            if (l == value):
                return i

    # Returns index of the letter passed as an arguement
    def indexOf_list(self, value):
        for i,l in enumerate(self.list_letters):
            if (l == value):   
                return i

    # Removes the pairing from the Available Map 
    def removeAvailable(self, key, value):
        index_1 = self.indexOf(key, value)
        index_2 = self.indexOf(value, key)
        del self.dict_available[key][index_1]
        if( key != value ):
            del self.dict_available[value][index_2]
    
    # Map the asumed and deduced pairs on the plugboard
    def mapValues(self, key, value):
        self.dict_right[key] = value
        self.dict_right[value] = key
        
    # Checks for any contradictions in the mapping
    def checkContradiction(self, key, value):
        if (self.dict_right.has_key(key)): 
            if(self.dict_right[key] != value):
                self.contradict_flag = True
        if (self.dict_right.has_key(value)):
            if(self.dict_right[value] != key):
                self.contradict_flag = True

    # Checks whether all the letters in list_process and list_known are mapped 
    def checkIfAllMapped(self, list_process):
        for i in self.list_known:
            if( not self.dict_right.has_key(i)):
                self.allMapped = False
                return False
        for i in list_process:
            if( not self.dict_right.has_key(i)):
                self.allMapped = False
                return False
        self.allMapped = True
        return True
        
    # Checks if the letter is available for mapping
    def isAvailable(self, key, value):
        for i in self.dict_available[key]:
            if (i == value):
                self.available = True
                break

    # Rotates the rotor by one step
    def rotateRotar(self):
        self.rotors[0].rotate()
        # Double step
        if self.rotors[1].base[0] in self.rotors[1].notch:
            self.rotors[1].rotate()

        # Normal stepping
        for i in range(len(self.rotors) - 1):
            if (self.rotors[i].turnover):
                self.rotors[i].turnover = False
                self.rotors[i + 1].rotate()


    # Configures the plugboard settings
    def plugBoardSetting(self, list_process, list_known):
        while self.should_restart:
            self.should_restart = False
            self.reset()
            for i in range(0,self.count):
                self.rotateRotar()
            assumption = True
            self.rotorRotateCounts = 0
            for j in range(len(list_process)):
                l = list_process[j]
                if( assumption ):
                    assumption = False
                    if(len(self.dict_available[l]) != 0):
                        if (not (self.dict_right.has_key(l))):
                            for b in self.dict_available[l]:
                                if (not (self.dict_right.has_key(b))):
                                    self.mapValues(l, b)
                                    self.removeAvailable(l, b)
                                    break
                    else:
                        self.count = self.count + 1
                        self.changeRotorPosition = True
                        self.dict_available.clear()
                        self.initAvailableMap()
                        break
                    value_order_1 = self.encrypt(l)
                    self.deduce(value_order_1, list_known[j])
                else:
                    if(self.dict_right.has_key(l)):
                        value_order_1 = self.encrypt(l)
                        self.deduce(value_order_1, list_known[j])
                    elif(self.dict_right.has_key(list_known[j])):
                        value_order_1 = self.encrypt(list_known[j])
                        self.deduce(value_order_1, l)
                    else:
                        self.rotateRotar()
                        self.rotorRotateCounts = self.rotorRotateCounts + 1

                if(self.should_restart):
                        break
            if(not self.checkIfAllMapped(list_process)):
                self.should_restart = True
        for i in self.list_letters:
            print(i , " : ", self.dict_available[i])
        print("plug Board Setting")

    def deduce(self, deduce, known):
                if (not (self.dict_right.has_key(known) or self.dict_right.has_key(deduce))):  # deduce is present in map
                    self.isAvailable(deduce, known)
                    if (not self.available):
                        self.contradict_flag = False
                        self.dict_right.clear()
                        
                        # Start a fresh
                        self.should_restart = True
                    else:
                        self.mapValues(deduce, known)
                        if (self.available):
                            self.available = False
                            self.removeAvailable(deduce, known)
                else:
                    self.checkContradiction(deduce,known)  ## Sets contradict_flag = true in case of contradiction
                    if (self.contradict_flag):
                        self.isAvailable(deduce, known)
                        if (self.available):
                            self.available = False
                            self.removeAvailable(deduce, known)
                        self.dict_right.clear()
                        self.contradict_flag = False
                        # Start a fresh
                        self.should_restart = True
                    else:
                        self.isAvailable(deduce, known)
                        if (self.contradict_flag):
                            self.contradict_flag = False
                            self.dict_right.clear()
                            
                            # Start a fresh
                            self.should_restart = True

    def decrypt(self, message):
        print("decrypting")
        # reset to the deduced setting
        self.reset()
        for i in range(0,self.count):
            self.rotateRotar()

        # prints the decoded message
        for i in message:
            if(i != '\n'):
                c = self.encrypt(i)
                c = self.dict_right[c]
                print c,


    def slider(self, myList):
        count = 1
        #self.knownText = "AKMSDOWQROFLWPAWAWFIWGKOBDFFMVMXCNBFDIZPVXLBPRPEHLEPLPCVPP"
        list_process = []
        self.stringToList(self.knownText, self.list_known)
        while (count > 0 and self.s < (len(myList) - len(self.list_known) - 1)):
            list_process = []
            count = 0
            for j in range(0, len(self.list_known)):
                if (myList[self.s + j] == self.list_known[j]):
                    count = count + 1
                    break
                else:
                    list_process.append(myList[self.s + j])

            self.s = self.s + 1
        self.s = self.s + 1
        return list_process

    def stringToList(self, myString, myList):
        for i, l in enumerate(myString):
            myList.append(l)
        print(" Converting String to List")



class Rotor:
    """
    Setting Wiring                      Notch   Window  Turnover
    Base    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    I       EKMFLGDQVZNTOWYHXUSPAIBRCJ  Y       Q       R
    II      AJDKSIRUXBLHWTMCQGZNPYFVOE  M       E       F
    III     BDFHJLCPRTXVZNYEIWGAKMUSQO  D       V       W
    IV      ESOVPZJAYQUIRHXLNFTGKDCMWB  R       J       K
    V       VZBRGITYUPSDNHLXAWMJQOFECK  H       Z       A
    VI      JPGVOUMFYQBENHZRDKASXLICTW  H/U     Z/M     A/N
    VII     NZJHGRCXMYSWBOUFAIVLPEKQDT  H/U     Z/M     A/N
    VIII    FKQHTLXOCBJSPDZRAMEWNIUYGV  H/U     Z/M     A/N

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
            "I": ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["R"], ["Q"]],
            "II": ["AJDKSIRUXBLHWTMCQGZNPYFVOE", ["F"], ["E"]],
            "III": ["BDFHJLCPRTXVZNYEIWGAKMUSQO", ["W"], ["V"]]}
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

        if (self.base[0] in self.turnovers):
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
        self.settings = {"B": "YRUHQSLDPXNGOKMIEBFZCWVJAT"}

        self.sequence = self.sequence_settings()

    # Setup initial sequence for Reflector
    def sequence_settings(self):
        return self.settings[self.setting]

    # Input into reflector
    def forward(self, index):
        return self.sequence.index(self.base[index])

def main():
    # Initialize an Enigma machine
    machine = Enigma()
    # Output
    ciphertext = ""

    #try:
    f = open("input.txt", "r")  # opens the input file
    message = f.read()
    # print message
    list_input = []  # List for input from text file
    list_process = []  # List for processing on extracted message
    # initial setting
    machine.knownText = "AKMSDOWQROFLWPAWAWFIWGKOBDFFMVMXCNBFDIZPVXLBPRPEHLEPLPCVPP"            # Known text 
    machine.initAvailableMap()
    machine.stringToList(message, list_input)
    list_process = machine.slider(list_input)
    print(list_process, machine.s)
    machine.plugBoardSetting(list_process, machine.list_known)
    machine.decrypt(message)

if __name__ == '__main__':
    main()
