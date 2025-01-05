# photobooth

Configuration photobooth à un seul RPi (pas d'affichage à la volée des photos prises via un second écran)

## 1/ Préparation :
$ sudo apt-get update
$ sudo apt-get dist-upgrade

Installation de l'économiseur d'écran (pour éviter la veille de l'écran)
$ sudo apt-get install xscreensaver

en mode graphique, aller dans Modes d'affichage et choisir le mode "Désactiver l'économiseur d'écran"

Librairies python :
$ sudo apt-get install python-picamera
$ sudo apt-get install python-RPi.gpio python3-RPi.gpio

## 2/ Câblage des leds et bouton sur le RPi
Fil rouge : led rouge (BCM 4)
Fil bleu : led verte (BCM 22)
Fil jaune : bouton (BCM 17)
Fil gris : masse

x			x
x			x
x			fil gris
rouge (4)	x
x			x
jaune (17)	x
x			x
bleu (22)	x
x			x
x			x
x			x
...h	

## 4/ Post-traitement des images
Il s'agit de refléter (horizontalement) toutes les images du répertoire
Installer imagemagick
--> se placer dans le répertoire concerné (# cd...)
$ mogrify -flop *.jpg

Remarque sur le post-traitement : si les images sont dans plusieurs répertoires, il est plus pratique de les regrouper dans un unique dossier.
On les renomme d'après le nom du répertoire
(nécessite l'installation préalable de rename : # sudo apt-get install rename)
# rename 's/^/jour-heure/' *
# mv * ../toutes_les_images

Eventuellement : créer une archive
# sudo apt-get install zip unzip
# cd photobooth/img
# zip -r images_evenement toutes_les_images


Remarque : Réglage picamera
Options de balance des blancs
'off'
'auto'
'sunlight'
'cloudy'
'shade'
'tungsten'
'fluorescent'
'incandescent'
'flash'
'horizon'
