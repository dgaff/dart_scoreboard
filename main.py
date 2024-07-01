# (c) 2024 Douglas Gaff
# All Rights Reserved

import time
import board
import digitalio
from adafruit_max7219 import matrices
from adafruit_debouncer import Debouncer
import adafruit_tlc59711

# Setup the SPI bus.
spi = board.SPI() # defaults to SCK and MOSI pins

# Setup the display controller chip selects
display_cs = [
    digitalio.DigitalInOut(board.D0),
    digitalio.DigitalInOut(board.D1),
    digitalio.DigitalInOut(board.D2),
    digitalio.DigitalInOut(board.D3),
    digitalio.DigitalInOut(board.D4),
    digitalio.DigitalInOut(board.D5),
    digitalio.DigitalInOut(board.D7)
]

# Setup the button LED controller chip select
score_button_LED_cs = digitalio.DigitalInOut(board.A4)

# Button inputs
score_button_pins = [
    digitalio.DigitalInOut(board.D9),
    digitalio.DigitalInOut(board.D10),
    digitalio.DigitalInOut(board.D11),
    digitalio.DigitalInOut(board.D12),
    digitalio.DigitalInOut(board.D13),
    digitalio.DigitalInOut(board.A2),
    digitalio.DigitalInOut(board.A3)
]

for pin in score_button_pins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.DOWN

score_buttons = []
for pin in score_button_pins:
    score_buttons.append(Debouncer(pin, interval = 0.05))

# TX and RX so the two boards can talk to each other. Just used as high and low right now
# for indicating the end of the game.
serial_pins = [
    digitalio.DigitalInOut(board.A0),
    digitalio.DigitalInOut(board.A1)
]

TX = 0
RX = 1
serial_pins[TX].direction = digitalio.Direction.OUTPUT
serial_pins[RX].direction = digitalio.Direction.INPUT
serial_pins[RX].pull = digitalio.Pull.DOWN

# Score button LEDS
leds = adafruit_tlc59711.TLC59711(spi)

score_button_led_channel = [
    9,   # R0 silkscreen
    10,  # G0 silkscreen
    11,  # B0 silkscreen
    6,   # R1 silkscreen
    7,   # G1 silkscreen
    8,   # B1 silkscreen
    3,   # R2 silkscreen
    4,   # G2 silkscreen
    5,   # B2 silkscreen
    0,   # R3 silkscreen
    1,   # G3 silkscreen
    2    # B3 silkscreen
]

# Game reset button
reset_button_pin = digitalio.DigitalInOut(board.A5)
reset_button_pin.direction = digitalio.Direction.INPUT
reset_button_pin.pull = digitalio.Pull.DOWN
reset_button = Debouncer(reset_button_pin, interval = 0.05)

# Setup the displays
# TODO Figure out the correct rotation after I hook things up.
# Note: for some reason I can't pass rotation to the Matrix8x8 constructor. So I'm using CustomMatrix.
# matrices.Matrix8x8(spi, display_cs[0])

display_matrix = [
    # matrices.Matrix8x8(spi, display_cs[0]),  # this is how you declare if you don't need rotation.
    # matrices.Matrix8x8(spi, display_cs[1]),
    # matrices.Matrix8x8(spi, display_cs[2]),
    # matrices.Matrix8x8(spi, display_cs[3]),
    # matrices.Matrix8x8(spi, display_cs[4]),
    # matrices.Matrix8x8(spi, display_cs[5]),
    # matrices.Matrix8x8(spi, display_cs[6])
    matrices.CustomMatrix(spi, display_cs[0],8,8,rotation=3),
    matrices.CustomMatrix(spi, display_cs[1],8,8,rotation=3),
    matrices.CustomMatrix(spi, display_cs[2],8,8,rotation=3),
    matrices.CustomMatrix(spi, display_cs[3],8,8,rotation=3),
    matrices.CustomMatrix(spi, display_cs[4],8,8,rotation=3),
    matrices.CustomMatrix(spi, display_cs[5],8,8,rotation=3),
    matrices.CustomMatrix(spi, display_cs[6],8,8,rotation=3)
]

