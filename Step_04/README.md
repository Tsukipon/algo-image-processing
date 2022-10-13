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

# Etape 4 - Simulation d'un dessin à main levé.

Le but de cette étape est de réaliser un algorithme permettant de dessiner une image de manière réaliste.

- Pour être très concis on peut mimer grossièrement ce "réalisme" assez facilement en respectant deux règles qui seront le fondement du fonctionnement des algorithmes proposés:
- - Tant qu'il existe un pixel voisin, on trace un segment entre les deux pixels. Nous verrons plus tard ce que veut dire pixel voisin.
- - S'il n'y a aucun pixel voisin, alors chercher le pixel le plus proche.

- Nous allons maintenant expliquer chacune des deux règles.
- Par pixel voisin, nous entendons pixel adjacent comme montré dans le dessin suivant :

![Alt text](pixelvoisin.png?raw=true "Pixel et ses voisins")

En comptabilisant les pixels en diagonale, un pixel donné peut avoir au maximum 8 voisins ( s'il est complètement entouré ) ou au minimum 0 voisins s'il est isolé
En terme de distances, les pixels adjacent (nord est ouest sud) ont une distance de 1 et les pixels en diagonal ont une distance euclidienne de sqrt(2) (environ 1.41...) ont peut donc définir un pixel voisin comme étant un pixel de distance inférieur à 1.42 par rapport au pixel de référence.

Pour rendre réaliste l'algorithme, il est important qu'il persiste dans le tracé de lignes continus. Une ligne continue est une série de pixels voisins.
Les pixels déjà traités ne doivent plus compter parmi les voisins potentiel car nous risquerions de faire une boucle infinie.
Une fois que nous ne trouvons plus de pixels voisin, nous commençons la recherche du pixel non traité le plus proche, de tel sorte à donner l'impression que le tracé se concentre dans une région particulière au lieu de sauter d'un bout à l'autre de l'image comme une machine.

- Nous avons mis en place deux algorithmes dont le fonctionnement est sensiblement similaire ; Nous traçons un segment vers un voisin tant qu'il y'en a , sinon nous cherchons le pixel le plus proche.

- Le premier algorithme (drawerBasic) est basique mais accompli son devoir remarquablement bien. Nous commençons par récupérer tous les pixels devant être traité ( les pixels noirs ). Pour chaque pixel restant, nous cherchons un pixel voisin parmi les pixels restants, s'il y'en a un nous traçons un segment et nous retirons le pixel actuel de la liste des pixels non traités. S'il n'y a pas de pixel voisin, nous cherchons le pixel le plus proche ( recherche exaustive sur l'ensemble de la liste des pixels restants).

- La fonction qui s'occupe de chercher un voisin s'occupe également de trouver le pixel le plus proche en un seul parcourt de la liste
```python
def getClosestFriend(coord,coords):
    minimum = np.Infinity
    for i,val in enumerate(coords):
        dist = math.dist(coord,val)
        if dist< 1.42:
            return coords.pop(i)
        if dist < minimum:
            minimum = dist
            closest = i
    return coords.pop(closest)
```
En entrée nous avons une paire de coordonnée et la liste de tous les autres points.
Si on trouve un pixel voisin, on arrete le parcourt et on le renvoit
Sinon on continue le parcourt en cherchant le point le plus proche.

- Il y'a quelques points intéréssants à noter pour ce premier algorithme: 
- - Lors de la recherche d'un pixel voisin, nous arrêtons la recherche au premier voisin trouvé (pas besoin de trouver les autres). Cela réduit grandement le temps de cherche de voisins.
- - La liste initial de tous les pixels est construite en balayant l'image. Cela a pour effet de construire une liste où les pixels sont assez bien triés ( on retrouve les pixels proches à proximité dans la liste). La recherche de pixel voisin se fait donc assez rapidement
- - La liste des pixels à traiter se réduit à chaque itération. Le problème est donc de moins en moins complexe.


- On voit bien que le principal défaut de la méthode se trouve dans la recherche de voisin et du pixel le plus proche.

- Pour palier à ce problème on peut utilser une structure de données qu'on appelle la KDtree, un arbre binaire qui permet de trouver rapidement le pixel le plus proche. Une version simplifié du fonctionnement : 
- - A la racine , placer un point ( dans notre cas une paire de coordonnée ) de tel sorte à ce que la moitié des autres points aient une coordonnée y inférieur et les placer dans le sous arbre gauche, l'autres moitié des points ayant une coordonnée y supérieur dans le sous arbre droit.
Dans le niveau inférieur continuer sur le même principe en divisant selon la coordonnée x. On continue ainsi de suite en alternant une division selon l'axe x et y ( on peut aussi commencer par une division selon l'axe x).

- Le deuxième algorithme fonctionne donc ainsi:
- - On commence par récupérer la liste des pixels à traiter tout comme dans l'algorithme 1.
- - On construit un KDTree à partir de cette liste.
```python
tree = KDTree(coords) 
```
- - On choisit un pixel au hasard ( le premier )
```python
current = 0
explored_ind = [0]
```
- - On requête l'arbre pour récupérer les voisins ( pixels ayant une distance inférieur à 1.42 )
```python
ind= tree.query_radius([coords[current]], r=1.42)
ind = [value for value in ind if value not in explored_ind]
```
- - Si la requête renvoit au moins un pixel non traité on trace un segment vers un pixel voisin.
```python
if len(ind) >= 1:
    pen.pendown()
    pen.goto(coords[ind[0]][0] - (width/2), coords[ind[0]][1]- (height/2))
    pen.penup()
    explored_ind.append(ind[0])
    current = ind[0]
```
- - Si la requête ne renvoit pas de nouveau pixel voisin ( nous sommes dans un cul-de-sac) ,on supprime de la liste tout les pixels traités jusqu'ici.
```python
tmp=coords[current]
coords = [coords[i] for i in range(0,len(coords)) if i not in explored_ind]
explored_ind = []
```
- -  on construit un nouvel arbre sur le sous-ensemble restant puis on requête l'arbre pour avoir le pixel le plus proche
```python
tree = KDTree(coords)
dist,i = tree.query([tmp],k=2)
i = i.flatten()
current = i[1]
```

- - On continue ainsi jusqu'à ce qu'il n'y ait plus de pixel à traiter.


- Le défaut de cet algorithme se trouve clairement dans la reconstruction de l'arbre.
- Sur l'image de la licorne, l'algorithme reconstruit l'arbre KDTree dans environ 10% des itérations. En comparant le temps d'execution des deux algorithmes, le premier algorithme finit de dessiner l'image en environ 28 secondes , contre 37 secondes pour l'algorithme utilisant les KDtree.
- La question est donc de savoir, peut-on éviter de reconstruire l'arbre ?
- La réponse est oui MAIS. Si l'on construit l'arbre une seule fois au début et qu'on cherche à l'exploiter tout du long, on se heurte à un problème de taille. Peu à peu l'arbre devient pollué par les pixels que l'on a déjà traité. Il faudra donc vérifier très régulièrement que les pixels que l'on trouve ne font pas parti des pixels que l'on a déjà traité ( auquel cas nous ferons une boucle infinie). Au fur et à mesure que l'on avance, on perd énormement de temps à requêter l'arbre, et vérifier que les pixels renvoyé ne sont pas déjà traités.

















