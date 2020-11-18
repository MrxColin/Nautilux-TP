# Nautilux-TP


## Installation backend

Dépendances python :flask, flask_cors, datetime, json

Avec python 2.7 :
Pour lancer le backend : python api.py

## Installation frontend

npm install

Pour lancer le frontend : http-server -o

## Documentation

La vue principale comporte la liste des interventions sous forme de tableau
Une intervention est désigné par Un libellé, le nom de l'intervenant, la description, la date de l'intervention et le lieu. Il possède également un id unique.
Le statut de l'intervention fonctionne avec un code couleur : Gris = Brouillon, Jaune = Validé et Vert=Terminé
On peut éditer et supprimer une intervention via les deux boutons au bout de chaque ligne sur le tableau.

Après l'ajout d'une intervention, on peut soit recreer une nouvelle intervention, soit rebasculer sur la vue avec les tickets via le bouton "Visualiser les interventions"