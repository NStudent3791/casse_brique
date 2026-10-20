# Développement d’un jeu : Casse brique pour CPE Lyon
Bînome: **Nemo CHARPENTIER, Leandre GOSSELIN**

Github: *https://github.com/NStudent3791/casse_brique/tree/dev-leandre_gestionparties*

## Pour Lancer le jeu 
Python + tkinter        
Excécuter le fichier **main.py**


## Règles du jeu
- Le but est de détruire toutes les briques
- Le joueur déplace une raquette, pour renvoyer la balle.
- Quand la balle touche une brique, la brique disparaît
- Si la balle tombe en bas de l'écran, la partie est finie.

## Commandes pour le joueur

- Les touches flèches ← et → du clavier déplacent la raquette.
- Le bouton Commencer lance la partie.
- Le bouton Recommencer remet la partie à zéro.
- Le bouton Quitter ferme le jeu.

Les trois boutons sont aussi accessibles depuis la barre de menu, dans le menu « jeu ».


## Réglage par défault
- Canevas de 1024 × 600 pixels au lieu de 1024 × 768 : sur un écran avec une résolution plus petite, la zone du score et les autres informations risquaient de ne pas être visibles
- Mur de 50 briques, 5 rangées de 10
- 3 vies au départ
- La balle accélère tous les 20 points, jusqu'à une vitesse maximale


## Fonctionnalités en plus

- La balle reste figée au lancement et ne part qu'au clic sur Commencer.
- Le bouton Recommencer remet tout le jeu à zéro.
- La balle rebondit aussi sur les côtés de la raquette.

## Organisation des fichiers

Chaque partie du jeu a sa classe dans un fichier à part

- main.py, c'est le fichier à lancer. Il crée le jeu et le démarre
- jeu.py (classe Jeu), la fenêtre, le menu, le score, les vies et les boutons. C'est aussi lui qui crée la raquette, la balle et les briques, et qui fait tourner le jeu
- raquette.py (classe Raquette), la raquette, qu'on déplace avec les flèches
- balle.py (classe Balle), la balle, qui bouge, rebondit sur les murs et sur la raquette, et va de plus en plus vite
- brique.py (classe Brique), une brique, qui disparaît quand la balle la touche
- README.md : ce fichier

## À régler

- Quand la balle arrive pile entre deux briques, elle casse les deux, les traverse, et casse ainsi deux autres briques d'un coup.
- Faire changer la direction de la balle en fonction du mouvement de la raquette, pour éviter que la balle se déplace toujours de la même manière.
