class Brique:
    def __init__(self, Canava, PosX, PosY , Largeur, Hauteur, Couleur):
        self.Canava = Canava
        # position et dimension d'un brique
        self.PosX= PosX
        self.PosY= PosY
        self.Largeur= Largeur
        self.Hauteur= Hauteur

        #dessine le brique
        self.Rectangle = self.Canava.create_rectangle(self.PosX, self.PosY, self.PosX + self.Largeur, self.PosY + self.Hauteur, fill = Couleur)

    def Detruire(self):
        # efface la brique de canava 
        self.Canava.delete(self.Rectangle)

    def Touche(self, x, y, rayon):
        # renvoie True si la balle (centre x, y et rayon) touche la brique
        # la balle est entierement a gauche de la brique
        if x + rayon < self.PosX:
            return False
        # entierement a droite
        if x - rayon > self.PosX + self.Largeur:
            return False
        # entierement au dessus
        if y + rayon < self.PosY:
            return False
        # entierement en dessous
        if y - rayon > self.PosY + self.Hauteur:
            return False
        # sinon, elle touche
        return True