# Set the display brightness
# TODO I think the max brightness is current limited. Need to measure before I set the default.
for matrix in display_matrix:
    matrix.brightness(10)

# Bitmaps for 8x8 displays

twenty = [[0, 1, 1, 0, 0, 1, 1, 0],
 [1, 0, 0, 1, 1, 0, 0, 1],
 [0, 0, 0, 1, 1, 0, 0, 1],
 [0, 0, 0, 1, 1, 0, 0, 1],
 [0, 1, 1, 0, 1, 0, 0, 1],
 [1, 0, 0, 0, 1, 0, 0, 1],
 [1, 0, 0, 0, 1, 0, 0, 1],
 [1, 1, 1, 1, 0, 1, 1, 0]]

nineteen = [[0, 1, 0, 0, 0, 1, 1, 0],
 [1, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 0, 1, 1, 1],
 [0, 1, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [1, 1, 1, 0, 0, 1, 1, 0]]

eighteen = [[0, 1, 0, 0, 0, 1, 1, 0],
 [1, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 0, 1, 1, 0],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [1, 1, 1, 0, 0, 1, 1, 0]]

seventeen = [[0, 1, 0, 0, 1, 1, 1, 1],
 [1, 1, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [0, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 0, 0, 0, 1, 0, 0],
 [1, 1, 1, 0, 0, 1, 0, 0]]

sixteen = [[0, 1, 0, 0, 0, 1, 1, 0],
 [1, 1, 0, 0, 1, 0, 0, 0],
 [0, 1, 0, 0, 1, 0, 0, 0],
 [0, 1, 0, 0, 0, 1, 1, 0],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [0, 1, 0, 0, 1, 0, 0, 1],
 [1, 1, 1, 0, 0, 1, 1, 0]]

fifteen = [[0, 1, 0, 0, 1, 1, 1, 1],
 [1, 1, 0, 0, 1, 0, 0, 0],
 [0, 1, 0, 0, 1, 0, 0, 0],
 [0, 1, 0, 0, 0, 1, 1, 0],
 [0, 1, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 0, 1, 1, 1, 0]]

bull = [[0, 0, 1, 1, 1, 1, 0, 0],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [1, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 0, 1, 1, 0, 0, 1],
 [1, 0, 0, 1, 1, 0, 0, 1],
 [1, 0, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [0, 0, 1, 1, 1, 1, 0, 0]]

single = [[1, 0, 0, 0, 0, 0, 0, 0],
 [0, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 0, 0, 0],
 [0, 0, 0, 0, 0, 1, 0, 0],
 [0, 0, 0, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 0, 0, 0, 1]]

double = [[1, 0, 0, 0, 0, 0, 0, 1],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [0, 0, 1, 0, 0, 1, 0, 0],
 [0, 0, 0, 1, 1, 0, 0, 0],
 [0, 0, 0, 1, 1, 0, 0, 0],
 [0, 0, 1, 0, 0, 1, 0, 0],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [1, 0, 0, 0, 0, 0, 0, 1]]

triple = [[1, 0, 1, 1, 1, 1, 0, 1],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [1, 0, 1, 0, 0, 1, 0, 1],
 [1, 0, 0, 1, 1, 0, 0, 1],
 [1, 0, 0, 1, 1, 0, 0, 1],
 [1, 0, 1, 0, 0, 1, 0, 1],
 [0, 1, 0, 0, 0, 0, 1, 0],
 [1, 0, 1, 1, 1, 1, 0, 1]]

# Testing sending the control code for the button LED controller to see if there's SPI bus interference.
# I have MOSI tied to each 8x8 controller and to the LED controller. But the LED controller doesn't
# have a chip select. It just looks for a control sequence. I managed to convince myself on the logic
# analyzer that the control sequence wasn't possible when sending 8x8 commands, so there wasn't any
# danger of the button LED controller accidentally changing a button LED state.

# single = [[0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1]]

# double = [[0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1]]

# triple = [[0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 0, 1, 0, 1]]

score_displays = [ twenty, nineteen, eighteen, seventeen, sixteen, fifteen, bull ]

score_display_count = [ single, double, triple ]

score_count = [0, 0, 0, 0, 0, 0, 0]

# Used for blinking the game reset button
blink_timestamp_ns = 0
blink_brightness = 65535
blink_bright_down = True

# Helpful function for setting a score display.
def fill_matrix(score_display, matrix):
    for i_row, row in enumerate(score_display):
        for j_col, led_state in enumerate(row):
            matrix.pixel(j_col, i_row, led_state)

# Resets the game at power up and when user presses reset button.
def game_reset():
    # Turn off all the buttons
    for led_channel in score_button_led_channel:
        leds.set_channel(led_channel, 0)
    leds.show()

    # Turn off all LEDs
    for matrix in display_matrix:
        matrix.fill(False)
        matrix.show()

    # Pause
    time.sleep(0.5)

    # Turn on all the buttons
    for led_channel in score_button_led_channel:
        leds.set_channel(led_channel, 65535)
    leds.show()

    # Turn on all LEDs
    for matrix in display_matrix:
        matrix.fill(True)
        matrix.show()

    # Pause
    time.sleep(0.5)

    # Count up from Bull while gradually increasing score button brightness
    button_brightness = 0
    button_step = int(65535 / 28) # This is 7 score values x 4 brightness levels per score value
    for i_score, score in enumerate(reversed(score_displays)):
        for i, matrix in enumerate(display_matrix):
            fill_matrix(score, matrix)
            matrix.show()

        for j in range(0,4):
            button_brightness += button_step

            if button_brightness > (65535 - button_step): button_brightness = 65535 # Round up at the end
            for score_button in score_button_led_channel:
                leds.set_channel(score_button, button_brightness)
            leds.show()

            time.sleep(0.025)

    # Now set the scores to their correct values        
    time.sleep(0.3)
    for i, matrix in enumerate(display_matrix):
        leds.set_channel(score_button_led_channel[i], int(65535/3))
        leds.show()
        if i >= 0: # 20 is already displayed, so we can skip it.
            fill_matrix(score_displays[i], matrix)
            matrix.show()
            time.sleep(0.1)

    # Bring button lights back to full brightness
    time.sleep(0.3)
    for score_button in score_button_led_channel:
        leds.set_channel(score_button, 65535)
    leds.show()

    # These three blocks were animation experiments before I
    # settled on the final version.

    # This version just set displays back to 19, 18, 17, etc.
    # for i, matrix in enumerate(display_matrix):
    #     fill_matrix(score_displays[i], matrix)
    #     matrix.show()

    # This version counts down from 20
    # for i_score, score in enumerate(score_displays):
    #     for i, matrix in enumerate(display_matrix):
    #         if i >= i_score: 
    #             fill_matrix(score, matrix)
    #             matrix.show()
    #     time.sleep(0.4)

    # This version counts up from bull
    # for i_score, score in enumerate(reversed(score_displays)):
    #     for i, matrix in enumerate(reversed(display_matrix)):
    #         if i_score <= i: 
    #             fill_matrix(score, matrix)
    #             matrix.show()
    #     time.sleep(0.4)

    # Reset the score count.
    for i, score in enumerate(score_count):
        score_count[i] = 0

    # Reset the reset button blinker and game winning signal to
    # other board.
    blink_timestamp_ns = 0
    blink_brightness = 65535
    blink_bright_down = True
    serial_pins[TX].value = False

# Reset the game on power up.
game_reset()

# Test code for experimenting with display brightness.
# temp_bright = 10

# Main loop.
while True:
    # Scan the buttons
    for i, button in enumerate(score_buttons):
        # Update the button
        button.update()

        # Check for press
        # if button.value == True:
        # Check for button release
        if button.rose:
            # print("Button " + str(i) + " pressed")

            # Increment the score
            score_count[i] += 1
            if score_count[i] > 3: score_count[i] = 0

            # Check for whether to put button LED on or off
            if score_count[i] == 3:
                leds.set_channel(score_button_led_channel[i], 0)
                leds.show()
                # print("button LED off")
            else:
                leds.set_channel(score_button_led_channel[i], 65535)
                leds.show()
                # print("button LED on")

            # Mark the incremented score or reset to the default screen if count is back to zero.
            if score_count[i] == 0:
                for i_row, row in enumerate(score_displays[i]):
                    for j_col, led_state in enumerate(row):
                        display_matrix[i].pixel(j_col, i_row, led_state)
                display_matrix[i].show()
            else:
                for i_row, row in enumerate(score_display_count[score_count[i]-1]):
                    for j_col, led_state in enumerate(row):
                        display_matrix[i].pixel(j_col, i_row, led_state)
                display_matrix[i].show()

    # Alert other board if this is the end of game.
    if sum(score_count) == 21: serial_pins[TX].value = True
    else: serial_pins[TX].value = False

    # Blink the reset button if this in the end of game.
    # Note: the LED on the reset button is controlled by the board on the right, but we want to
    # use the same code on both boards. This code has no effect on the board on the left because
    # nothing is hooked to channel 7 on the LED controller.
    if sum(score_count) == 21 or serial_pins[RX].value:
        if time.monotonic_ns() > blink_timestamp_ns:
            # print("game over")

            if blink_bright_down:
                blink_brightness -= 1000
                if blink_brightness < 3000:
                    blink_brightness = 3000
                    blink_bright_down = False
            else:
                blink_brightness += 1000
                if blink_brightness > 65535:
                    blink_brightness = 65535
                    blink_bright_down = True

            leds.set_channel(score_button_led_channel[7], blink_brightness)
            leds.show()
            blink_timestamp_ns = time.monotonic_ns() + 15000000  # 15 ms
    # Game still going. This catches the case when someone clears a number and then un-clears it.
    elif blink_timestamp_ns != 0:
        blink_timestamp_ns = 0
        blink_brightness = 65535
        blink_bright_down = True
        leds.set_channel(score_button_led_channel[7], blink_brightness)
        leds.show()

    # Scan the reset button
    reset_button.update()
    if reset_button.rose:
        # print("reset pressed")
        game_reset()

    # test code for experimenting with brightness
    # temp_bright += 1
    # if temp_bright > 15: temp_bright = 0
    # print("bright " + str(temp_bright))
    # display_matrix[0].brightness(temp_bright)

# Test code to loop through all pixels on each 8x8 display
while False:
    # Turn on all LEDs
    for matrix in display_matrix:
        matrix.fill(True)
        matrix.show()

    # Turn on all the buttons
    for led_channel in score_button_led_channel:
        leds.set_channel(led_channel, 65535)
    leds.show()

    # Pause
    print("Heidi Ho there, neighbor")
    time.sleep(1.0)

    # Turn off all LEDs
    for matrix in display_matrix:
        matrix.fill(False)
        matrix.show()

    # Loop each display pixel by pixel to test addressing
    for i_row in range(0,8):
        for j_col in range (0,8):
            for matrix in display_matrix:
                matrix.pixel(j_col, i_row, 1)
                matrix.show()
            time.sleep(0.2)
            for matrix in display_matrix:
                matrix.pixel(j_col, i_row, 0)
                matrix.show()

# Test code to loop through all numbers and symbols on each 8x8 display
while False:

    time.sleep(0.1)

    matrix.fill(False)
    matrix.show()
    time.sleep(0.5)

    to_display = twenty

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = nineteen

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = eighteen

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = seventeen

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = sixteen

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = fifteen

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = bull

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = single

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = double

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)

    to_display = triple

    for i, row in enumerate(to_display):
        for j, col in enumerate(row):
            display_matrix[0].pixel(j, i, col)
    display_matrix[0].show()
    time.sleep(2.0)
