from tkinter import *

def deplacement(caneva, fenetre, objet, x, y, dx, dy, rayon, largeur, hauteur) :

    if x + rayon + dx > largeur :
        x = 2 * (largeur - rayon) - x
        dx = -dx

    if x - rayon + dx  < 0 :
        x = 2*rayon - x
        dx = -dx

    if y + rayon + dy > hauteur :
        y = 2 * (hauteur - rayon) - y
        dy = -dy

    if y - rayon + dy < 0 :
        y = 2 * rayon - y  
        dy = -dy

    x = x+dx
    y = y+dy

    caneva.coords(objet, x-rayon, y-rayon, x+rayon, y+rayon)
    fenetre.after(20, deplacement, caneva, fenetre, objet, x, y, dx, dy, rayon, largeur, hauteur)
import jeu

partie = jeu.Jeu()

#test
"""partie.AjouterPoints(20)
partie.PerdreVie()
partie.PerdreVie()"""

partie.lancer()

