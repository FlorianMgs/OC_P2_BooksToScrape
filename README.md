# OpenClassrooms: Projet 2: Books To Scrape

Ce script permet de récupérer les informations de tout les produits sur le site http://books.toscrape.com/.
Ces informations sont les suivantes:
 - URL du livre
 - Universal Product Code (upc)
 - Titre du livre
 - Prix, taxe incluse
 - Prix, taxe exclue
 - Quantité disponible
 - Description du produit
 - Catégorie
 - Rating
 - URL de l'image

Ces données sont ensuite classées par catégories et inscrites dans un fichier CSV correspondant. En plus de cela, les images des livres sont téléchargées.
Les données sont générées à la racine du projet suivant cette arborescence:
```
|-- data/
    |-- categorie1/
        |-- categorie1.csv
        |-- imgs/
            |-- img1.jpg
            |-- img2.jpg
            ...etc
    |-- categorie2/
    ...etc
```
# Installation:
Commencez tout d'abord par installer Python.
Lancez ensuite la console, placez vous dans le dossier de votre choix puis créez un environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
env/scripts/activate.bat
```
Linux:
```
source env/bin/activate
```
Clonez ensuite ce repository:
```
git clone https://github.com/FlorianMgs/OC_P2_BooksToScrape.git
```
Il ne reste plus qu'à installer les packages requis:
```
pip install -r requirements.txt
```
Vous pouvez enfin lancer le script:
```
python main.py
```
