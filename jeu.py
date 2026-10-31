from tkinter import *
import random
import balle
from tkinter import messagebox
import pile
import raquette
import brique
import winsound
import os

Largeur = 1024
Hauteur = 600

class Jeu:
    def __init__(self):

        self.Fen = Tk()
        self.Fen.title('Jeux casse brique')
        self.Score = 0

        # Gestion des bonus
        self.FileBonus = []
        self.NbBriquesDetruites = 0
        self.DelaiBonus = False
        self.ElementsBonus = []
        self.TempsRestant = 0
        self.TimerBonus = None

        # la partie n'a pas encore commence : la balle ne bouge pas
        self.EnCours = False
        
        self.ElementsFin = []
        self.BoutonFin = None

        #vitesse
        self.Niveau = 1
        self.VitesseBase = 8
        self.NbBriquesNiveau = 0

        # menu
        menubar = Menu(self.Fen)

        menujeu = Menu(menubar, tearoff = 0)
        menujeu.add_command(label = 'Commencer', command = self.commencer)
        menujeu.add_command(label = 'Recommencer', command = self.recommencer)
        menujeu.add_command(label = 'Quitter', command = self.Quitter)
        menubar.add_cascade(label = 'jeu', menu = menujeu)

        menuaide = Menu(menubar, tearoff = 0)
        menuaide.add_command(label = 'A propos de nous', command = self.Apropos)
        menubar.add_cascade(label = 'Aide', menu = menuaide)

        self.Fen.config(menu = menubar)

        # caneva
        self.Canava = Canvas(self.Fen, width=Largeur, height=Hauteur, bg="#101426", highlightthickness=0)
        self.Canava.pack(padx = 5, pady = 5)
        self.FondJeu()
        
        # raquette
        self.Raquette = raquette.Raquette(self.Canava, Largeur, Hauteur)
        # pour detecter les touches du clavier
        self.Fen.bind('<Key>', self.Raquette.Clavier)

        #bonus
        self.Fen.bind('<space>', self.UtiliserBonus)

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

        self.AffNiveau = StringVar()
        self.AffNiveau.set("Niveau : 1")

        LabelNiveau = Label(ZoneInfos, textvariable=self.AffNiveau, font=('Arial', 16, 'bold'), fg="#2979FF")

        LabelNiveau.pack(side='left', padx=20, pady=5)

        self.AffTimerBonus = StringVar()
        self.AffTimerBonus.set("")

        LabelTimerBonus = Label(ZoneInfos, textvariable=self.AffTimerBonus, font=('Arial', 12))
        LabelTimerBonus.pack(side='left', padx=20, pady=5)

        self.TempsRestantBonus = 0
        self.TimerBonus = None

        # boutons
        ZoneBoutons = Frame(self.Fen)
        ZoneBoutons.pack()
        self.BoutonMusique = Button(ZoneBoutons, text="Musique : OFF", command=self.BasculerMusique)

        self.BoutonMusique.pack(side='left', padx=5, pady=5)

        #balle
        self.balle = balle.Balle(self.Canava, self.Fen, Largeur, Hauteur, self.Raquette, self.VitesseBase)
        BouttonCommencer = Button(ZoneBoutons, text = 'Commencer', command = self.commencer)
        BouttonCommencer.pack(side = 'left', padx = 5, pady = 5)

        BouttonRecommencer = Button(ZoneBoutons, text = 'Recommencer', command = self.recommencer)
        BouttonRecommencer.pack(side = 'left', padx = 5, pady = 5)

        BouttonQuitter = Button(ZoneBoutons, text = 'Quitter', command = self.Quitter)
        BouttonQuitter.pack(side = 'left', padx = 5, pady = 5)

        #musique
        self.FichierMusique = os.path.join(os.path.dirname(__file__), "masterpepemusic.wav")

        self.MusiqueActive = False

    def Quitter(self):

        if self.MusiqueActive:
            winsound.PlaySound(None, winsound.SND_PURGE)

        self.Fen.destroy()

    def BasculerMusique(self):

        if self.MusiqueActive:

            # Arrête la musique
            winsound.PlaySound(None, winsound.SND_PURGE)

            self.MusiqueActive = False
            self.BoutonMusique.config(text="Musique : OFF")

        else:

            # Vérifie que le fichier existe
            if not os.path.exists(self.FichierMusique):
                messagebox.showwarning("Musique", "Le fichier musique.wav est introuvable.")
                return

            try:
                # Lance la musique en boucle
                winsound.PlaySound(self.FichierMusique, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

                self.MusiqueActive = True
                self.BoutonMusique.config(text="Musique : ON")

            except RuntimeError:
                messagebox.showwarning("Musique", "Impossible de lire ce fichier audio.")

    def FondJeu(self):

    # Petites étoiles dans le fond
        for i in range(100):

            x = random.randint(0, Largeur)
            y = random.randint(0, Hauteur)

            self.Canava.create_oval(x, y, x+2, y+2, fill="#39415F", outline="")

    # Bordure du terrain
        self.Canava.create_rectangle(2, 2, Largeur-2, Hauteur-2, outline="#39415F", width=2)
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
        self.ActualiserVies(3)

    def CreerMur(self):
        # cree le mur de briques et range toutes les briques dans une liste
        self.Briques = []
        # parametre du mur
        NbBriques = 10
        NbRangees = 5
        Espace = 4
        LargeurBrique = (Largeur - Espace * (NbBriques + 1)) / NbBriques
        HauteurBrique = 25
        Couleurs = [ "#FF4560", "#FF8C42", "#FFD166", "#06D6A0", "#00B4D8"]
        # largeur calculee pour que les briques remplissent toute la largeur du canevas
        for ligne in range(NbRangees):
            # chaque rangee est placee sous la precedente
            y = 50 + ligne * (HauteurBrique + Espace)
            for i in range(NbBriques):
                # chaque brique est placee a droite de la precedente
                x = Espace + i * (LargeurBrique + Espace)
                Couleur = Couleurs[ligne]

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

        #on réinitialise les paramètres de difficulté
        self.Niveau = 1
        self.AffNiveau.set("Niveau : 1")
        self.VitesseBase = 8
        self.NbBriquesNiveau = 0
        
        #on efface la balle et on en cree une nouvelle (au centre, vitesse de depart)
        self.Canava.delete(self.balle.identifiant)
        self.balle = balle.Balle(self.Canava, self.Fen, Largeur, Hauteur, self.Raquette)

        #score et vies remis a zero
        self.Score = 0
        self.CreerVies()
        self.AfficherInfos()
        self.FileBonus = []
        self.NbBriquesDetruites = 0
        if self.TimerBonus is not None:
            self.Fen.after_cancel(self.TimerBonus)
            self.TimerBonus = None

        self.DelaiBonus = False
        self.TempsRestantBonus = 0
        self.AffTimerBonus.set("")
        self.AfficherBonus()

    def AjouterPoints(self,points):
        self.Score = self.Score + points
        self.AfficherInfos()

    def PerdreVie(self):
        nombre = self.Vies.nb_elements - 1

        self.ActualiserVies(nombre)
        self.AfficherInfos()

    def ActualiserVies(self, nombre):

        # Efface les anciens coeurs
        while not self.Vies.Est_vide():
            self.Canava.delete(self.Vies.Depiler())

        # Recrée les coeurs en fonction du nombre de vies
        for i in range(nombre):

            x = Largeur - 30 * nombre + i * 30

            coeur = self.Canava.create_oval(x - 10, 15, x + 10, 35, fill='red', outline='white')

            self.Vies.Empiler(coeur)

    def RelancerBalle(self):
        self.Canava.delete(self.balle.identifiant)
        self.balle = balle.Balle(self.Canava, self.Fen, Largeur, Hauteur, self.Raquette, self.VitesseBase)

    def CasserBrique(self, BriqueTouchee):
    # Détruit la brique
        BriqueTouchee.Detruire()
        self.Briques.remove(BriqueTouchee)

    # Ajoute les points
        self.AjouterPoints(5)

    # Accélération de la balle
        self.NbBriquesNiveau += 1

        if self.NbBriquesNiveau % 4 == 0:
            self.balle.Accelerer()

    # Compte les briques détruites
        self.NbBriquesDetruites += 1

    # Tous les 20 blocs, attribue un bonus
        if self.NbBriquesDetruites % 20 == 0:
            self.AttribuerBonus()

    def AttribuerBonus(self):

        # Liste des bonus possibles
        BonusPossibles = ["vie", "points", "briques"]

        # Choisit un bonus au hasard
        bonus = random.choice(BonusPossibles)

        # Vérifie que la file n'est pas pleine
        if len(self.FileBonus) < 3:

            # Ajoute le bonus à la fin de la file
            self.FileBonus.append(bonus)

            # Actualise l'affichage
            self.AfficherBonus()

    def AfficherBonus(self):

    # Efface les anciens dessins
        for element in self.ElementsBonus:
            self.Canava.delete(element)

        self.ElementsBonus = []

        # Correspondance entre bonus et affichage
        Symboles = {"vie": "+1", "points": "100", "briques": "5X"}

        # Affiche les bonus dans l'ordre de la file
        for i, bonus in enumerate(self.FileBonus):

            x = 35 + i * 65
            y = 25 

            rectangle = self.Canava.create_rectangle(x - 25, y - 20, x + 25, y + 20, fill="white")

            texte = self.Canava.create_text(x, y, text=Symboles[bonus], fill="black", font=("Arial", 12, "bold"))

            self.ElementsBonus.append(rectangle)
            self.ElementsBonus.append(texte)

    def UtiliserBonus(self, event):

        # Vérifie que la file contient un bonus
        if len(self.FileBonus) == 0:
            return

        # Vérifie le délai de 10 secondes
        if self.DelaiBonus:
            return

        # Récupère le premier bonus de la file
        bonus = self.FileBonus.pop(0)

        # Actualise l'affichage
        self.AfficherBonus()

        # Active le délai
        self.DemarrerTimerBonus()

        # Active le bonus correspondant
        if bonus == "vie":
            self.AjouterVie()

        elif bonus == "points":
            self.AjouterPoints(100)

        elif bonus == "briques":
            self.DetruireCinqBriques()

    def DemarrerTimerBonus(self):

        self.DelaiBonus = True
        self.TempsRestantBonus = 10
        self.AfficherTimerBonus()


    def AfficherTimerBonus(self):

        if self.TempsRestantBonus > 0:
            self.AffTimerBonus.set("Il reste " + str(self.TempsRestantBonus) + " s")
            self.TempsRestantBonus -= 1
            self.TimerBonus = self.Fen.after(1000, self.AfficherTimerBonus)

        else:

            self.DelaiBonus = False
            self.AffTimerBonus.set("")
            self.TimerBonus = None

    def DetruireCinqBriques(self):

        # Nombre de briques à détruire
        nombre = min(5, len(self.Briques))

        # Sélectionne des briques au hasard
        selection = random.sample(self.Briques, nombre)

        # Détruit chaque brique sélectionnée
        for b in selection:
            self.CasserBrique(b)

    def AjouterVie(self):

        nombre = self.Vies.nb_elements + 1
        self.ActualiserVies(nombre)
        
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

        self.Niveau += 1
        self.VitesseBase += 1
        self.NbBriquesNiveau = 0
        self.AffNiveau.set("Niveau : " + str(self.Niveau))

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