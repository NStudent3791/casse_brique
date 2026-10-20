from tkinter import *
import balle
from tkinter import messagebox
import pile
import raquette
import brique

Largeur = 1024
Hauteur = 600

class Jeu:
    def __init__(self):

        self.Fen = Tk()
        self.Fen.title('Jeux casse brique')
        self.Score = 0
        # la partie n'a pas encore commence : la balle ne bouge pas
        self.EnCours = False
        
        self.ElementsFin = []
        self.BoutonFin = None


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
        # vies : une pile de 3 coeurs en haut a droite
        self.Vies = pile.Pile()
        self.CreerVies()


        ZoneInfos = Frame(self.Fen)
        ZoneInfos.pack()

        # texts
        self.AffScore = StringVar()
        self.AffScore.set('Score : 0')
        LabelScore = Label(ZoneInfos, textvariable = self.AffScore, font = ('Arial', 20))
        LabelScore.pack(side = 'left', padx = 20, pady = 5)

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

    def commencer(self):
        # demarre seulement s'il reste des vies et des briques
        if self.EnCours == False and self.Vies.Est_vide() == False and len(self.Briques) > 0:
            self.EnCours = True
            self.BoucleJeu()

    def CreerVies(self):
        # vide la pile, puis empile 3 nouveaux coeurs
        while self.Vies.Est_vide() == False:
            self.Canava.delete(self.Vies.Depiler())
        for i in range(3):
            x = Largeur - 90 + i * 30
            coeur = self.Canava.create_oval(x - 10, 15, x + 10, 35, fill = 'red', outline = 'white')
            self.Vies.Empiler(coeur)

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
        self.NettoyerFin()
        
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
        self.CreerVies()
        self.AfficherInfos()

    def AjouterPoints(self,points):
        self.Score = self.Score + points
        self.AfficherInfos()

    def PerdreVie(self):
        # on depile le coeur du sommet et on l'efface
        coeur = self.Vies.Depiler()
        self.Canava.delete(coeur)
        self.AfficherInfos()

    def RelancerBalle(self):
        self.Canava.delete(self.balle.identifiant)
        self.balle = balle.Balle(self.Canava, self.Fen, Largeur, Hauteur, self.Raquette)

    def CasserBrique(self, BriqueTouchee):
        # casse une brique et le joueur gagne 5 points
        BriqueTouchee.Detruire()
        self.Briques.remove(BriqueTouchee)
        self.AjouterPoints(5)
        # tous les 20 points, la balle accelere
        if self.Score % 20 == 0:
            self.balle.Accelerer()

    
    def NettoyerFin(self):
        for element in self.ElementsFin:
            self.Canava.delete(element)
        self.ElementsFin = []
        if self.BoutonFin is not None:
            self.BoutonFin.destroy()
            self.BoutonFin = None

    def AfficherFin(self, victoire):
        self.NettoyerFin()

        if victoire:
            texte = "VICTOIRE !"
            texte_bouton = "Niveau suivant"
            commande = self.NiveauSuivant
        else:
            texte = "GAME OVER"
            texte_bouton = "Recommencer"
            commande = self.recommencer

        fond = self.Canava.create_rectangle(250, 200, 774, 400, fill="white", outline="white")
        titre = self.Canava.create_text(Largeur / 2, 250, text=texte, fill="black", font=("Arial", 32, "bold"))
        score = self.Canava.create_text(Largeur / 2, 300, text=f"Score : {self.Score}", fill="black", font=("Arial", 18))

        self.BoutonFin = Button(self.Fen, text=texte_bouton, command=commande)
        bouton = self.Canava.create_window(Largeur / 2, 350, window=self.BoutonFin)
        self.ElementsFin = [fond, titre, score, bouton]

    
    def NiveauSuivant(self):
        self.NettoyerFin()

        for b in self.Briques:
            b.Detruire()

        self.CreerMur()
        self.RelancerBalle()

        self.EnCours = True
        self.BoucleJeu()


    def BoucleJeu(self):
        # fait avancer la balle et gere les collisions, 50 fois par seconde
        self.balle.deplacer()

        # La balle est sortie par le bas
        if self.balle.y - self.balle.rayon > Hauteur:
            self.PerdreVie()
            if self.Vies.Est_vide():
                self.EnCours = False
                self.AfficherFin(False)
                return
            self.RelancerBalle()
            self.Boucle = self.Fen.after(20, self.BoucleJeu)
            return

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

        
        # Victoire si toutes les briques sont detruites
        if len(self.Briques) == 0:
            self.EnCours = False
            self.AfficherFin(True)
            return

        
        # tour suivant dans 20 millisecondes
        self.Boucle = self.Fen.after(20, self.BoucleJeu)

    def lancer(self):
        self.Fen.mainloop()