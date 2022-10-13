### Get started
- Pour générer un environnement virtuel:
```
 python -m venv name_env
```
- Pour activer l'environnement virtuel:
#### Sur linux
```
source name_env/bin/activate
```
#### Sur windows:
```
.\name_env\Scripts\activate
```
- Pour installer les dépendances dans l'environnement virtuel:
```
 pip install -r requirements.txt
```
- Pour lancer le script sur cette étape:
```
python main.py -i ../images/licorne.png --speed 10
```
- Pour avoir des informations sur les paramètres de la ligne de commande:
```
python main.py -h
```
Il est aussi possible d'utiliser le launch.json avec le debugger vscode pour lancer les script. Les lignes de commande sont y déjà configurées.

# Etape 3 - Simulation d'une impression itérative.

- Nous avonc crée un argument supplémentaire en ligne de commande afin de prendre en compte un paramètre de vitesse de tracage du dessin:
```
cli.add_argument("-s", "--speed", required=False,
                 help="drawing speed in pixels")
```

- Avant de commencer à reproduire les contours de l'image, nous savons que nous devons la dessiner en noir et blanc. Il est donc plus simple pour turtle d'avoir à analyser des informations binaires afin d'éviter les calculs à chaque pixel parcouru. Nous faisons un traitement au préalable en comparant les niveaux de gris. Sur une image en gris comme on a pu le voir, la valeur des pixel va de 0 à 255. En comparant la valeur du niveau de gris de pixel à un seuil défini à 127 on détermine sa valeur binaire pour savoir s'il doit être colorié par turtle -> 255 divisé par 2 = 127.
```
retval, dst = cv.threshold(automatically_edged, 127, 255, cv.THRESH_BINARY)
```

- dst contient ainsi la matrice des pixels de l'image dont la valeur est soit égale à 0 soit égale à 255.


- On initalise ensuite la fenêtre de turtle, et la vitesse de tracage est stockée dans drawing_speed (on cache également le curseur pour des raisons esthétiques):
```
pen = turtle.Turtle()
pen.hideturtle()
screen.tracer(drawing_speed)
```
- On atteint ensuite la double itération:
On parcours l'image de gauche à droite en levant le pinceau pour ne pas tout colorer et en replacant le pinceau au premier pixel à gauche de la fenêtre (taille de la fenêtre parsée dans la cli) ce qui revient à la moitié de la taille de l'image en négatif car la position de départ du curseur est à (0,0) au centre de la fenêtre.

- Ensuite, on regarde dans la matrice binaire dst de l'image le pixel actuellement parcouru dans la boucle (en coordonnées x et y). S'il est égal à 0 donc noir, on pose le crayon et on le colore puis on avance au pixel suivant. Dans le cas contraire (255), on lève le pinceau si celui-ci est posé pour ne pas colorier un pixel qui n'est pas sensé l'être (pixel ne réprésentant pas un contour) puis on avance également au pixel suivant:
```
if dst[pix_height, pix_width] == 0:
    pen.pendown()
    pen.forward(1)
else:
    pen.penup()
    pen.forward(1)
```