class Raquette:
    def __init__(self, Canava, LargeurCanevas, HauteurCanevas):
        self.Canava = Canava
        self.LargeurCanevas = LargeurCanevas

        # dimensions de la raquette
        self.Largeur = 120
        self.Hauteur = 15

        self.PosX = (LargeurCanevas - self.Largeur) / 2
        self.PosY = HauteurCanevas - 40

        # dessin de la raquette
        self.Rectangle = self.Canava.create_rectangle(self.PosX, self.PosY, self.PosX + self.Largeur, self.PosY + self.Hauteur, fill = 'white')

    def Clavier(self, event):
        touche = event.keysym
        if touche == 'Left':
            self.PosX = self.PosX - 20
        if touche == 'Right':
            self.PosX = self.PosX + 20
        ## bloque a gauche
        if self.PosX < 0:
            self.PosX = 0
        ## bloque a droite
        if self.PosX > self.LargeurCanevas - self.Largeur:
            self.PosX = self.LargeurCanevas - self.Largeur
        # changement de coordonnées si bouton appuye
        self.Canava.coords(self.Rectangle, self.PosX, self.PosY, self.PosX + self.Largeur, self.PosY + self.Hauteur)