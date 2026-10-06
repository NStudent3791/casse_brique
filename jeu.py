from tkinter import *
from tkinter import messagebox
Largeur = 1024
Hauteur = 768

def Apropos():
    messagebox.showinfo('A propos', 'Développé par Nemo et Léandre ')

Fen = Tk()
Fen.title('Jeux casse brique')

menubar = Menu(Fen)
menujeu= Menu(menubar, tearoff= 0)
menujeu.add_command(label= 'Commencer')
menujeu.add_command(label = 'Quitter', command= Fen.destroy)
menubar.add_cascade(label= 'jeu', menu= menujeu)

menuaide= Menu(menubar, tearoff= 0)
menuaide.add_command(label = 'A propos', command= Apropos)
menubar.add_cascade(label= 'Aide', menu= menuaide)

Fen.config(menu = menubar)

Canava = Canvas(Fen, width = Largeur, height= Hauteur, bg = 'black')
Canava.pack(padx = 5, pady = 5)

ZoneInfos = Frame(Fen)
ZoneInfos.pack()

AffScore = StringVar()
AffScore.set('Score : 0')
LabelScore = Label(ZoneInfos, textvariable= AffScore, font = ('Arial', 20))
LabelScore.pack(side = 'left', padx =20, pady =5)

AffVie = StringVar()
AffVie.set('Vie : 3')
LabelVie = Label(ZoneInfos, textvariable= AffVie, font = ('Arial', 20))
LabelVie.pack(side = 'left', padx =20, pady =5)

ZoneBoutons = Frame(Fen)
ZoneBoutons.pack()

BouttonCommencer = Button(ZoneBoutons, text = 'Commencer')
BouttonCommencer.pack(side = 'left', padx = 5, pady = 5)
BouttonQuitter = Button(ZoneBoutons, text = 'Quitter', command = Fen.destroy)
BouttonQuitter.pack(side = 'left', padx = 5, pady = 5)

Fen.mainloop()