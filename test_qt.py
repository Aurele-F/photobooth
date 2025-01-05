from picamera2 import Picamera2, Preview
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from picamera2.previews.qt import QGlPicamera2
import time

# Initialiser la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

# Créer l'application Qt
app = QApplication([])

# Créer la fenêtre de prévisualisation sans bordure
qpicamera2 = QGlPicamera2(picam2, width=800, height=600, keep_ar=False)
qpicamera2.setWindowFlags(QtCore.Qt.FramelessWindowHint)
qpicamera2.showFullScreen()

# Démarrer la caméra
picam2.start()

# Fermer la fenêtre après 5 secondes
QtCore.QTimer.singleShot(5000, qpicamera2.close)

# Exécuter l'application Qt
app.exec()