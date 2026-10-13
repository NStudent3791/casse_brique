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