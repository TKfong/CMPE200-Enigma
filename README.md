CMPE 200 Group Project
Enigma Machine Emulator and Decoder

Abstract:
This project is to emulate the Enigma machine, a electro-mechanical rotor cipher machine used during WW2, purely with software and to exploit built-in flaws of the device to break the message keys.

Summary:
The purpose of this project is to investigate the World War 2 encryption machines, specifically the German Enigma machine, and present a possible way to decrypt and decode its messages keys. To achieve this task, we implemented two programs: a program to emulate Enigma purely through software and another program that takes in decrypted messages from the first program and outputs the machine's settings for each encryption. This project involves research and design of cryptographic algorithms as well as how to break each instance of the Enigma code by exploiting flaws in the encryption algorithm. The programs are written in Python.

Description of the problem:
With the spread of the Internet, encryption has become a prevalent but invisible part of our every day lives. Encryption helps to keep private information secure from public perception and is an invisible armor as we traverse through the internet. To better understand encryption and its functionality in modern society, we chose to trace it back to its origin: the military and war. Encryption, like with most technology, originated from the military to protect information of commands from officers. We chose to reproduce a recently retold WW2 story of Alan Turing and the breaking of the Enigma code. 

Implementation:
Enigma at its base is a simple circuit that lights up a letter when you press down on the keyboard. Its uniqueness stems from how the circuit changes after each time you press the keyboard. So each letter has its unique encryption, as opposed to traditional encryption that would repeat the encryption method across the entire message. The changes in the circuit were implemented through a series of rotors and crossed wiring. We emulated the rotors through arrays that would increment, changing the code as the rotors did, and copied the pathing of the wiring changing the original letter to a guaranteed different letter. Likewise for the decryption, flaws in the Enigma machine were utilized to obtain the machine's settings. Flaws included no letter could be enciphered to itself and if a guessed setting was incorrect, then all the subsequent deduced settings were also incorrect and could be eliminated in the next trial.

Future Works:
Improving the decrypter to require a smaller known message to determine the machine's encryption settings and to speed up the process.
Improve the GUI to be more interactive with the user.

References:
https://www.youtube.com/watch?v=G2_Q9FoD-oQ
https://www.youtube.com/watch?v=V4V2bpZlqx8
