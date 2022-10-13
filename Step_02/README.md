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
python main.py -i ../images/lion.jpg -b gaussian -k 3
```
- Pour avoir des informations sur les paramètres de la ligne de commande:
```
python main.py -h
```
Il est aussi possible d'utiliser le launch.json avec le debugger vscode pour lancer les script. Les lignes de commande sont y déjà configurées.

# Etape 2 - Filtres

- Le but de cette étape est de faire un floutage de l'image avant le cunny edge detection. Dans le principe , le floutage est sensé réduire les détails sans éliminer le contraste dans les zones de contours.

- Nous avons intégré deux paramètres supplémentaires dans la ligne de commande du programme pour séléctionner le type de floutage à appliquer: linéaire,médian ou gaussian.

```
cli.add_argument("-b", "--blur", type=blur, choices=list(blur), required=False,
                 help="Blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")
```

- L'unité de mesure du floutage, qui détermine son intensité, aussi appelé kernel est le second paramètre de la ligne de commande que nous implémentons sur cette étape:
```
cli.add_argument("-k", "--kernel", required=False,
                 help="kernel level of blurring")

```
- Le kernel est un masque qui modifie la valeur des pixels sur la base de la valeur des pixels alentours. Les pixels autour du pixel central sont appelés les "pixels voisins". Lorsque le masque se déplace sur l'image pixel par pixel, la valeur du pixel central est ainsi modifiée en fonction de la valeur des pixels voisins. (voir image kernel.png) Comme on peut le voir sur l'image la taille du masque est determinée par les valeurs du kernel en ligne de commande. Plus le kernel est grand, plus le pixel central a de pixels voisins pris en compte lors du calcul et inversement ce qui impacte le résultat final.

![Alt text](fig1.png?raw=true "Masque")

![Alt text](fig2.png?raw=true "Calcul convolution")

- L'image est floutée en fonction du choix effectué en ligne de commande, son information (matrice de pixels) est stockée dans la variable blurred pour le reste du traitement de détection des bords et est affichée à l'écran:
```
cv.imshow("Canny Edge Detection", blurred)
```
![Alt text](res1.png?raw=true "Image normale et image floutée par un filtre gaussien kernel de taille 3")

- Par défaut, l'algorithme Canny applique un floutage gaussian à l'image d'entrée dans l'objectif d'en réduire le bruit.

- En fin de compte, quel que soit le flou employé, le résultat est relativement similaire sur les images que nous avons utilisées. En revanche, nous avons estimé qu'un kernel de 3 était le plus fiable pour le calcul de contours de bords.

- Resultat de cunny edge detection : 
![Alt text](res2.png?raw=true "Cunny edge detection")

