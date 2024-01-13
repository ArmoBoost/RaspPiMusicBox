#!/usr/bin/env python
import os
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pygame
from time import sleep, time
from gpiozero import PWMLED, Button
import threading
#MUSIC BOX (VERSION 1.0)

#sets current working directory. So that pi can see the music files
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)


# Pin numbers for Buttons and LEDs
BUTTON_PIN1 = 21
LED_PIN1 = 26

BUTTON_PIN2 = 20
LED_PIN2 = 16

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN1, GPIO.OUT)

button2 = Button(BUTTON_PIN2)
led2 = PWMLED(LED_PIN2)
button1 = Button(BUTTON_PIN1)
led1 = PWMLED(LED_PIN1)

DEBOUNCE_TIME = 0.5 #Button debounce time

status1 = True #Pause Status
status2 = True #Playlist Status
last_press_time1 = 0
last_press_time2 = 0
led1.on()


def is_pause():
    global status1, last_press_time1
    current_time = time()
    if current_time - last_press_time1 > DEBOUNCE_TIME:
        if status1 and pygame.mixer.music.get_busy():
            led1.pulse()
            pygame.mixer.music.pause()
            print("Pause")
        else:
            led1.on()
            pygame.mixer.music.unpause()
            print("Unpause")
        status1 = not status1
        last_press_time1 = current_time


def is_playlist():
    global status2, last_press_time2,status1
    current_time = time()
    if button2.is_pressed and (current_time - last_press_time2 > DEBOUNCE_TIME):
        if status2:
            status1=True
            led1.on()
            led2.on()
            play_mp3("playlistSong.mp3")
            print("YES")
        else:
            led2.off()
            print("NO")
            restart_script()  # Restart the script just in case something goes wrong since this is headless
        status2 = not status2
        last_press_time2 = current_time

def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def play_mp3(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    sleep(1.5)


def rfid_thread():
    global status2, status1
    reader = SimpleMFRC522()
    try:
        while True:
            print("Waiting for you to scan an RFID sticker/card")
            id = reader.read()[0]
            print("The ID for this card is:", id)
            status1=True
            led1.on()
            status2=True
            led2.off()
            # Check if the ID exists in the MP3_FILE_MAPPING
            if id in MP3_FILE_MAPPING:
                file_path = MP3_FILE_MAPPING[id]
                print(f"Playing {file_path}")
                play_mp3(file_path)
            else:
                print(f"No MP3 file found for ID {id}")

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


# Initialize Pygame
pygame.init()

# Define the paths to mp3 files
MP3_FILE_MAPPING = {
    902705803771: "Lonely.mp3",
    286596035069: "LastOfUs.mp3",
    146304692531: "IGotLove.mp3",
    560517378306: "YoungBeautiful.mp3",
    9369383208: "RedBone.mp3",
    287116194207: "Mambo.mp3",
    834758209951: "YouDaOne.mp3",
    903947252128: "Belle.mp3",
    764713136571: "Russian.mp3",
    1040161141186: "BYMoveMe.mp3",
    491949289983: "Fairytale.mp3",
    627727364531: "MissIndependent.mp3",
    492972700082: "WinePonYou.mp3",
    492754465229: "NightTime.mp3",
    490137416042: "Nathalie.mp3",
    283576070470: "StereoLove.mp3",
    834204234235: "Calabria.mp3",
    558554706315: "MeAndJones.mp3",
    217943667081: "ManDown.mp3",
    216601555288: "FlashingLights.mp3",
    766726533425: "LoveOnBrain.mp3",
    10241536352: "DieForU.mp3",
    631082348924: "Beetlejuice.mp3",
    627676967345: "Stranger.mp3",
    630881350005: "BeWithoutYou.mp3",
    422827094292: "TeenageFantasy.mp3",
    148049785183: "RUDEYouth.mp3",
    347708265654: "StudyMusic.mp3",
    72665815450: "OneYear.mp3",

    # Add more mappings as needed
}

try:
    # Start the RFID thread
    rfid_thread = threading.Thread(target=rfid_thread)
    rfid_thread.start()

    # Set up the button callback
    button1.when_pressed = is_pause
    button2.when_pressed = is_playlist
    # Main loop for other tasks (if any)
    while True:
        pygame.mixer.music.set_volume(1.0)
        # Your main loop code here
        sleep(1)

except KeyboardInterrupt:
    pass
finally:
    pygame.mixer.music.stop()  # Stop any playing music
    rfid_thread.join()  # Wait for the RFID thread to finish
    GPIO.cleanup()

