#!/usr/bin/python

import sys
import csv
import cv2
import time
import screeninfo
from pynput import keyboard

VIDEO_PATH = "../testing_videos/"
CSV_PATH = "../result_files/"
CSV_NAME = "result_datasheet"
VIDEOS = ["1B1H.m4v", "1B1L.m4v", "1B2H.m4v", "1B2L.m4v", "1B3H.m4v", "1B3L.m4v", "1C1H.m4v", "1C1L.m4v", "1C2H.m4v", "1C2L.m4v", "1C3H.m4v", "1C3L.m4v", "2B1H.m4v", "2B1L.m4v", "2B2H.m4v", "2B2L.m4v", "2B3H.m4v", "2B3L.m4v", "2C1H.m4v", "2C1L.m4v", "2C2H.m4v", "2C2L.m4v", "2C3H.m4v", "2C3L.m4v", "3B1H.m4v", "3B1L.m4v", "3B2H.m4v", "3B2L.m4v", "3B3H.m4v", "3B3L.m4v", "3C1H.m4v", "3C1L.m4v", "3C2H.m4v", "3C2L.m4v", "3C3H.m4v", "3C3L.m4v", "4B1H.m4v", "4B1L.m4v", "4B2H.m4v", "4B2L.m4v", "4B3H.m4v", "4B3L.m4v", "4C1H.m4v", "4C1L.m4v", "4C2H.m4v", "4C2L.m4v", "4C3H.m4v", "4C3L.m4v"]

# Find the tested_videos
tested_videos = sys.argv[1:5]
try:
    iVideos = [VIDEOS.index(i) for i in tested_videos]
except ValueError:
    print("Invalid name of tested_videos.")

# Open the file
f = open(CSV_PATH+CSV_NAME,'a')#time.strftime("%d-%m_%H:%M"), 'w')
reader = csv.reader(f)
writer = csv.writer(f)

#Screen parameters
screen_id = 0
screen = screeninfo.get_monitors()[screen_id]
width, height = screen.width, screen.height
window_name = 'projector'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)


# Time variables
starting_times = []
events_time = []



def on_press(key):
    if key == keyboard.Key.space :
        events_time.append(time.time())
        global space_pressed
        space_pressed = True

    return 0

listener = keyboard.Listener(on_press=on_press)
listener.start()

for tested_video in tested_videos :
    space_pressed = False
    cap = cv2.VideoCapture(VIDEO_PATH + tested_video) # Encapsulation de la tested_video dans une classe dediee
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Determination des fps

    if cap.isOpened() == False:
        print("Error File Not Found")

    starting_times.append(time.time() + 1/fps)

    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True and space_pressed == False:


            time.sleep(1.0 / fps)  # Lit l'image a vitesse humaine prescrite par la variable "fps"

            cv2.imshow(window_name, frame)  # Affiche l'image dans uen nouvelle fenetre

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Quitte lors de l'appuie sur q
                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    raw_input("Press Enter to continue...")

corrected_time_event=[]
for i,t in enumerate(events_time) :
    corrected_time_event.append(t - starting_times[i])

row = [time.strftime("%d-%m_%H:%M")]
row =append( [0] * len(VIDEOS))

for i, t in enumerate(corrected_time_event):
    row[iVideos[i]] = t


# write a row to the csv file
writer.writerow(row)

# close the file
f.close()

listener.stop()