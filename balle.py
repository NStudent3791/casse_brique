import math
import random

class Balle:
    def __init__(self, canevas, fenetre, largeur, hauteur,raquette):
        self.canevas = canevas
        self.fenetre = fenetre

        # Dimensions du terrain
        self.largeur = largeur
        self.hauteur = hauteur
        self.raquette = raquette

        # Caractéristiques de la balle
        self.rayon = 15
        self.vitesse = 8
        self.vitesse_max = 12

        self.x = largeur / 2
        self.y = hauteur / 2

        angle = math.radians(random.uniform(225, 315))
        self.dx = self.vitesse * math.cos(angle)
        self.dy = self.vitesse * math.sin(angle)

        # Création du dessin sur le canevas
        self.identifiant = self.canevas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon, fill="red")

    def deplacer(self) :
        # Rebonds horizontaux
        if self.x + self.dx + self.rayon >= self.largeur:
            self.x = self.largeur - self.rayon
            self.dx = -abs(self.dx)

        elif self.x + self.dx - self.rayon <= 0:
            self.x = self.rayon
            self.dx = abs(self.dx)

        # Rebonds verticaux
        if self.y + self.dy + self.rayon >= self.hauteur:
            self.y = self.hauteur - self.rayon
            self.dy = -abs(self.dy)

        elif self.y + self.dy - self.rayon <= 0:
            self.y = self.rayon
            self.dy = abs(self.dy)
            
        # Collision avec les côtés de la raquette
        if (self.y + self.rayon > self.raquette.PosY and self.y - self.rayon < self.raquette.PosY + self.raquette.Hauteur):

            # Collision avec le côté gauche
            if (self.dx > 0 and self.x + self.rayon <= self.raquette.PosX and self.x + self.dx + self.rayon >= self.raquette.PosX):
                self.x = self.raquette.PosX - self.rayon
                self.dx = -abs(self.dx)

            # Collision avec le côté droit
            elif (self.dx < 0 and self.x - self.rayon >= self.raquette.PosX + self.raquette.Largeur and self.x + self.dx - self.rayon <= self.raquette.PosX + self.raquette.Largeur):
                self.x = self.raquette.PosX + self.raquette.Largeur + self.rayon
                self.dx = abs(self.dx)

        # Mise à jour de la position
        self.x += self.dx
        self.y += self.dy

        # Mise à jour du dessin
        self.canevas.coords(self.identifiant, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)
        
    def Accelerer(self):
        # augmente la vitesse de la balle de 1, sans changer sa direction
        if self.vitesse < self.vitesse_max:
            # dx et dy grandissent dans la meme proportion que la vitesse
            facteur = (self.vitesse + 1) / self.vitesse
            self.dx = self.dx * facteur
            self.dy = self.dy * facteur
            self.vitesse = self.vitesse + 1