from tkinter import *
import balle
from tkinter import messagebox

import raquette
import brique

Largeur = 1024
Hauteur = 600

class Jeu:
    def __init__(self):

        self.Fen = Tk()
        self.Fen.title('Jeux casse brique')
        self.Score = 0
        self.Vie = 3
        # la partie n'a pas encore commence : la balle ne bouge pas
        self.EnCours = False

        # menu
        menubar = Menu(self.Fen)

        menujeu = Menu(menubar, tearoff = 0)
        menujeu.add_command(label = 'Commencer', command = self.commencer)
        menujeu.add_command(label = 'Recommencer', command = self.recommencer)
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

        # mur de briques
        self.CreerMur()


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

        #balle
        self.balle = balle.Balle(self.Canava, self.Fen, Largeur, Hauteur, self.Raquette)

        BouttonCommencer = Button(ZoneBoutons, text = 'Commencer', command = self.commencer)
        BouttonCommencer.pack(side = 'left', padx = 5, pady = 5)

        BouttonRecommencer = Button(ZoneBoutons, text = 'Recommencer', command = self.recommencer)
        BouttonRecommencer.pack(side = 'left', padx = 5, pady = 5)

        BouttonQuitter = Button(ZoneBoutons, text = 'Quitter', command = self.Fen.destroy)
        BouttonQuitter.pack(side = 'left', padx = 5, pady = 5)

    def Apropos(self):
        messagebox.showinfo('A propos', 'Développé par Nemo et Léandre ')

    def AfficherInfos(self):
        self.AffScore.set('Score : ' + str (self.Score))
        self.AffVie.set('Vie : ' + str(self.Vie))

    def commencer(self):
        # demarre la partie, seulement si elle n'est pas deja en cours
        if self.EnCours == False:
            self.EnCours = True
            self.Score = 0
            self.Vie = 3
            self.AfficherInfos()
            # demarrage de la boucle du jeu
            self.BoucleJeu()

    def CreerMur(self):
        # cree le mur de briques et range toutes les briques dans une liste
        self.Briques = []
        # parametre du mur
        NbBriques = 10
        NbRangees = 5
        Espace = 4
        LargeurBrique = (Largeur - Espace * (NbBriques + 1)) / NbBriques
        HauteurBrique = 25
        Couleur = 'red'
        # largeur calculee pour que les briques remplissent toute la largeur du canevas
        for ligne in range(NbRangees):
            # chaque rangee est placee sous la precedente
            y = 50 + ligne * (HauteurBrique + Espace)
            for i in range(NbBriques):
                # chaque brique est placee a droite de la precedente
                x = Espace + i * (LargeurBrique + Espace)
                NouvelleBrique = brique.Brique(self.Canava, x, y, LargeurBrique, HauteurBrique, Couleur)
                self.Briques.append(NouvelleBrique)

    def recommencer(self):
        # remet le jeu comme au lancement
        #on arrete la boucle du jeu si elle tourne
        if self.EnCours == True:
            self.Fen.after_cancel(self.Boucle)
            self.EnCours = False

        # on efface les briques restantes et on reconstruit le mur complet
        for b in self.Briques:
            b.Detruire()
        self.CreerMur()

        #on efface la balle et on en cree une nouvelle (au centre, vitesse de depart)
        self.Canava.delete(self.balle.identifiant)
        self.balle = balle.Balle(self.Canava, self.Fen, Largeur, Hauteur, self.Raquette)

        #score et vies remis a zero
        self.Score = 0
        self.Vie = 3
        self.AfficherInfos()

    def AjouterPoints(self,points):
        self.Score = self.Score + points
        self.AfficherInfos()

    def PerdreVie(self):
        self.Vie = self.Vie - 1
        self.AfficherInfos()

    def CasserBrique(self, BriqueTouchee):
        # casse une brique et le joueur gagne 5 points
        BriqueTouchee.Detruire()
        self.Briques.remove(BriqueTouchee)
        self.AjouterPoints(5)
        # tous les 25 points (donc toutes les 5 briques), la balle accelere
        if self.Score % 25 == 0:
            self.balle.Accelerer()

    def BoucleJeu(self):
        # fait avancer la balle et gere les collisions, 50 fois par seconde
        self.balle.deplacer()

        # rebond sur la raquette
        if self.balle.dy > 0 and self.Raquette.Touche(self.balle.x, self.balle.y, self.balle.rayon):
            self.balle.dy = -self.balle.dy

        # collision avec les briques
        for b in self.Briques:
            if b.Touche(self.balle.x, self.balle.y, self.balle.rayon):
                # rebond par le dessus ou dessous ou par le cote
                if b.PosX <= self.balle.x <= b.PosX + b.Largeur:
                    self.balle.dy = -self.balle.dy
                else:
                    self.balle.dx = -self.balle.dx
                self.CasserBrique(b)
                break

        # tour suivant dans 20 millisecondes
        # (on garde le numero de ce rendez-vous pour pouvoir l'annuler)
        self.Boucle = self.Fen.after(20, self.BoucleJeu)

    def lancer(self):
        self.Fen.mainloop()