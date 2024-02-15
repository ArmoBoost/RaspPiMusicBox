# RaspPi MusicBox
This is my first project using a RaspPi4. So I decided to make a music box that uses RFID stickers to play music. This is heavily inspired by [talaexe](https://talaexe.com/moderndayrecordplayer). I highly recommend checking her website where she does the same thing but by connecting the Pi to Spotify API instead of using local MP3 files. Follow her steps up to the point where she starts integrating the Spotify API, the rest you can find here. 

  __DISCLAIMER__  
Please keep in mind, this is my first time working on a project with Python and a Unix-based OS. 

## Installation Parts
1. Raspberry Pi4 and all the essentials (power cable, MicroSD, etc...)
2. RFID Scanner
3. RFID Stickers
4. Buttons (Push ones, nothing that switches or stays down when pressed)
5. LEDS
6. Resistors for LEDs
7. Speakers
8. Soldering Iron (for RFID scanner, buttons, and LEDs)
9. Something to store everything in (Wooden Box for example)

## Pi Setup
After following [talaexe's](https://talaexe.com/moderndayrecordplayer) steps, you might find yourself in an issue with pip3. Use the following but be warned, this might break your system if you don't know what you're doing. 
```bash
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
```

## How It Works
Here is a quick rundown of how the box works. There are 2 LEDs and 3 Buttons attached to the Pi's GPIO pins. LED1 stays lit up when the script is running and if BUTTON1 is pressed, the music will pause and LED1 will start to pulse. BUTTON2 has two features. Since this will be a headless unit and a gift, I wanted to make it as user-friendly as possible and prevent the need for an SSH. So when pressed, BUTTON2 causes LED2 to glow and will play an MP3 file called playlist which has all the songs combined into one (yes I know there is a better way to do this, but I was running into issues with pausing and I didn't have any more time to fix it...and my brain started to hurt). If pressed again, the script will restart (stopping the playlist AND in case of an error, restarting the script). BUTTON3 uses Pin 5 of the Pi's GPIO pins to turn the Pi On and Off.


## Code
### musicBox.py and power button
The code is pretty simple. Just change the RFID numbers to the ones you have and the song names to the ones you downloaded. You can also change the pins to whichever one you want. BUT pin 5 must be used for the on/off button. I will add [Howchoo's](https://github.com/Howchoo/pi-power-button) GitHub repo for further power button explanation and installation. It's fairly simple.  
### Start at boot
To get the script to start when it boots up, we need to do the following
```bash
sudo crontab -e
```
There will be an option if this is the first time opening crontab, pick option 1 (nano). Go to the very bottom of that file and type @reboot <Your Command>&. Here's an example of mine:
```bash
@reboot python3 /home/pi/Desktop/musicBox.py &
```
If this is giving you issues, create a .sh file and run @reboot that file in your crontab
### Reboot Sound Not Coming Out 
Last little thing, I did run into a pretty annoying issue that took me days to figure out. It has to do with PulseAudio (the sound server used for audio processing). I think the issue is that PulseAudio would not be ready before the script starts running at reboot, so no audio comes through even though it does when you run it in the IDE. In my case, audio was coming out of my HDMI port, but not the AUX. To fix this I had to create a systemd service file:
```bash
[Unit]
Description=PulseAudio Daemon
[Install]
WantedBy=multi-user.target
[Service]
Type=simple
PrivateTmp=true
ExecStart=/usr/bin/pulseaudio --system --realtime --disallow-exit --no-cpu-limit
```
Then modify /etc/pulse/system.pa. Add auth-anonymous=1 to the line that starts with load-module module-native-protocol-unix

So you should have 'load-module module-native-protocol-unix auth-anonymous=1' as the final edited line.


## Your Ready To Play Music!
Thats it! Now you can play music using RFID stickers. Get creative and put the components into something so that it looks nicer. I hope this little project was helpful!
Pictures of my set up coming soon!
