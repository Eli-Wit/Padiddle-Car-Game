from rpi_lcd import LCD
from datetime import datetime
import time
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Player 1 Button (Red)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Player 2 Button (Blue)

# Setup LEDs
GPIO.setup(17, GPIO.OUT)  # White LED (Always ON)
GPIO.setup(27, GPIO.OUT)  # Blue LED
GPIO.setup(22, GPIO.OUT)  # Red LED

# Player scores
player_one_score = 0
player_two_score = 0 
lcd = LCD(address=0x27)

# Turn ON White LED to indicate power is on
GPIO.output(17, GPIO.LOW)

def startup():
    lcd.clear()
    lcd.text('!!  Padiddle  !!', 1)
    for _ in range(4):
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.1)
    time.sleep(3)
    lcd_display('player scored')

def flicker_led_tie():
    for _ in range(4):
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.1)

def flicker_led_win(led):
    for _ in range(4):
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.15)
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.1)

def lcd_display(protocol):
    match protocol:
        case 'player scored':
            global player_one_score, player_two_score
            padding = ''
            line_1 = '<Red       Blue>'
            line_2 = ' ' + str(player_one_score) + padding + str(player_two_score) + ' '
            while len(line_2) < 16:
                padding += ' '
                line_2 = ' ' + str(player_one_score) + padding + str(player_two_score) + ' '
        case 'tie':
            line_1 = '      TIE'
            line_2 = ''
        case 'reset':
            line_1 = '  Scores Reset'
            line_2 = ''
        case 'shutdown':
            line_1 = ' Shutting  Down'
            line_2 = ''
    lcd.text(line_1, 1)
    lcd.text(line_2, 2)

def button_one_pressed(channel):
    global player_one_score
    if GPIO.input(21) == GPIO.HIGH and GPIO.input(20) == GPIO.LOW:
        player_one_score += 1
        lcd_display('player scored')
        flicker_led_win(22)  # Red LED
    elif GPIO.input(21) == GPIO.HIGH and GPIO.input(20) == GPIO.HIGH:
        check_for_reset_shutdown()
    lcd_display('player scored')

def button_two_pressed(channel):
    global player_two_score
    if GPIO.input(20) == GPIO.HIGH and GPIO.input(21) == GPIO.LOW:
        player_two_score += 1
        lcd_display('player scored')
        flicker_led_win(27)  # Blue LED
    elif GPIO.input(20) == GPIO.HIGH and GPIO.input(21) == GPIO.HIGH:
        check_for_reset_shutdown()
    lcd_display('player scored')

def check_for_reset_shutdown():
    global player_one_score, player_two_score
    reset = False
    shutdown = False
    start_time = time.time()
    
    while GPIO.input(21) == GPIO.HIGH and GPIO.input(20) == GPIO.HIGH:
        
        if (time.time() - start_time) >= 5:
            shutdown = True
            lcd_display('shutdown')
            os.system("sudo shutdown -h now")
            GPIO.output(17, GPIO.HIGH)  # White LED OFF after shutdown
            
        while (2 <= (time.time() - start_time) < 5) and (GPIO.input(21) == GPIO.HIGH and GPIO.input(20) == GPIO.HIGH):
            reset = True
            lcd_display('reset')
            player_one_score = 0
            player_two_score = 0
        time.sleep(0.1)

# Setup event detection
GPIO.add_event_detect(21, GPIO.BOTH, callback=button_one_pressed, bouncetime=50)
GPIO.add_event_detect(20, GPIO.BOTH, callback=button_two_pressed, bouncetime=50)

startup()

# Main loop to display scores
while True:
    time.sleep(1)

