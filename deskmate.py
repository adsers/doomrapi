import os
import pygame
import time
import requests
from datetime import datetime
from mpv import MPV

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((320, 240))  # Adjust for your display size
pygame.display.set_caption("Desk Mate UI")

# Fonts & Colors
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# MPV Player Setup
player = MPV()
player.volume = 50

# Button & Scroll Wheel Mapping (GPIO placeholders)
BUTTON_HOME = 17
BUTTON_ENTER = 27
BUTTON_EXIT = 22
SCROLL_NAV = 23
SCROLL_VOL = 24

# Setup GPIO (if using physical buttons)
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([BUTTON_HOME, BUTTON_ENTER, BUTTON_EXIT], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup([SCROLL_NAV, SCROLL_VOL], GPIO.IN)
except ImportError:
    print("Running in non-RPi mode")

# Fetch Weather Data
def get_weather():
    try:
        response = requests.get("https://wttr.in/?format=%C+%t", timeout=5)
        return response.text
    except:
        return "Weather: N/A"

# UI State
state = "home"
music_playlist = ["song1.mp3", "song2.mp3"]  # Add your songs here
current_song = 0

# Main Loop
running = True
while running:
    screen.fill(BLACK)
    
    # Get time & weather
    current_time = datetime.now().strftime("%H:%M:%S")
    weather = get_weather()
    
    # Display UI
    if state == "home":
        text = font.render(f"Time: {current_time}", True, WHITE)
        screen.blit(text, (50, 50))
        text = font.render(weather, True, WHITE)
        screen.blit(text, (50, 100))
    elif state == "music":
        text = font.render(f"Playing: {music_playlist[current_song]}", True, WHITE)
        screen.blit(text, (50, 50))
    
    pygame.display.flip()
    time.sleep(1)  # Refresh every second
    
    # Button Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # For debugging with keyboard
            if event.key == pygame.K_h:
                state = "home"
            elif event.key == pygame.K_m:
                state = "music"
                player.play(music_playlist[current_song])
            elif event.key == pygame.K_q:
                running = False
    
pygame.quit()
