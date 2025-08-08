"""Wack a Mole Game"""

# Imports:
import machine
import time
import random

""" Set Up """
# Points:
pts = 0
# Variable for the timer:
start_of_game = time.ticks_ms()
# Variables, to be initialized later:
BUT_state = None
LED_state = None
lastLEDchange = None
timeLength_forLEDchange = None
rangeForlengthLEDchange = None
divider_forLengthLEDchange = None

# RGB LED and indicator LED:
ledR = machine.PWM(machine.Pin(4), 5000)
ledG = machine.PWM(machine.Pin(17), 5000)
ledB = machine.PWM(machine.Pin(16), 5000)
RGBtup = (ledR, ledG, ledB)
colors = {
    "red": (65535, 0, 0),
    "green": (0, 65535, 0),
    "blue": (0, 0, 65535),
    "orange": (65535, 35000, 0),
    "yellow": (65535, 65535, 0),
    "cyan": (0, 65535, 65535),
    "none": (0, 0, 0),
}

led_indicator = machine.Pin(2, machine.Pin.OUT)

# LED's:
led0 = machine.Pin(14, machine.Pin.OUT)
led1 = machine.Pin(12, machine.Pin.OUT)
led2 = machine.Pin(13, machine.Pin.OUT)
led3 = machine.Pin(5, machine.Pin.OUT)
led4 = machine.Pin(21, machine.Pin.OUT)
led5 = machine.Pin(23, machine.Pin.OUT)
led6 = machine.Pin(19, machine.Pin.OUT)
led7 = machine.Pin(18, machine.Pin.OUT)
led8 = machine.Pin(22, machine.Pin.OUT)
LEDtup = (led0, led1, led2, led3, led4, led5, led6, led7, led8)

# Buttons:
but_start_game = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
but0 = machine.Pin(36, machine.Pin.IN, machine.Pin.PULL_UP)
but1 = machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_UP)
but2 = machine.Pin(35, machine.Pin.IN, machine.Pin.PULL_UP)
but3 = machine.Pin(39, machine.Pin.IN, machine.Pin.PULL_UP)
but4 = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)
but5 = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP)
but6 = machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_UP)
but7 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
but8 = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

# Turn everything off:
for i in LEDtup:
    i.off()
ledR.duty_u16(0)
ledG.duty_u16(0)
ledB.duty_u16(0)

"""Functions and other stuff"""
# To set a color:
def set_RGB(color):
    for colorLED in RGBtup:
        colorLED.duty_u16(colors[color][RGBtup.index(colorLED)])

# 3... 2... 1... GO!
def RGB_321_go():
    set_RGB("red")
    time.sleep(0.75)
    set_RGB("yellow")
    time.sleep(0.75)
    set_RGB("green")
    time.sleep(0.75)
    set_RGB("none")

# Timer function:
def timer():
    now = time.ticks_ms()
    elapsed_time = time.ticks_diff(now, start_of_game)
    if pts < int(elapsed_time / 1000) - 3:
        return("game over")

# LED change:
def ledChange(pressIndex=None):
    global timeLength_forLEDchange, lastLEDchange, LED_state, rangeForlengthLEDchange, divider_forLengthLEDchange
    now = time.ticks_ms()
    elasped = time.ticks_diff(now,lastLEDchange)
    if elasped >= timeLength_forLEDchange or succeed: # If it's time to change
        for index, state in enumerate(LED_state):
            if state:
                LED_state[index] = 0
                LEDtup[index].off()
        LEDto_turnOn = random.choice(LEDtup)
        LEDto_turnOn.on()
        LED_state[LEDtup.index(LEDto_turnOn)] = 1
        lastLEDchange = time.ticks_ms()
        timeLength_forLEDchange = int(random.uniform(rangeForlengthLEDchange["start"], rangeForlengthLEDchange["stop"]))
        if rangeForlengthLEDchange["start"] < (divider_forLengthLEDchange - 1) * 6500:
            divider_forLengthLEDchange = 1 + ((divider_forLengthLEDchange - 1) * 0.3)
        rangeForlengthLEDchange["start"] /= divider_forLengthLEDchange
        rangeForlengthLEDchange["stop"] /= divider_forLengthLEDchange

# If you made a mistake:
def mistake(timeMistakeMade, reason):
    set_RGB("red")
    timeWait = 1000 if reason else 2000
    while time.ticks_diff(time.ticks_ms(), timeMistakeMade) < timeWait:
        if timer():
            break
    set_RGB("none")

# Button things:
def butStuff():
    global BUT_state, succeed, pts
    BUT_state = [but0.value(), but1.value(), but2.value(), but3.value(), but4.value(), but5.value(), but6.value(), but7.value(), but8.value()]
    now = time.ticks_ms()
    if sum(BUT_state) != 9:
        if sum(BUT_state) < 8:
            mistake(now, False)
            succeed = False
        elif sum(BUT_state) == 8:
            if BUT_state.index(0) == LED_state.index(1):
                set_RGB("cyan")
                pts += 1
                succeed = True
            else:
                mistake(now, True)
        while sum(BUT_state) != 9:
            pass
        set_RGB("none")
        
    else:
        succeed = False

# The game:
def game(pin):
    for i in LEDtup:
        i.off()
    ledR.duty_u16(0)
    ledG.duty_u16(0)
    ledB.duty_u16(0)
    led_indicator.on()
    global start_of_game, BUT_state, LED_state, lastLEDchange, timeLength_forLEDchange, rangeForlengthLEDchange, divider_forLengthLEDchange, succeed, pts
    pts = 0
    divider_forLengthLEDchange = 1.1
    lastLEDchange = 0
    timeLength_forLEDchange = 0
    rangeForlengthLEDchange = {
        "start": 1000,
        "stop": 5000
    }
    BUT_state = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    LED_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    succeed = False
    RGB_321_go()
    start_of_game = time.ticks_ms()
    while True:
        timer_result = timer()
        if timer_result == "game over":
            break
        ledChange()
        butStuff()
    led_indicator.off()
    print(f"Game Over!\nPoints: {pts}")

"""Finally, the game code"""
but_start_game.irq(trigger=machine.Pin.IRQ_FALLING, handler=game)
