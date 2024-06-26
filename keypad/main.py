# Matrix Keypad

# Original creator and code source
# NerdCave - https://www.youtube.com/channel/UCxxs1zIA4cDEBZAHIJ80NVg - Subscribe if you found this helpful.
# Github - https://github.com/Guitarman9119

from machine import Pin
from utime import sleep
from secret import sequences

# utility pin on off functions
def turn_on(pin): pin.value(1)
def turn_off(pin): pin.value(0)

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

# Loop to assign GPIO pins and setup input and outputs
for pin in range(0,4):
    row_pins.append(Pin(keypad_rows[pin], Pin.OUT))
    turn_on(row_pins[pin])
    col_pins.append(Pin(keypad_columns[pin], Pin.IN, Pin.PULL_DOWN))
    turn_off(col_pins[pin])

# Keys entered by the user
guess = []

# When Pico turns on run opening light sequence
program_stating = True

# Setup led pins to be an output
led_green = Pin(15, Pin.OUT, Pin.PULL_UP)
led_clear = Pin(13, Pin.OUT, Pin.PULL_UP)
led_red   = Pin(11, Pin.OUT, Pin.PULL_UP)

# Setup and initialize state object
class States:
    START     = 'start'
    ACTIVE    = 'active'
    INACTIVE    = 'inactive'
    CORRECT   = 'correct'
    INCORRECT = 'incorrect'
State = States()

#### Light State ####

def light_dance():
    leds = [led_green, led_clear, led_red]

    for led in leds:
        turn_on(led)
        sleep(0.3)
        turn_off(led)

    turn_on(led_clear)
    sleep(0.3)
    turn_off(led_clear)

    for led in leds:
        turn_on(led)
        sleep(0.3)
        turn_off(led)

    for led in reversed(leds[:-1]):
        turn_on(led)
        sleep(0.3)
        turn_off(led)

def light_start():
    light_dance()

    global program_stating
    program_stating = False

def light_inactive():
    turn_on(led_clear)

def light_active():
    turn_off(led_clear)
    sleep(0.2)
    light_inactive()

def light_correct():
    turn_off(led_clear)
    light_dance()
    turn_on(led_green)
    sleep(3)
    turn_off(led_green)

def light_incorrect():
    turn_off(led_clear)
    light_dance()
    turn_on(led_clear)
    sleep(0.3)
    turn_off(led_clear)
    turn_on(led_red)
    sleep(3)
    turn_off(led_red)

def light(state):
    if state == State.START: light_start()
    if state ==  State.ACTIVE: light_active()
    if state ==  State.INACTIVE: light_inactive()
    if state ==  State.CORRECT: light_correct()
    if state ==  State.INCORRECT: light_incorrect()

##### To check Pin #####

def checkPin(guess):
    print(guess)

    if guess in sequences:
        print("You have entered the correct pin number")
        light(State.CORRECT)
        guess.clear()
    else:
        print("Better luck next time")
        light(State.INCORRECT)
        guess.clear()

#### Scan keys #####
    
def scan_keys():
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
                    light(State.ACTIVE)
                    checkPin(guess)

                if key_press == 'CLR':
                    light(State.ACTIVE)
                    guess.clear()
                    
        row_pins[row].low()

##### Initialize Application #####

print("Enter the secret Pin")

try:
    while True:
        if program_stating == True: light(State.START)
        if len(guess) == 0: light(State.INACTIVE)
        scan_keys()

except KeyboardInterrupt:
    turn_off(led_clear)
    print('Program terminated')