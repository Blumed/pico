# Matrix Keypad

# Original creator and code source
# NerdCave - https://www.youtube.com/channel/UCxxs1zIA4cDEBZAHIJ80NVg - Subscribe if you found this helpful.
# Github - https://github.com/Guitarman9119

from machine import Pin
from utime import sleep
import _thread
import secret

# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'P'],
               ['7', '8', '9', 'T'],
               ['CLR', '0', 'ENT', 'EX']]

# PINs according to schematic
keypad_rows = [9,8,7,6]
keypad_columns = [5,4,3,2]

# Create two empty lists to set up pins
col_pins = []   #inputs
row_pins = []   #output   

# Keys entered by the user
guess = []

# Setup led pins to be an output
led_green = Pin(14, Pin.OUT, Pin.PULL_UP)
led_clear = Pin(13, Pin.OUT, Pin.PULL_UP)
led_red   = Pin(11, Pin.OUT, Pin.PULL_UP)

# Setup and initialize state object
class States:
    INACTIVE  = 'inactive'
    ACTIVE    = 'active'
    CORRECT   = 'correct'
    INCORRECT = 'incorrect'

State = States()

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,4):
    
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)


#### Light State ####

def light(state):
    if state == State.INACTIVE:
        led_clear.value(1)
        sleep(1)
        led_clear.value(0)

    if state == State.ACTIVE:
        led_clear.value(1)
        sleep(0.01)
        led_clear.value(0)

    if state == State.CORRECT:
        led_clear.value(0)
        led_green.value(1)
        sleep(3)
        led_green.value(0)
        light(State.INACTIVE)

    if state == State.INCORRECT:
        led_clear.value(0)
        led_red.value(1)
        sleep(3)
        led_red.value(0)
        light(State.INACTIVE)

#### Scan keys #####
    
def scankeys():
    for row in range(4):
        for col in range(4): 
            row_pins[row].high()
            
            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                sleep(0.2)

                if key_press.isdigit():
                    light(State.ACTIVE)
                    guess.append(key_press)
               
                if key_press == 'ENT':
                    checkPin(guess)

                if key_press == 'CLR':
                    guess.clear()
                    
        row_pins[row].low()

##### To check Pin #####

def checkPin(guess):
    print(guess)

    if guess in [secret.sequence_1,secret.sequence_2, secret.sequence_3, secret.sequence_4,secret.sequence_5]:
        print("You got the secret pin correct")
        light(State.CORRECT)
        guess.clear()
    else:
        print("Better luck next time")
        light(State.INCORRECT)
        guess.clear()

##### Initialize Application #####

print("Enter the secret Pin")

while True:
    scankeys()

    # if len(guess) == 0:
    #     light(State.ACTIVE)