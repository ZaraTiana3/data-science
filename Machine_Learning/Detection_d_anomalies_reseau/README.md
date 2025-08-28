## Implementation-de-modele-de-detection-d-anomalies-reseau

## Description 
Ce projet porte sur la détection d’anomalies réseau à l’aide d’un modèle de deep learning basé sur un autoencodeur.
L’objectif est d’identifier des comportements atypiques dans le trafic réseau qui peuvent correspondre à des intrusions, des attaques ou des activités inhabituelles.
L’approche repose sur l’idée que :
   - l’autoencodeur est entraîné uniquement sur des données normales afin d’apprendre à reconstruire fidèlement leurs caractéristiques.
   - lorsque des données anormales (par ex. un trafic suspect) sont présentées au modèle, celui-ci échoue à les reconstruire correctement, ce qui se traduit par une erreur de reconstruction élevée.
   - cette erreur devient alors un indicateur d’anomalie, permettant de différencier le trafic légitime du trafic potentiellement malveillant.

### Étapes principales du projet
Le notebook "Implementation_de_modele_de_detection_d'anomalies_reseau.ipynb" contient les differentes transformations appliquées au dataset avant d'effectuer l'implementation du modele ainsi que l'évaluation du modèle.
1. **Importation des données** qui correspond au chargement des données réseau nécessaires à l’analyse.
   -  Telechargeable  à   ce  <a href="https://www.kaggle.com/datasets/tahianasoa/nfu-dataset">lien</a> si sur Kaggle ou <a href="https://rdm.uq.edu.au/files/e2412450-ef9c-11ed-827d-e762de186848">ici</a> . Ce sont des données  du jeu de données NF-UQ-NIDS-v2 au format Netflow.
   -   Les détails sur les colonnes du dataset sont alors: les adresses IP sources et de destination et leurs ports correspondants, les protocoles de la couche 4, les cumulatifs du TCP_FLAGS, les quantités d’octets entrants et sortants, le nombre de paquets entrants et sortants et les protocoles de la couche 7 

2. **Feature engineering**
   - Transformation des colonnes en une représentation exploitable par le modèle.
   - Les colonnes numériques (ex. : quantités d’octets entrants) sont utilisées telles quelles.
   - Les colonnes de type object sont encodées avec du target encoding, qui convertit chaque valeur catégorique en une valeur numérique correspondant à la probabilité que cette valeur soit associée à une anomalie.
   
3. **Entraînement du modèle**:
   - D'abord la division des données en données d’entraînement, données de test et données d’anomalies
   - Puis utilisation d’un autoencodeur deep learning pour apprendre la représentation des données normales.

4. **Évaluation du modèle**: Le modèle est évalué successivement sur les données d’entraînement, les données de test, les données d’anomalies
   
5. **Sauvegarde du modèle**: Export du modèle entraîné ainsi que des paramètres de prétraitement et d’entraînement pour une réutilisation future stockés dans le dossier "Modele_et_differents_parametres.


## Test du modèle sauvegardé
<p>Dans le notebook "Test-anomaly-detection-model.ipynb", on retrouve la prédiction de quelques activités du réseau avec leurs  transformations en  utilisant  les différents paramètres.</p> 






















