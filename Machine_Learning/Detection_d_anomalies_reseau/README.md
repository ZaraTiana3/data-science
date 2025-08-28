## Implementation-de-modele-de-detection-d-anomalies-reseau

## Description 
<p>Ceci concerne l'implementation de modele de detection d'anomalies reseau par utilisation du modele de deep learning autoencodeur.

<p>Dans le notebook "Implementation-de-modele-de-detection-d'anomalies-reseau", on retrouve les differentes transformations appliquées au dataset avant d'effectuer l'implementation du modele ainsi que l'évaluation du modèle. Les modeles et differents parametres utilisés dans les transfomations, le scaling et l'implementation du modele sont ensuite sauvegardés et  stockés dans le dossier "Modele_et_differents_parametres". </p>

<p>Dans le notebook "Test-anomaly-detection-model", on retrouve la prédiction de quelques activités du réseau avec leurs  transformations en  utilisant  les différents paramètres.</p> 

### Dataset
-  Telechargeable  à   ce  <a href="https://www.kaggle.com/datasets/tahianasoa/nfu-dataset">lien</a> si sur Kaggle ou <a href="https://rdm.uq.edu.au/files/e2412450-ef9c-11ed-827d-e762de186848">ici</a> . Ce sont des données  du jeu de données NF-UQ-NIDS-v2 au format Netflow.
-   Les détails sur les colonnes du dataset sont alors: les adresses IP sources et de destination et leurs ports correspondants, les protocoles de la couche 4, les cumulatifs du TCP_FLAGS, les quantités d’octets entrants et sortants, le nombre de paquets entrants et sortants et les protocoles de la couche 7 

### Dataset
- Utilisé : [Face Mask Dataset](https://www.kaggle.com/datasets/omkargurav/face-mask-dataset)  
- Contient des images de visages **avec masque** et **sans masque**.  

### Étapes principales du projet  
1. **Prétraitement des images** :  
   - Redimensionnement (224x224), normalisation et encodage en tenseurs  
   - Génération des labels correspondants (masque / sans masque)  
2. **Séparation des données** :  
   - Train/Test split (80% entraînement, 20% test)  
3. **Augmentation des données** :  
   - Utilisation de `ImageDataGenerator` (rotation, translation, zoom, luminosité) pour améliorer la robustesse du modèle  
4. **Entraînement du modèle** :  
   - Réseau **VGG16** (transfer learning) adapté au dataset  
5. **Évaluation** :  
   - Prédiction sur le jeu de test  
6. **Sauvegarde du modèle** :  
   - Export du modèle entraîné pour une réutilisation future  

## 🎥 Détection en temps réel avec la webcam

En plus de l’entraînement et de l’évaluation du modèle, le projet inclut un script `detect_mask.py` permettant de tester la détection du port de masque en temps réel via la webcam de l’ordinateur.  

### Utilisation
Après sauvegarde du  modèle entraîné (`mask_detector_model.h5`), suivre ces étapes suivantes: 

#### Installer les dépendances Python
Crée un environnement virtuel puis installe les librairies :
```bash
python -m venv venv
source venv/bin/activate   # sous Linux/Mac
venv\Scripts\activate      # sous Windows
pip install -r requirements.txt
```

#### Lancer l’application
```bash
python detect_mask.py
```


