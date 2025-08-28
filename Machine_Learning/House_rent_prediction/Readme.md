#Implémentation d’un modèle de prédiction des loyers de maison avec Random Forest

Ce projet vise à développer un modèle de Machine Learning supervisé capable de prédire le loyer d’une maison en fonction de ses caractéristiques (surface, nombre de pièces, localisation, etc.).
L’algorithme utilisé est la Random Forest Regressor, qui est un ensemble d’arbres de décision permettant d’améliorer la robustesse et la précision de la prédiction.
Le dataset utilisé se trouve à ce <a href="https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset">lien</a> avec les détails des differentes colonnes contenues.

##Étapes principales du projet :

Exploration et préparation des données

Nettoyage des valeurs manquantes et aberrantes.

Encodage des variables catégorielles (comme la localisation).

Normalisation ou mise à l’échelle des variables numériques si nécessaire.

Feature Engineering

Création ou transformation de certaines variables pour mieux représenter les caractéristiques influençant le prix (par exemple, prix par m²).

Sélection des variables les plus pertinentes pour la prédiction.

Séparation des données

Division en ensembles d’entraînement et de test afin de valider la performance du modèle.

Entraînement du modèle

Utilisation de la Random Forest Regressor pour apprendre la relation entre les caractéristiques des maisons et leur loyer.

Optimisation éventuelle des hyperparamètres (nombre d’arbres, profondeur, etc.) pour améliorer la précision.

Évaluation du modèle

Calcul des métriques d’évaluation (MAE, RMSE, R²).

Analyse des erreurs de prédiction.

Importance des variables (features importance) pour comprendre les facteurs clés qui influencent le loyer.
