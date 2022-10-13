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
python main.py -i ../images/lion.jpg
```
- Pour avoir des informations sur les paramètres de la ligne de commande:
```
python main.py -h
```
Il est aussi possible d'utiliser le launch.json avec le debugger vscode pour lancer les script. Les lignes de commande sont y déjà configurées.

# Etape 1 - Pré-traitement de l'image

Tout d'abord, nous avons conçu géré les arguments par ligne de commande avec la librairie argparse qui permet au script de traiter les commandes via cli.

- La première étape dans le traitement d'une image en vue de détecter ses contours consiste à réduire le "bruit" (pixels contenant des valeurs anormales) généralement en appliquant un filtre sur l'image. Simplifier ainsi l'image permet de pourvoir la traiter plus facilement.

- Dans un premier temps, nous convertissons l'image en niveaux de gris, toujours dans un soucis de simplifier la tâche.  L'information apportée par les trois canaux RGB ne sont pas utiles pour la détection de contours et seraient susceptibles de ralentir les algorithmes utilisés plus tard. Une fois l'image en niveau de gris obtenue, les pixels de cette dernière ont une seule valeur comprise entre 0 (noir) et 255 (blanc) au lieu d'un ensemble de trois valeurs.

![Alt text](grayscale.png?raw=true "Pixels d'une image en niveau de gris")
![Alt text](rgb_image.png?raw=true "Pixels d'une image RGB")


```
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```
- Si l'on applique directement l'algorithme Canny en paramétrant les valeurs de seuil manuellement, il est possible d'arriver à un résultat satisfaisant, cependant nous risquons d'avoir une image en sortie avec trop de "bruit" ou alors avec trop peu de contours détéctés au risque de ne pas reconnaitre l'image initiale. De plus, le paramétrage manuel empêche d'avoir une solution généraliste pour traiter un ensemble d'images rapidement sans input utilisateur.

- Afin d'obtenir une détection de contours satisfaisante quelque soit l'image de départ, nous allons calculer la médiane des niveaux de gris de l'image donc de sa matrice de pixels.
http://www.kerrywong.com/2009/05/07/canny-edge-detection-auto-thresholding/
Cette article justifie la méhode de seuillage automatique pour l'algorithme canny edge detection.

- Il faut savoir qu'en général , l'histogramme d'une image a une forme gaussienne

![Alt text](hist1.png?raw=true "Histogramme d'une image normale")

- Cette histogramme représente la répartition des pixels selon la valeur en niveau de gris.
L'essentiel de l'information représentant une image se situe à [μ – σ=0.33, μ + 0.33] autour de la moyenne μ
Dans un cas classique, la moyenne et la médiane sont à peu près égales.
Le problème se situe plutot dans les images non harmonisées , ou le profil de l'image ne se représente pas par une simple gaussienne exemple :

![Alt text](hist2.png?raw=true "Histogramme d'une image non harmonisée")

- Dans ce cas la médiane et la moyenne sont très différentes, et la médiane obtient de bien meilleurs résultats.
C'est pour cette raison que nous avons choisi d'utiliser la médiane et non la moyenne pour le seuillage automatique.






```
computed_median = np.median(gray)
```

- A partir de cette médiane, nous utilisons une technique de segmentation de l'image en définissant un seuil max et un seuil min pour l'algorithme Canny. On cherche à determiner quels pixels sont situés dans l'intervalle construit par ces deux seuils.

 ```
lower_treshold = (1.0 - 0.33) * computed_median
upper_treshold = int(min(255, (1.0 + 0.33) * computed_median))
 ```
- On applique ensuite l'algorithme de Canny sur l'image en prenant en compte les deux seuils.
```
automatically_edged = ~cv.Canny(img, lower_treshold, upper_treshold)
```

- L'opérateur tild inverse la valeur de chaque bit individuel qui constitue l'image ce qui visuellement inverse la couleur de l'image pour obtenir ce qui était demandé. Le résultat est satisfaisant de notre point de vue sur plusieurs images différentes.
```
np.hstack([tight,wide,automatically_edged])
```
- A gauche figure l'image traitée par Canny avec des seuils de gris faible,
au centre des seuils de gris élevés et à droite nous avons l'image traitée par Canny traitée avec la médiane des niveaux de gris.
![Alt text](result.png?raw=true "Images résultats ( lowtreshold, hightreshold, auto-treshold)")