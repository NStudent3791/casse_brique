from tkinter import *

def affichage() :
    mafenetre = Tk()
    mafenetre.title('Casse-brique')

    largeur = 800
    hauteur = 600

    frame_infos = Frame(mafenetre)
    frame_caneva = Frame(mafenetre)
    frame_dem_quit = Frame(mafenetre)
    frame_menu = Frame(mafenetre)

    frame_infos.pack(padx = 10, pady = 10)
    frame_caneva.pack(padx=10, pady=10)
    frame_dem_quit.pack(padx=10, pady=10)
    frame_menu.pack(padx=10, pady=10)

    caneva = Canvas(frame_caneva, width = largeur, height = hauteur, bg = 'white')
    caneva.pack()

    boutondem = Button(frame_dem_quit, text = 'Démarrer', command = demarrer)
    boutonquit = Button(frame_dem_quit, text = "Quitter", command = quitter)
    boutondem.pack(side = LEFT, padx=50)
    boutonquit.pack(side = RIGHT, padx=50)

    score = Label(frame_infos, text = 'score : 0')
    vies = Label(frame_infos, text = 'Vies = 3')
    score.pack(side = LEFT, padx=50)
    vies.pack(side = RIGHT, padx=50)

    mafenetre.mainloop()

def demarrer() :
    return True

def quitter() :
    return True
