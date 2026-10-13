from tkinter import *
from tkinter import messagebox
import raquette
import brique

Largeur = 1024
Hauteur = 768

class Jeu:
    def __init__(self):

        self.Fen = Tk()
        self.Fen.title('Jeux casse brique')
        self.Score = 0
        self.Vie = 3

        # menu
        menubar = Menu(self.Fen)

        menujeu = Menu(menubar, tearoff = 0)
        menujeu.add_command(label = 'Commencer', command = self.commencer)
        menujeu.add_command(label = 'Quitter', command = self.Fen.destroy)
        menubar.add_cascade(label = 'jeu', menu = menujeu)

        menuaide = Menu(menubar, tearoff = 0)
        menuaide.add_command(label = 'A propos de nous', command = self.Apropos)
        menubar.add_cascade(label = 'Aide', menu = menuaide)

        self.Fen.config(menu = menubar)

        # caneva
        self.Canava = Canvas(self.Fen, width = Largeur, height = Hauteur, bg = 'black')
        self.Canava.pack(padx = 5, pady = 5)
        
        # raquette
        self.Raquette = raquette.Raquette(self.Canava, Largeur, Hauteur)
        # pour detecter les touches du clavier
        self.Fen.bind('<Key>', self.Raquette.Clavier)

        # mur de brique 
        self.Briques = []
        # parametre du mur
        NbBriques = 10
        NbRangees = 5
        Espace = 4
        LargeurBrique = (Largeur - Espace * (NbBriques + 1)) / NbBriques
        HauteurBrique = 25
        Couleur = 'red'
        # largeur calculee pour que les briques remplisset toute la largeur du canavas
        for ligne in range(NbRangees):
            #chaque rangee est placee sous la precedente
            y = 50 + ligne * (HauteurBrique + Espace)
            for i in range(NbBriques):
                # chaque brique est placee a droite de la precedente
                x = Espace + i * (LargeurBrique + Espace)
                NouvelleBrique = brique.Brique(self.Canava, x, y, LargeurBrique, HauteurBrique, Couleur)
                self.Briques.append(NouvelleBrique)


        ZoneInfos = Frame(self.Fen)
        ZoneInfos.pack()

        # texts
        self.AffScore = StringVar()
        self.AffScore.set('Score : 0')
        LabelScore = Label(ZoneInfos, textvariable = self.AffScore, font = ('Arial', 20))
        LabelScore.pack(side = 'left', padx = 20, pady = 5)

        self.AffVie = StringVar()
        self.AffVie.set('Vie : 3')
        LabelVie = Label(ZoneInfos, textvariable = self.AffVie, font = ('Arial', 20))
        LabelVie.pack(side = 'left', padx = 20, pady = 5)

        # boutons
        ZoneBoutons = Frame(self.Fen)
        ZoneBoutons.pack()

        BouttonCommencer = Button(ZoneBoutons, text = 'Commencer')
        BouttonCommencer.pack(side = 'left', padx = 5, pady = 5)

        BouttonQuitter = Button(ZoneBoutons, text = 'Quitter', command = self.Fen.destroy)
        BouttonQuitter.pack(side = 'left', padx = 5, pady = 5)

    def Apropos(self):
        messagebox.showinfo('A propos', 'Développé par Nemo et Léandre ')

    def AfficherInfos(self):
        self.AffScore.set('Score : ' + str (self.Score))
        self.AffVie.set('Vie :' + str(self.Vie))

    def commencer(self):
        self.AffScore.set('Score : 0')
        self.AffVie.set('Vie : 3')

    def AjouterPoints(self,points):
        self.Score = self.Score + points
        self.AfficherInfos()

    def PerdreVie(self):
        self.Vie = self.Vie - 1
        self.AfficherInfos()

    def lancer(self):
        self.Fen.mainloop()

    def CasserBrique(self, BriqueTouchee):
        BriqueTouchee.Detruire()
        self.Briques.remove(BriqueTouchee)
        self.AjouterPoints(5)