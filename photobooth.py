########################################################################
# Module photobooth pour RPi (PiCamera)
#
# Les images sont enregistrees en miroir. Pour les retourner
# utiliser imagemagick et la commande :
# mogrify -flop *jpg
#
########################################################################

from picamera2 import Picamera2, Preview
from libcamera import Transform
from RPi import GPIO
#from tkinter import filedialog
import tkinter as tk
import time
import os
from PIL import Image, ImageTk

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from picamera2.previews.qt import QGlPicamera2

#Dialogue selection du répertoire

root_img_dir = "/home/pi/Documents/photobooth/img/" + time.strftime("%Y-%m-%d_%Hh%M")
os.makedirs(root_img_dir)


def capture_image(camera, preview_config, still_config, root_img_dir, frame):
    camera.stop()
    camera.configure(still_config)
    camera.start()
    dte_img = time.strftime("%Y-%m-%d_%Hh%M")
    filename = f"{root_img_dir}/{dte_img}_image{frame:03}.jpg"
    #filename = '%(dir)s/%(dte)s_image%(frm)03d.jpg' % {"dir": root.directory, "dte": time.strftime("%Y-%m-%d_%Hh%M"), "frm": frame}
    camera.capture_file(filename)
    print(f"Image capturée : {filename}")
    camera.stop()
    #camera.stop_preview()
    
    #display_image(camera, filename, 2)
        
    camera.configure(preview_config)
    camera.start()
    
def display_image(camera, filename, duration):
    image = Image.open(filename)
    
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background = 'black')
    
    tk_image = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=tk_image, bg='black')
    label.pack(expand=True)
    
    root.after(int(duration * 1000), root.destroy)
    
    root.mainloop()

# Config GPIO
PHOTO_BUTTON = 17
PHOTO_BUTTON = 17
STOP_BUTTON = 18
RED_LED = 4
GREEN_LED = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTO_BUTTON, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(PHOTO_BUTTON, GPIO.RISING, bouncetime=500)

GPIO.setup(STOP_BUTTON, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(STOP_BUTTON, GPIO.RISING)

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# Config caméra
camera = Picamera2()
preview_config = camera.create_preview_configuration(main={"size": (640, 480)}, transform=Transform(vflip=1))
#preview_config = camera.create_preview_configuration(main={"size": (1920, 1080)}, transform=Transform(vflip=1))
#still_config = camera.create_still_configuration(main={"size": (1920, 1080)}, transform=Transform(hflip=1, vflip=1))
#still_config = camera.create_still_configuration(main={"size": (3840, 1920)}, transform=Transform(hflip=1, vflip=1))
still_config = camera.create_still_configuration(main={"size": (4608, 2592)}, transform=Transform(hflip=1, vflip=1))

# Démarrage caméra
camera.configure(preview_config)

# Créer l'application Qt
app = QApplication([])

# Créer la fenêtre de prévisualisation sans bordure
qpicamera2 = QGlPicamera2(camera, width=640, height=480, keep_ar=False)
qpicamera2.setWindowFlags(QtCore.Qt.FramelessWindowHint)
qpicamera2.showFullScreen()

#camera.start_preview(Preview.QTGL)
#camera.start_preview(Preview.DRM)
camera.start()

app.exec()

# Numérotation des photos
frame = 1

while True:

    GPIO.output(RED_LED, 0)
    GPIO.output(GREEN_LED, 1)
    
    # gestion de l'arrêt par appui sur le bouton dédié
    if GPIO.event_detected(STOP_BUTTON):
        camera.stop_preview()
        qpicamera2.close()
        camera.close()
        GPIO.cleanup()
        print("Photobooth interrompu")
        break

    if GPIO.event_detected(PHOTO_BUTTON):
        # lorsque le bouton est actionné, on fait clignoter la led rouge 3s
        GPIO.output(GREEN_LED, 0)
        i = 0
        while i < 2 :
            GPIO.output(RED_LED, 1)
            time.sleep(0.5)
            GPIO.output(RED_LED, 0)
            time.sleep(0.5)
            i += 1
        # puis 2 fois rapidement
        i = 0
        while i < 2 :
            GPIO.output(RED_LED, 1)
            time.sleep(0.1)
            GPIO.output(RED_LED, 0)
            time.sleep(0.1)
            i += 1
        
        # Led rouge allumée, on prend la photo
        GPIO.output(RED_LED, 1)
        capture_image(camera, preview_config, still_config, root_img_dir, frame)
        GPIO.output(RED_LED,0)
        
        #incrément du compteur d'images
        frame += 1
