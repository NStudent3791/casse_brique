import math
import random

class Balle:
    def __init__(self, canevas, fenetre, largeur, hauteur, raquette, vitesse_initiale=8):
        self.canevas = canevas
        self.fenetre = fenetre

        # Dimensions du terrain
        self.largeur = largeur
        self.hauteur = hauteur
        self.raquette = raquette

        # Caractéristiques de la balle
        self.rayon = 15
        self.vitesse = vitesse_initiale
        self.vitesse_max = vitesse_initiale + 4

        self.x = largeur / 2
        self.y = hauteur / 2

        # Choisit aléatoirement une direction
        if random.choice([True, False]):
            angle = random.uniform(210, 240)
        else:
            angle = random.uniform(300, 330)

        # Convertit l'angle en radians
        angle = math.radians(angle)

        # Calcule les composantes de la vitesse
        self.dx = self.vitesse * math.cos(angle)
        self.dy = self.vitesse * math.sin(angle)

        # Création du dessin sur le canevas
        self.identifiant = self.canevas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon, fill="#00E5FF")

    def deplacer(self) :
        # Rebonds horizontaux
        if self.x + self.dx + self.rayon >= self.largeur:
            self.x = self.largeur - self.rayon
            self.dx = -abs(self.dx)

        elif self.x + self.dx - self.rayon <= 0:
            self.x = self.rayon
            self.dx = abs(self.dx)

        # Rebonds en haut

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